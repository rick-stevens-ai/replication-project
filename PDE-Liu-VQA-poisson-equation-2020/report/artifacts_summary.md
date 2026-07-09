# Artifacts Summary — Liu 2020 VQA-Poisson Replication

## Directory Tree
```
PDE-Liu-VQA-poisson-equation-2020/
├── report/
│   ├── REPORT.md               (12 KB — markdown source of truth)
│   ├── REPORT.tex              (LaTeX version of REPORT.md, with critique section)
│   ├── open_questions.json     (5 open scientific questions grounded in this paper)
│   ├── workflow.md             (end-to-end pipeline documentation)
│   ├── artifacts_summary.md    (this file)
│   ├── failure_analysis.md     (m=6 sweep truncation + other limits)
│   ├── brief.md                (1-paragraph summary)
│   ├── attempt_log.md          (chronological log)
│   ├── artifact_harvest.md     (public artifacts pulled)
│   └── evidence/
│       ├── results.json        (full C1/C2/C3 numeric evidence)
│       ├── llm_judge.json      (Argo gpt-5.2 verdict, raw + parsed)
│       └── main_run.log        (local main-sweep console log)
└── work/
    ├── venv/                   (python 3.14 + numpy 2.5.0 + scipy 1.18.0)
    ├── liu_vqa.py              (main implementation, 14 KB, MIT)
    ├── liu_vqa_parallel.py     (uicgpu one-shot wrapper for a single (m,p))
    ├── finalize.py             (merges local+uicgpu results into results.json)
    ├── llm_judge.py            (Argo LLM-judge caller)
    ├── liu_vqa_poisson.pdf     (paper arXiv PDF, 720 KB, 6 pages + refs + Appendix A)
    └── vqa_m56_results.jsonl   (uicgpu parallel sweep results, one JSON per (m,p))
```

## Primary Artifacts

### Paper Source
- **`work/liu_vqa_poisson.pdf`** — 720 KB, 6 pages plus references and
  Appendix A. Fetched from `https://arxiv.org/pdf/2012.07014.pdf`.
  Preprint arXiv:2012.07014v1 (13 Dec 2020); published Phys. Rev. A **104**,
  022418 (Aug 2021); DOI `10.1103/PhysRevA.104.022418`; 108 citations per
  replication brief.

### Implementation
- **`work/liu_vqa.py`** — 14 KB, MIT-licensed, python 3.
  All decomposition functions, the ansatz, the cost function, the VQA driver,
  and the layer-search routine. Re-derived entirely from paper equations
  (Eqs. 11–18); no paper-provided reference code was used.
- **`work/liu_vqa_parallel.py`** — one-shot wrapper: takes `(m, p, n_restarts)`
  on the command line, prints a single JSON line to stdout, used by
  GNU parallel on uicgpu.
- **`work/finalize.py`** — merges local `main_run.log` output with
  `vqa_m56_results.jsonl` into unified `report/evidence/results.json`.
- **`work/llm_judge.py`** — calls `argo:gpt-5.2` via the Argo proxy
  (`http://127.0.0.1:44497/v1/chat/completions`, key `stevens`, FREE endpoint)
  with `results.json` and the console log as context; requests structured
  JSON verdict per claim.

### Evidence
- **`report/evidence/results.json`** — canonical numeric evidence:
  - `C1_A_decomposition`: m=1..6, item counts (all = 2m+1),
    reconstruction errors (all = 0.0e+00).
  - `C2_Asq_decomposition_pure`: m=1..6, pure item counts (all = 4m+1),
    nested/compound counts, reconstruction errors (all = 0.0e+00).
  - `C3_VQA_sweep_local`: m=2..4, per-`p` best fidelity, per-`p` min-fidelity,
    optimizer wall time.
  - `C3_VQA_sweep_uicgpu`: m=5..6, per-`p` best fidelity (m=5 complete
    p=1..8, m=6 partial p=1..2).
- **`report/evidence/llm_judge.json`** — raw Argo response and parsed JSON.
  Fields: `per_claim` (with verdict + confidence for C1, C2, C3),
  `overall` (verdict + confidence).
- **`report/evidence/main_run.log`** — full console output of the local
  m=2..4 sweep, including per-restart optimizer traces.

### Text Outputs
- **`report/REPORT.md`** — 12 KB markdown; the source of truth.
- **`report/REPORT.tex`** — LaTeX re-render with a dedicated Genuine
  Critique section (§8, 9 numbered concerns).
- **`report/open_questions.json`** — 5 open scientific questions
  grounded in this specific paper (barren-plateau susceptibility at
  larger m, variable-coefficient / higher-dim Poisson extension,
  comparison vs. HHL and other quantum linear solvers, Pauli-basis
  vs. `{I, σ+, σ-}`-basis measurement compilation, NISQ noise
  resilience).
- **`report/workflow.md`** — end-to-end pipeline documentation with
  data flow diagram, reproduction recipe, compute budget table.
- **`report/failure_analysis.md`** — root-cause analysis for the
  m=6 sweep truncation, environment-drift risks, and untested claims
  (C4, C5).

## Numeric Highlights

### C1 — `A_m` decomposition (paper: 2m+1 items)
All 6 tested m values (1..6) match exactly with reconstruction error 0.0e+00.

### C2 — `A_m²` decomposition (paper: 4m+1 pure items)
All 6 tested m values (1..6) match exactly with reconstruction error 0.0e+00.

### C3 — VQA fidelity ≥ 0.99
| m | Our p_min | Our best fidelity |
|---|:---:|:---:|
| 2 | 1 | 0.9955 |
| 3 | 2 | 0.9958 |
| 4 | 3 | 0.9955 |
| 5 | 3 | 0.9917 |
| 6 | not reached | 0.9692 (at p=2) |

## Verdict Chain
- Analytic reconstruction (C1, C2): **REPLICATED**, 6/6 for each.
- Numerical VQA sweep (C3): **PARTIAL** — m=2..5 replicated, m=6 not run
  to threshold.
- LLM-judge (`argo:gpt-5.2`, non-regex, FREE endpoint): **PARTIAL**,
  confidence 90.
- Overall this replication: **PARTIAL**.

## Compute Provenance
- **Local:** CherryRd (macOS, arm64), python 3.14, numpy 2.5.0, scipy 1.18.0.
- **Remote:** uicgpu (Ubuntu, 8×A100), python 3.10, numpy 1.23.5, scipy 1.10.1.
- **LLM-judge:** Argo proxy `http://127.0.0.1:44497/v1/chat/completions`,
  model `argo:gpt-5.2`, FREE endpoint per standing rules.

## Licensing
- Paper PDF: authors' copyright / Phys. Rev. A + arXiv redistribution.
- All replication code (`liu_vqa.py`, `liu_vqa_parallel.py`, `finalize.py`,
  `llm_judge.py`) authored for this replication, released MIT.
