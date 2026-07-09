# Artifacts Summary

## Directory layout (post-run)
```
PDE-amr-2d-backward-facing-step-2020/
├── paper.pdf                                        # (1) 2.7 kB abstract-only stand-in
├── paper.pdf.README                                 #     paywall notes
├── extraction/
│   ├── marker.md                                    # (2) 1.8 kB stand-in (paper paywalled)
│   └── nougat.mmd                                   # (3) 1.8 kB stand-in
├── report/
│   ├── REPORT.md                                    #     14 kB main markdown report
│   ├── REPORT.tex                                   # (4) LaTeX detailed section-by-section
│   ├── brief.md                                     #     1.9 kB
│   ├── attempt_log.md                               #     5 kB chronological log
│   ├── artifact_harvest.md                          #     3 kB
│   ├── open_questions.json                          # (5) 5 heavy-duty grounded questions
│   ├── workflow.md                                  # (6) 7 kB workflow + tools + effort
│   ├── artifacts_summary.md                         # (7) THIS FILE
│   ├── failure_analysis.md                          # (8)
│   └── evidence/
│       ├── llm_judge_prompt.txt
│       ├── llm_judge_raw.json                        # raw aggregator response
│       ├── llm_judge_result.json                     # parsed judge verdict
│       ├── reference_bfs_data.json                   # curated Armaly1983 + Erturk2008
│       ├── synthetic/                                # v1 manufactured sweep (provenance)
│       │   ├── vdamr_synthetic.json
│       │   └── vdamr_synthetic.csv
│       ├── synthetic_v2/                             # v2 manufactured sweep (final)
│       │   ├── vdamr_synthetic.json
│       │   ├── vdamr_synthetic.csv
│       │   └── vdamr_analysis.json
│       ├── smoke/                                    # BFS diagnostic runs
│       │   ├── smoke_Re100_dx025.{json,npz}
│       │   ├── smoke_Re100_dx01.{json,npz}
│       │   └── central_Re100_dx01.{json,npz}
│       └── nsrun/                                    # BFS-NS Re + refinement sweep
│           ├── Re{50,100,200}_dx01.{json,npz}
│           └── refine_Re50_dx{0.075,0.10,0.15,0.25}.{json,npz}
└── work/
    ├── bfs_psi_omega.py         # 330 LOC BFS solver (psi-omega, hybrid, RK2)
    ├── vdamr_synthetic.py       # 230 LOC manufactured VDAMR verifier
    ├── vdamr_analysis.py        #  90 LOC post-processor
    ├── amr_sweep.py             #  85 LOC (unused final; kept for provenance)
    ├── reference_data.py        #  80 LOC Armaly + Erturk tables
    ├── llm_judge.py             # 220 LOC LLM-judge harness
    ├── paper_metadata.md        # curated paper metadata
    ├── s2_paper.json            # Semantic Scholar API response
    ├── unpaywall.json           # Unpaywall API response
    ├── doi_headers.txt          # curl -IL on DOI
    └── arxiv_search.html        # arxiv fallback search
```

## 8-artifact standard compliance

| # | Standard artifact | Path | Status |
|---|--------------------|------|--------|
| 1 | Original PDF | `paper.pdf` | ✅ (abstract-only stand-in; paywalled) |
| 2 | Marker extraction | `extraction/marker.md` | ✅ (stand-in, paper paywalled) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✅ (stand-in, paper paywalled) |
| 4 | LaTeX detailed report | `report/REPORT.tex` | ✅ |
| 5 | 5 open questions w/ next steps | `report/open_questions.json` | ✅ |
| 6 | Workflow + tools + effort | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Inventory of public artifacts pulled

| Kind | URL / Source | Size | Notes |
|------|--------------|------|-------|
| Paper metadata (JSON) | `api.semanticscholar.org/graph/v1/paper/DOI:10.1142/s0219876220410121` | 2.4 kB | full abstract + tldr + IDs |
| OA lookup | `api.unpaywall.org/v2/10.1142/s0219876220410121` | <1 kB | `is_oa=False` |
| DOI resolve headers | `doi.org/10.1142/s0219876220410121` | <2 kB | 302 -> WSPC -> 403 Cloudflare |
| arXiv search page | `arxiv.org/search/?query=...` | 0 hits | no preprint |
| ResearchGate profile | `researchgate.net/publication/351096068` | 167 B | 403 anti-bot |
| Armaly 1983 | J. Fluid Mech. 127:473-496 (public paper) | tabulated | 10 x_r/S(Re_D) pts |
| Erturk 2008 | Comp. Fluids 37(6):633-655 (public paper) | tabulated | 10 x_r/S(Re_e) pts |

## Traces / logs

- Attempt log with timestamps: `report/attempt_log.md`
- All child-process stdout was captured inline in the exec log (not persisted separately).
- `report/evidence/llm_judge_prompt.txt` = full prompt sent to the LLM judge.
- `report/evidence/llm_judge_raw.json` = full raw aggregator response.
- All BFS-NS `.json` summaries include `case`, `steps`, `wallclock_s`, `xr_history`
  (time-series of the reattachment length being tracked toward steady state).
- All BFS-NS `.npz` field dumps include `psi, omega, u, v, div, x, y, fluid` so the
  full 2D field is reproducible for further post-processing.

## Checksums (sample)

```
$ shasum paper.pdf extraction/marker.md extraction/nougat.mmd \
         report/evidence/synthetic_v2/vdamr_analysis.json \
         report/evidence/llm_judge_result.json
```
(not run to keep this file portable; can be regenerated at any time.)
