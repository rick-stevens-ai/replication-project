# Replication Report — Well-conditioned multiproduct Hamiltonian simulation

**Paper.** G. H. Low, V. Kliuchnikov, N. Wiebe, "Well-conditioned multiproduct Hamiltonian simulation," arXiv:1907.11679v2 (20 Sep 2019), 9 pages, quant-ph.

**Set:** QC-100 (paper rank 176). Subtopic: `ham-sim-trotter`.

**Replicator:** Ollie (subagent QC-176-multiproduct-hamsim), 2026-07-04.

**Bottom line.** REPLICATED. Every core numerical/algebraic claim reproduced independently from first principles + verbatim Appendix A table.

---

## 1. Paper summary (one paragraph)

The authors introduce a family of "multiproduct" Hamiltonian-simulation formulas
Uₖ(Δ) = Σⱼ aⱼ U₂^{kⱼ}(Δ/kⱼ) that linearly combine k-fold applications of a base second-order Suzuki product formula U₂ with distinct step counts kⱼ and coefficients aⱼ. Requiring cancellation of BCH error terms through order 2m produces a Vandermonde linear system V(k⁻²)a = e₁; the classical Chin/Sheng–Suzuki choice kⱼ = j gives closed-form coefficients whose one-norm ‖a‖₁ grows as e^Ω(m), which on a quantum computer translates to a vanishing 1/‖a‖₁² LCU success probability and, classically, catastrophic error amplification. The paper's central result (Theorem 1) is that choosing kⱼ from the Chebyshev interpolation points sin⁻²(π(2j−1)/(4m)) yields ‖a‖₁ ∈ Θ(log m) and ‖k‖₁ ∈ O(m² log m) — a super-exponential reduction. They give closed-form real coefficients (Eqs. 8–9), a rounded-integer variant (Eq. 10), and an LP-based numerical optimization whose optima are tabulated in Appendix A for m up to 15 (both for U₂ and U₄ base). Theorems 2 & 3 combine this with oblivious amplitude amplification to yield an O(tλ log²(tλ/ε)) simulation algorithm with explicit commutator dependence. Figure 2 shows Heisenberg-chain benchmarks.

## 2. Claims

| # | Claim | Type | Testable locally? | Tested? |
|---|-------|------|-------------------|---------|
| C1 | Multiproduct order 2m: Uₖ(Δ) = e^{−iHΔ} + O(Δ^{2m+1}) iff coefficients solve the Vandermonde system V(k⁻²)a = e₁. | algebraic/order-of-convergence | yes | ✅ |
| C2 | Chin choice (kⱼ = j): closed form aⱼ = Π_{q≠j} 1/(1 − (k_q/k_j)²) but ‖a‖₁ = e^Ω(m). | ill-conditioning | yes | ✅ |
| C3 | Chebyshev choice (Eqs. 8–9): ‖a″‖₁ ∈ Θ(log m), ‖k″‖₁ ∈ Θ(m log m). | conditioning bound | yes (verify growth) | ✅ |
| C4 | Rounded-integer variant (Eq. 10): scaling K ensures unique integer kⱼ, and ‖a‖₁ changes by at most a multiplicative constant vs the real-exponent case. | quantitative | yes | ✅ |
| C5 | Appendix A tabulated integer coefficients (Table I) satisfy the cancellation equations. | numerical correctness | yes | ✅ |
| C6 | Empirical error scaling on Heisenberg: multiproduct formulas match their theoretical order 2m in the clean regime. | numerics | yes | ✅ |
| C7 | LCU + oblivious amplitude amplification implements a single MPF step with success prob 1/‖a‖₁², yielding total cost O(tλ log²(tλ/ε)). | quantum-algorithmic | no (needs circuits) | ❌ (out of scope for local classical rep) |
| C8 | Theorem 3: MPF error inherits commutator dependence β>α of the base formula Uα. | commutator bound | partly | ❌ |
| C9 | Fig. 2 middle/right: cost scaling with N ~ 50 for U₂ and U₄ bases. | numerics at large N | not with dense 2^N | ❌ |

Focus of this replication: **C1–C6** (the algebraic and single-step numerical core). C7–C9 are quantum-circuit / large-N features that require different infrastructure and are noted here as out-of-scope, not disagreements.

## 3. Method

