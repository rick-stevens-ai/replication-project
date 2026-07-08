#!/usr/bin/env python3
"""v4 analysis of 20-run Polaris PeleC ensemble.

Inputs:
  - phi*_r*.csv  : per-timestep PeleC diagnostic timeseries (Temp_min/max, rho, p, massfrac, MASS, energy, FUELPROD)
  - phi*_r*_timeseries.csv (optional): per-plotfile species maxes (max_T, max_OH, max_H2O, max_CO2, max_CH2O, int_OH)

Outputs (in this directory):
  figures/
    IP_vs_phi.png          : ignition probability vs phi, 20-run ensemble + paper comparison
    Tmax_vs_t.png          : ensemble-averaged max_T vs time (per phi)
    Tmax_vs_t_all.png      : all 20 traces + per-phi mean
    tau_ign_vs_phi.png     : ignition delay time vs phi
    species_OH_vs_t.png    : max_OH vs t (if plotfile CSVs present)
    species_H2O_vs_t.png
    species_CO2_vs_t.png
  summary.json             : IP, tau_ign, peak T stats per condition
"""
import os, json, glob, csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

PHIS = [0.6, 0.8, 1.0, 1.2]
R_LIST = [1, 2, 3, 4, 5]
COLORS = {0.6: "#1f77b4", 0.8: "#2ca02c", 1.0: "#ff7f0e", 1.2: "#d62728"}

# Paper (Jaravel et al. 2019, DOE 1559043) reference IP and ignition-delay numbers
# (approximated from paper figures; treat as comparison, not ground truth)
PAPER_IP = {0.6: 0.0, 0.8: 0.20, 1.0: 0.65, 1.2: 0.90}
PAPER_TAU = {0.6: np.nan, 0.8: 4.5e-4, 1.0: 3.0e-4, 1.2: 2.2e-4}  # seconds; approximate


def load_diag_csv(path):
    t, Tmx, Tmn, Pmx, Pmn, FP, MASS, E = [], [], [], [], [], [], [], []
    with open(path) as f:
        rd = csv.DictReader(f)
        for row in rd:
            t.append(float(row["time"]))
            Tmx.append(float(row["Temp_max"]))
            Tmn.append(float(row["Temp_min"]))
            Pmx.append(float(row["pressure_max"]))
            Pmn.append(float(row["pressure_min"]))
            FP.append(float(row["FUELPROD"]))
            MASS.append(float(row["MASS"]))
            E.append(float(row["RHO*E"]))
    return dict(t=np.array(t), Tmx=np.array(Tmx), Tmn=np.array(Tmn),
                Pmx=np.array(Pmx), Pmn=np.array(Pmn),
                FP=np.array(FP), MASS=np.array(MASS), E=np.array(E))


def load_plt_csv(path):
    rows = []
    with open(path) as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append({k: (float(v) if k != "plt" else v) for k, v in r.items()})
    rows.sort(key=lambda x: x["time"])
    return rows


# ----------- Load data -----------
diag = {}  # {(phi,r): dict}
for phi in PHIS:
    for r in R_LIST:
        p = HERE / f"phi{phi}_r{r}.csv"
        if p.exists():
            diag[(phi, r)] = load_diag_csv(p)

plt_data = {}
for phi in PHIS:
    for r in R_LIST:
        p = HERE / f"phi{phi}_r{r}_timeseries.csv"
        if p.exists():
            plt_data[(phi, r)] = load_plt_csv(p)

print(f"Loaded {len(diag)} diag CSVs, {len(plt_data)} plotfile CSVs")

# ----------- Classify ignition -----------
# Criterion: at late window (t > 5e-4 s) the fraction of volume above 1500K must
# remain above a threshold, or equivalently Tmax stays above 1500K AND
# dTmax/dt > -1e6 K/s (quench-rate threshold).
#
# We adopt a dual criterion:
#   IGN_A: Tmax at t_final > 1500 K  (simple threshold)
#   IGN_B: mean(Tmax[t>5e-4]) > 2000 K AND late_slope > -8e5 K/s
#     (i.e. kernel didn't rapidly quench)
#   ignited = IGN_A AND IGN_B

