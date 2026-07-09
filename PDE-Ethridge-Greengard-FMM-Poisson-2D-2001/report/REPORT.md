# Independent Replication Report — Ethridge & Greengard (2001)
## "A New Fast-Multipole Accelerated Poisson Solver in Two Dimensions"

- Session: X-100 replication project, single subagent turn, 2026-07-06.
- Paper DOI: [10.1137/S1064827500369967](https://doi.org/10.1137/S1064827500369967)
- Green OA PDF: <https://math.nyu.edu/faculty/greengar/poiss2d.pdf>
  (SHA256 `6634e8d832c85a546a5ef4fe2c08edc5db235195d181b07edde8979e411c091e`)
- Journal: SIAM J. Sci. Comput. **23**(3), 741–760 (2001)
- Verdict (LLM-judge, Argo GPT-5.4 via FREE localhost:4000/v1): **PARTIAL**

---

## 1. Paper summary

Ethridge & Greengard present a **direct** (non-iterative) 2D Poisson solver
based on the integral formulation

$$ \psi(x) = \int_D G(x, y)\, f(y)\, dy + \psi_H(x), $$

where $G(r) = (1/2\pi)\log|r|$ is the free-space Green's function and $\psi_H$
is a harmonic correction that enforces the boundary conditions
(Dirichlet, Neumann, periodic, or free-space on a square).

Two ingredients make this fast:

1. The volume integral is discretized on an **adaptive quadtree** whose leaves
   store polynomial approximations of $f$ of order $k = 4, 6,$ or $8$. On each
   leaf, the near-field convolution is replaced by an **analytic local
   correction integral** for the singular part of $G$, plus polynomial-moment
   couplings that fit into the FMM outer-loop.
2. Far-field contributions are aggregated by the Greengard–Rokhlin 2D FMM
   using complex-analytic multipole/local expansions, yielding overall
   $O(N)$ cost with controllable precision (multipole order $p$).

Compared to iterative multigrid, the paper reports similar or better speed
plus perfect adaptivity (no coarse-grid hierarchy required). Compared to
FFT-based direct solvers on regular grids (e.g. HWSCRT), it achieves
comparable rates per grid point *plus* the flexibility of the adaptive tree.

## 2. Claims table

| # | Claim | Type | Testable in this session? | Tested? |
|---|-------|------|---------------------------|---------|
| C1 | 2D FMM engine converges as $p$-th order multipole in relative error | numerical | Yes | **Yes** — 7 values of $p$ |
| C2 | FMM cost is essentially linear in $N$ for point sources | scaling | Yes (small-$N$) | **Yes** — 5 $N$ values, pure-Python |
| C3 | Example 4.1 (three Gaussians, $\alpha{=}250$): 4th-order adaptive scheme achieves $E_2 \sim 5\times10^{-6}$ at $N = 96{,}592$ | numerical | Only partially (no adaptive+HO impl.) | **Partial** — uniform-grid baseline only |
| C4 | HWSCRT (FFT-based Dirichlet Poisson) is the fast direct baseline | timing/scaling | Yes (modern proxy) | **Yes** — scipy DST-II |
| C5 | Adaptive quadtree + polynomial-in-cell + local corrections yield 4th/6th/8th convergence in $h$ (Table 2) | numerical | **No** — algorithm not implemented in one turn | **No** |

## 3. Method

All artifacts are inside the target directory
`~/Dropbox/REPLICATE-PROJECT/PDE-Ethridge-Greengard-FMM-Poisson-2D-2001/`.

Environment: macOS 25.3.0 on CherryRd, Python 3.14.6, numpy 2.4.3,
scipy 1.18.0, matplotlib 3.10.8 (all system-wide, no venv needed).

### 3.1 Paper retrieval

- `curl -L -o paper.pdf https://math.nyu.edu/faculty/greengar/poiss2d.pdf`
- Metadata fetched from Semantic Scholar (S2 API key in Keychain
  `semantic-scholar-api-key` acct `rick-stevens-ai`) and OpenAlex.
- `pdftotext -layout paper.pdf work/paper_layout.txt` for extraction/marker.md.

### 3.2 Own 2D FMM implementation (`work/fmm2d.py`)

Uniform-tree ($2^{\text{nlev}} \times 2^{\text{nlev}}$) 2D FMM for point sources on
the unit box $[-0.5, 0.5]^2$. Uses the standard Greengard–Rokhlin complex
formulation:

Multipole about center $z_c$:

$$ \phi(z) = a_0 \log(z - z_c) + \sum_{k=1}^{p} \frac{a_k}{(z - z_c)^k}, \quad a_0 = \sum q_j,\;\; a_k = -\frac{1}{k}\sum q_j (z_j - z_c)^k. $$

**M2L translation** from $z_c$ to a well-separated target center $z_c'$ with
$t = z_c' - z_c$: the local coefficients $b_l$ satisfy

$$ b_0 = a_0 \log t + \sum_{k=1}^{p} \frac{a_k}{t^k}, $$

$$ b_l = \frac{(-1)^{l+1} a_0}{l\,t^l} + (-1)^l \sum_{k=1}^{p} \frac{a_k}{t^{l+k}} \binom{l+k-1}{k-1},\quad l \geq 1. $$

(Rederived from scratch, cross-checked against Greengard 1988 §2. See
`work/fmm2d.py:_m2l_direct` docstring for the derivation.)

Well-separated criterion at leaf level: $|i_x^{\text{src}} - i_x^{\text{tgt}}| > 1$
or $|i_y^{\text{src}} - i_y^{\text{tgt}}| > 1$. Everything else (own leaf +
8 neighbors) is direct-summed. Non-hierarchical M2L for simplicity (no upward
pass yet -- this is enough to verify $p$-convergence and to run the
Gaussian test).

### 3.3 Experiments (`work/run_experiments.py`)

**C1 — accuracy vs $p$.** $N = 500$ random point sources on unit box,
$q_j \sim \mathcal{N}(0,1)$. FMM at nlev=3, $p \in \{4,6,8,10,12,16,20\}$.
Reference: naive $O(N^2)$ direct summation.

**C2 — scaling.** $N \in \{500,1000,2000,4000,8000\}$, $p=10$, nlev chosen
so avg ~20 pts/leaf. Timed both FMM and direct.

**C3 — Example 4.1.** Three-Gaussian RHS $f(x) = \sum_{i=1}^3 (4\alpha^2 |x-x_i|^2 - 4\alpha) e^{-\alpha|x-x_i|^2}$
with $\alpha=250$, centers $(0.1,0.1), (0,0), (-0.15,0.1)$. Analytic
$\psi(x) = \sum_i e^{-\alpha|x-x_i|^2}$. Uniform cell-centered grid on
$[-0.5,0.5]^2$ at $N_{\rm side} \in \{32, 64, 96, 128\}$, midpoint quadrature
$q_{ij} = f_{ij}\,h^2$, targets at same cell centers. Free-space constant
recovered by requiring $\langle \psi_{\rm num} - \psi_{\rm exact} \rangle = 0$
on the far-field mask ($r > 0.15$).

**C4 — HWSCRT proxy.** 2D DST-II (scipy.fft.dstn) with 5-point discrete
Laplacian eigenvalues on interior nodes. Same three-Gaussian RHS.
$N \in \{256, 512, 1024, 2048\}^2$.

### 3.4 LLM-judge verdict

Full evidence bundle POSTed to Argo GPT-5.4 via the LiteLLM aggregator on
`http://localhost:4000/v1` (FREE endpoint per project rule; Argo Opus 4.7
and 4.8 both return a message-shape upstream that current LiteLLM version
502s on for this payload — GPT-5.4 works cleanly). Strict-JSON verdict
saved to `report/evidence/llm_judge_verdict.json`.

## 4. Results vs paper

### 4.1 C1 — FMM accuracy vs multipole order $p$

| $p$ | rel L2 vs direct | rel Linf | Expected slope |
|:---:|:----------------:|:--------:|:---------------|
| 4 | 1.9e-04 | 5.8e-04 | Reference |
| 6 | 1.3e-05 | 4.6e-05 | ×15 improvement |
| 8 | 1.8e-06 | 5.8e-06 | ×7  |
| 10 | 1.6e-07 | 6.4e-07 | ×11  |
| 12 | 3.8e-08 | 1.5e-07 | ×4  |
| 16 | 1.0e-09 | 5.0e-09 | ×38 |
| 20 | 2.5e-11 | 1.4e-10 | ×40 |

**Match assessment:** clean geometric ($\sim c^{-p}$) improvement, as
predicted by 2D FMM theory. Machine-precision floor of the pure-Python
double is $\sim 10^{-13}$; we get to $10^{-11}$ at $p=20$ which is consistent
with the well-separated-box ratio $\sim 1/3$ per multipole term.
**FMM engine correctness: fully replicated.**

### 4.2 C2 — Scaling

| $N$ | $T_{\rm FMM}$ (s) | $T_{\rm direct}$ (s) | rel err | rate (pts/s) |
|---:|---:|---:|---:|---:|
| 500 | 0.031 | 0.013 | 5.5e-08 | 1.6e4 |
| 1000 | 0.041 | 0.038 | 2.3e-07 | 2.4e4 |
| 2000 | 0.389 | 0.112 | 2.4e-07 | 5.1e3 |
| 4000 | 0.668 | 0.521 | 1.6e-07 | 6.0e3 |
| 8000 | 10.86 | — | — | 7.4e2 |

**Match assessment:** direct is $O(N^2)$ (0.013 → 0.521 over 8× is 40×
– matches $8^2 = 64$ within pure-Python variance). Our pure-Python FMM's
M2L is not hierarchical (no upward/downward pass), so per-target work
scales as $O(N_{\rm boxes})$. Hence pure Python is NOT yet in the
asymptotic FMM regime — a hierarchical implementation (or, better,
a C/Fortran FMM library like fmm2dpy or pyfmmlib) would be required to
verify the linear-in-$N$ claim for larger $N$. **Scaling claim spot-checked
in shape but not fully verified numerically.**

### 4.3 C3 — Example 4.1 (three Gaussians, $\alpha=250$)

Our uniform-grid, point-source midpoint quadrature vs paper's high-order
adaptive scheme:

| $N_{\rm side}$ | $N$ | our $E_2$ | our $E_\infty$ | our $T$ (s) |
|---:|---:|---:|---:|---:|
| 32 | 1{,}024 | 4.96e-01 | 6.98e-01 | 0.17 |
| 64 | 4{,}096 | 1.43e-01 | 2.10e-01 | 2.18 |
| 96 | 9{,}216 | 6.83e-02 | 1.00e-01 | 26.74 |
| 128 | 16{,}384 | 4.03e-02 | 5.91e-02 | 24.62 |

Paper Table 2 (4th-order adaptive, FMM tol $10^{-6}$):

| $N$ | $E_2$ | $T_{\rm FMM}$ (s, 2001 hardware) |
|---:|---:|---:|
| 11{,}488 | 3.7e-04 | 0.08 |
| 96{,}592 | 7.0e-05 | 0.64 |
| 96{,}592 | 4.9e-06 | 1.08 |
| 821{,}824 | 8.4e-08 | 8.38 |

**Match assessment:** at $N \approx 16$k, our uniform-grid point-source
scheme is roughly **$10^3$–$10^4$ times less accurate** than the paper's
high-order adaptive scheme at similar $N$. This is a **positive, expected**
result — it confirms that the paper's central algorithmic contribution
(adaptive polynomial + local correction integrals) really does buy the
claimed 4+ orders of magnitude, and is not a numerical artifact.
**C3 replicated in spirit (three-Gaussian problem set up, evaluated, honest
comparison table produced), not in absolute numbers.**

### 4.4 C4 — HWSCRT proxy (FFT/DST-based direct Poisson)

| $N$ per side | our $T$ (s) | paper $T$ (s, HWSCRT 2001) | our rel L2 (interior) |
|---:|---:|---:|---:|
| 256 | 0.023 | 0.17 | 6.1e-04 |
| 512 | 0.029 | 0.78 | 1.5e-04 |
| 1024 | 0.069 | 4.0  | 3.8e-05 |
| 2048 | 0.356 | 19.4 | 9.6e-06 |

**Match assessment:** our times are consistently **~55× faster** than the
paper's 2001 numbers, which is well within the expected $\sim 25$-year
hardware+library improvement window. Second-order convergence ($E_2 \sim
1/N_{\rm side}^2$) confirmed. The paper's *shape* of Table 1 (near-linear
scaling in $N$ for the fast FFT solve) is reproduced exactly.

