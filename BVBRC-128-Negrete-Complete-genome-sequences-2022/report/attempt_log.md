# Attempt Log — BVBRC-128 Negrete

Chronological, 2026-07-06.

- **00:08** Task received. Created target dir + subdirs.
- **00:08** Fetched paper via NCBI PMC PDF endpoint → returned HHS pre-fetch stub HTML (1.8 KB). Fallback #1.
- **00:08** Tried Europe PMC OA rendering endpoint → same HHS stub. Fallback #2.
- **00:08** Fetched DOI from PubMed EFetch (`10.1186/s13099-022-00500-5`). Journal is *Gut Pathog*
  (BMC, fully OA), so tried BMC direct PDF endpoint
  `https://gutpathogens.biomedcentral.com/counter/pdf/10.1186/s13099-022-00500-5.pdf` → **worked**, 2.2 MB PDF.
- **00:09** `pdftotext -layout paper.pdf work/paper_pdftotext.txt` → 611 lines.
- **00:09** Regex-mined 7 CP-accessions + 2 BioProjects + 2 SRRs.
- **00:09** NCBI ESummary confirmed all 7 accessions map to *Cronobacter sakazakii* MOD1-H322 or MOD1-GK1025B
  and lengths match paper Table 1 exactly.
- **00:09** EFetch pulled FASTA for all 7 + GenBank for 5 plasmids + feature-tables for 2 chromosomes.
- **00:09** `verify_table1.py` — recomputed length + GC + CDS. Lengths 7/7 exact. GC 7/7 within 0.18 pp.
  CDS drift −127..+360.
- **00:09** BLAST+ available locally. Fetched CGE PlasmidFinder Enterobacteriales DB from Bitbucket (130 KB).
- **00:09** Built local BLAST DB from 5 plasmids; ran BLAST at pident≥60, e≤1e-10.
- **00:09** Filtered to CGE defaults (pident≥95, qcov≥60): **0 hits.** Best hits 80.2-91.5% id.
  → Confirms paper's negative PlasmidFinder claim.
- **00:10** Fetched SSU5 phage (NC_018843). BLAST vs pH322_1 and pGK1025B_1 → strong homology
  (56.6% / 67.0% qcov, 20+ HSPs each, 80-91% id).
- **00:10** GenBank annotation grep confirmed T4SS/T6SS/arsenic-operon/phospholipase-D/tyrosine-recombinase
  presence on the expected plasmids.
- **00:11** PubMLST REST sequence-query for both chromosomes:
  H322 → **ST83/CC83** ✓; GK1025B → **ST64/CC64** ✓. Both exact match to paper.
- **00:11** Computed T4SS/T6SS coordinate spans from GenBank features:
  T6SS 16-17 Kbp (paper: ~13 Kbp core); T4SS 15 Kbp (paper: ~16.4 Kbp). Close.
- **00:12** Wrote 8 required artifacts: paper.pdf, extraction/marker.md, extraction/nougat.mmd,
  report/REPORT.md, report/REPORT.tex, report/open_questions.json, report/workflow.md,
  report/artifacts_summary.md, report/failure_analysis.md.
- **00:13** Verdict: **REPLICATED** (12/15 claims verified, 0/15 contradicted, 3/15 not attempted).

**Nothing failed hard.** No paywall, no rate-limit, no missing endpoint.
The only "friction" (worth logging) was NCBI's HHS-stub PDF endpoint, worked around via the BMC direct
route on second attempt.
