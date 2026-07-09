# Workflow — Mariotti et al. 2013 split-dose γ-H2AX replication

Paper: Mariotti et al., *Use of the γ-H2AX Assay to Investigate DNA Repair Dynamics
Following Multiple Radiation Exposures*, PLoS ONE 8(11):e79541 (2013).
DOI 10.1371/journal.pone.0079541.

## Chronology
- **Pass 1** — 5-parameter model (Eqs 1–4) implemented; published fits overlaid vs
  digitized Fig-1A and Fig-5 data. Verdict PARTIAL (cov 7, agr 7). Preserved as
  `REPORT.pass1.md`.
- **Pass 2 (2026-06-23)** — Marker re-parse of the PDF; `code/pass2_claims.py` adds
  8 claim-level tests (T-1…T-8) each tied to a verbatim quote + numeric threshold;
  `code/pass2_fig4_plot.py` reproduces the Fig-4 net-foci bar chart. Verdict
  upgraded to REPLICATED (cov 9/11, agr 8/11). Report: `REPORT.md`.
- **2026-07-06** — 8-artifact backfill (this pass): `report/REPORT.tex`,
  `report/open_questions.json` (+ `open_questions_section.tex`), `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`, `extraction/nougat.mmd`
  stub. **No sims re-run** — synthesized from the existing REPORT.md + on-disk
  results/figures + paper re-read. Written directly in the parent session after
  subagent attempts timed out on write-flush.

## Tools / versions
- Python 3 (NumPy, SciPy, Matplotlib), free local CPU (CherryRd).
- Ground truth: `data/TableS1.docx` (PLoS supplementary, CC-BY) + Eqs (3)/(4).
- Canonical text: Marker (UICGPU 2026-06-22 run); provenance `PARSER_PROVENANCE.md`.
- No paid endpoints, no network dependency in the claim-test code.

## Reproducer
```
python3 code/pass2_claims.py     # 8 claim tests -> results/pass2_claims.json
python3 code/pass2_fig4_plot.py  # bar chart    -> figures/fig4_reproduction.png
python3 code/validate.py; python3 code/refit.py   # pass-1 artifacts
```
Total runtime <5 s on a laptop-class CPU.

## Repo layout
- `code/pass2_claims.py`, `code/pass2_fig4_plot.py`, `code/validate.py`, `code/refit.py`
- `data/TableS1.docx` — 2 single-acute + 5 split-dose fit parameter rows
- `results/pass2_claims.json` — full per-claim numbers
- `figures/fig4_reproduction.png` — net-foci-from-2nd bar chart
- `REPORT.md`, `REPORT.pass1.md`, `PARSER_PROVENANCE.md`

## Work estimate
~1.5 person-days across pass 1 + pass 2 (model implementation, digitization,
8 claim tests, figure reproduction), + ~0.5 h backfill. No HPC/GPU.
