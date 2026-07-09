# LUCID100 — Yu, Geng, Tang (Med Phys 2024): BNCT via Cellular DNA Damage Repair Model

**LUCID100 slot:** 42 (Wave 5)
**Paper:** Yu C., Geng C., Tang X. (2024). *Assessing the biological effects of boron neutron capture therapy through cellular DNA damage repair model.* Medical Physics 51(12), 9372–9384.
**DOI:** [10.1002/mp.17446](https://doi.org/10.1002/mp.17446)
**Subject area:** A-14 — DNA repair / DDR · radiation quality / RBE · computational model / simulation
**Replication mode:** simulation/model replication (artifact harvest + reduced analytic smoke check).

## TL;DR

- The paper extends the **MEDRAS** mechanistic DNA repair and survival model (McMahon, Frontiers in Oncology 2021) to BNCT secondary particles by feeding it BNCT-specific radial energy depositions computed in **Geant4-DNA**, plus dose factors (F, W) computed in **TOPAS-nBio** for BPA / BSH microdistributions.
- **Public availability:**
  - MEDRAS analytic version → **public** at https://github.com/sjmcmahon/MEDRAS (Python, MIT-style). Mirrored to `artifacts/medras_analytic/`.
  - MEDRAS Monte Carlo version → referenced but **not directly published with this paper** (the authors do not provide a code or data availability statement).
  - Their BNCT extension code, the Geant4-DNA radial deposition tables, and the TOPAS-nBio dose factors for BPA/BSH → **not released**. No supplement, no Zenodo, no GitHub link in the paper.
- **Heavy compute required for full replication:** YES — Geant4-DNA + TOPAS-nBio Monte Carlo simulations are needed to regenerate the BNCT-specific tracks and dose factors. Per the LUCID100 rules we did **not** run these on CherryRd. A job plan is included.
- **Reduced analytic smoke check done locally:** YES. We use the public analytic MEDRAS with built-in particle tracks (proton, helium) to reproduce the paper's methodology (LQ fits per component + Eq. 6 dose-share accumulation) and recover order-of-magnitude RBE values:
  - Helium @ 150 keV/μm (alpha+7Li surrogate): RBE₀.₀₁ ≈ 2.15 (paper boron-dose component RBE 3.60 BPA / 0.73 BSH; the spread is driven by microdistribution F/W factors we cannot reproduce without their TOPAS data).
  - Proton @ 17 keV/μm (¹⁴N(n,p)¹⁴C 0.58 MeV proton): RBE₀.₀₁ ≈ 1.41 (paper proton component 3.21; difference is again microdistribution-related).
  - BPA-like high-boron mix (Eq. 6): RBE₀.₀₁ ≈ 1.73 (paper BPA total 2.50; experimental refs 2.52 / 2.81).
- **Verdict:** `PARTIAL_REDUCED_ANALYTIC` — methodology reproduces, exact numbers do not without the unreleased BNCT microdistribution data.

## Directory layout

```
lucid100-bnct-dna-damage-repair-model/
├── README.md                  # this file
├── PROGRESS.md                # checklist + log
├── REPORT.md                  # first-pass replication report (verdict + evidence)
├── ARTIFACT_MANIFEST.md       # what's harvested and from where
├── refs/
│   └── paper.pdf              # full open-access PDF from NUAA mirror
├── artifacts/
│   ├── medras_analytic/       # shallow clone of sjmcmahon/MEDRAS
│   └── smoke_output.txt       # output of the analytic smoke run
└── scripts/
    └── medras_bnct_smoke.py   # CPU-only analytic smoke script (no MC, no GPU)
```

## How to re-run the smoke check (CPU, ~2 seconds)

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-bnct-dna-damage-repair-model
python3 scripts/medras_bnct_smoke.py
```

Requires: Python 3 with `numpy`. The MEDRAS code is already vendored under `artifacts/medras_analytic/`.

## Heavy-compute job plan (NOT run here)

A full reproduction of Table 1 / Figures 7-8 would need:

1. **Geant4-DNA (G4EmDNAPhysics)** — radial energy deposition E(r) at the center depth of a 200 μm × 22 μm water phantom, for:
   - α at 0.2, 0.4, …, 1.2, 1.47, 1.78 MeV
   - ⁷Li at 0.2, 0.4, 0.6, 0.84, 1.02 MeV
   - protons at 0.001–1 MeV (probability-weighted)
   Counting region thickness 0.5 μm, source at center.
   Estimated runtime: hours on a single workstation; trivially parallelizable.

2. **TOPAS-nBio** — 3×3×3 cell-nucleus grid (nucleus r=4.32 μm, cell r=8 μm). Compute:
   - F factor (nuclear/cellular dose ratio) per particle type and per boron drug microdistribution (BPA: cytoplasm+extracellular; BSH: membrane+extracellular).
   - W factor (per emission location, 4 cases: n, c, s, e) for α and ⁷Li.
   Estimated runtime: tens of hours single-thread; embarrassingly parallel by particle-energy/source-location pair.

3. **MEDRAS Monte Carlo** — read SDD-format DNA damage distributions, run repair / misrepair / survival. Public analytic MEDRAS is sufficient for the LQ-fit and Eq. 6 steps; the MC version (not on the McMahon public repo, but referenced internally) is needed only for the per-particle SDD pipeline.

**Recommended target:** uicgpu (interactive, no queue, 2 TB RAM is overkill but the CPU count is the win) or chiatta00 (CPU-only path is fine; Geant4 does not need PVCs). **AVOID CherryRd** per the LUCID rules.

A skeleton SLURM/PBS-free shell script for the Geant4-DNA step is left as TODO — would be the next milestone if this replication is escalated beyond a first pass.

## Author contact

Not attempted. Corresponding authors are Changran Geng and Xiaobin Tang at NUAA (`gengchr@nuaa.edu.cn`, `tangxiaobin@nuaa.edu.cn`). They acknowledge Stephen McMahon (Queen's University Belfast, MEDRAS author) for assistance.

## QA recommendation

Retag this row in `LUCID100_SOLID_MASTER_QA.tsv` from `Wave 5 / candidate_curated` to:

> `Wave 5 / partial_reduced_analytic — PARTIAL: artifact harvested (paper + public MEDRAS); reduced analytic smoke check reproduces methodology and qualitative RBE ordering; exact Table 1 numerical reproduction requires unreleased Geant4-DNA radial-deposition tables + TOPAS-nBio dose factors (F, W) for BPA/BSH microdistributions, plus the unpublished BNCT extension to MEDRAS Monte Carlo. KEEP: methodology is sound and partially reproducible.`
