# Artifacts Summary — Sato 2021 VQA-Poisson Replication

All files live under `~/Dropbox/REPLICATE-PROJECT/PDE-Sato-VQA-poisson-2021/`.

## Source (paper + reference code)

| Path | Origin | License | Notes |
|---|---|---|---|
| `work/sato_2021.pdf` | `curl https://arxiv.org/pdf/2106.09333` | arXiv preprint | 785,930 B. Master reference for equation numbers. |
| `work/sato_2021.txt` | `pdftotext -layout work/sato_2021.pdf` | derived | Plain-text extraction used for search. |
| `work/VQAPoisson/` | `git clone https://github.com/ToyotaCRDL/VQAPoisson` | Apache-2.0 | Authors' reference implementation. Cloned for cross-check; **not executed** (Qiskit 0.23 + retired qiskit-aqua). |

## Replication code

| Path | Description |
|---|---|
| `work/vqa_poisson_replicate.py` | Independent NumPy statevector reimplementation. Ansatz (Ry^n + CNOT ladder)^L Ry^n with L=5; cost per Eq. (14); norm per Eq. (48); metrics per Eq. (46). Written from scratch against the paper's equations. |
| `work/.venv/` | Python virtualenv (numpy + scipy only). Not versioned. |

## Report

| Path | Description |
|---|---|
| `report/REPORT.md` | Full replication report. Verdict: **REPLICATED**. Contains claims table, method, results-vs-paper tables, verdict rationale, file index. |
| `report/REPORT.tex` | LaTeX version of REPORT.md with dedicated Genuine Critique section (this backfill). |
| `report/brief.md` | One-paragraph summary of the replication. |
| `report/attempt_log.md` | Chronological log of the replication attempt. |
| `report/artifact_harvest.md` | Log of every public artifact pulled (paper PDF, reference repo, etc.). |
| `report/workflow.md` | Reproduction protocol (this backfill). |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Honest inventory of the parts that did NOT succeed or were skipped (this backfill). |
| `report/open_questions.json` | Five open research questions grounded in the replication (this backfill). |

## Evidence (numerical outputs)

| Path | Contents | Size / count |
|---|---|---|
| `report/evidence/results_dirichlet.json` | Full per-trial records for Dirichlet BC. Fields per trial: `n`, `seed`, `eps_tr`, `norm_q`, `norm_c`, `rel_L2`, `iters`, `nfev`, `converged`. | 40 trials (10 each for n = 2, 3, 4, 5). |
| `report/evidence/results_periodic.json` | Same schema, periodic BC. | 5 trials at n=5. |
| `report/evidence/run_dirichlet.log` | Driver stdout from the replication run. | Single file, ~90 s of output. |
| `report/evidence/judge_response.json` | LLM-judge (Argo Opus 4.7) verdict rationale on REPLICATED/PARTIAL/… given the claims + results. | Single JSON. |

## Headline numeric results (extracted from evidence, for quick reference)

Dirichlet BC — Fig. 4 comparison (mean ± std over 10 trials):

| n | This replication ε_tr | Quantum norm | Classical norm |
|---|---|---|---|
| 2 | (2.4 ± 3.0) · 10⁻⁷ | 0.7071 | 0.7071 |
| 3 | (2.1 ± 6.4) · 10⁻⁶ | 2.061 | 2.061 |
| 4 | (2.9 ± 8.7) · 10⁻⁶ | 6.858 | 6.858 |
| 5 | **0.0070 ± 0.0074** | **24.66** | **25.30** |

Dirichlet BC — Fig. 3(b) at n=5:

| | Quantum norm | Classical norm |
|---|---|---|
| Paper | 24.6 | 25.3 |
| Replication | 24.66 (mean of 10) | 25.30 (deterministic) |

Periodic BC — Fig. 3(a) at n=5 (5 trials):

| | Quantum norm | Classical norm |
|---|---|---|
| Paper | 22.9 | 23.5 |
| Replication | 22.68 (mean of 5) | 22.89 |

Mean ε_tr periodic n=5: 0.0034 (< 0.01 target).

## Provenance chain

1. arXiv 2106.09333 (paper) →
2. paper Eq. (14), (45), (46), (48) →
3. `work/vqa_poisson_replicate.py` (independent NumPy implementation) →
4. `report/evidence/results_*.json` (raw per-trial output) →
5. `report/REPORT.md` (tables + verdict) →
6. `report/evidence/judge_response.json` (LLM verdict cross-check) →
7. `report/REPORT.tex` + this artifacts_summary.md (packaging).

Everything after step 2 is fully reproducible from step 1 using the commands in
`workflow.md`.

## Not archived (would strengthen the replication)

- Digitized version of Fig. 4 (currently only visual estimates).
- Neumann-BC run data (skipped, C7 partial).
- Noise-model runs / real-hardware runs (would test NISQ-friendliness claim).
- Head-to-head Liu-2020 / VQLS runs in the same harness.
