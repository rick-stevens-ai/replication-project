#!/usr/bin/env python3
"""
audit_horst2024.py
==================

Real-data replication audit for:
  Horst et al. (2024). "Dose and dose rate dependence of the tissue sparing
  effect at ultra-high dose rate studied for proton and electron beams using
  the zebrafish embryo model." Radiother Oncol 194:110197.

Pipeline:
  1. Load digitized Figure 1 (12 panels: 4 endpoints x 3 beams; REF + UHDR).
  2. Fit the paper's exact NTCP model:
       NTCP(D) = a * 2^(-exp(b * (1 - D/c)))
     - a fixed at 1 for {pericardial_edema, curved_spine} (classical NTCP).
     - a fitted freely for {embryo_length, eye_diameter}.
  3. Compute iso-effect FMF(D) = D_REF(y) / D_UHDR(y) by inverting the fits
     over the dose range, and report curve summary stats including the
     saturating FMF in the 50-95 Gy band.
  4. Compare to Figure 3 digitization (paper's reported FMFs).
  5. Compare claim by claim:
       - "FMF saturates at ~0.7-0.8 above ~50 Gy"
       - "Magnitude comparable across the four endpoints"
       - "Less sparing for proton beams than electron beam"
       - "~10% RBE shift for SOBP vs proton entrance / electron at REF"

Outputs:
  results/fit_params.csv
  results/fmf_per_panel.csv
  results/fmf_compare_to_paper.csv
  results/claim_audit.csv
  figures/audit_panel_<endpoint>_<beam>.png  (per panel)
  figures/audit_fmf_panelA_electron.png
  figures/audit_fmf_panelB_spine_threebeams.png
"""
from __future__ import annotations
import csv, math, os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
RES = ROOT / "results"
FIG.mkdir(exist_ok=True, parents=True)
RES.mkdir(exist_ok=True, parents=True)

BEAMS = ("proton_entrance", "proton_SOBP", "electron_30MeV")
ENDPOINTS = ("pericardial_edema", "curved_spine", "embryo_length", "eye_diameter")
A_FIXED_ENDPOINTS = {"pericardial_edema", "curved_spine"}


def ntcp_a_fixed(D, b, c):
    D = np.asarray(D, dtype=float)
    return 1.0 * np.power(2.0, -np.exp(b * (1.0 - D / np.clip(c, 1e-6, None))))


def ntcp_a_free(D, a, b, c):
    D = np.asarray(D, dtype=float)
    return a * np.power(2.0, -np.exp(b * (1.0 - D / np.clip(c, 1e-6, None))))


def fit_panel(doses, response, a_fixed: bool):
    """Fit Horst 2024 NTCP form. Returns dict with params and inverse function."""
    doses = np.asarray(doses, dtype=float)
    response = np.asarray(response, dtype=float)
    # Initial guess based on data scale
    y_max = max(np.max(response), 1e-6)
    # D50 = dose at half max
    half = y_max / 2.0
    try:
        # find rough D50 by linear interp
        order = np.argsort(doses)
        ds = doses[order]; ys = response[order]
        if ys[-1] < half:
            d50_guess = ds[-1] * 0.8
        else:
            d50_guess = float(np.interp(half, ys, ds))
        if not np.isfinite(d50_guess) or d50_guess <= 0:
            d50_guess = float(np.median(doses[doses > 0])) if np.any(doses > 0) else 30.0
    except Exception:
        d50_guess = 30.0

    if a_fixed:
        # 2 params: b, c
        p0 = [3.0, d50_guess]
        bounds = ([0.1, 1.0], [30.0, 500.0])
        popt, pcov = curve_fit(ntcp_a_fixed, doses, response, p0=p0, bounds=bounds, maxfev=20000)
        a, b, c = 1.0, popt[0], popt[1]
        fn = lambda D, _a=a, _b=b, _c=c: _a * np.power(2.0, -np.exp(_b * (1.0 - np.asarray(D, dtype=float) / _c)))
    else:
        # 3 params
        a_guess = max(y_max * 1.05, 0.01)
        p0 = [a_guess, 3.0, d50_guess]
        bounds = ([0.001, 0.1, 1.0], [200.0, 30.0, 500.0])
        popt, pcov = curve_fit(ntcp_a_free, doses, response, p0=p0, bounds=bounds, maxfev=20000)
        a, b, c = popt
        fn = lambda D, _a=a, _b=b, _c=c: _a * np.power(2.0, -np.exp(_b * (1.0 - np.asarray(D, dtype=float) / _c)))

    # Quality
    pred = fn(doses)
    ss_res = float(np.sum((response - pred) ** 2))
    ss_tot = float(np.sum((response - np.mean(response)) ** 2)) or 1e-9
    r2 = 1.0 - ss_res / ss_tot
    return dict(a=float(a), b=float(b), c=float(c), r2=r2, n=len(doses), fn=fn)


