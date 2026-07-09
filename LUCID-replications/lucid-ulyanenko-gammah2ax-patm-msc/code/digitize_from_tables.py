"""
Recover absolute foci counts from Tables 1, 2, 3 of Ulyanenko et al. 2019 (IJMS 20:2645).

Key identity:
  I_REL = I_Di / I_0
  K     = (I_Di - I_0) / D_i * 100  (%)

So:
  I_Di = I_0 * I_REL
  I_Di - I_0 = K * D_i / 100
  => I_0 * (I_REL - 1) = K * D_i / 100
  => I_0 = (K * D_i / 100) / (I_REL - 1)
  => I_Di = I_REL * I_0

We have 5 dose points per dose-rate per marker. Each yields an independent estimate of
I_0 (the control mean). They should be consistent (within rounding/SEM). We use the
mean across the 5 estimates as our best I_0 and then back-compute I_Di at each dose.

This also lets us cross-check against the linear regressions reported in the text:
  gH2AX acute:  y = 2.478 + 0.021*x,  R^2 = 0.988
  gH2AX chronic:y = 2.249 + 0.008*x,  R^2 = 0.888
  pATM  acute:  y = 0.993 + 0.016*x,  R^2 = 0.997
The intercept should match I_0; the slope should ~match K_acute/100 (averaged).
"""

import numpy as np
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

DOSES = np.array([30, 100, 160, 240, 300], dtype=float)

# ---------- Table 1: I_REL for gH2AX ----------
IREL_GH2AX = {
    "chronic_0.1": {
        "mean": np.array([1.28, 1.43, 1.32, 1.93, 2.23]),
        "sem":  np.array([0.11, 0.18, 0.20, 0.36, 0.30]),
    },
    "acute_30.0": {
        "mean": np.array([1.55, 2.07, 2.78, 3.27, 4.05]),
        "sem":  np.array([0.27, 0.33, 0.45, 0.60, 0.50]),
    },
}

# ---------- Table 2: K (%) for gH2AX ----------
K_GH2AX = {
    "chronic_0.1": {
        "mean": np.array([2.03, 0.95, 0.44, 0.85, 0.90]),
        "sem":  np.array([0.74, 0.37, 0.26, 0.30, 0.19]),
    },
    "acute_30.0": {
        "mean": np.array([4.01, 2.34, 2.44, 2.07, 2.23]),
        "sem":  np.array([1.85, 0.65, 0.54, 0.48, 0.30]),
    },
}

# ---------- Table 3: K (%) for pATM ----------
K_PATM = {
    "chronic_0.1": {
        "mean": np.array([0.98, 0.59, 0.16, 0.36, 0.67]),
        "sem":  np.array([1.22, 0.34, 0.27, 0.16, 0.16]),
    },
    "acute_30.0": {
        "mean": np.array([2.18, 1.60, 1.62, 1.56, 1.66]),
        "sem":  np.array([1.35, 0.37, 0.35, 0.18, 0.26]),
    },
}


def recover_absolute(irel, k, doses):
    """Recover I_0 (control) and I_Di (per dose) from I_REL and K."""
    # Per-dose estimate of I_0
    I0_est = (k * doses / 100.0) / (irel - 1.0)
    I0 = np.mean(I0_est)
    I0_sd = np.std(I0_est, ddof=1)
    I_Di = irel * I0
    return I0, I0_sd, I_Di, I0_est


def fit_linear(x, y):
    """Simple linear regression y = a + b*x; return (a, b, R^2)."""
    p, cov = np.polyfit(x, y, 1, cov=True)
    b, a = p[0], p[1]
    yhat = a + b * x
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot
    return float(a), float(b), float(r2)


def hockey_stick(x, y, threshold):
    """Hockey-stick fit: y = a for x<=threshold, y = a + b*(x-threshold) for x>threshold.
    Returns (a, b, SSE)."""
    below = x <= threshold
    above = ~below
    # Estimate a from "below" + control; for simplicity weight control too if y has 0 entry.
    # Here we just fit a as the mean of below points, then b from above points.
    a = np.mean(y[below]) if below.any() else y[0]
    if above.any():
        # b minimizes sum((y[above] - a - b*(x[above]-threshold))^2)
        dx = x[above] - threshold
        b = np.sum(dx * (y[above] - a)) / np.sum(dx ** 2)
    else:
        b = 0.0
    yhat = np.where(x <= threshold, a, a + b * (x - threshold))
    sse = float(np.sum((y - yhat) ** 2))
    return float(a), float(b), sse


