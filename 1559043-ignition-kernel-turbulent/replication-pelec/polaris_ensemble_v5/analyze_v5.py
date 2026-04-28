#!/usr/bin/env python3
"""Analyze v5 PeleC ensemble (AMR-level-1, 5ms target window).
Parses run.log TIME/Temp lines, computes IP, generates figures.
"""
import re, glob, os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LINE_RE = re.compile(r"TIME\s*=\s*([0-9.eE+-]+)\s+Temp\s+MIN\s*=\s*([0-9.eE+-]+)\s+MAX\s*=\s*([0-9.eE+-]+)")
SRC = "/tmp/v5_harvest"
OUT = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec/polaris_ensemble_v5")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "figures"), exist_ok=True)

# Ignition criteria — paper definition: sustained flame, not just kernel transient.
# A run is ignited iff at the end of its available window, T_max remains above the
# combustion threshold (≥2000 K) — i.e. there is a self-sustaining hot region after
# the seeded kernel has had time to either propagate or be quenched.
T_END_IGN = 2000.0     # K, T_max at last available step must exceed this

phis = [0.6, 0.8, 1.0, 1.2]
runs = {}
for phi in phis:
    runs[phi] = []
    for r in range(1, 6):
        f = os.path.join(SRC, f"temp_phi{phi}_r{r}.tsv")
        if not os.path.exists(f):
            continue
        ts, tmin_, tmax_ = [], [], []
        with open(f) as fh:
            for line in fh:
                m = LINE_RE.search(line)
                if not m:
                    continue
                ts.append(float(m.group(1)))
                tmin_.append(float(m.group(2)))
                tmax_.append(float(m.group(3)))
        ts = np.array(ts); tmax = np.array(tmax_); tmin = np.array(tmin_)
        runs[phi].append({"r": r, "t": ts, "Tmax": tmax, "Tmin": tmin,
                          "t_final": ts[-1] if len(ts) else 0.0})

# Classify
def classify(rec):
    t, T = rec["t"], rec["Tmax"]
    tf = rec["t_final"]
    if len(t) == 0:
        return None
    # Filter late window: t > 1.5e-3
    late = T[t > 1.5e-3]
    early = T[(t > 0.5e-3) & (t <= 1.5e-3)]
    end_T = T[-1]
    rec["T_end"] = float(end_T)
    rec["T_late_max"] = float(late.max()) if late.size else float("nan")
    rec["T_late_mean"] = float(late.mean()) if late.size else float("nan")
    rec["T_early_max"] = float(early.max()) if early.size else float("nan")
    rec["T_global_max"] = float(T.max())
    # Single criterion: end-of-available-window T_max > 2000 K means a self-sustaining
    # flame is present. This is paper-faithful (if the kernel quenches the run is
    # "failed"; if it sustains it's "ignited").
    rec["ignited"] = bool(end_T > T_END_IGN)
    rec["ign_reason"] = "sustained" if end_T > T_END_IGN else "quenched"
    rec["complete"] = tf >= 4.5e-3
    return rec

per_run = []
for phi in phis:
    for rec in runs[phi]:
        rec["phi"] = phi
        classify(rec)
        per_run.append(rec)
        print(f"phi={phi} r={rec['r']} t_f={rec['t_final']*1000:.2f}ms "
              f"Tmax_global={rec['T_global_max']:.0f} Tlate_max={rec['T_late_max']:.0f} "
              f"T_end={rec['T_end']:.0f} ignited={rec['ignited']} ({rec['ign_reason']}) "
              f"complete={rec['complete']}")

# IP per phi (Wilson 1σ band)
def wilson_band(p, n, z=1.0):
    if n == 0:
        return (float("nan"), float("nan"))
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denom
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))

ip = {}
for phi in phis:
    rs = runs[phi]
    n = len(rs)
    nig = sum(1 for r in rs if r["ignited"])
    p = nig / n if n else float("nan")
    lo, hi = wilson_band(p, n)
    ip[phi] = {"N": n, "N_ignited": nig, "IP": p, "band_lo": lo, "band_hi": hi,
               "n_complete": sum(1 for r in rs if r["complete"])}

