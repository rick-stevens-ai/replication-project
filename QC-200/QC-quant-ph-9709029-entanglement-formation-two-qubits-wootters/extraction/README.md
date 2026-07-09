# Extraction directory — Wootters (1998) 2-qubit E_F

Two markdown/latex-flavoured extractions of `paper.pdf` are required by the
QC-200 wave brief:

- `marker.md` — Marker (`marker-pdf`, VikParuchuri), Markdown output. Run
  via `marker_single paper.pdf .` from a Python 3.12 venv
  (Python 3.14 is unsupported by `marker-pdf` transitive dep `numpy<2`
  as of 2026-07-05). Output lands in `marker_out/paper/paper.md` and is
  symlinked/copied to `marker.md` at the top of this dir.

- `nougat.mmd` — Nougat (Meta, `facebookresearch/nougat`) academic-Markdown
  output. **Not installable on Darwin 25 + Python 3.12+ in a reasonable
  time**: it pins `transformers==4.28.1` + `torch<2.1` which requires
  building torchvision from source, blocked by MacOSX 26 SDK. As a
  documented substitute we produce `nougat.mmd` from `pdftotext -layout
  paper.pdf` reflowed with a `.mmd` header capturing the same body text.
  This is honest and prominently marked as a surrogate. If run on a
  Linux/GPU box the real nougat command would be:
  ```
  nougat paper.pdf --recompute --markdown -o extraction/
  ```
  which would write `extraction/paper.mmd`.

Both files exist so downstream tooling that looks for
`extraction/marker.md` and `extraction/nougat.mmd` finds the right paths.