def run_marker(name, irel_data, k_data, doses, fit_intercept_check=None):
    out = {"marker": name, "doses_mGy": doses.tolist(), "by_dose_rate": {}}
    for mode in ("chronic_0.1", "acute_30.0"):
        irel = irel_data[mode]["mean"] if irel_data else None
        irel_sem = irel_data[mode]["sem"] if irel_data else None
        k = k_data[mode]["mean"]
        k_sem = k_data[mode]["sem"]
        if irel is None:
            # We don't have I_REL for pATM (Table 1 is gH2AX only).
            # Use linear fit's intercept as a proxy for I_0 only if available.
            entry = {
                "K_percent_mean": k.tolist(),
                "K_percent_sem":  k_sem.tolist(),
            }
        else:
            I0, I0_sd, I_Di, I0_est = recover_absolute(irel, k, doses)
            entry = {
                "I_REL_mean": irel.tolist(),
                "I_REL_sem":  irel_sem.tolist(),
                "K_percent_mean": k.tolist(),
                "K_percent_sem":  k_sem.tolist(),
                "I0_recovered_mean":  float(I0),
                "I0_recovered_std":   float(I0_sd),
                "I0_per_dose_estimates": I0_est.tolist(),
                "I_Di_mean": I_Di.tolist(),
            }
            # Linear fit including (0, I0)
            x_full = np.concatenate([[0.0], doses])
            y_full = np.concatenate([[I0], I_Di])
            a, b, r2 = fit_linear(x_full, y_full)
            entry["linear_fit_with_control"] = {"a": a, "b": b, "R2": r2}
            # Linear fit using doses only (no 0)
            a2, b2, r2_2 = fit_linear(doses, I_Di)
            entry["linear_fit_doses_only"] = {"a": a2, "b": b2, "R2": r2_2}
            # Hockey stick at threshold = 150 mGy
            a3, b3, sse3 = hockey_stick(x_full, y_full, 150.0)
            entry["hockey_stick_150mGy"] = {"a": a3, "b_above": b3, "SSE": sse3}
            # Hockey stick at 200 mGy (used for pATM in paper)
            a4, b4, sse4 = hockey_stick(x_full, y_full, 200.0)
            entry["hockey_stick_200mGy"] = {"a": a4, "b_above": b4, "SSE": sse4}
            # Linear-only SSE for comparison
            yhat_lin = a + b * x_full
            sse_lin = float(np.sum((y_full - yhat_lin) ** 2))
            entry["linear_fit_with_control"]["SSE"] = sse_lin
        out["by_dose_rate"][mode] = entry
    return out


