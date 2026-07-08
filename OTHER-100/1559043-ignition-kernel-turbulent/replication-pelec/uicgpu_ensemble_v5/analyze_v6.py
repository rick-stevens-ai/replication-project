#!/usr/bin/env python3
"""Analyze v6 PeleC uicgpu single-realization-per-phi sweep.

Inputs: raw_runs/phi_{0.6,0.8,1.0,1.2}_run.log
  Pre-filtered grep of TIME=... Temp/pressure lines from the full uicgpu run.log

This is NOT the 5x4 jitter ensemble of v5: it is a single deterministic
realization per phi, run to 5 ms with AMR L=1 (125 um effective) on
uicgpu 8x A100. We report it as such and flag N=1 in the IP plot.

Outputs:
  summary.json       — per-run timeseries summary + IP table
  figures/ip_vs_phi.png/pdf
  figures/tmax_timeseries_phi_all.png
  figures/tmax_pmax_panel.png
"""
import re, os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(HERE, "raw_runs")
OUT  = HERE
FIGD = os.path.join(OUT, "figures")
os.makedirs(FIGD, exist_ok=True)

PHIS = [0.6, 0.8, 1.0, 1.2]

T_END_IGN = 2000.0   # K — paper-faithful sustained-flame threshold

TEMP_RE = re.compile(
    r"TIME\s*=\s*([0-9.eE+-]+)\s+Temp\s+MIN\s*=\s*([0-9.eE+-]+)\s+MAX\s*=\s*([0-9.eE+-]+)"
)
PRESS_RE = re.compile(
    r"TIME\s*=\s*([0-9.eE+-]+)\s+pressure\s+MIN\s*=\s*([0-9.eE+-]+)\s+MAX\s*=\s*([0-9.eE+-]+)"
)
MASS_RE = re.compile(
    r"TIME\s*=\s*([0-9.eE+-]+)\s+MASS\s*=\s*([0-9.eE+-]+)"
)


def parse_run(path):
    t_T, Tmin, Tmax = [], [], []
    t_P, Pmin, Pmax = [], [], []
    with open(path) as fh:
        for line in fh:
            m = TEMP_RE.search(line)
            if m:
                t_T.append(float(m.group(1)))
                Tmin.append(float(m.group(2)))
                Tmax.append(float(m.group(3)))
                continue
            m = PRESS_RE.search(line)
            if m:
                t_P.append(float(m.group(1)))
                Pmin.append(float(m.group(2)))
                Pmax.append(float(m.group(3)))
    return {
        "t":     np.array(t_T),
        "Tmin":  np.array(Tmin),
        "Tmax":  np.array(Tmax),
        "tP":    np.array(t_P),
        "Pmin":  np.array(Pmin),
        "Pmax":  np.array(Pmax),
    }


def wilson_band(p, n, z=1.0):
    if n == 0:
        return (float("nan"), float("nan"))
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


# Paper Fig 3 approximate IP values (from Jaravel et al. 2019)
PAPER_IP = {0.6: 0.0, 0.8: 0.20, 1.0: 0.65, 1.2: 0.90}

runs = {}
for phi in PHIS:
    path = os.path.join(RAW, f"phi_{phi}_run.log")
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        continue
    rec = parse_run(path)
    rec["phi"] = phi
    t = rec["t"]; T = rec["Tmax"]
    rec["t_final_ms"] = float(t[-1] * 1000) if len(t) else 0.0
    rec["T_global_max"] = float(T.max()) if len(T) else float("nan")
    rec["T_end"] = float(T[-1]) if len(T) else float("nan")
    rec["T_min_end"] = float(rec["Tmin"][-1]) if len(rec["Tmin"]) else float("nan")
    # Late-window (>1.5 ms) statistics
    late_mask = t > 1.5e-3
    rec["T_late_max"]  = float(T[late_mask].max())  if late_mask.any() else float("nan")
    rec["T_late_mean"] = float(T[late_mask].mean()) if late_mask.any() else float("nan")
    rec["T_late_min_floor"] = float(rec["Tmin"][late_mask].min()) if late_mask.any() else float("nan")
    rec["P_end_atm"] = float(rec["Pmax"][-1] / 1.01325e6) if len(rec["Pmax"]) else float("nan")
    rec["P_max_global_atm"] = float(rec["Pmax"].max() / 1.01325e6) if len(rec["Pmax"]) else float("nan")
    rec["ignited"] = bool(rec["T_end"] > T_END_IGN)
    rec["ign_reason"] = "sustained (T_end > 2000 K)" if rec["ignited"] else "quenched (T_end <= 2000 K)"
    rec["complete"] = rec["t_final_ms"] >= 4.95
    rec["n_samples"] = int(len(t))
    runs[phi] = rec
    print(f"phi={phi}  t_f={rec['t_final_ms']:.3f} ms  N_samples={rec['n_samples']:5d}  "
          f"T_global_max={rec['T_global_max']:.0f}  T_late_max={rec['T_late_max']:.0f}  "
          f"T_end={rec['T_end']:.0f}  P_end={rec['P_end_atm']:.2f} atm  "
          f"ignited={rec['ignited']}  complete={rec['complete']}")

