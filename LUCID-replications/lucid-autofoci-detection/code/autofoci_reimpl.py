"""
Python reimplementation of the AutoFoci object-evaluation pipeline
(Lengert et al., Sci Rep 8:17282, 2018; DOI 10.1038/s41598-018-35660-5).

Implements equations 1-4 from the paper exactly as specified, plus the
intermediate scoring steps used in Fig. 2c/d:

  (1) compactness  C = 1 / sum_i r_i^2 * I_i   (inverse moment of inertia,
      intensity-weighted, computed in a disk of radius 3 around the
      intensity-weighted centroid in the original image)
  (2) OEP_{red/green} = (I_TH / I_nucl) * I_LC * C
        I_TH = mean of 3 brightest pixels within the object in the
               top-hat-transformed image
        I_LC = mean of 3 brightest pixels within the object in the LoG-
               transformed image
        I_nucl = mean intensity of the nucleus (this channel)
  (3) w = ISTD_red / ISTD_green, computed per cell
  (4) OEP = OEP_red^w * OEP_green^(1/w)

Intermediate scores reported in the paper:
  - mean object intensity (panels i, ii)
  - top-hat 3 brightest pixels per channel (panels iii, iv)
  - LoG 3 brightest pixels per channel (panels v, vi)
  - per-channel OEP via equation (2) (panels vii, viii)
  - combined OEP via equation (4) (panel ix)

Implementation choices that follow the published Java source
(github.com/nleng/AutoFoci, ObjectFinder.java):
  - LoG kernel is the exact 5x5 matrix given in Materials & Methods.
  - Top-hat = morphological opening with a disk structuring element of
    radius = struct_element_diameter/2 = 5 px.
  - Object growing: 4-connected flood fill bounded by
        eThresh = 0.5 * I_max (area-growing rule from paper)
        max distance from local max = maxArea_radius (2 * minSeparation = 6 px)
  - "3 brightest pixels" = top 3 pixel values inside the grown object
    region, averaged (matching getMean_without0 in ObjectFinder.java).
  - Nucleus mask = DAPI (blue) channel above a threshold; nucleus mean
    is per-channel mean intensity inside the mask.
  - Moment of inertia: intensity-weighted centroid -> radius-3 disk
    around it; pixels outside the nucleus mask use the nucleus mean
    (matches ObjectFinder.java lines 970+).
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
import tifffile
from scipy import ndimage as ndi
from scipy.signal import convolve2d
from scipy.stats import spearmanr
from skimage.morphology import disk, opening as morph_opening
from skimage.filters import threshold_otsu

# ---------------------------------------------------------------------------
# Constants from the paper (Materials & Methods, User-defined parameters)
# ---------------------------------------------------------------------------
LOG_KERNEL = np.array([
    [-2, -4, -4, -4, -2],
    [-4,  0, 10,  0, -4],
    [-4, 10, 32, 10, -4],
    [-4,  0, 10,  0, -4],
    [-2, -4, -4, -4, -2],
], dtype=np.float32)

STRUCT_ELEMENT_DIAMETER = 10        # px (paper: "set to 10 pixels")
TOPHAT_RADIUS = STRUCT_ELEMENT_DIAMETER // 2  # 5

LOCAL_MAX_RADIUS = 3                # px
MIN_AREA = 3                        # px (also = number of top pixels averaged)
MIN_REL_INTENSITY = 1.1             # pixel must be >= 1.1 * cell mean

# minSeparation default = 3 -> maxArea_radius = 6 in the Java source
MIN_SEPARATION = 3
MAX_AREA_RADIUS = 2 * MIN_SEPARATION  # 6

INERTIA_RADIUS = 3                  # px (hard-coded in ObjectFinder.java)

# Channel convention for the AutoFoci test images:
# R = 53BP1 ("red"), G = gammaH2AX ("green"), B = DAPI
CH_RED = 0
CH_GREEN = 1
CH_DAPI = 2

# ---------------------------------------------------------------------------

@dataclass
class ObjectFeatures:
    image: str
    obj_x: int
    obj_y: int
    cell_number: int
    # raw means in nucleus
    Inucl_red: float
    Inucl_green: float
    ISTD_red: float
    ISTD_green: float
    # weighting factor
    w: float
    # mean object intensity (panels i, ii)
    mean_int_red: float
    mean_int_green: float
    # top-hat 3 brightest (panels iii, iv)
    ITH_red: float
    ITH_green: float
    # LoG 3 brightest (panels v, vi)
    ILC_red: float
    ILC_green: float
    # compactness (eq. 1)
    C_red: float
    C_green: float
    # per-channel OEP (eq. 2; panels vii, viii)
    OEP_red: float
    OEP_green: float
    # combined OEP (eq. 4; panel ix)
    OEP: float
    # object footprint size for diagnostics
    n_obj_pixels: int


def make_nucleus_mask(dapi: np.ndarray) -> np.ndarray:
    """Build a binary nucleus mask from the DAPI channel.

    For these 120x120 single-cell images, the DAPI signal is strong
    inside the nucleus and ~0 outside. A simple Otsu threshold with a
    small floor produces a clean nucleus mask.
    """
    d = dapi.astype(np.float32)
    if d.max() <= 1:
        return np.zeros_like(d, dtype=bool)
    try:
        t = threshold_otsu(d[d > 0])
    except Exception:
        t = d.mean()
    t = max(t, 5)  # floor: ignore essentially-zero pixels
    mask = d >= t
    # Take the largest connected component (the nucleus itself)
    lbl, n = ndi.label(mask)
    if n == 0:
        return mask
    sizes = ndi.sum(mask, lbl, index=np.arange(1, n + 1))
    keep = np.argmax(sizes) + 1
    mask = lbl == keep
    # Small closing to fill DAPI gaps
    mask = ndi.binary_closing(mask, structure=np.ones((3, 3)), iterations=2)
    return mask


def top_hat(img: np.ndarray, radius: int = TOPHAT_RADIUS) -> np.ndarray:
    """Morphological white top-hat = img - opening(img, disk(radius)).

    Matches AutoFoci's ImageJ "morphological_opening" + "Subtract create".
    """
    se = disk(radius)
    opened = morph_opening(img, se)
    return img.astype(np.float32) - opened.astype(np.float32)


def log_transform(img: np.ndarray) -> np.ndarray:
    """Apply the published 5x5 LoG kernel via 2D convolution."""
    return convolve2d(img.astype(np.float32), LOG_KERNEL, mode="same",
                      boundary="symm")


def find_local_max_near(img: np.ndarray, x: int, y: int,
                        search_radius: int = 4) -> tuple[int, int]:
    """Return (x_max, y_max) inside a small window around (x,y) where the
    value is highest. Handles small mismatches between the recorded
    object position and the actual local maximum."""
    H, W = img.shape
    x0 = max(0, x - search_radius); x1 = min(W, x + search_radius + 1)
    y0 = max(0, y - search_radius); y1 = min(H, y + search_radius + 1)
    sub = img[y0:y1, x0:x1]
    j, i = np.unravel_index(np.argmax(sub), sub.shape)
    return x0 + i, y0 + j


def grow_object(img: np.ndarray, x: int, y: int,
                cell_mean: float,
                max_radius: int = MAX_AREA_RADIUS,
                min_rel_intensity: float = MIN_REL_INTENSITY,
                ) -> np.ndarray:
    """Region-grow (4-connected) from (x, y).

    Reproduces ObjectFinder.grower():
      - eThresh = 0.5 * I_max  (area-growing rule from paper)
      - Pixel must be < I_max (i.e., maxThresh) and >= eThresh
      - Pixel must be within max_radius (Euclidean) of the local max
      - Pixel must be >= min_rel_intensity * cell_mean
    Returns a boolean mask of object pixels (always >= 1 pixel: the seed).
    """
    H, W = img.shape
    I_max = int(img[y, x])
    eThresh = 0.5 * I_max
    abs_thresh = max(eThresh, min_rel_intensity * cell_mean)
    visited = np.zeros((H, W), dtype=bool)
    obj = np.zeros((H, W), dtype=bool)
    obj[y, x] = True
    visited[y, x] = True
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            if visited[ny, nx]:
                continue
            visited[ny, nx] = True
            r2 = (nx - x) ** 2 + (ny - y) ** 2
            if r2 > max_radius * max_radius:
                continue
            v = img[ny, nx]
            if v < abs_thresh:
                continue
            if v > I_max:
                continue
            obj[ny, nx] = True
            stack.append((nx, ny))
    return obj


def mean_top_n(values: np.ndarray, n: int = MIN_AREA) -> float:
    """Mean of the top n values (sorted descending). If fewer than n values
    are available, use what's there."""
    if values.size == 0:
        return 0.0
    if values.size <= n:
        return float(values.mean())
    return float(np.sort(values)[-n:].mean())


