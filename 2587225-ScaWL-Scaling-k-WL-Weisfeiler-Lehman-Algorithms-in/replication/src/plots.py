"""Generate scaling plots for the ScaWL replication."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent.parent / "results"
FIGS = Path(__file__).resolve().parent.parent / "figures"
FIGS.mkdir(parents=True, exist_ok=True)


def strong_scaling():
    data = json.loads((RESULTS / "main_n200.json").read_text())
    recs = data["results"]
    p = np.array([r["procs"] for r in recs])
    t = np.array([r["time_s"] for r in recs])
    sp = np.array([r["speedup"] for r in recs])

    # ScaWL paper Table 4 (2-WL, averaged): {1:1, 2:2.38, 4:4.26, 8:7.64, 16:13.20, 20:16.06}
    paper_p = np.array([1, 2, 4, 8, 16, 20])
    paper_sp = np.array([1.0, 2.38, 4.26, 7.64, 13.20, 16.06])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.loglog(p, t, "o-", color="#0b6e4f", lw=2, label="This work (n=200, d=4)")
    ax1.loglog(p, t[0] / p, "--", color="gray", label="Ideal T(1)/p")
    ax1.set_xlabel("Worker processes p")
    ax1.set_ylabel("Runtime (s)")
    ax1.set_title("Strong scaling — runtime")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend()

    ax2.plot(p, sp, "o-", color="#0b6e4f", lw=2, label="This work")
    ax2.plot(paper_p, paper_sp, "s--", color="#c94a4a", lw=1.5, label="ScaWL paper (Table 4 avg)")
    ax2.plot(p, p, ":", color="gray", label="Ideal linear")
    ax2.set_xlabel("Worker processes p")
    ax2.set_ylabel("Speedup  T(1)/T(p)")
    ax2.set_title("Strong scaling — speedup")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    fig.tight_layout()
    fig.savefig(FIGS / "strong_scaling.pdf")
    fig.savefig(FIGS / "strong_scaling.png", dpi=150)
    print("wrote strong_scaling.{pdf,png}")


def size_scaling():
    ns, ts = [], []
    for f in sorted(RESULTS.glob("size_n*.json")):
        d = json.loads(f.read_text())
        ns.append(d["config"]["n"])
        ts.append(d["results"][0]["time_s"])
    ns = np.array(ns); ts = np.array(ts)

    # fit log-log
    coeffs = np.polyfit(np.log(ns), np.log(ts), 1)
    slope = coeffs[0]

    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.loglog(ns, ts, "o-", color="#355691", lw=2, label=f"Measured (p=8)")
    ref = ts[0] * (ns / ns[0]) ** 3
    ax.loglog(ns, ref, "--", color="gray", label=r"$O(n^3)$ reference")
    ax.set_xlabel("Graph size n")
    ax.set_ylabel("Runtime (s)")
    ax.set_title(f"Problem-size scaling — fitted slope = {slope:.2f}")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGS / "size_scaling.pdf")
    fig.savefig(FIGS / "size_scaling.png", dpi=150)
    print(f"wrote size_scaling.{{pdf,png}} (slope={slope:.2f})")


if __name__ == "__main__":
    strong_scaling()
    size_scaling()
