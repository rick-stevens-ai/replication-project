# PARSER_PROVENANCE — Optimized Schwarz Helmholtz repass

**Date:** 2026-06-23 (re-pass)
**Operator:** Ollie (subagent), main agent: OpenClaw.

## Source files

- `paper_arxiv.pdf` — Gander, Magoulès, Nataf (2002), SIAM JSC 24(1), 38–60 (23 pages, GPL Ghostscript 9.10 output of a DVIPSONE TeX source). MD5: `41685f5d128ed6ce80a6c3877796b102`.
- `paper_ddm.pdf` — DD13 conference companion (8 pages, Aladdin Ghostscript 6.0). MD5: `2c81345ad0f9047d945ec33f3035c2d8`.

## Parser

- Tool: `pdftotext -layout` (poppler 25.x on macOS 25.3.0, `/usr/local/bin/pdftotext`).
- Re-run command: `pdftotext -layout paper_arxiv.pdf paper_arxiv.txt`
- Resulting text: 1543 lines, 100,361 bytes for `paper_arxiv.txt`.
- Equations are reasonably preserved as plain text; Greek letters / subscripts (ω, ω_-, ω_+, p*, q*, α*, β*) parse with no UTF-8 fallback issues.
- Tables 6.1 and 6.2 render with column alignment intact — direct visual diff against the original PDF figures confirms numeric values transcribed correctly.
- Figures (Fig. 4.1, 4.2, 6.1, 6.2, 6.3, 6.4, 6.5) appear as raster-converted text-noise blocks in the extract; relied on the PDF rendering for figure interpretation (Skim / Preview).
- No author code located on Geneva, GitHub, or HAL pages cited in the paper.

## What this parse reliably gives us (used as canonical numerical anchors)

- Theorem 3.1 eq. (3.7): OO0 optimal `p* = q* = ((ω²-ω_-²)(k_max²-ω²))^{1/4} / sqrt(2)`.
- Theorem 3.10 eqs. (3.20),(3.21): OO2 optimal `α*, β*`.
- Theorem 4.1 eq. (4.1): `ρ = 1 - 2 sqrt(2(ω²-ω_-²)^{1/2}/π) sqrt(h) + O(h)`.
- Theorem 4.2 eqs. (4.2) (propagating) and (4.3) (evanescent):
  - `ρ_p = 1 - 4 (2Δω)^{1/4} (1/ω)^{1/4} + O(1/√ω)`, `Δω = ω - ω_-`.
  - `ρ_e = 1 - 4 (ω_+² - ω²)^{1/4} / √π · √h + O(h)`.
- Eq. (6.1): model problem (unit square, Dirichlet top/bottom, 1st-order radiation at x=0,1).
- Table 6.1 (model problem, ω = 9.5π, ω between two modal frequencies):

  | h | OO0 iter | OO0 Krylov | Taylor (Robin) Krylov | OO2 iter | OO2 Krylov | Taylor2 Krylov |
  |---|---|---|---|---|---|---|
  | 1/50  | 457 | 16 | 26 | 22 |  9 | 28 |
  | 1/100 | 126 | 21 | 34 | 26 | 10 | 33 |
  | 1/200 | 153 | 26 | 44 | 36 | 13 | 40 |
  | 1/400 | 215 | 34 | 57 | 50 | 15 | 50 |
  | 1/800 | 308 | 43 | 72 | 71 | 19 | 61 |

  Taylor iterative columns are listed as "-" (do not converge as iterative).

- Table 6.2 (same model, ω = 10π directly **on** a problem frequency — only Krylov works):

  | h | Taylor-Krylov | OO0-Krylov | Taylor2-Krylov | OO2-Krylov |
  |---|---|---|---|---|
  | 1/50  | 24 | 15 | 27 |  9 |
  | 1/100 | 35 | 21 | 35 | 11 |
  | 1/200 | 44 | 26 | 41 | 13 |
  | 1/400 | 56 | 33 | 52 | 16 |
  | 1/800 | 73 | 43 | 65 | 20 |

- Figure 6.1 (left): on log–log iter vs h, OO0-Krylov slope `h^{-0.32}`, Taylor-Krylov slope `h^{-0.5}`. (Right) OO2-Krylov slope `h^{-0.27}`, Taylor2-Krylov slope `h^{-0.5}`.
- Figure 6.2: iteration-count contour vs (p, q) at h=1/50, `ω = 9.3596π`, `ω_- = 8.8806π`, `ω_+ = 9.8363π`. Star at the Fourier-predicted (p*, q*).
- Figure 6.3: same idea for (α, β) in OO2.
- §6.2 Volvo S90: 105 (Taylor) vs 34 (OO2) iters with 16 subdomains; not reproducible without the geometry.

## Targets for this re-pass

Lift coverage by attacking previously skipped/partial claims that are reproducible on CPU with numpy/scipy:

1. **C7 — Theorem 4.2 ρ_OO2 asymptotic h-scaling** (propagating `h^{1/4}`, evanescent `h^{1/2}`) via per-mode numerics (1D / Fourier).
2. **C12 — Table 6.2** quantitative match (ω = 10π directly on a modal frequency; only Krylov should converge).
3. **C13 — Fig 6.2 parameter-robustness**: numerical iteration count surface vs (p, q) on a coarse grid; check that the analytic (p*, q*) lies in the minimum basin and the Krylov surface is much flatter than the iterative one.
4. **C14 — OO2 in 2D PDE solver** (interface row carries `p + q ∂_{ττ}`): GMRES counts vs paper Table 6.1 OO2 columns.

Targets 1 and 3 are the cheapest and highest-value additions; 2 is a small variant of the existing 2D harness; 4 needs a real code change but is straightforward. Compute is free CPU on CherryRd.