def compactness(obj_mask: np.ndarray, intensity_img: np.ndarray,
                nucleus_mask: np.ndarray, channel_mean: float,
                radius: int = INERTIA_RADIUS) -> float:
    """Compactness = 1 / moment_of_inertia where mass = intensity.

    Procedure (matches ObjectFinder.java lines 972-1010):
      1. Compute intensity-weighted centroid (cx, cy) using obj_mask
         pixels in the *original* image.
      2. Sum I_i * r_i^2 over a disk of radius=3 around (cx, cy) in the
         original image.
      3. Pixels outside the nucleus mask are replaced with the channel's
         per-nucleus mean intensity to avoid edge artefacts.
      4. moment_of_inertia /= total_intensity in that disk.
      5. return 1 / moment_of_inertia (cap if denom is ~0).
    """
    H, W = intensity_img.shape
    ys, xs = np.nonzero(obj_mask)
    if ys.size == 0:
        return 0.0
    I = intensity_img[ys, xs].astype(np.float64)
    if I.sum() == 0:
        return 0.0
    cx = float((xs * I).sum() / I.sum())
    cy = float((ys * I).sum() / I.sum())
    icx = int(round(cx)); icy = int(round(cy))
    if not (radius <= icx < W - radius and radius <= icy < H - radius):
        # paper/java fallback when too close to edge: large moment -> small C
        return 1.0 / 30.0

    moi = 0.0
    tot = 0.0
    for i in range(icx - radius, icx + radius + 1):
        for j in range(icy - radius, icy + radius + 1):
            if (i - icx) ** 2 + (j - icy) ** 2 > radius ** 2:
                continue
            if nucleus_mask[j, i]:
                inten = float(intensity_img[j, i])
            else:
                inten = float(channel_mean)
            r2 = (cx - i) ** 2 + (cy - j) ** 2
            moi += r2 * inten
            tot += inten
    if tot <= 0:
        return 0.0
    moi /= tot
    if moi <= 0:
        return 0.0
    return 1.0 / moi


