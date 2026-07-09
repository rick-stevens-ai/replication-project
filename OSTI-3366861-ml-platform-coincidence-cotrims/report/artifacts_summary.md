# Artifacts Summary — OSTI 3366861

## Local artifacts (this replication directory)

```
OSTI-3366861-ml-platform-coincidence-cotrims/
├── paper.pdf                          2.8 MB   original OSTI PDF
├── extraction/
│   ├── marker.md                      pdftotext-extracted paper text (900 lines)
│   └── nougat.mmd                     same (marker/nougat not available at runtime)
├── work/
│   ├── paper.txt                      pdftotext layout output
│   ├── paper.pdf                      copy of paper
│   ├── replicate.py                   v1 replication script
│   ├── replicate_v2.py                v2 with eps sweep + coarse-5 config (primary)
│   └── llm_judge.py                   Argo-based verdict script
└── report/
    ├── brief.md                       1-paragraph what/why
    ├── REPORT.md                      full report (claims, method, results, verdict)
    ├── REPORT.tex                     LaTeX version of the report
    ├── open_questions.json            5 new open research questions
    ├── workflow.md                    end-to-end workflow diagram
    ├── artifacts_summary.md           this file
    ├── attempt_log.md                 chronological log
    ├── failure_analysis.md            what failed / gaps / cautions
    └── evidence/
        ├── replicate_v1.json          v1 raw output
        ├── replicate_v2.json          v2 raw output (all metrics + eps sweep)
        ├── ari_vs_state.txt           ARI(cluster, true state) = 0.617
        └── llm_judge.json             LLM-judge full request/response
```

## External artifacts pulled

| # | Artifact | URL | Size | SHA256 (first 12) |
|---|---|---|---|---|
| 1 | OSTI paper PDF | https://www.osti.gov/servlets/purl/3366861 | 2 781 106 B | pending |
| 2 | SCULPT source (git repo) | https://github.com/AMOS-experiment/CoInML.git | ~1 MB | commit head @ 2026-07-05 |
| 3 | D₂O sample dataset (zip) | https://zenodo.org/api/records/18478576/files/D2O_dataset.zip/content | 56 502 479 B | pending |
| 4 | Zenodo metadata JSON | https://zenodo.org/api/records/18478576 | ~10 KB | — |

## Software versions used

| Package | Version |
|---|---|
| Python | 3.8 (uicgpu venv) |
| numpy | 1.24.4 |
| pandas | 2.0.3 |
| scikit-learn | 1.3.2 |
| umap-learn | 0.5.7 |
| scipy | 1.10.1 |

## LLM endpoint

* Argo proxy on cherryrd, `http://127.0.0.1:44497/v1/chat/completions`, model `argo:gpt-5.2` (fell back from `argo:claude-opus-4.8` which returned 502 during the run window). Free endpoint. `argo:claude-opus-4.8` was the first choice per Rick's standing free-endpoint default but a transient 502 caused the fall-back.
