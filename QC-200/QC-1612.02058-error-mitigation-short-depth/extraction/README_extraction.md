# Extraction fallback note (2026-07-05)

Both **`marker.md`** and **`nougat.mmd`** in this directory are pdftotext-based fallbacks,
not real Marker (VikParuchuri/marker) or Nougat (facebookresearch/nougat) parses.

**Why:**
- Neither `marker_single` nor `nougat` CLIs are installed in the replication env used
  for QC-200 wave 2026-07-05.
- The central `~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTED/` corpus does not exist yet
  (`ls` returned no match), so we could not pull a canonical parse.
- Installing Marker (torch + tesseract) or Nougat (torch + custom checkpoints) on the fly
  would blow the wave budget and download several GB.

**What we did instead:**
- `pdftotext paper.pdf paper.txt` → prepended a short header and used the raw text as
  BOTH `marker.md` (with Markdown wrapper) and `nougat.mmd` (with LaTeX wrapper).
- This is a **lossy substitute**: equations, figures, tables and section hierarchy are
  not marked up. But the paper's linear textual content — including the derivation of the
  Richardson coefficients (Eq. 3-4), the noise-model definitions, and the numerical-example
  descriptions — is fully present, and that is what the replication actually depended on.

**Follow-up (if wave sponsor wants clean parses):** re-run Marker + Nougat against
`paper.pdf` from a GPU host and drop the outputs in place; downstream reports do not
depend on the parse structure.
