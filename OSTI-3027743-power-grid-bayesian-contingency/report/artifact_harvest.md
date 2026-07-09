# Artifact Harvest

## Primary source
- **PDF:** `https://www.osti.gov/servlets/purl/3027743` → `work/osti_3027743.pdf` (5,237,127 B, 20 pages)
- OSTI record ID: 3027743
- DOI: 10.1115/1.4069339 (ASCE-ASME Journal of Risk and Uncertainty in Engineering Systems, Part A)
- INL Technical Report ID: INL/JOU-24-81251-Revision-0
- Publisher preprint: August 2025

## Code / data availability
- **NO PUBLIC CODE:** Paper's Data Availability Statement (§ "Data Availability Statement", p. 20):
  > "Some or all data, models, or code generated or used during the study are proprietary or confidential in nature and may only be provided with restrictions."
- No GitHub, Zenodo, or supplementary code URL mentioned in the manuscript.
- SCANN (Smart Contingency Analysis Neural Network) platform referenced ([6] = Yang et al. 2020 Resilience Week) — a survey paper, not a code release.
- Related INL work by same team: `[30] Dhulipala et al., "Harnessing Distributed GPU Computing for Generalizable Graph Convolutional Networks in Power Grid Reliability Assessments," Energy and AI 19 (2025), DOI 10.1016/j.egyai.2025.100471` — also does not release code.

## Open-source software used for the replication
| Package | Version | Purpose | URL |
|---|---|---|---|
| pandapower | 3.4.0 | AC (Newton-Raphson) & DC power flow on IEEE 14-bus | https://www.pandapower.org/ |
| numpy | 1.26.4 | Arrays | — |
| scipy | (dep) | `norm` for CDF/PPF | — |
| torch | 2.2.2 | Anchored-ensemble training | https://pytorch.org/ |
| scikit-learn | 1.9.0 | (imported for potential preprocessing; not used in final path) | — |
| matplotlib | (latest) | Figures | — |

## Reference network
- **IEEE 14-bus test case:** built-in `pandapower.networks.case14()` — 14 buses, 15 lines, 4 generators, 11 loads, 1 external grid (slack). Matches the description in Section 4.1 of the paper (paper says "14 buses, 5 generators, 11 loads" — one of the "generators" is the ext_grid slack; equivalent modeling).

## Generated artifacts (this replication)
- `work/dataset_14bus.npz` (560 KB) — 1280 train + 1200 test samples, {X (features), A (adjacency), VMnr, VAnr, VMdc, VAdc, K (contingency level)}
- `work/predictions_14bus.npz` (3.8 MB) — 40-member ensemble VM and VA predictions for every test point
- `work/results_14bus.json` — per-contingency RMSE, miscalibration areas (diag + low-rank), NLL, DC baseline
- `work/llm_judge.txt` — Argo/gpt-5 judge assessment against paper's Table 1
- `report/evidence/predictions_14bus.png` — pred vs true scatter with ±2σ error bars
- `report/evidence/miscalibration_14bus.png` — VM/VA calibration curves (low-rank)
- `work/generate_data.py` — reproducible data-gen script
- `work/train_ensemble.py` — reproducible training + metrics script
- `work/make_figures.py` — figure generation script
- `work/llm_judge.py` — LLM-judge invocation

## LLM endpoint
- Argo proxy `http://127.0.0.1:44497/v1/chat/completions` with `Authorization: Bearer stevens`, model `argo:gpt-5` (free per project rules; claude-opus-4.7 hit a 502 upstream response-shape validation error).