def compute_features_for_object(img: np.ndarray, x: int, y: int,
                                cell_number: int, name: str) -> ObjectFeatures:
    """Compute all features for a single object at recorded (x, y)."""
    red = img[..., CH_RED].astype(np.float32)
    grn = img[..., CH_GREEN].astype(np.float32)
    dap = img[..., CH_DAPI].astype(np.float32)

    nucl_mask = make_nucleus_mask(dap)
    if nucl_mask.sum() == 0:
        # Fall back: whole image (rare for these test crops)
        nucl_mask = np.ones_like(dap, dtype=bool)

    Inucl_red = float(red[nucl_mask].mean())
    Inucl_grn = float(grn[nucl_mask].mean())
    ISTD_red = float(red[nucl_mask].std(ddof=0))
    ISTD_grn = float(grn[nucl_mask].std(ddof=0))

    # Weighting factor w = ISTD_red / ISTD_green
    w = ISTD_red / ISTD_grn if ISTD_grn > 0 else 1.0

    # Transformations
    red_TH = top_hat(red)
    grn_TH = top_hat(grn)
    red_LC = log_transform(red)
    grn_LC = log_transform(grn)

    # Refine to local maximum near recorded (X,Y) in the original 53BP1
    # channel (paper: "An algorithm detects objects in the red channel
    # with the 53BP1 signal by the identification of local maxima").
    x_lm, y_lm = find_local_max_near(red, x, y, search_radius=4)

    # Grow the object on the original red channel (matches Java default
    # `use_tophat_for_search = false`).
    obj_mask = grow_object(red, x_lm, y_lm, cell_mean=Inucl_red,
                           max_radius=MAX_AREA_RADIUS,
                           min_rel_intensity=MIN_REL_INTENSITY)
    n_obj_pixels = int(obj_mask.sum())

    obj_red = red[obj_mask]
    obj_grn = grn[obj_mask]
    obj_red_TH = red_TH[obj_mask]
    obj_grn_TH = grn_TH[obj_mask]
    obj_red_LC = red_LC[obj_mask]
    obj_grn_LC = grn_LC[obj_mask]

    mean_int_red = float(obj_red.mean()) if obj_red.size else 0.0
    mean_int_grn = float(obj_grn.mean()) if obj_grn.size else 0.0
    ITH_red = max(mean_top_n(obj_red_TH), 1.0)
    ITH_grn = max(mean_top_n(obj_grn_TH), 1.0)
    ILC_red = max(mean_top_n(obj_red_LC), 1.0)
    ILC_grn = max(mean_top_n(obj_grn_LC), 1.0)

    C_red = compactness(obj_mask, red, nucl_mask, Inucl_red)
    C_grn = compactness(obj_mask, grn, nucl_mask, Inucl_grn)

    # Equation (2)
    OEP_red = (ITH_red / max(Inucl_red, 1e-3)) * ILC_red * C_red
    OEP_grn = (ITH_grn / max(Inucl_grn, 1e-3)) * ILC_grn * C_grn

    # Equation (4)
    # Guard against negative bases or zeros for the power operation.
    OEP_red_safe = max(OEP_red, 1e-9)
    OEP_grn_safe = max(OEP_grn, 1e-9)
    OEP = (OEP_red_safe ** w) * (OEP_grn_safe ** (1.0 / w))

    return ObjectFeatures(
        image=name, obj_x=x, obj_y=y, cell_number=cell_number,
        Inucl_red=Inucl_red, Inucl_green=Inucl_grn,
        ISTD_red=ISTD_red, ISTD_green=ISTD_grn, w=w,
        mean_int_red=mean_int_red, mean_int_green=mean_int_grn,
        ITH_red=ITH_red, ITH_green=ITH_grn,
        ILC_red=ILC_red, ILC_green=ILC_grn,
        C_red=C_red, C_green=C_grn,
        OEP_red=OEP_red, OEP_green=OEP_grn, OEP=OEP,
        n_obj_pixels=n_obj_pixels,
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main(ratings_xlsx: str, test_image_dir: str, out_csv: str) -> None:
    df = pd.read_excel(ratings_xlsx, sheet_name="Tabelle1", header=2)
    df = df.dropna(subset=["ImageName"]).copy()
    df["Experimenter 1"] = df["Experimenter 1"].astype(float)
    df["Experimenter 2"] = df["Experimenter 2"].astype(float)
    df["Experimenter 3"] = df["Experimenter 3"].astype(float)
    df["avg"] = df[["Experimenter 1", "Experimenter 2",
                    "Experimenter 3"]].mean(axis=1)

    feats: list[dict] = []
    for i, row in df.iterrows():
        name = row["ImageName"]
        path = os.path.join(test_image_dir, name)
        if not os.path.exists(path):
            continue
        img = tifffile.imread(path)
        # Some single-cell tiffs may be (3,H,W) instead of (H,W,3).
        if img.ndim == 3 and img.shape[0] == 3:
            img = np.transpose(img, (1, 2, 0))
        if img.ndim == 2:
            # Replicate single channel into RGB
            img = np.stack([img, img, np.zeros_like(img)], axis=-1)
        x = int(row["Object position X"])
        y = int(row["Object position Y"])
        try:
            f = compute_features_for_object(
                img, x, y, int(row["CellNumber"]), name)
        except Exception as exc:
            print(f"  ! {name} ({x},{y}): {exc}", file=sys.stderr)
            continue
        d = vars(f).copy()
        d["ObjectCounter"] = int(row["ObjectCounter"])
        d["rating_1"] = row["Experimenter 1"]
        d["rating_2"] = row["Experimenter 2"]
        d["rating_3"] = row["Experimenter 3"]
        d["rating_avg"] = row["avg"]
        feats.append(d)
        if (i + 1) % 50 == 0:
            print(f"  processed {i + 1}/{len(df)}", file=sys.stderr)

    out = pd.DataFrame(feats)
    out.to_csv(out_csv, index=False)
    print(f"wrote {len(out)} rows -> {out_csv}", file=sys.stderr)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ratings", required=True)
    p.add_argument("--images", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    main(args.ratings, args.images, args.out)
