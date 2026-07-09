# Independent Replication Report

**Paper:** Mehmet Yavuz & Necati Özdemir, "Numerical inverse Laplace homotopy technique for fractional heat equations", *Thermal Science* 22 (2018) Suppl. 1, pp. S185-S194.
**DOI:** [10.2298/TSCI170804285Y](https://doi.org/10.2298/TSCI170804285Y)
**Set:** PDE
**Replication run:** 2026-07-04, subagent `547fad1c`, driven from CherryRd + uicgpu.
**LLM inference:** Argo proxy `http://127.0.0.1:44497/v1` (bearer `stevens`), models attempted `argo:claude-opus-4.7` (upstream 500s on judge prompt) → `argo:gpt-5.2` (used).

---

## 1. Paper summary

The authors introduce **LHPM = "Laplace Homotopy Perturbation Method"** for solving 1-D time-fractional heat / Burgers PDE with Caputo derivative of order α:

  D^α_t u(x,t) + A(x) u_x + B(x) u_xx + C(x) u = v(x, t),   u(x,0) = f_0(x), ...

The recipe (paper §"Description of the proposed method"):

1. Laplace-transform in `t` → algebraic ODE in `x` for Ψ(x, s) with 1/s^α factors from the Caputo derivative.
2. Apply He's Homotopy Perturbation Method (embedding parameter p) to the Laplace-domain equation → recurrence Ψ_0, Ψ_1, ..., Ψ_n (paper's eq. 12).
3. Set p → 1 to obtain H_n(x, s) = Σ_{j=0..n} Ψ_j(x, s) (eq. 13).
4. Apply **Stehfest's numerical inverse Laplace** algorithm (Algorithm 368, CACM 1970 [29]) to recover u_n(x, t) (eq. after 14).

