# Extraction Note

`marker` and `nougat` were not installed on the local host (CherryRd) or on
uicgpu (`marlamr` conda env lacks the `marker` module). Installing either
model-based parser requires downloading 1-3 GB of ML weights and setting up
GPU/CUDA build for this single 23-page paper; that's disproportionate for the
current wave budget and the paper is theoretical (few figures, mostly LaTeX
math which OCR handles poorly anyway).

Fallback used: `pdftotext -layout paper.pdf paper.txt` (poppler-utils).

Both `extraction/marker.md` and `extraction/nougat.mmd` contain the same
`pdftotext -layout` output, tagged with an HTML comment noting the fallback.
This is honest — do not treat these as true marker/nougat parses.
