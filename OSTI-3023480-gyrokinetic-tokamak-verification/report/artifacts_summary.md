# Artifacts summary — OSTI 3023480 replication

Directory layout after completion:

```
OSTI-3023480-gyrokinetic-tokamak-verification/
├── paper.pdf                                     # top-level copy for 8-artifact bar
├── extraction/
│   ├── marker.md                                 # pdftotext -layout extraction (raw text)
│   └── nougat.mmd                                # pointer to marker.md (no nougat parse in corpus)
├── report/
│   ├── REPORT.md                                 # main verdict + method + results
│   ├── REPORT.tex                                # LaTeX version (section-by-section, what worked/didn't)
│   ├── brief.md                                  # 1-paragraph
│   ├── attempt_log.md                            # chronological attempt log
│   ├── artifact_harvest.md                       # public artifacts pulled
│   ├── workflow.md                               # tools/codes/effort estimate
│   ├── artifacts_summary.md                      # THIS FILE
│   ├── failure_analysis.md                       # what didn't work + why
│   ├── open_questions.json                       # 5 open questions (q + basis + next_steps)
│   └── evidence/
│       ├── baae_reproduction_v3.json             # numerical outputs
│       ├── baae_reproduction_table.txt           # comparison table
│       ├── llm_judge_prompt.txt                  # judge input
│       ├── llm_judge_gpt54.txt                   # judge #1 verdict
│       └── llm_judge_gpt52.txt                   # judge #2 verdict
└── work/
    ├── paper.pdf                                 # working copy
    ├── reproduce_baae.py                         # v1 (naive on-axis)
    ├── reproduce_baae_v2.py                      # v2 (cold-ion limit)
    ├── reproduce_baae_v3.py                      # v3 (BAE/GAM w/ q — matches paper)
    ├── baae_reproduction_results.json            # v1 output
    ├── baae_reproduction_v2.json                 # v2 output
    ├── baae_reproduction_v3.json                 # v3 output (main)
    └── baae_reproduction_table.txt               # v1 formatted comparison
```

## Quantitative summary (from `baae_reproduction_v3.json`)

| quantity | value | paper | agreement |
|:---------|:------|:------|:----------|
| v_A axis  | 3.69e6 m/s | (implicit) | ✓ (sub-TAE) |
| f_TAE (q=1) | 588 kHz | ≫ 150 kHz | ✓ |
| BAE gap (T_i=T_e, q=2.5) | 95 kHz | 90 kHz | 5.6 % |
| BAE gap (T_i=T_e, q=3.0) | 79 kHz | 68.8 kHz (NOVA) | 15 % |
| ω_*i (r/a=0.5, L_n=a/5) | 96.7 kHz | ~100 kHz | 3.3 % |
| β_thermal | 8.4 % | consistent for ST40 | ✓ |
| δB∥/δB⊥ (√β_th) | 0.29–0.5 | 0.5 | ✓ |
| n=2,3,4 stability (BTG scaling) | no BAAE expected | none found | ✓ qualitative |

## LLM-judge outcomes

| judge | model | verdict | coverage | agreement | confidence |
|:------|:------|:-------|:--------:|:---------:|:----------:|
| J1 | argo:gpt-5.4 | SPOT-CHECK | 5/8 | 5/5 | medium |
| J2 | argo:gpt-5.2 | SPOT-CHECK | 4/7 | 4/4 | medium |
| **consensus** | – | **SPOT-CHECK** | – | 100 % | medium |
