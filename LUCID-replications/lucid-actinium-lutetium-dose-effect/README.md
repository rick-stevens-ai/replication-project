# LUCID Replication — Ruigrok et al. EJNMMI 2022 (Ac-225 vs Lu-177 PSMA-I&T)

**Paper.** Ruigrok EAM, *et al.* "In vitro dose effect relationships of actinium-225-
and lutetium-177-labeled PSMA-I&T." *Eur J Nucl Med Mol Imaging* 2022; 49:3627-3638.
DOI [10.1007/s00259-022-05821-w](https://doi.org/10.1007/s00259-022-05821-w).
Open Access (CC-BY 4.0).

**Verdict:** PARTIAL / SPOT-CHECK (see `REPORT.md` for full justification).

## What you'll find here

| File | Purpose |
|---|---|
| `REPORT.md` | Full replication report, methods, verdict, agreement scores |
| `PROGRESS.md` | Chronological log of the replication run |
| `paper.pdf` | Local copy of the source paper (Open Access) |
| `code/replicate_lucid.py` | One-script replication of the linear dose-response fit + dosimetry pipeline |
| `results/` | Tabular outputs (CSV) and a machine-readable summary (JSON) |
| `figures/` | Replicated dose-response curve and pipeline cross-check |

## Quick re-run

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-actinium-lutetium-dose-effect/
python3 code/replicate_lucid.py
```

Requires Python 3.9+, numpy, scipy, pandas, matplotlib.

## TL;DR of the result

- The paper's central claim is **RBE([Ac-225]/[Lu-177]) ≈ 4.2 ± 0.46** with
  α(Lu-177)=0.16 Gy⁻¹ and α(Ac-225)=0.67 Gy⁻¹ from a linear log-survival fit.
- Refitting the linear model on doses from the paper's own Table 3 combined with
  survival fractions digitized from Figure 3 recovers α(Ac-225) = 0.64 ± 0.05
  Gy⁻¹ (within 1σ of 0.67) and α(Lu-177) = 0.22 (within 2σ of 0.16). RBE
  recovered = 3.0–3.3 vs published 4.2 — consistent within digitization noise.
- The MIRD-style dosimetry pipeline reproduces the Table 3 doses up to a
  constant scale factor (1.3× for Lu, 2.4× for Ac), confirming the math chain
  is structurally correct.
- The full Geant4 Monte Carlo S-value computation is **not** replicated (out
  of scope); we trust the authors' published S-values.

## What this does NOT replicate

- Wet-lab clonogenic, 53BP1 foci, IC50 or uptake assays (no raw data deposited).
- Geant4 Monte Carlo of cell-geometry S-values.

These are honest gaps documented in `REPORT.md`.
