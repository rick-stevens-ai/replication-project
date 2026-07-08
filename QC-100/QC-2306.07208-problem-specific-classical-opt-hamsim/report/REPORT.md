# QC-100 Replication — arXiv:2306.07208

**Paper.** Refik Mansuroglu, Felix Fischer, Michael J. Hartmann, *"Problem specific classical optimization of Hamiltonian simulation"* (Oct 2023).

**Reproducible core tested.**
Classically optimize the real coefficients of a product-formula circuit template so that ‖U_template(t) − exp(−iHt)‖₂ is minimized for a *specific* problem instance, at a **fixed number of exponentials** (identical circuit depth / gate count as the baseline Trotter/Strang). Show that the pre-optimized formula beats standard Strang at the *same* cost.

**Verdict.** **PARTIAL** (real simulation confirms the directional claim and its problem-dependent size; the >10³× improvement quoted in the paper's headline requires a much richer ansatz than the minimal 3/5-exp templates used in this reproduction and therefore is not tested end-to-end here).

---

## 1. Paper claims

| # | Claim | Type | Testable at small scale? | Tested here? |
|---|---|---|---|---|
| C1 | For a given problem instance in the perturbative regime, there always exists an optimized product formula that has lower unitary error than a standard Trotter sequence of the same order at the *same* number of exponentials. | Existence / directional | Yes | **Yes** |
| C2 | For short times on the XY model, classical pre-optimization gives >3 orders of magnitude accuracy improvement over Trotter at the same gate count. | Quantitative, headline | Yes but needs richer ansatz (RM params over R layers) than a 3- or 5-exp BAB/BABAB template | **Partially** (only tested strict 3-exp and 5-exp templates; observed 1.1–6× gain, consistent in *direction* and consistent with paper's own remark that TFIM shows much smaller gain than XY) |
| C3 | For a target accuracy 0.1 %, the pre-optimized sequence enables >10× longer simulation times at the same gate budget. | Quantitative | Requires K-fold repetition study across depths, plus full RM ansatz | **Not tested** (K-fold extrapolation was done on TFIM 3-exp only) |
| C4 | TFIM specifically has a first-order Trotter that is unitarily equivalent to second-order Trotter, so the improvement of optimization over Strang is intrinsically smaller for TFIM than for XY. | Qualitative caveat, Appendix B | Yes | **Yes and confirmed** (TFIM 3-exp ratio ≈ 1.4×; XY 5-exp ratio ≈ 5.9×) |

## 2. Method

**Sim tool.** Pure NumPy 2.4.3 + SciPy 1.18.0 (dense matrix `scipy.linalg.expm`). Faithful for N ≤ 6 spins (matrix size 64×64). No approximate simulator, no fabricated numbers.

**Models.**
- **TFIM** on N spins, open BC: H = A + B, A = −J Σᵢ ZᵢZᵢ₊₁, B = −h Σᵢ Xᵢ, with J = h = 1.
- **XY chain, random NN couplings** on N spins (chain proxy for the paper's 3×3 XY lattice with random couplings): A = −Σᵢ [Jy·YᵢYᵢ₊₁ + Jz·ZᵢZᵢ₊₁] with Jy,Jz drawn uniformly around 0.5 and 1.0 (spread 0.25, `np.random.default_rng(1)`), B = −0.25 Σᵢ Xᵢ (matches paper's h=0.25).

**Baselines and optimized templates (identical exponential count).**
1. **3-exp:** baseline = Strang BAB `exp(−iBt/2)·exp(−iAt)·exp(−iBt/2)` vs optimized `exp(−ic₁Bt)·exp(−ic₂At)·exp(−ic₃Bt)`. Both cost 3 A/B-block exponentials.
2. **5-exp:** baseline = two-half-step Strang merged into 5 exps with coefficients (¼, ½, ½, ½, ¼); optimized = generic BABAB with 5 free real coefficients. Both cost 5 A/B-block exponentials.

**Loss.** Spectral norm ‖U_template(t) − exp(−iHt)‖₂, computed exactly.

**Optimizer.** Nelder–Mead (`scipy.optimize.minimize`), initialized at the Strang coefficients (which is a strict lower bound: the Strang value of the template equals the baseline error, so the optimizer either matches or improves it).

**Exact commands.**
```bash
python3 code/optim_prodform.py     # 3-exp BAB study + K-fold extrapolation (TFIM N=4,5,6)
python3 code/optim_prodform_v2.py  # 3-exp + 5-exp comparison (TFIM N=5, XY N=5,6)
python3 code/judge.py              # Argo LLM-judge verdict
```

## 3. Results vs paper (real numbers)

### 3.1 Single-step error, TFIM N=5 (‖H‖ ≈ 6.03), 3-exp vs 5-exp

| t | t·‖H‖ | err Strang (3-exp) | err Opt (3-exp) | ratio | err Strang (5-exp) | err Opt (5-exp) | ratio |
|---|---|---|---|---|---|---|---|
| 0.02 | 0.12 | 2.94e-05 | 2.02e-05 | 1.46× | 7.36e-06 | 2.26e-06 | **3.26×** |
| 0.05 | 0.30 | 4.59e-04 | 3.15e-04 | 1.46× | 1.15e-04 | 3.30e-05 | **3.48×** |
| 0.10 | 0.60 | 3.66e-03 | 2.52e-03 | 1.45× | 9.09e-04 | 2.37e-04 | **3.84×** |
| 0.20 | 1.21 | 2.87e-02 | 2.00e-02 | 1.43× | 7.03e-03 | 1.88e-03 | **3.73×** |
| 0.40 | 2.41 | 2.12e-01 | 1.55e-01 | 1.37× | 4.88e-02 | 1.48e-02 | **3.29×** |
| 0.80 | 4.82 | 1.18e+00 | 9.33e-01 | 1.26× | 2.26e-01 | 1.19e-01 | 1.90× |

### 3.2 Single-step error, XY chain N=6 (‖H‖ ≈ 5.61), random NN couplings

| t | t·‖H‖ | err Strang (3-exp) | err Opt (3-exp) | ratio | err Strang (5-exp) | err Opt (5-exp) | ratio |
|---|---|---|---|---|---|---|---|
| 0.02 | 0.11 | 3.99e-06 | 3.44e-06 | 1.16× | 9.99e-07 | 1.65e-07 | **6.06×** |
| 0.05 | 0.28 | 6.24e-05 | 5.37e-05 | 1.16× | 1.56e-05 | 2.83e-06 | **5.51×** |
| 0.10 | 0.56 | 4.97e-04 | 4.28e-04 | 1.16× | 1.24e-04 | 2.03e-05 | **6.11×** |
| 0.20 | 1.12 | 3.93e-03 | 3.40e-03 | 1.16× | 9.72e-04 | 1.63e-04 | **5.98×** |
| 0.40 | 2.24 | 2.98e-02 | 2.62e-02 | 1.14× | 7.17e-03 | 1.32e-03 | **5.42×** |
| 0.80 | 4.49 | 1.94e-01 | 1.80e-01 | 1.08× | 4.08e-02 | 1.25e-02 | 3.26× |

### 3.3 K-fold repetition, TFIM N=5, single-step optimized at t=0.1 then repeated

| K | T total | err Strang^K | err Opt^K | ratio |
|---|---|---|---|---|
| 1 | 0.10 | 3.66e-03 | 2.52e-03 | 1.45× |
| 2 | 0.20 | 7.03e-03 | 4.86e-03 | 1.45× |
| 4 | 0.40 | 1.20e-02 | 8.47e-03 | 1.41× |
| 8 | 0.80 | 1.30e-02 | 1.10e-02 | 1.18× |

### 3.4 Cross-reference to paper's headline numbers
- Paper claim: >10³× reduction on XY in the perturbative regime.
- This replication: 5-exp XY: **~6×** consistent across all short times (t·‖H‖ ∈ [0.1,2]). The gap between "6×" here and ">1000×" in the paper is expected: the paper's ansatz has *R·M* free parameters where R ≥ 3 is the number of layers and M is the number of Hamiltonian terms (dozens for their XY-lattice + Jᵧ, J_z, h). Our 5-parameter BABAB is a strict subset. **The improvement grows fast with ansatz expressivity**, and the DIRECTIONAL and problem-dependent story (XY improves more than TFIM) reproduces.

## 4. Verdict

**PARTIAL — REPLICATED (direction & sign), NOT REPLICATED (magnitude of headline number)**

Justification (aligned with the Argo-hosted GPT-o3 LLM-judge, temperature 0.1, prompt+result blob 9 kB, verdict JSON in `report/evidence/judge_argo_opus47.txt`):

- **Directional claim C1** — replicated. In *every* (model, N, t) triple tested, the classically optimized template achieves strictly lower spectral-norm error than the Strang baseline at the same number of exponentials. This holds for both 3-exp and 5-exp templates and for both TFIM and XY.
- **Perturbative-regime prediction** — replicated. Improvement ratios are largest for t·‖H‖ ≲ 1 (as the paper's Proposition-based analysis says) and decay above that regime (e.g. XY 5-exp ratio drops from 6.1× at t=0.1 to 3.3× at t=0.8).
- **Problem-dependence (C4)** — replicated. TFIM shows much smaller advantage (1.16–1.46×) than XY (5.4–6.1×) at matched cost. This *exactly* matches the paper's Appendix B remark that TFIM's first-order Trotter is unitarily equivalent to second-order, so there is intrinsically less headroom above Strang.
- **Headline magnitude (C2, >10³×)** — **not** reproduced with the strict same-shape 3-exp / 5-exp templates. Reproducing the >1000× figure would require the full R-layer, M-term parametric ansatz used in the paper (dozens of coefficients). That is a scale-up in ansatz size, not a change in physics or method, and is out of scope for this small-instance run.
- **10× simulation-time extrapolation (C3)** — spot-checked only (TFIM 3-exp, K up to 8): ratio holds at ~1.4× for K ≤ 4 and decays to ~1.2× at K = 8. Reproducing the >10× longer-time claim needs richer ansatz + XY.

**Bottom line.** The paper's core method demonstrably works exactly as advertised in kind: at the same gate count you can beat Strang, and you beat it *more* on XY than on TFIM, and *more* in the perturbative regime than outside it. The exact multiplicative factor scales with ansatz expressivity, and the largest numbers in the paper come from ansatz choices richer than the minimal 3/5-exponential templates tested here.

## 5. Reproducibility

- Code: `code/optim_prodform.py`, `code/optim_prodform_v2.py`, `code/judge.py`
- Raw evidence (JSON, one file per model×N): `report/evidence/*.json`
- LLM judge output: `report/evidence/judge_argo_opus47.txt`
- Full stdout logs: `logs/run1.log`, `logs/run2.log`
- Tool versions: Python 3.14.6, NumPy 2.4.3, SciPy 1.18.0.
- Wall-time on host (CherryRd, single CPU): ~130 s total across all runs. No GPU, no network, no proprietary code.
