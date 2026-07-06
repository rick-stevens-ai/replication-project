# SPOT-CHECK Promotion Assessment — Batch 2

**Date:** 2026-06-25
**Auditor:** Ollie subagent (Claude Opus 4.7 via Argo)
**Scope:** 13 replication slots (7 LUCID, 1 PDE, 5 BVBRC) judged for promotion potential beyond SPOT-CHECK.

Promotion verdicts:
- **PROMOTABLE→PARTIAL** = realistic path to PARTIAL exists with bounded, locally-feasible additional work.
- **PROMOTABLE→REPLICATED** = realistic path to full REPLICATED (≥80% scope + ≥80% claim agreement) with bounded work.
- **CEILING-SPOTCHECK** = SPOT-CHECK is the honest ceiling; data is permanently unavailable, proprietary code blocks the path, or the paper is review/concept with no quantitative target.

---

## One-liners

```
lucid100-cho-low-dose-rate-dna-repair-deficient: CEILING-SPOTCHECK — closed Elsevier BBRC + zero data deposit; no path without paper PDF + author spreadsheets.
lucid100-flash-oxygen-repair-mechanistic-model: CEILING-SPOTCHECK — Elsevier paywall + UNIVERSE engine never released across 4+ Liew/Mairani papers; structural block.
lucid100-neutron-rbe-pre-post-dna-repair: PROMOTABLE→PARTIAL — author code is open MIT; pull Zenodo Data.zip (690 MB) + clusterer sweep unblocks C1–C3/C5/C7 without TOPAS rerun.
lucid100-intensity-modulated-protective-doserate: PROMOTABLE→PARTIAL — OA paper + Table 1 in hand; implement full IMK with intercellular term + WebPlotDigitizer Figs 2/3 → quantitative comparison feasible locally.
lucid100-arabidopsis-aox1a-gamma-irradiation: CEILING-SPOTCHECK — closed T&F paper, no public deposit, AS-12/XX-2 lines lab-internal (Komi/Syktyvkar), wet-lab only.
lucid100-stochastic-nhej-track-structure-2010: CEILING-SPOTCHECK (unless library pull) — BioOne paywall blocks 4-scenario parameters; ANL/UIC library pull would unlock PARTIAL.
lucid100-multiscale-uhdr-survival-model: PROMOTABLE→PARTIAL (already PARTIAL) — already PARTIAL per report (cov=5/agr=4); to REPLICATED needs author Julia + TRAX-CHEM spectra + raw clonogenic (3 missing artifacts, author contact required).
fipy-wave4: PROMOTABLE→REPLICATED — FiPy is open NIST code; just add 2D phase-field + Neumann/periodic BCs + self-reference convergence study (~1 day work, all local).
BVBRC-16-Efaecium-probiotic-genome-factors-2018: PROMOTABLE→REPLICATED — all genomes public in BV-BRC; rerun Roary + ResFinder + VFDB + ISEScan (~24 CPU-h local).
BVBRC-17-Ecoli-B2-IBD-metabolic-2018: PROMOTABLE→REPLICATED — 5,737 E. coli genomes public, GEMs in BiGG; rerun pan-genome + COBRApy FBA on mucus glycans (~1–2 weeks).
BVBRC-18-Marine-Streptomyces-BGC-2019: PROMOTABLE→PARTIAL — corpus available; rerun antiSMASH + GET_HOMOLOGUES on 87-strain list from Supp Table S1 (~16 CPU-cores × 1 week).
BVBRC-19-Propionibacterium-pangenome-metabolic: PROMOTABLE→PARTIAL — all 5 species public + GEM in paper supplement; rerun ModelSEED + COBRApy FBA (~2 weeks local).
BVBRC-11-VREfm-LatAm-Rios2020: PROMOTABLE→REPLICATED (already PARTIAL) — pass-2 already at cov=12/agr=10; BEAST MCMC for time-tree claims C10–C13 + curated virulence reference set → REPLICATED.
```

---

## Detailed rationale per slot

### LUCID — closed-access / data-blocked cluster

