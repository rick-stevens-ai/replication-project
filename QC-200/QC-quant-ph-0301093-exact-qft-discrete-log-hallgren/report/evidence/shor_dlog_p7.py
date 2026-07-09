"""
Reproduce Shor's discrete logarithm algorithm using the EXACT QFT
(as guaranteed by Mosca & Zalka 2003, quant-ph/0301093).

Setup per paper Section 3:
  "α generates a cyclic group of some finite order, here a prime.  Thus α^p = e."
  β = α^a.  Goal: find a = log_α β.
  Registers: |x, y> with x, y in Z_p (uniform superposition of p^2 basis states).
  Compute α^x β^y in a work register, measure it.
  Post-measurement:  state ∝ Σ_y |x0 - a y  (mod p), y>   (paper eq., Sec 3)
                    where arithmetic is mod p.
  Apply QFT_p on both registers.
  Measure (c, d):  the paper claims a can be recovered "in all cases except
  when x = 0", giving success probability 1 - 1/p.

We simulate this exactly for prime p = 7 and p = 11:
  - Build the pre-QFT joint statevector for each a ∈ {0, ..., p-1}.
  - Apply the EXACT QFT_p (constructed as an explicit unitary; the paper's
    result guarantees this is realizable with an exact circuit).
  - Read out the full probability distribution.
  - Compute the success probability of recovering a.
  - Compare to paper's claim (1 - 1/p).

The full pre-QFT state (uniform superposition over the coset) is treated with
x0 uniformly random -- but by translational symmetry the SUCCESS probability
is independent of x0 (only the outcome c shifts by a constant).  We fix x0 = 0.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("results_dlog.json")


def dft_matrix(N: int) -> np.ndarray:
    """The EXACT QFT_N unitary (target of Mosca-Zalka's exact circuit)."""
    j = np.arange(N)
    k = j.reshape(-1, 1)
    return np.exp(2j * np.pi * k * j / N) / np.sqrt(N)


def dlog_success_stats(p: int, a: int) -> dict:
    """Simulate Shor dlog in a cyclic group of prime order p.

    Registers of dimension p.  Post-oracle-measurement state (x0 fixed to 0):
        |ψ> = (1/sqrt(p)) Σ_y |(-a y) mod p, y>
    Then apply QFT_p ⊗ QFT_p and read out.
    """
    x0 = 0
    dim = p * p
    psi = np.zeros(dim, dtype=complex)
    for y in range(p):
        x = (x0 - a * y) % p
        psi[x * p + y] = 1.0
    psi /= np.linalg.norm(psi)

    F = dft_matrix(p)
    U = np.kron(F, F)
    phi = U @ psi
    probs = np.abs(phi) ** 2

    # ---- Recover a from measured (c, d) ----
    # For the state Σ_y |x0 - a y, y> the QFT gives non-zero amplitude only on
    # (c, d) satisfying  d ≡ a * c  (mod p)   (see standard Shor dlog analysis).
    # We recover a = d * c^{-1} mod p whenever c != 0.  Since p is prime,
    # gcd(c, p) = 1 for all c in {1, ..., p-1}.
    good_prob = 0.0
    c_zero_prob = 0.0
    for c in range(p):
        for d in range(p):
            p_out = probs[c * p + d]
            if p_out < 1e-12:
                continue
            if c == 0:
                c_zero_prob += p_out
                continue
            c_inv = pow(int(c), -1, p)
            a_est = (d * c_inv) % p
            if a_est == a:
                good_prob += p_out

    return {
        "p": p,
        "a_true": a,
        "good_recovery_prob": float(good_prob),
        "c_zero_prob": float(c_zero_prob),
        "paper_claim_1_minus_1_over_p": 1 - 1 / p,
        "phi_norm": float(np.linalg.norm(phi)),
    }


def full_dlog_averaging_over_x0(p: int, a: int) -> float:
    """Sanity check: does averaging over x0 change anything?  (It shouldn't;
    x0 just shifts c by a fixed offset in the QFT domain.)"""
    F = dft_matrix(p)
    U = np.kron(F, F)
    good_total = 0.0
    for x0 in range(p):
        psi = np.zeros(p * p, dtype=complex)
        for y in range(p):
            x = (x0 - a * y) % p
            psi[x * p + y] = 1.0
        psi /= np.linalg.norm(psi)
        phi = U @ psi
        probs = np.abs(phi) ** 2
        for c in range(p):
            for d in range(p):
                if probs[c * p + d] < 1e-12 or c == 0:
                    continue
                c_inv = pow(int(c), -1, p)
                a_est = (d * c_inv) % p
                if a_est == a:
                    good_total += probs[c * p + d]
    return good_total / p


def main() -> None:
    results: dict = {"instances": [], "avg_over_x0": []}

    for p in [7, 11]:
        for a in range(p):
            r = dlog_success_stats(p, a)
            results["instances"].append(r)
            avg = full_dlog_averaging_over_x0(p, a)
            results["avg_over_x0"].append({"p": p, "a": a, "avg_prob": avg})

    # Summarise
    summary = {}
    for row in results["instances"]:
        key = f"p={row['p']}"
        summary.setdefault(key, {"good": []})
        summary[key]["good"].append(row["good_recovery_prob"])
    for key, s in summary.items():
        vals = s["good"]
        p_ = int(key.split("=")[1])
        s["mean_success"] = float(np.mean(vals))
        s["min_success"] = float(np.min(vals))
        s["max_success"] = float(np.max(vals))
        s["n_instances"] = len(vals)
        s["paper_claim"] = 1 - 1 / p_
        s["abs_diff_from_paper"] = float(abs(np.mean(vals) - (1 - 1 / p_)))
        del s["good"]
    results["summary"] = summary

    OUT.write_text(json.dumps(results, indent=2))
    print(f"Wrote {OUT}")
    print("\nPer-instance success probabilities:")
    for row in results["instances"]:
        print(f"  p={row['p']:3d} a={row['a_true']:3d}: "
              f"prob={row['good_recovery_prob']:.5f}  "
              f"(paper 1-1/p={row['paper_claim_1_minus_1_over_p']:.5f})")
    print("\nSummary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
