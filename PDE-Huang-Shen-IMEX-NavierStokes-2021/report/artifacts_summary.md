# Artifacts Summary — Huang & Shen (2021) IMEX/SAV NS replication

**Location root:** `~/Dropbox/REPLICATE-PROJECT/PDE-Huang-Shen-IMEX-NavierStokes-2021/`

## Layout

```
PDE-Huang-Shen-IMEX-NavierStokes-2021/
├── extraction/
│   └── (paper extraction workspace)
├── report/
│   ├── REPORT.md                 # human-readable replication report (verdict: REPLICATED)
│   ├── REPORT.tex                # LaTeX report + Genuine Critique section
│   ├── open_questions.json       # 5 genuinely open questions grounded in the paper
│   ├── workflow.md               # end-to-end replication workflow
│   ├── artifacts_summary.md      # this file
│   └── failure_analysis.md       # honest failure/near-miss narrative
└── work/
    ├── hs_solver.py              # from-scratch Fourier-spectral IMEX-BDFk/SAV solver
    ├── derive_forcing.py         # hand-coded forcing + SymPy cross-check (max diff 5.7e-14)
    ├── run_convergence.py        # convergence sweep driver
    ├── stability_test.py         # large-Δt stability spot-check
    ├── plot_convergence.py       # log-log convergence plot generator
    ├── judge.py                  # multi-Argo-judge harness (gpt-5.2, gemini-2.5-pro, gpt-4.1)
    ├── attempt_log.md            # session log incl. the forced-SAV subtlety
    └── evidence/
        ├── convergence_results.json  # per-scheme, per-Δt H¹ errors + fitted orders
        ├── stability_results.json    # H¹-energy trace, SAV factor η range at Δt=0.05
        ├── convergence_plot.png      # log-log ‖e_u‖_{H¹} vs Δt
        └── judges.json               # full text of 3 LLM verdicts
```

## Key results (from REPORT.md §3)

**Fitted temporal convergence orders (H¹):**

| Scheme    | Velocity order | Pressure order | Expected | Match |
|-----------|----------------|----------------|----------|-------|
| SAV/BDF1  | 1.00           | 0.95           | 1        | ✓     |
| SAV/BDF2  | 1.89           | 1.95           | 2        | ✓     |
| SAV/BDF3  | 3.02           | 3.01           | 3        | ✓     |
| SAV/BDF4  | 4.14           | 4.08           | 4        | ✓     |

Representative velocity H¹ error at Δt=1/160: BDF1 3.9e-2 → BDF4 3.2e-8.

**Stability spot-check at Δt=0.05:**

| Scheme   | max H¹-energy (SAV) | exact final E | η range           |
|----------|---------------------|---------------|-------------------|
| SAV/BDF2 | 707.5               | ~707.8        | [0.9850, 1.0000]  |
| SAV/BDF3 | 707.8               | ~707.8        | [1.0000, 1.0008]  |

**Multi-judge verdicts:** all 3 REPLICATED (argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1).

## Internal-consistency validations

| Check                                            | Result       |
|--------------------------------------------------|--------------|
| `∇·u ≡ 0` for manufactured solution (SymPy)      | exact        |
| Hand-coded `f` vs SymPy `lambdify` reference     | 5.7e-14      |
| Pressure recovery from exact velocity            | 2.5e-13      |
| Order-k slope for k=1..4 (least-squares fit)     | 1.00/1.89/3.02/4.14 velocity |
| SAV factor η stays ≈ 1 at Δt=0.05                | [0.9850, 1.0008] |

## Scope of what was verified

- **Verified numerically:** claims C1, C2 (temporal convergence orders) and C3 (numerical stability at a large step).
- **Not run:** C4 (Example 2, double shear layer — qualitative, no reference number).
- **Out of scope:** C5 (analytical error estimates).
- **Coverage:** 2D periodic only. 3D and no-slip BCs untouched. See `open_questions.json` for the genuinely open extensions.
