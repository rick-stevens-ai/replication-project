# Attempt Log

**2026-07-02 (all times CDT)**

1. Read priority list `PDE_NEXT50_2026-06-26.tsv` + `WAVE_BRIEF_2026-07-01.md`; listed
   existing sibling dirs. Skipped the already-done set. Chose rank-39
   **Hou & Xu, time-fractional Allen-Cahn SAV schemes** (arXiv-hosted OA, clean numerical
   PDE core with manufactured analytic test cases + concrete convergence-slope numbers).
2. Dedup: `grep -i hou|fractional-allen|tfac` over REPLICATE-PROJECT/ and PDE-replications/
   → no collision. `PDE-allen-cahn-maxprinciple-shen-zhang-2021` is a *different* paper
   (integer-order max-principle FD), so no overlap.
3. Local network is firewalled (arXiv fetch returns 0 bytes). Routed all downloads through
   `ssh uicgpu` with `source ~/env.sh` (Squid proxy <lan-host>:3128). arXiv requires
   https (http→301). Pulled paper.pdf (4.76 MB) + e-print tarball (9.64 MB). `pdftotext
   -layout` on uicgpu, then scp'd paper.pdf/paper.txt/revised1106.tex back to work/.
4. Extracted the PDE (Ex 5.1/5.2/5.3), the double-well potential F(φ)=¼(φ²−1)², the L1
   scheme (3.9→3.12) and L1-CN scheme (4.1), and the graded-mesh coefficient formulas.
   Re-derived the manufactured source term for Ex 5.1 including Caputo derivative of t⁵
   (`Γ(6)/Γ(6−α) t^{5−α}`), Laplacian eigenvalue −2 for sin x cos y, and the cubic term.
5. **L1 scheme** (`work/l1_scheme.py`): Fourier spectral 128×128, θ=0, C₀=0, uniform mesh,
   T=1. Re-derived the SAV two-solve elimination *including a source term* (paper's
   elimination is source-free). Ran α∈{0.1,0.5,0.9}, M∈{20..320}.
   → first-order convergence confirmed (rates→1.0 for α=0.1,0.5; ≥1 for α=0.9). ~10 s.
6. **L1-CN scheme** (`work/l1cn_scheme.py`): midpoint L1-CN coefficients, explicit
   half-step extrapolation of φ and R, θ=0 elimination re-derived with source.
   → α=0.1 rate 1.985 (paper 1.9); α=0.9 rate 1.25→1.1 (paper 1.1); α=0.5 ~1.7. ~13 s.
7. **Energy dissipation** (`work/energy_dissip.py`): source-free coarsening,
   φ₀=cos4πx cos4πy, ε²=0.001, L1-CN. Modified energy Ẽ=(ε²/2)‖∇φ‖²+|R|² monotone
   decreasing every step for all α,M (max per-step Δ ≤ 0). Confirms Thm 3.1/4.1.
8. Multi-judge (`work/judge.py`, free Argo): gpt-5.2, gemini-2.5-pro → PARTIAL;
   gpt-4.1 → REPLICATED. **All three: C1,C2,C3 all reproduced.** Consensus **PARTIAL**
   (headline L1/L1-CN claims + energy law reproduced; L1+-CN & graded-mesh not attempted).

## What worked
- arXiv OA source + PDF via uicgpu proxy; pdftotext -layout for equation extraction.
- SAV two-solve elimination generalizes cleanly to include a source term.
- Fourier spectral removes spatial error, isolating the temporal order exactly as intended.

## What was not done (out of scope for time budget)
- L1+-CN (4.3) second-order scheme.
- Graded-mesh optimal-r experiments (Ex 5.3) and shrinking-circle benchmark (Sec 5.2).
- Legendre-Galerkin space discretization (Fourier used throughout; equivalent for the
  smooth periodic test data in the negligible-spatial-error regime).
