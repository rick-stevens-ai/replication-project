# Workflow — Huang & Shen (2021) IMEX/SAV Navier–Stokes replication

**Paper:** Huang & Shen, SINUM 59(6):2926–2954, 2021 (doi:10.1137/21M1404144).
**Replicator:** OpenClaw subagent (Ollie), 2026-07-02.
**Verdict:** REPLICATED.

## 0. Ground rules
- No public code accompanies the paper. Solver written from scratch from the paper's equations.
- Free-endpoint only (Argo). No paid inference. Judges = 3 independent Argo models (gpt-5.2, gemini-2.5-pro, gpt-4.1) at temperature 0.
- Compare **invariant quantities** (fitted temporal orders) against the paper's Figure-1 log-log slopes; do not chase error magnitudes that are constant-of-integration / forcing dependent.

## 1. Read the paper and extract testable claims
- Pulled arXiv:2103.11025 (open access) and the SINUM published version.
- Enumerated claims C1–C5 in a table (see REPORT.md §1). Marked C1+C2 as the numerical headline; C3 as a numerical spot-check; C4 as qualitative (skip, honestly flagged); C5 as analytical (out of scope).

## 2. Set up the manufactured problem (Example 1)
- Ω=(0,2)², periodic, ν=1, T=1; smooth exponential-of-sine velocity and pressure fields.
- Verified `∇·u ≡ 0` symbolically in SymPy.
- Derived `f = u_t − νΔu + (u·∇)u + ∇p` analytically by hand.
- Cross-checked hand-coded forcing against SymPy `lambdify` reference → max abs diff **5.7e-14** (`derive_forcing.py`).

## 3. Implement Fourier-spectral spatial operators (`hs_solver.py: Spectral2D`)
- N=40 modes/direction; FFT-based ∂x, ∂y, Δ.
- Leray projection `𝕡` in Fourier space (diagonal).
- Spectral advection `(u·∇)u`.
- Pressure recovery `Δp = ∇·f − ∇·(u·∇u)`; sanity check against the exact velocity → exact pressure to **2.5e-13**.

## 4. Implement IMEX-BDFk / AB-k / SAV time stepper (`hs_solver.py`)
- BDFk coefficients (paper eqs. 3.8–3.11) hard-coded for k=1,2,3,4.
- AB-k extrapolation of the convective term.
- SAV variable `r(t) = E(u) + 1` with `E = ½‖∇u‖²` (2D).
- Discrete dissipation law ∝ `‖Δū‖²`.
- Forced-case r-update includes the analytically-derived production term `(f, −Δū) = (∇f, ∇ū)` (see failure_analysis.md — this was the fix for the collapse mode).
- Rescale `u^{n+1} = η_k^{n+1} ū^{n+1}` with `η_k = 1 − (1−ξ)^k`, `ξ = r^{n+1}/(E(ū^{n+1})+1)`.
- Multistep bootstrap: seed the first k levels from the exact solution.

## 5. Convergence sweep (`run_convergence.py`)
- Δt ∈ {1/10, 1/20, 1/40, 1/80, 1/160} for each BDFk.
- Compute `‖e_u‖_{H¹}` and `‖e_p‖_{H¹}` at T=1 via Parseval.
- Fit log‖e‖ vs logΔt by least squares → order.
- Dump JSON to `evidence/convergence_results.json`.

## 6. Stability spot-check (`stability_test.py`)
- Δt = 0.05 (deliberately coarse relative to the sweep).
- Track H¹-energy and SAV factor η over the full run.
- Dump JSON to `evidence/stability_results.json`.

## 7. Plot (`plot_convergence.py`)
- Log-log plot of `‖e_u‖_{H¹}` vs Δt with fitted slopes, saved to
  `evidence/convergence_plot.png`. Visually confirms clean order-k halving.

## 8. Multi-judge assessment (`judge.py`)
- Prompt: paper claim + our fitted orders + stability numbers.
- 3 endpoints (gpt-5.2, gemini-2.5-pro, gpt-4.1), temperature 0.
- Dump full text to `evidence/judges.json`.
- All 3 return REPLICATED (see REPORT.md §4).

## 9. Report (`report/REPORT.md`, `report/REPORT.tex`)
- Structured summary of paper, method, results vs paper, judges, verdict.
- Explicit **Genuine Critique** section in the LaTeX report enumerating honest limitations (see failure_analysis.md for the failure narrative and REPORT.tex §"Genuine critique" for the itemized caveats).

## 10. Reproduce
```bash
cd work
python3 hs_solver.py           # full sweep to stdout
python3 run_convergence.py     # -> evidence/convergence_results.json
python3 stability_test.py      # -> evidence/stability_results.json
python3 plot_convergence.py    # -> evidence/convergence_plot.png
python3 judge.py               # -> evidence/judges.json
```

## Decision log
- **Compare orders, not magnitudes.** Paper's headline is a Figure-1 log-log slope; magnitudes depend on the manufactured constant. Orders are the invariant, and are what we report.
- **Skip Example 2.** Qualitative (vorticity contours); no reference number to check against.
- **Derive the forced r-update ourselves.** Paper theory sets f=0; without the analytic production term the SAV factor collapses. Documented as an honest subtlety, not a paper-quoted equation.
- **LLM judges are corroborative, not the primary evidence.** The primary evidence is the clean order-k halving under Δt-refinement.
