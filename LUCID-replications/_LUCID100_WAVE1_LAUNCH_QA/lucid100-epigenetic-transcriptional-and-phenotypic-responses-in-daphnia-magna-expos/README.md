# LUCID100 Wave 1 — Slot 5

## Paper

- **Title:** Epigenetic, transcriptional and phenotypic responses in *Daphnia magna* exposed to low-level ionizing radiation.
- **Authors:** Jens Thaulow, You Song, Leif C. Lindeman, Jorke H. Kamstra, YeonKyeong Lee, Li Xie, Peter Aleström, Brit Salbu, Knut Erik Tollefsen.
- **Affiliations:** Norwegian Institute for Water Research (NIVA); Centre for Environmental Radioactivity (CERAD) at NMBU; NMBU Faculty of Veterinary Medicine; Utrecht University IRAS; NMBU Faculty of BioSciences; NMBU MINA.
- **Venue / year:** *Environmental Research* **190** 109930, 2020-11.
- **DOI:** [10.1016/j.envres.2020.109930](https://doi.org/10.1016/j.envres.2020.109930)
- **Open-access full text (publisher preprint):** Utrecht University repository, hdl `http://hdl.handle.net/1874/408631` — PDF copy harvested to `artifacts/thaulow2020_envres.pdf` (7.94 MB, 13 pp).

## LUCID100 metadata

- Wave: 1
- Rank in master TSV: 36
- Tier / priority score: **A / 20**
- Themes: DNA repair / DDR; dose-rate / low-dose response; omics / biomarkers / signatures; immune / inflammation / senescence.
- Worktype declared in master: *omics/signature replication*.
- QA decision in master: KEEP — relevant and replication-plausible.

## Source code, data, and supplementary availability

| Artifact class                              | Status | Notes |
| ------------------------------------------- | ------ | ----- |
| Source PDF (publisher preprint)             | ✅ Harvested | `artifacts/thaulow2020_envres.pdf`; text extracted to `artifacts/thaulow2020_envres.txt`. Mirror under workspace at `~/.openclaw/workspace/lucid-replications/slot5-daphnia/artifacts/`. |
| Public sequencing accessions (GEO/SRA/ENA)  | ❌ None | Paper contains **no** GEO, SRA, ENA, ArrayExpress, PRJNA, PRJEB, Dryad, Figshare, or Zenodo accession. No high-throughput sequencing was performed. |
| Supplementary files (Elsevier MMC)          | ❌ None found | PDF has no "Appendix / Supplementary data" section. Probed `https://ars.els-cdn.com/content/image/1-s2.0-S0013935120308252-mmc{1..4}.{pdf,docx,xlsx}` — all return HTTP 404. |
| Code repository (GitHub / Zenodo)           | ❌ None | No repository or code DOI is cited. |
| Raw per-individual measurements             | ❌ Not deposited | Authors used GraphPad Prism v8.0.2 and XLSTAT v2019.3.2 for analysis; underlying spreadsheets are not deposited. |
| Reagent catalog numbers                     | ✅ In text | Antibodies: H3K9me3 Diagenode `C15410056`, H3K9ac Diagenode `C1541009` (likely typo for `C15410004`), H3 Diagenode `C15310135`. Kits: Gentra Puregene Tissue (Qiagen), ZR Tissue & Insect RNA MicroPrep (Zymo), qScript cDNA SuperMix (Quanta), PerfeCTa SYBR Green FastMix (Quanta). |
| Primers (qPCR + ChIP-PCR)                   | ⚠️ Cited only | "Previously published primers were used (Gomes et al., 2018; Lindeman et al., 2019b; Song et al., 2020)" — primer sequences must be lifted from those three secondary citations, not from this paper. |
| Internal-standard isotope reagents          | ✅ In text | 2′-deoxyguanosine-13C10,15N5 (TRC), 5-methyl-2′-deoxycytidine-d3 (TRC). |
| Daphnia magna sequence references           | ⚠️ Personal communication | "Jana Asselman (Ghent University) for kindly providing the Daphnia sequences" — not in a public repository tied to this paper. |

## Target claims / figures

Quantitative findings that could be checked against re-derivable raw data (none of which is public):

1. **Fig. 1 — Global DNA methylation.** LC-MS 5mC/G ratio, n=5 pools (5 daphnids each). Controls ≈ 0.34 % 5mC (consistent with prior Daphnia values 0.25–0.53 %). **Dose-rate-dependent increase**; 10 mGy/h is significantly elevated relative to control.
2. **Fig. 2 — ChIP-qPCR H3K9me3 / H3K9ac at 7 promoters** (Dnmt1, Dnmt3a1, Dnmt3a2, Gnmt, Metk, Sahh, Mthfr). n=3 pools, 8 daphnids each. Dose-rate-dependent increases in H3K9me3 for Dnmt3a1, Dnmt3a2, Gnmt. Significant H3K9ac enrichment: Dnmt3a1 @ 10 mGy/h, Metk @ 1 mGy/h. Actin used as a high-H3K9ac housekeeping reference.
3. **Fig. 3 — qPCR transcription of 16 biomarker genes.** n=4–5 pools (4 daphnids each), reference genes Actin + Gadph, ΔΔCq / Pfaffl normalisation. 7/16 genes downregulated dose-rate-dependently. At 10 mGy/h, significant suppression of Sahh, Dnmt3a2, Calm, Rad50, Triap, Gst. Dnmt3a2 significantly down at 0.4–10 mGy/h. Vtg1, Vtg2 upregulated dose-rate-dependently; Met significantly up at 1 mGy/h; non-significant Tet2 up-trend.
4. **Fig. 4 — Temporal mROS and lpoROS** (mitochondrial / lipid-peroxidation-associated), n=3, days 2/4/7. At day 2, ≥1 mGy/h significantly reduces mROS; lpoROS reduced only at 10 and 40 mGy/h. Day 4: no significant differences. Day 7: non-significant uptrend in irradiated groups (except 0.4 mGy/h).
5. **Fig. 5 — Histology** (qualitative, n=1). Increased empty follicles from 0.4 mGy/h; abnormal oocytes from 4 mGy/h; abnormal gut cells/hair across doses; thinner epidermis from 4 mGy/h.
6. **Fig. 6 — Fecundity** (n=10). No significant effect on cumulative fecundity; positive trend for brood 1, brood 2, and total offspring at 4–40 mGy/h.
7. **Fig. 7 — PCA biplot.** PC1+PC2 explain **85.41 %** of variance; specific qualitative correlation structure described in §3.8.
8. **Figs. 8–9 — Conceptual / pathway figures** (not data).

## Acceptance criteria for any future replication

Set **before** running anything.

- **Numerical exact-rerun acceptance:** out of scope — raw per-individual data are not deposited.
- **Independent in-silico re-derivation acceptance:** out of scope — no genome/transcriptome dataset to mine.
- **Figure-digitization replication acceptance** (the only feasible path):
  - Manually digitize Figs. 1, 2, 3, 4, 6 from the published bitmaps (e.g. WebPlotDigitizer) and reconstruct:
    - the qualitative dose-response direction (up / down / flat) for each panel — must match the paper's narrative in §3.1–3.8 for ≥ 90 % of (gene × dose) cells.
    - the significant-vs-not significance star pattern (matching paper's `*` annotations) for ≥ 90 % of cells.
    - PCA variance share PC1+PC2 = 85.41 % ± 1 percentage point when the digitized mean dose-response table is fed through standard PCA (any package, scale=TRUE).
  - PASS if all three are met; PARTIAL if only the PCA variance is met; NO-GO if dose-response directions disagree, because that would indicate a digitization or interpretation error rather than a true replication failure of the paper.
- **Wet-lab re-replication acceptance:** out of scope for LUCID100 (requires Daphnia magna clone husbandry, a 60Co irradiator at NMBU/CERAD-equivalent dose-rates, LC-MS for 5mC/G, ChIP-qPCR pipeline, and 28 days of animal work).

## Source-of-truth pointers

- Campaign master: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` row rank=36.
- Repo folder (this brief): `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_WAVE1_LAUNCH_QA/lucid100-epigenetic-transcriptional-and-phenotypic-responses-in-daphnia-magna-expos/`.
- Workspace mirror: `/Users/stevens/.openclaw/workspace/lucid-replications/slot5-daphnia/`.
- Progress JSON: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave1-5-epigenetic--transcriptional-and-phenotypic-responses-in-daph.json`.

## Artifact harvest checklist

- [x] Source PDF saved locally (Utrecht repo, hdl 1874/408631)
- [x] Full text extracted (`pdftotext -layout`)
- [x] Supplementary files searched — **none exist** (confirmed by PDF inspection + Elsevier MMC URL probe)
- [x] Code repository searched — **none cited**
- [x] Public data accession searched — **none cited** (paper used qPCR + ChIP-qPCR + LC-MS, not next-gen sequencing)
- [x] Environment / dependencies plan written (see `MANIFEST.md`)
- [x] Acceptance metrics defined above
- [x] Blockers listed explicitly in `FIRST_PASS_REPORT.md`

## Execution checklist

- [x] Smoke test / minimal calculation — see `repro/pca_variance_smoke.py` and `repro/digitized_dose_response_template.csv`
- [ ] Main replication run — requires manual figure digitisation; deferred (see FIRST_PASS_REPORT.md verdict)
- [ ] Figures/tables regenerated or digitized comparison done
- [ ] Logs, hashes, environment, and provenance captured
- [x] `FIRST_PASS_REPORT.md` written
- [x] Progress JSON updated under OpenClaw memory

## Initial abstract / notes

Ionizing radiation is known to induce oxidative stress and DNA damage as well as epigenetic effects in aquatic organisms. To investigate the potential roles of epigenetic mechanisms in low-dose ionizing radiation-induced stress responses, adult *Daphnia magna* were chronically exposed to external 60Co gamma radiation at 0, 0.4, 1, 4, 10, and 40 mGy/h for seven days. Biological effects at the molecular (global DNA methylation, histone modification, gene expression), cellular (ROS formation), tissue/organ (ovary, gut and epidermal histology) and organismal (fecundity) levels were investigated. Results showed dose-rate-dependent global DNA hypermethylation, loci-specific H3K9me3 / H3K9ac changes, downregulation of genes involved in DNA methylation, one-carbon metabolism, antioxidant defense, DNA repair, apoptosis, calcium signaling, and endocrine regulation of development and reproduction.
