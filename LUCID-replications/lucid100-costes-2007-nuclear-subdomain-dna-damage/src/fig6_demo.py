"""
Reproduce Figure 6 of Costes et al. 2007: demonstrate that
  * Rdna > 1, Rgrad < 1 when foci are in bright (dense DNA) interior
  * Rdna ~ 1, Rgrad > 1 when foci are at the bright/dim interface
  * Rdna < 1, Rgrad ~ low when foci are in dim regions

We construct a single 2-D synthetic nucleus slice (so the figure is human-
readable) with one bright DAPI blob, hand-place three foci patterns, and
compute Rdna/Rgrad on each.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, sobel, binary_erosion

VOXEL_UM = 0.16
SHAPE = (140, 140)


def make_slice() -> tuple[np.ndarray, np.ndarray]:
    ny, nx = SHAPE
    yy, xx = np.indices(SHAPE)
    cy, cx = ny // 2, nx // 2
    nucleus_radius = 55
    mask = (yy - cy) ** 2 + (xx - cx) ** 2 <= nucleus_radius ** 2

    dna = np.zeros(SHAPE, dtype=np.float32)
    # baseline euchromatin in the whole nucleus
    dna[mask] = 0.5
    # one bright heterochromatin blob, off-center
    by, bx, br = cy - 12, cx - 6, 22
    blob = ((yy - by) ** 2 + (xx - bx) ** 2) <= br ** 2
    dna[blob & mask] += 1.5
    # smaller blob
    by2, bx2, br2 = cy + 18, cx + 14, 12
    blob2 = ((yy - by2) ** 2 + (xx - bx2) ** 2) <= br2 ** 2
    dna[blob2 & mask] += 1.2

    dna = gaussian_filter(dna, sigma=2.0)
    dna[~mask] = 0.0
    return dna, mask


def gradient_magnitude(img: np.ndarray) -> np.ndarray:
    gy = sobel(img, axis=0, mode="nearest")
    gx = sobel(img, axis=1, mode="nearest")
    return np.sqrt(gy * gy + gx * gx)


def conservative(mask, n=3):
    out = mask.copy()
    for _ in range(n):
        out = binary_erosion(out)
    return out


def compute_rdna_rgrad(dna, foci_yx, cons_mask):
    grad = gradient_magnitude(dna)
    mean_dna = dna[cons_mask].mean()
    mean_grad = grad[cons_mask].mean()
    dna_at = np.array([dna[y, x] for y, x in foci_yx])
    grad_at = np.array([grad[y, x] for y, x in foci_yx])
    return float(dna_at.mean() / mean_dna), float(grad_at.mean() / mean_grad)


def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../figures"))
    os.makedirs(out_dir, exist_ok=True)

    dna, mask = make_slice()
    cons = conservative(mask, n=3)
    grad = gradient_magnitude(dna)

    # Three foci patterns
    # Pattern A: deep in bright blob -> Rdna > 1, Rgrad < 1
    foci_A = [(58, 58), (60, 62), (55, 56), (62, 58), (57, 60)]
    # Pattern C: at the interface (bright edge) -> Rdna ~ 1, Rgrad > 1
    # The blob center is (cy-12, cx-6) = (58, 64) with radius 22.
    # Edge of that blob in original coords (pre-blur) is at radius ~ 22 from (58, 64).
    cy_blob, cx_blob, r_blob = 58, 64, 22
    angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    foci_C = [(int(cy_blob + r_blob * np.sin(a)),
               int(cx_blob + r_blob * np.cos(a))) for a in angles]
    foci_C = [(y, x) for y, x in foci_C if cons[y, x]]
    # Pattern E: in dim regions -> Rdna < 1, Rgrad low
    foci_E = [(30, 30), (32, 100), (100, 30), (105, 105), (110, 70)]
    foci_E = [(y, x) for y, x in foci_E if cons[y, x]]

    patterns = [("A: in bright (heterochromatin)", foci_A),
                ("C: at interface", foci_C),
                ("E: in dim (euchromatin)", foci_E)]

    fig, axes = plt.subplots(2, 3, figsize=(13, 8.5))
    results = []
    for col, (label, foci) in enumerate(patterns):
        rdna, rgrad = compute_rdna_rgrad(dna, foci, cons)
        results.append((label, rdna, rgrad))

        # Row 0: DAPI + foci
        ax = axes[0, col]
        ax.imshow(dna, cmap="Blues")
        ys, xs = zip(*foci)
        ax.scatter(xs, ys, c="red", s=60, marker="o", edgecolors="white")
        # show conservative mask boundary
        ax.contour(cons, levels=[0.5], colors="cyan", linewidths=0.6)
        ax.set_title(f"{label}\nRdna={rdna:.2f}  Rgrad={rgrad:.2f}")
        ax.axis("off")

        # Row 1: gradient + foci
        ax2 = axes[1, col]
        ax2.imshow(grad, cmap="Greens")
        ax2.scatter(xs, ys, c="red", s=60, marker="o", edgecolors="white")
        ax2.contour(cons, levels=[0.5], colors="cyan", linewidths=0.6)
        ax2.set_title("DAPI gradient")
        ax2.axis("off")

    fig.suptitle("Figure 6 replication — Rdna / Rgrad on three hand-placed foci patterns",
                 fontsize=13)
    fig.tight_layout()
    out_path = os.path.join(out_dir, "fig6_replication.png")
    fig.savefig(out_path, dpi=140)
    print(f"Saved {out_path}")
    for label, rdna, rgrad in results:
        print(f"  {label}: Rdna={rdna:.3f}  Rgrad={rgrad:.3f}")


if __name__ == "__main__":
    main()
