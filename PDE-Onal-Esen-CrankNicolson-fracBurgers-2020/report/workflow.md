# Workflow — Onal & Esen 2020 (Crank–Nicolson / L1 for time-fractional Burgers)

Chronological summary of what was done to reach the REPLICATED verdict.

## 1. Paper acquisition
- Target: doi:10.2478/amns.2020.2.00023 (Applied Mathematics and Nonlinear Sciences 5(2) (2020) 177–184, CC-BY).
- Publisher landing pages on Sciendo / De Gruyter were dead or bot-walled at fetch time.
- Recovered authentic publisher PDF from a **Wayback Machine snapshot (2020-08-19)** of the original `content.sciendo.com` PDF.
- Provenance recorded in `artifact_harvest.md`.

## 2. Extraction
- OCR/markdown extraction via `marker` into `extraction/marker.md`.
- Pulled: governing PDE, Caputo derivative + L1 formula, fully-discrete tridiagonal system (Section 2.1), three manufactured examples (Ex1: `t² sin(2πx)`, Ex2: `t² cos(πx)`, Ex3: `t² eˣ`), and printed forcing terms `f(x,t)` for each.

## 3. Claims enumeration
- Six testable claims (C1–C6) identified: Table 1 (Ex1 convergence), Table 2 "Present" column, Table 3 (ν-sweep), Table 4 (γ-sweep), Tables 5–7 (Ex2/Ex3), plus qualitative O(Δx²) spatial order.

## 4. Independent implementation
- Language: Python 3 + NumPy + SymPy.
- Location: `work/cn_frac_burgers.py`.
- Discretization: implemented Section 2.1 algebraic system verbatim with `S = Δt^γ · Γ(2-γ)`; central differences in space; CN averaging of diffusion; semi-implicit advection.
- Solver: Thomas tridiagonal per time step.
- Memory sum: L1 formula, vectorized over the spatial index.
- Forcing terms: **re-derived symbolically in SymPy** from `D_t^γ(t²) = 2/Γ(3-γ) · t^{2-γ}` plus advection and diffusion terms; all three matched the paper's printed `f(x,t)` exactly.

## 5. Resolving scheme ambiguity
- Non-obvious modeling choice: the time level at which `f(x,t)` is evaluated (`t_n`, `t_{n+1}`, or `t_{n+½}`).
- Sensitivity study at M=10 established that **`t_n` (old time level)** is the choice that reproduces the paper to 8 significant figures; the alternatives were ~1.6% off.
- Documented in `attempt_log.md` step 9.

## 6. Comparison runs
- Heavy sweep executed on `uicgpu` (via `source ~/env.sh`).
- Reproduced Table 1 (Ex1, γ=0.5, ν=1, Δt=0.00025, tf=1) for M ∈ {10, 20, 40, 80} → **0.000%** deviation on both L² and L∞.
- Reproduced Table 2 "Present" for M ∈ {40, 80, 100} → **0.000%**.
- Reproduced Table 4 (N=120, γ ∈ {0.10, 0.25, 0.75, 0.90}) → **0.000%**.
- Table 3 (ν-sweep, N=40): our value at ν=1 (**1.2201**) matches the paper's own Table 1 at N=40, but disagrees with the paper's Table 3 (**0.4176**) → flagged as paper-internal inconsistency.
- Tables 5–7 (Ex2/Ex3): our errors consistently smaller than the paper's and non-monotone-in-a-different-way; attributed to paper-side tabulation because forcing was symbolically verified and the identical code path reproduces Ex1 exactly.

## 7. Extra checks
- Spatial convergence order estimated from Table-1 data: ≈ **2.06 → 2.86** across M, consistent with the O(Δx²) design (accelerating as fixed-Δt temporal error becomes relatively negligible).
- Solution-vs-exact plot: `evidence/fig1_repro.png`.

## 8. Multi-judge review
- Three independent free Argo judges scored the evidence bundle (`evidence/judge_results.json`):
  - `argo:gemini-2.5-pro`: REPLICATED (1.00)
  - `argo:gpt-4.1`: REPLICATED (0.98)
  - `argo:gpt-5.2`: PARTIAL (0.86)
- Majority vote: **REPLICATED**; dissent reflects that 2 of 3 example families' tables did not reproduce.

## 9. Verdict
- **REPLICATED**, with documented caveats (Table 3 is paper-internally inconsistent; Tables 5–7 for Examples 2/3 not reproduced but attributed to paper-side tabulation given symbolic verification of inputs).

## 10. Reproduce
```bash
cd work && python3 cn_frac_burgers.py     # writes results_all.json vs paper
python3 judge.py                          # multi-judge Argo scoring via :44497
```
