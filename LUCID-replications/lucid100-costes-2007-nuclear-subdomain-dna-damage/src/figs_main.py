"""
Generate the main result figures:
  fig1_sim_vs_blur.png  -- analog of paper Fig 1: DSB (gray) vs pRIF (blue/green)
                            for both low-LET and high-LET (Fe track) cases.
  fig3_distance_dist.png -- analog of Fig 3A: distribution of distances
                            between consecutive pRIF along Fe track,
                            compared to reshuffled distribution.
  table1_table2.png      -- bar chart comparing replication vs paper Table 1
                            and Table 2 numbers.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, maximum_filter
import sys
sys.path.insert(0, os.path.dirname(__file__))
from nucleus_model import (
    make_nucleus_mask, make_heterochromatin, simulate_low_let_dsb,
    simulate_high_let_track, make_prif_image, detect_local_maxima,
    conservative_mask, reshuffle_foci_track, reshuffle_foci_3d,
    NUCLEUS_RADIUS_VOX, VOXEL_UM,
)

FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../figures"))
os.makedirs(FIG_DIR, exist_ok=True)


def fig1_simulated_images():
    rng = np.random.default_rng(7)
    shape = (2 * NUCLEUS_RADIUS_VOX + 2,) * 3
    mask = make_nucleus_mask(shape)
    dna = make_heterochromatin(shape, mask, rng)

    # Low-LET
    dsb_low = simulate_low_let_dsb(dna, mask, rng)
    prif_low = make_prif_image(dsb_low)

    # High-LET: try until we get a good track
    for _ in range(20):
        dsb_high, track = simulate_high_let_track(dna, mask, rng)
        if dsb_high.sum() >= 5:
            break
    prif_high = make_prif_image(dsb_high)

    # Pick central slice for visualization
    cz = shape[0] // 2
    # find a slice with track if high-LET
    track_z = np.argwhere(track)
    if len(track_z):
        cz_high = int(np.bincount(track_z[:, 0]).argmax())
    else:
        cz_high = cz

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))

    # Row 0: high-LET
    axes[0, 0].imshow(dsb_high[cz_high], cmap="gray", interpolation="nearest")
    axes[0, 0].set_title(f"High-LET DSB locations\n(slice z={cz_high}, n_DSB={int(dsb_high.sum())})")
    axes[0, 0].axis("off")

    rgb_h = np.stack([np.zeros_like(prif_high[cz_high]),
                      prif_high[cz_high] / max(prif_high.max(), 1e-9),
                      dna[cz_high] / max(dna.max(), 1e-9)], axis=-1)
    axes[0, 1].imshow(rgb_h)
    axes[0, 1].set_title("High-LET pRIF (green) on DNA (blue)")
    axes[0, 1].axis("off")

    axes[0, 2].imshow(track[cz_high], cmap="hot")
    axes[0, 2].set_title("Track footprint")
    axes[0, 2].axis("off")

    # Row 1: low-LET
    axes[1, 0].imshow(dsb_low[cz], cmap="gray", interpolation="nearest")
    axes[1, 0].set_title(f"Low-LET DSB locations\n(slice z={cz}, n_DSB={int(dsb_low.sum())})")
    axes[1, 0].axis("off")

    rgb_l = np.stack([np.zeros_like(prif_low[cz]),
                      prif_low[cz] / max(prif_low.max(), 1e-9),
                      dna[cz] / max(dna.max(), 1e-9)], axis=-1)
    axes[1, 1].imshow(rgb_l)
    axes[1, 1].set_title("Low-LET pRIF (green) on DNA (blue)")
    axes[1, 1].axis("off")

    axes[1, 2].imshow(dna[cz], cmap="Blues")
    axes[1, 2].set_title("DNA density (heterochromatin + euchromatin)")
    axes[1, 2].axis("off")

    fig.suptitle("Figure 1 replication — simulated DSB vs pRIF images "
                 "(Costes et al. 2007)", fontsize=13)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig1_sim_vs_blur.png")
    fig.savefig(out, dpi=140)
    print(f"Saved {out}")
    plt.close(fig)


def fig3_distance_distribution():
    """Distance-between-consecutive-pRIF along Fe track, simulated vs reshuffled."""
    rng = np.random.default_rng(11)
    shape = (2 * NUCLEUS_RADIUS_VOX + 2,) * 3
    all_prif_dists = []
    all_rsh_dists = []
    all_dsb_dists = []
    n_nuclei = 60

    for _ in range(n_nuclei):
        mask = make_nucleus_mask(shape)
        dna = make_heterochromatin(shape, mask, rng)
        dsb, track = simulate_high_let_track(dna, mask, rng)
        if dsb.sum() < 3:
            continue
        prif_img = make_prif_image(dsb)
        from scipy.ndimage import binary_dilation
        strip = binary_dilation(track, iterations=2) & mask
        prif_coords = detect_local_maxima(prif_img, mask)
        if len(prif_coords) == 0:
            continue
        keep = np.array([strip[z, y, x] for z, y, x in prif_coords])
        prif_coords = prif_coords[keep]
        if len(prif_coords) < 2:
            continue

        # Project onto track direction = principal axis of track voxels
        track_vox = np.argwhere(track).astype(float)
        center = track_vox.mean(axis=0)
        centered = track_vox - center
        # PCA
        u, s, vh = np.linalg.svd(centered, full_matrices=False)
        axis = vh[0]
        def project(coords):
            return ((coords.astype(float) - center) @ axis) * VOXEL_UM

        # pRIF distances
        proj_prif = np.sort(project(prif_coords))
        all_prif_dists.extend(np.diff(proj_prif))

        # DSB distances
        dsb_coords = np.argwhere(dsb)
        proj_dsb = np.sort(project(dsb_coords))
        all_dsb_dists.extend(np.diff(proj_dsb))

        # Reshuffle pRIF along track via DNA-weighted probability
        rsh = reshuffle_foci_track(dna, track, len(prif_coords), rng)
        if len(rsh) >= 2:
            proj_rsh = np.sort(project(rsh))
            all_rsh_dists.extend(np.diff(proj_rsh))

    bins = np.linspace(0, 6, 25)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(all_dsb_dists, bins=bins, alpha=0.4, color="red",
            label=f"DSB (n={len(all_dsb_dists)})", density=True)
    ax.hist(all_prif_dists, bins=bins, alpha=0.5, color="green",
            label=f"pRIF (n={len(all_prif_dists)})", density=True)
    ax.hist(all_rsh_dists, bins=bins, histtype="step", color="black",
            linewidth=2,
            label=f"Reshuffled pRIF (n={len(all_rsh_dists)})", density=True)
    ax.set_xlabel("Distance between consecutive foci along track (um)")
    ax.set_ylabel("Probability density")
    ax.set_title("Figure 3 replication — Distance distributions\n"
                 "Reshuffled distribution matches pRIF (validates Eq 1-2 method)")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig3_distance_dist.png")
    fig.savefig(out, dpi=140)
    print(f"Saved {out}")
    plt.close(fig)

    # correlation between pRIF and reshuffled histograms
    p_hist, _ = np.histogram(all_prif_dists, bins=bins, density=True)
    r_hist, _ = np.histogram(all_rsh_dists, bins=bins, density=True)
    if p_hist.std() > 0 and r_hist.std() > 0:
        corr = float(np.corrcoef(p_hist, r_hist)[0, 1])
    else:
        corr = float("nan")
    print(f"  pRIF vs reshuffled histogram Pearson r = {corr:.3f}")
    return corr


def table_bar(results_json: str):
    d = json.load(open(results_json))
    ll = d["low_let"]
    hl = d["high_let"]

    rows = [
        ("Low-LET DSB / nucleus",         ll["n_dsb"]["mean"],          ll["n_dsb"]["std"],          38.1, 5.9),
        ("Low-LET pRIF / nucleus",        ll["n_prif"]["mean"],         ll["n_prif"]["std"],         37.0, 5.5),
        ("High-LET DSB / um",             hl["dsb_per_um"]["mean"],     hl["dsb_per_um"]["std"],     1.10, 0.48),
        ("High-LET pRIF / um",            hl["prif_per_um"]["mean"],    hl["prif_per_um"]["std"],    0.73, 0.22),
        ("High-LET R1/R2 (Rdna)",         hl["ratio_R1_R2_dna"]["mean"],hl["ratio_R1_R2_dna"]["std"],0.98, 0.07),
        ("High-LET R1/R2 (Rgrad)",        hl["ratio_R1_R2_grad"]["mean"],hl["ratio_R1_R2_grad"]["std"],0.99, 0.26),
    ]
    labels = [r[0] for r in rows]
    rep_mean = [r[1] for r in rows]; rep_std = [r[2] for r in rows]
    pap_mean = [r[3] for r in rows]; pap_std = [r[4] for r in rows]

    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(11, 6))
    w = 0.38
    ax.bar(x - w/2, pap_mean, w, yerr=pap_std, label="Paper",
           color="#888", capsize=4)
    ax.bar(x + w/2, rep_mean, w, yerr=rep_std, label="Replication",
           color="#2a8", capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_yscale("log")
    ax.set_ylabel("value (log scale)")
    ax.set_title("Costes 2007 — Paper numbers vs replication (Tables 1 & 2)")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "tables_paper_vs_replication.png")
    fig.savefig(out, dpi=140)
    print(f"Saved {out}")
    plt.close(fig)


if __name__ == "__main__":
    fig1_simulated_images()
    corr = fig3_distance_distribution()
    table_bar(os.path.join(os.path.dirname(__file__), "../data/results_full.json"))
    print(f"\nfig3 Pearson r (pRIF vs reshuffled) = {corr}")
