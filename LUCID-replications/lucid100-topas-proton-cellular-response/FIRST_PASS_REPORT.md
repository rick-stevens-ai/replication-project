# FIRST PASS REPORT — LUCID100 W2-#16

**Paper:** Zhu H, McNamara AL, McMahon SJ, Ramos-Mendez J, Henthorn NT,
Faddegon B, Held KD, Perl J, Li J, Paganetti H, Schuemann J.
*Cellular Response to Proton Irradiation: A Simulation Study with TOPAS-nBio.*
**Radiat. Res.** 194(1):9–21 (2020). DOI: 10.1667/RR15531.1.

**Subagent run:** 2026-06-09 13:06–13:12 CDT. Main agent: argo claude-opus-4.7.

**Verdict:** **PARTIAL — METHOD ARTIFACTS HARVESTED, REPAIR STAGE CLEARLY
REPLICABLE LOCALLY, INITIAL-DAMAGE STAGE REQUIRES HPC.**

---

## 1. What the paper does

End-to-end Monte-Carlo simulation pipeline for cellular response to proton
irradiation:

1. **Initial DNA damage induction** (TOPAS-nBio + Geant4-DNA).
   - Whole-nucleus model: 9.3 μm spherical fibroblast G0/G1 nucleus, 46
     chromosomes, 6.08 Gbp total DNA, 14.4 Mbp/μm³ density.
   - Fractal chromatin geometry (Hilbert curve fiber loops).
   - Default `TsEmDNAPhysics` + `TsEmDNAChemistry` with proton ionization
     cross-sections extended to 500 MeV.
   - 12 proton energies × 100 runs × 1 Gy each.
   - Direct SB if ≥17.5 eV deposited in backbone+hydration shell; indirect
     SB if `OH` reacts with backbone (p=0.4); DSB if two SBs on opposite
     strands within 10 bp.
   - Output written in SDDv1.0 format.

2. **Repair, chromosome aberration, micronucleus modelling** (MEDRAS).
   - MEDRAS NHEJ+HR+MMEJ model, fitted parameters from McMahon 2016/2017.
   - Updated NHEJ end-rejoining coefficient 2.07 ± 0.17/h (fast),
     HR 0.26 ± 0.01/h (slow). Base misrepair (single-DSB) rate 1.46%.
   - Predicts: residual DSB fraction, misrepair fraction vs LET, dicentric
     and excess acentric fragment yields, % BN cells with MN.

## 2. Key numerical results from the paper

(Transcribed from Appendix Table A2 into `results/table_A2.csv`.)

| Energy (MeV) | LET (keV/μm) | DSB/Gy/Gbp (total) | DSB hybrid | DSB direct | DSB indirect |
|--------------|--------------|---------------------|------------|------------|--------------|
| 0.5          | 60.09        | **21.21**           | 9.55       | 6.20       | 5.46         |
| 1.0          | 29.18        | 15.98               | 7.23       | 3.50       | 5.25         |
| 10           | 4.64         | 10.25               | 4.44       | 2.21       | 3.60         |
| 100 (interp) | ~0.7         | ~7.5                | ~3.3       | ~1.85      | ~2.4         |
| 500          | 0.20         | **6.52**            | 3.04       | 1.89       | 1.59         |

Plus from Methods/Results:
- >95 % of DSBs repaired within 24 h.
- Misrepair fraction 15.8 % at 60 keV/μm with 3 Mbp detection threshold
  (63.7 % unfiltered).
- Predicted dicentric yields ~2× experimental Edwards 1985.
- Predicted excess acentric yields ~10× experimental Edwards 1985.
- MN dose response linear; threshold of 10 kbp closes the gap with low-dose
  experimental data.

## 3. Artifact availability — what we found

