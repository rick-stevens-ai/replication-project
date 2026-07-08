#!/usr/bin/env python3
"""
Independent replication of Pascuzzi et al. arXiv:2110.13338
"Computationally Efficient Zero Noise Extrapolation for Quantum Gate Error Mitigation"

Reproducible core (Fig 2/3 of the paper):
- 2-qubit circuit prepared in |11>, with r = 2n+1 CNOTs applied to the same qubit pair.
- Since CNOT^2 = I on |11>, the noiseless expectation value <Pr(|11>)> = 1 (raw = 1).
- With 2-qubit depolarizing noise, raw <Pr(|11>)> decays with number of CNOTs.
- ZNE ("fiim"-like) with global folding across noise scales should mitigate this and
  push the extrapolated Pr(|11>) back toward 1.
- An "efficient" ZNE variant (fewer noise scales, less circuit inflation) should
  achieve comparable accuracy at reduced sampling cost (paper's central efficiency claim).

Tools:
- Qiskit Aer noisy simulator (density-matrix / statevector, plus shot noise)
- Mitiq ZNE (linear factory, fold_global vs fold_gates_at_random)

Real simulation only. No fabrication. Shot-noise-limited numbers.
"""
import json
import os
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, amplitude_damping_error, thermal_relaxation_error

from mitiq import zne
from mitiq.zne.scaling import fold_global, fold_gates_at_random
from mitiq.zne.inference import LinearFactory, RichardsonFactory

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EPSILON = 0.01           # 2-qubit depolarizing error rate (paper uses "of order a percent"; Fig 2 uses eps=1%)
T1_US = 50.0             # T1 in microseconds (paper Fig 2)
TCNOT_NS = 200.0         # CNOT gate time in ns (paper Fig 2)
# Fig 2 caption: "even number of cnot gates as specified by the horizontal axis".
# For |11> initial and CNOT(0,1), even count leaves state at |11> (noiseless), so Pr(|11>) = 1 exactly.
CNOT_COUNTS = [2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 30]
SHOTS = 8192             # per-circuit shots for the shot-noise comparison
SEED = 20260703
OUTPUT_DIR = Path(__file__).parent
RESULTS_JSON = OUTPUT_DIR / "results.json"

rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------------------
# Noise model — paper Fig 2 recipe
# ---------------------------------------------------------------------------
def build_noise_model(epsilon: float, t1_us: float, tcnot_ns: float) -> NoiseModel:
    """
    2-qubit depolarizing noise on CNOT with probability `epsilon`,
    plus amplitude damping (thermal relaxation with T2=T1) with gamma = 1 - exp(-Tcnot/T1).
    Applied ONLY to cx (CNOT); single-qubit gates left noiseless (matches paper: "ZNE
    is typically applied only to cnot gates").
    """
    nm = NoiseModel()
    # depolarizing part
    depo = depolarizing_error(epsilon, 2)
    # amplitude-damping / thermal relaxation on the two CNOT qubits (each qubit gets
    # amplitude damping with gamma from T1). Model as thermal_relaxation with T2=T1.
    t1_ns = t1_us * 1e3
    ad_1q = thermal_relaxation_error(t1=t1_ns, t2=t1_ns, time=tcnot_ns, excited_state_population=0.0)
    ad_2q = ad_1q.expand(ad_1q)  # tensor product on both qubits
    # composition: apply depolarizing then amp-damping
    cnot_err = depo.compose(ad_2q)
    nm.add_all_qubit_quantum_error(cnot_err, ["cx"])
    return nm


# ---------------------------------------------------------------------------
# Circuit — Fig 3 of paper: |11> prep, r CNOTs, measure Pr(11)
# ---------------------------------------------------------------------------
def build_circuit(num_cnots: int) -> QuantumCircuit:
    """Prepare |11>, apply num_cnots CNOTs (0-control, 1-target). No measurement gates
    (mitiq executor will handle the shot sampling and observable)."""
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    for _ in range(num_cnots):
        qc.cx(0, 1)
    return qc


# ---------------------------------------------------------------------------
# Executor — Aer noisy simulation, returns <Pr(|11>)>
# ---------------------------------------------------------------------------
_noise_model = build_noise_model(EPSILON, T1_US, TCNOT_NS)
_backend = AerSimulator(noise_model=_noise_model, seed_simulator=SEED)


def executor_shots(circuit: QuantumCircuit, shots: int = SHOTS) -> float:
    """Run `circuit` with SHOTS on the noisy backend and return the frequency of |11>."""
    qc = circuit.copy()
    qc.measure_all()
    tqc = transpile(qc, _backend, optimization_level=0)
    result = _backend.run(tqc, shots=shots).result()
    counts = result.get_counts()
    # measure_all appends bits in reverse order; look for '11'
    # Qiskit bitstring order: c_{n-1}...c_0
    p11 = counts.get("11", 0) / shots
    return p11


def executor_exact(circuit: QuantumCircuit) -> float:
    """Density-matrix (noiseless-shots) expectation of Pr(|11>)."""
    from qiskit_aer import AerSimulator as _AerSim
    from qiskit.quantum_info import DensityMatrix
    dm_backend = _AerSim(noise_model=_noise_model, method="density_matrix", seed_simulator=SEED)
    qc = circuit.copy()
    qc.save_density_matrix()
    tqc = transpile(qc, dm_backend, optimization_level=0)
    result = dm_backend.run(tqc, shots=1).result()
    dm = result.data(0)["density_matrix"]
    # Diagonal element |11><11|
    p11 = float(np.real(dm.data[3, 3]))
    return p11