# IP table (N=1 per phi here)
ip_table = {}
for phi in PHIS:
    rec = runs[phi]
    n   = 1
    nig = 1 if rec["ignited"] else 0
    p   = nig / n
    lo, hi = wilson_band(p, n)
    ip_table[phi] = {
        "N":  n,
        "N_ignited": nig,
        "IP": p,
        "band_lo": lo,
        "band_hi": hi,
        "paper_IP": PAPER_IP[phi],
        "delta_vs_paper": p - PAPER_IP[phi],
    }

l1 = sum(abs(ip_table[p]["delta_vs_paper"]) for p in PHIS)

summary = {
    "ensemble": "v6_uicgpu_single_realization",
    "n_phi": len(PHIS),
    "n_realizations_per_phi": 1,
    "compute": "uicgpu 8x A100 80GB (1 GPU per phi, parallel)",
    "amr_max_level": 1,
    "effective_resolution_um": 125,
    "target_window_ms": 5.0,
    "ignition_criterion": {
        "T_END_IGN_K": T_END_IGN,
        "definition": "T_max at last available step > 2000 K = sustained flame",
    },
    "per_phi": {
        f"{phi}": {
            "t_final_ms":   runs[phi]["t_final_ms"],
            "T_global_max": runs[phi]["T_global_max"],
            "T_end":        runs[phi]["T_end"],
            "T_late_max":   runs[phi]["T_late_max"],
            "T_late_mean":  runs[phi]["T_late_mean"],
            "T_late_min_floor": runs[phi]["T_late_min_floor"],
            "P_end_atm":    runs[phi]["P_end_atm"],
            "P_max_global_atm": runs[phi]["P_max_global_atm"],
            "ignited":      runs[phi]["ignited"],
            "ign_reason":   runs[phi]["ign_reason"],
            "complete":     runs[phi]["complete"],
            "n_samples":    runs[phi]["n_samples"],
        }
        for phi in PHIS
    },
    "IP_table": {f"{p}": ip_table[p] for p in PHIS},
    "paper_IP": PAPER_IP,
    "L1_distance_to_paper_IP": l1,
}


def _clean(o):
    if isinstance(o, dict):  return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, list):  return [_clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)): return None
    return o


with open(os.path.join(OUT, "summary.json"), "w") as f:
    json.dump(_clean(summary), f, indent=2)

# === Figures ===

# 1. IP vs phi (with paper overlay) — both .png and .pdf
for ext in ("png", "pdf"):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    xs = PHIS
    ys = [ip_table[p]["IP"] for p in PHIS]
    lo = [ip_table[p]["IP"] - ip_table[p]["band_lo"] for p in PHIS]
    hi = [ip_table[p]["band_hi"] - ip_table[p]["IP"] for p in PHIS]
    ax.errorbar(xs, ys, yerr=[lo, hi], fmt="o-", color="C0", lw=2,
                capsize=6, markersize=10,
                label="v6 PeleC uicgpu (AMR L=1, 5 ms, N=1/φ)")
    ax.plot(list(PAPER_IP.keys()), list(PAPER_IP.values()),
            "s--", color="C3", lw=2, markersize=9,
            label="Paper Fig 3 (Jaravel et al. 2019)")
    for p in PHIS:
        ax.annotate(f"{ip_table[p]['N_ignited']}/{ip_table[p]['N']}",
                    (p, ip_table[p]["IP"]),
                    textcoords="offset points", xytext=(8, -12), fontsize=9)
    ax.set_xlabel(r"Equivalence ratio $\phi$")
    ax.set_ylabel(r"Ignition probability $P_{\rm ign}$")
    ax.set_title(r"Ignition probability vs $\phi$ — uicgpu v6 sweep (AMR L=1, 5 ms)")
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0.5, 1.3)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="center right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGD, f"ip_vs_phi.{ext}"), dpi=140)
    plt.close(fig)

