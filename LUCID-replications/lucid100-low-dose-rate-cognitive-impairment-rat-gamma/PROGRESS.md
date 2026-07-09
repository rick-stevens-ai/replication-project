# PROGRESS — LUCID100 Wave 6 slot 55 (Ma et al. 2024, fpubh.2024.1387330)

## 2026-06-09 — first pass (subagent depth 1)

1. **Identified record** in `LUCID100_SOLID_MASTER_QA.tsv` at rank 86 (Wave 6, tier B, priority 13). Status was `candidate_curated`, worktype tag `omics/signature replication`.
2. **Created folder** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-low-dose-rate-cognitive-impairment-rat-gamma/`.
3. **Fetched** open-access PDF (5.8 MB) and article landing HTML — Frontiers OA CC-BY.
4. **Discovered SM URLs** via OpenClaw browser (initial REST guesses 404'd; the real URL pattern is
   `https://public-pages-files-2025.frontiersin.org/articles/<ID>/file/Data_Sheet_N.zip/<token>_supplementary-materials_datasheets_N_zip/2` ).
5. **Downloaded all 3 supplementary zips** (Data_Sheet_1.zip 30 MB, Data_Sheet_2.zip 12 MB, Data_Sheet_3.zip 15 MB) → 100 files total: 11 xlsx, 19 SPSS/GraphPad stat files, 70 original-image files.
6. **Downloaded** 9 publication figure JPGs from Frontiers images CDN.
7. **Catalogued** xlsx contents — per-figure raw data with explicit Control/LDR/HDR group labels, full n=8 per group for behavior.
8. **Built** `scripts/smoke_replicate.py` covering 9 quantitative anchors:
   - Figure 1 NOR DI 2w/4m (Kruskal-Wallis re-derivation)
   - Figure 1 Y-maze 4m
   - Figure 1 SAB 2w
   - Figure 7 DEG counts (210 LDR, 329 HDR)
   - Figure 8 PI3K-Akt enrichment present in both
9. **Smoke result: 9/9 PASS** on first run.
   - All KW p-values within expected ranges (0.001 < p < 0.025).
   - DEG counts exact match to paper text (210, 329).
   - PI3K-Akt KEGG row found in both LDR and HDR annotation tables.
10. **Worktype retag recommendation** added to README: this is a wet-lab in vivo study with partial omics summary tables, NOT a pure omics replication. Raw FASTQ not deposited publicly.
11. **Verdict:** GO at table/figure/qualitative level. No-go for read-realignment without author contact.
12. **Progress JSON** written to `~/.openclaw/workspace/memory/subagent-progress/`.

### Blockers encountered

* Initial supplementary download URL guesses returned HTML 404 pages stored as `.zip` (size ~10 KB each). Resolved by using the OpenClaw browser to evaluate the real DOM links.
* One file in Data_Sheet_3 (`β-actin.tif`) had a unicode-β filename that unzip stumbled on; the file is recoverable but the qualitative WB direction is already captured by `WB.xlsx`, so left as-is.

### No follow-ups required for first-pass deliverable.
