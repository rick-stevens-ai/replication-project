#!/usr/bin/env python3
"""
Minimal runnable smoke for LUCID100 slot 28 (Koturbash et al. 2016, dvw025).

The paper's only computational content is:
  * Student's t-test (one-tailed/two-tailed not specified) with Bonferroni
    correction at alpha/m = 0.05/5 = 0.01 for the DNA-damage and Western
    blot panels (Fig 2, 3, 4, 5).
  * One-way ANOVA + Tukey HSD on behavioral data (Fig 6, 7).

There is no raw data, no omics, no model. This smoke confirms that the
Bonferroni threshold is implemented correctly and that, on FELDIR-shaped
synthetic data (cerebellum fold-change ~1.5x reported on Day 1, 6 h),
the test rejects H0 at alpha = 0.01 as the paper reports.

PASS criterion:
  * alpha_corrected == 0.01 exactly
  * synthetic cerebellum 1.5x signal rejects H0 at alpha=0.01
  * synthetic null (no signal) fails to reject at alpha=0.01

No external data, no network. Runtime well under 1 s.
"""
from __future__ import annotations
import math
import statistics
from typing import Sequence


def bonferroni_alpha(alpha: float, m: int) -> float:
    """Return per-test alpha after Bonferroni correction for m tests."""
    if m <= 0:
        raise ValueError("m must be positive")
    return alpha / m


def welch_t_test(a: Sequence[float], b: Sequence[float]) -> tuple[float, float]:
    """Two-sample Welch's t-test. Returns (t_statistic, two-sided p-value).

    Uses the survival function of the t distribution via a Lentz-style
    continued fraction for the regularized incomplete beta function so
    the script has zero dependencies beyond the stdlib.
    """
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        raise ValueError("need >=2 samples per group")
    m1, m2 = statistics.fmean(a), statistics.fmean(b)
    v1, v2 = statistics.variance(a), statistics.variance(b)
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0.0:
        return (math.inf if m1 != m2 else 0.0), 0.0
    t = (m1 - m2) / se
    # Welch-Satterthwaite degrees of freedom
    df = (v1 / n1 + v2 / n2) ** 2 / (
        (v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1)
    )
    # two-sided p from t-distribution survival function
    x = df / (df + t * t)
    p = _betai(df / 2.0, 0.5, x)
    return t, p


def _betai(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a,b) via continued fraction (NR sec 6.4)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _betacf(a: float, b: float, x: float, maxit: int = 200, eps: float = 3e-7) -> float:
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            return h
    return h


def main() -> int:
    # ---- Test 1: Bonferroni threshold matches paper ---------------------------
    alpha = 0.05
    m = 5  # paper compares 5 doses to control => 5 hypotheses
    a_corr = bonferroni_alpha(alpha, m)
    assert abs(a_corr - 0.01) < 1e-12, f"expected 0.01, got {a_corr}"
    print(f"[PASS] Bonferroni alpha (0.05/5) = {a_corr:.4f} matches paper.")

    # ---- Test 2: FELDIR-shaped synthetic cerebellum 1.5x signal rejects at 0.01
    # Paper: cerebellum, Day 1 (6 h), 1.5-fold DSB increase vs sham, P < 0.005.
    # Build synthetic n=8 control DPM around mean=1.0 and n=6 treated around 1.5.
    rng_state = 20260609  # deterministic
    import random
    random.seed(rng_state)
    control = [random.gauss(1.0, 0.10) for _ in range(8)]
    treated = [random.gauss(1.5, 0.10) for _ in range(6)]
    t, p = welch_t_test(control, treated)
    assert p < a_corr, f"expected p < {a_corr}, got p={p:.3g}"
    print(f"[PASS] Synthetic 1.5x signal: t={t:.2f}, p={p:.2e} < {a_corr}.")

    # ---- Test 3: Null synthetic does NOT reject at alpha=0.01 -----------------
    random.seed(rng_state + 1)
    control2 = [random.gauss(1.0, 0.10) for _ in range(8)]
    treated2 = [random.gauss(1.0, 0.10) for _ in range(6)]
    t0, p0 = welch_t_test(control2, treated2)
    assert p0 > a_corr, f"expected null to fail to reject; got p={p0:.3g}"
    print(f"[PASS] Null sample: t={t0:.2f}, p={p0:.3f} > {a_corr}.")

    print("[OK] All smoke checks passed (Bonferroni-corrected t-test sanity).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