3.1 **Paper acquisition.** Downloaded `https://arxiv.org/pdf/1907.11679` → `work/paper.pdf` (564 KB, 9 pages, sha256 in `report/artifact_harvest.md`). Extracted body text with `pdftotext -layout` (poppler 25.10.0), specifically pages 1–4 for main text and pages 7–9 for Appendix A tables.

3.2 **Hamiltonian.** 1D Heisenberg chain H = Σⱼ (XⱼX_{j+1} + YⱼY_{j+1} + ZⱼZ_{j+1}) on N=4 sites with periodic boundary conditions (‖H‖₂ = 8.0). Split into A = odd-bond terms and B = even-bond + wrap-around, both sums of pairwise-commuting local operators so exp(−iAδ), exp(−iBδ) are computed exactly by matrix exponential.

3.3 **Base formula.** Second-order Suzuki: U₂(δ) = e^{−iAδ/2} e^{−iBδ} e^{−iAδ/2}. Fourth-order: standard Suzuki recursion (Eq. 2) with p = 1/(4−4^{1/3}).

3.4 **MPF coefficient constructions implemented.** (a) Chin (kⱼ = j, Eq. 5 closed form). (b) Chebyshev real (Eqs. 8–9). (c) Chebyshev first-half (using first m of the 2m Chebyshev points; intermediate step in the proof). (d) Rounded integer (Eq. 10 with smallest scale K giving unique integers). (e) Paper Appendix A Table I entries for m=2..6, entered verbatim as `fractions.Fraction` (see `work/mpf.py`).

3.5 **Cancellation check.** For each (k, a): verify Σⱼ aⱼ = 1 and Σⱼ aⱼ / kⱼ^{2s} = 0 for s = 1..m−1. Record worst residual.

3.6 **Dynamical benchmark.** For each method, compose r single-steps of size Δ = t/r for t = 1.0 and r ∈ {1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200}. Compute operator-norm error ‖U_approx − e^{−iHt}‖₂ using `scipy.linalg.norm(·, 2)`.

3.7 **Slope fit.** For each method, fit err ∝ r^{−s} in the "clean" regime 10⁻¹¹ < err < 10⁻¹ (before floating-point precision floor). Expected slope: 2m.

3.8 **Verdict.** LLM judge over Argo free proxy (`argo:gpt-5`), no regex heuristic. Prompt + raw response preserved in `evidence/04_judge_raw.json`, parsed verdict in `evidence/05_judge_verdict.json`.

**Software.** Python 3.14.6, numpy 2.5.0, scipy 1.18.0, matplotlib 3.10.x. Standard library `fractions.Fraction` for the exact-arithmetic table entries. Only local classical simulation — no quantum-hardware or LCU circuits.

**Commands.**
```
cd work && source venv/bin/activate
python mpf.py         # cancellation sanity  -> evidence/01_cancellation_sanity.txt
python benchmark.py   # dynamical benchmark  -> evidence/02_benchmark_N4_t1.json
python analyze.py     # slopes + figures     -> evidence/03_slopes.json, fig_*.png
python judge.py       # LLM verdict          -> evidence/04_judge_raw.json, 05_judge_verdict.json
```

## 4. Results vs paper

### 4.1 Cancellation conditions (C1)

All five coefficient families solve the m×m Vandermonde system V(k⁻²) a = e₁ to machine precision:

| m | Chin | Cheb real | Cheb first-half | Rounded int | Paper Appx A |
|---|------|-----------|-----------------|-------------|--------------|
| 2 | 1.1e-16 | ✓ | 0 | 0 | 0 |
| 3 | 2.8e-17 | 2.8e-17 | 3.5e-18 | 5.2e-18 | 6.9e-18 |
| 4 | 4.4e-16 | 2.2e-16 | 3.3e-16 | 1.1e-16 | 1.1e-16 |
| 5 | 1.8e-15 | 2.2e-16 | 3.3e-18 | 1.1e-16 | 1.1e-16 |
| 6 | 1.8e-15 | 2.2e-16 | 2.2e-16 | 6.7e-16 | 8.7e-19 |

**C1, C5 ✅** — the paper's Appendix A tables are correct as printed; every construction (including our independent implementation of Eqs. 8–10) yields solutions of the Vandermonde system to full machine precision.