# Paper Fig 3 IP values
paper_ip = {0.6: 0.0, 0.8: 0.20, 1.0: 0.65, 1.2: 0.90}

summary = {
    "ensemble": "v5_amr1_5ms",
    "criteria": {"T_END_IGN": T_END_IGN,
                 "definition": "T_max at last available step > 2000 K = sustained flame"},
    "IP": {str(k): v for k, v in ip.items()},
    "paper_IP": {str(k): v for k, v in paper_ip.items()},
    "per_run": [{k: (v if not isinstance(v, np.ndarray) else None)
                 for k, v in r.items() if k not in ("t", "Tmax", "Tmin")}
                for r in per_run],
}
def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return None
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o
with open(os.path.join(OUT, "summary.json"), "w") as f:
    json.dump(_clean(summary), f, indent=2)

# === Figures ===
# 1. IP vs phi with band
fig, ax = plt.subplots(figsize=(7, 5))
xs = phis
ys = [ip[p]["IP"] for p in phis]
los = [ip[p]["IP"] - ip[p]["band_lo"] for p in phis]
his = [ip[p]["band_hi"] - ip[p]["IP"] for p in phis]
ax.errorbar(xs, ys, yerr=[los, his], fmt="o-", color="C0", lw=2, capsize=6,
            label=f"v5 PeleC (AMR L=1, 5ms target, N=5/φ)")
ax.plot(list(paper_ip.keys()), list(paper_ip.values()), "s--", color="C3",
        label="Paper Fig 3 (Jaravel et al. 2019)")
for p in phis:
    ax.annotate(f"{ip[p]['N_ignited']}/{ip[p]['N']}",
                (p, ip[p]["IP"]), textcoords="offset points", xytext=(8, -10), fontsize=9)
    if ip[p]["n_complete"] < ip[p]["N"]:
        ax.annotate(f"({ip[p]['n_complete']} compl)",
                    (p, ip[p]["IP"]), textcoords="offset points", xytext=(8, 8), fontsize=8, color="gray")
ax.set_xlabel(r"Equivalence ratio $\phi$")
ax.set_ylabel("Ignition probability $P_{ign}$")
ax.set_title("Ignition probability vs $\\phi$ — v5 ensemble (AMR L=1)")
ax.set_ylim(-0.05, 1.1)
ax.set_xlim(0.5, 1.3)
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "figures", "ignition_probability_vs_phi.png"), dpi=140)
plt.close(fig)

# 2. Tmax timeseries
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = {0.6: "C0", 0.8: "C2", 1.0: "C1", 1.2: "C3"}
for phi in phis:
    for rec in runs[phi]:
        ax.plot(rec["t"]*1000, rec["Tmax"], color=colors[phi], alpha=0.4, lw=0.8)
    # Mean
    if runs[phi]:
        # Resample to common grid
        tgrid = np.linspace(0, max(r["t_final"] for r in runs[phi]), 400)
        Tg = []
        for rec in runs[phi]:
            if len(rec["t"]) > 5:
                Tg.append(np.interp(tgrid, rec["t"], rec["Tmax"], right=np.nan))
        if Tg:
            Tg = np.array(Tg)
            mean = np.nanmean(Tg, axis=0)
            ax.plot(tgrid*1000, mean, color=colors[phi], lw=2.5,
                    label=f"$\\phi={phi}$ mean (N={len(runs[phi])})")
ax.axhline(2700, color="gray", ls=":", alpha=0.5, label="T=2700K")
ax.set_xlabel("time [ms]")
ax.set_ylabel(r"$T_{\max}$ [K]")
ax.set_title("Maximum temperature — v5 ensemble (5ms target, AMR L=1)")
ax.set_ylim(400, 3500)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", ncol=2)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "figures", "Tmax_vs_t.png"), dpi=140)
plt.close(fig)

print("\n=== IP summary ===")
for p in phis:
    s = ip[p]
    pp = paper_ip[p]
    print(f"  phi={p}: IP={s['IP']:.2f} band=[{s['band_lo']:.2f},{s['band_hi']:.2f}] N={s['N']} (compl {s['n_complete']})  paper={pp:.2f}")
print(f"\nWrote: {OUT}/summary.json + figures/")
