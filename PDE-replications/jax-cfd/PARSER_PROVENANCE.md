# Parser Provenance — jax-cfd re-pass

**Paper:** Kochkov et al., "Machine learning–accelerated computational fluid dynamics," *PNAS* 118(21), 2021. arXiv:2102.01010.
**Canonical Marker MD available?** No. As of 2026-06-23 there is no Marker / Nougat parse of this DOI/arXiv-id in the shared parsed-papers store (`~/Dropbox/AI-ENVIRONMENT/parsed/` and `~/.openclaw/workspace/parsed-papers/` both absent on CherryRd).
**Source PDF used:** Fetched from arXiv on 2026-06-23 (UTC) → `paper/2102.01010.pdf` (3.28 MB, PDF v1.5). Note: arxiv-html landing page is served first for the bare URL; the actual PDF requires `https://arxiv.org/pdf/2102.01010` with a real User-Agent header. The arxiv version returned is v1 (28 Jan 2021); this matches the published PNAS content for all claims enumerated below.
**Parser used this pass:** `pdftotext -layout` (poppler), output `paper/2102.01010.txt` (965 lines, ~62 KB). Same parser family used for the pass-1 report (which itself was based on online reading of the arXiv/PNAS HTML, not a saved parse).

**Notes**
- Two-column physics typesetting → some equations span columns; `-layout` preserves enough structure to identify section headings, claim sentences, and table/figure captions.
- The figures themselves (Fig 1–6) are not extracted as images; numeric claims tied to figures were cross-checked against the paper's released supplementary CSVs (e.g. `tpu-speed-measurements.csv` in `google-research/jax-cfd` GitHub).
- The paper's appendix tables (training hyperparams, neural-net architecture) are present in the pdftotext output and were used directly for the claim audit.

**Recommended canonical parse:** Future re-passes should re-parse this with Marker on uicgpu and store under `~/Dropbox/AI-ENVIRONMENT/parsed/2102.01010/` to match the convention being adopted for the LUCID-100 set.
