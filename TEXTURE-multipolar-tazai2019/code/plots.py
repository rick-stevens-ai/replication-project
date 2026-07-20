"""plots.py — generate figures for the report from saved .npz/.json."""
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Fig A: band structure + Fermi surface ---
from model import eps_c, H_full, MU


def fig_bands():
    nk = 200
    ks = np.linspace(-np.pi, np.pi, nk)
    # path Gamma-X-M-Gamma
    path = []
    for i in range(nk // 2):
        path.append((ks[nk // 2] * 0, 0))  # placeholder
    # simpler: sample lowest few bands along diagonal Gamma->M
    diag = np.linspace(0, np.pi, 100)
    bands = []
    for t in diag:
        w = np.linalg.eigh(H_full(t, t))[0]
        bands.append(w)
    bands = np.array(bands)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for b in range(6):
        ax[0].plot(diag / np.pi, bands[:, b], lw=1)
    ax[0].axhline(MU, color="k", ls="--", lw=0.8, label=f"$\\mu$={MU}")
    ax[0].set_xlabel(r"$k$ along $\Gamma\!\to\!M$ ($/\pi$)")
    ax[0].set_ylabel("energy")
    ax[0].set_title("(a) PAM band dispersion")
    ax[0].legend(fontsize=8)
    # Fermi surface map (lowest band crossing)
    KX, KY = np.meshgrid(np.linspace(-np.pi, np.pi, 160),
                         np.linspace(-np.pi, np.pi, 160), indexing="ij")
    E0 = np.zeros_like(KX)
    for i in range(KX.shape[0]):
        for j in range(KX.shape[1]):
            E0[i, j] = np.linalg.eigh(H_full(KX[i, j], KY[i, j]))[0][0]
    cs = ax[1].contour(KX / np.pi, KY / np.pi, E0, levels=[MU], colors="C3")
    ax[1].set_xlabel(r"$k_x/\pi$"); ax[1].set_ylabel(r"$k_y/\pi$")
    ax[1].set_title("(b) Fermi surface (lowest band)")
    ax[1].set_aspect("equal")
    fig.tight_layout()
    fig.savefig("fig_bands.png", dpi=130)
    print("wrote fig_bands.png")


def fig_qscan():
    d = np.load("qscan_paths.npz")
    seg = d["seg"]; n = len(seg)
    x = np.arange(n)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(x, d["Jz0"], label=r"$\chi^0_{J_z}$", color="C0")
    ax[0].plot(x, d["Oxy0"], label=r"$\chi^0_{O_{xy}}$", color="C3")
    ax[0].set_title("(a) bare bubble (channel-independent)")
    ax[0].set_ylabel(r"$\chi^0_Q(q,0)$")
    ax[0].legend(fontsize=9)
    ax[1].plot(x, d["JzR"], label=r"$\chi^{RPA}_{J_z}$", color="C0")
    ax[1].plot(x, d["OxyR"], label=r"$\chi^{RPA}_{O_{xy}}$", color="C3")
    ax[1].set_title("(b) RPA: magnetic dominates")
    ax[1].set_ylabel(r"$\chi^{RPA}_Q(q,0)$")
    ax[1].legend(fontsize=9)
    nk = 40; h = nk // 2
    for a in ax:
        a.set_xticks([0, h, 2 * h, n - 1])
        a.set_xticklabels([r"$\Gamma$", "X", "M", r"$\Gamma$"])
        a.axvline(h, color="gray", lw=0.4); a.axvline(2 * h, color="gray", lw=0.4)
    fig.tight_layout()
    fig.savefig("fig_qscan.png", dpi=130)
    print("wrote fig_qscan.png")


def fig_scaling():
    s = json.load(open("al_scaling_summary.json"))
    xis = np.array(s["xis"]); al = np.array(s["X_AL"]); mt = np.array(s["X_MT"])
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].loglog(xis, al, "o-", label=r"$X^{AL}\sim\xi^2$")
    ax[0].loglog(xis, mt, "s-", label=r"$X^{MT}\sim\log\xi$")
    ax[0].set_xlabel(r"$\xi$"); ax[0].set_ylabel("VC magnitude")
    ax[0].set_title("(a) AL vs MT scaling (2D)")
    ax[0].legend(fontsize=9)
    ax[1].semilogx(xis, al / mt, "^-", color="C2")
    ax[1].set_xlabel(r"$\xi$"); ax[1].set_ylabel(r"$X^{AL}/X^{MT}$")
    ax[1].set_title("(b) AL dominates near criticality")
    fig.tight_layout()
    fig.savefig("fig_scaling.png", dpi=130)
    print("wrote fig_scaling.png")


if __name__ == "__main__":
    fig_bands()
    fig_qscan()
    fig_scaling()
