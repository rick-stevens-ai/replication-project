# Parser provenance — OSTI 1997354

## Paper source
- `1997354.pdf` (268,667 bytes, OSTI fetch, Apr 5 2026)
- Published version: Journal of Integer Sequences, Vol. 26 (2023), Article 23.6.6
- Authors: Steven Schlicker, Roman Vasquez, Rachel Wofford
  (NB: the OSTI catalogue listed authors as "Bobrowski, Elpers, Helmkamp,
   Ovsyannikov, Xique" — that is metadata noise; the paper PDF carries the
   three real authors above. Repass uses the PDF as canonical.)

## Canonical text parse
- **Tool:** Poppler `pdftotext` v25.x via `/usr/local/bin/pdftotext`
- **Output:** `/Users/stevens/.openclaw/workspace/tmp-pdf/1997354.txt`
  (1,585 lines, full PDF body extracted as plain text)
- **Command:** `pdftotext 1997354.pdf 1997354.txt`
- **Fidelity:** Math glyphs (subscripts, multiplication dot, en-dash) are
  preserved as Unicode characters. Sub/superscripts collapse to `n−1`
  / `n−3` notation. We hand-transcribed the 24 closed-form polynomials in
  Tables 1, 2, and 3 from this plain-text dump.

## Why no `pdf` tool model parse
- The OpenClaw `pdf` analyzer tool returned `400 Bad Request` (Anthropic
  credit balance exhausted at the moment of the repass), and the
  fallback Gemini/GPT-5 models were unavailable or unsupported. So we
  parsed locally with `pdftotext` and verified every transcribed formula
  against the recurrence (Section "Repass step 3" of the report) AND
  against the OEIS canonical-formula text for each cited sequence.

## Pass-1 source code
- `replication/src/edge_covers.py` (10,030 bytes, Apr 18 2026) implements
  all 11 functions (E, E1, E2_k, E3_k) with exact integer arithmetic and
  `lru_cache`. Repass reuses it unchanged via `PYTHONPATH=replication/src`.
- `replication/src/brute_force.py` (5,726 bytes) and
  `replication/src/oeis_verify.py` (6,072 bytes) — pass-1 brute-force and
  OEIS-pulling utilities; not invoked from the repass script (which has
  its own brute-force and OEIS-fetch routines for clarity).
- `replication/tests/test_formulas.py` — 8 unit tests, all PASS as of
  2026-06-23 (`pytest tests/` with `PYTHONPATH=src`).

## Repass script
- `code/repass/repass.py` (~27,900 bytes) — single self-contained script.
  Imports the pass-1 `edge_covers` module, then runs 7 verification
  steps writing JSON/CSV under `results/repass/`.
- **OEIS data source:** live HTTP GET against
  `https://oeis.org/<AID>/b<num>.txt` with a 10-second timeout and
  graceful fallback. Each match is recorded with the alignment shift
  (n value of the OEIS first term).
- **Runtime:** ~1.5 seconds total. No GPU. No private data. Free Argo /
  cherryrd CPU only.

## Known OCR / paper artefacts surfaced by the repass
1. **Paper Table 3, row `E3_3(5, n)`** prints the closed form as
   `3·31^(n−1) − 11·15^(n−1) + 15·7^(n−1) − 3^(n−1) + 2`.
   This conflicts with the recurrence by exactly `8·3^(n−1)`. The
   OEIS-canonical formula for A340434 (registered by Andrew Howroyd,
   Nov 11 2025) is
   `a(n) = 3·31^(n−1) − 11·15^(n−1) + 15·7^(n−1) − 3^(n+1) + 2`.
   The paper has a typo: it should read `−3^(n+1)` not `−3^(n−1)`.
   The recurrence (Theorem 12 + Theorem 11) is correct; only the
   typeset closed form in Table 3 is wrong.
2. **OEIS offset convention.** For the Table-3 sequences A340403/4/5,
   A340433/4/5, A340437/8, A341551, A341553, A342327/8, A343373/4,
   A343800, the OEIS b-file's first value corresponds to `n = m − 1`
   (via symmetry E(m,n)=E(n,m)), not `n = m` as the table caption
   suggests. The repass handles this by searching for the alignment
   shift; all 19 sequences match without modification of the
   recurrence values.
