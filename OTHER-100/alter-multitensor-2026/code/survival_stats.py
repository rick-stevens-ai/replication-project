"""
survival_stats.py
=================

Survival-analysis utilities for scoring the Alter et al. 2026 NBL predictors
against Table I:

    * Kaplan-Meier per-group median survival
    * Log-rank test (any number of groups)
    * Cox univariate hazard ratio + 95% CI + Wald p-value
    * Harrell's concordance index (C-index)

If `lifelines` is installed, it is used (preferred — battle-tested, matches
R's survival package to machine precision). Otherwise we fall back to a
SciPy/NumPy reference implementation that is correct for the use cases in
this project (two-group log-rank, univariate Cox, Harrell C).

Conventions
-----------
* `times` : (N,) float array of follow-up times (any positive units).
* `events`: (N,) int array (1 = event observed, 0 = censored).
* `groups`: (N,) int array of group labels (any nonnegative integers).
* `x`    : (N,) float covariate (for Cox/C-index).

Target Table I numbers for reference (combined predictor, n=90):
    log-rank P = 2.3e-5, HR = 4.0 (95% CI 2.0-8.1), Wald P = 8.6e-5,
    Harrell C = 0.80.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

try:
    import lifelines                              # noqa: F401
    from lifelines import CoxPHFitter, KaplanMeierFitter
    from lifelines.statistics import logrank_test, multivariate_logrank_test
    from lifelines.utils import concordance_index as ll_concordance_index
    _HAVE_LIFELINES = True
except ImportError:                              # pragma: no cover
    _HAVE_LIFELINES = False


# ---------------------------------------------------------------------------
# Kaplan-Meier
# ---------------------------------------------------------------------------

@dataclass
class KMResult:
    group: int
    n: int
    n_events: int
    median: Optional[float]      # None if not reached


def kaplan_meier_medians(times: np.ndarray,
                         events: np.ndarray,
                         groups: np.ndarray) -> List[KMResult]:
    """Return per-group Kaplan-Meier median survival times."""
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)
    groups = np.asarray(groups, dtype=int)
    out: List[KMResult] = []
    for g in sorted(np.unique(groups).tolist()):
        mask = groups == g
        t = times[mask]
        e = events[mask]
        n = int(mask.sum())
        n_ev = int(e.sum())
        med = _km_median(t, e)
        out.append(KMResult(group=g, n=n, n_events=n_ev, median=med))
    return out


def _km_median(times: np.ndarray, events: np.ndarray) -> Optional[float]:
    """Median of the Kaplan-Meier survival curve. Returns None if not reached."""
    if _HAVE_LIFELINES:
        kmf = KaplanMeierFitter()
        kmf.fit(times, event_observed=events)
        med = kmf.median_survival_time_
        if np.isinf(med) or np.isnan(med):
            return None
        return float(med)

    # Fallback: build step function from event times.
    order = np.argsort(times)
    t_sorted = times[order]
    e_sorted = events[order]
    surv = 1.0
    n_at_risk = len(times)
    prev_t = 0.0
    median = None
    last_surv = 1.0
    for t, e in zip(t_sorted, e_sorted):
        if e == 1:
            surv = surv * (1 - 1.0 / n_at_risk)
        if surv <= 0.5 and last_surv > 0.5:
            median = float(t)
            break
        last_surv = surv
        n_at_risk -= 1
    return median


# ---------------------------------------------------------------------------
# Log-rank test
# ---------------------------------------------------------------------------

@dataclass
class LogRankResult:
    statistic: float
    df: int
    p_value: float


def log_rank(times: np.ndarray,
             events: np.ndarray,
             groups: np.ndarray) -> LogRankResult:
    """Multi-group log-rank test. df = (#groups - 1)."""
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)
    groups = np.asarray(groups, dtype=int)
    uniq = sorted(np.unique(groups).tolist())
    G = len(uniq)
    if G < 2:
        raise ValueError("log_rank needs >= 2 groups")

    if _HAVE_LIFELINES:
        if G == 2:
            g0, g1 = uniq
            m0 = groups == g0
            m1 = groups == g1
            res = logrank_test(times[m0], times[m1],
                               event_observed_A=events[m0],
                               event_observed_B=events[m1])
            return LogRankResult(statistic=float(res.test_statistic),
                                 df=1, p_value=float(res.p_value))
        res = multivariate_logrank_test(times, groups, events)
        return LogRankResult(statistic=float(res.test_statistic),
                             df=G - 1, p_value=float(res.p_value))

    # SciPy fallback: build the standard observed-minus-expected vector and
    # its covariance, then a chi^2 statistic on (G-1) df.
    from scipy import stats
    # Unique event times across all groups.
    ev_mask = events == 1
    ev_times = np.sort(np.unique(times[ev_mask]))
    # For each event time, count at-risk & events per group.
    O = np.zeros(G)           # observed events per group, summed across t
    V = np.zeros((G, G))      # covariance matrix
    E = np.zeros(G)
    for t in ev_times:
        at_risk_idx = times >= t
        n_at_risk_total = int(at_risk_idx.sum())
        d_total = int(((times == t) & ev_mask).sum())
        if n_at_risk_total == 0 or d_total == 0:
            continue
        per_grp_at_risk = np.array(
            [int(((groups == g) & at_risk_idx).sum()) for g in uniq],
            dtype=float)
        per_grp_obs = np.array(
            [int(((groups == g) & (times == t) & ev_mask).sum())
             for g in uniq], dtype=float)
        expected = per_grp_at_risk * d_total / n_at_risk_total
        O += per_grp_obs
        E += expected
        if n_at_risk_total > 1:
            var_factor = (d_total * (n_at_risk_total - d_total)) / (
                (n_at_risk_total - 1) * n_at_risk_total ** 2)
            # V_{ij} = var_factor * n_at_risk_total * (n_i * delta_{ij} - n_i n_j / n_at_risk_total)
            for i in range(G):
                for j in range(G):
                    if i == j:
                        V[i, j] += var_factor * per_grp_at_risk[i] * (
                            n_at_risk_total - per_grp_at_risk[i])
                    else:
                        V[i, j] -= var_factor * per_grp_at_risk[i] * per_grp_at_risk[j]
    diff = O - E
    # Drop one component (rank G-1 covariance).
    diff_red = diff[:-1]
    V_red = V[:-1, :-1]
    try:
        chi2 = float(diff_red @ np.linalg.solve(V_red, diff_red))
    except np.linalg.LinAlgError:
        chi2 = float(np.nan)
    p = float(stats.chi2.sf(chi2, df=G - 1)) if np.isfinite(chi2) else float("nan")
    return LogRankResult(statistic=chi2, df=G - 1, p_value=p)


