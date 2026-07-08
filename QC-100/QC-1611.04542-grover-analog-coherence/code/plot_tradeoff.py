"""Plot the coherence <-> success-probability tradeoff for n=3,4,5."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EV = Path(__file__).resolve().parents[1] / "report" / "evidence"

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, n in zip(axes, [3, 4, 5]):
    data = json.loads((EV / f"grover_coherence_n{n}.json").read_text())
    recs = data["records"]
    ks = [r["k"] for r in recs]
    ps = [r["p_success"] for r in recs]
    cs = [r["c_l1"] for r in recs]
    crs = [r["c_relative_entropy"] for r in recs]
    ax2 = ax.twinx()
    ax.plot(ks, ps, "o-", color="tab:blue", label="P_success")
    ax2.plot(ks, cs, "s--", color="tab:red", label="C_l1")
    ax2.plot(ks, crs, "d:", color="tab:orange", label="C_r (rel. ent.)")
    ax.axvline(data["k_opt_theory_rounded"], color="k", ls=":", alpha=0.5,
               label=f"k_opt={data['k_opt_theory_rounded']}")
    ax.set_xlabel("Grover iteration k")
    ax.set_ylabel("P_success", color="tab:blue")
    ax2.set_ylabel("Coherence", color="tab:red")
    ax.set_title(f"n={n} qubits (N={2**n})")
    ax.set_ylim(0, 1.05)
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labs1 + labs2, loc="center right", fontsize=8)

plt.suptitle("arXiv:1611.04542 replication: coherence collapses as success peaks")
plt.tight_layout()
out = EV / "coherence_success_tradeoff.png"
plt.savefig(out, dpi=140)
print("wrote", out)
