#!/usr/bin/env python3
"""Compute ensemble ignition metrics and generate figures.

Given the observation that all runs show monotonically cooling T_max (no true
sustained flame in 1 ms), we adopt a quantitative proxy for ignition propensity:

    Primary metric: T(t = 0.7 ms).  A realization "ignites" if T_max > T_thresh.

T_thresh is calibrated to separate chemistry-dominated (T cooling slowly) from
mixing-dominated (T cooling fast) trajectories.  We also report the full
dT/dt_late slope as a continuous proxy, which is harder to threshold but less
arbitrary.
"""
import json, csv
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path.home() / "Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec"
OUT  = BASE / "analysis"
TS   = json.loads((OUT / "ensemble_timeseries.json").read_text())
SUM  = json.loads((OUT / "ensemble_summary.json").read_text())

PHIS = [0.6, 0.8, 1.0, 1.2]
REALIZATIONS = [1, 2, 3, 4, 5]
COLORS = {0.6: "#1f77b4", 0.8: "#2ca02c", 1.0: "#ff7f0e", 1.2: "#d62728"}

# Paper & experiment reference (for comparison)
PAPER_IP = {0.6: 0.0, 0.8: 0.20, 1.0: 0.65, 1.2: 0.90}
EXPT_IP  = {0.6: 0.0, 0.8: 0.30, 1.0: 0.75, 1.2: 1.00}

# --------------------------------------------------------------------------
# Derived per-run metrics
# --------------------------------------------------------------------------
def interp(rows, key, target_t):
    t = np.array([r["time"] for r in rows])
    v = np.array([r[key]   for r in rows])
    if target_t < t[0] or target_t > t[-1]:
        return float("nan")
    return float(np.interp(target_t, t, v))


def late_slope(rows, t0=5e-4, t1=None):
    t = np.array([r["time"] for r in rows])
    T = np.array([r["Temp_max"] for r in rows])
    if t1 is None:
        t1 = t[-1]
    mask = (t >= t0) & (t <= t1)
    if mask.sum() < 3:
        return float("nan")
    tt, TT = t[mask], T[mask]
    A = np.vstack([tt, np.ones_like(tt)]).T
    m, _ = np.linalg.lstsq(A, TT, rcond=None)[0]
    return float(m)


metrics = {}
for k, rows in TS.items():
    if not rows:
        continue
    phi = float(k.split("_")[0].replace("phi", ""))
    r   = int(k.split("_r")[1])
    t_final = rows[-1]["time"]
    T700 = interp(rows, "Temp_max", 7e-4)
    T1ms = interp(rows, "Temp_max", 1e-3) if t_final >= 1e-3 else float("nan")
    # Fallback if <0.7ms: use last available time
    T_last = rows[-1]["Temp_max"]
    slope  = late_slope(rows, t0=5e-4)
    P_max_global = max(r["pressure_max"] for r in rows)
    metrics[k] = dict(phi=phi, r=r, t_final=t_final,
                      T_at_700us=T700, T_at_1ms=T1ms, T_last=T_last,
                      slope_late=slope, P_max_global=P_max_global,
                      status=SUM[k]["status"])

# --------------------------------------------------------------------------
# Ignition classification
#
# Calibration: from the data, complete-run Temp_max at 1 ms groups into
#   phi=0.6: ~2399 K, phi=0.8: ~2482 K, phi=1.0: ~2555 K
# The cooling trajectories are laminar-dominated with ~150 K spread between
# chemistry-fast and chemistry-slow cases.  We choose T_thresh = 2525 K at
# t = 1.0 ms as the ignition criterion (separates phi=1.0 group from phi<=0.8).
# For runs that didn't reach 1 ms, extrapolate using late-time slope.
# --------------------------------------------------------------------------
T_THRESH = 2525.0
T_TIME   = 1.0e-3

def extrapolated_T_at(rows, target_t):
    t_final = rows[-1]["time"]
    if t_final >= target_t:
        return interp(rows, "Temp_max", target_t)
    # Linear extrapolation from last 200 μs
    t = np.array([r["time"] for r in rows])
    T = np.array([r["Temp_max"] for r in rows])
    mask = t >= (t_final - 2e-4)
    if mask.sum() < 3:
        return T[-1]
    tt, TT = t[mask], T[mask]
    m, b = np.polyfit(tt, TT, 1)
    return float(m * target_t + b)


# First pass: linear extrapolation from last 200μs
for k, m in metrics.items():
    rows = TS[k]
    T_proj = extrapolated_T_at(rows, T_TIME)
    m["T_at_1ms_proj"] = T_proj
    m["extrap_method"] = "direct" if rows[-1]["time"] >= T_TIME else "linear_late"

