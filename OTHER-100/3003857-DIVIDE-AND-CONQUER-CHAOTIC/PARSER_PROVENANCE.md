# Parser Provenance — OSTI 3003857

**Paper:** Chakraborty, Chung, Arcomano, Maulik (2024).
*Divide and Conquer: Learning Chaotic Dynamical Systems with Multi-Step Penalty Neural ODEs.*
arXiv:2407.00568v5 (15 Oct 2024).

## Source files

- `paper.pdf` — full v5 preprint (11.7 MB), present in the directory since 2026-04-21.
- `paper.txt` — pre-extracted plain-text rendering (74,827 bytes / 1,554 lines), present since 2026-04-21.

## Re-pass parser

For the re-pass (2026-06-23) I did **not** re-fetch the paper. The pre-existing
`paper.txt` was already in the working directory and was inspected directly with
`grep`/`sed`/`head`/`tail` for:

- Section/subsection headers and figure captions (`grep -nE "(Figure|Fig\.|Table|Algorithm) [0-9]+"`)
- Lorenz-63 control problem definition (Section 4.1)
- KS equation setup, Lyapunov time, training data range (Section 4.2)
- Kolmogorov flow architecture, hyperparameters, SWA description (Section 4.3)
- ERA5 description (Section 4.4)
- Appendix Table 1: KL divergences for KS ablation (Section 6.2, p. 25)

No additional fetch from OSTI / arXiv was required; the local `paper.txt` covers
all sections including the appendix Table 1. The file appears to be a direct
pdftotext-style extraction (no markdown reflow; figure captions appear inline as
`Figure N: ...` lines).

## Sanity check

Cross-checked key quantities against `paper.txt`:

- "Lyapunov time τ_L ≈ 22" (KS) — confirmed l.~850
- Kolmogorov: A=1, k=4, r=0.1, Re=1000 — confirmed l.~912
- ERA5: Jan 2000 – Dec 15 2009, T30 Gaussian grid — confirmed l.~1000
- KS Table 1 best: MP-NODE 7 (µmin=10⁻⁴, T=75 steps, K=25 discontinuities, KL=0.02915)
  — confirmed l.~1528–1547

The text extraction faithfully preserves the appendix Table 1, which is the
single highest-fidelity quantitative benchmark in the paper for the KS system.
