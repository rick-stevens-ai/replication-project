#!/usr/bin/env python3
"""
End-to-end period finding with AQFT_m for f(x) = a^x mod N.
Follows the paper's Sec. 4 test scenario: the post-modular-exponentiation
input register is in the superposition (1/sqrt(N_states)) sum_{x: f(x)=l} |x>
= a periodic delta comb with period r and unknown offset l.

We simulate JUST the periodic-register + AQFT part (no modular exp circuit
needed — we prepare the periodic state directly, since that is exactly what
the QFT/AQFT receives after tracing over the output register in Shor's
algorithm, per Eqs. (11)-(12) of the paper). Then we measure and score
success = the measurement outcome c satisfies (c * r) mod 2^L is "close"
to a multiple of 2^L, specifically the estimator c/2^L rounds via
continued fractions to k/r for some integer k. For a=7 N=15 r=4, and
L such that 2^L >= N^2 = 225 (i.e. L>=8), the "good" outcomes are exactly
c ∈ {0, 2^L/4, 2^L/2, 3·2^L/4} = {0, 64, 128, 192} for L=8.

We report success probability = sum of |amplitude|^2 over these "good"
outcomes, plus paper's theoretical lower bound
  Prob_A >= (8/π^2) sin^2(π m / (4 L)).
"""
import json, math, os, time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from aqft_fidelity import qft_circuit  # reuse the AQFT builder


def periodic_state(L: int, r: int, offset: int) -> np.ndarray:
    """Prepare the register state (1/sqrt(#{a: a mod r == offset, 0<=a<2^L}))
    sum over |a> with a mod r == offset. This is exactly the collapsed input to
    QFT/AQFT in Shor's algorithm (Eqs. 11-12)."""
    dim = 2 ** L
    xs = [a for a in range(dim) if a % r == offset]
    v = np.zeros(dim, dtype=complex)
    for a in xs:
        v[a] = 1.0
    v /= np.linalg.norm(v)
    return v


def measure_probs(state: np.ndarray) -> np.ndarray:
    return np.abs(state) ** 2


def success_prob_period_finding(L: int, r: int, m: int, offsets_to_avg=None):
    """Average success probability over offset l ∈ {0..r-1}.
    Success = measured c s.t. c is a multiple of 2^L / r (exact since 2^L | r*int here for L>=some).
    More generally, we allow any c whose continued-fraction convergent
    matches a k/r with 0<k<r and gcd(k,r)>0 handled outside — for r=4 the
    "good" c's are exactly the multiples of 2^L/r if r | 2^L.
    Note: Qiskit uses little-endian, so the "reversed order read-out" in the
    paper is handled by the SWAP layer at the end of qft_circuit(swap=True).
    """
    if offsets_to_avg is None:
        offsets_to_avg = list(range(r))
    dim = 2 ** L
    assert dim % r == 0, "for the exact-comb setup we want r | 2^L"
    good_cs = set(int(k * dim / r) for k in range(r))  # {0, dim/r, 2*dim/r, ...}
    aqft = qft_circuit(L, m=m, swap=True)

    per_offset = {}
    for off in offsets_to_avg:
        psi_in = periodic_state(L, r, off)
        psi_out = np.asarray(Statevector(psi_in).evolve(aqft).data)
        probs = measure_probs(psi_out)
        p_success = float(sum(probs[c] for c in good_cs))
        per_offset[off] = {
            "success_prob": p_success,
            "top5_c_probs": sorted(
                [(int(i), float(probs[i])) for i in np.argsort(probs)[-5:][::-1]],
                key=lambda t: -t[1],
            ),
        }
    mean_success = float(np.mean([per_offset[o]["success_prob"] for o in offsets_to_avg]))
    lower_bound_paper = (8.0 / math.pi ** 2) * math.sin(math.pi * m / (4 * L)) ** 2
    exact_bound = 4.0 / math.pi ** 2
    return {
        "L": L, "r": r, "m": m,
        "mean_success_prob": mean_success,
        "paper_lower_bound_ProbA": lower_bound_paper,
        "paper_lower_bound_ProbQFT_4_over_pi2": exact_bound,
        "per_offset": per_offset,
    }


if __name__ == "__main__":
    t0 = time.time()
    # a=7, N=15, r=4. For L=8, 2^L=256, 256/4=64 → good c's = {0,64,128,192}.
    a, N, r = 7, 15, 4
    print(f"Period finding: f(x)={a}^x mod {N}, r={r}")

    all_results = {}
    for L in (6, 8):
        print(f"\n=== L={L} qubits (dim={2**L}) ===")
        per_m = {}
        for m in range(1, L + 1):
            res = success_prob_period_finding(L, r, m)
            per_m[m] = res
            print(f"  m={m}: success_prob (avg over offsets)={res['mean_success_prob']:.4f}  "
                  f"paper LB (8/π²)sin²(πm/4L)={res['paper_lower_bound_ProbA']:.4f}  "
                  f"exact QFT LB 4/π²={res['paper_lower_bound_ProbQFT_4_over_pi2']:.4f}")
        all_results[L] = per_m

    out = {
        "meta": {
            "paper": "quant-ph/9601018 Barenco/Ekert/Suominen/Törma 1996",
            "problem": "period finding of 7^x mod 15 (period r=4)",
            "elapsed_sec": time.time() - t0,
        },
        "results": all_results,
    }
    out_path = os.path.join(os.path.dirname(__file__), "results_period_finding.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")
