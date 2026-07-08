# Replication: Empirical Trotter (Product-Formula) Error Scaling for Heisenberg Spin-Chain Simulation

**Set:** QC-100  ·  **Slug:** QC-trotter-error-speedup-Childs2018  ·  **Status:** COMPLETE

## 1. Paper

Andrew M. Childs, Dmitri Maslov, Yunseong Nam, Neil J. Ross, Yuan Su,
**"Toward the first quantum simulation with quantum speedup,"**
*Proceedings of the National Academy of Sciences* **115** (38), 9456–9461 (2018).
- Journal DOI: **10.1073/pnas.1801723115**
- Preprint: **arXiv:1711.10980** (quant-ph), DOI 10.48550/arXiv.1711.10980

## 2. What the paper claims (targets of this replication)

The paper synthesizes circuits for three leading Hamiltonian-simulation algorithms
(product formulas, Taylor-series/LCU, and quantum signal processing) applied to
spin systems, and makes two quantitative points that are directly reproducible in
classical simulation:

- **Claim A — Empirical error scaling of product formulas.** For an order-*p*
  Suzuki–Trotter product formula with *r* steps over time *t*, the error scales as
  `O((t/r)^{p+1} · r) = O(r^{-p})`. Hence on a log–log plot of error vs *r* the
  slope should be **−1 (PF1), −2 (PF2), −4 (PF4)**. The paper relies on such
  *empirical* error estimates (rather than loose rigorous bounds) to argue that
  **"higher-order product formulas prevail if empirical error estimates suffice."**
- **Claim B — Empirical error ≪ analytical worst-case bound.** The a-priori
  (commutator) Trotter bounds substantially over-estimate the actual error, which
  is why using empirical error estimates dramatically reduces the resource count.

The paper's benchmark model is a nearest-neighbor Heisenberg chain with a random
on-site z-field:
`H = Σ_j (X_jX_{j+1}+Y_jY_{j+1}+Z_jZ_{j+1}) + Σ_j h_j Z_j`, `h_j ~ U[-h,h]`.

## 3. What I actually ran

Pure `numpy`/`scipy` operator-level simulation (no qiskit/pennylane available;
none needed). Full 2^n × 2^n matrices.

- System: **n = 6 spins** (Hilbert dim 64), total time **t = 1.0**, random z-field
  `h_j ∈ U[−1,1]` (seed 20260702), `||H||₂ = 10.77`, 11 Hamiltonian terms
  (5 XX+YY+ZZ bonds on the open chain + 6 single-site field terms).
- Exact evolution `U_exact = expm(−iHt)` via `scipy.linalg.expm`.
- Implemented **PF1** (Lie–Trotter), **PF2** (symmetric Strang), **PF4**
  (Suzuki 4th-order fractal, `u = 1/(4−4^{1/3})`, `S4 = S2(u)²S2(1−4u)S2(u)²`).
- Metric: **spectral-norm (operator) error** `||U_exact − U_PF||₂` vs `r ∈ {1,…,128}`.
- Fitted log–log slopes on the clean asymptotic regime (above the ~1e-13 numerical floor).
- Separately compared PF1 empirical error to the textbook first-order commutator
  bound `(t²/2r)·Σ_{i<j}||[H_i,H_j]||₂`.

Code: `code/trotter_error.py`, `code/bound_vs_empirical.py`.
Data: `results/trotter_results.json`, `results/bound_vs_empirical.json`.

## 4. Results — per-claim, my numbers vs paper

### Claim A: error-scaling exponents (log–log slope of error vs r)

| Formula | Paper (theory) | My fitted slope | Match |
|--------|:--------------:|:---------------:|:-----:|
| PF1    | −1             | **−0.967**      | ✓     |
| PF2    | −2             | **−1.977**      | ✓     |
| PF4    | −4             | **−4.197**      | ✓     |

Raw error vs r (spectral norm):

```
 r      PF1        PF2        PF4
 1    2.000e0    2.000e0    9.394e-1
 2    1.999e0    1.380e0    9.834e-2
 4    1.681e0    4.235e-1   3.690e-3
 8    9.519e-1   1.119e-1   2.378e-4
16    4.865e-1   2.833e-2   1.507e-5
32    2.436e-1   7.104e-3   9.451e-7
64    1.216e-1   1.777e-3   5.912e-8
128   6.074e-2   4.444e-4   3.696e-9
```

