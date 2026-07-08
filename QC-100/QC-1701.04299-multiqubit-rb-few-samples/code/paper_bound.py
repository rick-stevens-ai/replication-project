"""
Evaluate the Helsen et al. 2019 variance bound (eq. 10, no-SPAM) and
their SPAM-including bound (eq. 11) for our 2-qubit RB experiment,
and derive the number of sequences N needed for a 99% CI of size epsilon.

Bounds (from arXiv:1701.04299):

  V2_m  <=  f^(m-1) * (d^2 - 2)/(4 (d-1)^2)          * r^2
           + u^(m-2) * (d^2 m (m-1))/(2 (d-1)^2)     * r^2      (eq. 10)

  V2_SPAM <= (d^2 - 2)/(4 (d-1)^2)                       * r^2 m f^(m-1)
           + (d^2 (1+4 eta))/(d-1)^2 * r^2 (m-1) * (u^(2m-1) - (f^2/u)^m + 1) / (1 - f^2/u)^2 * u^(m-2)
           + (2 eta d m r^(m-1) f)/(d-1)                                         (eq. 11)

For a two-sided (1 - delta) confidence interval of size epsilon using the
Chebyshev / variance-based approach used in the paper (see eq. 5 / sec IV D),
the number of independent random sequences needed is

   N >= V2_m / (delta * epsilon^2)                       (Chebyshev)

For a fixed sequence length m we take the *worst-case m across the lengths
used* to get a per-m N. The paper's headline example (d=2, m=100, r=1e-4,
epsilon=1e-2, 99% CI => delta=0.01) yields N=173. We reproduce the formula
first for that scenario as a sanity check, then apply it to our own
2-qubit experiment.
"""

import json
import os

import numpy as np

D_1Q = 2
D_2Q = 4


def bound_no_spam(m, d, r, f=None, u=None):
    if f is None:
        # depolarizing parameter: f = 1 - r * d/(d-1)
        f = 1 - r * d / (d - 1)
    if u is None:
        u = (1 + f ** 2) / 2  # partially coherent noise assumption from paper
    term1 = (d ** 2 - 2) / (4 * (d - 1) ** 2) * (r ** 2) * m * (f ** (m - 1))
    term2 = (d ** 2 * m * (m - 1)) / (2 * (d - 1) ** 2) * (r ** 2) * (u ** (m - 2))
    return f ** (m - 1) * ((d ** 2 - 2) / (4 * (d - 1) ** 2) * r ** 2) \
        + (u ** (m - 2) * (d ** 2 * m * (m - 1)) / (2 * (d - 1) ** 2)) * r ** 2


def N_from_variance(V, delta, epsilon):
    return V / (delta * epsilon ** 2)


def sanity_paper_example():
    # d=2, m=100, r=1e-4, epsilon=1e-2, delta=0.01 -> paper says N=173 (single-qubit, SPAM-free)
    m, d, r = 100, 2, 1e-4
    epsilon, delta = 1e-2, 1e-2
    V = bound_no_spam(m, d, r)
    N = int(np.ceil(N_from_variance(V, delta, epsilon)))
    return dict(m=m, d=d, r=r, epsilon=epsilon, delta=delta,
                V=V, N=N, paper_N=173)


def our_experiment(r_our, lengths):
    """Compute the paper's implied N for our depolarizing 2-qubit RB."""
    d = D_2Q
    epsilon = 1e-2
    delta = 1e-2
    # take worst-case m across our lengths (early m usually dominates for small r)
    Ns = {}
    for m in lengths:
        V = bound_no_spam(m, d, r_our)
        Ns[m] = int(np.ceil(N_from_variance(V, delta, epsilon)))
    return dict(r=r_our, epsilon=epsilon, delta=delta, N_per_m=Ns,
                N_worst=max(Ns.values()))


def main():
    HERE = os.path.dirname(os.path.abspath(__file__))
    ev = os.path.join(HERE, "..", "report", "evidence")

    # Load our fitted r
    with open(os.path.join(ev, "rb_bootstrap_summary.json")) as f:
        summary = json.load(f)
    r_ref = summary["fit_full"]["r"]

    with open(os.path.join(ev, "rb_raw_survivals.json")) as f:
        raw = json.load(f)
    lengths = raw["config"]["lengths"]

    out = {"paper_example": sanity_paper_example(),
           "our_experiment": our_experiment(r_ref, lengths),
           "r_ref": r_ref}

    print("Paper example (d=2, m=100, r=1e-4, eps=1e-2, 99% CI):")
    px = out["paper_example"]
    print(f"  Our N from eq. (10)+Chebyshev: {px['N']}  (paper: {px['paper_N']})")
    print("  (paper uses eq. 9, not eq. 10, so ours will be an overestimate)")

    print("\nOur 2-qubit experiment: r_ref =", r_ref)
    oe = out["our_experiment"]
    print(f"  epsilon=1e-2, delta=1e-2, per-m N:")
    for m, N in oe["N_per_m"].items():
        print(f"    m={m:4d}   N={N}")
    print(f"  Worst-case N across our lengths: {oe['N_worst']}")

    # Compare against our empirical relative_std
    print("\nEmpirical relative_std (from bootstrap) vs N:")
    for N, row in summary["per_N"].items():
        print(f"  N={N:>3}  r_std/r={row['relative_std']:.4f}  bias={row['bias_vs_reference']:.6f}")

    out_path = os.path.join(ev, "paper_bound_comparison.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
