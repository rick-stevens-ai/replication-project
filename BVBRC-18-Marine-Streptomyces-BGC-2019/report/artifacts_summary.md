# Artifacts Summary — BVBRC-18 Marine *Streptomyces* BGC Replication

Directory: `~/Dropbox/REPLICATE-PROJECT/BVBRC-18-Marine-Streptomyces-BGC-2019/`
Paper: Xu et al. 2019, *Marine Drugs* 17(9):498, DOI 10.3390/md17090498.
Verdict: **PARTIAL**.

## Report artifacts (`report/`)

| File | Type | Purpose |
|---|---|---|
| `REPORT.md` | Markdown | Canonical human-readable replication report. All §-numbered claims, tables of results-vs-paper, verdict rationale, coverage/agreement, honest limitations. |
| `REPORT.tex` | LaTeX | Publication-formatted version of `REPORT.md` with a dedicated Genuine Critique section (structural gaps, sampling concerns, method-substitution risks, roadmap to FULL verdict). |
| `open_questions.json` | JSON | Five open scientific questions grounded in the replication findings (MIBiG novelty scoring, marine-vs-terrestrial BGC diversity, antiSMASH-version sensitivity, sponge/coral-vs-sediment host niche, wet-lab validation hit-rate). Each carries `{q, basis, next_steps}`. |
| `workflow.md` | Markdown | ASCII pipeline diagram + step-by-step table (executed and NOT-executed steps), determinism/reproducibility notes, provenance trail. |
| `artifacts_summary.md` | Markdown | This file. |
| `failure_analysis.md` | Markdown | What did not replicate, why, and what would fix it. |
| `REPORT.md.bak-pre-promo` | Backup | Pre-promotion (Wave 4 spot-check) version of the report, preserved for provenance. |

## Data / working artifacts (`work/`)

| File | Type | Purpose |
|---|---|---|
| `work/paper.pdf` | PDF | Europe PMC mirror of the OA paper (CC BY 4.0). Source of all headline claims. |
| `work/genomes/bvbrc_marine.json` | JSON | BV-BRC snapshot of 287 marine *Streptomyces* hits with fields `genome_id`, `checkm_completeness`, `checkm_contamination`, `genome_length`, `gc_content`, `cds`, `isolation_source`. |
| `work/corpus_stats.txt` | Text | Corpus-level reproduction stats: 141 QC-passing genomes, size range 4.84–10.03 Mb (median 7.18), GC 70.30–74.42 mol% (median 72.80), CDS 4631–9636 (median 6755), ecotype sediment=84 / sponge=25. |
| `work/bgc_scan/sample.json` | JSON | The 12 stratified genome IDs used for the BGC marker scan. |
| `work/bgc_scan/scan.py` | Python | BGC marker-scan script. Curated keyword patterns for PKS-I/II, NRPS, terpene, RiPP/lanti, siderophore, bacteriocin, butyrolactone. Class-specific divisors to convert marker counts → rough per-BGC estimates. |
| `work/bgc_scan/results.json` | JSON | Per-strain BGC marker hits, per-class breakdown, rough BGC estimate. Basis for BGC-level claims C6–C10. |
| `extraction/marker.md` (or similar) | Text | Extraction workspace (parser outputs). Optional; not required for the report. |

## Numeric artifact highlights (grounded in REPORT.md)

- **Corpus size:** 141 QC-passing marine *Streptomyces* today (vs paper's 87 in Jan 2019).
- **Total marine hits before QC:** 287.
- **Total *Streptomyces* in BV-BRC:** 14,474.
- **Genome-size range this pass:** 4.84–10.03 Mb (paper: 5.77–11.50 Mb).
- **GC-content range this pass:** 70.30–74.42 mol% (paper: 69.9–73.8 mol%).
- **Gene-count range this pass:** 4631–9636 (BV-BRC CDS; paper's RAST: 5363–10,776).
- **BGC estimate range (12-strain proxy):** ~36–87 (paper: 16–84).
- **BGC density (12-strain proxy):** 4.24–11.55 BGC/Mb (paper: 1.94–9.21).
- **BGC-vs-size correlation:** Pearson r = 0.24 (12 strains); consistent with paper's "not positively correlated."
- **Class universality (12/12 unless noted):** PKS-I 12/12, NRPS 12/12, terpene 12/12, siderophore 12/12, PKS-II 11/12, RiPP/lanti 11/12, bacteriocin 11/12, butyrolactone 10/12.
- **Outgroup:** *Kitasatospora setae* KM-6054 = GCA_000269985.1 = BV-BRC PRJNA19951, 8.78 Mb, CheckM 98% / 0%.

## Coverage / agreement

- Coverage: **5/10** (original spot-check: 2/10).
- Agreement: **9/10** — every tested claim verified or overlapped; one mild quantitative gap (per-Mb BGC density) attributable to the documented antiSMASH-substitute method.

## What is NOT in the artifact set (and why)

- No antiSMASH GBK outputs (antiSMASH not installed).
- No Proteinortho OC file (not re-run).
- No IQ-Tree Newick / clade partition (not re-built).
- No MDPI Table S1 87-strain accession list (HTTP 403 across variants).

See `failure_analysis.md` for the full "what did not replicate" catalog.
