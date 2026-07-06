# PARSER_PROVENANCE.md — ScaWL re-pass

**Canonical text extracted with:** `pdftotext -layout` (Poppler 25.x via `/usr/local/bin/pdftotext` on CherryRd)

**Source PDF:** `2587225.pdf` (2,344,219 bytes, OSTI 2587225 = ACM TACO Vol. 22 No. 1 Article 45, March 2025, DOI 10.1145/3715124)

**Canonical text:** `~/.openclaw/workspace/repass-scawl/scawl.txt` (1,278 lines)

**Parse sanity checks (all PASS):**
- Title line 1 = "ScaWL: Scaling k-WL (Weisfeiler-Lehman) Algorithms in"
- DOI line 49 = `https://doi.org/10.1145/3715124`
- Table 1 (Datasets, line ~723) rendered with vertices/edges/min/max columns; example: `LFAT5 14 30 2 5`, `Trefethen_20 20 89 6 6`, `celegansneural 297 4,690 0 134`.
- Table 2 (Raw runtimes + speedups) line ~860–880 rendered with the per-graph rows readable (`ScaWL 662_bus 7.23s vs K-WL speedup 2,193.6`).
- §6.3 (line ~890) explicit numeric averages found:
  - 2-WL single-node speedups: 2.38, 4.26, 7.64, 13.20, 16.06 (cores 2/4/8/16/20).
  - 3-WL single-node speedups: 1.91, 3.36, 6.04, 10.63, 12.69 (cores 2/4/8/16/20).
- §6.4 averages found: 2-WL multi-node 1.53/2.06/3.20 (2/4/8 nodes); 3-WL 1.54/2.33/3.25.
- Figures 7–14 referenced by caption text (no raw figure data extracted).
- References list (1–31) intact through line 1278.

**No OCR was used.** Native text layer is clean; `pdftotext -layout` produced rich tables we can ground claims against.

**Re-pass timestamp:** 2026-06-23 (Tue) on CherryRd; pdftotext invocation reproducible.
