# PARSER_PROVENANCE.md

## Paper source
- **Self-sourced (PASS-2, 2026-06-23):** `paper/paper.pdf` (1,287,445 bytes, 8 pages, PDF v1.6)
  - Origin: `https://europepmc.org/articles/PMC8448721?pdf=render`  (PMC native PDF was POW-challenged)
  - DOI: 10.1007/s10482-021-01637-0  PMID: 34463860  PMC: PMC8448721
  - Journal: Antonie van Leeuwenhoek, 114(10):1721-1733 (2021)
- **PASS-1 source:** abstract + structured metadata via PubMed/PMC E-utilities (no PDF on disk; `paper/paper_notes.md` was created by hand-curating the abstract + selected tables).

## Parser(s) used
- **PASS-1 (original subagent, 2026-05-05):** PubMed E-utilities `esummary.fcgi` + `efetch.fcgi?db=pubmed&retmode=xml` (text-only); supplementary table data hand-typed into `paper/paper_notes.md`. No PDF parser was used; therefore Tables 1-3, Figs 1-3, and the OXA/16S phylogeny details were captured only as summary numbers, not as machine-parsed evidence.
- **PASS-2 (this re-pass, 2026-06-23):**
  - PDF acquired with `curl` (User-Agent Mozilla/5.0) → `paper/paper.pdf`.
  - Read with the `pdf` tool (Anthropic native PDF) and with `pdftotext -layout` (poppler) for table extraction.
  - Tables verified against `paper/paper_notes.md`; any discrepancies recorded in the re-pass section of `report/REPORT.md`.

## Re-pass code/output layout
- New code lives under `code/repass/`
- New outputs land under `results/repass/`
- Pass-1 report preserved verbatim as `report/REPORT.pass1.md`
- Re-pass report overlays `report/REPORT.md`
