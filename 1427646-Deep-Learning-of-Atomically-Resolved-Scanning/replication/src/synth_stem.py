"""
Synthetic STEM-like image generator for SrTiO3 / La0.7Sr0.3MnO3 [001] perovskite.

Produces images mimicking HAADF-STEM contrast (intensity ~ Z^1.7) with
pixel-wise class label maps for supervised FCN training.

Classes (6):
  0 = vacuum/background
  1 = Sr  (A-site in STO)
  2 = Ti  (B-site in STO; visually dimmer, no O co-lumns in simplified model)
  3 = La/Sr (A-site in LSMO; brighter than pure Sr)
  4 = Mn  (B-site in LSMO)
  5 = defect / vacancy marker (optional)

Design choices:
  - Perovskite ABO3 [001] projection: A and B sublattices form two interleaved
    square lattices offset by (a/2, a/2).
  - We build a heterostructure along the vertical axis: bottom half STO,
    top half LSMO, with a sharp or slightly diffuse interface.
  - Defects: A-site vacancy, B-site vacancy, A/A anti-site between STO and LSMO,
    B/B anti-site (Ti<->Mn).
  - Intensity: Gaussian blob per atomic column with amplitude ~ Z^1.7 weighted.
    Poisson noise + scan-line jitter simulate experimental conditions.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Tuple

# Atomic numbers and HAADF-like weights (~Z^1.7 for dominant element of column).
# For mixed column (La0.7Sr0.3) use weighted average.
Z_SR = 38
Z_TI = 22
Z_LA = 57
Z_MN = 25
Z_O  = 8

def z17(z: float) -> float:
    return z ** 1.7

# Column intensities (arbitrary units, will be normalized).
I_SR = z17(Z_SR)                          # ~pure Sr
I_TI = z17(Z_TI)                          # Ti (ignore O cols for simplicity)
I_LASR = 0.7 * z17(Z_LA) + 0.3 * z17(Z_SR)
I_MN = z17(Z_MN)

CLASS_NAMES = ["vacuum", "Sr", "Ti", "LaSr", "Mn", "defect"]
NUM_CLASSES = len(CLASS_NAMES)

@dataclass
class SimConfig:
    img_size: int = 256
    a_px: float = 20.0          # pixels per perovskite a (~3.9 Å). 20 px -> ~0.2 Å/px.
    sigma_px: float = 3.2       # Gaussian blob sigma per column
    label_sigma_px: float = 2.0 # Gaussian label footprint
    noise_level: float = 0.06   # Poisson-equivalent + gauss
    jitter_px: float = 0.4      # scan-line y-jitter amplitude
    defect_prob_vac: float = 0.02
    defect_prob_anti: float = 0.02
    interface_frac: float = 0.5 # y-fraction where STO ends, LSMO begins
    interface_diffuse_uc: float = 0.5  # diffuseness (in unit cells)
    rot_deg: float = 0.0        # optional global rotation


def _gauss_stamp(size: int, sigma: float) -> np.ndarray:
    r = size // 2
    y, x = np.mgrid[-r:r+1, -r:r+1]
    g = np.exp(-(x*x + y*y) / (2 * sigma * sigma))
    return g.astype(np.float32)


def build_columns(cfg: SimConfig, rng: np.random.Generator):
    """Return (cols, labels) where cols is list of (xc,yc,intensity,cls,is_defect)."""
    H = W = cfg.img_size
    a = cfg.a_px

    # A sublattice at integer a positions; B sublattice offset by (a/2, a/2).
    n_a = int(np.ceil(W / a)) + 2
    n_b = int(np.ceil(H / a)) + 2

    cols = []
    interface_y = cfg.interface_frac * H

    def in_lsmo(y: float) -> bool:
        # Diffuse interface: probability grows smoothly across interface
        w = cfg.interface_diffuse_uc * a
        if w <= 1e-6:
            return y < interface_y  # image y grows downward; top = LSMO
        p = 0.5 * (1 - np.tanh((y - interface_y) / w))
        return rng.random() < p

    # A-site (integer grid shifted by a/2 to center): positions (i*a, j*a) + offset
    off = a * 0.5
    for j in range(-1, n_b + 1):
        for i in range(-1, n_a + 1):
            xa, ya = i * a + off, j * a + off
            if -a < xa < W + a and -a < ya < H + a:
                is_lsmo = in_lsmo(ya)
                if is_lsmo:
                    I0, cls = I_LASR, 3
                else:
                    I0, cls = I_SR, 1
                # Defects on A-site
                r = rng.random()
                is_def = False
                if r < cfg.defect_prob_vac:
                    continue  # vacancy: column absent
                elif r < cfg.defect_prob_vac + cfg.defect_prob_anti:
                    # Anti-site: swap STO <-> LSMO A cation locally
                    if is_lsmo:
                        I0, cls = I_SR, 1
                    else:
                        I0, cls = I_LASR, 3
                    is_def = True
                # Random small intensity jitter
                Ij = I0 * rng.normal(1.0, 0.05)
                cols.append((xa, ya, Ij, cls, is_def))

    # B-site: positions (i*a + a, j*a + a), i.e. same grid without offset
    for j in range(-1, n_b + 1):
        for i in range(-1, n_a + 1):
            xb, yb = i * a, j * a
            if -a < xb < W + a and -a < yb < H + a:
                is_lsmo = in_lsmo(yb)
                if is_lsmo:
                    I0, cls = I_MN, 4
                else:
                    I0, cls = I_TI, 2
                r = rng.random()
                is_def = False
                if r < cfg.defect_prob_vac:
                    continue
                elif r < cfg.defect_prob_vac + cfg.defect_prob_anti:
                    # Ti<->Mn antisite
                    if is_lsmo:
                        I0, cls = I_TI, 2
                    else:
                        I0, cls = I_MN, 4
                    is_def = True
                Ij = I0 * rng.normal(1.0, 0.05)
                cols.append((xb, yb, Ij, cls, is_def))

    return cols


def render(cfg: SimConfig, rng: np.random.Generator):
    H = W = cfg.img_size
    img = np.zeros((H, W), dtype=np.float32)
    lbl = np.zeros((H, W), dtype=np.int64)  # 0 = vacuum default
    score = np.zeros((NUM_CLASSES, H, W), dtype=np.float32)

    cols = build_columns(cfg, rng)

    # Normalize intensities to ~[0, 1] before adding
    Is = np.array([c[2] for c in cols], dtype=np.float32)
    Inorm = Is / (Is.max() + 1e-6)

    # stamp sizes
    stamp_r = int(np.ceil(3.5 * cfg.sigma_px))
    stamp = _gauss_stamp(stamp_r * 2 + 1, cfg.sigma_px)
    lstamp_r = int(np.ceil(3.0 * cfg.label_sigma_px))
    lstamp = _gauss_stamp(lstamp_r * 2 + 1, cfg.label_sigma_px)

    for (xc, yc, _, cls, is_def), Inrm in zip(cols, Inorm):
        ix = int(round(xc)); iy = int(round(yc))
        # image blob
        x0 = ix - stamp_r; x1 = ix + stamp_r + 1
        y0 = iy - stamp_r; y1 = iy + stamp_r + 1
        sx0 = max(0, -x0); sy0 = max(0, -y0)
        ex0 = max(0, x0); ey0 = max(0, y0)
        ex1 = min(W, x1); ey1 = min(H, y1)
        if ex1 > ex0 and ey1 > ey0:
            img[ey0:ey1, ex0:ex1] += Inrm * stamp[sy0:sy0 + (ey1-ey0), sx0:sx0 + (ex1-ex0)]

        # label score (argmax later)
        x0 = ix - lstamp_r; x1 = ix + lstamp_r + 1
        y0 = iy - lstamp_r; y1 = iy + lstamp_r + 1
        sx0 = max(0, -x0); sy0 = max(0, -y0)
        ex0 = max(0, x0); ey0 = max(0, y0)
        ex1 = min(W, x1); ey1 = min(H, y1)
        if ex1 > ex0 and ey1 > ey0:
            score[cls, ey0:ey1, ex0:ex1] = np.maximum(
                score[cls, ey0:ey1, ex0:ex1],
                lstamp[sy0:sy0 + (ey1-ey0), sx0:sx0 + (ex1-ex0)],
            )
            if is_def:
                # also mark as defect class channel (weaker)
                score[5, ey0:ey1, ex0:ex1] = np.maximum(
                    score[5, ey0:ey1, ex0:ex1],
                    0.9 * lstamp[sy0:sy0 + (ey1-ey0), sx0:sx0 + (ex1-ex0)],
                )

    # Scan-line y-jitter: per-row small horizontal shift
    if cfg.jitter_px > 0:
        shifts = rng.normal(0, cfg.jitter_px, size=H)
        out = np.zeros_like(img)
        for y in range(H):
            s = shifts[y]
            f = int(np.floor(s)); frac = s - f
            cols_idx = np.arange(W)
            src = cols_idx - f
            out[y] = (1 - frac) * np.take(img[y], src, mode='wrap') + \
                     frac * np.take(img[y], src - 1, mode='wrap')
        img = out

    # Gaussian background + Poisson-like noise
    img = np.clip(img, 0, None)
    # scale up for poisson
    peak_counts = 400.0
    noisy = rng.poisson(img * peak_counts) / peak_counts
    noisy = noisy + rng.normal(0, cfg.noise_level, size=img.shape)
    noisy = noisy.astype(np.float32)

    # Labels: argmax over score channels; vacuum where all scores near zero
    # Set vacuum channel to small baseline so that low-score pixels are vacuum.
    score[0] = 0.05
    label = np.argmax(score, axis=0).astype(np.int64)

    # Normalize image to [0,1]
    lo, hi = np.percentile(noisy, [1, 99])
    noisy = np.clip((noisy - lo) / (hi - lo + 1e-6), 0, 1).astype(np.float32)

    return noisy, label


def generate_dataset(n: int, cfg: SimConfig | None = None, seed: int = 0):
    if cfg is None:
        cfg = SimConfig()
    rng = np.random.default_rng(seed)
    X = np.empty((n, 1, cfg.img_size, cfg.img_size), dtype=np.float32)
    Y = np.empty((n, cfg.img_size, cfg.img_size), dtype=np.int64)
    for i in range(n):
        # Randomize some params per sample
        c = SimConfig(
            img_size=cfg.img_size,
            a_px=cfg.a_px * rng.uniform(0.95, 1.05),
            sigma_px=cfg.sigma_px * rng.uniform(0.9, 1.15),
            label_sigma_px=cfg.label_sigma_px,
            noise_level=cfg.noise_level * rng.uniform(0.6, 1.4),
            jitter_px=cfg.jitter_px * rng.uniform(0.5, 1.5),
            defect_prob_vac=cfg.defect_prob_vac,
            defect_prob_anti=cfg.defect_prob_anti,
            interface_frac=rng.uniform(0.35, 0.65),
            interface_diffuse_uc=rng.uniform(0.0, 1.5),
        )
        img, lbl = render(c, rng)
        X[i, 0] = img
        Y[i] = lbl
    return X, Y


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    X, Y = generate_dataset(4, seed=42)
    fig, ax = plt.subplots(2, 4, figsize=(12, 6))
    for i in range(4):
        ax[0, i].imshow(X[i, 0], cmap="gray")
        ax[0, i].set_title(f"synthetic STEM #{i}")
        ax[0, i].axis("off")
        ax[1, i].imshow(Y[i], cmap="tab10", vmin=0, vmax=9)
        ax[1, i].set_title("ground-truth labels")
        ax[1, i].axis("off")
    plt.tight_layout()
    plt.savefig("sample_data.png", dpi=120)
    print("wrote sample_data.png; shapes:", X.shape, Y.shape)
