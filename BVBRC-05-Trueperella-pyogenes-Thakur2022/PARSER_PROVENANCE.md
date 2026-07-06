# Parser Provenance — Pass 2 (Re-pass for coverage lift)

**Run date:** 2026-06-23
**Paper:** Thakur et al. 2022, *Antibiotics* 12:24, DOI 10.3390/antibiotics12010024
**PDF source:** `paper/thakur2022.pdf` (SHA-256 verified in checksums; size 3,510,423 bytes)

## Parser pipeline

1. **Text layer extraction:** `pdftotext -layout /paper/thakur2022.pdf /tmp/thakur2022.txt`
   - Tool: `pdftotext` (poppler-utils, /usr/local/bin/pdftotext on macOS)
   - Mode: `-layout` (preserves table column alignment for Table 1 / Tables S* reproduction)
   - Output: 1429 lines, all body text + references + Tables 1, 7-bound facts visible.
2. **Claim enumeration:** human read of full extracted text, cross-checked against:
   - Pass-1 report (`report/REPORT.pass1.md`)
   - Pass-1 supporting analysis files (`analysis/prokka/*.txt`, `analysis/roary/summary_statistics.txt`, `analysis/ani/`, `analysis/amr/`, `analysis/virulence/`)
3. **No paid PDF model was used.** Anthropic / OpenAI `pdf` tool failed (credit / unavailable). All claim extraction is from local `pdftotext` output, which is fully reproducible.

## Tables / figures relied on

- **Table 1** — per-strain bases, GC%, CDS, rRNA, tRNA, tmRNA, repeat regions (RR). Cleanly recovered from `pdftotext -layout`.
- **Figure 9a** — GI count per strain (paper narrative: range 12-25, max SH02, min TP8).
- **Figure 9b** — prophage count per strain (paper narrative: range 1-4, max TP1 with 4).
- **Figure 10** — ARG presence/absence by strain (paper narrative: max SH01/SH02 (6) and TP1 (5); none in DSM20630, NCTC5224, Bu5, UFV1; tet(W/N/W) in 13/19; ermX in 7).
- **Sections 3.3, 3.4, 3.7-3.10** — quantitative claims (genome stats, pan-genome, VFs, GIs, prophages, ARGs).
- **Section 4** Discussion — repeats and refines counts ("346 GIs", "31 prophages") in some places that differ from the main figure caption ("206 GIs"/"190 GIs" abstract). Internal paper inconsistency noted explicitly in claims list.

## Internal inconsistencies in the paper (recorded, not "fixed")

- **GI total:** Abstract says **190**, Section 3.8 says **206**, Discussion says **346**. We test the per-strain range (12-25) and per-strain extremes (max SH02, min TP8) rather than the global total, because the global total is internally contradictory in the source.
- **Prophage total:** Abstract says **31**, Section 3.9 says **30** ("2 intact + 26 incomplete + 2 questionable"), Discussion says **31** ("2 intact + 2 questionable + 27 incomplete"). Range 1-4 and max-in-TP1 are consistent across sections; we test those.
- **Singleton total:** Section 3.4 says **307**, Discussion says **310** ("31.29% out of 310"). We treat range (2-63) and "0 singletons in TP3/TP6375/TP4479/TP-2849" as the canonical sub-claims.
- **Pan-genome CDS:** 3214 in Section 3.4; "3215 on addition of 19th genome" in Figure 3a narrative. Treated as ~3214-3215.
