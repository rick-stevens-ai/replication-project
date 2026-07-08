"""
Replication of arXiv:2307.05203 core claim:
Choice of extrapolation family + noise-factor range materially affects
ZNE accuracy. Compare Linear, Polynomial (quadratic), Richardson,
and Exponential fits on the same raw noise-amplified scan.

Approach: build a 6-qubit brickwork spin-dynamics-like circuit (following
the paper's benchmark family), run under depolarizing noise on Qiskit Aer,
scan noise factors (both wide {1,3,5} and narrow {1,1.1,1.2} regimes), fit
different families to the *same* raw data, compare mitigated expectation
to the noise-free reference.

Real Mitiq + Qiskit Aer. No fabrication.
"""

import json, math, os, sys, time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_gates_at_random, fold_global
from mitiq.zne.inference import (
    LinearFactory,
    PolyFactory,
    RichardsonFactory,
    ExpFactory,
)

ROOT = Path(__file__).resolve().parent.parent
EVID = ROOT / "report" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Circuit: 6-qubit brickwork spin dynamics (Trotterized XY-like), var. depth
# -----------------------------------------------------------------------------
def brickwork_circuit(n_qubits: int, depth: int, seed: int = 0) -> QuantumCircuit:
    """Random-parameter brickwork of 2-qubit gates.
    This is the family the paper uses as a benchmark (Sec/Fig 6, App B).
    Each 'layer' has an even bond row then an odd bond row of RXX/RYY/RZZ-like
    entanglers implemented as CX-RZ-CX ladders parameterized by random angles.
    """
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n_qubits)
    # initial state: X on all qubits to leave |+>^n (non-trivial <Z> observable)
    for q in range(n_qubits):
        qc.h(q)
    for d in range(depth):
        # even bonds (0-1, 2-3, 4-5)
        for q in range(0, n_qubits - 1, 2):
            theta = float(rng.uniform(0, 2 * math.pi))
            qc.cx(q, q + 1)
            qc.rz(theta, q + 1)
            qc.cx(q, q + 1)
        # odd bonds (1-2, 3-4)
        for q in range(1, n_qubits - 1, 2):
            theta = float(rng.uniform(0, 2 * math.pi))
            qc.cx(q, q + 1)
            qc.rz(theta, q + 1)
            qc.cx(q, q + 1)
        # single-qubit rotations to break commutation
        for q in range(n_qubits):
            qc.rx(float(rng.uniform(0, math.pi)), q)
    return qc


# -----------------------------------------------------------------------------
# Observable: Z0 * Z_{n-1}  (correlator, expected in [-1, 1])
# -----------------------------------------------------------------------------
N_QUBITS = 6
OBS_STR = "Z" + "I" * (N_QUBITS - 2) + "Z"
OBSERVABLE = SparsePauliOp.from_list([(OBS_STR, 1.0)])


def make_noise_model(depol_2q: float) -> NoiseModel:
    """Depolarizing noise on 2-qubit gates only (matches paper's model)."""
    nm = NoiseModel()
    err = depolarizing_error(depol_2q, 2)
    nm.add_all_qubit_quantum_error(err, ["cx"])
    return nm


# Basis gates for transpilation - must match what the noise model applies to.
BASIS_GATES = ["cx", "rz", "rx", "ry", "h", "sx", "x", "id"]


def ideal_expectation(qc: QuantumCircuit) -> float:
    """Noiseless statevector expectation of OBSERVABLE."""
    sim = AerSimulator(method="statevector")
    tqc = transpile(qc, sim, basis_gates=BASIS_GATES, optimization_level=0)
    tqc.save_statevector()
    result = sim.run(tqc, shots=1).result()
    sv = result.get_statevector(tqc)
    # <psi|H|psi>
    return float(np.real(sv.expectation_value(OBSERVABLE)))


def noisy_executor(qc: QuantumCircuit, noise_model: NoiseModel, shots: int) -> float:
    """Run qc under the noise model with sampling. Return <ZZ> estimate."""
    sim = AerSimulator(noise_model=noise_model)
    meas = qc.copy()
    meas.measure_all()
    tqc = transpile(meas, sim, basis_gates=BASIS_GATES, optimization_level=0)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    # <Z0 * Z_{n-1}> = sum_x p(x) * (-1)^(x0 + x_{n-1})
    total = sum(counts.values())
    exp = 0.0
    for bitstr, c in counts.items():
        # Qiskit bit ordering: bitstr is q_{n-1} ... q_0
        bits = bitstr.replace(" ", "")
        b0 = int(bits[-1])  # q0
        bn = int(bits[0])   # q_{n-1}
        parity = (b0 + bn) % 2
        val = 1.0 if parity == 0 else -1.0
        exp += val * c / total
    return exp


# -----------------------------------------------------------------------------
# ZNE experiment
# -----------------------------------------------------------------------------
def scan_raw_at_scale_factors(
    qc: QuantumCircuit,
    noise_model: NoiseModel,
    scale_factors,
    shots: int,
    seed: int,
    reps: int = 3,
):
    """Fold circuit to each scale factor, run noisy_executor. Return
    (scale_factors, mean_values, std_values). Uses global folding
    (paper's canonical choice for integer scales) with light averaging.
    """
    rng = np.random.default_rng(seed)
    means, stds = [], []
    for lam in scale_factors:
        vals = []
        for r in range(reps):
            # For non-integer scales use random partial folding
            if abs(lam - round(lam)) > 1e-9:
                folded = fold_gates_at_random(qc, scale_factor=lam, seed=int(rng.integers(1e9)))
            else:
                folded = fold_global(qc, scale_factor=lam)
            v = noisy_executor(folded, noise_model, shots)
            vals.append(v)
        means.append(float(np.mean(vals)))
        stds.append(float(np.std(vals) / math.sqrt(len(vals))))
    return list(scale_factors), means, stds