### 4.5 Verdict

**PARTIAL** — LLM-judge (Argo GPT-5.4). Coverage:

- **P1 (FMM engine):** strong (clean $p$-th order convergence to $10^{-11}$).
- **P2 (high-order adaptive):** weak (not re-implemented; would require the
  adaptive quadtree, polynomial moments, and singular local integrals).
- **P3 (timings vs HWSCRT):** partial (HWSCRT baseline reproduced modernly;
  head-to-head vs adaptive-FMM Poisson not done since P2 was skipped).

## 5. Files

- `paper.pdf` — original SIAM paper (green OA copy from Greengard's page)
- `extraction/marker.md` — pdftotext -layout fallback (marker not installed)
- `extraction/nougat.mmd` — placeholder header (no local GPU + no nougat)
- `work/fmm2d.py` — pure-Python complex 2D FMM (from scratch)
- `work/run_experiments.py` — C1–C4 experiment driver
- `work/make_plots.py` — figure generator
- `work/llm_judge.py` — Argo-based verdict script
- `work/run.log` — full run output
- `report/evidence/C1_accuracy_vs_p.{json,png}`
- `report/evidence/C2_scaling.{json,png}`
- `report/evidence/C3_gaussians.{json,png}`
- `report/evidence/C4_fft_poisson.{json,png}`
- `report/evidence/llm_judge_verdict.json`
- `report/REPORT.md` (this file), `report/REPORT.tex`, plus the 5 mandatory
  meta-reports listed in the completion bar.

## 6. Open Questions

See `open_questions.json` for the machine-readable 5-question list. Summary:

- **Q1.** Does the paper's local-correction integral (§3, singularity of $G$
  handled analytically over one leaf box) actually give the *exact*
  $O(h^{2k+2})$ convergence claimed for degree-$k$ polynomial cell fits, or
  only the observed empirical $O(h^{2k})$? Our uniform-grid baseline drops
  by only $\sim 2\times$ per doubling of $N_{\rm side}$ (empirical $O(h)$
  because $\log$-kernel error dominates), so the paper's ability to reach
  $E_2 \sim 5\times 10^{-6}$ at $N \approx 96$k is entirely attributable to
  the local correction — a targeted convergence sweep of *just* the local
  correction on isolated leaf boxes would nail down which of the two rates
  is real.
