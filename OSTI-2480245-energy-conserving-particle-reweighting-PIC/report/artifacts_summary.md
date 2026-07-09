# Artifacts Summary — OSTI 2480245

## Directory layout

```
OSTI-2480245-energy-conserving-particle-reweighting-PIC/
├── report/
│   ├── REPORT.md                       # primary replication report (native, 2026-07-01)
│   ├── REPORT.tex                      # LaTeX equivalent (backfill 2026-07-06)
│   ├── open_questions.json             # 5 bare-list open questions
│   ├── open_questions_section.tex      # LaTeX section (\input'd by REPORT.tex)
│   ├── workflow.md                     # step-by-step methodology
│   ├── artifacts_summary.md            # this file
│   ├── failure_analysis.md             # honest critique of gaps
│   ├── brief.md                        # original task brief
│   ├── attempt_log.md                  # per-attempt log
│   ├── artifact_harvest.md             # provenance / artifact search
│   └── evidence/
│       ├── conservation_results.json   # all seven conservation invariants
│       ├── growth_independence.json    # Test-4.2 abstracted β(N_c)
│       ├── growth_stochastic.json      # C7 isolation attempt
│       ├── judge_prompt.txt            # LLM-judge input
│       └── llm_judge_verdict.json      # LLM-judge output
├── work/
│   ├── paper.pdf                       # OSTI 2480245 primary paper
│   ├── paper.txt                       # pdftotext extraction
│   ├── reweight.py                     # operator reimplementation
│   ├── test_conservation.py            # 20k splits / 18.6k merges
│   ├── test_growth_independence.py     # 0D swarm scaling
│   ├── test_growth_stochastic.py       # Poisson-noise probe
│   ├── judge_prompt.txt                # LLM-judge input
│   ├── requirements.txt                # numpy 2.5.0, scipy 1.18.0
│   └── SETUP.txt                       # venv setup notes
└── extraction/
    └── nougat.mmd                      # placeholder (no real Nougat parse done)
```

## Artifact inventory (this backfill brings dir to standard)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Primary report (Markdown) | `report/REPORT.md` | pre-existing |
| 2 | Primary report (LaTeX) | `report/REPORT.tex` | **backfilled** |
| 3 | Open questions (JSON list) | `report/open_questions.json` | **backfilled** |
| 4 | Open questions (LaTeX) | `report/open_questions_section.tex` | **backfilled** |
| 5 | Workflow doc | `report/workflow.md` | **backfilled** |
| 6 | Artifacts summary | `report/artifacts_summary.md` | **backfilled** |
| 7 | Failure analysis | `report/failure_analysis.md` | **backfilled** |
| 8 | Extraction stub | `extraction/nougat.mmd` | **backfilled (placeholder)** |

## Evidence files (quantitative results)

- **`evidence/conservation_results.json`** — measured relative errors for every operator invariant (mass, COM, energy for splits; mass, momentum, ΔKE ≥ 0 sign check, ΔKE magnitude for merges). All at machine precision except ΔKE magnitude (median 0.062 %, 95th pct 0.587 %).
- **`evidence/growth_independence.json`** — fitted β = 3.0507 s⁻¹ for every N_c ∈ {10, 100, 1000, 10000}; relative spread ~1e-15; computational count bounded in [N_c, 1.11 N_c].
- **`evidence/growth_stochastic.json`** — attempt at C7 isolation; abstracted model recovers β to machine precision at all N_c → C7 not isolable without Aleph's DSMC noise.
- **`evidence/llm_judge_verdict.json`** — Argo gpt-5.2 verdict: coverage 0.78, agreement 0.80, PARTIAL.

## Reproduction bundle

Everything needed to reproduce the operator-level replication is in `work/`. The paper PDF (`work/paper.pdf`) is the source-of-truth; `work/reweight.py` is a single-file dependency-light reimplementation. No Aleph, no GPU, no CI required.
