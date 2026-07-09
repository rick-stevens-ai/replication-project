"""
LUCID100 partial-scope replication of Costes et al. 2007
(PLoS Comput Biol 3(8): e155, doi:10.1371/journal.pcbi.0030155).

This is NOT a full reproduction. The 2007 paper relies on private
HMEC-184 / HeLa microscopy data and an unreleased in-house Matlab +
DIPimage pipeline, plus a NASA-internal HZE / PFGE Monte Carlo
generator (Ponomarev & Cucinotta 2006). None of those artifacts were
deposited.

What IS reproducible from the paper text alone:

1. The relative-DNA-density estimator R_dna (Eq. 3).
2. The relative-DNA-gradient estimator R_grad (Eq. 4).
3. The DNA-density-weighted Monte Carlo "reshuffling" procedure
   used to place pseudo-foci (Eqs. 1, 2).
4. The qualitative claims from Figure 6:
     - foci on dense DNA   => R_dna > 1, R_grad ~ low
     - foci on edges       => R_grad > 1
     - foci on dim regions => R_dna < 1
5. The Poisson-like along-track distance distribution from Figure 3
   when foci are reshuffled proportionally to DNA density.

We reproduce 1-5 on SYNTHETIC nuclei built from a sum of 2-D
Gaussian "heterochromatin" blobs (a deliberate cartoon of the
random-walk-derived dense regions described in the Materials
and Methods section of the paper, where Ponomarev & Cucinotta's
random-walk chromosome packings are referenced but not provided).
This is a methods sanity check, not a quantitative test of the
biological claims.

Run:
    python3 rdna_rgrad_smoke.py

Outputs land in ../figs/ relative to this script.
"""

from __future__ import annotations

import os
import sys
import json
import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 0. Reproducibility
# ---------------------------------------------------------------------------
RNG = np.random.default_rng(20260609)