# 2. T_max(t) overlay across all phi
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = {0.6: "C0", 0.8: "C2", 1.0: "C1", 1.2: "C3"}
for phi in PHIS:
    rec = runs[phi]
    ax.plot(rec["t"] * 1000, rec["Tmax"], color=colors[phi], lw=1.4,
            label=fr"$\phi={phi}$  (T_end={rec['T_end']:.0f} K)")
ax.axhline(T_END_IGN, color="gray", ls=":", alpha=0.7,
           label=f"ignition threshold = {T_END_IGN:.0f} K")
ax.set_xlabel("time [ms]")
ax.set_ylabel(r"$T_{\max}$ [K]")
ax.set_title(r"Maximum temperature evolution — uicgpu v6 (5 ms, AMR L=1)")
ax.set_ylim(400, 3500)
ax.set_xlim(0, 5.05)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGD, "tmax_timeseries_phi_all.png"), dpi=140)
fig.savefig(os.path.join(FIGD, "tmax_timeseries_phi_all.pdf"))
plt.close(fig)

# 2b. Per-phi T_max in 4 subplots (separate file per phi-overlay request)
for phi in PHIS:
    rec = runs[phi]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(rec["t"] * 1000, rec["Tmax"], color=colors[phi], lw=1.3, label=r"$T_{\max}$")
    ax.plot(rec["t"] * 1000, rec["Tmin"], color=colors[phi], lw=0.8, ls="--", alpha=0.6, label=r"$T_{\min}$")
    ax.axhline(T_END_IGN, color="gray", ls=":", alpha=0.7, label="2000 K threshold")
    verdict = "IGNITED" if rec["ignited"] else "QUENCHED"
    ax.set_title(fr"$\phi={phi}$ — {verdict}   T_end={rec['T_end']:.0f} K   P_max={rec['P_max_global_atm']:.1f} atm")
    ax.set_xlabel("time [ms]")
    ax.set_ylabel("T [K]")
    ax.set_ylim(300, 3500)
    ax.set_xlim(0, 5.05)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGD, f"tmax_timeseries_phi_{phi}.png"), dpi=140)
    plt.close(fig)

# 3. Combined T_max + P_max(t) panel
fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
ax = axes[0]
for phi in PHIS:
    rec = runs[phi]
    ax.plot(rec["t"] * 1000, rec["Tmax"], color=colors[phi], lw=1.4,
            label=fr"$\phi={phi}$")
ax.axhline(T_END_IGN, color="gray", ls=":", alpha=0.6, label="2000 K threshold")
ax.set_ylabel(r"$T_{\max}$ [K]")
ax.set_ylim(400, 3500)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", fontsize=9)
ax.set_title("Hot-spot diagnostics — uicgpu v6 (AMR L=1, 5 ms)")

ax = axes[1]
for phi in PHIS:
    rec = runs[phi]
    ax.plot(rec["tP"] * 1000, rec["Pmax"] / 1.01325e6, color=colors[phi], lw=1.4)
ax.axhline(1.0, color="gray", ls=":", alpha=0.6, label="1 atm")
ax.set_xlabel("time [ms]")
ax.set_ylabel(r"$P_{\max}$ [atm]")
ax.set_xlim(0, 5.05)
ax.set_yscale("linear")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGD, "tmax_pmax_panel.png"), dpi=140)
plt.close(fig)

print("\n=== IP summary ===")
for phi in PHIS:
    s = ip_table[phi]
    print(f"  phi={phi}: IP={s['IP']:.2f} band=[{s['band_lo']:.2f},{s['band_hi']:.2f}] N={s['N']}  paper={s['paper_IP']:.2f}  delta={s['delta_vs_paper']:+.2f}")
print(f"  L1(IP_v6, IP_paper) = {l1:.2f}")
print(f"\nWrote {OUT}/summary.json")
print(f"Wrote {FIGD}/ip_vs_phi.{{png,pdf}}")
print(f"Wrote {FIGD}/tmax_timeseries_phi_all.{{png,pdf}}, per-phi PNGs, and tmax_pmax_panel.png")
