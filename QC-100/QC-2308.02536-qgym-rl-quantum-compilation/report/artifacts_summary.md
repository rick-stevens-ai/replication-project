# Artifacts Summary — QC-2308.02536 (qgym) Replication

**Paper:** arXiv 2308.02536v1 — van der Linde et al., *qgym: A Gym for Training and Benchmarking RL-Based Quantum Compilation* (IEEE QCE'23).
**Verdict:** REPLICATED
**Set:** QC-100

## Standard 8-artifact bundle

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | REPORT.md | `report/REPORT.md` | Primary human-readable report (Markdown), source of truth |
| 2 | REPORT.tex | `report/REPORT.tex` | LaTeX-typeset version of the report, with critique section and `\input{open_questions_section.tex}` at end |
| 3 | open_questions.json | `report/open_questions.json` | Machine-readable list of 5 open questions (bare JSON list of `{q, basis, next_steps}` objects) |
| 4 | open_questions_section.tex | `report/open_questions_section.tex` | LaTeX Open-Questions section, `\input`-ed by REPORT.tex |
| 5 | workflow.md | `report/workflow.md` | Chronological workflow: paper → extraction → env → H1 → H2/H3 → verdict |
| 6 | artifacts_summary.md | `report/artifacts_summary.md` | This file — index of all artifacts |
| 7 | failure_analysis.md | `report/failure_analysis.md` | Honest critique — reproducibility hole, PPO=ALAP not >, no independent qgym reimpl, no real-hardware baseline |
| 8 | nougat.mmd | `extraction/nougat.mmd` | Nougat Markdown-math extraction of the paper body |

## Evidence files (`report/evidence/`)

| File | What it holds | Supports |
|------|---------------|----------|
| `commutation_mechanism.json` | ALAP-vs-commutation schedule lengths (23 vs 13 cycles) + blocking matrices for both rulebooks on the Fig. 3A circuit | H1 (deterministic mechanism) |
| `scheduling_results.json`    | Primary PPO PoC: 10-decile mean episode length + reward curves, ALAP vs PPO completion fraction + mean cycles on 50-circuit held-out set | H2, H3 |
| `training_curves.png`        | Rendered plot of the 10-decile mean episode length + reward vs training progress; visually mirrors paper Fig. 4A/B | H2 |
| `results.json`, `routing_results.json` | Companion Routing-env run (PPO vs Qiskit SabreSwap/BasicSwap on 5-qubit path); PPO did not converge → non-completion artifact | transparency only — NOT used to support any claim |
| `judge_panel.json`, `judge3.txt` | Earlier 3-judge Argo verdicts against the pre-fix failing PPO config (all PARTIAL) | provenance |

## Code (`code/`)

| File | Purpose |
|------|---------|
| `reproduce.py` | H1 mechanism (deterministic) + earlier failing PPO PoC (`n_steps=1024`) |
| `run_scheduling.py` | Primary H2/H3 PPO PoC (SB3-default `n_steps=2048`, 10^5 steps, seed 20260703) |
| `run_experiment.py` | Companion Routing PPO vs Qiskit swap baselines |
| `plot_curves.py`    | Renders `training_curves.png` from `scheduling_results.json` |
| `judge_panel.py`    | Argo 3-judge panel driver (provenance run) |

## Reproduction commands

```bash
cd QC-2308.02536-qgym-rl-quantum-compilation
.venv/bin/python code/reproduce.py 0            # H1 mechanism (deterministic, seconds)
.venv/bin/python code/run_scheduling.py         # H2/H3 PPO PoC (~6 min, 1e5 steps)
.venv/bin/python code/plot_curves.py            # Fig 4-style training curves
```

## Notes
- All compute was on local macOS CPU in a Python 3.11.15 venv. No paid endpoints used.
- The authors' own `qgym 0.3.1` was pip-installed and used as-is. No independent reimplementation of `qgym` was performed (see `failure_analysis.md` #1).
- ALAP baseline is a greedy-legal-first policy running **inside** the same qgym `Scheduling` env on the same seeded random circuits as PPO — so both policies are compared on literally identical inputs.
