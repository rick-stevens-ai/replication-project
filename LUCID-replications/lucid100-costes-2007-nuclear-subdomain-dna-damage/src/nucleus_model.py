"""
Costes et al. 2007 (PLoS Comput Biol 3(8):e155) — replication of the
core image-based model.

We cannot replicate the experimental RIF measurements (Tables 1, 3, Figs 4-9)
because (a) the raw microscope DAPI + cH2AX/53BP1/ATMp image stacks were
never released, and (b) the original DSB-along-Fe-track Monte Carlo
(Ponomarev/Cucinotta 2006, refs 22/24) is a separate amorphous-track-
structure code that was also not released.

What this code DOES replicate:
  * Synthetic 3-D nucleus with heterochromatin (random-walk dense bands)
    and lower-density euchromatin, on 0.16 um voxels (paper Methods).
  * Low-LET DSB generation as a Poisson process with probability per
    voxel proportional to local DNA density (paper Eq 5: w = 1 - exp(-Q*D*rho)).
  * High-LET 1 GeV/amu Fe DSB generation: a linear track through the
    nucleus, with linear DSB density tuned so total DSBs match Table 1.
  * pRIF construction: Gaussian blur with sigma = 0.16 um (paper PSF)
    followed by local-maxima detection.
  * Frequencies (Table 1): DSB and pRIF per nucleus (low LET) and per
    micron-of-track (high LET).
  * Reshuffling validation (Table 2): generate pRIF, then re-place the
    SAME NUMBER of foci via DNA-weighted Monte Carlo, and verify
    R1/R2 of Rdna and Rgrad are ~1 (paper: 0.98 +/- 0.07 and 0.99 +/- 0.26).
  * Demonstration of Rdna and Rgrad metric definitions (Eq 3, 4) on three
    hand-placed foci patterns (paper Fig 6).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter, sobel

# --------------------------------------------------------------------------- #
# Constants from paper Methods / Table 1
# --------------------------------------------------------------------------- #
VOXEL_UM = 0.16                   # pixel size, paper Methods
PSF_SIGMA_UM = 0.16               # Gaussian blur sigma, paper Methods
PSF_SIGMA_VOX = PSF_SIGMA_UM / VOXEL_UM  # = 1.0
NUCLEUS_RADIUS_UM = 5.0           # typical HMEC-184 ~10 um diameter
NUCLEUS_RADIUS_VOX = int(round(NUCLEUS_RADIUS_UM / VOXEL_UM))   # 31

# Target frequencies from Table 1 (we tune Q so DSBs match)
TARGET_DSB_LOW_LET = 38.1         # DSB / nucleus, 1 Gy gamma
# Paper measures pRIF/um = 0.73 +/- 0.22 and DSB/um in synthetic = 1.10 +/- 0.48.
# Since pRIF is what's actually observed in the imaging chain, calibrate to that
# (pRIF/um = 0.73). Our DSB-rate input becomes:
TARGET_DSB_HIGH_LET_PER_UM = 0.73 * (1.10 / 0.73)  # = 1.10 (same as paper's DSB rate)
TARGET_PRIF_HIGH_LET_PER_UM = 0.73                  # paper Table 1

# Inward erosion for conservative nuclear mask used in Rdna/Rgrad
CONSERVATIVE_INSET_UM = 0.48
CONSERVATIVE_INSET_VOX = int(round(CONSERVATIVE_INSET_UM / VOXEL_UM))  # 3


# --------------------------------------------------------------------------- #
# Synthetic nucleus
# --------------------------------------------------------------------------- #

def make_nucleus_mask(shape: tuple[int, int, int]) -> np.ndarray:
    """Spherical boolean mask centered in `shape`."""
    z, y, x = np.indices(shape)
    cz, cy, cx = [(s - 1) / 2 for s in shape]
    r2 = (z - cz) ** 2 + (y - cy) ** 2 + (x - cx) ** 2
    return r2 <= NUCLEUS_RADIUS_VOX ** 2


def make_heterochromatin(shape: tuple[int, int, int],
                         mask: np.ndarray,
                         rng: np.random.Generator,
                         n_walks: int = 18,
                         steps_per_walk: int = 800,
                         step_um: float = 0.2) -> np.ndarray:
    """
    Random-walk chromosome territory model (paper Methods, ref 23 Munkel99):
    a few self-avoiding-ish random walks deposit DNA into voxels;
    pixels visited many times become "heterochromatin" (high density);
    pixels visited rarely or never form the "euchromatin" baseline.
    """
    dna = np.zeros(shape, dtype=np.float32)
    step_vox = step_um / VOXEL_UM

    nz, ny, nx = shape
    coords = np.argwhere(mask)

    for _ in range(n_walks):
        start = coords[rng.integers(0, len(coords))]
        pos = start.astype(np.float64)
        for _ in range(steps_per_walk):
            # random unit-vector step
            v = rng.normal(size=3)
            v /= np.linalg.norm(v) + 1e-12
            new_pos = pos + v * step_vox
            iz, iy, ix = int(round(new_pos[0])), int(round(new_pos[1])), int(round(new_pos[2]))
            if not (0 <= iz < nz and 0 <= iy < ny and 0 <= ix < nx):
                continue
            if not mask[iz, iy, ix]:
                continue
            pos = new_pos
            dna[iz, iy, ix] += 1.0

    # Add euchromatin baseline so empty pixels still have some signal
    base = mask.astype(np.float32) * 0.5
    dna = dna + base

    # Smooth slightly so adjacent voxels are correlated (paper Methods says
    # neighboring pixels are slightly correlated [26])
    dna = gaussian_filter(dna, sigma=0.7)
    dna[~mask] = 0.0
    return dna


# --------------------------------------------------------------------------- #
# DSB generation (Eq 5)
# --------------------------------------------------------------------------- #

def simulate_low_let_dsb(dna: np.ndarray,
                         mask: np.ndarray,
                         rng: np.random.Generator,
                         target_count: float = TARGET_DSB_LOW_LET) -> np.ndarray:
    """
    Low-LET (gamma) DSB generation. Paper Eq 5: w = 1 - exp(-Q * D * rho).
    For 1 Gy gamma we want ~38 DSB per nucleus. We pick Q so expected
    sum(w) = target_count, then draw Bernoulli per voxel.
    """
    rho = dna * mask
    total_rho = rho.sum()
    Q = target_count / max(total_rho, 1e-12)        # since dose D=1 Gy folded into Q
    w = 1.0 - np.exp(-Q * rho)
    draws = rng.random(rho.shape) < w
    return draws  # boolean mask of DSB voxels


def simulate_high_let_track(dna: np.ndarray,
                            mask: np.ndarray,
                            rng: np.random.Generator,
                            per_um: float = TARGET_DSB_HIGH_LET_PER_UM
                            ) -> tuple[np.ndarray, np.ndarray]:
    """
    1 GeV/amu Fe ion: a straight line through the nucleus.
    Place DSBs as a Poisson process along the track with linear density
    `per_um`, then weight by local DNA density (paper Methods).
    Returns (dsb_bool, track_voxels_bool).
    """
    nz, ny, nx = mask.shape
    cz, cy, cx = (nz - 1) / 2, (ny - 1) / 2, (nx - 1) / 2

    # Random direction approximately in-plane (Costes images cells in 2D slices
    # for tracks); we pick a direction in y-x and a random z offset.
    theta = rng.uniform(0, 2 * np.pi)
    direction = np.array([0.0, np.sin(theta), np.cos(theta)])
    # Random z slice
    z0 = cz + rng.uniform(-NUCLEUS_RADIUS_VOX / 2, NUCLEUS_RADIUS_VOX / 2)

    # Walk the line in fine steps
    n_steps = int(2 * NUCLEUS_RADIUS_VOX / 0.5) + 1
    ts = np.linspace(-NUCLEUS_RADIUS_VOX, NUCLEUS_RADIUS_VOX, n_steps)
    pts = np.array([z0 + 0 * ts, cy + direction[1] * ts, cx + direction[2] * ts]).T

    track = np.zeros_like(mask, dtype=bool)
    track_voxel_set = set()
    for p in pts:
        iz, iy, ix = int(round(p[0])), int(round(p[1])), int(round(p[2]))
        if 0 <= iz < nz and 0 <= iy < ny and 0 <= ix < nx and mask[iz, iy, ix]:
            track[iz, iy, ix] = True
            track_voxel_set.add((iz, iy, ix))

    track_voxels = np.array(sorted(track_voxel_set))
    if len(track_voxels) == 0:
        return np.zeros_like(mask, dtype=bool), track

    # Track length in microns (unique voxels along line * voxel size)
    track_len_um = len(track_voxels) * VOXEL_UM

    # DNA density along track
    dna_track = np.array([dna[iz, iy, ix] for iz, iy, ix in track_voxels])
    # Normalize so probability proportional to dna density
    p = dna_track / max(dna_track.sum(), 1e-12)

    expected_dsb = per_um * track_len_um
    # Number of DSBs: draw from Poisson with mean expected_dsb
    n_dsb = rng.poisson(expected_dsb)

    dsb = np.zeros_like(mask, dtype=bool)
    if n_dsb > 0:
        choices = rng.choice(len(track_voxels), size=n_dsb, replace=True, p=p)
        for c in choices:
            iz, iy, ix = track_voxels[c]
            dsb[iz, iy, ix] = True
    return dsb, track


# --------------------------------------------------------------------------- #
# pRIF: blur + local maxima
# --------------------------------------------------------------------------- #

def make_prif_image(dsb_bool: np.ndarray) -> np.ndarray:
    """Apply Gaussian blur with sigma = PSF_SIGMA_VOX (= 1 voxel = 0.16 um)."""
    return gaussian_filter(dsb_bool.astype(np.float32), sigma=PSF_SIGMA_VOX)


def detect_local_maxima(img: np.ndarray,
                        mask: np.ndarray,
                        min_dist_vox: int = 2,
                        rel_threshold: float = 0.05) -> np.ndarray:
    """Find local-maxima coordinates in a 3-D blurred image (voxel coords).
    `min_dist_vox` = 2 corresponds to the paper's "more than two-pixel gap to
    be separate, which corresponds to 0.48 um" (Fig 3 caption)."""
    if img.max() <= 0:
        return np.zeros((0, 3), dtype=int)
    size = 2 * min_dist_vox + 1
    maxf = maximum_filter(img, size=size, mode="constant", cval=0.0)
    peaks = (img == maxf) & (img > rel_threshold * img.max()) & mask
    coords = np.argwhere(peaks)
    return coords


