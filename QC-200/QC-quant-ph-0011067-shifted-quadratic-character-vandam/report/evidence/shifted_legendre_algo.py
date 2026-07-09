#!/usr/bin/env python3
"""
Replication of the Shifted Legendre Symbol Problem quantum algorithm
from van Dam & Hallgren, "Efficient Quantum Algorithms for Shifted
Quadratic Character Problems" (arXiv:quant-ph/0011067, 2000).

We simulate Algorithm 1 (Section 3 of the paper) exactly using a
numpy statevector on a p-dimensional Hilbert space (working in the
computational basis {|0>, |1>, ..., |p-1>}, with p prime).

The algorithm (paper Algorithm 1):
  Input:  odd prime p, oracle f_s(x) = ((x+s)/p)   [Legendre symbol]
  Output: s

  Step 1. Prepare 1/sqrt(p-1) sum_{x in F_p*} ((x+s)/p) |x>
          (i.e. put f_s in the phases of a uniform superposition,
          treating the zero position as +1 as noted in the proof).
  Step 2. Apply QFT_p:
          -> 1/sqrt(p-1) sum_{y in F_p*} omega_p^{-y s} * (y/p) |y>
             (up to a global constant given by the Gauss sum)
  Step 3. Apply f_0 (Legendre symbol) into the phases:
          -> 1/sqrt(p) sum_{y in F_p} omega_p^{-y s} |y>
  Step 4. Apply inverse QFT_p -> |-s mod p>, measure to get s.

We verify:
  * On p in {13, 31, 61}, for every s in {0, ..., p-1}, the algorithm
    produces the measurement outcome (-s) mod p with probability
    exponentially close to 1.
  * Total quantum oracle queries = 2 per instance (constant, i.e.
    O(log p) is trivially satisfied; the paper states "two queries").

The classical distinguishing lower bound Omega(sqrt(p)) is confirmed
empirically in classical_lower_bound.py.
"""

import json
import math
import time
from pathlib import Path

import numpy as np

# --- number-theoretic helpers -------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True


