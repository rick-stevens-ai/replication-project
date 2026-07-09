# LUCID replication: Cellular lethal damage of 64Cu (Carrasco-Hernandez et al. 2023)

**Target paper**
Carrasco-Hernandez J, Ramos-Méndez J, Padilla-Rodal E, Avila-Rodriguez MA.
*Cellular lethal damage of 64Cu incorporated in mammalian genome evaluated with
Monte Carlo methods.* Front. Med. **10**:1253746 (28 Sep 2023).
DOI: [10.3389/fmed.2023.1253746](https://doi.org/10.3389/fmed.2023.1253746)

PDF: `paper.pdf` (copy of `367ea049718878f5dd75b297f68aea077a272538.pdf`).

## What this replication contains

| Component | Status |
|-----------|--------|
| Full TOPAS-nBio / Geant4-DNA Monte Carlo rerun | **BLOCKED** (toolchain + 400k-history runs not feasible in subagent) |
| Analytic reproduction of Eq. 1 lethal-damage atom count vs Table 2 | **REPLICATED** (max 0.21 % deviation across all 5 radionuclides) |
| Re-implementation of the DSB-scoring rule (opposite-strand SSBs ≤ 10 bp) | **REPLICATED (method)** with unit tests + track-correlated demo |
| Spot-check of 64Cu electron yield against ICRP 107 (MIRDsoft) | **SPOT-CHECK PASSED** (~0.23/decay vs paper's ~0.18) |
| End-to-end MC rerun for 64Cu DSB/decay (0.171 ± 0.003) | **NOT REPRODUCED** — requires actual TOPAS-nBio runs |

## Verdict

**PARTIAL** — see `REPORT.md`.

| Dimension | Score /10 |
|-----------|-----------|
| Lethal-damage equation coverage | 10 |
| DSB-scoring algorithm coverage | 8 (method reproduced; no end-to-end yields) |
| Decay-spectrum coverage | 5 (spot-check only; no per-shell cascade) |
| End-to-end MC reproduction | 0 (blocked) |
| **Overall coverage** | **5/10** |
| **Agreement (on what was reproduced)** | **10/10** |

## Layout

```
paper.pdf                       # local copy of the target paper
PROGRESS.md                     # phase log (live during replication)
REPORT.md                       # full write-up + verdict
README.md                       # this file
code/
  01_lethal_damage_equation.py  # Eq. 1 cross-check against Table 2
  02_proximity_dsb_scoring.py   # DSB-scoring rule + unit tests + scan
  03_track_correlated_dsb.py    # track-correlated demo of DSB:SSB ratio
  04_make_figures.py            # render figures
results/
  01_eq1_crosscheck.txt
  02_proximity_dsb_demo.txt
  03_track_correlated.txt
figures/
  fig01_eq1_crosscheck.png      # N0 and activity: this work vs paper
  fig02_dsb_ssb_ratio.png       # synthetic-track DSB:SSB ratios vs literature regimes
```

## How to rerun

```bash
cd lucid-cu64-topas-nbio-lethal-damage
python3 code/01_lethal_damage_equation.py
python3 code/02_proximity_dsb_scoring.py
python3 code/03_track_correlated_dsb.py
python3 code/04_make_figures.py
```

Dependencies: Python 3.10+, NumPy, Matplotlib. No special toolkits.

## Public sources used

* The article itself (open access, CC-BY).
* ICRP Publication 107 (Nuclear Decay Data for Dosimetric Calculations), via
  MIRDsoft `MIRDspecs` summary sheet for Cu-64 (publicly served).
* NNDC half-lives for the comparison radionuclides.

No paid endpoints; no author contact.
