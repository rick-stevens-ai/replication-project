"""
Independent replication of key experiment from arXiv:2402.04000
"Quantum error mitigation by layerwise Richardson extrapolation"
(Russo & Mari, Unitary Fund, 2024/2025)

Reproduces the paper's Table I (GHZ-like benchmark under amplitude-damping noise):
  - Unmitigated
  - Global Richardson Extrapolation (RE)
  - Layerwise Richardson Extrapolation (LRE)

Circuit family: n-qubit GHZ prep followed by its inverse, so ideal <O> = 1
   for O = |0...0><0...0|.

Both RE and LRE implemented from scratch (multivariate Lagrange coefficients
   for LRE, linear extrapolation d=1 for a clean minimal reproduction).
   Cross-checked qualitatively against paper's numbers.

Noise: local amplitude damping on every 1-qubit and 2-qubit gate layer,
   with layerwise unitary folding used as the noise-scaling knob
   (folding = G -> G G^dag G repeated m_k times => noise scale = 1 + 2*m_k).

Author: Ollie (subagent, 2026-07-05)
"""
from __future__ import annotations
import argparse, json, math, time, itertools, sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence
import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, amplitude_damping_error

# -------- circuit construction --------

def ghz_like_circuit(n_qubits: int) -> QuantumCircuit:
    """n-qubit GHZ prep + inverse.  Ideal <|0><0|> = 1."""
    qc = QuantumCircuit(n_qubits, n_qubits)
    # GHZ prep
    qc.h(0)
    for k in range(n_qubits - 1):
        qc.cx(k, k + 1)
    # Inverse
    for k in reversed(range(n_qubits - 1)):
        qc.cx(k, k + 1)
    qc.h(0)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def layer_split(qc: QuantumCircuit) -> list[list]:
    """Split a QuantumCircuit into a sequence of single-instruction layers
    (measurements excluded and appended at end).  Each layer is a list of
    (instruction, qubits) tuples.  For LRE folding, we fold each gate
    layer independently."""
    layers, meas = [], []
    for inst in qc.data:
        op = inst.operation
        if op.name in ("measure", "barrier"):
            meas.append(inst)
        else:
            layers.append([inst])
    return layers, meas

def _apply_inst(qc, inst):
    qc.append(inst.operation, inst.qubits, inst.clbits)

def _apply_inst_inverse(qc, inst):
    inv = inst.operation.inverse()
    qc.append(inv, inst.qubits, inst.clbits)

def fold_layers(qc: QuantumCircuit, m_vec: Sequence[int]) -> QuantumCircuit:
    """Unitary folding, gate-by-gate.  m_vec[k] = number of extra G G^dag pairs
    applied at gate-layer k.  Effective noise scale for layer k = 1 + 2*m_vec[k]."""
    layers, meas = layer_split(qc)
    assert len(m_vec) == len(layers), f"m_vec len {len(m_vec)} != layers {len(layers)}"
    new = QuantumCircuit(qc.num_qubits, qc.num_clbits)
    for lyr, m in zip(layers, m_vec):
        for inst in lyr:
            _apply_inst(new, inst)
        for _ in range(m):
            for inst in lyr:
                _apply_inst_inverse(new, inst)
            for inst in lyr:
                _apply_inst(new, inst)
    for inst in meas:
        _apply_inst(new, inst)
    return new

# -------- noise + execution --------

def build_noise_model(gamma_1q: float, gamma_2q: float) -> NoiseModel:
    nm = NoiseModel()
    e1 = amplitude_damping_error(gamma_1q)
    e2 = amplitude_damping_error(gamma_2q).tensor(amplitude_damping_error(gamma_2q))
    nm.add_all_qubit_quantum_error(e1, ["h", "u", "u1", "u2", "u3", "rx", "ry", "rz",
                                       "sx", "sxdg", "x", "y", "z", "s", "sdg", "t", "tdg"])
    nm.add_all_qubit_quantum_error(e2, ["cx", "cz", "swap"])
    return nm

