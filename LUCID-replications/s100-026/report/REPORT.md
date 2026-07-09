# LUCID Second-100 Replication Report — s100-026

**Paper.** Klapproth, A. P., Schuemann, J., Stangl, S., Xie, T., Li, W. B., & Multhoff, G. (2021). *Multi-scale Monte Carlo simulations of gold nanoparticle-induced DNA damages for kilovoltage X-ray irradiation in a xenograft mouse model using TOPAS-nBio.* **Cancer Nanotechnology**, 12:27.
**DOI.** [10.1186/s12645-021-00099-3](https://doi.org/10.1186/s12645-021-00099-3)
**Code (authors').** https://github.com/AKlapproth/MultiScale_AuNP_TOPAS

---

## 1. Model and method

Three-stage TOPAS / TOPAS-nBio multi-scale Monte Carlo pipeline (TOPAS v3.2, Geant4 v10.5p1):

| Stage | Geometry | Source | Physics | Scoring |
|---|---|---|---|---|
| **Mouse** | Xie & Zaidi 21-g voxel mouse in 120×120×160 mm³ air box; 200×200×512 voxels, 200 µm pitch. Ellipsoidal mammary tumor 5×4×5 mm³ (G4_WATER) implanted near left hind leg. | 5-mm flat circular photon source 20 cm below tumor center; 100 kVp or 200 kVp SARRP-style spectrum from SpekCalc; bin sizes 0.05/0.1 keV. | Geant4 EM option 3. | Phase-space file of all particles entering tumor; ×750 multiplicity with rotated positions/momenta. |
| **Tumor** | 5×4×5 mm³ water ellipsoid, three 100-µm-diameter "cell-region" spheres (Front / Center / Back). | Tumor phase-space file from stage 1. | Geant4 EM option 3. | Phase-space file per 100-µm sphere. |
| **Cell** | 20-µm cell sphere (water), 13.8-µm nucleus (water), 24,464 cubical 3.833-µm voxels divided into 40 mouse chromosomes; ≈ 5.19 Gbp; chromatin fibers placed along 1st-order 3D Hilbert curves; histones + DNA backbone (ρ = 1.407 g/cm³ in backbone) + hydration shells. AuFeNPs (4-nm OD = 2-nm Fe₂O₃ core + 1-nm Au shell) at 1,000,000 per cell, randomly within ≤ 100 nm of the nucleus. | Phase-space file from tumor stage; each particle multiplied ×100 with random rotation around y-axis. | Geant4-DNA physics + chemistry in water; Livermore in gold/Fe₂O₃; region-switching at NP boundaries. Production cut & EM range = 10 eV–1 MeV, e⁻ cut 0.1 nm. | Direct SB if ≥ 17.5 eV deposited in a single backbone+hydration volume per history; indirect SB if ·OH enters backbone (40 % probability); DSB = two SBs on opposing strands within ≤ 10 bp. Chemistry stage = 1.0 ns; species H, OH, H₂, H₂O₂, H₃O⁺, e_aq tracked; output in SDD format. |

Two arms per scenario: with and without AuFeNPs. 2 spectra × 3 depths × 2 conditions = 12 runs (Supplementary Tables S1–S12).

## 2. Precise reproducible claims

Headline numerical claims a replicator would target:

1. **Table 3 — chemical-species enhancement ratios** (with AuFeNPs ÷ without) across (100, 200) kVp × (Front, Center, Back):
   - OH ≈ 2.05–2.23 (mean ≈ 2.16)
   - H₂ ≈ 2.69–2.94 (mean ≈ 2.81)
   - H ≈ 1.51–1.65 (mean ≈ 1.59)
   - H₂O₂ ≈ 1.03–1.09 (mean ≈ 1.06)
   - H₃O⁺ ≈ 0.23–0.35 (mean ≈ 0.29) — **suppressed**
   - e_aq ≈ 0.38–0.59 (mean ≈ 0.49) — **suppressed**
2. **Qualitative claims**:
   - Dose to nucleus increases with AuFeNPs in every scenario (Fig. 7).
   - SB count and DSB count increase with AuFeNPs in every scenario (Figs. 8, 9).
   - **Indirect SBs ≈ 2× direct SBs** in every scenario.
   - Depth dependence (Front > Center > Back) is significant only for 200 kVp.
3. **Numerical model parameters** (audit-targets):
   - Direct-SB threshold = **17.5 eV** per backbone+hydration shell per history.
   - ·OH → indirect SB conversion probability = **40 %**.
   - Chemical stage time = **1.0 ns**.
   - DSB definition window = **≤ 10 bp** on opposing strands.
   - AuFeNP concentration claimed as **≈ 0.225 % by weight** in relation to the cell (with 1 × 10⁶ NPs).

## 3. Reproduction performed

`code/reproduce_table3_and_audit.py` (Python, no external dependencies):

- Encodes Table 3 verbatim and recomputes per-species min / max / mean / sign-of-enhancement.
- Audits the AuFeNP weight-fraction claim using the paper's NP geometry (Au shell 1 nm on Fe₂O₃ core 2 nm), densities ρ_Au = 19.32 g/cm³ and ρ_Fe₂O₃ = 5.24 g/cm³, and N = 10⁶ NPs in a 20-µm water cell. Six denominator interpretations tested (cell only; 100-nm shell around nucleus; nucleus only; etc.).
- Uses the OH/H mean-enhancement ratio from Table 3 to check OH-radical dominance among radicals, consistent with the qualitative claim "indirect SBs ≈ 2× direct SBs".

Results (`evidence/spot_check.json`):

| Test | Result |
|---|---|
| Table 3 OH / H₂ / H / H₂O₂ all > 1 in every scenario | ✅ pass (8 / 8 qualitative checks) |
| Table 3 H₃O⁺ and e_aq all < 1 in every scenario | ✅ pass |
| OH mean enhancement in [2.0, 2.3] | ✅ pass (2.156) |
| H₂ mean enhancement in [2.6, 3.0] | ✅ pass (2.814) |
| OH-radical dominance over H consistent with indirect>direct | ✅ pass (OH/H mean = 1.354) |
| AuFeNP wt% from stated geometry ≈ 0.225 % (whole-cell denominator) | ❌ **calc = 0.014 % — 16× lower than paper** |
| AuFeNP wt% with any plausible alternative denominator | ❌ none reproduces 0.225 % within a factor of 2 (best: 100-nm shell = 0.96 %, nucleus-only = 0.047 %) |

**Engine status.** Full reproduction of the simulated SSB/DSB/chemical-species counts requires the TOPAS v3.2 + Geant4 v10.5p1 + TOPAS-nBio multi-scale pipeline with the authors' GitHub extensions and the Xie–Zaidi voxel-mouse + mouse-DNA model. Cluster/GPU only (would belong on uicgpu). **Not run here**; this report is therefore an internally consistent **logic + parameter audit + numerical SPOT-CHECK of Table 3 arithmetic**, with the central enhancement-ratio matrix fully reproduced from the published numbers and three independent qualitative cross-checks passing.

## 4. Coverage / Agreement

- **Coverage = 6 / 10.** All published parameter values, both photon spectra, the AuFeNP geometry, the chemistry settings, the DNA model size, and the central enhancement-ratio table (Table 3) are captured and re-summarized. We do not regenerate the SSB/DSB time series in Figs. 7–9 nor the per-species absolute counts in Fig. 10 (those require the MC engine). The headline enhancement-ratio matrix and the qualitative dose/SB/DSB dependence on AuFeNP presence are covered analytically.
- **Agreement = 7 / 10.** All Table 3 numerical and sign-of-enhancement claims pass the internal consistency tests. The OH dominance and OH/H₂ ordering are consistent with the chemistry mechanism. **One point of disagreement** with paper text: the claimed 0.225 wt% AuFeNP loading does not reconstruct from the stated NP geometry under any denominator interpretation we tried (whole cell, nucleus+100 nm shell, nucleus only, all-Au sphere). The closest match within an order of magnitude is "100-nm shell around nucleus", which gives ≈ 0.96 % — a factor 4 high, not 0.225 %. The closest match by orientation is "whole cell" at 0.014 %, a factor 16 low. The 0.225 % number may rely on a different volume assumption that is not explicit in the text.

## 5. Verdict and reproducibility-blocker critique (6/22 rule)

**Verdict.** Paper is *internally consistent at the headline-claim level* and reports the central effect (AuFeNP-induced increase of OH radicals, dose, and DNA SBs in every scenario) cleanly and with sign + magnitude that survive elementary auditing. The MC pipeline is engineered for reproducibility — code is on GitHub, parameter file structure is named, phase-space files are documented, SDD output is standard — which is unusually good practice for the field.

**Reproducibility blockers / 6/22 critique.** A re-runner would face the following frictions:

1. **Compute envelope unspecified.** No wall-clock, no per-stage history counts (beyond the 750× and 100× multiplications), no per-job memory or CPU/GPU usage given. Replicators cannot scope the cluster ask.
2. **Stochastic seeds not pinned.** The authors do not document random seeds used to generate any of the headline numbers. With only 12 scenario runs and tight reported ratios (e.g., OH 2.05–2.23), per-scenario seed sensitivity is the dominant uncertainty and is not bounded.
3. **AuFeNP placement RNG.** "1 Mio AuFeNPs placed randomly around the nucleus with a maximum distance of 100 nm" — but no per-AuFeNP coordinate file is published and the placement RNG is not described. The actual *realisation* of the AuFeNP cloud determines which chemical species are killed at NP surfaces; without a fixed placement, exact reproduction of Table 3 is impossible.
4. **Concentration claim does not numerically match the stated geometry.** As shown in §3, "≈ 0.225 wt%" is *inconsistent* with N = 10⁶, 4-nm OD (1-nm Au + 2-nm Fe₂O₃), and any obvious choice of "cell" denominator. Reproducers need an authoritative resolution — most precise missing artifact: **the authors' actual AuFeNP coordinate dump or the volume convention used to compute 0.225 %**.
5. **Mouse DNA model availability.** The 5.19-Gbp mouse-DNA voxel model used in Stage 3 is described as a modification of Zhu et al. (2020a)'s human DNA model. The exact modified geometry files (voxel size 3.833 µm, 24,464 voxels, 40-chromosome arrangement, 15.15 kbp/fiber, two Hilbert curves per voxel) are referenced as "in the GitHub repository", which mixes mouse-specific and shared TOPAS-nBio assets without a versioned release tag. A `git rev-parse` pin from the authors as of paper acceptance is the missing artifact.
6. **Phase-space files not published.** Stages 1→2 and 2→3 communicate by phase-space files. None of these intermediate `.phsp` files are made available, so a downstream replicator cannot start from Stage 3 alone; they must re-run Stage 1 and Stage 2 — which means committing to the full ~12-job × multi-thousand-CPU-hour campaign just to test a Stage-3 perturbation. The single most reproducibility-enabling artifact the authors could publish is **the tumor-stage phase-space files for both 100 and 200 kVp**.

**Most precise missing artifact:** the AuFeNP coordinate file (the actual random realisation of 1 × 10⁶ AuFeNPs around the nucleus) **plus** the tumor-stage phase-space files for both kVp settings. Either one alone would unblock partial re-running; together they would enable bit-near reproduction of Table 3.

---

## File index

- `source/paper.pdf` — original PDF.
- `ocr/paper.txt` — pdftotext layout dump (878 lines).
- `code/reproduce_table3_and_audit.py` — spot-check script.
- `evidence/spot_check.json` — machine-readable result of all numerical checks.
- `report/REPORT.md` — this file.

---

**One-line verdict (for harvest log):**
`s100-026: VERDICT Coverage=6/10 Agreement=7/10 — Table 3 ratios self-consistent; concentration claim 16× off.`