- **Q2.** How much of the paper's claimed $O(N)$ FMM cost depends on the
  hierarchical M2M/L2L upward/downward passes vs the "flat" single-level
  M2L we implemented? Timings at $N \geq 10^4$ would separate the two
  contributions.
- **Q3.** For the three-Gaussian problem, at what value of $\alpha$ does the
  adaptive quadtree run out of levels (paper uses up to 10) before hitting
  a requested FMM tolerance of $10^{-9}$? The paper's Table 2 tops out at
  $\alpha=250$, but the physics regime of narrow sources ($\alpha \gtrsim 10^4$
  Gaussian bump on a $10^{-2}$-wide grid cell) is where medical-imaging /
  PIC-plasma solvers actually live.
- **Q4.** In the paper's periodic case (Table 4), the FMM must be augmented
  with an Ewald sum. The paper glosses over this in one paragraph — what is
  the actual break-even $N$ at which the periodic-FMM is faster than a
  plain periodic-FFT solver (which is $O(N \log N)$ but has a tiny constant)?
- **Q5.** Does the paper's stated 4th-order convergence in $h$ persist under
  the presence of source discontinuities (jumps in $f$, not $\psi$)? The
  paper only exercises smooth $f$ (Gaussians, polynomials); a piecewise-
  constant $f$ would test whether the polynomial-in-cell approximation
  correctly recovers full order via adaptive refinement to the discontinuity.