# --------------------------------------------------------------------------- #
# Rdna, Rgrad metrics (Eq 3, 4)
# --------------------------------------------------------------------------- #

def conservative_mask(mask: np.ndarray, inset_vox: int = CONSERVATIVE_INSET_VOX) -> np.ndarray:
    """Erode mask inward by `inset_vox` voxels (paper Methods: 0.48 um inward)."""
    from scipy.ndimage import binary_erosion
    struct = np.ones((3, 3, 3), dtype=bool)
    out = mask.copy()
    for _ in range(inset_vox):
        out = binary_erosion(out, structure=struct)
    return out


def gradient_magnitude(img: np.ndarray) -> np.ndarray:
    gz = sobel(img, axis=0, mode="nearest")
    gy = sobel(img, axis=1, mode="nearest")
    gx = sobel(img, axis=2, mode="nearest")
    return np.sqrt(gz * gz + gy * gy + gx * gx)


def compute_rdna_rgrad(dna: np.ndarray,
                       foci_coords: np.ndarray,
                       cons_mask: np.ndarray) -> tuple[float, float]:
    """Eq 3 (Rdna) and Eq 4 (Rgrad)."""
    if len(foci_coords) == 0:
        return float("nan"), float("nan")

    in_mask = np.array([cons_mask[z, y, x] for z, y, x in foci_coords])
    foci_coords = foci_coords[in_mask]
    if len(foci_coords) == 0:
        return float("nan"), float("nan")

    grad = gradient_magnitude(dna)
    mean_dna_nuc = dna[cons_mask].mean()
    mean_grad_nuc = grad[cons_mask].mean()

    dna_at_foci = np.array([dna[z, y, x] for z, y, x in foci_coords])
    grad_at_foci = np.array([grad[z, y, x] for z, y, x in foci_coords])

    rdna = dna_at_foci.mean() / max(mean_dna_nuc, 1e-12)
    rgrad = grad_at_foci.mean() / max(mean_grad_nuc, 1e-12)
    return float(rdna), float(rgrad)