HERE = Path(__file__).resolve().parent
FIGDIR = HERE.parent / "figs"
FIGDIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = HERE.parent / "artifacts" / "smoke_results.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Synthetic nucleus
# ---------------------------------------------------------------------------
def synthetic_nucleus(
    size: int = 256,
    n_hetero_blobs: int = 40,
    blob_sigma_range: tuple[float, float] = (3.0, 8.0),
    radius: float = 110.0,
    background: float = 0.15,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Cartoon DAPI image: a circular nuclear mask filled with a smooth
    low-density background plus a number of Gaussian "heterochromatin"
    blobs.

    Returns
    -------
    dna : 2-D float array of "DNA density" (DAPI proxy), in [0, 1] roughly.
    mask : 2-D bool array, True inside the nucleus.
    """
    if rng is None:
        rng = RNG

    y, x = np.indices((size, size), dtype=float)
    cx, cy = size / 2.0, size / 2.0

    # nuclear mask
    rr = np.hypot(x - cx, y - cy)
    mask = rr <= radius

    # smooth low-density euchromatin background
    dna = np.where(mask, background, 0.0).astype(float)

    # heterochromatin blobs
    for _ in range(n_hetero_blobs):
        # random center inside an inner disc
        r = rng.uniform(0, radius * 0.85)
        theta = rng.uniform(0, 2 * np.pi)
        bx = cx + r * np.cos(theta)
        by = cy + r * np.sin(theta)
        sigma = rng.uniform(*blob_sigma_range)
        amp = rng.uniform(0.4, 1.0)
        g = amp * np.exp(-((x - bx) ** 2 + (y - by) ** 2) / (2 * sigma ** 2))
        dna += g

    dna *= mask
    # gentle PSF-like smoothing (sigma ~ 1 px, just to avoid pixel artefacts)
    dna = _gauss2d(dna, sigma=1.0)
    return dna, mask


def _gauss2d(img: np.ndarray, sigma: float) -> np.ndarray:
    """Separable Gaussian filter, FFT-free, small kernel."""
    if sigma <= 0:
        return img
    radius = max(1, int(math.ceil(3 * sigma)))
    k = np.arange(-radius, radius + 1, dtype=float)
    kernel = np.exp(-(k ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    # rows then cols
    tmp = np.apply_along_axis(lambda v: np.convolve(v, kernel, mode="same"), 1, img)
    out = np.apply_along_axis(lambda v: np.convolve(v, kernel, mode="same"), 0, tmp)
    return out


def gradient_magnitude(img: np.ndarray) -> np.ndarray:
    """Euclidian norm of the discrete gradient (central differences)."""
    gy, gx = np.gradient(img)
    return np.hypot(gx, gy)


# ---------------------------------------------------------------------------
# 2. Estimators -- the heart of the paper
# ---------------------------------------------------------------------------
def conservative_mask(mask: np.ndarray, shrink_px: int = 3) -> np.ndarray:
    """
    The paper uses a conservative inner contour (0.48 µm = 3 pixels inward
    at their 0.16 µm/px sampling) to avoid edge effects when measuring
    R_grad. We approximate with a simple morphological erosion.
    """
    inner = mask.copy()
    for _ in range(shrink_px):
        inner = (
            inner
            & np.roll(inner, 1, 0)
            & np.roll(inner, -1, 0)
            & np.roll(inner, 1, 1)
            & np.roll(inner, -1, 1)
        )
    return inner


def r_dna(dna: np.ndarray, foci_xy: np.ndarray, mask: np.ndarray) -> float:
    """
    R_dna = (mean DAPI intensity at foci centres) /
            (mean DAPI intensity over the nucleus).  Eq. 3 of the paper.
    """
    if len(foci_xy) == 0 or mask.sum() == 0:
        return float("nan")
    ix = foci_xy[:, 0].astype(int)
    iy = foci_xy[:, 1].astype(int)
    num = dna[iy, ix].mean()
    den = dna[mask].mean()
    return float(num / den) if den > 0 else float("nan")


def r_grad(dna: np.ndarray, foci_xy: np.ndarray, mask: np.ndarray) -> float:
    """
    R_grad = (mean |∇DAPI| at foci centres) /
             (mean |∇DAPI| over the conservative nucleus mask).  Eq. 4.
    """
    if len(foci_xy) == 0 or mask.sum() == 0:
        return float("nan")
    g = gradient_magnitude(dna)
    inner = conservative_mask(mask, shrink_px=3)
    ix = foci_xy[:, 0].astype(int)
    iy = foci_xy[:, 1].astype(int)
    num = g[iy, ix].mean()
    den = g[inner].mean()
    return float(num / den) if den > 0 else float("nan")


# ---------------------------------------------------------------------------
# 3. DNA-density-weighted Monte Carlo "reshuffling"
# ---------------------------------------------------------------------------
def reshuffle_foci(
    dna: np.ndarray,
    mask: np.ndarray,
    n_foci: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Sample n_foci pixel locations inside `mask` with probability
    proportional to `dna` (DAPI as DSB probability surface; Eq. 1-2).

    Returns array of shape (n, 2) in (x, y) order.
    """
    if rng is None:
        rng = RNG
    flat_dna = (dna * mask).ravel().astype(float)
    s = flat_dna.sum()
    if s <= 0:
        # uniform fallback (should not happen for our synthetic nuclei)
        flat_dna = mask.ravel().astype(float)
        s = flat_dna.sum()
    p = flat_dna / s
    idx = rng.choice(p.size, size=n_foci, p=p, replace=True)
    ys, xs = np.unravel_index(idx, dna.shape)
    return np.stack([xs, ys], axis=1).astype(float)


# ---------------------------------------------------------------------------
# 4. Hand-placed foci patterns (Figure 6 cartoon reproduction)
# ---------------------------------------------------------------------------
def pick_topk_pixels(score: np.ndarray, mask: np.ndarray, k: int) -> np.ndarray:
    """Return (x, y) of the top-k pixels of `score` within `mask`, well-separated."""
    s = np.where(mask, score, -np.inf)
    flat_order = np.argsort(s.ravel())[::-1]
    picks = []
    used = np.zeros_like(mask, dtype=bool)
    sep = 6  # pixel separation
    for f in flat_order:
        y, x = np.unravel_index(f, s.shape)
        if not mask[y, x]:
            continue
        if used[max(0, y - sep) : y + sep + 1, max(0, x - sep) : x + sep + 1].any():
            continue
        picks.append((x, y))
        used[y, x] = True
        if len(picks) >= k:
            break
    return np.array(picks, dtype=float)


# ---------------------------------------------------------------------------
# 5. Synthetic along-track foci for Figure 3 style distance distribution
# ---------------------------------------------------------------------------
def along_track_distances(
    dna: np.ndarray, mask: np.ndarray, track_y: int, n_foci: int, n_iter: int = 50
) -> np.ndarray:
    """
    Mimic the 1-D track analysis: along a single horizontal line through
    the nucleus, sample `n_foci` positions each iteration with probability
    proportional to DAPI along that line, then collect sorted nearest-
    neighbour distances. Repeat n_iter times.
    """
    profile = dna[track_y].astype(float) * mask[track_y]
    s = profile.sum()
    if s <= 0:
        return np.array([])
    p = profile / s
    dists = []
    for _ in range(n_iter):
        xs = np.sort(RNG.choice(p.size, size=n_foci, p=p, replace=True))
        d = np.diff(np.unique(xs))
        dists.extend(d.tolist())
    return np.array(dists, dtype=float)


# ---------------------------------------------------------------------------
# 6. Run smoke tests
# ---------------------------------------------------------------------------
def main() -> int:
    dna, mask = synthetic_nucleus()

    # ---- 6.1  Figure 6 cartoon: foci on dense / interface / dim ----
    grad = gradient_magnitude(dna)
    dense_foci = pick_topk_pixels(dna, mask, 40)
    edge_foci = pick_topk_pixels(grad, conservative_mask(mask), 40)
    dim_foci = pick_topk_pixels(-dna * mask + (~mask) * (-1e9), mask, 40)

    results = {
        "panel_A_dense": {
            "r_dna": r_dna(dna, dense_foci, mask),
            "r_grad": r_grad(dna, dense_foci, mask),
            "n_foci": int(len(dense_foci)),
        },
        "panel_C_interface": {
            "r_dna": r_dna(dna, edge_foci, mask),
            "r_grad": r_grad(dna, edge_foci, mask),
            "n_foci": int(len(edge_foci)),
        },
        "panel_E_dim": {
            "r_dna": r_dna(dna, dim_foci, mask),
            "r_grad": r_grad(dna, dim_foci, mask),
            "n_foci": int(len(dim_foci)),
        },
    }

    # ---- 6.2  Density-weighted Monte Carlo reshuffle: expect R~1 ----
    n_mc = 100
    mc_rdna, mc_rgrad = [], []
    for _ in range(n_mc):
        f = reshuffle_foci(dna, mask, n_foci=40)
        mc_rdna.append(r_dna(dna, f, mask))
        mc_rgrad.append(r_grad(dna, f, mask))
    results["mc_density_weighted_reshuffle"] = {
        "n_iter": n_mc,
        "n_foci_per_iter": 40,
        "r_dna_mean": float(np.mean(mc_rdna)),
        "r_dna_std": float(np.std(mc_rdna)),
        "r_grad_mean": float(np.mean(mc_rgrad)),
        "r_grad_std": float(np.std(mc_rgrad)),
        "note": (
            "DNA-density-weighted sampling is the Monte Carlo 'reshuffle' "
            "used in the paper. Reshuffled foci should give R_dna and "
            "R_grad both >1 on a non-uniform DAPI image because dense "
            "regions also have stronger gradients. Paper's Table 2 reports "
            "R_dna ~ 1.10, R_grad ~ 1.09 for simulated pRIF, and R1/R2 "
            "ratios ~ 1.0 between pRIF and reshuffled pRIF."
        ),
    }

    # ---- 6.3  Uniformly-random foci: control for R~1 ish wrt mask ----
    n_uni = 100
    uni_rdna, uni_rgrad = [], []
    flat_mask = mask.ravel().astype(float)
    p_unif = flat_mask / flat_mask.sum()
    for _ in range(n_uni):
        idx = RNG.choice(p_unif.size, size=40, p=p_unif, replace=True)
        ys, xs = np.unravel_index(idx, mask.shape)
        f = np.stack([xs, ys], axis=1).astype(float)
        uni_rdna.append(r_dna(dna, f, mask))
        uni_rgrad.append(r_grad(dna, f, mask))
    results["mc_uniform_in_mask"] = {
        "n_iter": n_uni,
        "n_foci_per_iter": 40,
        "r_dna_mean": float(np.mean(uni_rdna)),
        "r_dna_std": float(np.std(uni_rdna)),
        "r_grad_mean": float(np.mean(uni_rgrad)),
        "r_grad_std": float(np.std(uni_rgrad)),
        "note": "Uniform-in-mask control should give R_dna ~ 1 and R_grad ~ 1 by construction.",
    }

    # ---- 6.4  Figure 3-style along-track distance histogram ----
    ty = dna.shape[0] // 2
    d_mc = along_track_distances(dna, mask, ty, n_foci=20, n_iter=200)
    results["along_track_distance_hist"] = {
        "track_y": int(ty),
        "n_foci_per_iter": 20,
        "n_iter": 200,
        "n_distances": int(d_mc.size),
        "mean_distance_px": float(d_mc.mean()) if d_mc.size else float("nan"),
        "median_distance_px": float(np.median(d_mc)) if d_mc.size else float("nan"),
        "note": (
            "Distance distribution between consecutive density-weighted "
            "foci along a single horizontal line through the synthetic "
            "nucleus. Paper Fig 3A shows a similar Poisson-like decreasing "
            "histogram for simulated 1 GeV/amu Fe tracks."
        ),
    }

    # ---- 6.5  Save figures ----
    _save_panel_figure(dna, mask, dense_foci, edge_foci, dim_foci, results)
    _save_distance_hist(d_mc)
    _save_mc_summary(mc_rdna, mc_rgrad, uni_rdna, uni_rgrad)

    # ---- 6.6  Persist numeric results ----
    OUT_JSON.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"\nWrote {OUT_JSON}")
    print(f"Figures written to {FIGDIR}")

    # ---- 6.7  Sanity-check assertions for CI-style smoke ----
    ok = True
    a = results["panel_A_dense"]["r_dna"]
    e = results["panel_C_interface"]["r_grad"]
    d = results["panel_E_dim"]["r_dna"]
    print()
    print(f"Sanity: R_dna(dense)={a:.3f}  (expect > 1)")
    print(f"Sanity: R_grad(edge)={e:.3f}  (expect > 1)")
    print(f"Sanity: R_dna(dim)={d:.3f}  (expect < 1)")
    ok &= a > 1
    ok &= e > 1
    ok &= d < 1
    print(f"Sanity: MC density-weighted R_dna={results['mc_density_weighted_reshuffle']['r_dna_mean']:.3f}  (expect > 1)")
    print(f"Sanity: MC uniform-in-mask R_dna={results['mc_uniform_in_mask']['r_dna_mean']:.3f}  (expect ~ 1)")
    return 0 if ok else 2


