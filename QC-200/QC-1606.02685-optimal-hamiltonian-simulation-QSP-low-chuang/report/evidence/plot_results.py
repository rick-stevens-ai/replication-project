#!/usr/bin/env python3
"""Generate plots: (i) truncation error vs K (super-exp decay);
(ii) Kmin vs log(1/eps)/loglog(1/eps) grouped by t (linear fit)."""
import csv, math, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Plot 1: truncation error vs K ----
data = {}
with open(os.path.join(HERE, "trunc_err_vs_K.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        t = float(row["t"]); K = int(row["K"]); err = float(row["err_spectral_norm"])
        data.setdefault(t, []).append((K, err))

fig, ax = plt.subplots(figsize=(6, 4))
for t, pts in sorted(data.items()):
    pts = sorted(pts)
    Ks = [p[0] for p in pts]; errs = [max(p[1], 1e-17) for p in pts]
    ax.semilogy(Ks, errs, marker="o", ms=3, label=f"t={t}")
ax.set_xlabel("truncation order K")
ax.set_ylabel(r"$\|e^{-iHt} - A_K\|_2$")
ax.set_title("Claim (A): Jacobi-Anger truncation error")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_A_truncation_vs_K.png"), dpi=140)
plt.close(fig)

# ---- Plot 2: Kmin vs x = log(1/eps)/loglog(1/eps) ----
data2 = {}
with open(os.path.join(HERE, "min_K_vs_eps.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        t = float(row["t"]); eps = float(row["eps"]); Kmin = int(row["Kmin"])
        data2.setdefault(t, []).append((eps, Kmin))

fig, ax = plt.subplots(figsize=(6, 4))
for t, pts in sorted(data2.items()):
    xs = [math.log(1/e) / math.log(math.log(1/e)) for e, _ in pts]
    ys = [K for _, K in pts]
    ax.plot(xs, ys, marker="s", label=f"t={t}")
ax.set_xlabel(r"$\log(1/\epsilon) / \log\log(1/\epsilon)$")
ax.set_ylabel(r"$K_{\min}(t,\epsilon)$")
ax.set_title("Claim (B): Optimal query scaling")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B_Kmin_vs_x.png"), dpi=140)
plt.close(fig)

# ---- Plot 3: intercept vs t (should be linear) ----
ints = {}
with open(os.path.join(HERE, "results.json")) as f:
    R = json.load(f)
fits = R["claim_B_fits_by_t"]
ts = sorted(float(k) for k in fits.keys())
intercepts = [fits[str(t) if str(t) in fits else f"{t:.1f}"]["intercept"]
              for t in ts]
# Try both string forms.
intercepts = []
for t in ts:
    key = None
    for k in fits.keys():
        if abs(float(k) - t) < 1e-6:
            key = k; break
    intercepts.append(fits[key]["intercept"])
slope, off = np.polyfit(ts, intercepts, 1)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(ts, intercepts, "o", ms=8, label="fitted intercept")
xx = np.linspace(min(ts), max(ts), 50)
ax.plot(xx, slope * xx + off, "--", label=f"linear fit: {slope:.3f} t + {off:.3f}")
ax.set_xlabel("t")
ax.set_ylabel("intercept b(t)")
ax.set_title(r"Claim (B): intercept scales linearly in $t$")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B_intercept_vs_t.png"), dpi=140)
plt.close(fig)

print("Wrote 3 PNGs.")
