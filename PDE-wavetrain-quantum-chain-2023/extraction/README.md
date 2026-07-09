# Extraction provenance

- `paper.txt` — pdftotext -layout (poppler) of `../paper.pdf`.
- `marker.md`, `nougat.mmd` — **substitute** extractions (identical to paper.txt).
  Marker and Nougat were not installed on this host (CherryRd), and no
  pre-parsed copy of arXiv:2302.03725 was available in the central corpus.
  These files are the honest pdftotext output preserved under the standard
  filenames so downstream tools can find them; they do not carry Marker/Nougat
  structural markup and should not be treated as such.

If a real Marker/Nougat parse becomes available in the SCOUT/LUCID/OSTI
manifest, it should overwrite these files.
