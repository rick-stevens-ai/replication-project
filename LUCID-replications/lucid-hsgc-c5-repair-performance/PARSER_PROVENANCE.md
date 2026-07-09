# PARSER_PROVENANCE

**Re-pass date:** 2026-06-23
**Source PDF:** `data/paper.pdf` (sha256 `49bd0f0e5286145da48f3200ddddad6e1d527901ea4976d7ad4f12a7bb5be861`, 737,445 bytes)
**Original sha-named PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d.pdf`

## Parser used for the re-pass

**Canonical Marker output** from the LUCID-100 admin Marker batch
(`~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d/`).

Copied locally to:
- `data/marker/paper.md` — 380 lines, sha256 `8bc885e405b8254d24c2fffc170a3c9bc3cd2eef5b8167a7470f4a791902def0`
- `data/marker/paper_meta.json` — Marker page stats / TOC metadata

Marker batch produced on `uicgpu` on 2026-06-22. This is the canonical, project-wide LUCID-100 parser output and is what the re-pass enumerated claims against.

## Why this matters

- The original v1+v2 replication on 2026-05-30 used `pdftotext -layout` (`data/paper.txt`, 930 lines). That parser kept the body text fine but stripped figures, table structure was lossy, and inline math came out garbled (e.g. paper Eq 6 PDF artifact `SF = ln(-Lf)` survived into the text).
- Marker output preserves table 1 / table A1 as clean Markdown tables (verified by direct read), keeps inline math much closer to the source, and labels the figure JPEGs (e.g. `_page_8_Figure_1.jpeg` = Figure 4 DSB yields plot, `_page_8_Figure_4.jpeg` = Figure 5 SF/FAR composite, `_page_12_Figure_3.jpeg` = Figure A1 NB1RGB).
- Using the Marker text I was able to enumerate **5 previously-missed testable claims** (M1, M2, M3/M5, M7+M11, M9+M10) — see `REPORT.md` re-pass section. The Appendix A NB1RGB material (M9, M10) had been entirely skipped in the 2026-05-30 pass.

## Supplement provenance (unchanged from original)

- `data/supplement.zip` — 3,590 bytes, fetched 2026-05-30 from
  `https://res.mdpi.com/d_attachment/cancers/cancers-13-06046/article_deploy/cancers-13-06046-s001.zip`
- `data/supplement/SF.csv`  sha256 `96a523aee5d39bfe56afe514ace982119d9fcc51a07a5f1a4c3f199e04642cb1`
- `data/supplement/FAR.csv` sha256 `3009deb95872afdabd253524810b339c1be7fdb7f137aba04bb139e936f9d1b8`
- `data/supplement/DepthDose.csv` sha256 `368da6269d03bd6f93ce7bbe5f6d7b97818e9e9123364cba942dd6cddeaad5b0`
