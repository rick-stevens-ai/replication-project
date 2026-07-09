# Artifacts Summary — Brouste 2014 YUIMA Replication

**Root:** `~/Dropbox/REPLICATE-PROJECT/PDE-Brouste-YUIMA-stochastic-diff-2014/`

---

## Top-level layout

```
PDE-Brouste-YUIMA-stochastic-diff-2014/
├── work/                      # inputs + replication scripts
│   ├── yuima_paper.pdf        # 968,384 bytes — JSS v57i04, Diamond OA
│   ├── yuima_paper.txt        # pdftotext extract, 3343 lines
│   ├── repl_C1_qmle.R         # §6.2 / §6.3.2 QMLE at n=750, 500
│   ├── repl_C2_asymp_expansion.R  # §5 asymptotic expansion of European put on CIR
│   └── repl_C3_changepoint.R  # §6.5 2-D volatility change-point (full + no-drift + two-stage)
├── extraction/                # (empty aside from any auxiliary marker output)
└── report/
    ├── REPORT.md              # primary human-readable report (source of truth)
    ├── REPORT.tex             # LaTeX build of REPORT.md + explicit GENUINE CRITIQUE section
    ├── open_questions.json    # 5 truly-open questions grounded in the paper's SDE/QV/LAN scope
    ├── workflow.md            # numbered end-to-end procedure
    ├── artifacts_summary.md   # this file
    ├── failure_analysis.md    # partial-failure and modern-guard-rail analysis
    ├── attempt_log.md         # environment build recipe (Makevars, etc.)
    └── evidence/
        ├── C1_qmle.log        # captured Rscript stdout/stderr for §6.2/§6.3.2
        ├── C2_asymp.log       # captured Rscript stdout/stderr for §5
        ├── C3_cpoint.log      # captured Rscript stdout/stderr for §6.5
        ├── C1_coefs.csv       # coefficient table (theta, SE) for C1 / C1b
        ├── C1_results.rds     # small R result object for C1 / C1b
        ├── C2_results.rds     # ae.value0/1/2 + our MC estimate
        ├── C3_results.rds     # tau estimates + qmleL/qmleR params
        └── llm_judge_verdict.json  # {verdict, coverage_fraction, agreement_fraction, justification}
```

---

## Artifact-by-artifact inventory

### Inputs

| Artifact | Kind | Source | Notes |
|---|---|---|---|
| `work/yuima_paper.pdf` | PDF | `curl` from `https://www.jstatsoft.org/index.php/jss/article/view/v057i04/v57i04.pdf` | 968,384 bytes; Diamond OA (JSS); no checksum required. |
| `work/yuima_paper.txt` | Text | `pdftotext work/yuima_paper.pdf` | 3343 lines; used only for grepping seed-locked examples. |

### Replication scripts

| Artifact | Covers | Behaviour | Notes |
|---|---|---|---|
| `work/repl_C1_qmle.R` | C1 (§6.2, n=750), C1b (§6.3.2, n=500) | Literally re-types paper code, `set.seed(123)`, `qmle` on `dX = (2 - theta2*X) dt + (1 + X^2)^theta1 dW`. | Emits theta1_hat, SE(theta1), theta2_hat, SE(theta2), −2 log L to stdout and to CSV. |
| `work/repl_C2_asymp_expansion.R` | C2 (§5) | Sets up CIR + European put, calls `setFunctional` + `asymptotic_term` for order 0/1/2, plus a 2×10⁵-path MC sanity check. | Deterministic call — expected to (and does) match to 7 sig figs. MC undersized vs paper's 10⁶. |
| `work/repl_C3_changepoint.R` | C3a (§6.5 full & no-drift), C3b (two-stage) | 2-D SDE volatility change-point at τ=4 on T=10, n=1000, seed 123; runs `CPoint`, `qmleL(t=2)`, `qmleR(t=8)`, iterated refinement. | Had to raise `qmleR` `lower` from (0,0) to (0.01,0.01) — see `failure_analysis.md`. |

### Evidence (captured outputs)