def zero_state_prob(counts: dict[str, int], n_qubits: int) -> float:
    key = "0" * n_qubits
    total = sum(counts.values())
    return counts.get(key, 0) / total if total else 0.0

def run_circuit(qc: QuantumCircuit, shots: int, noise_model: NoiseModel,
                seed: int | None = None) -> float:
    sim = AerSimulator(noise_model=noise_model, seed_simulator=seed)
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()
    return zero_state_prob(counts, qc.num_qubits)

# -------- Richardson-style extrapolators --------

def linear_extrapolate(scales: Sequence[float], values: Sequence[float]) -> float:
    """Fit y = a + b*x, return a."""
    x = np.asarray(scales, float); y = np.asarray(values, float)
    coeffs = np.polyfit(x, y, 1)   # highest-deg first
    return float(coeffs[-1])

def global_re(qc: QuantumCircuit, shots_per_point: int, noise_model: NoiseModel,
              m_values=(0, 1, 2), seed: int | None = None) -> tuple[float, list[float]]:
    """Standard global Richardson: uniform folding, m same on every layer.
    Scale factors c_i = 1 + 2*m_i.  Linear fit -> y(c=0)."""
    n_layers = len(layer_split(qc)[0])
    scales, values = [], []
    for i, m in enumerate(m_values):
        folded = fold_layers(qc, [m] * n_layers)
        val = run_circuit(folded, shots_per_point, noise_model,
                          seed=(seed + i if seed is not None else None))
        scales.append(1 + 2 * m); values.append(val)
    return linear_extrapolate(scales, values), values

def lre_linear(qc: QuantumCircuit, shots_per_point: int, noise_model: NoiseModel,
               m_per_layer=(0, 1), seed: int | None = None) -> tuple[float, list[float]]:
    """LRE at extrapolation order d=1 (linear).  Uses the standard-basis
    scale-factor vectors:
        lambda_0 = (1,1,...,1)       -> all-ones
        lambda_k = (1,...,2*m+1,...,1) -> only layer k is folded
    which spans the linear polynomial in ell variables.

    For a linear multivariate model f(l_1,...,l_L) = a_0 + sum_k a_k l_k,
    the zero-noise value f(0,...,0) = a_0 satisfies
        f(0,...,0) = (1 + L*t) * y_0 - t * sum_k y_k
    where y_0 = eval at all-ones, y_k = eval at only-layer-k folded,
    and t = 1 / (2*m).  (Derived by inverting the 2x2 per-coordinate system.)

    We use m = m_per_layer[1]-m_per_layer[0]=1 by default (scales 1 and 3).
    """
    layers, _ = layer_split(qc)
    L = len(layers)
    m_base, m_fold = m_per_layer   # (0, 1) => scales 1 and 3
    assert m_base == 0 and m_fold >= 1

    # Reference run: all layers at scale 1
    ref = fold_layers(qc, [m_base] * L)
    y_ref = run_circuit(ref, shots_per_point, noise_model,
                        seed=(seed if seed is not None else None))

    # Per-layer perturbed runs
    y_k = []
    for k in range(L):
        m_vec = [m_base] * L
        m_vec[k] = m_fold
        cir = fold_layers(qc, m_vec)
        val = run_circuit(cir, shots_per_point, noise_model,
                          seed=(seed + k + 1 if seed is not None else None))
        y_k.append(val)

    # scale factor per axis = 1 + 2*m_fold
    c = 1 + 2 * m_fold
    # Linear model: y(lambda) = a0 + sum_k a_k (lambda_k - 1)
    # y_ref = a0;  y_k = a0 + a_k * (c - 1)  =>  a_k = (y_k - a0)/(c-1)
    # y(0,...,0) = a0 + sum_k a_k * (0 - 1) = a0 - sum_k a_k
    a_k = [(v - y_ref) / (c - 1) for v in y_k]
    zne = y_ref - sum(a_k)
    return zne, [y_ref] + y_k

# -------- experiment driver --------