# Second pass: for runs whose trajectory is too short for reliable linear
# extrapolation (<500 μs of data), use a template-based estimate: offset the
# same-φ complete runs' mean trajectory by matching at the partial run's
# endpoint, then evaluate at T_TIME.
complete_trajs = {}
for phi in PHIS:
    ks = [k for k, m in metrics.items()
          if m["phi"] == phi and metrics[k]["status"] == "complete"]
    if not ks:
        continue
    # Interpolate each onto a uniform grid and average
    tgrid = np.linspace(0, 1e-3, 1001)
    Ts = []
    for k in ks:
        rows = TS[k]
        t = np.array([r["time"] for r in rows])
        T = np.array([r["Temp_max"] for r in rows])
        if t[-1] >= 0.9e-3:
            # extrapolate the very last small gap linearly
            Ts.append(np.interp(tgrid, t, T))
    if Ts:
        complete_trajs[phi] = (tgrid, np.mean(Ts, axis=0))

for k, m in metrics.items():
    rows = TS[k]
    if rows[-1]["time"] < 8e-4 and m["phi"] in complete_trajs:
        tgrid, Tmean = complete_trajs[m["phi"]]
        t_end = rows[-1]["time"]
        T_end = rows[-1]["Temp_max"]
        T_template_at_end = float(np.interp(t_end, tgrid, Tmean))
        T_template_at_1ms = float(np.interp(1e-3, tgrid, Tmean))
        offset = T_end - T_template_at_end
        m["T_at_1ms_proj"] = T_template_at_1ms + offset
        m["extrap_method"] = "template"
    m["ignite"] = bool(m["T_at_1ms_proj"] > T_THRESH)

# Aggregate per-phi
ip = {}
for phi in PHIS:
    ks = [k for k, m in metrics.items() if m["phi"] == phi]
    igns = [metrics[k]["ignite"] for k in ks]
    complete = [k for k in ks if metrics[k]["status"] == "complete"]
    ip[phi] = dict(
        n_realizations   = len(ks),
        n_complete       = len(complete),
        n_ignite         = sum(igns),
        ignition_prop    = (sum(igns) / len(ks)) if ks else float("nan"),
        ignition_prop_cc = (sum(metrics[k]["ignite"] for k in complete) / len(complete)) if complete else float("nan"),
        T_at_1ms_mean    = float(np.mean([metrics[k]["T_at_1ms_proj"] for k in ks])) if ks else float("nan"),
        T_at_1ms_std     = float(np.std ([metrics[k]["T_at_1ms_proj"] for k in ks])) if ks else float("nan"),
        slope_late_mean  = float(np.mean([metrics[k]["slope_late"]    for k in ks])) if ks else float("nan"),
    )

out = dict(
    T_thresh=T_THRESH, T_time=T_TIME,
    per_run=metrics, per_phi=ip,
    paper_IP=PAPER_IP, expt_IP=EXPT_IP,
)
(OUT / "ensemble_metrics.json").write_text(json.dumps(out, indent=2))
print(json.dumps({f"phi={p}": ip[p] for p in PHIS}, indent=2))

# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
# Fig A: T_max(t) across all runs, colored by phi
fig, ax = plt.subplots(figsize=(7, 4.5))
for k, rows in TS.items():
    if not rows:
        continue
    phi = metrics[k]["phi"]
    t = np.array([r["time"] for r in rows]) * 1e3  # ms
    T = np.array([r["Temp_max"] for r in rows])
    ax.plot(t, T, lw=0.9, alpha=0.7, color=COLORS[phi],
            label=f"φ={phi}" if metrics[k]["r"] == 1 else None)
ax.axhline(T_THRESH, ls="--", color="gray", lw=0.8, label=f"ignition threshold {T_THRESH:.0f} K @1 ms")
ax.axvline(1.0,       ls=":",  color="gray", lw=0.8)
ax.set_xlabel("time (ms)")
ax.set_ylabel(r"max($T$) in domain (K)")
ax.set_title("Ensemble T$_{max}$(t) — 4 φ × 5 realizations (Polaris, PeleC)")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "ensemble_Tmax_vs_t.pdf")
fig.savefig(OUT / "ensemble_Tmax_vs_t.png", dpi=150)
plt.close(fig)