# ---------------------------------------------------------------------------
# Sweep: raw vs FIIM-like ZNE (global folding, many scales) vs efficient ZNE
# ---------------------------------------------------------------------------
def run_sweep():
    records = []

    # FIIM-like: global folding at scale_factors [1, 2, 3] (rich scan)
    # Efficient variant: fewer scales [1, 3] (linear extrapolation), gates-at-random folding
    #   -> less circuit inflation on average, fewer distinct circuits, fewer total shots
    fac_full = RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])
    fac_eff = LinearFactory(scale_factors=[1.0, 3.0])

    for nc in CNOT_COUNTS:
        qc = build_circuit(nc)

        # exact (no-shot) noisy expectation
        raw_exact = executor_exact(qc)

        # shot-limited raw
        raw_shots = executor_shots(qc, shots=SHOTS)

        # FIIM-like full ZNE via global folding, 3 scales
        t0 = time.perf_counter()
        zne_full_val = zne.execute_with_zne(
            qc,
            executor=lambda c: executor_shots(c, shots=SHOTS),
            factory=fac_full,
            scale_noise=fold_global,
        )
        t_full = time.perf_counter() - t0
        # count total shots used by the FIIM-like protocol
        shots_full = SHOTS * len(fac_full.get_scale_factors())

        # Efficient ZNE: 2 scales, gates-at-random folding
        t0 = time.perf_counter()
        zne_eff_val = zne.execute_with_zne(
            qc,
            executor=lambda c: executor_shots(c, shots=SHOTS),
            factory=fac_eff,
            scale_noise=fold_gates_at_random,
        )
        t_eff = time.perf_counter() - t0
        shots_eff = SHOTS * len(fac_eff.get_scale_factors())

        rec = dict(
            num_cnots=nc,
            raw_exact=raw_exact,
            raw_shots=raw_shots,
            zne_full=float(zne_full_val),
            zne_eff=float(zne_eff_val),
            shots_full=shots_full,
            shots_eff=shots_eff,
            time_full_s=t_full,
            time_eff_s=t_eff,
        )
        records.append(rec)
        print(
            f"nc={nc:3d}  raw_exact={raw_exact:.4f}  raw_shots={raw_shots:.4f}  "
            f"zne_full={zne_full_val:.4f}  zne_eff={zne_eff_val:.4f}  "
            f"shots_full={shots_full}  shots_eff={shots_eff}"
        )

    return records


def summarize(records):
    """Compute headline claim numbers to compare to the paper."""
    truth = 1.0  # noiseless Pr(|11>) is exactly 1.0

    def mae(key):
        return float(np.mean([abs(r[key] - truth) for r in records]))

    def rmse(key):
        return float(np.sqrt(np.mean([(r[key] - truth) ** 2 for r in records])))

    total_shots_full = sum(r["shots_full"] for r in records)
    total_shots_eff = sum(r["shots_eff"] for r in records)

    summary = dict(
        n_points=len(records),
        cnot_range=[records[0]["num_cnots"], records[-1]["num_cnots"]],
        epsilon=EPSILON,
        t1_us=T1_US,
        tcnot_ns=TCNOT_NS,
        shots_per_circuit=SHOTS,
        seed=SEED,
        # accuracy (lower = closer to noiseless truth = 1.0)
        mae_raw=mae("raw_shots"),
        mae_zne_full=mae("zne_full"),
        mae_zne_eff=mae("zne_eff"),
        rmse_raw=rmse("raw_shots"),
        rmse_zne_full=rmse("zne_full"),
        rmse_zne_eff=rmse("zne_eff"),
        # cost (total shots executed across the sweep)
        total_shots_full=total_shots_full,
        total_shots_eff=total_shots_eff,
        shot_cost_ratio_eff_over_full=total_shots_eff / total_shots_full,
        # headline efficiency: does efficient ZNE stay close to full ZNE?
        mean_abs_delta_eff_vs_full=float(
            np.mean([abs(r["zne_eff"] - r["zne_full"]) for r in records])
        ),
    )
    return summary


def main():
    print("=" * 72)
    print("QC-100 replication: arXiv:2110.13338 efficient ZNE")
    print("=" * 72)
    print(f"epsilon={EPSILON}  T1={T1_US}us  Tcnot={TCNOT_NS}ns")
    print(f"CNOT counts: {CNOT_COUNTS}")
    print(f"shots/circuit: {SHOTS}   seed: {SEED}")
    print()

    t0 = time.perf_counter()
    records = run_sweep()
    total_time = time.perf_counter() - t0

    summary = summarize(records)
    summary["total_wallclock_s"] = total_time

    out = dict(
        paper="arXiv:2110.13338",
        title="Computationally Efficient Zero Noise Extrapolation for Quantum Gate Error Mitigation",
        tools=dict(
            mitiq=__import__("mitiq").__version__,
            qiskit=__import__("qiskit").__version__,
            qiskit_aer=__import__("qiskit_aer").__version__,
            numpy=np.__version__,
        ),
        config=dict(
            epsilon=EPSILON, t1_us=T1_US, tcnot_ns=TCNOT_NS,
            cnot_counts=CNOT_COUNTS, shots=SHOTS, seed=SEED,
        ),
        records=records,
        summary=summary,
    )

    RESULTS_JSON.write_text(json.dumps(out, indent=2))
    print()
    print("SUMMARY")
    print("-" * 72)
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print()
    print(f"Wrote: {RESULTS_JSON}")


if __name__ == "__main__":
    main()