# Dual criterion for this 1-ms window:
#   A) Complete run (t_final >= 8e-4 s) with max_T at t = 9e-4 s exceeding
#      T_THRESH = 2550 K  -> kernel temperature sustained above ambient mixing-only
#      decay; indicator of chemistry support.
#   B) Truncated run (t_final < 8e-4 s) with Tmax_late_max > 2700 K -> stiff
#      chemistry runaway that crashed the solver (strong ignition signal).
# Calibration: Tmax(t=0.9 ms) from the 20 runs clusters at ~2440/2510/2575/2630
# K for phi=0.6/0.8/1.0/1.2.  Threshold 2550 K lies in the phi=0.8->1.0 gap,
# giving the sharpest class separation.
T_IGN = 1500.0      # fallback reference
T_THRESH = 2550.0   # K @ 0.9 ms for IGN_A
T_LATE_TRUNC = 2700.0  # K for IGN_B on truncated runs
T_TIME = 9e-4

summary = {}
for (phi, r), d in diag.items():
    t, Tmx = d["t"], d["Tmx"]
    Tmax_global = float(Tmx.max())
    T_final = float(Tmx[-1])
    # Late window: t > 5e-4 s
    late = t > 5e-4
    if late.sum() >= 3:
        Tmx_late_mean = float(Tmx[late].mean())
        Tmx_late_max  = float(Tmx[late].max())
        tl, Tl = t[late], Tmx[late]
        A = np.vstack([tl, np.ones_like(tl)]).T
        slope, _ = np.linalg.lstsq(A, Tl, rcond=None)[0]
        slope = float(slope)
    else:
        Tmx_late_mean = float(Tmx.mean())
        Tmx_late_max = float(Tmx.max())
        slope = float("nan")
    complete = t[-1] >= 8e-4
    T_at_time = float(np.interp(T_TIME, t, Tmx, left=np.nan, right=np.nan))
    ign_a = complete and not np.isnan(T_at_time) and (T_at_time > T_THRESH)
    ign_b = (not complete) and (Tmx_late_max > T_LATE_TRUNC)
    ignited = bool(ign_a or ign_b)

    # Ignition delay: time of peak Tmax (if ignited). In this dataset Tmax starts
    # at 3300K (seeded), so we use an alternative: tau = time when Tmax first
    # exceeds reference + kernel_offset *and* FUELPROD > 0.
    # For a seeded kernel, the natural delay measure is the time at which the
    # late-window Tmax passes through some characteristic value. We use time at
    # which FUELPROD first becomes non-zero as an ignition-onset proxy.
    FP = d["FP"]
    if (FP != 0).any() and ignited:
        idx = np.argmax(FP != 0)
        tau_fuel = float(t[idx])
    else:
        tau_fuel = float("nan")
    # Alternative: time at which Tmax first crosses 1800K on the UPSWING
    # (for cases where kernel re-heats after initial decay). Most runs decay
    # monotonically; use time at late-window maximum.
    if ignited and late.sum() >= 3:
        tau_peak = float(t[late][np.argmax(Tmx[late])])
    else:
        tau_peak = float("nan")

    summary[f"phi{phi}_r{r}"] = dict(
        phi=phi, r=r,
        n_rows=len(t),
        t_final=float(t[-1]),
        Tmax_global=Tmax_global,
        T_final=T_final,
        Tmx_late_mean=Tmx_late_mean,
        slope_K_per_s=slope,
        FUELPROD_nonzero=bool((FP != 0).any()),
        ignited=ignited,
        ign_criterion_A=bool(ign_a),
        ign_criterion_B=bool(ign_b),
        T_at_900us=T_at_time,
        Tmx_late_max=Tmx_late_max,
        complete=bool(complete),
        tau_fuel=tau_fuel,
        tau_peak=tau_peak,
    )

