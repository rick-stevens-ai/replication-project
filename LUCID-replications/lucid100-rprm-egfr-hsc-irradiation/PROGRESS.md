# PROGRESS — lucid100-rprm-egfr-hsc-irradiation

Tracking turn-by-turn progress on first-pass artifact harvest for cbin.11900 (RPRM/EGFR/HSC).

## 2026-06-09 13:17 CDT — Subagent kickoff

- Confirmed paper in master TSV: row 49, Wave 2, slot **17** (task said slot 18 — slot 17 is the canonical match for DOI 10.1002/cbin.11900; treated as slot mismatch).
- Created `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-rprm-egfr-hsc-irradiation/` with subdirs (artifacts, code, figures, logs, results, source).

## 2026-06-09 13:19 — Paper harvest

- Wiley direct PDF (`https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/cbin.11900`) → **HTTP 403** (anti-bot).
- Crossref metadata fetched OK → confirmed CC-BY-NC-ND 4.0 license.
- Europe PMC search → **PMC9804513** (open access).
- Europe PMC OA render `https://europepmc.org/articles/PMC9804513?pdf=render` → 4.34 MB PDF ✅.
- Europe PMC fullTextXML → 130 KB JATS XML ✅.
- `pdftotext -layout` → 679 lines of body+refs+captions ✅.
- `pdfimages -j` → 6 JPEGs (Figs 1–5 + abstract panel) → `source/figures/` ✅.

## 2026-06-09 13:21 — Supplementary harvest (FAILED)

Tried all free routes for `CBIN-46-2158-s001.pdf` through `s006.pdf` (one is a DOCX):

| Route | Result |
| ----- | ------ |
| `europepmc.org/articles/PMC9804513/bin/CBIN-46-2158-s00N.*` | 301 → ptpmcrender.fcgi → STREAM_CLOSED (HTTP/2 err 5), empty HTTP/1.1 reply |
| `pmc.ncbi.nlm.nih.gov/articles/PMC9804513/bin/CBIN-46-2158-s00N.*` | 404 (HTML, 48676 bytes) |
| `europepmc.org/backend/ptpmcrender.fcgi?acc=PMC9804513&blobtype=image&blobname=...` | empty reply (HTTP/2 stream not closed cleanly) |
| `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/b5/97/PMC9804513.tar.gz` (path from oa.fcgi) | 550 (FTP) / 404 (HTTPS) — index is stale |
| Wiley `action/downloadSupplement?doi=10.1002%2Fcbin.11900&file=...` | 403 (anti-bot) |
| EPMC `/supplementaryFiles` REST endpoint | 500 (HTML error) |

**Decision:** stop trying free routes for supp; proceed with what we have. JATS XML preserves the file names and section references for S1–S5, so we know what each supp file *contains* even though we can't read the bytes.

## 2026-06-09 13:22 — Deposit / accession hunt

- NCBI GEO esearch ("RPRM hematopoietic", "RPRM hematopoietic stem cell irradiation") → **0 hits**.
- Crossref author list — Beijing Genomics Institute (BGI) is the sequencing vendor per §2.8; **no GEO/SRA/PRJNA/ArrayExpress accession in body, methods, or data-availability statement**.
- Data availability: literally "available from the corresponding author upon reasonable request." Task forbids author contact, so this is a hard wall.

## 2026-06-09 13:24 — Content audit & claim extraction

Read full body, figure captions, M&M, and discussion from XML (avoiding truncated PDF text). Reclassified the paper:

- Master labels it **"simulation/model replication"** — **WRONG.** This is a pure wet-lab in vivo mouse study (RPRM⁻/⁻ vs WT C57BL/6, ±X-irradiation 4 Gy or 6 Gy at 2.0 Gy/min on X-RAD320ix, ±erlotinib, ±NU7441), with flow cytometry, RT-qPCR, comet assay, BrdU, IF microscopy, and one bulk RNA-seq of sorted LSK cells (n=3/group, 1 h post 4 Gy, BGI).
- No equations, no kinetic model, no simulation, no code.

Logged 8 primary scientific claims (see FIRST_PASS_REPORT.md claim matrix). All claims rest on flow-cytometry mean ± SEM with Student's t-test (GraphPad Prism 6.01) on n=3–6 mice/group.

## 2026-06-09 13:25 — Smoke script + report write-out

- `code/smoke_check.py` parses the qPCR primer table from JATS XML, reasserts the 10-gene primer set, and writes `results/smoke_output.json` with harvest verdict + deposit probe results.
- FIRST_PASS_REPORT.md drafted with claim matrix, what-would-be-needed, friction tags, verdict.
- MANIFEST.json with checksums.
- JSON progress record at `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-rprm-egfr-hsc-irradiation.json`.

## 2026-06-09 13:27 — Done

Verdict: **scoping complete, no runnable replication possible from public artifacts; recommend QA retag**.

Heavy compute on CherryRd: **none used**, none planned (paper has no computational content to run).
