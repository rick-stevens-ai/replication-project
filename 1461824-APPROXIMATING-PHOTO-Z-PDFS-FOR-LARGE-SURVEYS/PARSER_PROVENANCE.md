# PARSER_PROVENANCE — 1461824 (Malz+ 2018, photo-z PDF approximation)

## Canonical parse search
- No prior canonical parse found in this project directory (no `paper.md`, no `paper_parsed/`, no `parsed_*.json`, no `marker_output/`).
- The only "parsed" artifacts that existed before this repass were narrative replication notes (`replication/replication_report.md`, `replication/results.json`) — these are derivative reproduction outputs, not a source-of-record parse of the paper.

## Parser used for this repass
- **poppler / pdftotext (with `-layout`)** on `1461824.pdf` → `/Users/stevens/.openclaw/workspace/1461824_photoz.txt`.
- Plain-text inspection (no model-based PDF extraction; the in-tool `pdf` analyzer was unavailable on this run — Anthropic returned a billing error, Google returned an unknown-model error, and the local pdf extractor plugin is disabled — so we deliberately fell back to `pdftotext` + targeted grep on the layout-preserving text dump).
- Used grep over the layout text to enumerate claims, then read sections 2 (formats/metrics), 3 (datasets), 4 (results), 5 (conclusions) and the Appendix (KLD intuition with Figures 9 and 10) directly.

## Why this matters
- The Appendix contains closed-form Gaussian KLD identities (Eq. 11 and the limiting cases) that are **testable without any survey data** and were not exercised in pass 1.
- Figures 7 and 8 give per-format×Nf curves for the stacked n̂(z) KLD and stacked-n̂(z) moment percent errors that pass 1 only reproduced visually; the repass extracts and tests them quantitatively where possible.

## Conformance note on figures
- The paper reports per-format curves through figures (no in-text numerical tables for Figures 4/5/7/8). For quantitative repass we read the figure curves' qualitative shape (sign, ordering, asymptote) and check against our reproduction.
- This means the repass agreement metric for figure-derived claims is necessarily a **shape/ordering** match, not an exact-value match.