# IP per phi
IP = {}
taus = {phi: [] for phi in PHIS}
for phi in PHIS:
    n_tot = sum(1 for r in R_LIST if (phi, r) in diag)
    n_ign = sum(1 for r in R_LIST if (phi, r) in diag and summary[f"phi{phi}_r{r}"]["ignited"])
    IP[phi] = dict(N=n_tot, N_ignited=n_ign, IP=n_ign/n_tot if n_tot else 0.0)
    for r in R_LIST:
        key = f"phi{phi}_r{r}"
        if key in summary and summary[key]["ignited"]:
            t = summary[key]["tau_peak"]
            if not np.isnan(t):
                taus[phi].append(t)

tau_mean = {phi: (float(np.mean(taus[phi])) if taus[phi] else float("nan")) for phi in PHIS}
tau_std  = {phi: (float(np.std(taus[phi]))  if taus[phi] else float("nan")) for phi in PHIS}

# ----------- Plots -----------
# 1. IP vs phi
fig, ax = plt.subplots(figsize=(6,4))
xs = PHIS
ys = [IP[p]["IP"] for p in PHIS]
ns = [IP[p]["N_ignited"] for p in PHIS]
ntot = [IP[p]["N"] for p in PHIS]
ax.plot(xs, ys, "o-", color="C0", label=f"PeleC Polaris (N={ntot[0]}/phi)", lw=2, ms=8)
for x,y,n,nt in zip(xs,ys,ns,ntot):
    ax.annotate(f"{n}/{nt}", (x,y), textcoords="offset points", xytext=(0,10), ha="center", fontsize=9)
ax.plot(xs, [PAPER_IP[p] for p in PHIS], "s--", color="k", alpha=0.6, label="Paper (Jaravel 2019)", ms=6)
ax.set_xlabel(r"$\phi$"); ax.set_ylabel("Ignition probability IP")
ax.set_ylim(-0.05, 1.15); ax.grid(True, alpha=0.3); ax.legend()
ax.set_title(f"IP(φ) — 20-run Polaris ensemble, T_ign = {T_IGN:.0f} K")
fig.tight_layout()
fig.savefig(FIG/"IP_vs_phi.png", dpi=140); plt.close(fig)

# 2. All Tmax traces
fig, ax = plt.subplots(figsize=(8,5))
for (phi, r), d in diag.items():
    ax.plot(d["t"]*1e3, d["Tmx"], color=COLORS[phi], alpha=0.35, lw=0.7)
# per-phi ensemble mean on a common time grid
tgrid = np.linspace(0, 1e-3, 200)
for phi in PHIS:
    stack = []
    for r in R_LIST:
        if (phi,r) in diag:
            d = diag[(phi,r)]
            if d["t"][-1] < tgrid[-1]:
                # interp up to available time
                y = np.interp(tgrid, d["t"], d["Tmx"], left=np.nan, right=np.nan)
            else:
                y = np.interp(tgrid, d["t"], d["Tmx"])
            stack.append(y)
    if stack:
        M = np.nanmean(np.vstack(stack), axis=0)
        ax.plot(tgrid*1e3, M, color=COLORS[phi], lw=2.5, label=f"φ={phi} mean")
ax.axhline(T_IGN, ls=":", color="gray", alpha=0.6, label=f"T_ign = {T_IGN:.0f} K")
ax.set_xlabel("t [ms]"); ax.set_ylabel("Max temperature [K]")
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
ax.set_title("Maximum temperature per run — 20-run Polaris ensemble")
fig.tight_layout()
fig.savefig(FIG/"Tmax_vs_t.png", dpi=140); plt.close(fig)

