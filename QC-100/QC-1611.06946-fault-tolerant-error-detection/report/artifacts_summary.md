# Artifacts Summary — QC-1611.06946 (fault-tolerant error detection)

## Canonical report artifacts (8-standard, post-backfill 2026-07-05)

| # | Path | Purpose |
|---|------|---------|
| 1 | `report/REPORT.md`                    | Human-readable canonical report (verdict + full table set) |
| 2 | `report/REPORT.tex`                   | LaTeX form of REPORT.md with critique section (backfilled) |
| 3 | `report/open_questions.json`          | Bare 5-object JSON list of open questions (backfilled) |
| 4 | `report/open_questions_section.tex`   | LaTeX open-questions section inlined into REPORT.tex (backfilled) |
| 5 | `report/workflow.md`                  | Step-by-step reproduction workflow (backfilled) |
| 6 | `report/artifacts_summary.md`         | This file — inventory + provenance (backfilled) |
| 7 | `report/failure_analysis.md`          | Honest critique of what the replication does / does not close (backfilled) |
| 8 | `extraction/nougat.mmd`               | Nougat-format extraction stub (backfilled — pdf-only source, real Nougat not re-run) |

## Simulation and evidence artifacts (already present, preserved)

| Path | Content |
|------|---------|
| `work/paper.pdf`                              | arXiv:1611.06946 PDF (389 KB) |
| `work/paper.txt`                              | pdftotext extraction (807 lines) |
| `work/ft422_stim.py`                          | Main Stim Monte-Carlo scan (4 encodings × 2 stabilizers × 8 p values × 1e6 shots) |
| `work/ft_single_fault_test.py`                | Exhaustive single-Pauli-fault enumeration on naive cat encoding (baseline / negative control) |
| `work/ft_flag_test.py`                        | Exhaustive single-Pauli-fault enumeration on flag-qubit encoding (0/324 undetected La errors — structural FT proof) |
| `work/make_plot.py`                           | Generates paper-Fig-4a-analog log-log plot |
| `report/evidence/results_main.json`           | Full JSON scan output (128 scan points) |
| `report/evidence/run_main.log`                | Wall-time log of the main scan |
| `report/evidence/ft_single_fault_check.log`   | Enumeration log — cat encoding (shows FT breakage as expected) |
| `report/evidence/ft_flag_check.log`           | Enumeration log — flag encoding (confirms FT property) |
| `report/evidence/fig4_replication.png`        | Replication of paper's Fig 4a (La, Lb, bare-qubit vs physical p) |

## Provenance and cost

- **Endpoint policy:** free endpoints only. All simulation is local Stim
  on CherryRd (macOS 25.3, Python 3.14, Stim 1.16.0). No paid API calls.
  Paper downloaded from arXiv (free).
- **Backfill pass (2026-07-05):** added artifacts 2–8 without re-running
  any simulation. All existing evidence (work/, report/evidence/) is
  untouched. See `failure_analysis.md` for honest gaps.
- **Nougat stub:** the paper was ingested via `pdftotext` (already in
  `work/paper.txt`) rather than Nougat, because Nougat's benefit is on
  math-heavy Markdown output and this replication used the PDF+text pair
  directly. The stub at `extraction/nougat.mmd` documents this choice
  and points at the working text extraction.