@dataclass
class Point:
    n_qubits: int
    n_layers: int
    unmitigated: float
    re: float
    lre: float
    abs_err_unmit: float
    abs_err_re: float
    abs_err_lre: float
    lre_raw: list
    re_raw: list
    ideal: float = 1.0

def run_sweep(n_qubit_list, shots_budget=200_000, trials=5, gamma=0.02, seed0=42):
    """For each n in n_qubit_list, run trials repetitions.
    Report mean abs err for unmit/RE/LRE, mirroring paper Table I (depth = n_qubits-1
    for the paper's convention where l = 2n and n_qubits is small).

    Shot budget is TOTAL across all sub-circuits, matching paper's convention.
    """
    nm = build_noise_model(gamma_1q=gamma, gamma_2q=gamma)
    rows = []
    for n in n_qubit_list:
        qc = ghz_like_circuit(n)
        L = len(layer_split(qc)[0])
        # Budget splits:
        #   Unmit: all shots on one circuit
        #   RE (3 points, linear-ish with 3 scales): shots/3 each
        #   LRE (1 + L per-layer runs): shots/(1+L) each
        shots_unmit = shots_budget
        shots_re    = shots_budget // 3
        shots_lre   = shots_budget // (1 + L)

        errs_unmit, errs_re, errs_lre = [], [], []
        raws = None
        for t in range(trials):
            seed = seed0 + 1000 * t + n
            unmit_val = run_circuit(qc, shots_unmit, nm, seed=seed)
            re_val, re_raw = global_re(qc, shots_re, nm, m_values=(0, 1, 2), seed=seed + 1)
            lre_val, lre_raw = lre_linear(qc, shots_lre, nm, m_per_layer=(0, 1), seed=seed + 2)

            errs_unmit.append(abs(1.0 - unmit_val))
            errs_re.append(abs(1.0 - re_val))
            errs_lre.append(abs(1.0 - lre_val))
            if t == 0:
                raws = (re_raw, lre_raw)

        rows.append(Point(
            n_qubits=n,
            n_layers=L,
            unmitigated=float(np.mean(errs_unmit)),
            re=float(np.mean(errs_re)),
            lre=float(np.mean(errs_lre)),
            abs_err_unmit=float(np.mean(errs_unmit)),
            abs_err_re=float(np.mean(errs_re)),
            abs_err_lre=float(np.mean(errs_lre)),
            re_raw=raws[0],
            lre_raw=raws[1],
        ))
        # progress print
        r = rows[-1]
        print(f"[n={n:>2} L={L:>2}] |1-unmit|={r.unmitigated:.4f}  "
              f"|1-RE|={r.re:.4f}  |1-LRE|={r.lre:.4f}  "
              f"LRE-improv-vs-RE={(r.re/max(r.lre,1e-9)-1)*100:+.1f}%")
        sys.stdout.flush()
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nqubits", type=int, nargs="+", default=[2, 3, 4, 5])
    ap.add_argument("--shots", type=int, default=200_000)
    ap.add_argument("--trials", type=int, default=5)
    ap.add_argument("--gamma", type=float, default=0.02)
    ap.add_argument("--out", type=str, default="results.json")
    args = ap.parse_args()

    t0 = time.time()
    rows = run_sweep(args.nqubits, shots_budget=args.shots, trials=args.trials,
                     gamma=args.gamma)
    dt = time.time() - t0

    payload = {
        "meta": {
            "paper_arxiv": "2402.04000",
            "circuit_family": "GHZ + GHZ^-1",
            "observable": "|0...0><0...0|  (ideal = 1)",
            "noise_model": "amplitude damping per gate, gamma_1q=gamma_2q="
                           + str(args.gamma),
            "shots_budget_total": args.shots,
            "trials": args.trials,
            "runtime_sec": dt,
            "extrapolation_order": 1,
            "re_scale_factors": [1, 3, 5],
            "lre_scale_factors": "layerwise: base=1 on all layers, one layer perturbed to 3",
        },
        "rows": [asdict(r) for r in rows],
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, default=list))
    print(f"\nDone in {dt:.1f}s.  Wrote {args.out}")

if __name__ == "__main__":
    main()
