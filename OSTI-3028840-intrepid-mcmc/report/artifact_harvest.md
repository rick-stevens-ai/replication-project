# Artifact Harvest

| Artifact | Source | Detail |
|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3028840 | INL/JOU-24-82292-Rev-0; 37 pages; 21,671,168 bytes; PDF v1.4. Fetched via `ssh uicgpu` proxy (direct CherryRd fetch avoided per brief). Saved `work/paper.pdf`. |
| Paper text | pymupdf extraction on uicgpu | 103,951 chars, 37 pages → `work/paper.txt`. |
| Public code | — | **None found.** The paper (INL journal article / CMA 2025) does not release a code repository or supplementary data. Core is fully specified by equations (Algorithms 1–2, Eqs. 9–31, Tables 2–4), so we reimplemented from scratch. |
| Public data | — | Not applicable — Section 4.1 targets are analytically defined (indicator × parent density). IID references generated locally by rejection sampling. |

## Reimplementation artifacts (this replication)
- `work/intrepid.py` — Intrepid + CMH kernels, 9 analytical targets (Tables 2–4), rejection reference sampler, TVD metric. Overflow-safe density evaluation.
- `work/run_experiments.py` — β-sweep driver (30 trials × 7 β × 9 cases × 100k-sample chains, 10k burn-in), 32-way ProcessPool on uicgpu.
- `report/evidence/results.json` — full metric summary (TVD, err-in-mean, acceptance, no-mode-failure counts) per case per β.
- `report/evidence/results_v1.json` — first pass (before valid-start fix), retained for transparency.
- `report/evidence/bimodal_coverage.txt`, `circles_quicktest.txt` — targeted mode-coverage checks.

## Compute
- Host: uicgpu01 (8×A100 node; CPU numpy 1.23.5 / scipy 1.10.1 used — algorithm is CPU-bound MCMC). Internet proxy via `~/env.sh`.
- LLM judge: Argo proxy (free), model gpt-5.2 / opus-4.8 fallback.
