#!/usr/bin/env python3
"""Plot success probability vs query count k for each (q, d)."""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("results.json") as f:
    R = json.load(f)

# Group by (q, d) -> list of (k, avg_p_measured, k_opt, regime)
by_qd = {}
for s in R["summary"]:
    by_qd.setdefault((s["q"], s["d"]), []).append(
        (s["k"], s["avg_p_success_measured"], s["k_opt"], s["regime"], s["avg_classical_success"])
    )

fig, ax = plt.subplots(1, 1, figsize=(8, 5.5))
markers = {2:"o", 3:"s"}
colors = {7:"tab:blue", 11:"tab:orange", 13:"tab:green"}

for (q, d), pts in sorted(by_qd.items()):
    pts.sort()
    ks = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    lbl = f"q={q}, d={d} (k_opt={pts[0][2]})"
    ax.plot(ks, ys, marker=markers[d], color=colors[q], linestyle="-",
            label=lbl, markersize=9, linewidth=1.5)

ax.axhline(0.9, color="grey", linestyle=":", linewidth=1)
ax.text(2.02, 0.905, "0.9 success threshold", fontsize=8, color="grey")

# Mark classical baseline: k = d+1 always -> 1.0
ax.scatter([3, 4], [1.0, 1.0], marker="*", s=200, color="black",
           label="classical baseline (d+1 queries)", zorder=5)

ax.set_xlabel("Number of quantum queries k", fontsize=12)
ax.set_ylabel("Success probability  |<c|IQFT|c_{R_k}>|²", fontsize=12)
ax.set_title("Childs–van Dam–Hung–Shparlinski (arXiv:1509.09271):\nQuantum polynomial interpolation over $F_q$, real numpy statevector",
             fontsize=11)
ax.set_ylim(-0.05, 1.08)
ax.set_xticks([2, 3, 4])
ax.legend(loc="lower right", fontsize=8)
ax.grid(True, alpha=0.3)

# Annotate the two theoretical predictions
ax.annotate("Theorem 2(i): d odd, k=(d+1)/2 → 1/k! ≈ 0.5\n(pts approach 0.5 as q grows)",
            xy=(2, 0.4), xytext=(2.2, 0.55),
            fontsize=8, ha="left",
            arrowprops=dict(arrowstyle="->", color="grey", lw=0.7))
ax.annotate("Theorem 2(ii): d even, k=d/2+1 → 1-O(1/q)",
            xy=(2, 0.99), xytext=(2.3, 0.82),
            fontsize=8, ha="left",
            arrowprops=dict(arrowstyle="->", color="grey", lw=0.7))

plt.tight_layout()
plt.savefig("success_vs_queries.png", dpi=140)
plt.savefig("success_vs_queries.pdf")
print("Wrote success_vs_queries.{png,pdf}")

# Second plot: success prob at k_opt as function of q, for odd d (should -> 1/k!)
fig2, ax2 = plt.subplots(1, 1, figsize=(7, 4.5))
qs = [7, 11, 13]
odd_pts = []
for q in qs:
    for s in R["summary"]:
        if s["q"]==q and s["d"]==3 and s["k"]==2:
            odd_pts.append((q, s["avg_p_success_measured"]))
odd_pts.sort()
ax2.plot([p[0] for p in odd_pts], [p[1] for p in odd_pts], "o-", label="measured (d=3, k=2)")
ax2.axhline(0.5, color="red", linestyle="--", label="paper asymptote 1/k! = 1/2")
# Theoretical curve 1/2 * (1 - c/q)
xs = np.linspace(6, 14, 100)
# Fit c from our points: p = 0.5 * (1 - c/q)  -> c = q * (1 - 2p)
cs = [q*(1 - 2*p) for (q,p) in odd_pts]
c_est = np.mean(cs)
ax2.plot(xs, 0.5*(1 - c_est/xs), "g:", label=f"fit 0.5·(1 - {c_est:.2f}/q)")
ax2.set_xlabel("q (finite field size)")
ax2.set_ylabel("success prob at k=(d+1)/2=2")
ax2.set_title("Odd-d asymptote check: 1/k!·(1-O(1/q)) approaching 1/2")
ax2.set_ylim(0.25, 0.55)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("odd_d_asymptote.png", dpi=140)
plt.savefig("odd_d_asymptote.pdf")
print("Wrote odd_d_asymptote.{png,pdf}")
print(f"Estimated leading-order c from fit: {c_est:.3f}")