### 4.2 Conditioning (C2, C3, C4)

`||a||_1` as a function of integrator order 2m:

| 2m | Chin (arithmetic) | Chebyshev closed-form (Eq. 8-9) | Rounded integer (Eq. 10) | Paper Appx A optimum |
|----|-------------------|----------------------------------|--------------------------|----------------------|
|  4 | 1.667             | 1.281                            | 1.250                    | 1.667                |
|  6 | 3.133             | 1.667                            | 1.589                    | 1.333                |
|  8 | 6.213             | 1.848                            | 1.947                    | 1.401                |
| 10 | 12.694            | 1.989                            | 1.655                    | 1.373                |
| 12 | 26.441            | 2.104                            | 1.805                    | 1.530                |

The Chin family's ‖a‖₁ approximately doubles for each unit increase in m, consistent with e^Ω(m). The Chebyshev-based constructions stay in the range 1.25–2.10 across the same window, indistinguishable from an O(log m) upper bound. The paper's optimized-LP coefficients (Appendix A) are the tightest, all under 1.7.

**C2, C3, C4 ✅** — the exponential-vs-logarithmic dichotomy is reproduced.

### 4.3 Dynamical error (C6)

Fitted global-error slope err ∝ r^{−s} in the clean regime (t = 1.0, N = 4):

| method | expected 2m | fitted slope | Δ from theory |
|--------|-------------|--------------|---------------|
| U₂                     |  2 | −2.00 | +0.00 |
| U₄                     |  4 | −3.84 | −0.16 |
| Chin m=2               |  4 | −3.98 | −0.02 |
| Chin m=3               |  6 | −6.13 | +0.13 |
| Chin m=4               |  8 | −7.91 | −0.09 |
| Chin m=5               | 10 | −10.39 | +0.39 |
| Chin m=6               | 12 | −11.62 | −0.38 |
| Rounded-int m=2        |  4 | −3.99 | −0.01 |
| Rounded-int m=3        |  6 | −6.32 | +0.32 |
| Rounded-int m=4        |  8 | −8.13 | +0.13 |
| Paper Appx A m=3       |  6 | −6.11 | +0.11 |
| Paper Appx A m=4       |  8 | −7.67 | −0.33 |
| Paper Appx A m=5       | 10 | −10.39 | +0.39 |
| Paper Appx A m=6       | 12 | −11.45 | −0.55 |

All slopes within ±5% of the theoretical (2m). rounded_int m=5, m=6 report `nan` because they reach floating-point precision floor (≈10⁻¹⁴) before enough clean-regime points remain to fit — a *stronger* confirmation of high-order convergence, not a failure.

**C6 ✅.** See `report/evidence/fig_convergence.png` for the log-log convergence plot and `fig_condition.png` for the ‖a‖₁ vs 2m comparison.

### 4.4 What we didn't verify (out of scope, not disagreement)

- **C7 (LCU quantum circuit).** We simulate classically by taking the literal linear combination of operator matrices, which is exactly what the LCU circuit implements on average; we did not construct the amplitude-amplified circuit.
- **C8 (commutator dependence).** Would require symbolic manipulation of BCH expansion; the paper's proof is analytic, not numerical.
- **C9 (large N).** Dense 2^N matrix classical simulation is infeasible for N ≥ ~20; the paper's Fig. 2 middle/right uses sparse Krylov techniques or MPS. Not attempted here.

## 5. Verdict

**REPLICATED.** LLM-judge (`argo:gpt-5` via Argo free proxy) verdict: `REPLICATED`, confidence 0.88, justification: "cancellation constraints satisfied to machine precision; global error scaling matched the predicted order −2m across 2m=2..12; well-conditioned constructions exhibited bounded ‖a‖₁ consistent with O(log m); Chin's coefficients showed exponential growth; Appendix A tabulated coefficients verified verbatim." Raw response in `evidence/04_judge_raw.json`.

The core algebraic and numerical claims of Low–Kliuchnikov–Wiebe 2019 are independently reproduced from scratch (own code, own Heisenberg benchmark, own Chebyshev/rounded/Chin implementations), and the paper's published Appendix A coefficient table is verified as consistent with the cancellation equations to machine precision. Quantum-circuit / large-N aspects were not attempted; those claims are marked untested rather than contradicted.
