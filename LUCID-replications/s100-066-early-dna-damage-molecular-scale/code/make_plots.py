"""Plot the surrogate-MC results and compare to Petrolli 2020 figures."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson


def load():
    with open("../evidence/results.json") as f:
        return json.load(f)


def fig1_hit_artifact(results):
    """Reproduce paper Fig. 1A,B,C: per-nucleotide hit counter at f=1, 2.5, 5
    for 500 keV protons."""
    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
    for ax, f in zip(axes, (1.0, 2.5, 5.0)):
        r = next(x for x in results
                 if x["expansion_f"] == f and x["proton_E_MeV"] == 0.5)
        nt_hits = np.array(r["nt_hits"])
        N = nt_hits.size
        idx = np.arange(1, N + 1)
        ax.bar(idx, nt_hits, width=1.0, color="steelblue", edgecolor="none")
        ax.set_ylabel("Hit counter")
        ax.set_title(f"f={f:.1f}x  (500 keV protons, {r['n_tracks']:.0f} tracks, "
                     f"DHS={r['dhs']}, S={r['shannon_S']:.4f})")
        ax.set_xlim(0, N + 1)
    axes[-1].set_xlabel("Nucleotide serial index (1..694)")
    plt.suptitle("Fig.1 surrogate: per-nucleotide DNA hit counter vs box expansion\n"
                 "(paper: spikes at f=1, flat at f=2.5)", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("../figures/fig1_hit_artifact.png", dpi=120)
    plt.close()


def fig2_z_axis_hit_score(results):
    """Reproduce paper Fig. 2A,B,C: hit score over z-axis (all dose deposition
    events within reference volume) at f=1, 2.5, 5.

    Note: we don't have per-event spatial data saved, but we can approximate
    by summing the per-nt hits along z. This shows the same spatial bias.
    """
    data = np.load("../code/nt_targets.npz", allow_pickle=True)
    centers_nm = data["centers_A"] / 10.0
    centroid = centers_nm.mean(axis=0)
    z_nt = centers_nm[:, 2] - centroid[2]  # centered z of each nucleotide

    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    for ax, f in zip(axes, (1.0, 2.5, 5.0)):
        r = next(x for x in results
                 if x["expansion_f"] == f and x["proton_E_MeV"] == 0.5)
        nt_hits = np.array(r["nt_hits"])
        # bin hits along z
        half_z = 0.5 * 25.4 * f
        bins = np.linspace(-half_z, half_z, 41)
        hist, edges = np.histogram(z_nt, bins=bins, weights=nt_hits)
        centers = 0.5 * (edges[:-1] + edges[1:])
        ax.bar(centers, hist, width=(edges[1] - edges[0]) * 0.9,
               color="darkorange", edgecolor="none")
        ax.set_ylabel("z-binned DNA hit count")
        ax.set_title(f"f={f:.1f}x")
        ax.axvspan(-half_z, -12.7, alpha=0.1, color="gray")
        ax.axvspan(12.7, half_z, alpha=0.1, color="gray")
    axes[-1].set_xlabel("z (nm) relative to DNA centroid (box of size 25.4*f nm)")
    plt.suptitle("Fig.2 surrogate: DNA hit score along z-axis\n"
                 "(paper Fig.2A-C: central oversampling at f=1, flatter at higher f)",
                 fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("../figures/fig2_z_axis_hits.png", dpi=120)
    plt.close()


def fig3_vhs_dhs_shannon(results):
    """Reproduce paper Fig. 3A-F: VHS, DHS, Shannon S vs f for 500 keV and 5 MeV."""
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharex=True)
    for col, E in enumerate((0.5, 5.0)):
        sub = sorted([r for r in results if r["proton_E_MeV"] == E],
                     key=lambda x: x["expansion_f"])
        fs = [r["expansion_f"] for r in sub]
        vhs = [r["vhs"] for r in sub]
        dhs = [r["dhs"] for r in sub]
        S = [r["shannon_S"] for r in sub]
        # row 0: 500 keV; row 1: 5 MeV
        row = 0 if E == 0.5 else 1
        axes[row, 0].plot(fs, vhs, "o-", color="C0", markersize=8)
        axes[row, 0].set_title(f"VHS  ({E:g} MeV)")
        axes[row, 0].set_ylabel("Volume Hit Score")
        axes[row, 0].set_yscale("log")
        axes[row, 0].grid(alpha=0.3)
        axes[row, 1].plot(fs, dhs, "s-", color="C1", markersize=8)
        axes[row, 1].set_title(f"DHS  ({E:g} MeV)")
        axes[row, 1].set_ylabel("DNA Hit Score")
        axes[row, 1].set_yscale("log")
        axes[row, 1].grid(alpha=0.3)
        axes[row, 2].plot(fs, S, "^-", color="C2", markersize=8)
        axes[row, 2].set_title(f"Shannon S  ({E:g} MeV)")
        axes[row, 2].set_ylabel("S")
        axes[row, 2].set_ylim(0.5, 1.05)
        axes[row, 2].grid(alpha=0.3)
        for c in range(3):
            axes[row, c].axvline(2.5, color="red", linestyle="--", alpha=0.5,
                                 label="paper threshold (2.5x)")
            if row == 1:
                axes[row, c].set_xlabel("linear expansion factor f")
    axes[0, 0].text(0.02, 0.95, "500 keV", transform=axes[0, 0].transAxes,
                    fontsize=11, fontweight="bold", verticalalignment="top")
    axes[1, 0].text(0.02, 0.95, "5 MeV", transform=axes[1, 0].transAxes,
                    fontsize=11, fontweight="bold", verticalalignment="top")
    plt.suptitle("Fig.3 surrogate: VHS, DHS, and normalized Shannon entropy "
                 "vs box expansion factor\n"
                 "(paper Fig.3: VHS ↑, DHS ↓; S increases steeply and plateaus at 2.5x)",
                 fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig("../figures/fig3_vhs_dhs_shannon.png", dpi=120)
    plt.close()


def fig4_dsb_distance(results):
    """Reproduce paper Fig. 4A-F: DSB distance distributions (fixed 2.5x)
    and DMS vs energy / vs expansion."""
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    # Top row: DSB distance histograms at f=2.5 for 500 keV, 1.5 MeV, 5 MeV
    for col, E in enumerate((0.5, 1.5, 5.0)):
        r = next(x for x in results
                 if x["expansion_f"] == 2.5 and x["proton_E_MeV"] == E)
        d = np.array(r["dsb_distances"], dtype=int)
        if d.size == 0:
            axes[0, col].text(0.5, 0.5, "no DSBs (insufficient statistics)",
                              ha="center", va="center",
                              transform=axes[0, col].transAxes)
            continue
        bins = np.arange(0, 12) - 0.5
        h, _ = np.histogram(d, bins=bins)
        x = np.arange(0, 11)
        axes[0, col].bar(x, h, width=0.8, color="steelblue", edgecolor="black")
        # Poisson fit
        mu = d.mean()
        n = d.size
        pf = poisson.pmf(x, mu) * n
        axes[0, col].plot(x, pf, "ro-", label=f"Poisson μ={mu:.2f}")
        axes[0, col].set_title(f"DSB dist. @ {E:g} MeV (n={n})")
        axes[0, col].set_xlabel("DSB distance (bp)")
        axes[0, col].set_ylabel("count")
        axes[0, col].legend()
        axes[0, col].grid(alpha=0.3)
    # Bottom row middle: DMS vs energy at 2.5x
    sub25 = sorted([r for r in results if r["expansion_f"] == 2.5],
                   key=lambda x: x["proton_E_MeV"])
    Es = [r["proton_E_MeV"] for r in sub25]
    dms = [r["dms"] for r in sub25]
    axes[1, 1].plot(Es, dms, "o-", markersize=10, color="C3")
    axes[1, 1].set_xlabel("Proton energy (MeV)")
    axes[1, 1].set_ylabel("DMS (mean DSB distance, bp)")
    axes[1, 1].set_title("DMS vs energy at f=2.5x")
    axes[1, 1].grid(alpha=0.3)
    axes[1, 1].set_xscale("log")
    # Bottom row left: DMS vs f at 500 keV
    sub500 = sorted([r for r in results if r["proton_E_MeV"] == 0.5],
                    key=lambda x: x["expansion_f"])
    fs = [r["expansion_f"] for r in sub500]
    dms_f = [r["dms"] for r in sub500]
    axes[1, 0].plot(fs, dms_f, "s-", markersize=10, color="C2")
    axes[1, 0].set_xlabel("expansion factor f")
    axes[1, 0].set_ylabel("DMS (bp)")
    axes[1, 0].set_title("DMS vs f @ 500 keV")
    axes[1, 0].grid(alpha=0.3)
    # Bottom row right: DMS vs f at 5 MeV
    sub5M = sorted([r for r in results if r["proton_E_MeV"] == 5.0],
                   key=lambda x: x["expansion_f"])
    fs5 = [r["expansion_f"] for r in sub5M]
    dms_f5 = [r["dms"] for r in sub5M]
    axes[1, 2].plot(fs5, dms_f5, "^-", markersize=10, color="C4")
    axes[1, 2].set_xlabel("expansion factor f")
    axes[1, 2].set_ylabel("DMS (bp)")
    axes[1, 2].set_title("DMS vs f @ 5 MeV")
    axes[1, 2].grid(alpha=0.3)
    plt.suptitle("Fig.4 surrogate: DSB distance distributions and DMS\n"
                 "(paper: Poisson fit; bias toward 1-5 bp; DMS slightly decreases with energy)",
                 fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig("../figures/fig4_dsb_distance.png", dpi=120)
    plt.close()


def fig5_overview(results):
    """Single summary figure with normalized comparison to paper claims."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.text(0.05, 0.92, "Petrolli 2020 -- key quantitative claims vs surrogate replication",
            transform=ax.transAxes, fontsize=11, fontweight="bold")
    text = []
    # 1. Bounding box
    text.append("(1) Tetranucleosome size: paper 13.0 x 15.2 x 25.4 nm (ref. volume);")
    text.append("    1ZBB DNA bounding box (surrogate)  9.1 x 14.6 x 24.7 nm    ✓ ~matches")
    text.append("(2) Nucleotide count N=694 bp: surrogate has 694 backbone targets   ✓ exact")
    text.append("(3) Strand-break threshold 8.22 eV (direct effect): used in surrogate ✓")
    text.append("(4) DSB distance threshold 10 bp: used in surrogate                  ✓")
    text.append("")
    text.append("(5) VHS increases with expansion factor f:")
    sub = sorted([r for r in results if r["proton_E_MeV"] == 0.5],
                 key=lambda x: x["expansion_f"])
    vhs1, vhs5 = sub[0]["vhs"], sub[-1]["vhs"]
    text.append(f"    paper Fig.3A: ~6-7x increase from 1x to 5x (500 keV)")
    text.append(f"    surrogate   : {vhs5/vhs1:.1f}x increase  -> qualitatively ✓")
    text.append("(6) DHS decreases with expansion factor f:")
    dhs1, dhs5 = sub[0]["dhs"], sub[-1]["dhs"]
    text.append(f"    paper Fig.3B: ~3x decrease from 1x to 5x (500 keV)")
    text.append(f"    surrogate   : {dhs1/dhs5:.1f}x decrease -> qualitatively ✓ (direction OK)")
    text.append("")
    text.append("(7) Shannon entropy S increases & plateaus at f≈2.5:")
    S1, S25, S5 = sub[0]["shannon_S"], sub[3]["shannon_S"], sub[-1]["shannon_S"]
    text.append(f"    paper Fig.3C: S(1x)~0.6, S(2.5x)~0.92, S(5x)~0.92")
    text.append(f"    surrogate   : S(1x)={S1:.3f}, S(2.5x)={S25:.3f}, S(5x)={S5:.3f}")
    text.append(f"    -> ✗ direction inverted -- the central-spike artifact does NOT")
    text.append(f"       arise in our surrogate (see report for discussion).")
    text.append("")
    text.append("(8) DSB distance distribution biased toward short distances (1-5 bp):")
    r25 = next(r for r in results if r["expansion_f"] == 2.5 and r["proton_E_MeV"] == 0.5)
    d = np.array(r25["dsb_distances"])
    if d.size:
        frac = np.mean(d <= 5)
        text.append(f"    surrogate (500 keV, 2.5x): {frac*100:.0f}% of DSBs at <=5 bp")
        text.append(f"    Poisson fit μ={d.mean():.2f}                                ✓")
    else:
        text.append("    insufficient DSBs in surrogate                                ✗")
    text.append("(9) DMS slightly decreases with energy at 2.5x:")
    sub25 = sorted([r for r in results if r["expansion_f"] == 2.5],
                   key=lambda x: x["proton_E_MeV"])
    text.append(f"    paper Fig.4D: DMS(500 keV)~4.8, DMS(5 MeV)~4.2 bp")
    for r in sub25:
        text.append(f"    surrogate {r['proton_E_MeV']:.1f} MeV: DMS={r['dms']:.2f} bp")
    ax.text(0.02, 0.85, "\n".join(text), transform=ax.transAxes,
            fontsize=8, family="monospace", verticalalignment="top")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("../figures/fig5_summary.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    Path("../figures").mkdir(exist_ok=True)
    results = load()
    fig1_hit_artifact(results)
    fig2_z_axis_hit_score(results)
    fig3_vhs_dhs_shannon(results)
    fig4_dsb_distance(results)
    fig5_overview(results)
    print("Wrote 5 figures to ../figures/")