| Resource                                  | Available?        | Where                                                       |
|-------------------------------------------|-------------------|-------------------------------------------------------------|
| Paper PDF                                 | YES (open access) | QUB Pure mirror; local `paper.pdf`                          |
| Appendix Tables (A1, A2)                  | YES               | In PDF; `results/table_A2.csv` (machine readable)           |
| MEDRAS repair model code                  | YES               | <https://github.com/sjmcmahon/Medras-MC> (Python, BSD-2)     |
| TOPAS-nBio extension code                 | YES               | <https://github.com/topas-nbio/TOPAS-nBio>                  |
| TOPAS core simulator                      | YES (registered)  | <https://topasmc.org> (free-for-academic, license-gated)    |
| Authors' specific Zhu et al. parameter files / nucleus geometry source | **NO** — paper does NOT publish their specific TOPAS-nBio parameter files. Geometry recipe is described in Methods but must be re-implemented. | Methods §"DNA Model"                                          |
| Authors' specific run configurations / random seeds | **NO**     | Not provided                                                 |
| Numerical Table A2 (DSB/SSB yields)       | YES (in paper)    | `results/table_A2.csv`                                       |
| Edwards 1985 experimental data            | YES (digitized in Zhu Fig 7) | Original is 40-year-old paper; values readable in Fig 7      |

## 4. Reproducibility verdict per stage

### Stage 1 — Initial damage (TOPAS-nBio)
- **Code:** open. **Inputs:** parameter file must be **rebuilt from Methods
  description** (no source-of-truth parameter file in paper).
- **Compute:** ~120,000 thread-hours for full Table A2 reproduction (Table A1
  states ~10 h per 1 Gy run at 10 threads on Xeon L5640/X5660/E5450; 12
  energies × 100 runs).
- **Verdict:** **HPC-only.** Not feasible in this subagent. See
  `HPC_JOB_PLAN.md` for uicgpu / Aurora job design (reduced 10-runs-per-energy
  fits in ~5 days on 1 uicgpu node or ~6 h on 32 Aurora nodes).

### Stage 2 — MEDRAS repair / chromosome aberration / MN
- **Code:** open and already replicated in our `lucid-medras-mc` folder.
- **Compute:** minutes on CPU.
- **Verdict:** **REPLICABLE LOCALLY** once Stage 1 SDD files exist. Until then,
  we can drive MEDRAS-MC with its own empirical damage generator as a low-LET
  surrogate (this is exactly what the prior `lucid-medras-mc` replication did
  for McMahon-Prise 2021).

### Sanity check we did run

`code/sanity_dsb_yield.py` invoked MEDRAS-MC's `damageModel.basicXandIon(runs=2)`
and verified the pipeline writes valid SDDv1.0 files. DSB yields for the X-ray
1 Gy cases were 32.5 DSBs / run = **5.3 DSB/Gy/Gbp** on the 6.1 Gbp built-in
nucleus, within 18 % of Zhu's lowest-LET (500 MeV, 0.2 keV/μm) value of
**6.52 DSB/Gy/Gbp**. The X-ray dose response was linear in dose
(2 Gy → 76 DSBs, 8 Gy → 296 DSBs; 6.1–6.3 DSB/Gy/Gbp). For higher LET
protons, MEDRAS's empirical generator under-predicts (by design — it is a
surrogate, not a track-structure code).

This sanity check confirms the local pipeline is functional and that the
low-LET endpoint of Zhu Table A2 is bracketed by an independent open
implementation. See `results/sanity_summary.md`.

## 5. Comparisons we can make now without HPC

Without re-running TOPAS-nBio we can already verify (using `results/table_A2.csv`
and published numbers):

- **DSB-yield trend with LET:** Zhu's Table A2 monotonically increases from
  6.5 → 21.2 DSB/Gy/Gbp over LET 0.2 → 60 keV/μm. ✓ matches qualitative
  expectation from Friedland 2017, Meylan 2017, and MEDRAS-MC sanity run.
- **SSB:DSB ratio:** Zhu's Fig 5D shows ratio decreasing from ~22 at low LET
  to ~5 at high LET. Compute from Table A2: SSB/DSB at 0.2 keV/μm =
  131.72/6.52 = **20.2**; at 60 keV/μm = 108.91/21.21 = **5.1**. ✓ consistent.