# --------------------------------------------------------------------------- #
# Reshuffling (Eq 1, 2)
# --------------------------------------------------------------------------- #

def reshuffle_foci_3d(dna: np.ndarray,
                      mask: np.ndarray,
                      n_foci: int,
                      rng: np.random.Generator) -> np.ndarray:
    """Place n_foci voxels with probability proportional to dna * mask."""
    rho = (dna * mask).ravel()
    rho = np.clip(rho, 0, None)
    total = rho.sum()
    if total <= 0 or n_foci <= 0:
        return np.zeros((0, 3), dtype=int)
    p = rho / total
    flat_idx = rng.choice(rho.size, size=n_foci, replace=False, p=p)
    return np.array(np.unravel_index(flat_idx, dna.shape)).T


def reshuffle_foci_track(dna: np.ndarray,
                         track: np.ndarray,
                         n_foci: int,
                         rng: np.random.Generator) -> np.ndarray:
    """Place n_foci voxels along the track (paper Eq 1, 2)."""
    coords = np.argwhere(track)
    if len(coords) == 0 or n_foci <= 0:
        return np.zeros((0, 3), dtype=int)
    rho = np.array([dna[z, y, x] for z, y, x in coords])
    rho = np.clip(rho, 0, None)
    total = rho.sum()
    if total <= 0:
        return np.zeros((0, 3), dtype=int)
    p = rho / total
    n_pick = min(n_foci, len(coords))
    idx = rng.choice(len(coords), size=n_pick, replace=False, p=p)
    return coords[idx]


