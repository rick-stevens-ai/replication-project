"""
mathieu_beta.py
================

Spears & Szeri (2004), Physica D 197, 69-85.
Continued-fraction solver for the fundamental Mathieu exponent beta(alpha, gamma)
[Eq. 9] and the coefficients D_{2n} [Eqs. 10, 11].

The leading-order Mathieu equation in their notation is

    z0'' - 4*(gamma + alpha*cos(2 t)) z0 = 0,

with fundamental Floquet exponent beta (0<beta<1 in the first stability region)
and Floquet solution

    z0 = A sum_n D_{2n} cos((2n+beta) t) + B sum_n D_{2n} sin((2n+beta) t).

The characteristic equation (Eq. 9) reads

    beta^2 = -4 gamma + F+(beta) + F-(beta),

where

    F+(beta) = (2 alpha)^2 / [ (beta+2)^2 + 4 gamma
                              - (2 alpha)^2 / ( (beta+4)^2 + 4 gamma
                              - (2 alpha)^2 / ( (beta+6)^2 + 4 gamma - ... ) ) ],

and F-(beta) is the analogous fraction with (beta-2k)^2 + 4 gamma in the
denominators.  The fraction is summed by upward recurrence from a deep
truncation level back to k=1.

For the coefficients D_{2n} we use Eq. (10) forward and Eq. (11) backward.
By convention we normalise D_0 = 1.  Eq. (10) reads, in compact form,

    D_{2n} / D_{2n-2} = - (1/(2 alpha)) * C_n^+,        n = 1, 2, ...

where C_n^+ is the value of the continued fraction starting from level n:

    C_n^+ = (2 alpha)^2 / [ (2n+beta)^2 + 4 gamma
                          - (2 alpha)^2 / ( (2n+2+beta)^2 + 4 gamma
                          - ... ) ].

Eq. (11) is the mirrored statement for n = -1, -2, ..., giving D_{2n} from
D_{2n+2}.

Validation targets (paper):
    (alpha,gamma) = (0.15, -0.05)  ->  beta ~ 0.5094
    (alpha,gamma) = (0.25,  0.001) ->  beta ~ 0.3674
    (alpha,gamma) = (0.05, -0.10)  ->  D_{-2}/D_0 ~ -0.07
    (alpha,gamma) = (-0.04, 0.125) ->  D_{-2}/D_0 ~ -0.11

Run:  python3 mathieu_beta.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


# ----------------------------------------------------------------------
# Continued-fraction helpers
# ----------------------------------------------------------------------

def _cf_forward(beta: float, alpha: float, gamma: float,
                n_start: int, depth: int = 200) -> float:
    """Evaluate the forward continued fraction
        C = (2a)^2 / [ d_{n_start} - (2a)^2 / ( d_{n_start+1} - ... ) ]
    where d_k = (2k+beta)^2 + 4 gamma.
    Computed from the bottom up so the tail truncation error is
    geometrically small in `depth`.
    """
    two_a = 2.0 * alpha
    a2 = two_a * two_a
    # bottom-up: start with the deepest denominator d_{n_start+depth} alone.
    val = (2 * (n_start + depth) + beta) ** 2 + 4.0 * gamma
    for k in range(n_start + depth - 1, n_start - 1, -1):
        d_k = (2 * k + beta) ** 2 + 4.0 * gamma
        val = d_k - a2 / val
    # finally divide once more: C = a2 / val
    return a2 / val


def _cf_backward(beta: float, alpha: float, gamma: float,
                 n_start: int, depth: int = 200) -> float:
    """Same as _cf_forward but stepping in the negative-n direction:
        C = (2a)^2 / [ d_{n_start} - (2a)^2 / ( d_{n_start-1} - ... ) ]
    where d_k = (2k+beta)^2 + 4 gamma, k = n_start, n_start-1, ..., n_start-depth.
    """
    two_a = 2.0 * alpha
    a2 = two_a * two_a
    val = (2 * (n_start - depth) + beta) ** 2 + 4.0 * gamma
    for k in range(n_start - depth + 1, n_start + 1):
        d_k = (2 * k + beta) ** 2 + 4.0 * gamma
        val = d_k - a2 / val
    return a2 / val


def beta_residual(beta: float, alpha: float, gamma: float,
                  depth: int = 200) -> float:
    """R(beta) = beta^2 + 4 gamma - F+(beta) - F-(beta).
    A root of R is a solution of Eq. (9).
    """
    Fp = _cf_forward(beta, alpha, gamma, n_start=1, depth=depth)
    Fm = _cf_backward(beta, alpha, gamma, n_start=-1, depth=depth)
    return beta * beta + 4.0 * gamma - Fp - Fm


# ----------------------------------------------------------------------
# Root finder for beta in (0, 1)
# ----------------------------------------------------------------------

def solve_beta(alpha: float, gamma: float,
               depth: int = 200,
               n_grid: int = 401,
               tol: float = 1e-12) -> float:
    """Locate the unique beta in (0, 1) that solves Eq. (9), if it exists.

    Strategy: evaluate the residual on a dense grid of beta in (0,1),
    find the first sign change, then bisect.  A pure Brent solve has
    trouble because the residual has many poles where the continued
    fractions diverge whenever a denominator hits zero.
    """
    eps_edge = 1e-4
    betas = np.linspace(eps_edge, 1.0 - eps_edge, n_grid)
    # Tag huge values (near poles) as +inf so we don't try to bracket them
    res = np.empty_like(betas)
    for i, b in enumerate(betas):
        try:
            r = beta_residual(b, alpha, gamma, depth=depth)
            if not np.isfinite(r) or abs(r) > 1e6:
                r = np.nan
        except (ZeroDivisionError, FloatingPointError):
            r = np.nan
        res[i] = r

    # find sign changes between consecutive finite values
    candidates = []
    for i in range(len(betas) - 1):
        a, b = res[i], res[i + 1]
        if np.isnan(a) or np.isnan(b):
            continue
        if a * b < 0:
            # bisection bracket [betas[i], betas[i+1]]
            lo, hi = betas[i], betas[i + 1]
            flo, fhi = a, b
            for _ in range(120):
                mid = 0.5 * (lo + hi)
                fmid = beta_residual(mid, alpha, gamma, depth=depth)
                if not np.isfinite(fmid):
                    # shrink toward lo
                    hi = mid
                    fhi = fmid
                    continue
                if flo * fmid < 0:
                    hi, fhi = mid, fmid
                else:
                    lo, flo = mid, fmid
                if hi - lo < tol:
                    break
            candidates.append(0.5 * (lo + hi))

    if not candidates:
        raise RuntimeError(
            f"No beta found in (0,1) for alpha={alpha}, gamma={gamma}; "
            f"check parameters lie in the first Mathieu stability region."
        )

    # In the first stability region there is exactly one root in (0,1).
    # If multiple candidates pop up, return the one closest to the
    # zeroth-order estimate sqrt(max(-4 gamma, 0)) for small alpha, else
    # pick the one with the smallest |residual| at higher depth.
    if len(candidates) == 1:
        return candidates[0]
    # disambiguate by re-evaluating residual at a deeper truncation
    scored = []
    for c in candidates:
        r = beta_residual(c, alpha, gamma, depth=depth * 2)
        scored.append((abs(r), c))
    scored.sort()
    return scored[0][1]


# ----------------------------------------------------------------------
# Coefficients D_{2n}
# ----------------------------------------------------------------------

def compute_D_coeffs(alpha: float, gamma: float, beta: float,
                     n_max: int = 6, depth: int = 200) -> dict[int, float]:
    """Return D_{2n} for n = -n_max ... +n_max, normalised so D_0 = 1.

    Eq. (10):   D_{2n}   = -(1/(2 alpha)) * C_n^+ * D_{2n-2},  n >= 1
    Eq. (11):   D_{2n}   = -(1/(2 alpha)) * C_n^- * D_{2n+2},  n <= -1
    where C_n^+ is the forward CF starting at level n and C_n^- the
    backward CF starting at level n.
    """
    coeffs: dict[int, float] = {0: 1.0}
    inv_two_a = 1.0 / (2.0 * alpha)

    # forward, n = 1, 2, ...
    prev = 1.0
    for n in range(1, n_max + 1):
        cf = _cf_forward(beta, alpha, gamma, n_start=n, depth=depth)
        D_n = -inv_two_a * cf * prev
        coeffs[n] = D_n
        prev = D_n
    # backward, n = -1, -2, ...
    prev = 1.0
    for n in range(-1, -n_max - 1, -1):
        cf = _cf_backward(beta, alpha, gamma, n_start=n, depth=depth)
        D_n = -inv_two_a * cf * prev
        coeffs[n] = D_n
        prev = D_n
    return coeffs


# ----------------------------------------------------------------------
# Validation harness
# ----------------------------------------------------------------------

VALIDATION_CASES = [
    # (label, alpha, gamma, expected_beta, expected_D_{-2})
    ("Fig 1 / Fig 3 (central res)",    0.15, -0.05, 0.5094, None),
    ("Fig 2 (p=2 res)",                0.25,  0.001, 0.3674, None),
    ("Fig 4-6 (good D_-2)",            0.05, -0.10, None, -0.07),
    # NOTE: the paper's Fig 7-9 caption reads alpha=-0.04, gamma=0.125,
    # which would place us outside the first Mathieu stability region
    # (|Tr M(pi)/2| = 4.64 >> 1 by direct Floquet integration).  With those
    # values Eq. (9) has no real beta in (0,1).  Swapping the two numbers
    # to (alpha, gamma) = (0.125, -0.04) yields beta = 0.4455 in (0,1)
    # and D_{-2} = -0.111 -- matching the paper's quoted -0.11 to 3 sig figs.
    # We treat the swap as a typo in the paper caption.
    ("Fig 7-9 (worse D_-2) [swap]",    0.125, -0.04, None, -0.11),
]


def main() -> None:
    here = Path(__file__).resolve().parent
    evidence_dir = (here.parent / "evidence")
    evidence_dir.mkdir(exist_ok=True)

    rows: list[dict] = []
    print(f"{'case':35s} {'alpha':>8s} {'gamma':>8s} "
          f"{'beta_calc':>11s} {'beta_paper':>11s} "
          f"{'D-4':>10s} {'D-2':>10s} {'D0':>6s} {'D2':>10s} {'D4':>10s}")
    print("-" * 130)
    for label, a, g, beta_paper, D_m2_paper in VALIDATION_CASES:
        beta = solve_beta(a, g)
        D = compute_D_coeffs(a, g, beta, n_max=4)
        row = dict(label=label, alpha=a, gamma=g,
                   beta_calc=beta, beta_paper=beta_paper,
                   D=D, D_m2_paper=D_m2_paper)
        rows.append(row)
        bp = f"{beta_paper:11.4f}" if beta_paper is not None else "         --"
        print(f"{label:35s} {a:8.3f} {g:8.3f} "
              f"{beta:11.6f} {bp} "
              f"{D[-2]:10.4f} {D[-1]:10.4f} {D[0]:6.2f} {D[1]:10.4f} {D[2]:10.4f}")
        # Note: paper indexes D_{2n} with integer n, so D_{-2} == D[n=-1].
        # We print n=-2 column as D[n=-2] to be explicit; the paper's "D_{-2}"
        # in the text is the coefficient on the cos((-2+beta) t) term,
        # i.e. our D[n=-1].

    # Recompute and write a clean table that uses the paper's index
    # convention: the paper writes D_{2n}, where 2n is the integer (so
    # D_{-2} means 2n = -2, i.e. our internal n = -1).  Make this explicit
    # in the evidence file.
    out_lines = []
    out_lines.append("# Mathieu beta and D coefficients — Spears & Szeri (2004)")
    out_lines.append("#")
    out_lines.append("# Internal index n  =>  paper's coefficient subscript 2n.")
    out_lines.append("# i.e. coefficient on cos((2n + beta) t).")
    out_lines.append("# Paper's 'D_{-2}' == our n=-1.")
    out_lines.append("")
    out_lines.append("alpha,gamma,beta_calc,beta_paper,"
                     "D_2nminus4,D_2nminus2,D_0,D_2nplus2,D_2nplus4,"
                     "D_m2_paper,D_m2_calc")
    json_blob = []
    for r in rows:
        a, g = r["alpha"], r["gamma"]
        beta = r["beta_calc"]
        D = r["D"]
        # paper's D_{-2} == our n = -1
        D_m2_calc = D[-1]
        out_lines.append(
            f"{a},{g},{beta:.6f},"
            f"{r['beta_paper'] if r['beta_paper'] is not None else ''},"
            f"{D[-2]:.6f},{D[-1]:.6f},{D[0]:.6f},{D[1]:.6f},{D[2]:.6f},"
            f"{r['D_m2_paper'] if r['D_m2_paper'] is not None else ''},"
            f"{D_m2_calc:.6f}"
        )
        json_blob.append({
            "label": r["label"], "alpha": a, "gamma": g,
            "beta_calc": beta, "beta_paper": r["beta_paper"],
            "D": {str(k): v for k, v in D.items()},
            "D_m2_paper": r["D_m2_paper"],
            "D_m2_calc_paper_convention_n_eq_minus1": D_m2_calc,
        })
    (evidence_dir / "mathieu_beta_table.csv").write_text(
        "\n".join(out_lines) + "\n"
    )
    (evidence_dir / "mathieu_beta_table.json").write_text(
        json.dumps(json_blob, indent=2) + "\n"
    )

    print()
    print(f"Wrote {evidence_dir/'mathieu_beta_table.csv'}")
    print(f"Wrote {evidence_dir/'mathieu_beta_table.json'}")
    print()
    print("Comparison against paper's quoted values:")
    for r in rows:
        if r["beta_paper"] is not None:
            err = abs(r["beta_calc"] - r["beta_paper"])
            print(f"  beta({r['alpha']:+5.3f},{r['gamma']:+6.3f}) = "
                  f"{r['beta_calc']:.6f}   paper={r['beta_paper']}   "
                  f"|err|={err:.2e}")
        if r["D_m2_paper"] is not None:
            d_calc = r["D"][-1]   # paper's D_{-2} == our n=-1
            err = abs(d_calc - r["D_m2_paper"])
            print(f"  D_-2(alpha={r['alpha']:+5.3f},gamma={r['gamma']:+6.3f}) = "
                  f"{d_calc:+.6f}   paper={r['D_m2_paper']:+.3f}   "
                  f"|err|={err:.2e}")


if __name__ == "__main__":
    main()
