"""Convergence + Cahn-Hilliard plots from the JSON result files."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

def conv_plot(json_path, title, out_png):
    d = json.loads(Path(json_path).read_text())
    grids = d["grids"]
    dx = np.array([g["dx"] for g in grids])
    l2 = np.array([g.get("L2_vs_ref", g.get("L2_vs_exact")) for g in grids])
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.loglog(dx, l2, "o-", label="FiPy L2 error")
    ref = l2[0] * (dx / dx[0]) ** 2
    ax.loglog(dx, ref, "k--", label=r"slope-2 reference")
    ax.set_xlabel(r"$\Delta x$")
    ax.set_ylabel("L2 error")
    ax.set_title(title)
    ax.grid(True, which="both", ls=":")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=140)
    plt.close(fig)
    print(f"wrote {out_png}")

def ch_plot(json_path, out_png):
    d = json.loads(Path(json_path).read_text())
    hist = d["history"]
    t = np.array([h["t"] for h in hist])
    F = np.array([h["F"] for h in hist])
    m = np.array([h["mass"] for h in hist])
    m_drift = m - m[0]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(t, F, "o-")
    ax1.set_xlabel("t"); ax1.set_ylabel("Free energy F[c]")
    ax1.set_title("Cahn-Hilliard: free energy (Lyapunov)")
    ax1.grid(True, ls=":")
    ax2.semilogy(t[1:], np.abs(m_drift[1:]) + 1e-20, "o-")
    ax2.set_xlabel("t"); ax2.set_ylabel("|mass(t) - mass(0)|")
    ax2.set_title(f"Mass drift (machine precision; max={np.max(np.abs(m_drift)):.1e})")
    ax2.grid(True, ls=":")
    fig.tight_layout()
    fig.savefig(out_png, dpi=140)
    plt.close(fig)
    print(f"wrote {out_png}")

if __name__ == "__main__":
    conv_plot(HERE / "results_self_convergence_1d.json",
              "1D diffusion: self-convergence vs FiPy ref (nx=2048)",
              HERE / "convergence_1d_self.png")
    conv_plot(HERE / "results_2d_mms.json",
              "2D diffusion (periodic, MMS): convergence vs exact",
              HERE / "convergence_2d_mms.png")
    ch_plot(HERE / "results_cahn_hilliard.json",
            HERE / "cahn_hilliard_conservation.png")