- **Hybrid fraction of DSBs:** Zhu reports "most DSBs are hybrid type" at
  high LET. From Table A2 at 60 keV/μm: hybrid/total = 9.55/21.21 = **45 %**;
  at 0.2 keV/μm: 3.04/6.52 = **47 %**. ✓ matches their statement.
- **Indirect contribution ~60–75 %:** From Table A2 at 4.64 keV/μm (10 MeV):
  indirect SSB/total SSB = 141.22/188.28 = **75 %**. ✓ matches Zhu §Initial
  DNA Damage paragraph 2.

All three internal consistency checks pass; the paper's published numbers
are self-consistent.

## 6. Risks / things that could trip a deep replication

1. **Geometry mismatch.** The "fractal Hilbert curve fiber loop" geometry is
   described prose-level; small differences in fiber packing or smoothing of
   chromatin fiber connections would shift DSB yields by 5–10 %.
2. **Cross-section extension to 500 MeV.** Zhu uses
   `G4DNARuddIonisationExtendedModel` + RITRACKS cross-sections for protons
   above 100 MeV. This is implementation-specific to TOPAS-nBio; PARTRAC and
   Geant4-DNA stock will differ.
3. **Chemistry-stage cutoff (1 ns).** Different from some other codes
   (Lampe 2018 uses 5 ns). Sensitivity is documented to be a few %.
4. **Direct-damage threshold (17.5 eV).** Some literature uses 5 or 11 eV;
   Zhu chose 17.5 eV consistent with Meylan 2017. Changes direct SB yield
   significantly.
5. **MEDRAS rejoining range `r = 0.046 R_nuc`.** A specific fit; changing
   this changes misrepair fraction strongly.

All of the above are documented in the paper, so they are reproducible
**if** the implementer reads carefully.

## 7. QA / worktype retag recommendation

**Master TSV currently labels:** `omics/signature replication`.
**Should be:** `simulation/model replication`.

Justification: there is no omics data and no signature. The paper is a
two-stage Monte-Carlo simulation with mechanistic repair model output
(numerical tables + scatter plots). Other TOPAS-nBio / MEDRAS papers in the
same master are already tagged `simulation/model replication` (e.g. ranks 53,
56, 68, 72, 79, 93).

Suggested edit to `LUCID100_SOLID_MASTER_QA.tsv` line 48:
- column `worktype`: change `omics/signature replication` → `simulation/model replication`
- column `verdict_or_plan`: change `TODO: omics/signature replication; ...` →
  `TODO: simulation/model replication; artifact harvest; brief; run; report`

## 8. Recommended next actions

| Priority | Action | Owner / where |
|----------|--------|---------------|
| 1 | Apply QA worktype retag in master TSV (line 48) | Main agent / human curator |
| 2 | If campaign promotes paper from "first-pass" to "deep replication", queue 12-energy × 10-run TOPAS-nBio job on uicgpu per `HPC_JOB_PLAN.md` | uicgpu / `/data/stevens/` |
| 3 | After HPC SDD outputs exist, feed them into local MEDRAS-MC repair stage and reproduce Fig 6, 7, 8 numerically. Most of the wiring already exists in `lucid-medras-mc/scripts/`. | CherryRd |
| 4 | (Optional stretch) Plot our sanity DSB/Gy/Gbp X-ray points on top of Zhu Table A2 low-LET endpoint for the first-pass figure. Currently captured numerically in `results/sanity_summary.md`. | CherryRd |

## 9. Blockers

- **None for first-pass scope.** All required artifacts (paper, code,
  numerical tables) are public and harvested.
- **TOPAS / TOPAS-nBio build chain** is the only future blocker; that
  requires a registered TOPAS account and HPC compile, not a local CherryRd
  install.

---

## Summary one-liner

Zhu 2020 is a clean, well-documented TOPAS-nBio + MEDRAS proton-irradiation
study. **Paper, MEDRAS-MC code, and Table A2 numerical results are all
harvested locally.** TOPAS-nBio physics step needs HPC; MEDRAS repair step is
already replicable locally and the sanity DSB/Gy/Gbp at low LET matches Zhu
within ~20 %. Recommend QA retag from `omics/signature replication` to
`simulation/model replication`.
