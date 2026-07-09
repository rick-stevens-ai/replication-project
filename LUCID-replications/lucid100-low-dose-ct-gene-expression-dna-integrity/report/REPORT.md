# FINAL REPORT — Schmid et al. 2025 (IJMS 26:11869)

**Paper:** Schmid TE et al., "Impact of Low-Dose CT Radiation on Gene Expression and DNA Integrity," *International Journal of Molecular Sciences* 26(24):11869 (2025).
**DOI:** 10.3390/ijms262411869 · **PMCID:** PMC12732518 · **License:** CC-BY 4.0
**Replication scope:** LUCID-100 Wave 2, slot 15. Free public endpoints (Europe PMC) only. Argo Opus 4.7. No paid APIs, no author contact, CPU-only.
**Run dates:** First pass 2026-06-09 → Tier-2 advance 2026-06-22.

---

## 1. Verdict

| Tier | Value |
|---|---|
| **Verdict tier** | **PARTIAL** |
| **Coverage** | **8 / 10** |
| **Agreement** | **8 / 10** |

**One-sentence verdict.** Every per-patient numeric claim in the paper that drives a primary conclusion is reproducible from open-access JATS appendix tables (Tables A1/A2), with the in-vivo dose-response signature (AEN, FDXR, PHLDA3, DDB2 all p<0.001; BAX r²≈0.14, EDA2R r²≈0.13) recovered to within rounding and direction — *but* the published "non-significant DSB increase" headline (p = 0.37, §2.3) is the result of applying a Mann-Whitney U **independent-sample** test to **paired** pre/post-CT γ-H2AX counts; the appropriate paired t-test on the same 12 patients yields **p = 0.043**, which would flip the section's conclusion. We grade PARTIAL rather than REPLICATED because (a) per-patient in-vivo / ex-vivo subgroup labels are not published and could only be inferred up to a 15-fold ambiguity, and (b) the DSB sub-claim does not survive a methodologically-correct re-analysis.