**lucid100-cho-low-dose-rate-dna-repair-deficient — CEILING-SPOTCHECK**
- Blocker: closed-access Elsevier BBRC (DOI 10.1016/j.bbrc.2024.149539), no PMC, no preprint, no CSU thesis copy. Zero data deposit in GEO/SRA/Zenodo/Figshare/OSF/Dryad/Mendeley.
- 5/8 claims are wet-lab-only (cell cycle, γ-H2AX foci, growth curves, cross-agent panel, panel composition); even with the paper text these need author source-data spreadsheets that don't exist publicly.
- The 3 directionally-tested claims (C1–C3) cannot be numerically verified without the paper's α/β tables. Author contact would in principle unlock data — but that's outside policy.
- Verdict: honest SPOT-CHECK ceiling.

**lucid100-flash-oxygen-repair-mechanistic-model — CEILING-SPOTCHECK**
- Blocker: Elsevier IJROBP paywall (paper + supplement with per-endpoint g_ROD, τ_reox, K_iDSB, K_cDSB, repair half-lives). UNIVERSE engine source never released by Liew/Mairani lab across 2019/2020/2021/2022 publications — this is a structural pattern, not a fixable gap.
- The smoke is mechanism-faithful from open predecessors but cannot be tuned to paper's headline numbers without the closed parameter tables.
- No path to PARTIAL without library/institutional pull of the paywalled supplement.
- Verdict: honest SPOT-CHECK ceiling.

**lucid100-neutron-rbe-pre-post-dna-repair — PROMOTABLE→PARTIAL**
- Paper is OA (IOP CC-BY); author code is open MIT on Zenodo (DOI 10.5281/zenodo.17087505). Blocker is purely compute + 690 MB Data.zip not yet downloaded.
- Promotion path: (1) pull `zenodo:17087505/Data.zip` (~690 MB) to HPC; (2) run shipped `ComplexDSbCounter.py::clusterer` with eps sweep on real SDD files — unblocks C1–C3, C5, C7 without TOPAS rerun. (3) For C4 (DaMaRiS misrepair) need ~25k CPU-h on HPC with TOPAS-nBio v1.0 build — feasible but heavier.
- PARTIAL is bounded: ~1 day to set up + 1 week of CPU. REPLICATED needs ~50k CPU-h on HPC.

**lucid100-intensity-modulated-protective-doserate — PROMOTABLE→PARTIAL**
- Paper is OA (Sci Rep CC-BY); Table 1 already transcribed; full IMK model published.
- Current SPOT-CHECK is acute-LQ limit only (omits intercellular communication term α_b, β_b, δ which dominates real survival).
- Promotion path: (1) Implement full IMK with dose-rate convolution + α_b/β_b/δ from Matsuya 2017/2018; (2) WebPlotDigitizer digitize Fig 2/3 survival curves; (3) chi-square fit. All local, ~2–3 days.
- C3 (γH2AX foci) still wet-lab-blocked but doesn't block PARTIAL.

**lucid100-arabidopsis-aox1a-gamma-irradiation — CEILING-SPOTCHECK**
- Closed T&F paper (no OA, no PMC). No GEO/SRA/ArrayExpress/BioStudies deposit (qPCR + biochem study).
- AS-12 / XX-2 transgenic lines are lab-internal at Komi/Syktyvkar; not in ABRC/NASC stock; wet-lab re-execution requires MTA + 200 Gy γ-facility.
- 6/8 claims are wet-lab biochemistry/phenotype that cannot be replicated from any public artifact.
- The lateral GSE112773 scaffold cross-check is the maximum tractable test; even that is qualitatively mixed (C8 partially contradicted).
- Verdict: honest SPOT-CHECK ceiling.

**lucid100-stochastic-nhej-track-structure-2010 — CEILING-SPOTCHECK (conditional)**
- Paper is BioOne-paywalled with no PMC, no preprint. 4-scenario parameter table, per-dose mis-rejoin numbers, and fast/slow time constants all locked behind paywall.
- **CONDITIONAL PROMOTABLE→PARTIAL** if ANL or UIC library can pull the PDF — then extract parameters and re-run. Otherwise CEILING.
- PARTRAC track-structure input is also unavailable as a free public download; uniform-sampling substitute is the structural ceiling without TOPAS-equivalent setup.
- Default verdict: SPOT-CHECK ceiling unless library access materializes.

