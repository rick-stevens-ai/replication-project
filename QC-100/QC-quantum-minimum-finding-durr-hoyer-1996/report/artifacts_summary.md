# Artifacts summary

## Inventory

### Top-level
| Path | Size (B) | SHA-256 | Provenance |
|------|---------|--------|-----------|
| paper.pdf | 77176 | ff5c2ff71415e22f0ddf799b31e9b82d1990db9c1fc9d62ea2aabea5907e06cf | https://arxiv.org/pdf/quant-ph/9607014 |

### Extraction
| Path | Size (B) | SHA-256 | Provenance |
|------|---------|--------|-----------|
| extraction/marker.md | 13488 | 7893a81c98090bafe91bb72bb19e14aa950f456ce728be6c4835706c800e446d | copied from sibling QC-200 (pdftotext -layout fallback; Marker binary N/A) |
| extraction/nougat.mmd | 7209 | db639da18b407d23c83f4a77f1f1ef7f0f219fa6f45a646411717322bcf2eb87 | copied from sibling QC-200 (nougat run) |

### Code (all in `work/`)
| File | Purpose | ~LOC |
|------|---------|-----|
| durr_hoyer_independent.py | Main: Grover + BBHT + DH outer loop + experiment driver | 250 |
| grover_sanity.py | Grover core cross-check vs closed form | 60 |
| bbht_t_sweep.py | BBHT scaling measurement | 60 |
| classical_baseline.py | Classical linear-scan baseline | 45 |
| llm_judge.py | Argo LLM-judge harness with model fallbacks | 130 |

### Evidence (all in `report/evidence/`)
| File | Content |
|------|---------|
| results.json | Main experiment: N ∈ {4,8,16,32,64}, 300 trials/size, per-trial iters/correct/updates |
| grover_sanity.json | 12 (N,k) cells, empirical vs closed-form single-Grover success prob |
| bbht_t_sweep.json | 21 (N,t) cells, mean/median/std BBHT iters, ratio vs √(N/t) |
| classical_baseline.json | 8 N sizes, mean/min/max classical probes |
| llm_judge.json | Raw judge response + parsed JSON verdict; judge_model recorded |
| smoke.json | Initial 50-trial smoke test |

### Report
| File | Content |
|------|---------|
| REPORT.md | Full Markdown report (7.8 KB) |
| REPORT.tex | Detailed LaTeX report (10.6 KB) |
| brief.md | 1-paragraph summary |
| attempt_log.md | Chronological attempt log |
| artifact_harvest.md | Table of public artifacts pulled |
| open_questions.json | 5 heavy-duty open questions with q, basis, next_steps |
| workflow.md | Workflow, tools, effort estimate |
| artifacts_summary.md | **This file** |
| failure_analysis.md | Honest failure / gap analysis |

## Traces

- **Run log for main experiment:** captured in `attempt_log.md`
  (`success_prob=1.000 mean_iters_to_first_hit=…` per N).
- **Judge attempt trace:** `llm_judge.py` stderr recorded 502s across
  Claude Opus 4.7/4.8 and `[judge] model=argo:gpt-5.2 ok`; the accepted model
  is stored in `llm_judge.json` under `judge_model`.
- **Reproducibility:** all seeds are hard-coded in scripts
  (`--seed 20260706` main, `seed=0` grover_sanity, `seed=42` bbht_t_sweep,
  `Random(0)` classical). Re-run any script from the target dir to reproduce.

## Verdict

**PARTIAL** — accepted from LLM-judge `argo:gpt-5.2`, second pass.
Per-claim: C1 PARTIAL, C2 REPRODUCED, C3 REPRODUCED, C4 REPRODUCED.
