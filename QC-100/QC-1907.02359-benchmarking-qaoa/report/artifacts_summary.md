# Artifacts Summary — QC-1907.02359 (Benchmarking QAOA)

## Directory
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1907.02359-benchmarking-qaoa/`

## Primary artifacts

| Artifact                                    | Kind              | Purpose                                                    |
|---------------------------------------------|-------------------|------------------------------------------------------------|
| `report/REPORT.md`                          | narrative         | Original human-readable replication report (verdict prose) |
| `report/REPORT.tex`                         | LaTeX             | Backfilled formal report with explicit Critique section    |
| `report/open_questions.json`                | JSON (list of 5)  | Structured open questions (q, basis, next_steps)           |
| `report/open_questions_section.tex`         | LaTeX             | Rendered version, `\input` from REPORT.tex                 |
| `report/workflow.md`                        | Markdown          | End-to-end reproducibility recipe                          |
| `report/artifacts_summary.md`               | Markdown          | This index                                                 |
| `report/failure_analysis.md`                | Markdown          | Honest critique of gaps and untested claims                |
| `extraction/nougat.mmd`                     | MMD (stub)        | Placeholder for nougat text extraction                     |

## Evidence

| File                                                 | Content                                              |
|------------------------------------------------------|------------------------------------------------------|
| `report/evidence/qaoa_results.json`                  | Per-(graph, p) result rows (18 rows: 6 graphs × 3 p) |
| `report/evidence/qaoa_results.csv`                   | Same table, CSV                                      |
| `report/evidence/qaoa_aggregate.json`                | Mean α per family × p                                |
| `report/evidence/aer_shot_crosscheck.json`           | 20 000-shot Aer QASM cross-check on 3reg_n8 p=1      |

## Code

| File                                | Purpose                                                             |
|-------------------------------------|---------------------------------------------------------------------|
| `code/qaoa_maxcut.py`               | Main benchmark: builds circuits, runs COBYLA, dumps results         |
| `code/aer_crosscheck.py`            | Shot-based Aer QASM cross-check at optimal (γ, β) for 3reg_n8 p=1   |

## Source paper

| File                    | Content                                       |
|-------------------------|-----------------------------------------------|
| `work/paper.pdf`        | Downloaded arXiv PDF                          |
| `work/paper.txt`        | `pdftotext` output (2261 lines)               |

## Logs

| File                            | Content                                        |
|---------------------------------|------------------------------------------------|
| `logs/run2.log`                 | Main sweep transcript (~63 s wallclock)        |
| `logs/aer_crosscheck.log`       | Aer shot-based cross-check transcript          |

## Verdict
**REPLICATED** on simulator-testable MaxCut claims (C1, C2, C4 fully; C3 partial). C5 (D-Wave), C6 (IBM Q hardware), plus 2-SAT and $n\ge 12$ scale are out-of-scope for QC-100's free-simulator wave; flagged in Critique and Failure Analysis, not held against the verdict.

## Artifact count (this backfill delta)
Added 7 artifacts:
1. `report/REPORT.tex`
2. `report/open_questions.json`
3. `report/open_questions_section.tex`
4. `report/workflow.md`
5. `report/artifacts_summary.md`
6. `report/failure_analysis.md`
7. `extraction/nougat.mmd` (stub)
