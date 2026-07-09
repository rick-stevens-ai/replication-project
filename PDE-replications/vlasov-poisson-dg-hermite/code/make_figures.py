"""Generate figures for the replication report."""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.abspath(os.path.join(HERE, "..", "results"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)


def fig_landau():
    d = np.load(os.path.join(RES, "landau_N64.npz"))
    t = d["t"]; E_max = d["E_max"]; E_l2 = d["E_l2"]
    gamma = float(d["gamma_fit"])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    ax.semilogy(t, E_max, "b-", lw=0.8, label=r"$\|E\|_\infty$")
    ax.semilogy(t, E_l2, "g-", lw=0.8, alpha=0.7, label=r"$\|E\|_2$")
    # Reference line  exp(-0.1533 t)
    t_ref = np.linspace(1, 18, 100)
    ax.semilogy(t_ref, 0.02 * np.exp(-0.1533 * t_ref), "r--", lw=1.2,
                label=r"$\propto e^{-0.1533\,t}$ (theory)")
    ax.semilogy(t_ref, 0.02 * np.exp(gamma * t_ref), "k:", lw=1.0,
                label=fr"fit: $\gamma={gamma:.4f}$")
    ax.set_xlabel("t")
    ax.set_ylabel("electric-field amplitude")
    ax.set_title("Linear Landau damping (k=0.5, α=0.01)\nNx=64, N_H=64, dt=0.005")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[1]
    # conservation diagnostics, all relative
    mass0 = d["mass"][0]; e0 = d["total_energy"][0]; l20 = d["l2"][0]
    ax.semilogy(t, np.abs(d["mass"] - mass0) / mass0 + 1e-18, label="|Δmass|/mass")
    ax.semilogy(t, np.abs(d["total_energy"] - e0) / abs(e0) + 1e-18, label="|ΔE_tot|/|E_tot|")
    ax.semilogy(t, np.abs(d["l2"] - l20) / l20 + 1e-18, label="|Δ‖f‖₂²|/‖f‖₂²")
    ax.semilogy(t, np.abs(d["momentum"]) + 1e-18, label="|momentum|")
    ax.set_xlabel("t")
    ax.set_ylabel("relative conservation error")
    ax.set_title("Conservation diagnostics (Landau)")
    ax.legend(fontsize=9, loc="best")
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_landau.png"), dpi=140)
    plt.close(fig)
    print("wrote fig_landau.png")


def fig_convergence():
    with open(os.path.join(RES, "convergence.json")) as fh:
        conv = json.load(fh)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    NH = [r["N_H"] for r in conv["NH_sweep"]]
    err = [r["rel_err_gamma"] for r in conv["NH_sweep"]]
    ax.semilogy(NH, err, "o-", color="C0")
    ax.set_xlabel(r"$N_H$ (Hermite modes)")
    ax.set_ylabel(r"relative error in $\gamma$")
    ax.set_title(r"Landau damping rate convergence vs Hermite truncation"
                 "\n(Nx=64 fixed)")
    ax.grid(True, which="both", alpha=0.3)
    # Annotate
    for nh, e in zip(NH, err):
        ax.annotate(f"{e:.2e}", (nh, e), fontsize=8, xytext=(3, 3), textcoords="offset points")

    ax = axes[1]
    Nx = [r["Nx"] for r in conv["Nx_sweep"]]
    e2 = [r["rel_err_gamma"] for r in conv["Nx_sweep"]]
    ax.semilogy(Nx, e2, "s-", color="C2")
    ax.set_xlabel("Nx (Fourier modes)")
    ax.set_ylabel(r"relative error in $\gamma$")
    ax.set_title(r"Landau damping rate vs spatial resolution"
                 "\n(N_H=48 fixed)")
    ax.grid(True, which="both", alpha=0.3)
    ax.set_ylim(1e-3, 1)

    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_convergence.png"), dpi=140)
    plt.close(fig)
    print("wrote fig_convergence.png")


def fig_two_stream():
    d = np.load(os.path.join(RES, "two_stream_classical.npz"))
    t = d["t"]; E_max = d["E_max"]; E_l2 = d["E_l2"]
    gamma = float(d["gamma_fit"])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    ax.semilogy(t, E_max, "b-", lw=0.8, label=r"$\|E\|_\infty$")
    ax.semilogy(t, E_l2, "g-", lw=0.8, alpha=0.7, label=r"$\|E\|_2$")
    t_ref = np.linspace(1, 10, 100)
    ax.semilogy(t_ref, 0.04 * np.exp(0.2845 * t_ref), "r--", lw=1.2,
                label=r"$\propto e^{+0.2845\,t}$ (theory)")
    ax.semilogy(t_ref, 0.04 * np.exp(gamma * t_ref), "k:", lw=1.0,
                label=fr"fit: $\gamma={gamma:.4f}$")
    ax.set_xlabel("t")
    ax.set_ylabel("electric-field amplitude")
    ax.set_title("Classical two-stream instability"
                 "\n(Filbet–Sonnendrücker IC, k=0.5, α=0.05, N_H=96)")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[1]
    mass0 = d["mass"][0]; e0 = d["total_energy"][0]; l20 = d["l2"][0]
    ax.semilogy(t, np.abs(d["mass"] - mass0) / mass0 + 1e-18, label="|Δmass|/mass")
    ax.semilogy(t, np.abs(d["total_energy"] - e0) / abs(e0) + 1e-18, label="|ΔE_tot|/|E_tot|")
    ax.semilogy(t, np.abs(d["l2"] - l20) / l20 + 1e-18, label="|Δ‖f‖₂²|/‖f‖₂²")
    ax.semilogy(t, np.abs(d["momentum"]) + 1e-18, label="|momentum|")
    ax.set_xlabel("t")
    ax.set_ylabel("relative conservation error")
    ax.set_title("Conservation diagnostics (two-stream)")
    ax.legend(fontsize=9, loc="best")
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_two_stream.png"), dpi=140)
    plt.close(fig)
    print("wrote fig_two_stream.png")


if __name__ == "__main__":
    fig_landau()
    fig_convergence()
    fig_two_stream()
