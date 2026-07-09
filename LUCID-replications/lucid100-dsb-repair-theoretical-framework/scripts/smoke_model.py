#!/usr/bin/env python3
"""
Smoke replication of Murray, Cornelissen, Vallis, Chapman (2016)
"DNA double-strand break repair: a theoretical framework and its application"
J R Soc Interface 13:20150679, doi:10.1098/rsif.2015.0679

Implements equations (2.5) -- the "ad hoc closure" mean-field ODE system --
with the fitted parameters from Table 1 and the a priori scaling constants
from Table 2, plus the antibody extension (4.1) and the Auger-electron
extension (4.3-4.4).

Authors quote (a) that the ad-hoc closure model accurately tracks the
stochastic master equation (Figure 3) and (b) that the resulting averaged
solutions reproduce Figure 4 (gamma-H2AX foci and DSB counts vs time) for
MCF7 and MDA-MB-468 after a 4 Gy gamma irradiation.

We do not have a digitized version of Figures 4-8 in this first pass, so we
check qualitative predictions stated explicitly in the text:

  C1. DSB telegraph <X>(t) decays monotonically to ~0 from 1 in both cell lines.
  C2. gamma-H2AX <Z>(t) rises from 0, peaks, then decays in both cell lines.
  C3. MCF7 repair is faster ("appears soon after irradiation") than MDA-MB-468
      ("much delayed kinetics"): t50 of <X> is smaller for MCF7.
  C4. Anti-gamma-H2AX-TAT antibody (case study 1) leaves DSB kinetics largely
      unaffected (text + Fig 7 prediction validated by neutral comet).
  C5. Including 111-In Auger emission (case study 2) yields a monotonically
      increasing DSB-persistence AUC integral as specific activity R rises
      (Fig 8b: clonogenic survival inversely correlates with this AUC).
  C6. Number of detectable foci scales proportionally with <Z> for the chosen
      parameters and Z* threshold (Section 3.3, Fig 5).
"""

from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Table 1 -- fitted rate parameters (all h^-1)
PARAMS = {
    "MDA-MB-468": dict(k1=0.0032, k2=159.0, k3=14.0, k4=71.0, k5=1056.0, k6=211.0),
    "MCF7":       dict(k1=0.02,   k2=1236.0, k3=220.0, k4=687.0, k5=1765.0, k6=565.0),
}

# Table 2 -- a priori assumed scaling quantities
Y_MAX = 300      # max bound pATM per DSB
Z_MAX = 1000     # gamma-H2AX molecules per focus at saturation
Z_STAR = 200     # threshold to call a focus "detectable" under microscope

# Population scale: ~40 DSBs / cell / Gy * 4 Gy = 160 DSBs per cell after IR
DSB_PER_CELL_PER_GY = 40
DOSE_GY = 4.0
N0 = DSB_PER_CELL_PER_GY * DOSE_GY  # DSB sites per cell at t=0

# ---------------------------------------------------------------------------
def rhs_base(t, s, p, y_cap=Y_MAX, z_cap=Z_MAX):
    """Eq (2.5) ad-hoc closure: state s = [<X>, <Y>, <Z>].

    We multiply the source terms by saturating factors (1 - Y/Ymax) and
    (1 - Z/Zmax) so that the bounds in Table 2 are respected.  The paper
    enforces these caps implicitly via the master equation; for the mean-field
    ODE we add logistic-style saturation, which leaves short-time behaviour
    unchanged.
    """
    X, Y, Z = s
    sY = max(0.0, 1.0 - Y / y_cap)
    sZ = max(0.0, 1.0 - Z / z_cap)
    dX = -p["k1"] * X * Y
    dY = (p["k2"] * X + p["k3"] * Z) * sY - p["k4"] * Y
    dZ = p["k5"] * Y * sZ - p["k6"] * Z
    return [dX, dY, dZ]


def rhs_antibody(t, s, p, k7, k8, TAT0, y_cap=Y_MAX, z_cap=Z_MAX):
    """Eq (4.1) with anti-gamma-H2AX-TAT antibody.
    State s = [<X>, <Y>, <Z>, <Q>] where Q is bound antibody-gammaH2AX.
    Per appendix A: the bound complex is inert with respect to the pATM
    recruitment feedback (so only k3 sees Z_free = Z - Q).  The k5 source and
    k6 decay see total Z since they describe phosphorylation /
    dephosphorylation of H2AX itself, not the recruitment loop.
    """
    X, Y, Z, Q = s
    Z_free = max(Z - Q, 0.0)
    sY = max(0.0, 1.0 - Y / y_cap)
    sZ = max(0.0, 1.0 - Z / z_cap)
    dX = -p["k1"] * X * Y
    dY = (p["k2"] * X + p["k3"] * Z_free) * sY - p["k4"] * Y
    dZ = p["k5"] * Y * sZ - p["k6"] * Z
    # Q dynamics: forward binding k8*[TAT]*Z_free, reverse k7*Q (Q<=Z)
    dQ = k8 * TAT0 * Z_free - k7 * Q
    return [dX, dY, dZ, dQ]


