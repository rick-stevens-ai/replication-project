# PARSER_PROVENANCE

**Date:** 2026-06-23 (re-pass)
**Operator:** Ollie subagent (Re-pass chiral-spin)
**Source artifact:** `1412756.pdf` (BNL-114729-2017-JA, Tsvelik & Yevtushenko, Sep 2017 draft of PRL submission)

## Parser used

- **Tool:** Poppler `pdftotext -layout` (Poppler 25.x, installed at `/usr/local/bin/pdftotext`)
- **Command:** `pdftotext -layout 1412756.pdf /tmp/1412756.txt`
- **Output size:** 60,907 bytes, full body + supplementary 1A/1B/1C/1D + section 2 (order parameters) + section 3 (charge/spin connection) recovered cleanly, including all equations 1–10 and supplementary 11–42.

## Notes

- `mutool` not present on CherryRd; Poppler `pdftotext -layout` was sufficient.
- The PDF is a born-digital BNL preprint (not a scan); OCR was not required.
- Greek letters and bracketed/inline math survived as ASCII placeholders (`α → α`, `J̃_H → J~H`, etc.) — readable but every numeric coefficient and equation form was preserved.
- All `Eq.(n)` and `Suppl.Mat.X` references resolved against the layout output.

## Claims index built from parser output

Eqs. (1)–(10) main text + Suppl. (11)–(42) used to enumerate testable claims.
See `REPORT.md` (post-repass) for the full claim ledger and which were already
covered by pass-1 vs newly covered by this re-pass.
