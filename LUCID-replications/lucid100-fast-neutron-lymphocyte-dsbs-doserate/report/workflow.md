# Workflow — LUCID replication of Nair et al. 2019 (fast-neutron DSBs, dose rate)

## 1. Paper acquisition
- Source: Europe PMC OA render (`articles/PMC6862539?pdf=render`), CC-BY 4.0.
- Secondary copy via Unpaywall/S2 route on 2026-06-09.
- Full-text JATS XML from EPMC `/PMC6862539/fullTextXML`.
- Local `pdftotext -layout paper.pdf paper.txt` (49 KB) as canonical digitization source.
- Provenance manifest: `artifacts/MANIFEST.md`.

## 2. Data digitization
- Tables 1, 2, 3 hand-digitized from `pdftotext -layout` output into:
  - `data/table1_induction.csv` (5 doses × HDR/LDR mean+SD)
  - `data/table2_hdr_ldr_ratio.csv` (per-dose HDR/LDR ratio)
  - `data/table3_repair_kinetics.csv` (6 time points × HDR/LDR mean+SD at 1 Gy)
- Abstract + Discussion headline claims into `data/paper_key_numbers.json`.
- No per-cell / per-donor data available anywhere; EPMC `hasSuppl:N`, no Zenodo/Figshare/GEO/GitHub.

## 3. First-pass smoke (2026-06-09)
- `scripts/smoke_replicate.py` → 3 reduced checks (C1 mean ratio, C2 poly2 R², C7 repair half-life).
- Output: `scripts/smoke_outputs/smoke_results.json`, `smoke_plots.png`.
- Result: 3/3 PASS.

## 4. Extended audit (2026-06-22, this session)
- `scripts/extended_replicate.py` → 7 checks E1–E7:
  - E1: per-dose HDR/LDR ratio vs Table 2 → max abs err 0.005.
  - E2: mean ratio vs abstract claim (+40 %) → 39.77 %.
  - E3: K-coefficient max locus (1.87 @ 0.250 Gy) → 1.872 @ 0.250 Gy.
  - E4: linear vs poly2 vs LQ AICc → poly2 wins by ΔAICc ~5–6 (LQ indistinguishable at n=5).
  - E5: three-variant repair half-life + parametric bootstrap 95 % CI.
  - E6: Welch t-test on 24 h residual (n=4 donors) → p=0.306.
  - E7: dose-rate ratio sanity check → 26.67×.
- Output: `results/extended_results.json`, `results/extended_summary.md`, `results/induction_and_repair_overlay.png`.
- Result: 7/7 PASS at table level; 1 method-text anomaly flagged (C7).

## 5. Backfill (2026-07-06, this session)
- 7 report/ artifacts written: REPORT.tex, open_questions.json,
  open_questions_section.tex, workflow.md, artifacts_summary.md,
  failure_analysis.md, extraction/nougat.mmd stub.
- Verdict cross-check vs queue REPLICATED: MATCH.
- No re-run of simulations; no new endpoint calls; free-tier only.

## Tools & endpoints (all free)
- Python 3.14 (CherryRd), numpy only.
- `pdftotext -layout` (poppler).
- Europe PMC REST (public), Unpaywall (public), S2 (free API key).
- No paid endpoints, no author contact, no heavy compute.

## Compute footprint
- Total wall-time < 2 s for both harnesses.
- No GPU, no HPC, no subagent fan-out beyond this backfill task.
