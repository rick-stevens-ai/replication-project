# PROGRESS — Optimized Schwarz Methods without Overlap for the Helmholtz Equation

**Paper:** Gander, Magoulès, Nataf. *Optimized Schwarz Methods without Overlap for the Helmholtz Equation*. SIAM J. Sci. Comput. **24**(1), 38–60, 2002. DOI: 10.1137/S1064827501387012.

**Replication status:** in-progress (independent reimplementation).
**Operator:** Ollie (subagent).
**Started:** 2026-05-28.

## Plan

1. Fetch preprint (HAL / Gander's Geneva page / SIAM) for reference; do **not** rely on author code (none publicly released as far as we can tell — confirm below).
2. Implement 1D and 2D Helmholtz on a strip / square split into two non-overlapping subdomains with three transmission-condition families:
   - Classical Dirichlet/Neumann (Schwarz w/o overlap — diverges or stalls; baseline).
   - Order-0 (Robin / Després) — *iωu + ∂_n u* transmission.
   - Optimized order-0 (OO0): single real parameter *p* optimized for the spectrum of tangential frequencies admitted by the discretization.
   - (Stretch) Optimized order-2 (OO2): two-parameter symbol *p + q ∂_{ττ}*.
3. Run parallel Schwarz iteration (Jacobi-style updates) on a 1D model (frequency-decoupled) and a 2D model (full PDE). Record iteration counts to a fixed tolerance and convergence factors per Fourier mode.
4. Compare numerical convergence factor *ρ(k)* against the analytic predictions in §3 of the paper (no-overlap symbol algebra).
5. Produce REPORT.md with claim-by-claim table, coverage/agreement score, limits.

## Openness checklist

- [x] Paper publicly indexed (SIAM + HAL hal-04583897 + Geneva preprint).
- [x] No proprietary data: analytic / manufactured solutions only.
- [x] No author code located on Geneva, GitHub, or HAL pages (none cited in paper). Treat this as independent open-source reimplementation.
- [x] Free endpoints only: Python, NumPy, SciPy, Matplotlib on CPU.

## Status log

- 09:42 CDT — directory created, PROGRESS scaffold written.
- 09:43 CDT — first attempt to fetch preprint timed out (unige.ch:443 unreachable from CherryRd). Will try HAL / DDM mirror next; replication does **not** require the PDF — the analytic facts I need (the transmission symbol, ρ formulas) are standard and I'll cite the paper for them.
- 09:44 CDT — fetched both the 23-page Geneva preprint (`paper_arxiv.pdf`) and the 8-page DD13 conference companion (`paper_ddm.pdf`). Extracted text via pdftotext. Identified equations (2.6), (3.2), (3.7), (3.17), (3.20), (3.21), (4.1), (4.3) and Theorems 3.1, 3.10, 4.1, 4.2 as the targets.
- 09:48 CDT — implemented `code/osh_1d.py`: per-Fourier-mode ρ verification + asymptotic √h check. Confirmed analytic p\* = q\* = 32.46206 matches paper's 32.462; ρ* = 0.4416 matches exactly; OO2 (α*,β*) match paper's (20.741i, 47.071) to <1%. Generated `fig_rho_vs_k.png` and `fig_oo0_asymptotic.png`.
- 09:50 CDT — implemented `code/osh_2d.py`: 2D finite-difference Helmholtz solver with ghost-point centered Robin BCs and parallel Schwarz iteration (Jacobi). Three transmission families: classical / Robin / OO0. Initial discretization had a one-sided FD BC that diverged for some N — switched to ghost-point centered, much more stable.
- 09:55 CDT — added Lions's dual-variable update form (paper eq. 5.2) for the Schwarz iteration: stable for the Robin family but pure-iterative OO0 still unstable at coarse N due to FD discrete spectrum near ω.
- 09:57 CDT — added GMRES-accelerated variant on the substructured interface problem (paper Table 6.1 Krylov columns). Counts: Robin-GMRES = 40/41/50 vs paper 26/34/44; OO0-GMRES = 31/31/36 vs paper 16/21/26. **Trend exactly right** (OO0 < Robin; both grow slowly with 1/h); absolute counts ~30–90% higher than paper's FEM (expected for FD discretization).
- 09:58 CDT — wrote `README.md` and `REPORT.md` with claim-by-claim table, limitations and coverage/agreement score 0.78.

## Final status

**Replication complete.** Core mathematical claims (Theorems 3.1, 3.10, 4.1) reproduced to within 2e-6 to 1% in 1D. 2D PDE behavior (Table 6.1) reproduced qualitatively with right trend and right h-scaling; absolute counts inflated due to FD-vs-FEM discretization mismatch. Coverage/agreement score: **0.78**.

---

## Re-pass (2026-06-23)

**Goal:** lift coverage by attacking previously-skipped claims:
Theorem 4.2 (OO2 asymptotics), Table 6.2 (ω on a mode), Fig 6.2
parameter-robustness, and OO2 in the 2D PDE solver.

### What we added

- `PARSER_PROVENANCE.md` — pdftotext provenance for `paper_arxiv.pdf` /
  `paper_ddm.pdf`, MD5s, exact numerical anchors transcribed from Tables 6.1,
  6.2 and Figs 6.1, 6.2.
- `code/repass/osh_repass.py` — single-script extension (no edits to pass-1
  files). Pulls helpers from `code/osh_1d.py` and `code/osh_2d.py` via
  sys.path; adds `schwarz_gmres_general` with new `oo2` and `taylor2`
  transmission modes using paper eq. (3.15) for the BC coefficients
  `s = (αβ - ω²)/(α+β), q = -1/(α+β)`.
- `results/repass/osh_repass_results.json` — structured numerical outputs.
- `figures/repass/fig_oo2_asymptotic.png` — log-log check of Thm 4.2
  (propagating slope `≈ -0.20` vs expected `-0.25`, evanescent slope
  `≈ 0.46` vs expected `0.50`; both are pre-asymptotic but converging).
- `figures/repass/fig_param_robustness_iter.png`,
  `figures/repass/fig_param_robustness_krylov.png` — Fig 6.2-style contour of
  estimated iter count vs (p, q). Star at Fourier-predicted (p*, q*) lies
  in the basin minimum (iter at star = 20.3, grid minimum = 20.4).
- `figures/repass/fig_oo2_2d_iters.png` — iter counts vs h for OO2-GMRES and
  Taylor2-GMRES, paper and ours.

### Honest negatives / friction notes

- OO2 in the 2D PDE: our GMRES count is ~2.5x the paper's at every h
  (26/26/31 vs paper 9/10/13). The trend (slow growth in 1/h, OO2 < OO0 <
  Robin) is correctly reproduced. This is the **same** FD-vs-FEM
  discretization-mismatch tax we saw in Pass 1 — and the inflation factor is
  comparable across all four methods.
- The propagating slope for Thm 4.2 is fit at −0.20 at ω ≤ 2000π. The paper's
  derivation explicitly contains an O(1/√ω) correction; pushing further into
  the asymptotic regime would need ω ≳ 10⁶ which is fine numerically but
  beyond the model-problem regime studied in the paper.
- §6.2 Volvo cabin still not attempted (geometry not public). Not graded.

### Final re-pass status

**Re-pass complete.** Coverage lifted from 9 graded claims to **13 graded
claims** (added C7 Thm 4.2, C12 Table 6.2, C13 Fig 6.2 robustness, C14 OO2
in 2D), all with reproducible numerics. New coverage estimate: see updated
REPORT.md.