# --------------------------------------------------------------------------- #
# Experiment drivers
# --------------------------------------------------------------------------- #

@dataclass
class LowLETResult:
    n_dsb: int
    n_prif: int
    rdna_prif: float
    rgrad_prif: float
    rdna_reshuffled: float
    rgrad_reshuffled: float


@dataclass
class HighLETResult:
    track_len_um: float
    n_dsb: int
    n_prif: int
    dsb_per_um: float
    prif_per_um: float
    rdna_prif: float
    rgrad_prif: float
    rdna_reshuffled: float
    rgrad_reshuffled: float


def run_low_let(rng: np.random.Generator, shape: tuple[int, int, int]) -> LowLETResult:
    mask = make_nucleus_mask(shape)
    dna = make_heterochromatin(shape, mask, rng)
    dsb = simulate_low_let_dsb(dna, mask, rng)

    prif_img = make_prif_image(dsb)
    prif_coords = detect_local_maxima(prif_img, mask)
    cons = conservative_mask(mask)

    rdna_p, rgrad_p = compute_rdna_rgrad(dna, prif_coords, cons)

    # Reshuffle: place the same number of foci via DNA-weighted Monte Carlo
    rsh = reshuffle_foci_3d(dna, cons, len(prif_coords), rng)
    rdna_r, rgrad_r = compute_rdna_rgrad(dna, rsh, cons)

    return LowLETResult(
        n_dsb=int(dsb.sum()),
        n_prif=int(len(prif_coords)),
        rdna_prif=rdna_p, rgrad_prif=rgrad_p,
        rdna_reshuffled=rdna_r, rgrad_reshuffled=rgrad_r,
    )


def run_high_let(rng: np.random.Generator, shape: tuple[int, int, int]) -> HighLETResult:
    mask = make_nucleus_mask(shape)
    dna = make_heterochromatin(shape, mask, rng)
    dsb, track = simulate_high_let_track(dna, mask, rng)

    track_len_um = int(track.sum()) * VOXEL_UM
    prif_img = make_prif_image(dsb)
    # restrict pRIF detection to the track strip + small radial widening
    from scipy.ndimage import binary_dilation
    track_strip = binary_dilation(track, iterations=2) & mask
    prif_coords_all = detect_local_maxima(prif_img, mask)
    if len(prif_coords_all) == 0:
        prif_coords = prif_coords_all
    else:
        keep = np.array([track_strip[z, y, x] for z, y, x in prif_coords_all])
        prif_coords = prif_coords_all[keep]

    cons = conservative_mask(mask)
    rdna_p, rgrad_p = compute_rdna_rgrad(dna, prif_coords, cons)

    rsh = reshuffle_foci_track(dna, track & cons, len(prif_coords), rng)
    rdna_r, rgrad_r = compute_rdna_rgrad(dna, rsh, cons)

    return HighLETResult(
        track_len_um=track_len_um,
        n_dsb=int(dsb.sum()),
        n_prif=int(len(prif_coords)),
        dsb_per_um=int(dsb.sum()) / max(track_len_um, 1e-12),
        prif_per_um=int(len(prif_coords)) / max(track_len_um, 1e-12),
        rdna_prif=rdna_p, rgrad_prif=rgrad_p,
        rdna_reshuffled=rdna_r, rgrad_reshuffled=rgrad_r,
    )


