# Extraction directory — Poremba (2023) Quantum Proofs of Deletion for LWE

Two markdown/latex-flavoured extractions of `paper.pdf` are required by the
QC-200 wave brief:

- `marker.md` — Marker (`marker-pdf`, VikParuchuri), Markdown output.
- `nougat.mmd` — Nougat (Meta, `facebookresearch/nougat`) academic-Markdown output.

**Both native extractors are unavailable on this host as of 2026-07-05:**

- `marker-pdf` (v0.2.6) fails with an internal
  `TypeError: Invalid input type 'PdfDocument'` at
  `pdftext.extraction._load_pdf` on Darwin 25 + Python 3.12/3.14 with
  the `pypdfium2 == 4.30.0` combination we could install.
- `nougat` pins `transformers==4.28.1` + `torch<2.1`, which requires
  building torchvision from source, blocked by the MacOSX 26 SDK on
  m1/CherryRd. Not installable in reasonable time.

As documented substitutes we produce:

- `marker.md` — `pdftotext -layout` output reflowed as GFM with a title
  header, honest surrogate marker prominently at the top.
- `nougat.mmd` — same body text with a Nougat-style `--- ... ---` YAML
  header. Content is identical to `marker.md`; only the header/format
  differs (real Nougat would produce LaTeX-flavoured output; ours does not).

If run on a Linux/GPU box the real commands would be:

```
marker_single paper.pdf .
nougat paper.pdf --recompute --markdown -o extraction/
```

Both files exist so downstream tooling that looks for
`extraction/marker.md` and `extraction/nougat.mmd` finds the right paths.

This mirrors the sibling QC-200 replication
(`QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters/extraction/`)
which used the same fallback under the same Darwin 25 + m1 constraints.