def fit_families_to_raw(scale_factors, means):
    """Fit multiple extrapolator families to the same raw scan.
    Returns dict family -> extrapolated value at lam=0.
    """
    out = {}
    sfs = list(scale_factors)

    # Linear
    lf = LinearFactory(scale_factors=sfs)
    lf._instack = [{"scale_factor": s} for s in sfs]
    lf._outstack = list(means)
    out["Linear"] = float(lf.extrapolate(sfs, means))

    # Polynomial degree 2 (Quadratic)
    if len(sfs) >= 3:
        out["Quadratic"] = float(PolyFactory.extrapolate(sfs, means, order=2))
    else:
        out["Quadratic"] = float("nan")

    # Richardson
    out["Richardson"] = float(RichardsonFactory.extrapolate(sfs, means))

    # Exponential (needs asymptote parameter; paper uses mono-exponential
    # with asymptote 0 for traceless observables in depolarizing saturation)
    try:
        out["Exponential"] = float(ExpFactory.extrapolate(sfs, means, asymptote=0.0))
    except Exception as e:
        out["Exponential"] = float("nan")

    return out


def run_case(depth: int, depol_2q: float, scale_factors, shots: int,
             reps: int, circ_seed: int, tag: str):
    print(f"\n=== case tag={tag} depth={depth} p2q={depol_2q} "
          f"scales={scale_factors} shots={shots} reps={reps} ===")
    qc = brickwork_circuit(N_QUBITS, depth, seed=circ_seed)
    ideal = ideal_expectation(qc)
    print(f"  ideal <ZZ> = {ideal:+.4f}")

    nm = make_noise_model(depol_2q)
    sfs, means, stds = scan_raw_at_scale_factors(
        qc, nm, scale_factors, shots=shots, seed=circ_seed + 101, reps=reps
    )
    for s, m, sd in zip(sfs, means, stds):
        print(f"  scale={s:>5.2f}  <ZZ>_noisy = {m:+.4f} +- {sd:.4f}")

    fits = fit_families_to_raw(sfs, means)
    print("  fits (mitigated <ZZ>):")
    errs = {}
    for fam, val in fits.items():
        e = abs(val - ideal)
        errs[fam] = e
        print(f"    {fam:12s} = {val:+.4f}   |err|={e:.4f}")
    unmit_err = abs(means[0] - ideal)
    print(f"    Unmitigated  = {means[0]:+.4f}   |err|={unmit_err:.4f}")

    return {
        "tag": tag,
        "depth": depth,
        "depol_2q": depol_2q,
        "scale_factors": sfs,
        "shots": shots,
        "reps": reps,
        "circ_seed": circ_seed,
        "ideal": ideal,
        "unmitigated": means[0],
        "unmitigated_err": unmit_err,
        "raw_means": means,
        "raw_stds": stds,
        "fits": fits,
        "fit_errors": errs,
    }


def main():
    t0 = time.time()

    # Compare 4 regimes crossing the paper's Fig. 6 axes:
    # A: weak noise, shallow depth      -> Linear should win
    # B: strong noise, deep depth       -> Exp/Quadratic should win
    # C: wide scales (1,3,5) vs narrow (1,1.1,1.2) -- both at moderate depth
    cases = []
    # Case A: weak, shallow, wide scales
    cases.append(dict(depth=4, depol_2q=0.002,
                      scale_factors=[1.0, 3.0, 5.0], tag="A_weak_shallow_wide"))
    # Case B: strong, deep, wide scales
    cases.append(dict(depth=20, depol_2q=0.02,
                      scale_factors=[1.0, 3.0, 5.0], tag="B_strong_deep_wide"))
    # Case C: moderate, wide scales
    cases.append(dict(depth=10, depol_2q=0.01,
                      scale_factors=[1.0, 3.0, 5.0], tag="C_mod_wide"))
    # Case D: same moderate, narrow scales
    cases.append(dict(depth=10, depol_2q=0.01,
                      scale_factors=[1.0, 1.1, 1.2], tag="D_mod_narrow"))
    # Case E: strong deep, narrow scales
    cases.append(dict(depth=20, depol_2q=0.02,
                      scale_factors=[1.0, 1.1, 1.2], tag="E_strong_deep_narrow"))

    all_results = []
    for c in cases:
        r = run_case(depth=c["depth"], depol_2q=c["depol_2q"],
                     scale_factors=c["scale_factors"],
                     shots=8000, reps=3, circ_seed=42, tag=c["tag"])
        all_results.append(r)

    # Also: fit families to same raw data of one case to visually show
    # they diverge on identical inputs.
    print("\n=== summary: |err| per family per case ===")
    header = f"{'case':30s}  " + "  ".join(f"{k:>11s}" for k in
        ["Linear", "Quadratic", "Richardson", "Exponential", "Unmit"])
    print(header)
    for r in all_results:
        row = f"{r['tag']:30s}  " + "  ".join(
            f"{r['fit_errors'][k]:>11.4f}" for k in
            ["Linear", "Quadratic", "Richardson", "Exponential"]) + \
            f"  {r['unmitigated_err']:>11.4f}"
        print(row)

    out_path = EVID / "zne_results.json"
    with open(out_path, "w") as f:
        json.dump({
            "paper": "arXiv:2307.05203",
            "n_qubits": N_QUBITS,
            "observable": OBS_STR,
            "shots_per_scale": 8000,
            "reps_per_scale": 3,
            "cases": all_results,
            "wall_seconds": time.time() - t0,
        }, f, indent=2)
    print(f"\nWrote {out_path}")
    print(f"Wall time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
