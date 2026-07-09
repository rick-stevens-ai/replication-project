"""Plot |1 - <O>| vs number of qubits for unmitigated / RE / LRE.
Mirrors the qualitative message of Fig. 6 and Table I of arXiv:2402.04000."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

for path in sys.argv[1:]:
    data = json.loads(Path(path).read_text())
    rows = data["rows"]
    xs = [r["n_qubits"] for r in rows]
    yu = [r["unmitigated"] for r in rows]
    yr = [r["re"] for r in rows]
    yl = [r["lre"] for r in rows]

    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(xs, yu, "o-", label="Unmitigated")
    ax.plot(xs, yr, "s-", label="Global RE (linear, scales 1,3,5)")
    ax.plot(xs, yl, "^-", label="LRE (linear, per-layer)")
    ax.set_xlabel("Number of qubits n")
    ax.set_ylabel(r"$|1 - \langle O \rangle|$ (mean abs. estimation error)")
    ax.set_yscale("log")
    ax.set_title(f"LRE vs RE on GHZ-like circuit (γ={data['meta']['noise_model'].split('=')[-1]})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    out = path.replace(".json", ".png")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print("Wrote", out)
