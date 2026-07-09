# Artifact Harvest

| Artifact | Source | Notes |
|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3024991 | OA PDF, 3.45 MB, fetched via uicgpu proxy (CherryRd times out on OSTI). PDF v1.5. `/tmp/osti_3024991.pdf` on uicgpu. |
| Paper text | `pdftotext` of above | 3501 lines; all equations + problem parameters (Sec 2, 5.1, 5.2) extracted cleanly, no OCR needed. |
| HyPar (paper's FOM code) | https://github.com/debog/hypar (ref [3]) | The paper's actual FOM is HyPar (Ghosh). We did NOT run HyPar; we reimplemented the described scheme independently in numpy (stronger independent test). |
| DOI | 10.1016/j.cpc.2026.110039 | — |

## Public code note
The paper cites HyPar as the FOM engine but does not release the specific ROM/driver scripts as an archived Zenodo/DOI package in the OA PDF. Independent reimplementation was therefore the appropriate replication path (and validates the *method description*, not just the authors' binaries).

## Reimplementation code (this work)
- `work/vlasov_fom.py` — 1D1V Vlasov-Poisson FOM (WENO5 Jiang-Shu + Rusanov LF splitting, FFT Poisson, RK4).
- `work/run_replication.py` — prescribed-E POD reducibility + Landau (paper params) + analytic dispersion roots.
- `work/run_landau_k05.py`, `work/landau_signsweep.py` — canonical k=0.5 Landau validation + E-field sign diagnosis.
- `work/make_plots.py`, `work/judge.py` — figures + LLM-judge (Argo gpt-5.2, free).

## Evidence outputs (report/evidence/)
- `replication_results.json` — prescribed-E POD table + Landau(paper params) + analytic roots.
- `landau_signsweep.json` — sign-convention sweep proving γ=-0.1495 at correct sign.
- `landau_k05_result.json`, `run.log` — run logs.
- `landau_k0.5_decay.png` — FOM field-energy decay vs analytic envelope.
- `prescribed_pod_reducibility.png` — POD energy-missing-ratio vs n_f (repro of paper Fig. 3).
- `llm_judge.txt` — LLM-judge verdict.
