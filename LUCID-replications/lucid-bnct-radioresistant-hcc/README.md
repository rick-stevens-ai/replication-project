# LUCID replication — BNCT in radioresistant HCC (Huang et al. 2022)

**Target paper**
Huang C-Y, Lai Z-Y, Hsu T-J, Chou F-I, Liu H-M, Chuang Y-J.
*Boron Neutron Capture Therapy Eliminates Radioresistant Liver Cancer Cells by
Targeting DNA Damage and Repair Responses.*
J Hepatocell Carcinoma. 2022;9:1385–1401. doi:[10.2147/JHC.S383959](https://doi.org/10.2147/JHC.S383959)

Open Access (Dove Medical Press, CC BY-NC 3.0).

## What this replication does

The paper is largely a wet-lab mechanism study (γH2AX foci, Western blots for HR/NHEJ/G2 checkpoint/apoptosis proteins, cell-cycle flow). Those panels are not numerically replicable from the PDF alone — no raw data, no supplements with numerical tables.

But the paper *does* contain a fully replicable **quantitative radiobiology core**:

- Clonogenic survival curves at 0,1,2,3,5,8 Gy γ-ray (Fig 1C) with mean ± SD reported in the Results text for HepG2 and HepG2-R at 1, 2, 5 Gy.
- Clonogenic survival curves for BNCT vs γ-ray at 0,1,2,3 Gy (Fig 3B).
- D10 values for all four conditions (paper Table 4).
- RBE = D10(γ-ray)/D10(BNCT) — closed-form definition, given in Table 4 legend.
- γ-ray dose-rate/time table (Table 1).

This repository fits the **linear-quadratic (LQ) model** SF(D) = exp(−αD − βD²) to each clonogenic curve, recovers D10 analytically, and recomputes RBE.

## Layout

```
code/replicate.py        single-file replication script (numpy/scipy/matplotlib/pandas)
results/                 fit_parameters.csv, rbe_table.csv, table1_check.csv
figures/                 clonogenic_gamma.png, clonogenic_bnct.png
PROGRESS.md              status timeline
REPORT.md                full verdict + agreement table
```

## Run

```bash
python3 code/replicate.py
```

Requires Python 3 with `numpy`, `scipy`, `pandas`, `matplotlib`.

## Verdict (summary)

**PARTIAL** replication, coverage **5/10**, agreement **8/10** on the quantitative core.

- ✅ Paper's own RBE arithmetic is **internally exact** (recomputed 3.6750 and 5.9717 vs stated 3.675 and 5.972).
- ✅ LQ refit of γ-ray Fig 1C reproduces paper D10 to within **~3.5–3.7%** for both HepG2 and HepG2-R using only the three text-cited mean ± SD points.
- ✅ Table 1 dose-rate/time entries are internally consistent (<1.3 s rounding gap).
- ⚠️ BNCT D10 refit (Fig 3B) reproduces paper D10 to within **~18–40%** — limited by figure-digitization since the paper does not print per-point SFs for Fig 3B.
- ❌ Wet-lab mechanism panels (γH2AX foci fold-changes, Western blot densitometry, cell-cycle %, caspase-3 fractions) are NOT replicable from the PDF: only summary fold-changes are listed in the text and there is no raw or per-replicate data.

See `REPORT.md` for the full breakdown.

## Data provenance

- Author-cited numerical values are quoted verbatim from the published Results section (DOI above).
- Where numerical means are not in the text (Fig 3B BNCT/γ-ray per-point SFs, Fig 1C 3 Gy/8 Gy points), values were digitized from the published figures using image analysis on the PDF; these points are flagged `cited=False` in the code and are NOT presented as author values.

No author contact, no paid APIs, no proprietary data. All inputs are derivable from the open-access PDF.
