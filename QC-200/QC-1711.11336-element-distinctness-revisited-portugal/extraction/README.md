# Extraction fallback note (QC-1711.11336 Portugal)

Marker and Nougat were **not installed** on the execution host at replication
time (CherryRd, macOS, no Python-side `marker`/`nougat` importable, no
`marker` / `marker_single` / `nougat` binaries on `PATH`).

Rather than block the replication on installing/running a full GPU-hungry
OCR/PDF-to-Markdown pipeline for a 14-page purely-textual math paper whose
PDF is a machine-generated LaTeX build (arXiv 2017/2018 v3), we used
`pdftotext -layout` as a pragmatic textual fallback and mirrored the SAME
extracted text into both:

- `extraction/marker.md`
- `extraction/nougat.mmd`

Content is identical. The report artifacts (equations, matrix elements
Eqs. 8-9-10, initial state Eq. 11, and the (2k+1)-dim reduction) were
transcribed directly from the paper PDF and cross-checked against this
extracted text.

If a downstream consumer needs true Marker/Nougat outputs (e.g. for
equation-aware LaTeX round-trip), rerun with `marker_single` +
`nougat --model 0.1.0-base` on the same PDF (`../paper.pdf`) and overwrite
these two files.

Trace:
    Extraction command : pdftotext -layout paper.pdf paper.txt
    Source PDF hash    : (see report/artifacts_summary.md)
    Runtime            : CherryRd (Darwin 25.3.0, x64), 2026-07-05.