# ---------------------------------------------------------------------------
# Cox univariate
# ---------------------------------------------------------------------------

@dataclass
class CoxResult:
    coef: float        # log hazard ratio (beta)
    hr: float          # exp(beta)
    se: float
    ci_lower: float
    ci_upper: float
    wald_p: float


def cox_univariate(times: np.ndarray,
                   events: np.ndarray,
                   x: np.ndarray) -> CoxResult:
    """Univariate Cox proportional hazards: hazard(t | x) = h0(t) exp(beta x).

    Uses lifelines.CoxPHFitter when available; else a Newton-Raphson on
    Breslow's partial likelihood for the single-covariate case.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)
    x = np.asarray(x, dtype=float)

    if _HAVE_LIFELINES:
        import pandas as pd
        df = pd.DataFrame({"T": times, "E": events, "x": x})
        cph = CoxPHFitter()
        cph.fit(df, duration_col="T", event_col="E")
        s = cph.summary.iloc[0]
        return CoxResult(
            coef=float(s["coef"]),
            hr=float(s["exp(coef)"]),
            se=float(s["se(coef)"]),
            ci_lower=float(s["exp(coef) lower 95%"]),
            ci_upper=float(s["exp(coef) upper 95%"]),
            wald_p=float(s["p"]),
        )

    # SciPy fallback: Newton-Raphson on log partial likelihood.
    from scipy import stats
    beta = 0.0
    for _ in range(100):
        eta = beta * x
        w = np.exp(eta)
        # Risk sets at each event time.
        order = np.argsort(-times)  # decreasing time => cumulative sums = risk sets
        t_sorted = times[order]
        w_sorted = w[order]
        x_sorted = x[order]
        e_sorted = events[order]
        cum_w = np.cumsum(w_sorted)
        cum_wx = np.cumsum(w_sorted * x_sorted)
        cum_wxx = np.cumsum(w_sorted * x_sorted ** 2)
        # For ties handle via Breslow's approximation (we just use ordering).
        score = 0.0
        info = 0.0
        # Map back to original order by iterating events in sorted order.
        for k in range(len(times)):
            if e_sorted[k] == 1:
                m = cum_wx[k] / cum_w[k]
                score += x_sorted[k] - m
                info += cum_wxx[k] / cum_w[k] - m ** 2
        if info <= 0 or not np.isfinite(info):
            break
        step = score / info
        beta_new = beta + step
        if not np.isfinite(beta_new):
            break
        if abs(step) < 1e-9:
            beta = beta_new
            break
        beta = beta_new
    se = 1.0 / np.sqrt(info) if info > 0 else float("nan")
    hr = float(np.exp(beta))
    ci_lower = float(np.exp(beta - 1.96 * se))
    ci_upper = float(np.exp(beta + 1.96 * se))
    wald = beta / se if se > 0 else 0.0
    p = 2.0 * (1.0 - stats.norm.cdf(abs(wald)))
    return CoxResult(coef=float(beta), hr=hr, se=float(se),
                     ci_lower=ci_lower, ci_upper=ci_upper, wald_p=float(p))


# ---------------------------------------------------------------------------
# Harrell's concordance index
# ---------------------------------------------------------------------------

def concordance_index(times: np.ndarray,
                      events: np.ndarray,
                      risk_score: np.ndarray) -> float:
    """Harrell's C-index. Higher risk_score should predict shorter survival
    (i.e. risk_score = +beta x from Cox, NOT -beta x). For an arbitrary
    predictor where larger values mean "high-risk group", that convention
    holds; if reversed, use 1 - C.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)
    risk_score = np.asarray(risk_score, dtype=float)
    if _HAVE_LIFELINES:
        # lifelines convention: predicted_scores higher => longer survival.
        # We pass -risk_score so "higher risk -> shorter survival".
        return float(ll_concordance_index(times, -risk_score, events))

    n = len(times)
    num = 0.0
    den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            # Comparable pair: earlier time has event observed.
            ti, tj = times[i], times[j]
            ei, ej = events[i], events[j]
            if ti == tj and not (ei or ej):
                continue
            if ti < tj and ei == 1:
                den += 1
                if risk_score[i] > risk_score[j]:
                    num += 1
                elif risk_score[i] == risk_score[j]:
                    num += 0.5
            elif tj < ti and ej == 1:
                den += 1
                if risk_score[j] > risk_score[i]:
                    num += 1
                elif risk_score[i] == risk_score[j]:
                    num += 0.5
            elif ti == tj and (ei or ej):
                den += 1
                num += 0.5
    return float(num / den) if den > 0 else float("nan")


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------

