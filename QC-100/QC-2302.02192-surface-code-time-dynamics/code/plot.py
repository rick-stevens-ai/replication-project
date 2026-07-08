#!/usr/bin/env python3
"""Plot per-round LER vs distance for the two variants."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"
data = json.loads((EVID / "results.json").read_text())

ds  = [r["distance"] for r in data["results_per_distance"]]
prs = [r["standard"]["per_round_p_L"] for r in data["results_per_distance"]]
prt = [r["time_dynamic"]["per_round_p_L"] for r in data["results_per_distance"]]

# guard: replace 0 with an upper bound = 1/shots for log plot
def clean(x, shots):
    return x if x > 0 else 1.0/shots
shots = [r["num_shots"] for r in data["results_per_distance"]]
prs2 = [clean(p, s) for p, s in zip(prs, shots)]
prt2 = [clean(p, s) for p, s in zip(prt, shots)]

plt.figure(figsize=(6.5,4.5))
plt.semilogy(ds, prs2, "o-", label="Standard rotated surface code (baseline)")
plt.semilogy(ds, prt2, "s--", label="Unrotated surface code (time-dyn variant)")
# annotate d=7 std as upper bound
for d, p_L, s in zip(ds, prs, shots):
    if p_L == 0:
        plt.annotate(f"<{1.0/s:.1e}", (d, 1.0/s), textcoords="offset points", xytext=(6,-4), fontsize=8)
plt.xlabel("Code distance d")
plt.ylabel("Logical error per round")
plt.title("arXiv:2302.02192 replication\nSurface code memory @ p=1e-3, rounds=d")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(EVID / "ler_vs_distance.png", dpi=150)
print("wrote", EVID / "ler_vs_distance.png")
