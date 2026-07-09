# Artifacts Summary — BVBRC-65 (pMOL412_FII)

**Target:** Diaconu et al. 2020, *J Antimicrob Chemother* 75(12):3475–3479 (DOI 10.1093/jac/dkaa374; PMC7662189).
**Verdict:** REPLICATED (spot-check, high confidence on all publicly resolvable claims).
**Date:** 2026-07-03.

All artifacts live under `~/Dropbox/REPLICATE-PROJECT/BVBRC-65-ecoli-blaNDM4-incFII-plasmid/`.

## Report directory: `report/`

| File | Role | Notes |
|------|------|-------|
| `REPORT.md` | Primary human-readable replication report | Markdown; source of truth for all downstream backfill |
| `REPORT.tex` | LaTeX version of REPORT.md + dedicated **Genuine Critique** section | Compilable standalone (`pdflatex REPORT.tex`); adds adversarial reading of the replication itself |
| `open_questions.json` | 5 truly open questions grounded in E. coli / blaNDM-4 / IncFII biology | Each includes `{q, basis, next_steps}`; suitable for follow-up experimental planning |
| `workflow.md` | Step-by-step reproducibility contract | 9 numbered steps, tool versions frozen |
| `artifacts_summary.md` | This file | Index of everything produced |
| `failure_analysis.md` | What could have failed, what did fail, what still could fail | Honest limits + partial-failure inventory |

## Evidence directory: `report/evidence/`

| File | Content | Provenance |
|------|---------|------------|
| `plasmid_stats.json` | Length (53,044 bp), GC% (51.59), accession (LR812026.1), BioSample (SAMEA6863320), BioProject (PRJEB38506) | Biopython 1.87 on downloaded FASTA |
| `abricate_ncbi.tsv` | AMR gene hits: `blaNDM-4`, `ble-MBL`, `sul1`, `aadA2`, `dfrA12` | abricate 1.4.0, NCBI AMR db 8232 seqs (2026-Jul-3) |
| `abricate_plasmidfinder.tsv` | Replicon call: `IncFII_1`, 100% ident, 98.85% cov, ref AY458016 | abricate 1.4.0, plasmidfinder 488 seqs (2026-Jul-3) |
| `blaNDM4_extracted.fasta` | 813 bp NDM-4 ORF (positions 10450–11262, +strand) | Extracted from LR812026.1 via Biopython |
| `tool_versions.txt` | abricate + Biopython + DB build dates | Frozen at run time |

## Working directory: `work/`

| File | Content | Provenance |
|------|---------|------------|
| `pMOL412_FII.fasta` | Full plasmid sequence, 53,044 bp | NCBI efetch on LR812026.1 |
| `pMOL412_FII.gb` | Full GenBank flat file (annotations + features) | NCBI efetch on LR812026.1 |
| `blaNDM4_extracted.fasta` | Same 813 bp ORF as in `report/evidence/` (working copy) | Biopython slice of LR812026.1 |
| `paper_abstract.txt` | Original PubMed abstract used for record identification | PubMed |

## Key numerical results (canonical)

| Metric | Value | Source |
|--------|-------|--------|
| Plasmid accession | `LR812026.1` (INSDC/EMBL) / `NZ_LR812026.1` (RefSeq) | NCBI |
| Plasmid length | 53,044 bp (paper: 53,043 bp; Δ = 1 bp) | Biopython on FASTA |
| Plasmid GC% | 51.59% (paper: not reported) | Biopython on FASTA |
| Replicon | IncFII_1 @ 100% ident / 98.85% cov | plasmidfinder |
| blaNDM-4 ORF | 813 bp @ 10450–11262 (+); 100% ident / 100% cov vs NG_049336.1 | abricate + NCBI AMR |
| NDM-4 authenticity | Leu at residue 154 (M154L diagnostic vs NDM-1) | Biopython translation |
| sul1 | 840 bp @ 100/100% | abricate |
| aadA2 | 792 bp @ 100/100% | abricate |
| dfrA12 | 498 bp @ 100/100% | abricate |
| ble-MBL | 366 bp @ 100/100%, at 11266–11631 (canonical NDM co-cassette) | abricate |
| WGS assembly available? | **No** (elink to `assembly` = 0 hits) | NCBI elink |

## Replicated claims (7 total)

- ✅ C1 (plasmid length, ±1 bp)
- ✅ C2 (IncFII replicon)
- ✅ C3a (blaNDM-4 present)
- ✅ C3b (allele authenticity via M154L)
- ✅ C4a (sul1)
- ✅ C4b (aadA2)
- ✅ C4c (dfrA12)
- ⚠ C5 (ST641/O108:H23) — spot-check unverifiable (WGS not deposited)
- ⚠ C6 (blaTEM-1B, sul3) — spot-check unverifiable (WGS not deposited)
- ⏭ C7 (relatedness to pM109_FII) — out of minimal-verification scope

## External references cited

- Paper primary: DOI [10.1093/jac/dkaa374](https://doi.org/10.1093/jac/dkaa374)
- PMC full text: PMC7662189
- Plasmid record: [LR812026.1](https://www.ncbi.nlm.nih.gov/nuccore/LR812026.1)
- BioSample: [SAMEA6863320](https://www.ncbi.nlm.nih.gov/biosample/SAMEA6863320)
- BioProject: [PRJEB38506](https://www.ncbi.nlm.nih.gov/bioproject/PRJEB38506)
- NDM-4 reference gene: [NG_049336.1](https://www.ncbi.nlm.nih.gov/nuccore/NG_049336.1)
- IncFII_1 reference: AY458016
- NDM-4 M154L discovery: Nordmann et al. 2012, *AAC* 56:2184–2186