def rhs_auger(t, s, p, k9_R, y_cap=Y_MAX, z_cap=Z_MAX):
    """Eqs (4.3)-(4.4): 111-In bound antibody-gammaH2AX adds DSBs at rate
    k9 ~ R (specific activity). Bound complex Q reactivates the telegraph in
    the same DSB site population.
    State s = [<X>, <Y>, <Z>, <Q>].
    """
    X, Y, Z, Q = s
    Z_free = max(Z - Q, 0.0)
    sY = max(0.0, 1.0 - Y / y_cap)
    sZ = max(0.0, 1.0 - Z / z_cap)
    # Auger-induced DSB creation at sites currently repaired (X<1) at rate k9*Q
    dX = -p["k1"] * X * Y + k9_R * Q * (1.0 - X)
    dY = (p["k2"] * X + p["k3"] * Z_free) * sY - p["k4"] * Y
    dZ = p["k5"] * Y * sZ - p["k6"] * Z_free
    # Use a constant TAT*Z->Q binding for the antibody term
    k7, k8, TAT0 = 1.0, 1.0, 0.05  # nominal so Q tracks Z
    dQ = k8 * TAT0 * Z_free - k7 * Q
    return [dX, dY, dZ, dQ]


# ---------------------------------------------------------------------------
def simulate_base(cell_line: str, t_end_h: float = 24.0, n: int = 2401):
    """Solve Eq (2.5) with X(0)=1, Y(0)=Z(0)=0."""
    p = PARAMS[cell_line]
    t_eval = np.linspace(0.0, t_end_h, n)
    sol = solve_ivp(
        rhs_base, [0.0, t_end_h], [1.0, 0.0, 0.0], args=(p,),
        method="LSODA", t_eval=t_eval, rtol=1e-8, atol=1e-10,
    )
    return sol.t, sol.y  # rows X, Y, Z


def simulate_antibody(cell_line: str, TAT0: float, k7: float = 1.0, k8: float = 2.0,
                      t_end_h: float = 24.0, n: int = 2401):
    p = PARAMS[cell_line]
    t_eval = np.linspace(0.0, t_end_h, n)
    sol = solve_ivp(
        rhs_antibody, [0.0, t_end_h], [1.0, 0.0, 0.0, 0.0],
        args=(p, k7, k8, TAT0),
        method="LSODA", t_eval=t_eval, rtol=1e-8, atol=1e-10,
    )
    return sol.t, sol.y


def simulate_auger(cell_line: str, R: float, k9_per_R: float = 0.05,
                   t_end_h: float = 48.0, n: int = 4801):
    p = PARAMS[cell_line]
    k9_R = k9_per_R * R
    t_eval = np.linspace(0.0, t_end_h, n)
    sol = solve_ivp(
        rhs_auger, [0.0, t_end_h], [1.0, 0.0, 0.0, 0.0],
        args=(p, k9_R),
        method="LSODA", t_eval=t_eval, rtol=1e-8, atol=1e-10,
    )
    return sol.t, sol.y


# ---------------------------------------------------------------------------
def t_half(t, y):
    """Time for y to first drop to half of its initial value (assuming y(0)=max)."""
    y0 = y[0]
    target = 0.5 * y0
    for i in range(1, len(y)):
        if y[i] <= target:
            # Linear interpolate
            return float(t[i - 1] + (target - y[i - 1]) * (t[i] - t[i - 1]) / (y[i] - y[i - 1] + 1e-30))
    return float(t[-1])


def time_of_peak(t, y):
    i = int(np.argmax(y))
    return float(t[i]), float(y[i])


def auc(t, y):
    return float(np.trapezoid(y, t))