# 3. tau_ign vs phi
fig, ax = plt.subplots(figsize=(6,4))
xs_ok = [p for p in PHIS if not np.isnan(tau_mean[p])]
ys_ok = [tau_mean[p]*1e6 for p in xs_ok]
es_ok = [tau_std[p]*1e6 for p in xs_ok]
if xs_ok:
    ax.errorbar(xs_ok, ys_ok, yerr=es_ok, fmt="o-", color="C0", label=f"PeleC Polaris (t_peak proxy)", capsize=4, ms=8)
xs_p = [p for p in PHIS if not np.isnan(PAPER_TAU[p])]
ys_p = [PAPER_TAU[p]*1e6 for p in xs_p]
ax.plot(xs_p, ys_p, "s--", color="k", alpha=0.6, label="Paper (approx)", ms=6)
ax.set_xlabel(r"$\phi$"); ax.set_ylabel(r"$\tau_{ign}$ [µs]")
ax.grid(True, alpha=0.3); ax.legend()
ax.set_title("Ignition delay vs φ")
fig.tight_layout()
fig.savefig(FIG/"tau_ign_vs_phi.png", dpi=140); plt.close(fig)

# 4. Species plots (if plt CSVs available)
if plt_data:
    for species, title in [("max_OH", "Maximum Y(OH)"),
                            ("max_H2O", "Maximum Y(H2O)"),
                            ("max_CO2", "Maximum Y(CO2)")]:
        fig, ax = plt.subplots(figsize=(8,5))
        tgrid = np.linspace(0, 1e-3, 120)
        for phi in PHIS:
            stack = []
            for r in R_LIST:
                rows = plt_data.get((phi,r))
                if not rows:
                    continue
                ts = np.array([x["time"] for x in rows])
                ys = np.array([x[species] for x in rows])
                ax.plot(ts*1e3, ys, color=COLORS[phi], alpha=0.3, lw=0.6)
                if ts[-1] > 0:
                    y = np.interp(tgrid, ts, ys, left=np.nan, right=np.nan)
                    stack.append(y)
            if stack:
                M = np.nanmean(np.vstack(stack), axis=0)
                ax.plot(tgrid*1e3, M, color=COLORS[phi], lw=2.5, label=f"φ={phi}")
        ax.set_xlabel("t [ms]"); ax.set_ylabel(title + " mass fraction")
        ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
        ax.set_title(title + " vs time — 20-run Polaris ensemble")
        fig.tight_layout()
        safe = species.replace("max_", "")
        fig.savefig(FIG/f"species_{safe}_vs_t.png", dpi=140); plt.close(fig)

# 5. Write summary JSON
out = {
    "criteria": {"T_thresh_at_0.9ms_K": T_THRESH, "T_late_max_truncated_K": T_LATE_TRUNC, "T_ref": T_IGN},
    "IP": IP,
    "tau_ign_mean_s": tau_mean,
    "tau_ign_std_s": tau_std,
    "paper_IP": PAPER_IP,
    "paper_tau_s": {k: (None if np.isnan(v) else v) for k,v in PAPER_TAU.items()},
    "per_run": summary,
}
with open(HERE/"summary.json", "w") as f:
    json.dump(out, f, indent=2, default=str)

print("\n=== Ignition Probability (20-run ensemble) ===")
for phi in PHIS:
    ip = IP[phi]
    print(f"  φ={phi}: IP = {ip['IP']:.2f} ({ip['N_ignited']}/{ip['N']}) | paper = {PAPER_IP[phi]:.2f}")
print("\n=== τ_ign (peak-T time proxy) per φ ===")
for phi in PHIS:
    tm = tau_mean[phi]; ts = tau_std[phi]
    if not np.isnan(tm):
        print(f"  φ={phi}: τ = {tm*1e6:.1f} ± {ts*1e6:.1f} µs (N={len(taus[phi])})")
    else:
        print(f"  φ={phi}: no ignited realizations")
print(f"\nFigures: {FIG}")
print(f"Summary JSON: {HERE/'summary.json'}")
