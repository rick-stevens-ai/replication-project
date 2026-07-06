# PARSER_PROVENANCE.md — Lightning Laplace replication, re-pass

**Repass date:** 2026-06-23
**Operator:** Ollie (subagent, Argo Claude Opus 4.7)
**Host:** CherryRd (M1 iMac, CPU only, free compute)

## Canonical parse

- No prior canonical structured parse (`.repcache/parse.json`, `claims.yaml`,
  etc.) was found under
  `/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/lightning-laplace/`
  or `~/Dropbox/REPLICATE-PROJECT/PARSED/` for this paper.
- Used **pdftotext (poppler-utils, layout mode)** on
  `refs/gopal-trefethen-2019.pdf` to extract a 394-line text representation,
  then manually enumerated every numerical / algorithmic claim from the
  resulting text. Paper is short (≈7pp PNAS-style; full arXiv 1902.00374v1),
  so manual enumeration is exhaustive rather than sampled.
- Extracted text staged at `/Users/stevens/.openclaw/workspace/tmp-pdf/gt2019.txt`
  (working copy, not committed).
- No LLM-side hallucinated values: every claim re-checked in the extracted
  text and cross-referenced with the included authors' MATLAB reference code
  (`refs/laplace.m`, `refs/examples.m`).

## Why no formal parser

- This is a short PNAS-style note (6 pages of text + 4 figures, single L-shape
  numerical experiment + Helmholtz sketch). A full claim-extraction pipeline
  was unnecessary.
- The pass-1 REPORT.md already grouped paper claims into a 5-row
  claim-by-claim table; the re-pass extends that table with previously
  unchecked items (point-evaluation timing, max-principle bound, sigma
  sensitivity, exact NA Digest probe value, etc.) read directly from the PDF.

## Versions

- pdftotext: `pdftotext version 25.05.0` (poppler-utils via Homebrew on
  CherryRd).
- Python: 3.x system / venv on CherryRd (numpy + scipy only — no torch / no
  MATLAB required for the re-pass).
