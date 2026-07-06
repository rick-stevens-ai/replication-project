# Parser Provenance — OSTI 1523841

**Paper:** Fregoso, Morimoto, Moore (2017), "Quantitative relationship between
polarization differences and the zone-averaged shift photocurrent", arXiv:1701.00172v2.

## Source artifact
- File: `1523841.pdf` (1.41 MB), top-level of project dir.
- SHA-256: see below.

## Parser used for repass
- Tool: `pdftotext -layout` (Poppler) on macOS (Homebrew build).
- Command: `pdftotext -layout 1523841.pdf 1523841.txt` (produced /tmp/1523841.txt, 72 608 bytes, 759 lines).
- Output: machine-readable text including all equations, figure captions, and appendices.
- All equation numbers verified to match the PDF rendering (Eq. 9, 13, 16, 17, D1–D16, E1–E8).

No canonical paper-supplied "parser" exists (no LaTeX source, no machine-readable supplement); pdftotext was used as the structured-text source and the PDF was cross-checked visually for figure data.

## What was extracted
- Eq. (D1), (D2), (D4), (D5) — Rice-Mele Bloch Hamiltonian, Berry connections.
- Eq. (D8)–(D10) — analytic limits of shift vector.
- Eq. (D16) — explicit Rice-Mele shift conductivity σ^zzz(ω).
- Eq. (E1)–(E8) — three-band model Hamiltonian, eigenvectors, polarization, charge pumping.
- Eq. (9), (13), (16), (17) — central identities (single band, 1D three-band, 2D, multi-band).
- Section V — explicit 2D extension (two coupled RM models) prescription.

## Hash
- File: `1523841.pdf`
- SHA-256: see `sha256.txt`.

```
shasum -a 256 1523841.pdf
```
