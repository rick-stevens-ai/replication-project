# Extraction artifacts

Marker (`marker_single`) and Nougat (`nougat`) are not installed on this
replication host (CherryRd) and the shared UICGPU parse cluster was
unreachable within this subagent's timeout budget on 2026-07-05.

The paper is a 7-page math/physics arXiv PDF (born-digital, LaTeX), not a
scan. `pdftotext` recovers the full body text faithfully (equations render
as inline mathy text — sufficient for LLM-judge / textual downstream use).

- `marker.md` — Markdown-style fallback assembled from `pdftotext` output
  (labelled clearly at the top as a fallback, not a genuine Marker parse).
- `nougat.mmd` — MMD-style fallback assembled from `pdftotext -layout`
  output (labelled clearly at the top as a fallback, not a genuine Nougat
  parse).

If Marker/Nougat become available on this host, both files can be
overwritten in-place with genuine parses; the replication result does not
depend on which extraction is used (the numeric replication was done
directly from the PDF math, not from an extracted representation).
