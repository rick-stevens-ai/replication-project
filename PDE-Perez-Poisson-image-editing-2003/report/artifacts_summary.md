# Artifacts Summary — Pérez et al. 2003 Poisson Image Editing replication

## Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary independent-replication report (Markdown). |
| `REPORT.tex` | LaTeX form of the report + dedicated Genuine Critique section. |
| `brief.md` | One-paragraph summary. |
| `attempt_log.md` | Chronological log. |
| `artifact_harvest.md` | Public artifacts / links. |
| `workflow.md` | Chronological, actually-executed steps. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Root-cause analysis of exploratory dead-ends. |
| `open_questions.json` | 5 genuinely-open follow-up questions. |

## Evidence bundle (`report/evidence/`)

### Images
| File | Content |
|---|---|
| `01_dest.png` … `08_mixed_text_on_stripes.png` | Raw scene + per-mode result images (disk-in-gradient and text-on-stripes scenes). |
| `figure_seamless_disk_comparison.png` | 5-panel: dest \| src \| naive \| seamless \| mixed for the disk scene. |
| `figure_mixed_text_comparison.png` | 5-panel: dest \| src \| naive \| seamless \| mixed for text-on-stripes. |

### Numeric evidence
| File | Content |
|---|---|
| `results.json` | Consolidated C1/C2/C3 numeric results (all experiments). |
| `c1_boundary_gradient_match.json` | **Primary C1 evidence.** Per-channel edited-jump vs. source-jump vs. naive-jump, mean absolute deviations, seam-reduction ratios. |
| `seam_index.json` | Exploratory C1 seam-index test — **superseded** by `c1_boundary_gradient_match.json`. |
| `boundary_verification.json` | Exploratory C1 boundary test — **superseded** by `c1_boundary_gradient_match.json`. |

### LLM-judge evidence
| File | Content |
|---|---|
| `llm_judge_prompt.txt` | Exact prompt (evidence + rubric) sent to all three referees. |
| `llm_judge_response_argo_gpt-4.1.json` | gpt-4.1 verdict JSON — REPLICATED. |
| `llm_judge_response_argo_gemini-2.5-pro.json` | gemini-2.5-pro verdict JSON — REPLICATED. |
| `llm_judge_response_argo_claude-sonnet-4.6.json` | claude-sonnet-4.6 verdict JSON — REPLICATED. |

## Code artifacts (`work/`)

| File | Purpose |
|---|---|
| `poisson_paper.pdf` | The paper (SHA-256 prefix `2f62b451`). |
| `poisson_editing.py` | Core Poisson solver: `solve_poisson_region(dest, src, mask, mode)` with modes `seamless`/`mixed`/`membrane`; RGB wrapper `solve_poisson_rgb(...)`. |
| `run_experiments.py` | Main driver: generates the two synthetic scenes, runs all three modes, emits C1/C2/C3 evidence. |
| `verify_c1_correct.py` | **Primary C1 test.** Boundary-edge gradient audit. |
| `verify_c1_final.py` | Exploratory C1 test (see failure_analysis.md). |
| `verify_boundary_v2.py` | Exploratory C1 test (see failure_analysis.md). |
| `make_comparison_figure.py` | Emits 5-panel comparison figures. |
| `llm_judge.py` | LLM-judge scoring driver (3 Argo models, JSON out). |
| `run.log` | Captured stdout of `run_experiments.py`. |

## Reproduction commands (from `work/`)
```
python3 run_experiments.py
python3 verify_c1_correct.py
python3 make_comparison_figure.py
python3 llm_judge.py
```

## Numeric headlines
- **C1** (mean absolute boundary-gradient deviation from source's own gradient): edited ≈ 2 units on 0–255; naive-paste 20–94 units → seam reduction **8.5×–43.9×** per channel.
- **C2** (max |Δf| in membrane solve, strict interior of Ω): `3.4–4.3 × 10⁻¹³` = machine epsilon.
- **C3** (Σ|∇f| inside Ω, text-on-stripes): dest 2,539,186; src 911,400; seamless 1,210,641; **mixed 3,408,319** (mixed preserves both).
- Timing: 0.063 s (disk seamless, |Ω|=5,013) → 0.387 s (text-stripes seamless/mixed, |Ω|=30,800) on 2020s CPU with direct sparse LU; same order of magnitude as paper's 0.4 s / 60k-pixel disk on Pentium 4.

## LLM-judge convergence
Three independent Argo referees, same rubric and evidence bundle, all
returned `"overall_verdict": "REPLICATED"`. Judges are confirmatory
(they saw the same evidence); the primary evidence remains the numeric
tables above.

## Verdict
**REPLICATED** across C1 (seamless boundary match), C2 (membrane
Laplace correctness), C3 (mixed-gradient structure preservation).
C4 (further downstream editing effects) not tested — out of scope for
a minimal reproduction.
