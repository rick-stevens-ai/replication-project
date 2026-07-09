# Artifacts inventory

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9812070-hidden-subgroup-nonabelian-rotteler-beth/`

## The 8 mandatory artifacts

| # | Artifact                              | Path                                   | Status |
|---|---------------------------------------|----------------------------------------|--------|
| 1 | Original paper PDF                    | `paper.pdf`                            | ✅ 166,896 bytes, arXiv fetched |
| 2 | Marker parse                          | `extraction/marker.md`                 | ⚠️ pdftotext fallback (Marker not installed) |
| 3 | Nougat parse                          | `extraction/nougat.mmd`                | ⚠️ pdftotext fallback (Nougat not installed) |
| 4 | Detailed LaTeX report                 | `report/REPORT.tex`                    | ✅ 15,578 bytes, full sections + tables |
| 5 | 5 heavy-duty open questions           | `report/open_questions.json`           | ✅ 5 objects with q/basis/next_steps |
| 6 | Workflow + tools + effort             | `report/workflow.md`                   | ✅ |
| 7 | Artifacts summary (this file)         | `report/artifacts_summary.md`          | ✅ |
| 8 | Failure analysis                      | `report/failure_analysis.md`           | ✅ |

## Evidence (real, reproducible)

| Path | Description |
|------|-------------|
| `report/evidence/hsp_wreath.py` | ~350-line numpy implementation of the paper's algorithm |
| `report/evidence/scaling_and_stress.py` | Stress sweep + non-abelian focus + n=3 scaling |
| `report/evidence/results.json` | Main-run results (6 trials at n=2, all p=1.00) |
| `report/evidence/stress_results.json` | Stress sweep + scaling results |
| `report/evidence/run.log` | stdout from main run (verdict: REPLICATED) |
| `report/evidence/stress_run.log` | stdout from stress/scaling run |

## Intermediates

| Path | Description |
|------|-------------|
| `work/paper.txt` | pdftotext -layout of paper.pdf |

## Traces
- Main-run verdict line: `[VERDICT] REPLICATED` in `run.log`
- Stress sweep total wall-clock: 2.75 s (from `stress_run.log` last line)
- DFT orthogonality error: `1.11e-16` at n=2 (from `run.log`)

## What the report claims and where the evidence lives
- **REPLICATED verdict** — see `results.json.verdict_note` ("REPLICATED"),
  reproducible with `python3 report/evidence/hsp_wreath.py`.
- **Empirical p=1.00 on 6 initial trials** — `results.json.trials[*].prob_success`.
- **Stress sweep tracks Lemma 6.3** — `stress_results.json.stress_n2[*]`
  with the `paper_bound_1-2^{-i/4}` field for direct comparison.
- **Non-abelian generators recovered** — `stress_results.json.nonabelian_focus_n2`.
- **n=3 scaling** — `stress_results.json.scaling_n3[*].prob_success` all 1.00.
