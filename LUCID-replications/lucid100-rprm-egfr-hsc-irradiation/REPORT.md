# LUCID-100 Replication Report

*Slot: lucid100-rprm-egfr-hsc-irradiation. Paper: RPRM/EGFR axis in hematopoietic stem cells after irradiation (Cell Biology International 46(2):2158, RPRM-KO mouse study). Report compiled by Ollie from on-disk first-pass artifacts (subagent completed the analysis but timed out before writing this file; no numbers fabricated — all carried from results/ and FIRST_PASS_REPORT.md).*

## TL;DR
This is a **wet-lab in vivo mouse paper** (RPRM-knockout, 4 Gy TBI, FACS-sorted LSK cells), mis-tagged as "simulation/model replication" in the LUCID-100 master TSV. It contains **no model, no equation, no simulation, no code**. Its one high-throughput dataset (bulk RNA-seq of sorted LSK cells, n=3/group, 1 h post 4 Gy, commissioned to BGI) **was never deposited** (GEO returns 0 hits; data-availability = "from corresponding author upon reasonable request"). All quantitative figures rest on confocal/flow cytometry analyzed in GraphPad Prism with Student's t on n=3–6 mice, with no underlying numeric tables published. **Independent quantitative replication from public artifacts is not feasible** — verdict NO-GO. Topically in-scope (DDR + HSC radioprotection); retained for corpus as a downstream-claim anchor.

## 1. Data sources
- Main PDF (4.34 MB), JATS XML (130 KB), full text (679 lines), 6 figure JPEGs, full qPCR primer table — all harvested (see source/{crossref,epmc,geo_search}.json).
- Supplementary S1–S6: blocked behind Wiley anti-bot wall + broken PMC re-render; contents inferable from in-text references (sex-matched controls, female-mouse parallels, replicate plots) but numerically unreadable. **Exact missing artifact: the six Wiley supplementary files (S1–S6) + the un-deposited BGI LSK RNA-seq count matrix.**
- GEO esearch for the study's own RNA-seq: **0 hits** (no deposit).

## 2. Methods comparison
Paper methods = wet-lab (RPRM-KO line, TBI, FACS, confocal γ-H2AX, comet assay, flow apoptosis, RT-qPCR, BGI RNA-seq). No computational method to re-implement. Our replication is therefore an artifact/claim audit + a lateral public-data cross-check (below), not a method reproduction.

## 3. Quantitative claim audit
8 primary claims enumerated (full matrix in FIRST_PASS_REPORT.md). All 8 are wet-lab readouts requiring the RPRM-KO mouse line:
1. RPRM dispensable for steady-state hematopoiesis — not reproducible (wet-lab).
2. RPRM-KO preserves BM/LSK/PLT/WBC after 4 Gy (male>female) — not reproducible.
4. RPRM-KO reduces γ-H2AX + comet tail moment post-IR — not reproducible.
5. RPRM-KO increases p-DNA-PKcs(T2609); NU7441 abolishes the protection (pharmacological epistasis) — not reproducible.
6. Protection via proliferation (Ki67/BrdU/colony) not survival (no apoptosis change) — not reproducible.
7. RPRM-KO upregulates EGFR/p-EGFR/Lin28a, downregulates IL-1α/IL-1β/TNF-α/IL-13 — **partial**: the 10-gene qPCR primer panel is fully captured + machine-readable (results/qpcr_primer_audit.json, qpcr_amplicon_audit.json, primer_refseq_blast_finding.json) and re-executable in any wet lab; the RNA-seq KEGG bubble needs the un-deposited BGI data.
3,8 — likewise wet-lab.

**Net: 0/8 claims quantitatively reproducible from public artifacts; 0/8 contradicted (none testable from available data).**

Lateral cross-check (the one computational asset attempted): re-analyzed **GSE244971** (Chen et al., Army Medical University; 12 samples, Ctrl/IR/Ab_IR/L_IR, n=3, 3 d post-IR) as a WT-only, direction-only proxy for the EGFR/inflammation axis (results/cross_check_GSE244971.json, pathway_signature_GSE244971.json). Honest caveats recorded in the JSON: n=3 (direction-only), timepoint mismatch (3 d proxy vs paper's 1 h), WT-only (cannot test the KO comparison), FPKM-like normalization, normal-approx p as a lower bound. This is a lateral sanity check, **not** a replication of the paper's KO claims.

## 4. Scope audit
8 primary analyzable units, all wet-lab. 0% reproducible from public artifacts (coverage failure driven entirely by non-deposition, not method quality). Mis-tag corrected: this is `wet-lab in-vivo`, not `simulation/model`.

## 5. What I actually ran
- Artifact harvest (PDF/XML/text/figures/primer table) — partial-but-clean.
- qPCR primer/amplicon audits + RefSeq BLAST sanity (results/*.json) — primers validate.
- GSE244971 lateral cross-check in pure-Python stdlib (no pandas/scipy), Welch normal-approx — direction-only.
- smoke_check.py (re-confirms primer-table machine readability).

## 6. Key output files
FIRST_PASS_REPORT.md, PROGRESS.md, results/{qpcr_primer_audit,qpcr_amplicon_audit,primer_refseq_blast_finding,pathway_signature_GSE244971,cross_check_GSE244971,smoke_output}.json, code/smoke_check.py, source/{geo_search,crossref,epmc}.json, figures/*.

## 7. Honest gaps
1. **The study's own LSK RNA-seq count matrix is not deposited anywhere** (GEO 0 hits) — the single computational asset is the inaccessible one. Exact missing artifact.
2. **Wiley supplementary S1–S6** anti-bot blocked (sex-matched/female-parallel panels) — one manual browser download would unblock.
3. All other claims are wet-lab requiring the **RPRM-KO mouse line** (not a data gap that any reanalysis can close).

## 8. Verdict
Topically in-scope (DDR + HSC radioprotection) but **no replicable computational asset**: no model/equation/code, the one RNA-seq dataset undeposited, supplements blocked, all claims wet-lab. Replication from public artifacts is not feasible (high confidence — exhaustive checks across Wiley/PMC/Europe PMC/NCBI OA/GEO all converge on "no public deposit"). Recommend KEEP-for-corpus as a downstream anchor for a future EGFR→DNA-PKcs→HSC-radioprotection meta-analysis slot (anchor on Fang 2020, 10.7150/thno.60143, if it deposited HSC RNA-seq), and correct the master-TSV worktype from simulation/model → wet-lab.

VERDICT=NO-GO COVERAGE=0/10 AGREEMENT=0/10
Repro-blocker summary:
1. Study's own sorted-LSK BGI RNA-seq count matrix never deposited (GEO 0 hits; "available on request") — the only computational asset is inaccessible.
2. Wiley supplementary files S1–S6 anti-bot/PMC-render blocked (sex-matched + female-parallel quantitative panels unreadable).
3. All 8 primary claims are wet-lab readouts requiring the RPRM-KO mouse line; no model/equation/code exists to reproduce — paper is mis-tagged as simulation/model in the master TSV.
