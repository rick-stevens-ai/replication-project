# Artifacts Summary — BVBRC-115

## Public artifacts pulled

| Type | Identifier | URL | Size | Notes |
|---|---|---|---|---|
| PMC full-text | PMC6788494 | https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:6788494&metadataPrefix=pmc | 78 kB | JATS-NXML source; PDF blocked at OUP (Cloudflare Turnstile) and PMC (PoW), used JATS as text source |
| Genome (paper's own) | GenBank CP039297.1 | E-utils efetch db=nuccore id=CP039297 | 3.9 MB FASTA + 9.0 MB GBK | UFLA258 complete chromosome, 3,947,206 bp, from BioProject PRJNA529593, BioSample SAMN11397814 |
| Genome (velezensis type) | NC_009725.2 | E-utils efetch id=NC_009725 | 3.9 MB | FZB42 = *B. velezensis* type strain, 3,918,596 bp |
| Genome (paper reclassifies) | HG328254.1 | E-utils efetch id=HG328254 | 3.9 MB | UCMB5113, deposited as "*B. amyloliquefaciens* subsp. plantarum", paper argues = *B. velezensis*, 3,889,532 bp |
| Genome (amyloliquefaciens type) | FN597644.1 | E-utils efetch id=FN597644 | 4.0 MB | DSM7 = *B. amyloliquefaciens* type strain, 3,980,199 bp |
| Genome (siamensis complete) | NZ_CP025001.1 | E-utils efetch id=NZ_CP025001 | 4.3 MB | *B. siamensis* SCSIO 05746 (used because paper's SCSIO 04756 has only draft assemblies), 4,268,316 bp |

Everything above is free, no-auth, freshly re-fetched during this replication (2026-07-05). NCBI E-utilities has a soft rate limit of 3 req/s without an api-key; hit it once during batch fetch (harmless retry).

## Derived artifacts written by this replication

### Root
- `paper.pdf` (54 kB) — pandoc-rendered from JATS-derived Markdown; visually inspectable but the JATS-Markdown `extraction/marker.md` is the semantic source of truth for text-based checks.

### `extraction/`
- `marker.md` (28 kB) — Marker-surrogate: JATS-derived full-text with provenance header explaining why the PDF path failed.
- `nougat.mmd` (28 kB) — Nougat-surrogate: same content, mmd extension, provenance header.
- `paper_full.md` (27 kB) — raw JATS-derived Markdown (source for the two above).

### `report/`
- `REPORT.md` — 15 kB, full report (this bundle's centrepiece).
- `REPORT.tex` — LaTeX render of the same report.
- `REPORT.pdf` — compiled LaTeX (if xelatex available at write time).
- `brief.md` — 1-paragraph what/why summary.
- `workflow.md` — full method + tools + effort accounting.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest partial-fail / gap analysis.
- `open_questions.json` — 5 grounded open-research questions with next-steps.

### `report/evidence/`
- `genome_stats.json` — length/GC/CDS/tRNA/rRNA per genome. **Key claim-C1..C3 numbers.**
- `fastani_all.tsv` — 5×5 fastANI matrix. **Key claim-C4 numbers.**
- `rpoB.fasta` — extracted rpoB CDS per genome (5 sequences, 3,582 nt each).
- `rpoB.aln` — MAFFT-auto alignment.
- `rpoB_pctid_matrix.json` — pairwise rpoB %ID matrix. **Key claim-C5 numbers.**
- `UFLA258_BGC_kcb_summary.json` — antiSMASH-v8 + KCB region → paper-compound mapping. **Key claim-C6, C7 numbers.**
- `BGC_presence_blastn.json` — first-pass BLAST-based BGC panel (superseded by antiSMASH; kept for provenance).
- `analysis_run.log` — full stdout+stderr of `analysis.sh`.

### `work/`
- `analysis.sh` — full uicgpu pipeline (8 kB).
- `analysis.sh.bak` — pre-python-path-fix backup.
- `PMC6788494.nxml.xml` — 78 kB JATS raw fetch.
- `UFLA258.gbk` — 9.0 MB GenBank flatfile with the paper's own deposited annotation.
- `results/UFLA258_antismash.gbk` — 8.2 MB antiSMASH-v8+KCB annotated GenBank.
- `genomes/*.fasta` — 5 genomes, ~20 MB total.

## Traces / logs

- `report/evidence/analysis_run.log` — the definitive run trace (fastANI progress, tool versions, all json dumps). ~8 kB.
- On uicgpu, `/data/stevens/bvbrc-115/results/antismash/UFLA258_kcb/` retains the full antiSMASH HTML output (~15 MB) for visual inspection — not copied to Dropbox to keep the shipped bundle small; can be re-fetched with `rsync uicgpu:/data/stevens/bvbrc-115/results/antismash/UFLA258_kcb/ ...`.

## Checksums (top-level)

| File | SHA256 | Bytes |
|---|---|---|
| paper.pdf | (see `sha256sum paper.pdf` in this dir) | 54,193 |
| extraction/marker.md | idem | 27,571 |
| extraction/nougat.mmd | idem | 27,686 |
| work/PMC6788494.nxml.xml | idem | 78,449 |
| report/evidence/fastani_all.tsv | idem | 1,630 |
| report/evidence/rpoB_pctid_matrix.json | idem | 721 |

(Checksums are quick to reproduce: `sha256sum <file>` — not committed to file to keep the summary editable across incremental additions.)