Each doubling of r reduces the error by the predicted factor: **~2× for PF1,
~4× for PF2, ~16× for PF4** (e.g. PF4 32→64: 9.45e-7 → 5.91e-8 ≈ /16.0;
PF2 32→64: 7.10e-3 → 1.78e-3 ≈ /4.0; PF1 32→64: 2.44e-1 → 1.22e-1 ≈ /2.0).
This is a clean, quantitative match to the paper's `O(r^{-p})` empirical scaling
and confirms exactly why higher-order formulas win in the empirical-estimate regime.

### Claim B: empirical error vs analytical worst-case bound (PF1)

`Σ_{i<j}||[H_i,H_j]||₂ = 61.9`.

| r   | empirical | analytic bound | bound / empirical |
|----:|----------:|---------------:|------------------:|
| 1   | 2.00e0    | 3.10e1         | 15.5×             |
| 4   | 1.68e0    | 7.74e0         | 4.6×              |
| 16  | 4.86e-1   | 1.93e0         | 4.0×              |
| 64  | 1.22e-1   | 4.84e-1        | 4.0×              |
| 128 | 6.07e-2   | 2.42e-1        | 4.0×              |

The a-priori commutator bound over-estimates the true error by **~4× asymptotically
(up to ~15× at small r)**, confirming the paper's qualitative point (Claim B) that
rigorous bounds are looser than empirically observed error — the motivation for
their empirical resource estimates. (The paper reports even larger gaps against the
*published loose* bounds and for higher orders; the standard textbook first-order
bound used here is already relatively tight at ~4×, so my factor is a conservative,
honest lower bound on the effect.)

## 5. Verdict & scores

- **Coverage:** I reproduce the paper's two directly-simulatable quantitative
  claims (empirical product-formula error scaling exponents for PF1/PF2/PF4, and
  empirical-vs-bound gap) on its own benchmark model (random-field Heisenberg
  chain). I do **not** reproduce the full circuit-synthesis T-count tables, the
  LCU/QSP algorithms, or the specific 50/100-spin resource numbers (those require
  fault-tolerant circuit compilation, out of scope for a laptop numpy sim).
- **Agreement:** Excellent on what was reproduced — fitted exponents −0.97/−1.98/−4.20
  vs theory −1/−2/−4, and the per-doubling error-reduction factors (2×/4×/16×) are
  essentially exact.

**Self-assessed: Coverage 7/10, Agreement 9/10.**

### Independent judge (Argo `argo:gpt-5.2`, temperature 0)
- **Coverage: 6/10**
- **Agreement: 8/10**
- **Verdict: PARTIALLY_REPRODUCED**
- Justification: "The replication covers the paper's empirically-estimated product-formula
  behavior by simulating PF1/PF2/PF4 on a random-field Heisenberg chain and reproducing
  the expected log-log error slopes (≈−1, −2, −4), a central quantitative ingredient in
  the paper's argument. However, it does not attempt the paper's headline
  resource-estimation outputs (fault-tolerant T-count/qubit tables for 50–100 spins,
  PF/LCU/QSP comparisons), and the bound-vs-empirical comparison is only for a relatively
  tight first-order commutator bound and a small n=6 instance, so it only partially
  addresses the 'bounds are very loose' narrative. Within the scoped simulation targets,
  numerical agreement is strong."

## 6. Reproducibility-blocker critique

- **Fully reproducible parts:** The empirical product-formula error scaling is
  model-agnostic and reproduces trivially from the paper's stated `O(r^{-p})`
  claim; no paper-specific data needed. Deterministic (fixed seed), runs in <5 s.
- **Blockers for the headline numbers:** The paper's marquee results are
  **T-gate/qubit counts** for classically-infeasible 50–100 spin instances after
  full fault-tolerant circuit synthesis. These depend on (a) their specific
  tightened error-bound derivations (several pages of analysis), (b) a Clifford+T
  synthesis/optimization toolchain, and (c) the QSP/LCU implementations — none of
  which are released as a runnable artifact with the paper. Reproducing those
  exactly would require re-deriving the bounds and re-implementing the compiler.
- **Ambiguities:** The exact random-field distribution parameters and system sizes
  used for each empirical-error figure are described qualitatively; I chose a
  representative instance (n=6, t=1, h=1). The *scaling exponents* (the physics)
  are insensitive to these choices, which is precisely why the empirical estimate
  is robust — but absolute error magnitudes are instance-dependent.
- **No paid/proprietary dependencies:** numpy + scipy only; free Argo endpoint for
  scoring.

## 7. Files
- `code/trotter_error.py` — PF1/PF2/PF4 vs exact, scaling fit.
- `code/bound_vs_empirical.py` — analytic commutator bound vs empirical (PF1).
- `results/trotter_results.json`, `results/bound_vs_empirical.json` — raw numbers.