def _save_panel_figure(dna, mask, dense, edge, dim, results):
    grad = gradient_magnitude(dna)
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    panels = [
        ("A: foci on dense DNA", dense, "panel_A_dense"),
        ("C: foci on DNA edges", edge, "panel_C_interface"),
        ("E: foci on dim DNA", dim, "panel_E_dim"),
    ]
    for col, (title, foci, key) in enumerate(panels):
        ax = axes[0, col]
        ax.imshow(dna, cmap="Blues", origin="upper")
        ax.scatter(foci[:, 0], foci[:, 1], s=12, c="red", edgecolors="white", linewidths=0.4)
        ax.set_title(f"{title}\nR_dna={results[key]['r_dna']:.2f}")
        ax.set_axis_off()
        ax = axes[1, col]
        ax.imshow(grad, cmap="magma", origin="upper")
        ax.scatter(foci[:, 0], foci[:, 1], s=12, c="cyan", edgecolors="black", linewidths=0.4)
        ax.set_title(f"|∇DAPI|, R_grad={results[key]['r_grad']:.2f}")
        ax.set_axis_off()
    fig.suptitle(
        "Costes et al. 2007 Figure 6 cartoon — synthetic nucleus, hand-placed foci",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig6_cartoon.png", dpi=140)
    plt.close(fig)


def _save_distance_hist(distances):
    fig, ax = plt.subplots(figsize=(6, 4))
    if distances.size:
        ax.hist(distances, bins=30, color="darkgreen", alpha=0.8, edgecolor="k")
    ax.set_xlabel("Distance between consecutive density-weighted foci (px)")
    ax.set_ylabel("Count")
    ax.set_title(
        "Costes 2007 Figure 3-style: along-track distance histogram\n"
        "(synthetic nucleus, density-weighted Monte Carlo reshuffle)"
    )
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig3_style_distance_hist.png", dpi=140)
    plt.close(fig)


def _save_mc_summary(mc_rdna, mc_rgrad, uni_rdna, uni_rgrad):
    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(
        [mc_rdna, mc_rgrad, uni_rdna, uni_rgrad],
        tick_labels=[
            "MC dens-wt\nR_dna",
            "MC dens-wt\nR_grad",
            "MC uniform\nR_dna",
            "MC uniform\nR_grad",
        ],
        patch_artist=True,
    )
    for patch, color in zip(bp["boxes"], ["#5577dd", "#5577dd", "#aaaaaa", "#aaaaaa"]):
        patch.set_facecolor(color)
    ax.axhline(1.0, color="red", linestyle="--", lw=0.8, label="reference = 1")
    ax.set_ylabel("ratio")
    ax.set_title("Monte Carlo control: density-weighted vs uniform reshuffle")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGDIR / "mc_reshuffle_box.png", dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
