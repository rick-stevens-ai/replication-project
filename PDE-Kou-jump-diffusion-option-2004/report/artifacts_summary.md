# Artifacts summary — Kou (2002) replication

Paper: Kou, S. G. (2002). "A Jump-Diffusion Model for Option Pricing." *Management Science* 48(8):1086–1101. DOI: 10.1287/mnsc.48.8.1086.166.

Verdict: **REPLICATED**.

## Directory layout

```
PDE-Kou-jump-diffusion-option-2004/
├── report/
│   ├── REPORT.md              # Canonical replication write-up (source of truth for numbers)
│   ├── REPORT.tex             # LaTeX version with dedicated "Genuine critique" section
│   ├── open_questions.json    # 5 truly-open follow-on research questions
│   ├── workflow.md            # End-to-end pipeline documentation
│   ├── artifacts_summary.md   # This file
│   ├── failure_analysis.md    # What went wrong / what remains unresolved
│   └── evidence/
│       ├── results.json       # Numerical outputs of all three routes + sweep
│       ├── run.log            # Full stdout from run_replication.py
│       └── llm_judge.txt      # Raw Argo claude-opus-4.7 verdict output
├── work/
│   ├── run_replication.py     # Driver script: MC + assembles all consistency checks
│   ├── kou_cos.py             # COS characteristic-function inversion pricer
│   └── kou_pricer.py          # PIDE explicit-Euler finite-difference solver
└── extraction/                # PDF text extraction (paper acquisition)
```

## Code artifacts

| File | Purpose | Key entry points |
|---|---|---|
| `work/kou_cos.py`      | Semi-analytic pricer via Kou characteristic function + Fang-Oosterlee COS inversion. | `kou_cf(u, T, params)`, `kou_call_cos(S0, K, T, r, params, N=512, L=12)` |
| `work/kou_pricer.py`   | PIDE explicit-Euler finite-difference solver on `x = log(S/S0)` grid. | `kou_pide(S0, K, T, r, params, Nx=601, Nt=20000, xrange=(-2.5, 2.5))` |
| `work/run_replication.py` | Top-level driver: runs COS + MC + PIDE + parity + BS limit + strike sweep; emits `results.json` + `run.log`; calls LLM judge. | `kou_mc_vectorised(...)`, `main()` |

## Numerical outputs (from `report/evidence/results.json`)

### Paper benchmark (footnote 9, p.1095)
Parameters: `S0=100, K=98, r=0.05, T=0.5, sigma=0.16, lambda=1, p=0.4, eta1=10, eta2=5`. Paper: `C = 9.14732`.

| Route | Price | |Error| vs paper |
|---|---|---|
| C1 · COS closed form (N=512, L=12)         | **9.147317**              | **2.7 × 10⁻⁶** |
| C2 · Monte Carlo (2 × 10⁶ paths, seed 42)  | 9.14844 ± 0.01673 (95% CI) | 0.001 (z = +0.13) |
| C3 · PIDE FD (601 × 20,000)                | 9.16756                    | 2.0 × 10⁻² (FD discretisation) |

### Strike sensitivity sweep

| K   | C_COS    | C_MC     | MC SE   | MC − COS | z-score |
|-----|----------|----------|---------|----------|---------|
|  90 | 14.81189 | 14.80093 | 0.01797 | −0.01096 | −0.61   |
|  95 | 11.11331 | 11.12721 | 0.01660 | +0.01390 | +0.84   |
| 100 |  7.95943 |  7.94670 | 0.01484 | −0.01273 | −0.86   |
| 105 |  5.45181 |  5.46717 | 0.01299 | +0.01537 | +1.18   |
| 110 |  3.59965 |  3.61299 | 0.01116 | +0.01334 | +1.20   |

All differences within ±1.5 MC standard errors across a full 20% strike range.

### Put-call parity (footnote-9 params)
- `C_COS = 9.14732`
- `P_parity = C - S0 + K·e^{-rT} = 4.72769`
- `P_MC = 4.72403 ± 0.01385`
- diff = 0.0037 (z = 0.26).

### Black–Scholes limit (`lambda = 10^{-10}`, `sigma = 0.2`, `K = S0 = 100`, `T = 1`, `r = 0.05`)
- `C_Kou_COS = 10.4505835721650`
- `C_BS_analytic = 10.4505835722381`
- `|diff| = 7.3 × 10^-12`

## Documentation artifacts

| File | What it contains |
|---|---|
| `REPORT.md`               | Primary write-up: paper summary, claims table, method (COS/MC/PIDE), all results tables, LLM-judge verdict, honest caveat on Hh route. **Source of truth for all numbers.** |
| `REPORT.tex`              | LaTeX rendering of REPORT.md with an expanded §7 "Genuine critique" (Hh not reproduced, single param set, no empirical smile fit, PIDE only at O(1e-2), unsigned COS derivation, single LLM judge). |
| `open_questions.json`     | Five open follow-on research questions: (1) stable Hh implementation, (2) Kou-Wang 2004 path-dependent replication, (3) empirical smile calibration vs Merton/Heston, (4) converged PIDE (CN + FFT + Richardson), (5) multi-asset extension. |
| `workflow.md`             | Step-by-step pipeline documentation from paper acquisition through LLM-judge scoring. |
| `failure_analysis.md`     | Detailed analysis of the Hh transcription failure and other residual gaps. |
| `evidence/results.json`   | Structured numerical outputs (JSON) of all runs. |
| `evidence/run.log`        | Full stdout capture of `run_replication.py`. |
| `evidence/llm_judge.txt`  | Verbatim output of Argo `claude-opus-4.7` judge. |

## Reproduce

```
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Kou-jump-diffusion-option-2004/work
python3 -m venv venv && . venv/bin/activate
pip install numpy scipy
python run_replication.py
```
Runtime: ≤ 30 s on a laptop CPU.
