# LUCID100 slot 4 — Stochastic multicellular modeling of x-ray irradiation, DNA damage induction, DNA free-end misrejoining and cell death

## Full citation

Forster, J. C., Douglass, M. J. J., Phillips, W. M., & Bezak, E. (2019).
**Stochastic multicellular modeling of x-ray irradiation, DNA damage induction, DNA free-end misrejoining and cell death.**
*Scientific Reports* 9: 18888.
DOI: <https://doi.org/10.1038/s41598-019-54941-1>
Open Access (CC BY 4.0). Corresponding author: `Jake.Forster@sa.gov.au`.

Wave-1 master entry: rank 35, tier A, priority score 20, themes
"DNA repair / DDR; radiation quality / RBE; computational model / simulation",
worktype "simulation/model replication".

## Source links

- HTML: <https://www.nature.com/articles/s41598-019-54941-1>
- PDF: <https://www.nature.com/articles/s41598-019-54941-1.pdf>
- Supplementary methods (P_surv derivation):
  <https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-019-54941-1/MediaObjects/41598_2019_54941_MOESM1_ESM.pdf>
  (saved locally as `supplementary_methods.pdf`)

## Code / data / supplement availability

| Item | Status | Detail |
|---|---|---|
| Code repository (Geant4 application) | **NOT PROVIDED** | Paper has no "Code Availability" section. The Geant4 / Geant4-DNA application is "developed in-house". |
| Data repository (DSB / cDSB lists, voxel arrays) | **NOT PROVIDED** | Paper has no "Data Availability" section. |
| Supplementary materials | **AVAILABLE** | One PDF (`Supplementary Methods`) deriving Eq. 9 by enumeration. No tables/data. |
| Upstream DNA damage induction algorithm | Described in Forster et al. 2018, *Radiat Res* 190(3): 248-261, DOI 10.1667/RR15050.1 — also no public code |
| Upstream HNSCC oxygenation / angiogenesis model | Described in Forster et al. 2017, *Sci Rep* 7: 11037, DOI 10.1038/s41598-017-11444-1 — also no public code |

The authors were **not contacted** (per replication-pass instructions).

## Target claims / figures

The paper has 13 figures and 6 tables. The primary quantitative claims, in order of replication priority:

1. **Tables 3-5 (sensitivity analysis).** For (DSB yield 30.1 /cell/Gy, r0 = 0.7 µm, P_nlmr = 0.5, full oxia):
   - α_mr ≈ 0.02 Gy⁻¹, β_mr ≈ 0.37 Gy⁻² (Eq. 13)
   - α_killing(mr) ≈ 0.02 Gy⁻¹, β_killing(mr) ≈ 0.17 Gy⁻² (Eq. 15)
   - SF2(mr) ≈ 0.49 (full oxia) / 0.94 (anoxia)
   - OER_killing(mr) ≈ 3.4

2. **Table 6 (impact of indirect effect).** Removing •OH radical pathway drops the DSB yield to ~1/3 and the cDSB yield to ~1/10 of full-chain values.

3. **Figures 8, 10, 13 (distributions).** Mean and frequency distributions of DSBs, cDSBs, misrejoinings and P_surv across 1224 cells (and 135 306 cells in the 1 mm³ HNSCC tumour) for 1 Gy dose.

4. **Headline conclusion.** The linear component of cell killing by same-primary misrejoining (α_killing(mr) ≈ 0.02 Gy⁻¹) is ~15× smaller than the typical empirical HNSCC α (~0.3 Gy⁻¹), implying that **other mechanisms** (terminal deletions, incomplete exchanges) dominate the linear part.

## Acceptance criteria (this replication pass)

The full Geant4 / Geant4-DNA / pO2 / multicellular pipeline cannot be re-run without (a) the authors' in-house code, (b) ~20 000 core-hours on an HPC, and (c) a 6 MV linac spectrum from a Pinnacle treatment planning system. Therefore the realistic acceptance bar for an artifact-harvest pass is:

- **Smoke test (PASS):** independently reimplement the downstream maths (Eqs. 1, 8-10, 13-16) in pure Python, fed by the paper-reported per-Gy DSB / cDSB yields, and reproduce α_mr, β_mr, α_killing, β_killing and SF2 from Tables 3-5 within ±25 % at baseline and the correct monotonic trends across the r0 and P_nlmr sweeps.
- **Stretch (out of scope this pass):** rebuild the Geant4-DNA track + voxelised-tumour chain. Requires a multi-node HPC allocation and a manual reimplementation of the DNA damage induction algorithm.

## Artifact harvest checklist

- [x] Source PDF saved locally
- [x] Full text extracted (`paper.txt`)
- [x] Supplementary methods downloaded + extracted (`supplementary_methods.pdf`)
- [x] No code repository exists (verified by absence of Code Availability statement)
- [x] No public data accession (verified by absence of Data Availability statement)
- [x] Environment plan written (pure Python + numpy; no Geant4 needed for smoke test)
- [x] Acceptance metrics defined (above)
- [x] Blockers listed (see `FIRST_PASS_REPORT.md`)

## Execution checklist

- [x] Smoke test / minimal calculation — **PASS** (see `FIRST_PASS_REPORT.md`)
- [ ] Main replication run (Geant4-DNA chain) — **not feasible on CherryRd**; job plan only
- [x] Figures/tables comparison done — Tables 3, 4, 5 baseline reproduced; Fig. 8C/D shape confirmed
- [x] Logs, hashes, environment captured (`MANIFEST.md` in workspace mirror)
- [x] `FIRST_PASS_REPORT.md` written
- [x] Progress JSON updated under OpenClaw memory

## Workspace mirror

All non-Dropbox artifacts (paper text, smoke-test code, results JSON, hashes)
live in the OpenClaw workspace at:

`/Users/stevens/.openclaw/workspace/lucid-replications/slot4-stochastic-multicellular/`

with subdirectories:

- `artifacts/` — paper.pdf, paper.txt, supp1.pdf, supp1.txt, SHA1SUMS
- `code/smoke_test.py` — independent Python reimplementation
- `results/smoke_test_results.json`, `results/smoke_test_summary.txt`
- `MANIFEST.md` — artifact manifest with sources and hashes

## Abstract / notes

The repair or misrepair of DNA double-strand breaks (DSBs) largely determines whether a cell will survive radiation insult or die. A new computational model of multicellular, track structure-based and pO2-dependent radiation-induced cell death was developed and used to investigate the contribution to cell killing by the mechanism of DNA free-end misrejoining for low-LET radiation. A simulated tumor of 1224 squamous cells was irradiated with 6 MV x-rays using the Monte Carlo toolkit Geant4 with low-energy Geant4-DNA physics and chemistry modules up to a uniform dose of 1 Gy. DNA damage including DSBs were simulated from ionizations, excitations and hydroxyl radical interactions along track segments through cell nuclei, with a higher cellular pO2 enhancing the conversion of DNA radicals to strand breaks. DNA free-ends produced by complex DSBs (cDSBs) were able to misrejoin and produce exchange-type chromosome aberrations, some of which were asymmetric and lethal.
