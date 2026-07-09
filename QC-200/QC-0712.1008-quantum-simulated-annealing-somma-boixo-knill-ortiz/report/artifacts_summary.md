# Artifacts summary — QC-200 / arXiv:0712.1008

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0712.1008-quantum-simulated-annealing-somma-boixo-knill-ortiz/`

## The 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Artifact | Path | Size | SHA-256 (short) | Present? |
|---|----------|------|------|-----------------|:--------:|
| 1 | Original PDF | `paper.pdf` | 420 852 B | `c7687dec8168…efbeb4df` | ✅ |
| 2 | Marker extraction | `extraction/marker.md` | 36 919 B | `93ddd6215c60…bc31ae8e` | ✅ (pdftotext fallback, provenance header explains) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | 59 975 B | `61f32005d311…b06a87f` | ✅ (pdftotext -layout fallback, provenance header explains) |
| 4 | Detailed LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf`) | 15 815 B / 289 470 B | `d730791c…e08ded4` / `144d5032…0e152f5dcf47` | ✅ (compiled 5 pages) |
| 5 | 5 open questions | `report/open_questions.json` | 5 134 B | | ✅ (each with q, basis, next_steps) |
| 6 | Workflow + tools + effort | `report/workflow.md` | 4 625 B | | ✅ |
| 7 | Artifacts summary (this file) | `report/artifacts_summary.md` | — | | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | — | | ✅ |

## Evidence + code
| Path | Size | Purpose |
|------|------|---------|
| `report/evidence/qsa_szegedy.py` | 13 899 B | Full replication driver, 405 LOC |
| `report/evidence/qsa_results.json` | ~28 KB | Structured per-instance/per-β numbers + aggregate verdict |
| `report/evidence/run.log` | ~2 KB | tee'd stdout of the replication run |

## Working intermediates
| Path | Purpose |
|------|---------|
| `work/paper.pdf` | Fetched arXiv PDF (identical to top-level `paper.pdf`) |
| `work/paper.txt` | `pdftotext -layout` dump used for skim |
| `work/paper_flow.txt` | `pdftotext` (flowing) dump used for grep of technical sections |

## External sources
- arXiv PDF: `https://arxiv.org/pdf/0712.1008` (fetched 2026-07-05).
- arXiv abs page: `https://arxiv.org/abs/0712.1008` (verified metadata).
- No other external data was consumed; this is a fully self-contained
  numerical replication.

## Numerical outputs (from `qsa_results.json`)
- 5 instances × 3 β = 15 (instance, β) rows.
- All 5 aggregate checks PASS: `db_ok`, `stationary_ok`, `gibbs_fixed_ok`,
  `quadratic_ok`, `prediction_match`.
- `c_ratio_min_all = 2.6808`, `c_ratio_min_per_beta = {0.5: 2.681, 1.0: 2.768, 2.0: 2.774}`.
- Verdict emitted by the driver: **REPLICATED**.

## Traces
- Replication run log: `report/evidence/run.log` (tee'd during the single successful run).
- LaTeX compile log: `report/REPORT.log` (5-page PDF, no errors).
- No PBS/Slurm/SSH invocations were needed (all compute on the CherryRd host).

## Provenance notes
- Marker/Nougat binaries are not installed on CherryRd; no central-corpus
  parse of 0712.1008 exists (checked BVBRC/OSTI/LUCID trees under
  `~/Dropbox/REPLICATE-PROJECT/`). Both extraction files are labeled
  fallbacks in their headers. The numerical replication does not depend
  on those files — it works directly from the PDF text.
- The task brief listed the paper's authors as "Somma, Boixo, Knill, Ortiz";
  the actual arXiv:0712.1008 v1 title page lists **R. D. Somma, S. Boixo,
  and H. Barnum**. (Knill is added in the later PRL 101, 130504 (2008)
  version. Ortiz coauthored the related arXiv:0706.1146 with Somma.)
  We stayed with the paper as identified by the trusted arxiv_id.