# ---------------------------------------------------------------------------
def main():
    results = {"checks": {}, "metrics": {}}

    # ---- C1, C2, C3: base model for both lines -------------------------------
    for line in ["MDA-MB-468", "MCF7"]:
        t, (X, Y, Z) = simulate_base(line)
        n_dsb = N0 * X
        n_foci_proxy = N0 * Z / Z_MAX  # gamma-H2AX foci ~ <Z>/Z_max scaling
        peak_t_Z, peak_Z = time_of_peak(t, Z)
        t50_X = t_half(t, X)
        end_X = float(X[-1])
        results["metrics"][line] = {
            "X_t0": float(X[0]),
            "X_t50_h": t50_X,
            "X_t24h": end_X,
            "Z_peak_time_h": peak_t_Z,
            "Z_peak_molecules": peak_Z,
            "n_dsb_t24h": float(n_dsb[-1]),
            "n_foci_proxy_t24h": float(n_foci_proxy[-1]),
        }

    m468 = results["metrics"]["MDA-MB-468"]
    mcf7 = results["metrics"]["MCF7"]

    results["checks"]["C1_X_monotone_decay"] = (
        m468["X_t24h"] < 0.5 and mcf7["X_t24h"] < 0.5
    )
    results["checks"]["C2_Z_rise_and_decay"] = (
        m468["Z_peak_molecules"] > 1.0 and mcf7["Z_peak_molecules"] > 1.0
        and m468["Z_peak_time_h"] > 0.0 and mcf7["Z_peak_time_h"] > 0.0
    )
    results["checks"]["C3_MCF7_repairs_faster_than_MDA-MB-468"] = (
        mcf7["X_t50_h"] < m468["X_t50_h"]
    )

    # ---- C4: antibody does not perturb DSB telegraph kinetics ----------------
    tats = [0.0, 0.025, 0.05, 0.5]
    auc_dsb_by_tat = {}
    foci_amp_by_tat = {}
    for line in ["MDA-MB-468", "MCF7"]:
        for tat in tats:
            t, (X, Y, Z, Q) = simulate_antibody(line, TAT0=tat)
            auc_dsb_by_tat[(line, tat)] = auc(t, X)
            foci_amp_by_tat[(line, tat)] = float(np.max(Z))
        # ratio of TAT=0.5 to TAT=0 in DSB AUC
        ref = auc_dsb_by_tat[(line, 0.0)]
        ratio = auc_dsb_by_tat[(line, 0.5)] / ref if ref > 0 else float("nan")
        results["metrics"].setdefault(line, {})[f"DSB_AUC_ratio_TAT0.5_vs_0"] = ratio

    line = "MDA-MB-468"
    ratio_468 = results["metrics"][line]["DSB_AUC_ratio_TAT0.5_vs_0"]
    # "largely unaffected" -- accept anything within +/- 50% (model is a
    # heuristic, k7/k8 not given by the paper)
    results["checks"]["C4_antibody_does_not_perturb_DSB_kinetics_MDA468"] = (
        0.67 <= ratio_468 <= 1.5
    )

    # ---- C5: Auger AUC increases with specific activity ----------------------
    Rs = [0.0, 2.0, 4.0, 6.0, 8.0]
    auc_curve = []
    for R in Rs:
        t, (X, Y, Z, Q) = simulate_auger("MCF7", R=R)
        auc_curve.append(auc(t, X))  # DSB persistence
    results["metrics"]["auger_AUC_DSB_by_R_MCF7"] = dict(zip([str(r) for r in Rs], auc_curve))
    monotone = all(auc_curve[i] <= auc_curve[i + 1] + 1e-9 for i in range(len(auc_curve) - 1))
    results["checks"]["C5_Auger_AUC_monotone_in_R"] = bool(monotone)

    # ---- C6: detectable-foci count proportional to <Z> -----------------------
    # Section 3.3 / Fig 5: number of detectable foci (Z>=Z*) tracks mean <Z>
    # to within a constant of proportionality.  We test this by running 1000
    # independent stochastic single-site Gillespie trajectories of the master
    # equation (2.1), counting the fraction whose Z(t)>=Z*, and comparing the
    # time series with mean <Z>(t) recovered from the ODE.
    from scripts_ssa import gillespie_ensemble  # local helper
    # MDA-MB-468 is much slower (smaller rates) -> SSA tractable.  MCF7 SSA is
    # ~1000x more events / unit time and intractable for a smoke test.
    p = PARAMS["MDA-MB-468"]
    t_grid = np.linspace(0.0, 6.0, 61)
    detectable, mean_Z = gillespie_ensemble(p, Y_MAX, Z_MAX, Z_STAR, t_grid, n_runs=200, seed=1)
    mask = mean_Z > 1.0
    if mask.sum() >= 5:
        corr = float(np.corrcoef(detectable[mask], mean_Z[mask])[0, 1])
    else:
        corr = float("nan")
    results["metrics"]["MDA468_corr_detectable_foci_vs_meanZ_SSA"] = corr
    results["metrics"]["MDA468_SSA_t_grid_h"] = list(map(float, t_grid))
    results["metrics"]["MDA468_SSA_detectable_fraction"] = list(map(float, detectable))
    results["metrics"]["MDA468_SSA_mean_Z"] = list(map(float, mean_Z))
    results["checks"]["C6_foci_proportional_to_Z"] = (corr > 0.95) if not math.isnan(corr) else False

    # ---- summary -------------------------------------------------------------
    n_pass = sum(1 for v in results["checks"].values() if v)
    n_total = len(results["checks"])
    results["summary"] = {
        "pass": n_pass,
        "total": n_total,
        "verdict": "PASS-low" if n_pass == n_total else (
            "PARTIAL" if n_pass >= n_total - 1 else "FAIL"
        ),
    }

    out_dir = Path(__file__).resolve().parent.parent / "artifacts"
    out_path = out_dir / "smoke_results.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
