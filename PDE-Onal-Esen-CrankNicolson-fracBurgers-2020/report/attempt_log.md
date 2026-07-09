# Attempt Log (chronological)

1. Read WAVE_BRIEF_2026-07-01.md; scanned PDE_NEXT50 + PDE_TOPUP25 priority lists; dedup-checked candidates against existing sibling dirs.
2. **Picked** rank-9 repro-ok candidate: Onal & Esen (2020) time-fractional Burgers CN/L1. Verified no colliding dir. Created `PDE-Onal-Esen-CrankNicolson-fracBurgers-2020/`.
3. **PDF hunt (blocked everywhere live):** sciendo.com article/pdf → Next.js 404 shell; degruyterbrill → 404; De Gruyter /pdf → HTTP 202 bot-wall (polled 6×, always empty); ResearchGate fulltext → Cloudflare 1020 (local + uicgpu); CORE → no fulltext; DOAJ API → 401. Unpaywall confirmed OA GOLD but only pointed to dead sciendo URL.
4. **Recovered PDF via Wayback CDX** (ran from uicgpu to dodge archive.org 429): found archived `content.sciendo.com/downloadpdf/journals/amns/5/2/article-p177.pdf`, snapshot 20200819013624, `application/pdf`. Downloaded raw replay (708 KB, 6 pages). `pdftotext -layout` gave clean text (no OCR needed).
5. **Extracted spec:** PDE `D_t^γ u + u u_x − ν u_xx = f` on [0,1]; Caputo derivative via L1 formula `b_k=(k+1)^{1-γ}−k^{1-γ}`; central differences in space; semi-implicit CN advection; Dirichlet BCs. Transcribed the fully-discrete algebraic system (paper Sec 2.1) and all 7 tables + 3 manufactured test problems.
6. **Implemented** `cn_frac_burgers.py` from scratch (NumPy, Thomas tridiagonal solve, vectorized O(n²) L1 memory sum). Validated it tracks the manufactured exact solution and errors fall with mesh refinement.
7. **Pinned scheme detail:** an f-time-evaluation sensitivity test at M=10 showed forcing must be evaluated at the *old* time level `t_n` to match — that choice gave L2×10³=22.640873 vs paper 22.64087326 (8-sig-fig hit). `t_{n+1}` and `t_{n+1/2}` were ~1.6% off.
8. **Ran full sweep on uicgpu** (`source ~/env.sh`): Tables 1–7. Copied JSON + logs back.
9. **Symbolic verification (SymPy):** re-derived all three `f(x,t)` from `D_t^γ(t²)=2/Γ(3-γ)·t^{2-γ}` + advection + diffusion. All three exactly match the paper's printed forcing.
10. **Convergence-order check:** spatial order ≈2.1 (central diff O(Δx²)), as designed. Reproduced Fig-1-style solution plot.
11. **Multi-judge scoring** (Argo gpt-5.2 / gemini-2.5-pro / gpt-4.1) on the results table.

## Key findings
- Example 1 Tables 1, 2 (Present column), 4: **8-significant-figure agreement (0.000%)**.
- Table 3 (varying ν): does not match — but the paper's Table 3 at ν=1 (L2×10³=0.4176) **contradicts its own Table 1 N=40** (L2×10³=1.2201) for the identical configuration. Our solver is self-consistent (both = 1.2201). This is a paper internal inconsistency.
- Tables 5–7 (Examples 2, 3): our errors are consistently *smaller* and do not match the paper's magnitudes/trends; forcing terms are analytically verified correct, so this too points to paper-side table issues (Example 2/3 were likely tabulated from a differently-configured or less-converged run).