def main():
    results = {
        "source": "Ulyanenko et al. 2019, IJMS 20:2645, doi:10.3390/ijms20112645",
        "method": "Algebraic recovery: I_Di = I_REL * I_0; I_0 = (K*D/100)/(I_REL-1).",
        "markers": {},
    }
    results["markers"]["gH2AX"] = run_marker("gH2AX", IREL_GH2AX, K_GH2AX, DOSES)

    # For pATM we have K only (Table 3). The paper reports the acute linear fit:
    #   y = 0.993 + 0.016*x.  We can use intercept 0.993 as I_0 for the acute mode,
    #   then I_Di = I_0 + K*D/100 (rearranged from K's definition).
    pa_acute_I0 = 0.993
    pa_acute_K = K_PATM["acute_30.0"]["mean"]
    pa_acute_I_Di = pa_acute_I0 + pa_acute_K * DOSES / 100.0

    # For chronic pATM, paper says "did not differ from control 30-160 mGy"; we
    # don't have a published intercept, but cells share a control, so I_0 should
    # match the acute control. We'll adopt I_0 = 0.993 as a working assumption.
    pa_chronic_I0 = 0.993
    pa_chronic_K = K_PATM["chronic_0.1"]["mean"]
    pa_chronic_I_Di = pa_chronic_I0 + pa_chronic_K * DOSES / 100.0

    patm_entry = {
        "marker": "pATM",
        "doses_mGy": DOSES.tolist(),
        "by_dose_rate": {
            "acute_30.0": {
                "K_percent_mean": pa_acute_K.tolist(),
                "K_percent_sem":  K_PATM["acute_30.0"]["sem"].tolist(),
                "I0_assumed":     pa_acute_I0,
                "I0_source":      "intercept of paper's reported linear fit y=0.993+0.016x",
                "I_Di_mean":      pa_acute_I_Di.tolist(),
            },
            "chronic_0.1": {
                "K_percent_mean": pa_chronic_K.tolist(),
                "K_percent_sem":  K_PATM["chronic_0.1"]["sem"].tolist(),
                "I0_assumed":     pa_chronic_I0,
                "I0_source":      "shared control with acute (same MSC population, same baseline)",
                "I_Di_mean":      pa_chronic_I_Di.tolist(),
            },
        },
    }
    # Fits
    for mode_key, I_Di in [("acute_30.0", pa_acute_I_Di), ("chronic_0.1", pa_chronic_I_Di)]:
        x_full = np.concatenate([[0.0], DOSES])
        y_full = np.concatenate([[pa_acute_I0], I_Di])
        a, b, r2 = fit_linear(x_full, y_full)
        a2, b2, r2_2 = fit_linear(DOSES, I_Di)
        a3, b3, sse3 = hockey_stick(x_full, y_full, 150.0)
        a4, b4, sse4 = hockey_stick(x_full, y_full, 200.0)
        yhat_lin = a + b * x_full
        sse_lin = float(np.sum((y_full - yhat_lin) ** 2))
        patm_entry["by_dose_rate"][mode_key].update({
            "linear_fit_with_control": {"a": a, "b": b, "R2": r2, "SSE": sse_lin},
            "linear_fit_doses_only":   {"a": a2, "b": b2, "R2": r2_2},
            "hockey_stick_150mGy":     {"a": a3, "b_above": b3, "SSE": sse3},
            "hockey_stick_200mGy":     {"a": a4, "b_above": b4, "SSE": sse4},
        })

    results["markers"]["pATM"] = patm_entry

    # Paper-reported fits for cross-check
    results["paper_reported_fits"] = {
        "gH2AX_acute":   {"a": 2.478, "b": 0.021, "R2": 0.988},
        "gH2AX_chronic": {"a": 2.249, "b": 0.008, "R2": 0.888},
        "pATM_acute":    {"a": 0.993, "b": 0.016, "R2": 0.997},
    }

    out_path = OUT / "digitized_tables.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    # Pretty-print a summary to stdout
    print("=== Recovered I_0 (control foci/cell) ===")
    for marker_key, m in results["markers"].items():
        for mode_key, dat in m["by_dose_rate"].items():
            i0 = dat.get("I0_recovered_mean") or dat.get("I0_assumed")
            print(f"  {marker_key:6s} {mode_key:13s}  I_0 = {i0:.3f}")

    print("\n=== Recovered I_Di (foci/cell) ===")
    for marker_key, m in results["markers"].items():
        for mode_key, dat in m["by_dose_rate"].items():
            print(f"  {marker_key:6s} {mode_key:13s}  doses={DOSES.tolist()}")
            print(f"    I_Di = {[round(v,3) for v in dat['I_Di_mean']]}")

    print("\n=== Our linear refit (intercept, slope, R^2) vs paper ===")
    pf = results["paper_reported_fits"]
    print(f"  Paper  gH2AX acute:   a={pf['gH2AX_acute']['a']:.3f}  b={pf['gH2AX_acute']['b']:.4f}  R^2={pf['gH2AX_acute']['R2']:.3f}")
    f = results["markers"]["gH2AX"]["by_dose_rate"]["acute_30.0"]["linear_fit_with_control"]
    print(f"  Ours   gH2AX acute:   a={f['a']:.3f}  b={f['b']:.4f}  R^2={f['R2']:.3f}")

    print(f"  Paper  gH2AX chronic: a={pf['gH2AX_chronic']['a']:.3f}  b={pf['gH2AX_chronic']['b']:.4f}  R^2={pf['gH2AX_chronic']['R2']:.3f}")
    f = results["markers"]["gH2AX"]["by_dose_rate"]["chronic_0.1"]["linear_fit_with_control"]
    print(f"  Ours   gH2AX chronic: a={f['a']:.3f}  b={f['b']:.4f}  R^2={f['R2']:.3f}")

    print(f"  Paper  pATM  acute:   a={pf['pATM_acute']['a']:.3f}  b={pf['pATM_acute']['b']:.4f}  R^2={pf['pATM_acute']['R2']:.3f}")
    f = results["markers"]["pATM"]["by_dose_rate"]["acute_30.0"]["linear_fit_with_control"]
    print(f"  Ours   pATM  acute:   a={f['a']:.3f}  b={f['b']:.4f}  R^2={f['R2']:.3f}")

    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
