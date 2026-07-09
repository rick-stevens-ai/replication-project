# Artifact Harvest

| Artifact | URL | Notes | Size / checksum |
|---|---|---|---|
| Paper landing page (OA, Iraqi J. Science / OJS) | https://ijs.uobaghdad.edu.iq/index.php/eijs/article/view/1496 | Open Access, no paywall; resolves from DOI 10.24996/ijs.2020.61.2.24 (HTTP 200) | HTML |
| Full-text PDF (galley 1310) | https://ijs.uobaghdad.edu.iq/index.php/eijs/article/download/1496/1310 | 9 pages, pp.444-452 | 687206 B, MD5 9905e28d1b0e1c1f141d1090ee7b3c53 |

## Data / code availability
- The paper provides **no** external data or code repository. It is a self-contained
  numerical-methods paper built entirely on two **manufactured (method-of-manufactured-
  solutions) test cases** with closed-form exact solutions specified in the text.
- Therefore replication does not require downloading external data: the "data" are the
  paper's own analytic test problems (coefficients, free boundaries, exact solutions,
  and error tables), which are fully transcribed from the OA PDF and re-derived here.

## Extraction method (no paid PDF tool used)
- PDF fetched via `curl` from the publisher OA galley.
- Text via `pdftotext -layout` (dropped math glyphs -> unreliable for equations).
- Equations recovered by rasterizing pages with `pdftoppm -r 300` and running local
  `tesseract` OCR (free, offline) on full pages and targeted crops (PIL).
- Vision LLM OCR was attempted but unavailable (no free image endpoint; Anthropic
  credit exhausted) — tesseract was sufficient to transcribe all governing equations,
  both test cases, and both error tables.