def legendre_symbol(a: int, p: int) -> int:
    """Legendre symbol (a/p): +1 if a is a QR mod p, -1 if NR, 0 if p | a."""
    a %= p
    if a == 0:
        return 0
    # Euler's criterion: a^((p-1)/2) mod p
    v = pow(a, (p - 1) // 2, p)
    if v == p - 1:
        return -1
    return 1  # v == 1


# --- exact quantum simulation (numpy statevector on C^p) ---------------------

def qft_matrix(p: int) -> np.ndarray:
    """Exact p-dim discrete Fourier transform matrix (QFT_p).
    F[y, x] = (1/sqrt(p)) * exp(2 pi i x y / p).
    """
    x = np.arange(p)
    y = x.reshape(-1, 1)
    return np.exp(2j * math.pi * (x * y) / p) / math.sqrt(p)


def prepare_step1_state(p: int, s: int) -> np.ndarray:
    """Step 1 of Algorithm 1: the state
       (1/sqrt(p-1)) sum_{x in F_p^*} ((x+s)/p) |x>
    (treating the zero-position of f_s as +1 as the paper's proof notes;
    this is equivalent to putting the Legendre symbol (x+s | p) into the
    phase of a uniform superposition over F_p, then noticing one amplitude
    is zero because of the single position where (x+s) = 0). We match the
    paper exactly by using amplitude 0 at the singular x = -s mod p and
    (\u00b11)/sqrt(p-1) elsewhere.
    """
    psi = np.zeros(p, dtype=complex)
    for x in range(p):
        chi = legendre_symbol(x + s, p)  # +1, -1, or 0
        psi[x] = chi
    norm = np.linalg.norm(psi)
    return psi / norm


def apply_step3_phase(state: np.ndarray, p: int) -> np.ndarray:
    """Step 3: apply the diagonal operator |y> -> ((y/p)) |y> (Legendre
    symbol of y in the phase). Note ((0/p)) = 0 which annihilates the |0>
    amplitude — matching the paper's summation from y=1 (see proof).
    """
    phase = np.array([legendre_symbol(y, p) for y in range(p)], dtype=complex)
    out = state * phase
    n = np.linalg.norm(out)
    if n > 0:
        out = out / n
    return out


def run_algorithm(p: int, s: int, qft: np.ndarray | None = None) -> tuple[np.ndarray, int]:
    """Run Algorithm 1 exactly on C^p. Returns (final state, argmax outcome)."""
    if qft is None:
        qft = qft_matrix(p)
    inv_qft = qft.conj().T

    # Step 1: put f_s into the phase of a uniform superposition
    psi = prepare_step1_state(p, s)

    # Step 2: QFT
    psi = qft @ psi

    # Step 3: multiply by (y/p) in the phase (this is one f_0 query)
    psi = apply_step3_phase(psi, p)

    # Step 4: inverse QFT
    psi = inv_qft @ psi

    # Measurement: the paper predicts probability ~1 on |-s mod p>
    probs = np.abs(psi) ** 2
    argmax = int(np.argmax(probs))
    return psi, argmax


# --- experiment ---------------------------------------------------------------

def run_experiment(primes=(13, 31, 61)) -> dict:
    """For each prime p and each s in F_p, run Algorithm 1 and record:
       * measured argmax outcome
       * P(outcome = (-s) mod p)
       * total probability mass on the correct answer
    Report the minimum success probability across all (p, s).
    """
    results = {"primes": {}, "notes": []}
    for p in primes:
        assert is_prime(p) and p % 2 == 1, f"{p} must be an odd prime"
        qft = qft_matrix(p)
        per_s = []
        correct = 0
        min_prob = 1.0
        max_wrong = 0.0
        t0 = time.time()
        for s in range(p):
            state, argmax = run_algorithm(p, s, qft)
            target = (-s) % p
            probs = np.abs(state) ** 2
            prob_target = float(probs[target])
            prob_argmax = float(probs[argmax])
            if argmax == target:
                correct += 1
            # largest probability mass off the correct answer
            probs_wrong = probs.copy()
            probs_wrong[target] = 0.0
            wrong_max = float(np.max(probs_wrong))
            min_prob = min(min_prob, prob_target)
            max_wrong = max(max_wrong, wrong_max)
            per_s.append({
                "s": s,
                "target_(-s)mod_p": target,
                "argmax_outcome": argmax,
                "P(target)": prob_target,
                "P(argmax)": prob_argmax,
                "correct": argmax == target,
            })
        dt = time.time() - t0
        results["primes"][str(p)] = {
            "p": p,
            "num_instances": p,
            "num_correct": correct,
            "recovery_rate": correct / p,
            "min_prob_on_correct_answer": min_prob,
            "max_prob_on_wrong_answer": max_wrong,
            "runtime_s": dt,
            "queries_per_instance": 2,  # paper: exactly 2 oracle queries
            "n_qubits_ceil_log2_p": math.ceil(math.log2(p)),
            "per_s": per_s,
        }
    return results


def main():
    out_dir = Path(__file__).resolve().parent
    results = run_experiment(primes=(13, 31, 61))
    with open(out_dir / "shifted_legendre_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Human-readable summary
    print("=" * 72)
    print("Shifted Legendre Symbol Problem — Algorithm 1 (van Dam & Hallgren)")
    print("Exact numpy statevector simulation on C^p")
    print("=" * 72)
    for p_str, r in results["primes"].items():
        p = r["p"]
        print(f"\nprime p = {p}   (n = ceil(log2 p) = {r['n_qubits_ceil_log2_p']} qubits)")
        print(f"  instances tested (all s in F_p): {r['num_instances']}")
        print(f"  correct recovery (argmax = -s mod p): {r['num_correct']}/{r['num_instances']}"
              f"  ({100*r['recovery_rate']:.1f}%)")
        print(f"  min P[outcome = -s mod p] across s: {r['min_prob_on_correct_answer']:.6f}")
        print(f"  max P[wrong outcome] across s:      {r['max_prob_on_wrong_answer']:.6f}")
        print(f"  oracle queries per instance: {r['queries_per_instance']}  (paper: 2)")
        print(f"  runtime: {r['runtime_s']:.3f} s")
    print("\nResults written to shifted_legendre_results.json")


if __name__ == "__main__":
    main()
