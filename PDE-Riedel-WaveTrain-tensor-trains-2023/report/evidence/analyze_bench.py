"""
Parse the raw wave_train TISE log to extract per-state energies (which is the
canonical WaveTrain output), pair them against the analytic tight-binding
spectrum, and produce a clean per-N table.

Log lines look like:
    TISE (als): state = 2, energy = 0.090025, CPU = 0.38 sec
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import numpy as np

LOG = Path(__file__).parent / 'run_tise_bench.log'
OUT = Path(__file__).parent.parent / 'report' / 'evidence' / 'tise_bench_final.json'

# Section boundaries (in log): "N= 4:", "N= 6:", ... and the primary "=== Primary" preceding "=== Scaling"

state_re = re.compile(r"TISE \(als\): state = (\d+), energy = ([-0-9.eE+]+), CPU = ([\d.]+) sec")
wall_re = re.compile(r"N=\s*(\d+): wall=([\d.]+)s")
primary_re = re.compile(r"=== Primary benchmark: N=6")
scale_re = re.compile(r"=== Scaling sweep")


def analytic(alpha, beta, N):
    k = np.arange(N)
    return np.sort(alpha + 2.0 * beta * np.cos(2.0 * np.pi * k / N))


def parse_log(text: str):
    # Split into: primary block (N=6, n_levels=8) and scale sweep blocks.
    lines = text.splitlines()
    primary_start = next((i for i, l in enumerate(lines) if primary_re.search(l)), None)
    scale_start = next((i for i, l in enumerate(lines) if scale_re.search(l)), None)
    if primary_start is None or scale_start is None:
        raise RuntimeError('log missing section markers')

    primary_text = '\n'.join(lines[primary_start:scale_start])
    scale_text = '\n'.join(lines[scale_start:])

    # Primary
    primary_states = [(int(m[1]), float(m[2]), float(m[3])) for m in state_re.finditer(primary_text)]

    # Scale sweep -> split by "N= K:" boundaries
    scale_lines = lines[scale_start:]
    walls = {}
    for m in wall_re.finditer(scale_text):
        walls[int(m.group(1))] = float(m.group(2))
    # Slice per-N by finding "TISE (als): state = 0" locations then reading until "N= X: wall=" or next state=0
    # Simpler: parse per line and reset each time we see state=0
    per_N = {}  # N -> list of (state, energy, cpu)
    current_states = []
    # We know N appears in walls order. But safer: after each wall line, capture the preceding block.
    current_block = []
    N_seq = []
    for line in scale_lines:
        m_state = state_re.search(line)
        m_wall = wall_re.search(line)
        if m_state:
            current_block.append((int(m_state.group(1)), float(m_state.group(2)), float(m_state.group(3))))
        if m_wall:
            N = int(m_wall.group(1))
            per_N[N] = current_block[:]
            N_seq.append(N)
            current_block = []
    return primary_states, per_N, walls


def main():
    text = LOG.read_text()
    primary_states, per_N, walls = parse_log(text)

    alpha, beta = 0.1, -0.01

    # PRIMARY (N=6, n_levels=8)
    # Analytic 1-exciton band on N=6 ring
    an6 = analytic(alpha, beta, 6)  # 6 values
    primary_energies = np.sort([e for (_, e, _) in primary_states])
    # Vacuum at 0, then 1-exciton band [~0.08, 0.12], then 2-exciton sector starts around 0.165
    band_1 = primary_energies[(primary_energies > 0.05) & (primary_energies < 0.15)]
    # Deduplicate (WaveTrain returns each level twice for degenerate ones? no, but rounding may collide)
    band_1_sorted = np.sort(band_1)
    # If we captured all 6 (or fewer if truncated), compare
    n_match = min(len(band_1_sorted), len(an6))
    band_err = np.abs(band_1_sorted[:n_match] - an6[:n_match])

    primary_out = {
        'params': {'n_site': 6, 'n_levels': 8, 'alpha': alpha, 'beta': beta,
                   'periodic': True, 'homogen': True, 'n_basis': 2,
                   'solver': 'als', 'eigen': 'eig', 'ranks': 15,
                   'repeats': 20, 'conv_eps': 1e-8},
        'all_energies_sorted': primary_energies.tolist(),
        'analytic_1exciton_band': an6.tolist(),
        'measured_1exciton_band': band_1_sorted.tolist(),
        'abs_errors_band': band_err.tolist() if n_match else [],
        'max_abs_err_band': float(band_err.max()) if n_match else None,
        'mean_abs_err_band': float(band_err.mean()) if n_match else None,
        'total_wall_sec': None,  # not captured for primary specifically
    }

    # SCALING SWEEP
    scale_out = []
    for N in sorted(per_N.keys()):
        states = per_N[N]
        energies = np.sort([e for (_, e, _) in states])
        cpus = [c for (_, _, c) in states]
        an = analytic(alpha, beta, N)
        band = energies[(energies > 0.05) & (energies < 0.15)]
        band = np.sort(band)
        # Take the lowest N (which is the full 1-exciton band)
        band_N = band[:N] if len(band) >= N else band
        errs = np.abs(band_N - an[:len(band_N)])
        # sum of per-state ALS CPU
        sum_cpu = sum(cpus)
        wall = walls.get(N)
        scale_out.append({
            'N': N,
            'n_levels_requested': N + 1,
            'n_states_returned': len(states),
            'all_energies': energies.tolist(),
            'analytic_band': an.tolist(),
            'measured_band': band_N.tolist(),
            'abs_errors': errs.tolist(),
            'max_abs_err': float(errs.max()) if len(errs) else None,
            'mean_abs_err': float(errs.mean()) if len(errs) else None,
            'per_state_cpu_sec': cpus,
            'sum_state_cpu_sec': float(sum_cpu),
            'wall_clock_sec': wall,
        })

    result = {
        'source_log': str(LOG),
        'primary': primary_out,
        'scale_sweep': scale_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2))
    print(f'Wrote {OUT}')
    print()
    print('=== PRIMARY (N=6, n_levels=8) ===')
    print(f'  1-exciton band (measured): {band_1_sorted}')
    print(f'  1-exciton band (analytic): {an6}')
    if n_match:
        print(f'  max|err| = {band_err.max():.3e}    mean|err| = {band_err.mean():.3e}')
    print()
    print('=== SCALING SWEEP ===')
    print(f'{"N":>4} {"wall(s)":>10} {"sum_CPU(s)":>12} {"max|err|":>12} {"scaling":>10}')
    prev_wall = None
    for row in scale_out:
        wcls = f'{row["wall_clock_sec"]:.2f}' if row["wall_clock_sec"] is not None else 'n/a'
        maxe = f'{row["max_abs_err"]:.2e}' if row["max_abs_err"] is not None else 'n/a'
        scaling = f'{row["wall_clock_sec"]/prev_wall:.2f}x' if prev_wall else '-'
        print(f'{row["N"]:>4} {wcls:>10} {row["sum_state_cpu_sec"]:>12.2f} {maxe:>12} {scaling:>10}')
        prev_wall = row['wall_clock_sec']


if __name__ == '__main__':
    main()