def invert(fn, y_target, d_min=0.5, d_max=300.0):
    """Find D such that fn(D) = y_target on a monotonic-rising portion of fn."""
    try:
        f0 = fn(d_min) - y_target
        f1 = fn(d_max) - y_target
        if f0 * f1 > 0:
            # Search a finer grid for sign change
            grid = np.linspace(d_min, d_max, 400)
            vals = fn(grid) - y_target
            sign_changes = np.where(np.diff(np.sign(vals)))[0]
            if len(sign_changes) == 0:
                return float("nan")
            i = sign_changes[0]
            return float(brentq(lambda D: float(fn(D) - y_target), grid[i], grid[i + 1]))
        return float(brentq(lambda D: float(fn(D) - y_target), d_min, d_max))
    except Exception:
        return float("nan")


def main():
    fig1_csv = DATA / "horst2024_fig1_digitized.csv"
    if not fig1_csv.exists():
        print("MISSING:", fig1_csv, file=sys.stderr); sys.exit(2)

    rows = []
    with open(fig1_csv) as f:
        for r in csv.DictReader(f):
            rows.append({"beam": r["beam"], "endpoint": r["endpoint"],
                         "dose_rate": r["dose_rate"], "dose_Gy": float(r["dose_Gy"]),
                         "response": float(r["response"])})

    # ===== fits =====
    fits = {}  # (endpoint, beam, dose_rate) -> dict
    fit_params_rows = []
    for endpoint in ENDPOINTS:
        for beam in BEAMS:
            for dose_rate in ("REF", "UHDR"):
                pts = [r for r in rows if r["endpoint"] == endpoint and r["beam"] == beam and r["dose_rate"] == dose_rate]
                if len(pts) < 4:
                    print(f"[warn] skipping {endpoint} {beam} {dose_rate}: only {len(pts)} pts")
                    continue
                D = np.array([p["dose_Gy"] for p in pts])
                Y = np.array([p["response"] for p in pts])
                fit = fit_panel(D, Y, a_fixed=(endpoint in A_FIXED_ENDPOINTS))
                fits[(endpoint, beam, dose_rate)] = fit
                fit_params_rows.append(dict(endpoint=endpoint, beam=beam, dose_rate=dose_rate,
                                            a=fit["a"], b=fit["b"], c=fit["c"], r2=fit["r2"], n=fit["n"]))
                print(f"  fit {endpoint:18s} {beam:18s} {dose_rate:4s}  a={fit['a']:.3f}  b={fit['b']:.3f}  c={fit['c']:.2f}  r2={fit['r2']:.3f}  n={fit['n']}")

    with open(RES / "fit_params.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["endpoint", "beam", "dose_rate", "a", "b", "c", "r2", "n"])
        w.writeheader(); w.writerows(fit_params_rows)

    # ===== iso-effect FMF =====
    # For each panel, scan iso-effect levels and compute FMF = D_REF / D_UHDR
    fmf_rows = []
    for endpoint in ENDPOINTS:
        for beam in BEAMS:
            ref = fits.get((endpoint, beam, "REF"))
            uhdr = fits.get((endpoint, beam, "UHDR"))
            if not ref or not uhdr:
                continue
            a_min = min(ref["a"], uhdr["a"])
            # Sweep iso-effects from 5% to 95% of min(a)
            levels = np.linspace(0.10 * a_min, 0.95 * a_min, 18)
            for y in levels:
                d_ref = invert(ref["fn"], y)
                d_uhdr = invert(uhdr["fn"], y)
                if not (np.isfinite(d_ref) and np.isfinite(d_uhdr)) or d_uhdr <= 0:
                    continue
                fmf = d_ref / d_uhdr
                fmf_rows.append(dict(endpoint=endpoint, beam=beam,
                                     iso_y=float(y), D_REF=float(d_ref),
                                     D_UHDR=float(d_uhdr), FMF=float(fmf)))

    with open(RES / "fmf_per_panel.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["endpoint", "beam", "iso_y", "D_REF", "D_UHDR", "FMF"])
        w.writeheader(); w.writerows(fmf_rows)

    # ===== Compare with Figure 3 digitized FMFs (paper's reported values) =====
    fig3_csv = DATA / "horst2024_fig3_fmf_digitized.csv"
    paper_fmf = []
    with open(fig3_csv) as f:
        for r in csv.DictReader(f):
            paper_fmf.append({"panel": r["panel"], "series": r["series"],
                              "dose": float(r["dose_Gy"]), "FMF": float(r["FMF"])})

    # Aggregate our FMF for the same beams/endpoints; compare to paper at high-dose plateau
    def plateau_mean(rows, min_d=40, max_d=95):
        vals = [r["FMF"] for r in rows if min_d <= r["D_UHDR"] <= max_d and 0.3 <= r["FMF"] <= 1.5]
        if not vals: return float("nan"), 0
        return float(np.mean(vals)), len(vals)

    def paper_plateau(rows, min_d=40, max_d=95):
        vals = [r["FMF"] for r in rows if min_d <= r["dose"] <= max_d]
        if not vals: return float("nan"), 0
        return float(np.mean(vals)), len(vals)

    compare_rows = []

    # Panel 3a: electron beam, four endpoints
    for endpoint, label in [("pericardial_edema", "pericardial_edema"),
                             ("curved_spine", "curved_spine"),
                             ("embryo_length", "embryo_length"),
                             ("eye_diameter", "eye_diameter")]:
        our = [r for r in fmf_rows if r["endpoint"] == endpoint and r["beam"] == "electron_30MeV"]
        pap = [r for r in paper_fmf if r["panel"] == "3a" and r["series"] == label]
        our_pl, n_our = plateau_mean(our)
        pap_pl, n_pap = paper_plateau(pap)
        compare_rows.append(dict(panel="Fig3a", series=label,
                                 our_FMF_plateau=round(our_pl, 3) if not math.isnan(our_pl) else None,
                                 paper_FMF_plateau=round(pap_pl, 3) if not math.isnan(pap_pl) else None,
                                 diff=round(our_pl - pap_pl, 3) if not (math.isnan(our_pl) or math.isnan(pap_pl)) else None,
                                 n_our=n_our, n_paper=n_pap))

    # Panel 3b: curved_spine, three beams
    beam_map = {"proton_entrance": "proton_entrance_240Gyps",
                "proton_SOBP": "proton_SOBP_600Gyps",
                "electron_30MeV": "electron_30MeV_9e4Gyps"}
    for beam, paper_series in beam_map.items():
        our = [r for r in fmf_rows if r["endpoint"] == "curved_spine" and r["beam"] == beam]
        pap = [r for r in paper_fmf if r["panel"] == "3b" and r["series"] == paper_series]
        our_pl, n_our = plateau_mean(our)
        pap_pl, n_pap = paper_plateau(pap)
        compare_rows.append(dict(panel="Fig3b", series=f"curved_spine_{beam}",
                                 our_FMF_plateau=round(our_pl, 3) if not math.isnan(our_pl) else None,
                                 paper_FMF_plateau=round(pap_pl, 3) if not math.isnan(pap_pl) else None,
                                 diff=round(our_pl - pap_pl, 3) if not (math.isnan(our_pl) or math.isnan(pap_pl)) else None,
                                 n_our=n_our, n_paper=n_pap))

    with open(RES / "fmf_compare_to_paper.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["panel", "series", "our_FMF_plateau", "paper_FMF_plateau", "diff", "n_our", "n_paper"])
        w.writeheader(); w.writerows(compare_rows)

    # ===== Quantitative claim audit =====
    claim_rows = []

    # Claim 1: "FMF saturates at ~0.7-0.8 for D >= 50 Gy"
    plateau_all = []
    for endpoint in ENDPOINTS:
        for beam in BEAMS:
            rs = [r["FMF"] for r in fmf_rows
                  if r["endpoint"] == endpoint and r["beam"] == beam
                  and 50 <= r["D_UHDR"] <= 95 and 0.3 <= r["FMF"] <= 1.5]
            if rs:
                plateau_all.append((endpoint, beam, float(np.mean(rs))))
    overall_mean = float(np.mean([v for _, _, v in plateau_all])) if plateau_all else float("nan")
    in_band = sum(1 for _, _, v in plateau_all if 0.65 <= v <= 0.85)
    claim_rows.append(dict(claim="FMF saturates at ~0.7-0.8 for D >= 50 Gy",
                           our_value=f"mean={overall_mean:.3f}, {in_band}/{len(plateau_all)} panels in [0.65,0.85]",
                           paper_value="~0.7-0.8 at D >= 50 Gy",
                           verdict="VERIFIED" if (0.65 <= overall_mean <= 0.85 and in_band >= max(1, int(0.5 * len(plateau_all)))) else "PARTIAL/CONTRADICTED"))

    # Claim 2: "Magnitude of sparing comparable across the four endpoints (for electron beam)"
    elec_plateau = [v for ep, bm, v in plateau_all if bm == "electron_30MeV"]
    if len(elec_plateau) >= 2:
        spread = max(elec_plateau) - min(elec_plateau)
        verdict = "VERIFIED" if spread <= 0.08 else ("PARTIAL" if spread <= 0.15 else "CONTRADICTED")
        claim_rows.append(dict(claim="Sparing magnitude comparable across endpoints (electron beam, D>=50)",
                               our_value=f"spread={spread:.3f}, values={[round(v,3) for v in elec_plateau]}",
                               paper_value="qualitatively comparable / 'similar magnitude'",
                               verdict=verdict))

    # Claim 3: "Less sparing for proton beams than electron beam (curved_spine)"
    spine_p_ent = [v for ep, bm, v in plateau_all if ep == "curved_spine" and bm == "proton_entrance"]
    spine_p_sob = [v for ep, bm, v in plateau_all if ep == "curved_spine" and bm == "proton_SOBP"]
    spine_e = [v for ep, bm, v in plateau_all if ep == "curved_spine" and bm == "electron_30MeV"]
    v_pe = spine_p_ent[0] if spine_p_ent else float("nan")
    v_ps = spine_p_sob[0] if spine_p_sob else float("nan")
    v_e = spine_e[0] if spine_e else float("nan")
    verdict = "VERIFIED" if (v_pe > v_e and v_ps > v_e) else ("PARTIAL" if (v_pe > v_e or v_ps > v_e) else "CONTRADICTED")
    claim_rows.append(dict(claim="Less sparing for proton beams than electron (curved_spine, D>=50)",
                           our_value=f"p_ent={v_pe:.3f}, p_sobp={v_ps:.3f}, electron={v_e:.3f}",
                           paper_value="Electron sparing >> proton sparing (smaller FMF for electrons)",
                           verdict=verdict))

    # Claim 4: "SOBP RBE shift ~10% vs proton entrance / electrons at REF (curved_spine, embryo_length)"
    def d50_at(endpoint, beam, dose_rate):
        f = fits.get((endpoint, beam, dose_rate))
        if not f: return float("nan")
        return f["c"]  # for a_fixed=1 NTCP form, c is the dose at which the exponent = 0; ~D50 surrogate.
    rbe_rows = []
    for ep in ("curved_spine", "embryo_length"):
        d_pe = invert(fits[(ep, "proton_entrance", "REF")]["fn"], 0.5 if ep == "curved_spine" else 15)
        d_ps = invert(fits[(ep, "proton_SOBP", "REF")]["fn"],     0.5 if ep == "curved_spine" else 15)
        d_e  = invert(fits[(ep, "electron_30MeV", "REF")]["fn"],   0.5 if ep == "curved_spine" else 15)
        if d_pe > 0 and d_ps > 0:
            shift_pe = (d_pe - d_ps) / d_pe * 100.0
        else:
            shift_pe = float("nan")
        if d_e > 0 and d_ps > 0:
            shift_e = (d_e - d_ps) / d_e * 100.0
        else:
            shift_e = float("nan")
        rbe_rows.append((ep, d_pe, d_ps, d_e, shift_pe, shift_e))
    shifts = [s for _, _, _, _, sp, se in rbe_rows for s in (sp, se) if np.isfinite(s)]
    if shifts:
        mean_shift = float(np.mean(shifts))
        verdict = "VERIFIED" if 5 <= mean_shift <= 18 else ("PARTIAL" if 2 <= mean_shift <= 25 else "CONTRADICTED")
    else:
        mean_shift = float("nan"); verdict = "NOT TESTED"
    claim_rows.append(dict(claim="SOBP iso-effect dose ~10% lower than proton entrance / electrons at REF (RBE)",
                           our_value=f"mean shift {mean_shift:.1f}%; per-endpoint details: " +
                                     "; ".join(f"{ep}: p_ent_shift={sp:.1f}%, electron_shift={se:.1f}%" for ep,_,_,_,sp,se in rbe_rows),
                           paper_value="~10% shift, highly significant",
                           verdict=verdict))

    # Claim 5: Curved spine UHDR sparing significant for all three beams
    # We test that FMF<0.95 at iso-y=0.5 for all three beams
    cs_check = []
    for beam in BEAMS:
        ref = fits.get(("curved_spine", beam, "REF")); uhdr = fits.get(("curved_spine", beam, "UHDR"))
        if not ref or not uhdr:
            cs_check.append((beam, None)); continue
        d_ref = invert(ref["fn"], 0.5); d_uhdr = invert(uhdr["fn"], 0.5)
        fmf = d_ref / d_uhdr if d_uhdr > 0 else float("nan")
        cs_check.append((beam, fmf))
    all_spared = all((v is not None and np.isfinite(v) and v < 0.97) for _, v in cs_check)
    claim_rows.append(dict(claim="Curved spine UHDR sparing observable for all three beams (FMF<0.97 at iso=0.5)",
                           our_value="; ".join(f"{b}: FMF={v:.3f}" if (v is not None and np.isfinite(v)) else f"{b}: NaN" for b, v in cs_check),
                           paper_value="significant UHDR sparing for all three beams",
                           verdict="VERIFIED" if all_spared else "PARTIAL"))

    with open(RES / "claim_audit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["claim", "our_value", "paper_value", "verdict"])
        w.writeheader(); w.writerows(claim_rows)

    # ===== Plots =====
    # Per-panel fit plots
    for endpoint in ENDPOINTS:
        for beam in BEAMS:
            ref = fits.get((endpoint, beam, "REF"))
            uhdr = fits.get((endpoint, beam, "UHDR"))
            if not ref or not uhdr: continue
            pts_ref = [r for r in rows if r["endpoint"] == endpoint and r["beam"] == beam and r["dose_rate"] == "REF"]
            pts_uhdr = [r for r in rows if r["endpoint"] == endpoint and r["beam"] == beam and r["dose_rate"] == "UHDR"]
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.scatter([p["dose_Gy"] for p in pts_ref], [p["response"] for p in pts_ref], marker="o", color="C0", label="REF (data)")
            ax.scatter([p["dose_Gy"] for p in pts_uhdr], [p["response"] for p in pts_uhdr], marker="^", color="C3", label="UHDR (data)")
            xx = np.linspace(0, 100, 300)
            ax.plot(xx, ref["fn"](xx), "-", color="C0", label="REF fit")
            ax.plot(xx, uhdr["fn"](xx), "-.", color="C3", label="UHDR fit")
            ax.set_xlabel("Dose (Gy)"); ax.set_ylabel("Response")
            ax.set_title(f"{endpoint}, {beam}\nREF c={ref['c']:.1f}  UHDR c={uhdr['c']:.1f}")
            ax.legend(); ax.grid(alpha=0.3)
            fig.tight_layout()
            fig.savefig(FIG / f"audit_panel_{endpoint}_{beam}.png", dpi=120)
            plt.close(fig)

    # Fig 3a-like plot for electrons (four endpoints, our FMF vs paper)
    fig, ax = plt.subplots(figsize=(6, 4.5))
    markers = {"pericardial_edema": "s", "curved_spine": "v",
               "embryo_length": "^", "eye_diameter": "D"}
    colors = {"pericardial_edema": "tab:orange", "curved_spine": "tab:green",
              "embryo_length": "tab:blue", "eye_diameter": "tab:purple"}
    for ep in ENDPOINTS:
        ours = [r for r in fmf_rows if r["endpoint"] == ep and r["beam"] == "electron_30MeV"]
        ours.sort(key=lambda r: r["D_UHDR"])
        if ours:
            ax.plot([r["D_UHDR"] for r in ours], [r["FMF"] for r in ours],
                    "-", color=colors[ep], alpha=0.6, label=f"OURS {ep}")
        pap = [r for r in paper_fmf if r["panel"] == "3a" and r["series"] == ep]
        if pap:
            ax.scatter([r["dose"] for r in pap], [r["FMF"] for r in pap],
                       marker=markers[ep], color=colors[ep], s=70, edgecolor="k", label=f"PAPER {ep}")
    ax.axhspan(0.7, 0.8, color="grey", alpha=0.2, label="Paper's claim band (0.7-0.8)")
    ax.set_xlabel("Dose UHDR (Gy)"); ax.set_ylabel("FMF = D_REF / D_UHDR")
    ax.set_title("Fig 3a replication: electron beam, four endpoints")
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "audit_fmf_panelA_electron.png", dpi=120); plt.close(fig)

    # Fig 3b-like plot
    fig, ax = plt.subplots(figsize=(6, 4.5))
    beam_colors = {"proton_entrance": "tab:blue", "proton_SOBP": "tab:orange", "electron_30MeV": "tab:green"}
    for beam in BEAMS:
        ours = [r for r in fmf_rows if r["endpoint"] == "curved_spine" and r["beam"] == beam]
        ours.sort(key=lambda r: r["D_UHDR"])
        if ours:
            ax.plot([r["D_UHDR"] for r in ours], [r["FMF"] for r in ours],
                    "-", color=beam_colors[beam], alpha=0.6, label=f"OURS {beam}")
        pap_series = beam_map[beam]
        pap = [r for r in paper_fmf if r["panel"] == "3b" and r["series"] == pap_series]
        if pap:
            ax.scatter([r["dose"] for r in pap], [r["FMF"] for r in pap],
                       marker="o", color=beam_colors[beam], s=70, edgecolor="k", label=f"PAPER {beam}")
    ax.axhspan(0.7, 0.8, color="grey", alpha=0.2, label="Paper claim band (0.7-0.8)")
    ax.set_xlabel("Dose UHDR (Gy)"); ax.set_ylabel("FMF")
    ax.set_title("Fig 3b replication: curved spine, three beams")
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "audit_fmf_panelB_spine_threebeams.png", dpi=120); plt.close(fig)

    print("\n=== CLAIM AUDIT ===")
    for c in claim_rows:
        print(f"- {c['claim']}\n  OUR: {c['our_value']}\n  PAPER: {c['paper_value']}\n  VERDICT: {c['verdict']}\n")
    print(f"\nWrote results/ and figures/ artifacts to {RES} and {FIG}")


if __name__ == "__main__":
    main()
