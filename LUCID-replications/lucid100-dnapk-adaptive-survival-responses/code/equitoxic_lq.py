#!/usr/bin/env python3
"""
Equitoxic-dose audit for Odegaard, Yang & Boothman (1998) Table 1.

The paper states the high-dose challenges were chosen to be EQUITOXIC:
  - SCID  (DNA-PKcs-) : 250 cGy  -> 9  +/- 1  % survival
  - CB-17 (DNA-PKcs+) : 500 cGy  -> 12 +/- 5  % survival

This little script:
  1. Confirms the equitoxic claim quantitatively (point + 1-sigma overlap test).
  2. Derives the radiosensitivity-ratio (dose modifying factor, DMF) implied
     by the dose pair: SCID is more sensitive by ~2x at equal survival.
  3. Under a simple log-linear approximation S = exp(-alpha*D), back-solves
     alpha for each cell line from the single (D, S) point and compares.
     (This is an interpretive minimum; the paper does NOT publish full
      survival curves, so a true LQ/alpha-beta fit is impossible.)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "results" / "equitoxic_lq.tsv"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Paper's challenge dose / survival pairs (Table 1, row "Challenged").
points = [
    # name,            dose_cGy, surv_pct, surv_sd_pct
    ("SCID  (DNA-PKcs-)", 250.0,  9.0, 1.0),
    ("CB-17 (DNA-PKcs+)", 500.0, 12.0, 5.0),
]

def alpha_from_point(D_cGy: float, S_pct: float):
    """S = exp(-alpha * D)  =>  alpha = -ln(S)/D  (alpha in cGy^-1)."""
    s = S_pct / 100.0
    return -math.log(s) / D_cGy

def alpha_uncertainty(D, S, sS):
    """1-sigma in alpha from 1-sigma in S, log-linear model."""
    s  = S  / 100.0
    ds = sS / 100.0
    # dalpha/dS = -1/(D*S); sigma_alpha = |dalpha/dS| * sigma_S
    return abs(1.0 / (D * s)) * ds

print("=" * 78)
print("Equitoxic-dose audit: log-linear alpha estimate from a single (D,S) point")
print("=" * 78)

rows = []
for name, D, S, sS in points:
    a  = alpha_from_point(D, S)
    sa = alpha_uncertainty(D, S, sS)
    rows.append((name, D, S, sS, a, sa))
    print(f"{name:>22s} | D = {D:>5.0f} cGy   S = {S:>5.1f} +/- {sS:.1f} %"
          f"   alpha = {a*100:.4f} +/- {sa*100:.4f}  (per Gy)")

# Equitoxic overlap check: do the two surviving fractions agree within 1 sigma?
name_a, _, Sa, sSa, _, _ = rows[0]
name_b, _, Sb, sSb, _, _ = rows[1]
delta   = Sb - Sa
delta_s = math.sqrt(sSa**2 + sSb**2)
overlap = "YES" if abs(delta) <= delta_s else "NO"
print("-" * 78)
print(f"Equitoxic claim: SCID(9+/-1) vs CB-17(12+/-5)  ->  delta = {delta:+.1f}"
      f" +/- {delta_s:.1f} %   (1-sigma overlap: {overlap})")

# Dose modifying factor (DMF) at equal survival, naive ratio of the doses.
DMF = 500.0 / 250.0
print(f"DMF (dose to reach same surv, CB-17/SCID): {DMF:.2f}  (paper says SCID"
      " 'much more sensitive'; 2x in dose at ~equal survival.)")

# alpha ratio between the two cell lines
alpha_scid = rows[0][4]
alpha_cb17 = rows[1][4]
ratio = alpha_scid / alpha_cb17
print(f"alpha(SCID)/alpha(CB-17) = {ratio:.2f}  (>1 means SCID more radio-sensitive)")

with OUT.open("w") as fh:
    fh.write("cell_line\tdose_cGy\tsurv_pct\tsurv_sd_pct\talpha_per_cGy\talpha_sd_per_cGy\n")
    for name, D, S, sS, a, sa in rows:
        fh.write(f"{name}\t{D:.0f}\t{S:.1f}\t{sS:.1f}\t{a:.6f}\t{sa:.6f}\n")
    fh.write(f"# DMF_CB17_over_SCID\t{DMF:.4f}\n")
    fh.write(f"# alpha_ratio_SCID_over_CB17\t{ratio:.4f}\n")
    fh.write(f"# equitoxic_overlap_1sigma\t{overlap}\n")
print(f"Wrote: {OUT}")

# Caveats baked into the output:
print("-" * 78)
print("CAVEATS:")
print(" * Single-point alpha is a lower bound; with no full survival curve")
print("   published, true linear-quadratic alpha/beta separation is impossible.")
print(" * The paper does NOT include raw counts, replicate-level data, or any")
print("   intermediate doses for clonogenic survival, so beta cannot be fit.")
print(" * Estimates here only check internal arithmetic consistency of the")
print("   paper's own 'equitoxic' and 'DNA-PKcs not required for ASR' claims.")
