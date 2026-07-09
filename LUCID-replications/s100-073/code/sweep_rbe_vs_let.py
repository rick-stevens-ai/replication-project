"""
Sweep MM model RBEs vs LET_t and write CSV + plot.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mm_model import (
    rbe_residual, rbe_misrepair, rbe_residual_and_misrepair,
    yield_residual_proton, yield_misrepair_proton,
    GAMMA_R, GAMMA_M,
)

OUT_CSV = os.path.join(os.path.dirname(__file__), "..", "evidence", "rbe_vs_let.csv")
OUT_PNG = os.path.join(os.path.dirname(__file__), "..", "figures", "rbe_vs_let.png")

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)

D = 1.8  # Gy per fraction (paper's prescription)

let_grid = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0]
rows = []
for L in let_grid:
    rr = rbe_residual(L)
    rm = rbe_misrepair(L)
    rrm = rbe_residual_and_misrepair(L)
    yr = yield_residual_proton(D, L)
    ym = yield_misrepair_proton(D, L)
    rows.append({
        "LET_t_keV_per_um": L,
        "RBE_r": rr,
        "RBE_m": rm,
        "RBE_rm": rrm,
        "yield_residual_per_cell_at_1.8Gy": yr,
        "yield_misrepair_per_cell_at_1.8Gy": ym,
        "residual_over_misrepair": yr / ym if ym > 0 else float("inf"),
    })

with open(OUT_CSV, "w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {OUT_CSV}")
print()
print(f"{'LET_t':>7} {'RBE_r':>8} {'RBE_m':>9} {'RBE_r&m':>9} {'Y_r':>8} {'Y_m':>8} {'Y_r/Y_m':>9}")
for r in rows:
    print(f"{r['LET_t_keV_per_um']:7.2f} {r['RBE_r']:8.4f} {r['RBE_m']:9.4f} "
          f"{r['RBE_rm']:9.4f} {r['yield_residual_per_cell_at_1.8Gy']:8.3f} "
          f"{r['yield_misrepair_per_cell_at_1.8Gy']:8.4f} {r['residual_over_misrepair']:9.2f}")

# Plot if matplotlib available
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Ls = [r["LET_t_keV_per_um"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))

    ax[0].plot(Ls, [r["RBE_r"] for r in rows], "g-o", label="RBE_r (residual)")
    ax[0].plot(Ls, [r["RBE_rm"] for r in rows], "b-s", label="RBE_r&m (combined)")
    ax[0].axhline(1.1, color="k", linestyle="--", alpha=0.5, label="Constant RBE=1.1")
    ax[0].set_xlabel("LET_t (keV/um)")
    ax[0].set_ylabel("RBE")
    ax[0].set_title("MM model: residual & combined RBE vs LET_t  (D=1.8 Gy)")
    ax[0].legend(loc="best")
    ax[0].grid(True, alpha=0.3)

    ax[1].plot(Ls, [r["RBE_m"] for r in rows], "r-^", label="RBE_m (misrepair)")
    ax[1].set_xlabel("LET_t (keV/um)")
    ax[1].set_ylabel("RBE_m")
    ax[1].set_title("MM model: misrepair RBE vs LET_t  (D=1.8 Gy)\n(huge magnitude due to small gamma_m)")
    ax[1].grid(True, alpha=0.3)
    ax[1].legend(loc="best")

    fig.suptitle("Smith et al. 2019 (s100-073) — independent replication of Eqs. 6,7,8")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=130)
    print(f"\nWrote {OUT_PNG}")
except ImportError:
    print("matplotlib not available; skipping plot")
