# LUCID100 slot 41 — Jolly & Fielding 2025 (TαT single-cell MC dosimetry)

**DOI:** 10.1007/s13246-025-01605-2  
**Citation:** Jolly A.L. & Fielding A.L. (2025). *Modelling single cell dosimetry and DNA damage of targeted alpha therapy using Monte-Carlo techniques.* Physical and Engineering Sciences in Medicine 48(4):1611–1624.  
**License:** Open access (Springer Nature, also mirrored on PubMed Central PMC12738655 and QUT ePrints 262590).  
**LUCID100 row:** 90 (Wave 5, A, slot 41 backfill — Group 14, candidate_curated).

## What the paper does

Uses **OpenTOPAS 3.9 + TOPAS-nBio (built on Geant4 v11.1 + Geant4-DNA)** to simulate four α-emitting radionuclides for targeted alpha therapy (TαT):

- **²²⁵Ac** (T½ ≈ 9.92 d) — long decay chain, 4α
- **²²³Ra** (T½ ≈ 11.4 d) — long decay chain, 4α
- **²¹²Pb** (T½ ≈ 10.6 h) — short chain, 1α (via daughter ²¹²Bi/²¹²Po)
- **²¹¹At** (T½ ≈ 7.2 h) — short chain, 1α (58% direct α emission)

**Cell model:** two concentric spheres in 30 µm water cube — cell R=10 µm, nucleus R=5 µm, both G4_WATER (ρ=1 g/cm³). 100 radionuclides randomly placed per simulation, 20 statistically-independent repeats.

**Four source distributions:** (1) 0.01 µm cell-wall shell, (2) cytoplasm volume, (3) 0.01 µm nucleus-wall shell, (4) nucleus volume.

**Physics:** outer cell — `g4em-standard_opt0, g4h-phy_QGSP_BIC_AllHP, g4decay, g4ion-binarycascade, g4h-elasticHP, g4stopping, g4radioactivedecay`. Nucleus — either `g4em-standard_opt0` (condensed history) or `g4em-dna` (track structure).

**Scorers:** `DoseToMedium` (nucleus, total + α-only via filter), `SurfaceTrackCount` (nucleus outer surface, total + α-filter), and TOPAS-nBio **DBSCAN scorer** for SSB/sDSB/cDSB.

**DBSCAN damage model (the key analytical part):**
- Per-ionisation linear probability ramp: P=0 for E<5 eV, linear up to P=1 at E≥37.5 eV.
- DNA volume fraction = 16% of nucleus → Bernoulli sampling.
- Cluster radius = 3.2 nm (≈10 bp) using density-based clustering → DSB.
- sDSB vs cDSB by lesion multiplicity inside the cluster.

**Headline results (Table 2, ²¹¹At, cGy/decay):**

| Config | Mem | Cyto | Nuc |
|---|---|---|---|
| Full decay, total, g4em-dna | 2.59 | 3.85 | 14.92 |
| Full decay, total, opt0 | 0.93 | 1.79 | 12.88 |
| α only (discrete), total, g4em-dna | 1.81 | 3.67 | 16.63 |
| Guerra Liberal et al. (α only, opt4) | 1.04 | 1.98 | 8.26 |

**Conclusion:** nucleus-localised radionuclides deliver 4–17× more dose/decay than membrane-localised ones; ²²⁵Ac/²²³Ra have higher dose/decay than ²¹¹At/²¹²Pb due to multi-α decay chains; ²¹¹At/²¹²Pb dose-per-decay is similar across radionuclides when sources are inside the nucleus.

## Replication scope (this folder)

This is a **first-pass artifact harvest + reduced analytical reproduction**. We do **NOT** run TOPAS-nBio in this subagent (heavy GPU/CPU cluster job, Geant4 v11.1 build required). See `HPC_JOB_PLAN.md` for what a full reproduction would need.

**What we DO reproduce locally (CPU, seconds):**
1. **Decay-chain α energy spectra** for ²²⁵Ac, ²²³Ra, ²¹²Pb, ²¹¹At from NNDC/ENSDF/ICRP-107 → matches Appendix 1 of paper. → `code/01_decay_chains.py`
2. **CSDA-range geometry check** — alpha range in liquid water (50–100 µm for 5–8 MeV) vs nucleus radius (5 µm) → predicts ~all alphas from the nucleus deposit ~100% of their kinetic energy in the cell, and only a fraction of cell-wall-launched alphas reach the nucleus. → `code/02_alpha_range_geom.py`
3. **Analytical S-value sanity check** — point-isotropic α source uniformly distributed in nucleus volume → estimated mean energy deposited per decay assuming CSDA. Used to bracket the Nuc-column in Table 2. → `code/02_alpha_range_geom.py`
4. **DBSCAN damage-model implementation** — Python re-implementation of the 5/37.5 eV ramp, 16% DNA fraction, 3.2 nm clustering. Unit test against a synthetic ionisation cloud. → `code/03_dbscan_damage.py`

**What we do NOT reproduce:** track-structure ionisation maps for ²¹¹At/²¹²Pb/²²⁵Ac/²²³Ra decay chains (requires TOPAS-nBio + Geant4-DNA cluster runs).

## Files

- `artifacts/paper.pdf` — full open-access PDF (2.4 MB, retrieved from Springer)
- `artifacts/paper.txt` — `pdftotext -layout` extraction
- `ARTIFACT_MANIFEST.md` — provenance for every external resource
- `code/01_decay_chains.py` — α energies and yields per parent decay (NNDC)
- `code/02_alpha_range_geom.py` — CSDA range + nucleus-geometry sanity check vs Table 2
- `code/03_dbscan_damage.py` — Python DBSCAN damage model + unit test
- `results/01_decay_chains.txt` — α spectra dump
- `results/02_alpha_geom.txt` — range/geometry numbers
- `results/03_dbscan_unit_test.txt` — clustering tests pass/fail
- `HPC_JOB_PLAN.md` — exact compute plan for the full TOPAS-nBio rerun
- `FIRST_PASS_REPORT.md` — verdict and what was reproduced
- `PROGRESS.md` — chronological log