def report(times: np.ndarray,
           events: np.ndarray,
           groups: np.ndarray,
           label: str = "predictor") -> Dict[str, object]:
    """One-shot bundle: KM medians + log-rank + Cox(univariate on group as
    ordered integer) + Harrell C. Returns a dict suitable for printing."""
    kms = kaplan_meier_medians(times, events, groups)
    lr = log_rank(times, events, groups)
    cox = cox_univariate(times, events, groups.astype(float))
    cidx = concordance_index(times, events, groups.astype(float))
    return {
        "label": label,
        "n_total": int(len(times)),
        "n_events": int(events.sum()),
        "groups": [(km.group, km.n, km.n_events,
                    None if km.median is None else round(km.median, 3))
                   for km in kms],
        "logrank_chi2": round(lr.statistic, 4),
        "logrank_df": lr.df,
        "logrank_p": lr.p_value,
        "cox_hr": round(cox.hr, 4),
        "cox_ci": (round(cox.ci_lower, 4), round(cox.ci_upper, 4)),
        "cox_wald_p": cox.wald_p,
        "concordance": round(cidx, 4),
        "engine": "lifelines" if _HAVE_LIFELINES else "scipy-fallback",
    }


if __name__ == "__main__":
    # Smoke test on synthetic two-group data with strong separation.
    rng = np.random.default_rng(0)
    n = 60
    groups = np.array([0] * (n // 2) + [1] * (n // 2))
    # Low-risk group: mean survival 5; high-risk group: mean survival 1.5.
    times_lo = rng.exponential(scale=5.0, size=n // 2)
    times_hi = rng.exponential(scale=1.5, size=n // 2)
    times = np.concatenate([times_lo, times_hi])
    events = np.ones(n, dtype=int)   # all observed
    rep = report(times, events, groups, label="synthetic_two_group")
    for k, v in rep.items():
        print(f"{k:>20}: {v}")