def aggregate(results: list, keys: list[str]) -> dict[str, dict[str, float]]:
    out = {}
    for k in keys:
        vals = np.array([getattr(r, k) for r in results], dtype=float)
        vals = vals[np.isfinite(vals)]
        out[k] = {
            "mean": float(vals.mean()),
            "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
            "n": int(len(vals)),
        }
    return out


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n-low", type=int, default=81)   # paper: 81 synthetic low-LET nuclei
    p.add_argument("--n-high", type=int, default=197) # paper: 197 synthetic Fe nuclei
    p.add_argument("--seed", type=int, default=20260621)
    p.add_argument("--out", default="../data/results.json")
    args = p.parse_args()

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.out))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    shape = (2 * NUCLEUS_RADIUS_VOX + 2,) * 3   # ~64^3
    rng = np.random.default_rng(args.seed)

    print(f"shape={shape}  voxel={VOXEL_UM} um  PSF sigma={PSF_SIGMA_UM} um")
    print(f"Running {args.n_low} low-LET nuclei...")
    low = [run_low_let(rng, shape) for _ in range(args.n_low)]
    print(f"Running {args.n_high} high-LET nuclei...")
    high = [run_high_let(rng, shape) for _ in range(args.n_high)]

    low_stats = aggregate(low, [
        "n_dsb", "n_prif",
        "rdna_prif", "rgrad_prif",
        "rdna_reshuffled", "rgrad_reshuffled",
    ])
    high_stats = aggregate(high, [
        "track_len_um", "n_dsb", "n_prif",
        "dsb_per_um", "prif_per_um",
        "rdna_prif", "rgrad_prif",
        "rdna_reshuffled", "rgrad_reshuffled",
    ])

    # Ratios R1/R2 (paper Table 2)
    def safe_ratios(results, num_key, den_key, min_den=0.05):
        vals = []
        for r in results:
            num = getattr(r, num_key)
            den = getattr(r, den_key)
            if not (np.isfinite(num) and np.isfinite(den)):
                continue
            if den < min_den:
                continue
            vals.append(num / den)
        return np.array(vals)

    r1_r2_dna = safe_ratios(high, "rdna_prif", "rdna_reshuffled")
    r1_r2_grad = safe_ratios(high, "rgrad_prif", "rgrad_reshuffled")
    high_stats["ratio_R1_R2_dna"] = {"mean": float(r1_r2_dna.mean()),
                                     "std": float(r1_r2_dna.std(ddof=1)),
                                     "n": int(len(r1_r2_dna))}
    high_stats["ratio_R1_R2_grad"] = {"mean": float(r1_r2_grad.mean()),
                                      "std": float(r1_r2_grad.std(ddof=1)),
                                      "n": int(len(r1_r2_grad))}

    low_r1_r2_dna = safe_ratios(low, "rdna_prif", "rdna_reshuffled")
    low_r1_r2_grad = safe_ratios(low, "rgrad_prif", "rgrad_reshuffled")
    low_stats["ratio_R1_R2_dna"] = {"mean": float(low_r1_r2_dna.mean()),
                                    "std": float(low_r1_r2_dna.std(ddof=1)),
                                    "n": int(len(low_r1_r2_dna))}
    low_stats["ratio_R1_R2_grad"] = {"mean": float(low_r1_r2_grad.mean()),
                                     "std": float(low_r1_r2_grad.std(ddof=1)),
                                     "n": int(len(low_r1_r2_grad))}

    payload = {
        "params": {
            "voxel_um": VOXEL_UM, "psf_sigma_um": PSF_SIGMA_UM,
            "nucleus_radius_um": NUCLEUS_RADIUS_UM,
            "target_dsb_low_let": TARGET_DSB_LOW_LET,
            "target_dsb_high_let_per_um": TARGET_DSB_HIGH_LET_PER_UM,
            "seed": args.seed,
        },
        "low_let": low_stats,
        "high_let": high_stats,
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nWrote {out_path}")
    print(json.dumps(payload, indent=2))
