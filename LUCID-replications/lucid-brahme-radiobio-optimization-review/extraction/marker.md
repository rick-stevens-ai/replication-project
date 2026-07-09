# extraction/marker.md — pdftotext-derived stub

**Status:** stub (pdftotext-derived, not a true Marker parse).
**Reason:** No GPU allocation attached during the 2026-06 audit passes
or the 2026-07-06 backfill. A proper Marker parse is pending the
central Eagle corpus sweep.

**Resolve later by SHA-256:**
`b768585e326b83b9e51165978c9fe3a1a9711d369762ea65b442e9077fcd00b9`
against `/eagle/projects/AuroraGPT/stevens/scout_corpus/md/<sha256>.md`.

**Paper text (208,293 B, 2,159 lines, pdftotext -layout) is already on
disk as `../paper.txt`.** For most narrative-level tasks, `paper.txt`
is adequate. It does **not** recover:

- The Figure 15 tabular insert (γ_C / σ_D/D̄ / RBE per modality).
- Text embedded inside conceptual diagrams (Figs.\,7, 8, 11, 13-18, 37, 38).
- Vector-annotation labels.

If any of the above matter for a downstream task, run Marker or Nougat
against `../paper.pdf` on a GPU node and replace this stub.

## Metadata

- Title: New Radiation Oncology Optimization Principles Based on
  In-Vivo Predictive Assay and Recent Developments in Molecular
  Radiation Biology
- Author: Anders Brahme
- Venue: *Annals of Case Reports* 9:1625 (Gavin Publishers), 2024
- DOI: 10.29011/2574-7754.101625
- OA source URL: gavinpublishers.com/assets/articles_pdf/New-Radiation-Oncology-Optimization-Principles--Based-On-In-Vivo-Predictive-Assay-and-Recent-Developments-in-Molecular-Radiation-Biology.pdf
- paper.pdf: 4,693,885 bytes, PDF 1.7
- SHA-256: b768585e326b83b9e51165978c9fe3a1a9711d369762ea65b442e9077fcd00b9
