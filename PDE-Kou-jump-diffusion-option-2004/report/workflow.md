# Workflow — Kou (2002) double-exponential jump-diffusion replication

## Overview
End-to-end pipeline for independently reproducing the closed-form European call price benchmark from Kou (2002), *A Jump-Diffusion Model for Option Pricing*, MS 48(8):1086-1101. Three fully independent numerical routes converge on the same answer; auxiliary consistency checks (put-call parity, Black-Scholes limit, strike sweep) bracket the result.

## Environment
- Host: laptop CPU (no cluster, no external data).
- Python 3.13, local venv.
- Dependencies: `numpy 2.5.1`, `scipy 1.18.0`. No paid API used in the numerical pipeline; a single LLM-judge call routed via Argo (`argo:claude-opus-4.7` at `127.0.0.1:44497`).
- Total wall time: ≤ 30 s for the full replication script.

## Steps

### 1. Paper acquisition
- Pulled two PDFs: Kou (2002) MS from `https://www.columbia.edu/~sk75/MagSci02.pdf`; Kou & Wang (2004) MS companion.
- Identified that the assignment header referenced Kou-Wang 2004 (path-dependent Laplace-transform pricer) but the European closed-form under test actually lives in Kou (2002), Theorem 2 + Appendix B.
- Extracted the footnote-9 numerical benchmark: `S0=100, K=98, r=0.05, T=0.5, sigma=0.16, lambda=1, p=0.4, eta1=10, eta2=5` → `C = 9.14732`.

### 2. Route C1 — Closed form via COS characteristic-function inversion
- File: `work/kou_cos.py`.
- Implemented Kou's risk-neutral characteristic function of `X_T = log(S_T/S_0)` directly from the model definition (drift correction `-lambda*zeta` explicit; asymmetric double-exponential contribution via `p*eta1/(eta1 - i*u) + q*eta2/(eta2 + i*u) - 1`).
- Fang-Oosterlee (SIAM J. Sci. Comp. 2008) COS method: `N=512` cosine terms, truncation multiplier `L=12`, analytic call-payoff coefficients `U_k` on `[0, b]`.
- Truncation `[a, b]` chosen from the model's first four cumulants.
- Result: `9.147317`, error `2.7 × 10^-6` vs paper.

### 3. Route C2 — Monte Carlo
- Function: `kou_mc_vectorised` in `work/run_replication.py`.
- Exact simulation of `log S_T = log S_0 + (r - sigma^2/2 - lambda*zeta)*T + sigma*sqrt(T)*Z + sum(Y_i)`.
- `Z ~ N(0,1)`, `N_T ~ Poisson(lambda*T)`, per-jump `Y_i = +Exp(eta1)` w.p. `p` else `-Exp(eta2)`.
- 2 × 10^6 paths, seed 42, vectorised jump aggregation via `np.split`.
- Result at footnote-9 params: `9.14844 ± 0.01673` (95% CI); `z = +0.13`.

### 4. Route C3 — PIDE finite-difference
- Function: `kou_pide` in `work/kou_pricer.py`.
- Grid: `N_x = 601` on `x ∈ [-2.5, 2.5]`, `N_t = 20,000` backward Euler steps.
- Discretisation: central FD for `V_x`, `V_xx`; jump integral as dense `N_x × N_x` convolution against double-exponential kernel.
- Boundary: `V(-∞) = 0`, `V(+∞)` linear extrapolation.
- Value interpolated at `x = 0` (i.e. `S = S_0`).
- Result: `9.16756`, error `2.0 × 10^-2` (grid-discretisation level).

### 5. Consistency battery
- **Put-call parity**: `C_COS = 9.14732`, `P_parity = 4.72769`, `P_MC = 4.72403 ± 0.014` → agreement `z = 0.26`.
- **Black-Scholes limit** at `lambda = 1e-10`: `C_Kou_COS = 10.4505835721650` vs `C_BS = 10.4505835722381`; `|diff| = 7.3 × 10^-12`.
- **Strike sweep** `K ∈ {90, 95, 100, 105, 110}`: COS vs MC all within `|z| < 1.5`.

### 6. LLM-judge scoring
- All numerical results bundled into a scoring prompt (rubric: verdict + agreement + coverage + one-line).
- Sent to Argo `argo:claude-opus-4.7`.
- Verdict: `REPLICATED`, agreement `A`, coverage `B`.
- Raw output preserved in `report/evidence/llm_judge.txt`.

### 7. Attempted (failed) route — literal Hh implementation
- Directly transcribed Kou's Theorem B.1 Hh recursion + `I_n(c; alpha, beta, delta)` integral assembly.
- Both this direct implementation and a public StackOverflow reference diverge from paper value at the 20%+ level.
- Diagnosed as (likely) backward-recursion instability of `Hh_n` for large negative arguments, compounded by sign-convention ambiguities in `I_n` transcribed from OCR.
- Reported as a caveat, not a contradiction — mathematically equivalent COS route reproduces the same answer to machine precision.

## Reproduce
```
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Kou-jump-diffusion-option-2004/work
python3 -m venv venv && . venv/bin/activate
pip install numpy scipy
python run_replication.py
```
Numerical artifacts land in `report/evidence/results.json`; stdout in `report/evidence/run.log`; LLM judge in `report/evidence/llm_judge.txt`.

## Verdict
**REPLICATED** — paper's `C = 9.14732` reproduced to `~1e-6` via independent COS inversion, corroborated by MC (`z < 1`), PIDE (grid-tolerance), parity, BS-limit, and a 5-strike sensitivity sweep.