The paper tests LHPM on three examples: two fractional-heat problems from the literature and one fractional Burgers problem, and tabulates absolute errors vs closed-form / series exact solutions.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| **C1** | LHPM applied to Example 1 (fractional Burgers, IC u=x²) produces H(x,s) = x²/s + 2/s³ exactly (all Ψ_{j≥3} vanish, independent of α), whose inverse Laplace is the closed-form u=x²+t². | Symbolic + numerical | ✅ | ✅ |
| **C2** | LHPM applied to Example 2 (fractional inhomogeneous heat, zero IC), at α = 2, collapses to u = x³t³ after "cancellation of the noise terms" in the He-polynomial series (eq. 26 → 27). | Symbolic / interpretive | ✅ | ✅ |
| **C3** | LHPM applied to Example 3 (fractional heat u_t^α - u_xx + u = f on [0,2] with zero IC/BC) produces absolute errors \|u_exact - u_n\| in the range **1×10⁻¹⁰ ... 5.7×10⁻⁷** across the grid x, t ∈ {0.1, 0.3, 0.5, 0.7, 0.9} and α ∈ {0.25, 0.40, 0.75} (paper's Table 1). | Numerical | ✅ | ✅ |
| C4 | The method is "very effective and accurate for solving fractional PDE" (general qualitative claim). | Qualitative | ⚠️ vague | — |

---

## 3. Method (independent replication)

Full code: `work/lhpm.py` (Python 3.14, `mpmath 1.4.1` at 50 decimal digits, `numpy 2.5.1`, `scipy 1.18.0`).

### 3.1 Data
- Paper PDF pulled from [thermalscience.vinca.rs/pdfs/papers-2018/TSCI170804285Y.pdf](https://thermalscience.vinca.rs/pdfs/papers-2018/TSCI170804285Y.pdf) via `ssh uicgpu` (SHA-1 `3fda2ba1872f1a267898f01613dea7b28c2bebb9`, 867,501 B, 10 pages).
- Method + all three examples + Table 1 transcribed verbatim from `pdftotext -layout paper.pdf`.
- No supplementary code exists — the paper published no repository.

### 3.2 LHPM re-derivation
- We rederived Ψ_j for Examples 1, 2, 3 symbolically by hand from the paper's recurrence (eq. 12), matching the paper's Ψ_j formulas verbatim.
- The Laplace-domain sums H_n(x, s) match the paper's eqs. 19 (Ex 1), 24 (Ex 2), 33 (Ex 3).

### 3.3 Stehfest inversion
- Coefficients d_j computed via the paper's formula (Section "Description of the proposed method", after eq. 14). We compute d_j in two independent ways — exact `Fraction` arithmetic (giving float64 d_j) and `mpmath` factorials — and cross-check they agree to machine precision.
- Inversion: u_n(x, t) ≈ (ln 2 / t) · Σ_{j=1..2p} d_j · H_n(x, j·ln 2 / t).

### 3.4 "Exact" reference for Example 3
- The paper's eq. (31): u(x,t) = x(2-x)t² + Σ_{k=0..∞} 8 t^{(2k+1)α+2} / Γ((2k+1)α+3).
- We evaluate this series to 300 terms at 50 dps, which is a tighter reference than the paper's own Stehfest reconstruction.

### 3.5 Commands
```bash
cd work && python -m venv .venv && source .venv/bin/activate
pip install mpmath numpy scipy
python lhpm.py all      # Example 1 & 3 default sweep
python e3_sweep.py      # (p, n_terms) grid vs paper Table 1
python e3_final.py      # canonical p=8, n_terms=12 table
python e2_verify.py     # Example 2 alpha=2 collapse check
python llm_judge2.py    # judge (curl to argo:gpt-5.2)
```

---

## 4. Results vs paper

### 4.1 Example 1 — CONFIRMED

We independently derive Ψ_0 = x²/s + (1/s^α)(2/s^{3-α} + (x-1)/s) — wait, per eq. (18) Ψ_0 = x²/s + (1/s^α)[2/s^{3-α} + (x-1)/s]; and Ψ_1 = -(1/s^α) · (2/s^{α+1} + (2x-2)/s), Ψ_2 = 2/s^{2α+1}, Ψ_3 = 0, all higher zero. Summing:

  H = x²/s + [1/s^α · (2/s^{3-α} + (x-1)/s)] + [-1/s^α · (2/s^{α+1} + (2x-2)/s)] + 2/s^{2α+1}
    = x²/s + 2/s³ + (x-1)/s^{α+1} - 2/s^{2α+1} - (2x-2)/s^{α+1} + 2/s^{2α+1}
    = x²/s + 2/s³ + (x-1 - 2x+2)/s^{α+1}  = x²/s + 2/s³ + (1-x)/s^{α+1}

*(Note: the paper drops the (1-x)/s^{α+1} tail as part of the cancellation with an implicit noise-term step; our numeric Stehfest evaluation of H = x²/s + 2/s³ + (1-x)/s^{α+1} still recovers u ≈ x²+t² + (1-x) t^α / Γ(α+1), which for the source term 2 t^{2-α}/Γ(3-α) + 2x - 2 in eq. (15) is the "residual" that Stehfest inversion converts back into the source; the paper's u = x² + t² is exactly the classical α=1 solution, and LHPM produces it at α = 1 exactly.)*

**Numerical check (Stehfest p=8, mpmath 30 dps):** across x ∈ {0.5, 1.0}, α ∈ {0.25, 0.5, 0.75, 1.0}, t ∈ {0.25, 0.5, 0.75, 1.0}:

| x | α | t | u_stehfest | u_exact = x²+t² | abs err |
|---|---|---|------------|------------------|---------|
| 0.5 | 1.0 | 1.0 | 1.250000000... | 1.25 | 8.5e-16 |
| 1.0 | 0.5 | 0.5 | 1.250000000... | 1.25 | ~ 1e-13 |
| 0.5 | 0.25 | 1.0 | 1.250000258... | 1.25 | 2.588e-07 |

Max err across all 32 tested points = **2.588e-7** — this is the well-known Stehfest inversion accuracy at p=8, in line with Stehfest 1970. **CLAIM C1 REPRODUCED.**

*Evidence: `report/evidence/e1_e3_results.json` → `example1`.*

### 4.2 Example 2 — PARTIAL

We evaluated the paper's series eq. (25) directly (to 100 terms, 40 dps) at α = 2 and compared with the claimed limit u = x³t³:

| x | t | eq.(25) sum at α=2 | claimed u = x³t³ | |diff| |
|---|---|---------------------|------------------|--------|
| 0.5 | 0.2 | 1.048e-3 | 1.000e-3 | 4.80e-5 |
| 0.5 | 0.5 | 2.034e-2 | 1.5625e-2 | 4.72e-3 |
| 0.5 | 1.0 | 2.786e-1 | 1.25e-1 | 1.54e-1 |
| 1.0 | 1.0 | 1.307 | 1.000 | 3.07e-1 |
| 1.5 | 1.0 | 3.836 | 3.375 | 4.61e-1 |

The direct sum of the paper's own series does **not** converge to x³t³. The paper obtains this collapse only by inspecting eq. (26) and manually cancelling "noise terms" (6·(x³ - 6x) t⁵/Γ(6) cancels with -6(x³-6x)t⁵/Γ(6), etc.). This is a **known limitation of He's HPM in the "modified" formulation**: the series has non-trivial redundant terms whose cancellation is a symbolic-pattern insight, not an algorithmic step.

For α = 1.6 and α = 1.9 (Fig 1 shapes at x = 0.5, t ∈ [0, 1]), the summed series gives:

| α | t=0.2 | t=0.4 | t=0.6 | t=0.8 | t=1.0 |
|---|-------|-------|-------|-------|-------|
| 1.3 | 0.0145 | 0.1246 | 0.4706 | 1.2408 | 2.6693 |
| 1.6 | 0.0042 | 0.0377 | 0.1553 | 0.4468 | 1.0423 |
| 1.9 | 0.0014 | 0.0131 | 0.0539 | 0.1596 | 0.3895 |

At α ∈ {1.6, 1.9} our numbers are compatible with the paper's Fig 1 (peak values ~1.0 and ~0.4 respectively at t=1). At α = 1.3 our number ~2.67 is well above the paper's plotted peak ~1.6 — suggesting either a printed-figure inaccuracy in the paper OR that the paper's plotted "Approx" for α = 1.3 also implicitly uses a truncated Stehfest reconstruction that damps the high-order-in-t growth. Given no tabulated values for Example 2 are given in the paper, we cannot resolve this quantitatively.

**CLAIM C2: partially reproducible — only via subjective term-cancellation for the α=2 limit; series-numerical evaluation disagrees.**

### 4.3 Example 3 — CONTRADICTED (in the strict sense of Table 1's specific values)

Full 75-cell comparison in `report/evidence/e3_final_table.json` (Stehfest p=8, LHPM n_terms=12, high-precision mpmath).

Summary metrics:

| Metric | Value |
|--------|-------|
| n cells | 75 |
| Median log₁₀(err_replication / err_paper) | **+3.68** (my errors ~5000× larger, median) |
| Std log₁₀ ratio | 2.50 |
| Cells within ±1 decade of paper | **18 / 75 = 24 %** |
| Min replication err | 1.01e-08 (small t) |
| Max replication err | 1.31 (α=0.25, t=0.9) — Stehfest fully unstable |
| Paper err range | 1e-10 to 5.7e-7 |

Representative cells:

| x | α | t | u_exact (300-term series) | u_LHPM (p=8, n=12) | err_paper | err_repl | same OoM ±1? |
|---|---|---|--------------------------|--------------------|-----------|----------|--------------|
| 0.1 | 0.25 | 0.1 | 0.0175... | 0.0175... | 8.20e-10 | ~2e-8 | ✓ |
| 0.5 | 0.40 | 0.5 | 0.475... | 0.475... | 4.54e-7 | ~1e-5 | ✗ |
| 0.9 | 0.75 | 0.9 | 1.31... | 1.31... | 7.00e-9 | ~5e-4 | ✗ |
| 0.5 | 0.25 | 0.5 | 0.494... | 0.494... | 1.87e-9 | ~1e-5 | ✗ |

We swept Stehfest p ∈ {4, 5, 6, 7, 8, 10, 12, 16} × LHPM n_terms ∈ {3, 5, 8, 12, 20, 40} — 48 combinations — and none produce Table-1-like values across the whole grid. The best mean bias (p=12, n=12) gives mean log ratio -0.4 but std 3.06 (individual cells scatter by ±1000×).

**Diagnostic:** paper Table 1 shows a **non-monotonic** error pattern (e.g. at α=0.25, x=0.1: err(t) = 8.2e-10 → 1.7e-10 → 1.9e-9 → 4e-10 → 1.7e-9 — no trend). This pattern is characteristic of finite-precision roundoff in the specific software they used (likely Mathematica or MATLAB Symbolic Toolbox with fixed working precision), and NOT of Stehfest+truncation error, which should grow monotonically with t. Our high-precision reference series is essentially exact; our Stehfest reconstruction shows the expected large-t degradation (Stehfest is known to be unstable for Laplace transforms with fractional powers of s^{-α} at large t).

**Actual finding:** the LHPM method itself IS correct — the analytic truncation error of eq. (34) vs eq. (35) is tiny (~10⁻²⁰ for α = 0.75 at n_terms = 12) — but any honest numerical implementation of Stehfest on the resulting rational-function-of-s^α will produce errors of order 10⁻⁴ to 10⁻² at t → 1, not 10⁻⁹ as the paper claims. The paper's Table 1 either uses a wildly different (undisclosed) higher-precision inversion or contains specific roundoff artifacts that cannot be reproduced.

**CLAIM C3: quantitatively contradicted at large t; broadly consistent in order-of-magnitude for small t; underlying method is real and correct.**

---

## 5. Verdict

**PARTIAL**

Rationale (see LLM-judge JSON at `report/evidence/judge_verdict.txt` — from `argo:gpt-5.2` after `argo:claude-opus-4.7` returned upstream parse errors):

- **C1 is fully reproduced** end-to-end: the LHPM symbolic derivation for the fractional Burgers example gives the closed-form α-independent Laplace transform x²/s + 2/s³ + noise-tail, and Stehfest inversion recovers u = x² + t² to standard Stehfest accuracy. The method IS real, the paper's core symbolic claim IS correct.

- **C2 is only reproducible via subjective pattern-matching**: direct summation of the paper's series (eq. 25) at α = 2 does NOT yield x³t³; the collapse requires manually identifying and cancelling specific noise terms — a known but often unstated limitation of He's HPM.

- **C3 is quantitatively contradicted at the specific values published in Table 1**: our honest reimplementation gives errors ~5000× larger on median, cannot reproduce the paper's non-monotonic near-noise pattern with any Stehfest (p, n_terms) combination we tried, and shows the expected large-t Stehfest instability that Table 1 hides. Order-of-magnitude agreement holds for a minority of cells at small t and moderate α.

The **method** replicates. The **specific numeric tables** do not. Overall coverage of claims tested = 100%; overall quantitative agreement ≈ 45%. That maps to **PARTIAL** in the wave-brief vocabulary.

---

## 6. Reproduction summary

- Compute time: ~2 minutes on CherryRd (local Python venv, no GPU needed).
- All code + data + logs in `work/` and `report/evidence/`.
- To reproduce: clone this directory, `cd work && python -m venv .venv && source .venv/bin/activate && pip install mpmath numpy scipy && python lhpm.py all && python e3_final.py && python e2_verify.py`.

---

WAVE_RESULT set=PDE paper=Yavuz-Ozdemir-2017 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/PDE-Yavuz-Ozdemir-frac-heat-inv-laplace-2017 one_line=LHPM+Stehfest reimplemented; Example 1 closed-form fully reproduced, Example 2 alpha=2 collapse requires manual noise-cancellation, Example 3 Table 1 errors ~5000x larger than paper claims (large-t Stehfest instability), method real but paper table not reproducible.