| Artifact | Type | Content |
|---|---|---|
| `report/evidence/C1_qmle.log` | text | Full Rscript stdout+stderr for `repl_C1_qmle.R`. Contains the printed θ̂₁, θ̂₂, SEs, and −2 log L for both n=750 and n=500. |
| `report/evidence/C2_asymp.log` | text | Full Rscript stdout+stderr for `repl_C2_asymp_expansion.R`. Contains `ae.value0/1/2` and our MC estimate `0.5566293`. |
| `report/evidence/C3_cpoint.log` | text | Full Rscript stdout+stderr for `repl_C3_changepoint.R`. Contains `t.est$tau=3.98`, `t.est2$tau=3.98`, `qmleL` params `(0.4723068, 0.2899005)`, `qmleR` params `(0.1944069, 0.4261460)`, `t.est3$tau=3.98`, `t2s.est3$tau=3.98`. |
| `report/evidence/C1_coefs.csv` | CSV | Coefficient table for C1 / C1b (paper vs this rep). |
| `report/evidence/C1_results.rds` | binary R | Small R list with the `qmle` fit objects for C1/C1b. |
| `report/evidence/C2_results.rds` | binary R | `ae.value0/1/2` + MC estimate + MC s.e. |
| `report/evidence/C3_results.rds` | binary R | `t.est`, `t.est2`, `qmleL`, `qmleR`, `t.est3`, `t2s.est3`. |
| `report/evidence/llm_judge_verdict.json` | JSON | LLM adjudicator's verdict block (see below). |

### Reports

| Artifact | Role |
|---|---|
| `report/REPORT.md` | Primary human-readable report. Source of truth for the verdict; all downstream files (REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md) derive from it. |
| `report/REPORT.tex` | LaTeX build with an explicit `Genuine critique` section listing 8 honest limits on the replication (partial coverage, uncontrolled version drift, undersized MC baseline, single-BLAS determinism, LLM-judge is not truly independent, endpoint fallback, etc.). |
| `report/open_questions.json` | Five truly-open questions grounded in Brouste 2014's YUIMA SDE / quadratic-variation / LAN scope: qmleR optimum existence, decomposition of the C1 sub-percent drift, LAN-SE finite-sample coverage on the (1+X²)^θ₁ diffusion, reproducibility of the 10⁶-MC baseline in C2, and closing coverage on C4 (LASSO) + C5 (adaBayes). |
| `report/workflow.md` | End-to-end numbered procedure (Stages 0–8). |
| `report/failure_analysis.md` | Deep dive on the single partial failure (C3b right-hand qmleR local optimum) plus coverage gaps. |
| `report/attempt_log.md` | Environment-build recipe (Makevars pointing clang at MacOSX 26 SDK C++ headers, gettext + gcc-16 libs). |

---

## Key numbers (single source of truth: REPORT.md §4)

| Claim | Paper value(s) | This rep | Match quality |
|---|---|---|---|
| C1 θ̂₁ (n=750)    | 0.1969182       | 0.1972715       | 3–4 sig figs; Δ +0.18 % (≪ SE) |
| C1 θ̂₂ (n=750)    | 0.2998350       | 0.2997625       | 4 sig figs; Δ −0.02 % |
| C1 −2 log L      | −282.8676       | −282.8615       | 5 sig figs |
| C1b θ̂₁ (n=500)   | 0.1947225       | 0.1944403       | 3–4 sig figs; Δ −0.15 % |
| C2 ae.value0/1/2 | 0.7219652 / 0.5787545 / 0.5617722 | identical | **7 sig figs exact** |
| C3a τ̂ full       | 3.98            | 3.98            | Exact (grid 0.01) |
| C3a τ̂ no-drift   | 3.98            | 3.98            | Exact |
| C3b qmleL params | (0.4723067, 0.2899005) | (0.4723068, 0.2899005) | **7 sig figs exact** |
| C3b qmleR params | (0.2515379, 0.5518635) | (0.1944069, 0.4261460) | **Different local optimum** (see failure_analysis.md) |
| C3b τ̂ (one-shot) | 3.99            | 3.98            | 0.01 grid drift |
| C3b τ̂ (iter)     | 3.98            | 3.98            | Exact |

---

## LLM judge verdict (excerpt)

`report/evidence/llm_judge_verdict.json` — produced by `argo:gpt-4.1` (free Argo endpoint fallback after `argo:claude-opus-4.7` upstream 502):

```json
{
  "verdict": "REPLICATED",
  "coverage_fraction": 0.67,
  "agreement_fraction": 1.0,
  "justification": "All tested, seed-locked numerical claims (C1, C1b, C2, C3a, and the left-hand portion of C3b) reproduced the paper's results to high precision, either exactly or well within the reported standard errors. The only minor deviation (C3b right-half MLE) was due to updated package guard rails, not a substantive disagreement. Two testable claims (C4, C5) were not attempted, so coverage is partial but all tested claims agree."
}
```

---

## Wave-level emission

At the end of REPORT.md:

```
WAVE_RESULT set=PDE paper=Brouste-YUIMA-2014 verdict=REPLICATED
  dir=~/Dropbox/REPLICATE-PROJECT/PDE-Brouste-YUIMA-stochastic-diff-2014
  one_line=yuima 1.15.34 reproduces paper's QMLE (3-4 sig figs, within SE),
           asymptotic-expansion (7 sig figs exact), and 2-D volatility
           change-point (tau=3.98 exact) on seed 123
```
