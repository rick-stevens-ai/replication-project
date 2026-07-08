"""Plot RB decay curves for the three protocols on one MU(4,8) channel."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

evidence = Path(__file__).resolve().parent.parent / "report" / "evidence"

# Compare-protocols data
with open(evidence / "results_compare.json") as fp:
    cmp = json.load(fp)
m_list = cmp["config"]["m_list"]
ch = cmp["per_channel"][0]  # first channel

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(m_list, ch["P_full"], "o-", label=f"P1 full Haar (F={ch['F_full']:.4f})", color="tab:blue")
ax.plot(m_list, ch["P_gen"],  "s-", label=f"P2 generators b=3 (F={ch['F_gen']:.4f})", color="tab:orange")
ax.plot(m_list, ch["P_apx"],  "^-", label=f"P3 approx-Haar b=15 (F={ch['F_apx']:.4f})", color="tab:green")
ax.axhline(1.0/4, color="gray", linestyle=":", alpha=0.6, label="1/d (asymptote)")
ax.set_xlabel("sequence length m")
ax.set_ylabel(r"survival probability $\langle 0|\rho_{\rm out}|0\rangle$")
ax.set_title("Approximate RB for MU(4,8), p=0.95, single random-state channel\n"
             r"True $F$ = {:.5f}".format(ch["F_true"]))
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
out = evidence / "rb_three_protocols.png"
plt.savefig(out, dpi=150)
print("wrote", out)

# Monomial replication (Table 1 style)
with open(evidence / "results_monomial.json") as fp:
    mon = json.load(fp)
res = mon["results"]
ds = sorted({r["d"] for r in res})
Ms = sorted({r["M"] for r in res})
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for M in Ms:
    xs = []
    ys = []
    yerrs = []
    for d in ds:
        for r in res:
            if r["d"] == d and r["M"] == M:
                xs.append(d)
                ys.append(r["mean_error"])
                yerrs.append(r["std_error"] / np.sqrt(r["n_channels"]))
    ax.errorbar(xs, np.array(ys)*1e3, yerr=np.array(yerrs)*1e3, marker="o", label=f"M = {M}", capsize=3)
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xlabel("dimension d = 2^n")
ax.set_ylabel(r"mean $|F - \hat F|$   ($\times 10^{-3}$)")
ax.set_title("Fidelity-estimation error for MU(d,8) RB (p=0.9)\n"
             "cf. paper Table 1 (paper reaches ~1-10 ×10^-3 at d≥64)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
plt.tight_layout()
out2 = evidence / "monomial_error_vs_d.png"
plt.savefig(out2, dpi=150)
print("wrote", out2)
