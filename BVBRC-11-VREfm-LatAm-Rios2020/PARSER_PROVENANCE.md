# PARSER_PROVENANCE.md
**Project:** BVBRC-11-VREfm-LatAm-Rios2020
**Re-pass date:** 2026-06-23
**Operator:** Ollie (OpenClaw subagent) for Rick Stevens

## Canonical PDF parse

The primary source files are:
- `paper/rios2020.pdf` — Rios et al. 2020, Sci Rep 10:5636 (open access)
- `paper/supp_info.pdf` — Supplementary material with Tables S1–S4

### Parser used (re-pass)
- `pdftotext` (Poppler) v25.x at `/usr/local/bin/pdftotext`
  - `pdftotext paper/rios2020.pdf rios2020.txt` → 711 lines plain text
  - `pdftotext paper/supp_info.pdf supp_info.txt` → 25,956 lines plain text
- Output cached at `/Users/stevens/.openclaw/workspace/tmp/bvbrc11/`

### Parser fallback tried
- Hosted `pdf` extraction tool → unavailable (Anthropic billing 400; OpenAI extraction disabled).
- `ocr_pdf` Tesseract on PDF → failed (UnicodeDecodeError on every page; PDF contains JPEG-encoded images that broke text-fallback path).
- → `pdftotext` produced clean readable text for both PDFs; used as the canonical parse.

### Parser quality
- Main paper text: clean, all 12 pages legible, all reference numbers preserved.
- Supplementary text: Tables 1–3 preserved column-by-column (each column on its own line), readable with line offsets. Required attentive cross-referencing to map rows to columns.
- Supplementary Table 1 (LATAM isolates 55 + global 285) preserved with `Strain | Source | Country | Year | ST` columns.
- Supplementary Tables 2 & 3 (clade A subgroup prevalences) preserved with `Animal / CRS-I / CRS-II` columns.

## Pass-1 parser
The pass-1 parser produced `data/erv_accessions.tsv` (55 LATAM strains with accession, country, year, source, ST, subclade) — verified against Supplementary Table 1 in this re-pass and matches the paper. The pass-1 analysis is structurally sound; the re-pass focuses on testing additional claims, not re-parsing.

## Cross-check
- 55 LATAM isolates in `data/erv_accessions.tsv` ↔ 55 fastas in `data/genomes/` ↔ 55 MLST results in `data/mlst/mlst_results.tsv` ↔ 55 entries in `analysis/abricate/summary_resfinder.tsv` (header + 55).
- All counts internally consistent.