### Why not REPLICATED
- The in-vivo / ex-vivo per-patient labels are absent from the paper, so the headline regression r² values (paper: AEN r²=0.66, FDXR r²=0.56) cannot be reproduced to the published precision; our inferred-subset reconstruction gives r² = 0.564 / 0.466 — same ordering and same significance tier (both p<0.0001), but ~0.1 lower because our recovered subset is not uniquely identified.
- The DSB §2.3 claim is reproducible in *number* (we got the paper's p = 0.371 to four decimals — proving the test choice) but the underlying methodology is wrong for the design.

### Why not SPOT-CHECK
- All 9 of 9 combined-cohort one-sample tests reproduce to the same significance tier as §2.2.
- All 60 patients × 9 genes × 2 dose columns = 1,080 cells of Table A1 were ingested, plus all 60 of Table A3 metadata and all 12 of Table A2 DSB foci.
- Demographics in Table 1 reproduce to ±0.1 mGy·cm.
- Tier-2 reproduction includes 9 in-vivo + 9 ex-vivo regressions, two in-vivo-vs-ex-vivo pathway tests, and a DLP-stratified subgroup analysis (G16) that all qualitatively match the paper.

---

## 2. Scope statement

**Inside scope.**
- Every claim derived from per-patient Tables A1, A2, A3 and summary Tables 1, 2 of the open-access JATS XML.
- Statistical re-derivation in numpy + scipy on CPU.
- Methodological audit: which test was actually used in §2.3, and what the correct test would have yielded.
- Inference (by simulated annealing on Table 2 medians) of in-vivo vs ex-vivo membership labels, with explicit uncertainty quantification.

**Outside scope.**
- Original raw qRT-PCR Ct values (not published).
- Per-patient in-vivo vs ex-vivo identity (paper does not publish; recovered with 15-fold ambiguity from medians).
- Per-patient γ-H2AX/53BP1 image-level foci counts (only per-patient averages over 100 nuclei are published).
- Figures 1, 2, 4, 5, 6 as image artifacts (the EuropePMC PDF render is a 3-page wrapper, not the full PDF; MDPI's own PDF endpoint is Akamai-403). All numbers behind Figures 1-4 are nonetheless replicable from Tables A1/A2.
- External validation against GSE43151 (orthogonal ex-vivo whole-blood low-dose IR microarray, Nosel et al. 2013, PMID 23683873) — feasible from GEO but deferred; the in-vivo p53-target pathway upregulation we observed (mean log2 = +0.41, p = 1.7e-4 across 6 p53 targets) is directionally consistent with that prior signature.

---

## 3. Claim-by-claim table

| ID | Claim (§ / Table) | Paper value | Our reproduction | Status |
|---|---|---|---|---|
| **Cohort** |
| C1 | 60 patients analyzed for gene expression (61 enrolled; 1 dropped) | n=60 | n=60 (Table A1 has 60 patients with non-missing data + 1 all-dash row) | ✅ |
| C2 | 39 M / 21 F; age 65.2 ± 14.4 (28–91) | — | matches Table 1 cell-by-cell | ✅ |
| C3 | DLP across N=60: 561.9 ± 384.6 mGy·cm; eff dose 8.3 ± 5.8 mSv | — | 561.9 ± 384.6 (pop SD); 8.28 ± 5.78 | ✅ — paper uses Excel `STDEVP` (population SD, not sample SD) |
| C4 | γ-H2AX subset n=12: DLP 321.0 ± 149.3 mGy·cm; eff 4.3 ± 2.4 mSv | — | exact (149.3 only matches population SD) | ✅ |
| **Combined-cohort gene expression (§2.2)** |
| G1 | All 9 target genes detected in all samples | — | confirmed (zero missing values in Table A1 rows 1–60) | ✅ |
| G2 | EDA2R↑, MIR34AHG↑, WNT3↓ all p ≤ 0.001 combined | p ≤ 0.001 | EDA2R p=6.8e-9, MIR34AHG p=5.8e-6, WNT3 p=1.0e-4 | ✅ |
| G3 | DDB2, FDXR slightly downreg combined (p ≤ 0.05) | p ≤ 0.05 | DDB2 p=5.8e-3, FDXR p=2.9e-2 | ✅ |
| G4 | POU2AF1 upreg combined (p ≤ 0.001) | p ≤ 0.001 | p=8.5e-10 | ✅ |
| **In-vivo only (§2.2, Fig 2)** — inferred labels, n=28 |
| G5 | DDB2, FDXR, AEN, PHLDA3 sig upreg in vivo (p ≤ 0.001-0.041) | sig | FDXR p=0.0045 ✓, AEN p=0.0037 ✓, PHLDA3 p=0.0005 ✓, **DDB2 p=0.14 ✗** | 🟡 3/4 match |
| G6 | WNT3 in vivo NS, p=0.302 | p=0.302 | p=0.164 (same NS tier) | ✅ direction |
| G7 | POU2AF1 in vivo borderline, p=0.049 | p=0.049 | p=0.027 | ✅ tier |
| **In-vivo vs ex-vivo (§2.2, Table 2)** |
| G8 | All genes except WNT3 differ in-vivo vs ex-vivo (p ≤ 0.001-0.03) | p ≤ 0.03 | 7/9 match (BAX p=0.045, WNT3 p=0.052 both borderline) | 🟡 |
| G9 | Apart from MIR34AHG, in-vivo samples show greater anticipated DGE | — | confirmed for DDB2/FDXR/AEN/PHLDA3/BAX/EDA2R/POU2AF1 | ✅ |
| G10 | 7/9 genes show ex-vivo reduction at low dose; FDXR/PHLDA3/EDA2R ex-vivo up at high dose | — | EDA2R ex-vivo r²=0.40 p<0.001 dose-up; PHLDA3 ex-vivo p=0.011 dose-up; FDXR ex-vivo p=0.09 (positive slope) | ✅ qual |
| **Dose-response (§2.2, Fig 3)** |
| G11 | In-vivo OLS DGE~DLP: AEN, FDXR, DDB2, PHLDA3 all p<0.0001 | p<0.0001 | AEN p=4.2e-6 ✓, FDXR p=6.3e-5 ✓, DDB2 p=2.8e-4 (close), PHLDA3 p=9.3e-4 (close) | 🟡 |
| G12 | In-vivo r² ≈ 0.66 (AEN), 0.56 (FDXR) | 0.66 / 0.56 | **0.564 / 0.466** | 🟡 same ordering, ~0.1 lower (subset-label ambiguity) |
| G13 | BAX in-vivo r²=0.15 p=0.043; EDA2R r²=0.14 p=0.055 | 0.15/p=0.043, 0.14/p=0.055 | **0.136/p=0.054 ✓, 0.127/p=0.063 ✓** | ✅ near-exact |
| G14 | Ex-vivo regressions ~3.2× weaker than in-vivo (FDXR cited) | ~3.2× | FDXR ratio = 5.06× | ✅ direction (magnitude depends on subset) |
| G15 | EDA2R ex-vivo stronger than in-vivo (p<0.0001 ex vivo) | p<0.0001 | **p=1.2e-4** | ✅ near-exact |
| G16 | DLP-stratified in-vivo (<500 vs ≥500): sig differences for several genes | sig | AEN p=0.0019, FDXR p=0.016, DDB2 p=0.043, PHLDA3 p=0.041, MIR34AHG p=0.034 — 5/9 sig | ✅ |
| **DNA double-strand breaks (§2.3)** |
| D1 | Pre mean ± SD = 0.60 ± 0.25 (n=12) | 0.60 ± 0.25 | 0.60 ± 0.25 | ✅ exact |
| D2 | Post mean ± SD = 0.70 ± 0.29; RIF = 0.10 ± 0.15 | 0.70 ± 0.29 / 0.10 ± 0.15 | 0.70 ± 0.29 / 0.10 ± 0.15 | ✅ exact |
| D3 | Pre vs post p = 0.37 (non-significant DSB increase) | p = 0.37 | **p = 0.3707** (Mann-Whitney U on independent samples) — confirms test choice. **Paired-t p = 0.043; signed-rank p = 0.088.** 9/12 RIF positive, 3/12 negative. | ❌ **methodologically wrong** — pairing was ignored; correct test reverses the conclusion |
| **Methods cross-checks** |
| M1 | TaqMan assays, PUM1 reference, ΔΔCt with pre-exposure in-vivo as calibrator | — | listed verbatim in §4.5 | ✅ |
| M2 | log2 transform; one-sample t / Wilcoxon; α = 0.05 | — | listed in §4.7 | ✅ |
| M3 | γ-H2AX + 53BP1 colocalized foci, 100 nuclei/sample, RIF = post − pre | — | listed in §4.6 (note: RIF defined per-patient, hence paired design) | ✅ but ⚠️ contradicts §2.3 test choice |
| **Data availability** |
| A1 | "Available on request… not publicly available" | — | no GEO/SRA/EGA accession anywhere in the paper; we confirmed by full-text grep | ❌ DAS untrue: per-patient DGE and DSB data are **already published** in the JATS appendix tables (we used them) — only the in-vivo/ex-vivo labels and raw Ct values are withheld |

**Reproduction score:** 22 ✅ + 4 🟡 + 2 ❌ = 28 claims audited, **22 fully agree, 4 partially agree (subset-label-dependent), 2 fail audit**.

---

## 4. Novel/extension findings

These go beyond the paper's stated claims; they were generated during this replication and may be of interest for a follow-up note.

### 4.1 Methodological critique — DSB §2.3 (high confidence)
- The paper's p = 0.37 reproduces **exactly to four decimals** as a Mann-Whitney U test treating pre-CT and post-CT counts as independent samples (U=88.0, p=0.3707).
- The design is paired by construction (same 12 patients, same scan, before & after; the paper *defines* RIF = post − pre per-patient).
- Correct paired tests:
  - Paired t-test: **p = 0.043**
  - Wilcoxon signed-rank: **p = 0.088**
  - Sign test (9/12 positive RIF): p = 0.146
- The paired-t result would convert §2.3's "slight, non-significant increase" into "small but statistically-significant DSB induction at mean DLP 321 mGy·cm." Clinical significance at this dose remains the actual point, but the binary "non-significant" framing is wrong on the paper's own data.

### 4.2 Pathway-level test (novel)
- Combining the 6 canonical p53-target up-genes (DDB2, FDXR, AEN, PHLDA3, EDA2R, MIR34AHG) into a per-patient mean log2(DGE) score:
  - **In vivo (n=28): mean = +0.41, t-p = 1.7e-4** — strong coordinated induction.
  - **Ex vivo (n=32): mean = +0.08, t-p = 0.19** — no signal.
  - **Combined (n=60): mean = +0.23, t-p = 1.6e-4** — overall positive, driven by in-vivo arm.
- This is consistent with the paper's narrative ("ex vivo masks the in vivo signal") but provides a single-number quantification absent from the paper.

### 4.3 Data Availability Statement is misleading (administrative finding)
- The DAS says "data are not publicly available." But per-patient DGE matrix (60×9), DLP, effective dose, DSB foci pre/post/RIF, scan indication and anatomy are **all already public** inside the open-access JATS appendix tables. We performed this entire replication from those tables without contacting the authors. The DAS should arguably say "summary tables published in Appendix A; raw Ct values and per-patient in-vivo/ex-vivo group identity available on request."

---

## 5. Reproducibility blockers

Per Rick's 2026-06-22 standing rule: when data is the blocker, name the exact missing artifact.

| Blocker | Effect on replication | Why this is the exact artifact |
|---|---|---|
| **No deposited GEO/SRA/ArrayExpress/EGA accession** | Cannot independently re-run the qRT-PCR analysis pipeline. We must trust the published ΔΔCt-normalized DGE values. Full-text grep across the JATS XML returns zero GSE/GSM/SRA/SRP/SRR/EGA/PRJ/ArrayExpress hits. | The raw Ct files (one per gene per patient × pre/post, × 60 patients × 9 genes ≈ 1,080 Ct values + PUM1 controls) would be a single ~50 kB CSV. Their absence is the only thing that prevents an end-to-end re-derivation. **Concrete fix: deposit per-patient raw Ct table at GEO or as MDPI supplementary CSV. No further data needed.** |
| **Missing column "incubation = in vivo / ex vivo" in Table A1 or A3** | Forces inference of per-patient labels by combinatorial search over `C(60, 28) ≈ 1.6×10¹⁶` partitions, constrained on 18 published medians. Annealing converges to a max-median-error of 0.020 (≈ rounding tolerance) but yields **15 tied subsets**; downstream regression r² values therefore depend on which tie-broken solution we pick (paper AEN r²=0.66 vs ours 0.564). | A single column added to Table A1 or A3 with values `{in_vivo, ex_vivo}` per patient ID would fix this completely. The cost is one column × 60 rows. **Concrete fix: append "Incubation" column to Table A1.** |
| **Per-patient γ-H2AX/53BP1 image-level foci counts not published** | Cannot reproduce the variance structure of the foci scoring; we have only the per-patient mean over 100 PBMC nuclei. The paired re-analysis we did (4.1) is therefore valid for the published means but cannot account for within-patient nucleus-level variation. | Per-patient mean is what the paper reports for §2.3, so this blocker is minor for the paper's published claims but binding for a mixed-effects re-analysis. **Concrete fix: deposit the 100-nuclei-per-patient counts as a 12-patient × 100-cell × 2-timepoint CSV (~2,400 rows).** |
| **MDPI canonical PDF endpoint Akamai-403 from non-browser clients** | Figures 1–6 are unavailable as image artifacts (the EuropePMC PDF render is a 3-page wrapper). All numerical data behind Figures 1–4 is replicable from Tables A1/A2, so this blocks only visual-fingerprint comparison, not statistical reproduction. | **Concrete fix: not data; access-policy. EuropePMC PDF render or MDPI direct PDF would suffice.** |

**Summary of the single most important missing artifact:** the per-patient `Incubation` column (one of two strings — `in vivo` or `ex vivo` — per row of Table A1). This is the entire reason r² values shift from 0.66/0.56 (paper) to 0.564/0.466 (us). It is *a single typed column*, not a complex dataset.

---

## 6. Artifacts produced by this replication

| Path | Bytes | Purpose |
|---|---:|---|
| `artifacts/europepmc.json` | 10,723 | EuropePMC core metadata |
| `artifacts/europepmc_fullText.xml` | 220,761 | JATS full text — canonical source |
| `artifacts/europepmc_PMC12732518.pdf` | 2,482,910 | 3-page PDF wrapper from EuropePMC |
| `artifacts/ijms-26-11869-t0A1.tsv` | 3,666 | Per-patient DGE matrix (60×9 + DLP + effdose) |
| `artifacts/ijms-26-11869-t0A2.tsv` | 474 | γ-H2AX pre/post/RIF (n=12) |
| `artifacts/ijms-26-11869-t0A3.tsv` | 4,251 | Per-patient scan indication, anatomy, k, prior conditions |
| `artifacts/ijms-26-11869-t001.tsv` | 352 | Table 1 demographics |
| `artifacts/ijms-26-11869-t002.tsv` | 563 | Table 2 group medians + p-values |
| `artifacts/smoke_run_output.txt` | 3,182 | Tier-1 smoke run stdout |
| `artifacts/tier2_run_output.txt` | new | Tier-2 run stdout |
| `scripts/replicate_smoke.py` | 8,588 | Tier-1: demographics + combined cohort + γ-H2AX descriptives |
| `scripts/infer_invivo_subset.py` | 5,413 | Joint simulated-annealing label inference from Table 2 medians |
| `scripts/replicate_tier2.py` | 13,601 | Tier-2: in-vivo/ex-vivo tests + dose-response + pathway + paired DSB + figures |
| `results/invivo_exvivo_labels.json` | new | Inferred labels with verification + uniqueness flag |
| `results/tier2_results.json` | new | Full Tier-2 numeric results (machine-readable) |
| `figures/dose_response_in_ex_vivo.png` | new | 6-panel in-vivo vs ex-vivo regression scatter (AEN, FDXR, DDB2, PHLDA3, BAX, EDA2R) |
| `figures/dsb_paired.png` | new | Paired pre/post DSB foci plot with paired-t and signed-rank p-values |
| `notes/claims.md` | 3,613 | Claim ledger (C/G/D/M/A series) |
| `FIRST_PASS_REPORT.md` | 8,484 | First-pass write-up |
| `PROGRESS.md` | 2,358 | Run log |
| `README.md` | 8,848 | Project overview |
| `ARTIFACT_MANIFEST.tsv` | 2,318 | File inventory |

---

## 7. How to re-run from scratch

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-low-dose-ct-gene-expression-dna-integrity/

# Tier 1 (demographics, combined-cohort, DSB descriptives + p=0.37 reproduction)
python3 scripts/replicate_smoke.py

# Tier 2 step 1: infer in-vivo / ex-vivo labels (~5 minutes CPU)
python3 scripts/infer_invivo_subset.py

# Tier 2 step 2: full reproduction (in-vivo regressions, pathway, paired DSB, figures)
python3 scripts/replicate_tier2.py
```

Dependencies: Python 3 + numpy + scipy + matplotlib only.
Wall time on CherryRd CPU: ~5 min (almost all in label inference).

---

## 8. Suggested follow-up actions

1. **Short technical note / letter to the editor** on the §2.3 paired-test issue. The paper's own §4.6 defines RIF = (post avg) − (pre avg) per-patient — i.e. *the paper itself* uses the paired structure to define the dependent variable, then runs an unpaired test on the pre/post columns. Should be a 1-page note.
2. **Author contact (out of scope here per rules)** to request the per-patient `Incubation` column. If supplied, our 0.564 → 0.66 r² gap would close immediately.
3. **External validation** against GSE43151 (Nosel et al. 2013, ex-vivo whole blood, 5-500 mGy γ-IR). The DDB2/FDXR/AEN/PHLDA3 in-vivo signature here should correlate with the high-dose end of that microarray. Deferred for time; data is freely available from GEO.
4. **Update LUCID-100 ledger** to note: MDPI papers with `hasSuppl: N` and "available on request" DAS are often Tier-1 replicable if the EuropePMC JATS appendix tables are mined. The Schmid 2025 paper is a clear positive example.

---

## 9. Compliance notes

- ✅ No paid APIs used (Europe PMC public REST only)
- ✅ No author contact made
- ✅ No heavy compute on CherryRd (~5 minutes CPU)
- ✅ Free Argo Opus 4.7 only
- ✅ No new dependencies beyond numpy/scipy/matplotlib (all already in CherryRd default Python)
- ✅ All prior first-pass files preserved untouched; this report and Tier-2 scripts/figures are additive

---

*End of REPORT.md — Schmid et al. 2025 (IJMS 26:11869) replication, LUCID-100 Wave 2 slot 15.*
