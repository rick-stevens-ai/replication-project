#!/usr/bin/env python3
"""
Replicate Barenco/Ekert/Suominen/Törma (1996) quant-ph/9601018:
'Approximate Quantum Fourier Transform and Decoherence'

Central claim we test:
  Truncating controlled-phase gates in the QFT circuit at |k-j| > m
  (AQFT of degree m) keeps the transform very close to the exact QFT.
  In particular:
    (a) state fidelity |<QFT ψ | AQFT_m ψ>|^2 -> 1 as m -> n and the
        deviation scales polynomially in n and shrinks with m.
    (b) matrix elements of QFT vs AQFT_m differ by phases exp(iε)
        with |ε| <= 2π L / 2^m  (paper, Sec. 3).

Uses Qiskit statevector (no noise; noise-free AQFT vs QFT comparison
is the reproducible core of Sec. 3-4 of the paper).
"""
import json, math, os, sys, time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

RNG = np.random.default_rng(20260705)

def qft_circuit(n: int, m: int | None = None, swap: bool = True) -> QuantumCircuit:
    """Build an AQFT of degree m on n qubits.
    m = None or m >= n  -> exact QFT
    m = 1               -> Hadamard transform (all controlled phases dropped)
    Convention: standard Coppersmith construction. Controlled-R_k gate with
    k = distance+1 is included only if distance+1 <= m (i.e. distance < m).
    Equivalently drop gates whose phase = 2π/2^k with k > m.
    """
    if m is None or m > n:
        m = n
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            dist = k - j  # controlled-phase R_{dist+1} with angle 2π/2^{dist+1}
            # Paper drops B_{jk} with π/2^{k-j} < π/2^m  <=>  k-j > m
            if dist <= m - 1:  # keep if k-j <= m-1, i.e. dist <= m-1
                # Wait — let's re-read: paper says drop B_jk when θ_jk = π/2^{k-j}
                # is smaller than π/2^m, i.e. k-j > m. So KEEP when k-j <= m.
                pass
    # Rebuild properly per paper convention: keep when (k-j) <= m
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            dist = k - j
            if dist <= m:
                angle = math.pi / (2 ** dist)
                qc.cp(angle, k, j)
    if swap:
        for i in range(n // 2):
            qc.swap(i, n - 1 - i)
    return qc


def random_pure_state(n: int, rng) -> np.ndarray:
    dim = 2 ** n
    v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
    v /= np.linalg.norm(v)
    return v


def fidelity(psi1: np.ndarray, psi2: np.ndarray) -> float:
    return float(abs(np.vdot(psi1, psi2)) ** 2)


def apply_circuit(state: np.ndarray, qc: QuantumCircuit) -> np.ndarray:
    sv = Statevector(state)
    out = sv.evolve(qc)
    return np.asarray(out.data)


def experiment_A_fidelity(n_list=(4, 6, 8), n_samples=100):
    """(a) direct state-fidelity |<QFT_exact ψ | QFT_approx ψ>|^2 across m∈{1..n}."""
    results = {}
    for n in n_list:
        qft_exact = qft_circuit(n, m=n)
        # Precompute exact QFT states on each sample
        rng = np.random.default_rng(20260705 + n)
        samples = [random_pure_state(n, rng) for _ in range(n_samples)]
        exact_out = [apply_circuit(s, qft_exact) for s in samples]

        per_m = {}
        for m in range(1, n + 1):
            aqft = qft_circuit(n, m=m)
            fids = []
            for s, ex in zip(samples, exact_out):
                app = apply_circuit(s, aqft)
                fids.append(fidelity(ex, app))
            per_m[m] = {
                "mean_fidelity": float(np.mean(fids)),
                "std_fidelity": float(np.std(fids)),
                "min_fidelity": float(np.min(fids)),
                "n_samples": n_samples,
            }
        results[n] = per_m
        print(f"n={n}:")
        for m, v in per_m.items():
            print(f"  m={m}: mean_fid={v['mean_fidelity']:.6f} ± {v['std_fidelity']:.4f} min={v['min_fidelity']:.6f}")
    return results


def matrix_epsilon_bound(n_list=(4, 6, 8)):
    """Verify paper's Sec.3 bound: matrix elements of QFT vs AQFT differ by
    factor exp(iε) with |ε| <= 2π L / 2^m.
    We compute the operator difference and the max phase deviation per matrix element."""
    out = {}
    for n in n_list:
        qft_exact = qft_circuit(n, m=n, swap=False)
        U_exact = np.asarray(Operator(qft_exact).data)
        rows = {}
        for m in range(1, n + 1):
            aqft = qft_circuit(n, m=m, swap=False)
            U_app = np.asarray(Operator(aqft).data)
            # per-element phase diff (ignore elements that are numerically zero)
            ratio = np.zeros_like(U_exact)
            mask = np.abs(U_exact) > 1e-10
            ratio[mask] = U_app[mask] / U_exact[mask]
            eps = np.angle(ratio[mask])  # signed phase in (-π, π]
            max_eps = float(np.max(np.abs(eps)))
            bound = 2 * math.pi * n / (2 ** m)
            rows[m] = {
                "max_phase_dev": max_eps,
                "paper_bound_2piL_over_2m": bound,
                "bound_holds": max_eps <= bound + 1e-9,
                "op_norm_diff": float(np.linalg.norm(U_app - U_exact, ord=2)),
            }
        out[n] = rows
        print(f"n={n} matrix eps check:")
        for m, r in rows.items():
            print(f"  m={m}: max|ε|={r['max_phase_dev']:.4f} bound=2πL/2^m={r['paper_bound_2piL_over_2m']:.4f} holds={r['bound_holds']} opnorm={r['op_norm_diff']:.4f}")
    return out


if __name__ == "__main__":
    t0 = time.time()
    print("=" * 60)
    print("Experiment A: state-fidelity AQFT_m vs exact QFT")
    print("=" * 60)
    fidA = experiment_A_fidelity(n_list=(4, 6, 8), n_samples=100)

    print()
    print("=" * 60)
    print("Matrix-element phase bound (Sec.3): |ε| <= 2π L / 2^m")
    print("=" * 60)
    epsB = matrix_epsilon_bound(n_list=(4, 6, 8))

    out = {
        "meta": {
            "paper": "quant-ph/9601018 Barenco/Ekert/Suominen/Törma 1996",
            "n_samples_per_m": 100,
            "seed": 20260705,
            "elapsed_sec": time.time() - t0,
        },
        "experiment_A_fidelity": fidA,
        "experiment_B_matrix_epsilon": epsB,
    }
    out_path = os.path.join(os.path.dirname(__file__), "results_fidelity.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}  ({time.time()-t0:.1f}s)")