**lucid100-multiscale-uhdr-survival-model — ALREADY PARTIAL; PROMOTABLE→REPLICATED (author-dependent)**
- Note: this report is already labeled **PARTIAL** (cov=5/10, agr=4/10), not SPOT-CHECK. Chemistry signature reproduced at 42/42 cells.
- Promotion to REPLICATED needs 3 named missing artifacts: (1) TRAX-CHEM per-event specific-energy spectra (upstream Trento Boscolo MC); (2) authors' Julia source for MS-GSM²; (3) raw per-replicate clonogenic counts for Adrian 2020 / Tessonnier 2021 / Tinganelli 2022a.
- All 3 require author contact — outside policy. Without them, PARTIAL is the ceiling.

### PDE

**fipy-wave4 — PROMOTABLE→REPLICATED**
- FiPy is open-source NIST software (public domain). Paper is the FiPy method paper itself.
- Current SPOT-CHECK only runs 1D linear diffusion against erfc reference (~1% interior agreement, plateau-limited by finite-domain boundary mismatch, not solver defect).
- Promotion path (all local, ~1 day):
  1. Add a 2D phase-field demo (FiPy's headline NIST use case) per the FiPy gallery.
  2. Add Neumann/periodic BC variants.
  3. Replace the erfc reference with a high-resolution self-reference for the convergence study — this would close out the "plateau at nx=200" complaint and demonstrate proper h-convergence.
- Nothing is data-blocked, nothing requires external compute. This should not have stayed at SPOT-CHECK.

### BVBRC — all OA papers, all data in BV-BRC

**BVBRC-16-Efaecium-probiotic-genome-factors-2018 — PROMOTABLE→REPLICATED**
- OA paper; both 17OM39 (GCF_001652715.1) and T110 comparator (GCA_000737555.1) public in BV-BRC.
- Promotion path (~24 CPU-h local on CherryRd):
  - C3 (AMR): rerun ResFinder + CARD on all comparator genomes.
  - C4 (virulence): VFDB BLAST on all genomes.
  - C5 (MGE): ISEScan + transposon annotation across all 4+ genomes.
  - C6 (phylogeny): Roary core-genome alignment + FastTree.
- All free, all open, all locally feasible.

**BVBRC-17-Ecoli-B2-IBD-metabolic-2018 — PROMOTABLE→REPLICATED**
- OA paper; 5,737 complete E. coli genomes in BV-BRC, 50× the 2018 corpus; canonical B2/AIEC references (LF82, UTI89, NRG857c) all present; per-strain GEMs openly available via BiGG.
- Promotion path (~1–2 weeks analyst time, 16–32 GB RAM workstation):
  - C3: Roary or PanX pan-genome on the 110-strain list (paper supplement has accessions).
  - C4: COBRApy + iJO1366 + per-strain GEMs from BiGG for FBA on mucus-glycan substrates (GlcNAc, sialic acid, fucose).
  - C5: BLAST/HMMER for Amadori-degradation gene presence/absence.
- All open, all feasible locally.

**BVBRC-18-Marine-Streptomyces-BGC-2019 — PROMOTABLE→PARTIAL**
- OA paper; BV-BRC has 14,474 Streptomyces genomes today; antiSMASH/OrthoMCL/GET_HOMOLOGUES all open.
- Promotion path (~16 CPU-cores × 1 week):
  - Parse Supp Table S1 to map all 87 strains to BV-BRC/NCBI accessions.
  - Rerun antiSMASH v6 on all 87 → C2 quantitative (paper's 16–84 BGC range).
  - Run GET_HOMOLOGUES → C4 pan-genome (123,302 OG clusters; may differ by ±5% due to OrthoMCL→GET_HOMOLOGUES substitution).
  - Run IQ-TREE for phylogeny → C3 (three clades 23/38/22).
- REPLICATED would require ecological metadata join for C5 — depends on whether `isolation_source` metadata is complete, hence PARTIAL is the more honest ceiling.

**BVBRC-19-Propionibacterium-pangenome-metabolic — PROMOTABLE→PARTIAL**
- OA paper; all 5 (former) species reachable in BV-BRC under modern split nomenclature; published GEM available as supplement.
- Promotion path (~2 weeks on 16-CPU workstation):
  - GET_HOMOLOGUES pan-genome on the 5-species set → C4.
  - Rebuild ModelSEED GEMs + COBRApy FBA on the ferredoxin-linked pathway → C5.
- PARTIAL is the honest ceiling because the novel ferredoxin pathway claim is a model prediction; reproducing it depends on faithful ModelSEED reconstruction parameters which the paper documents but doesn't fully script.

**BVBRC-11-VREfm-LatAm-Rios2020 — ALREADY PARTIAL; PROMOTABLE→REPLICATED**
- Note: this report self-labels "SPOT-CHECK REPLICATED" but the pass-2 numbers (cov=12/22, agr=10/22, ≥55% coverage, 8 VERIFIED + 5 PARTIAL of testable claims) put it functionally at PARTIAL by AUDIT_PROTOCOL.md thresholds.
- Promotion path to REPLICATED:
  - C10–C13 (clade A/B split ~2,765y; animal/clinical ~502y; CRS-I/II ~302y; substitution rate 3.41 SNPs/genome/y): run BEAST MCMC time-tree (the report flags "BEAST MCMC budget" as blocker; this is compute, not data — feasible on HPC).
  - C31 (Clade I lacks fms22/swpC/hylEfm): obtain paper's curated virulence reference protein set (author contact or careful literature trawl).
  - Refit C4/C5 with Prokka→RAST equivalent annotation to close the 1,674 vs 2,068 orthogroup gap.
- All 55 genomes already downloaded; AMR/virulence/VFDB calls already run. The path to REPLICATED is BEAST + virulence reference set, both bounded.

---

## Summary tally

| Verdict | Count | Slots |
|---|---:|---|
| PROMOTABLE→REPLICATED | 4 | fipy-wave4, BVBRC-16, BVBRC-17, BVBRC-11 (already PARTIAL) |
| PROMOTABLE→PARTIAL | 4 | lucid100-neutron-rbe-pre-post-dna-repair, lucid100-intensity-modulated-protective-doserate, BVBRC-18, BVBRC-19 |
| Already PARTIAL (mislabel/ceiling-author-dependent) | 1 | lucid100-multiscale-uhdr-survival-model (ceiling without author contact) |
| CEILING-SPOTCHECK | 4 | lucid100-cho-low-dose-rate-dna-repair-deficient, lucid100-flash-oxygen-repair-mechanistic-model, lucid100-arabidopsis-aox1a-gamma-irradiation, lucid100-stochastic-nhej-track-structure-2010 (conditional on library access) |

**Pattern:** All 5 BVBRC slots and the FiPy slot are promotable because their underlying papers are OA and their data lives in public databases (BV-BRC, BiGG, NCBI). All 4 ceiling-SPOTCHECK LUCID slots share the same pathology: closed-access publishers (Elsevier, T&F, BioOne) plus zero or lab-internal data deposits. The 3 promotable LUCID slots are precisely the ones with either OA papers (Matsuya 2019 Sci Rep, Desjardins-Proulx 2026 PMB CC-BY) or open author code (Zenodo MIT).

**Recommendation:** prioritize the 6 PROMOTABLE→REPLICATED/PARTIAL slots with all-local compute paths first (fipy-wave4, BVBRC-16/17/18/19, lucid100-intensity-modulated-protective-doserate) — these are days-to-weeks of bounded local work that would move 6 SPOT-CHECKs to PARTIAL/REPLICATED with high confidence. The 4 CEILING slots should be tagged "permanently capped at SPOT-CHECK absent publisher/library access" and removed from any "thin report" follow-up queue.