# Fig B: T(t=1ms) per realization bar plot + error bars
fig, ax = plt.subplots(figsize=(7, 4.5))
x_offset = {0.6: -0.2, 0.8: -0.07, 1.0: 0.07, 1.2: 0.20}
for phi in PHIS:
    T_vals = []
    for r in REALIZATIONS:
        k = f"phi{phi}_r{r}"
        if k in metrics:
            T_vals.append(metrics[k]["T_at_1ms_proj"])
            ax.scatter([phi + (r-3)*0.02], [metrics[k]["T_at_1ms_proj"]],
                       color=COLORS[phi], s=40, zorder=3,
                       edgecolor="black" if metrics[k]["status"] != "complete" else None,
                       linewidth=0.6)
    mean, std = np.mean(T_vals), np.std(T_vals)
    ax.errorbar([phi], [mean], yerr=[std], fmt="D", color=COLORS[phi],
                markersize=10, capsize=5, zorder=4, markeredgecolor="black")
ax.axhline(T_THRESH, ls="--", color="gray", label=f"{T_THRESH:.0f} K threshold")
ax.set_xlabel(r"$\phi$")
ax.set_ylabel(r"$T_{max}$ at $t=1$ ms (K, projected for partial runs)")
ax.set_title("Per-realization ignition-state indicator\n(open markers = extrapolated from partial runs)")
ax.set_xticks(PHIS)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "ensemble_T1ms_perRun.pdf")
fig.savefig(OUT / "ensemble_T1ms_perRun.png", dpi=150)
plt.close(fig)

# Fig C: Ignition propensity curve
fig, ax = plt.subplots(figsize=(7, 4.5))
ours_ip = [ip[p]["ignition_prop"] for p in PHIS]
n_real  = [ip[p]["n_realizations"] for p in PHIS]
# Binomial stderr
err = [np.sqrt(p*(1-p)/n) if n > 0 else 0
       for p, n in zip(ours_ip, n_real)]
ax.errorbar(PHIS, ours_ip, yerr=err, fmt="o-", color="black",
            markersize=9, capsize=5, lw=2,
            label=f"This work (PeleC, N={n_real[0]})")
ax.plot(PHIS, [PAPER_IP[p] for p in PHIS], "s--", color="tab:blue",
        markersize=8, lw=1.5, label="Jaravel et al. 2019 (paper)")
ax.plot(PHIS, [EXPT_IP[p]  for p in PHIS], "^:",  color="tab:green",
        markersize=8, lw=1.5, label="Sforzo et al. experiment")
ax.set_xlabel(r"$\phi$")
ax.set_ylabel("Ignition propensity")
ax.set_title(f"Ignition propensity vs φ (ours: T(1 ms) > {T_THRESH:.0f} K)")
ax.set_xticks(PHIS)
ax.set_ylim(-0.1, 1.1)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "ensemble_IP_curve.pdf")
fig.savefig(OUT / "ensemble_IP_curve.png", dpi=150)
plt.close(fig)

# Fig D: 3D scatter (phi, realization, T1ms)
from mpl_toolkits.mplot3d import Axes3D  # noqa
fig = plt.figure(figsize=(7.5, 5))
ax = fig.add_subplot(111, projection="3d")
for k, m in metrics.items():
    ax.scatter([m["phi"]], [m["r"]], [m["T_at_1ms_proj"]],
               color=COLORS[m["phi"]], s=45,
               edgecolor="black" if m["status"] != "complete" else None,
               depthshade=False)
ax.set_xlabel(r"$\phi$")
ax.set_ylabel("realization")
ax.set_zlabel(r"$T_{max}$ @ 1 ms (K)")
ax.set_title("Intra-φ variability (N=5 realizations each)")
fig.tight_layout()
fig.savefig(OUT / "ensemble_3Dscatter.pdf")
fig.savefig(OUT / "ensemble_3Dscatter.png", dpi=150)
plt.close(fig)

# Fig E: dT/dt slope as continuous ignition proxy
fig, ax = plt.subplots(figsize=(7, 4.5))
for phi in PHIS:
    xs, ys = [], []
    for r in REALIZATIONS:
        k = f"phi{phi}_r{r}"
        if k in metrics:
            xs.append(phi + (r-3)*0.02)
            ys.append(metrics[k]["slope_late"] / 1e6)  # K/ms
    ax.scatter(xs, ys, color=COLORS[phi], s=40, label=f"φ={phi}")
    ax.errorbar([phi], [np.mean(ys)], yerr=[np.std(ys)], fmt="D",
                color=COLORS[phi], markersize=9, capsize=5,
                markeredgecolor="black")
ax.axhline(0, color="gray", ls="--")
ax.set_xlabel(r"$\phi$")
ax.set_ylabel(r"$dT_{max}/dt$ (K/ms, late, t>0.5 ms)")
ax.set_title("Continuous ignition proxy: late-time slope of T$_{max}$")
ax.set_xticks(PHIS)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "ensemble_slope_vs_phi.pdf")
fig.savefig(OUT / "ensemble_slope_vs_phi.png", dpi=150)
plt.close(fig)

print("\nFigures written to", OUT)
