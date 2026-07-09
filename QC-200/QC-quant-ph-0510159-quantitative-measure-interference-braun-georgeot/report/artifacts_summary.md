# Artifacts inventory — quant-ph/0510159

## 8-artifact bar (Rick 2026-07-05 REPLICATION_DIR_STANDARD)

| # | Artifact                        | Path                                  | Status |
|---|---------------------------------|---------------------------------------|--------|
| 1 | Original PDF                    | `paper.pdf`                           | ✓ 361 KB |
| 2 | Marker parse                    | `extraction/marker.md`                | ✓ fallback (see failure_analysis) |
| 3 | Nougat parse                    | `extraction/nougat.mmd`               | ✓ fallback (see failure_analysis) |
| 4 | REPORT.tex + verdict            | `report/REPORT.tex`                   | ✓ REPLICATED |
| 5 | Open questions (JSON + section) | `report/open_questions.json` + REPORT.tex §Open Questions | ✓ 5 Q's each with `q/basis/next_steps` |
| 6 | Workflow + tools + versions     | `report/workflow.md`                  | ✓ |
| 7 | Artifacts summary               | `report/artifacts_summary.md`         | ✓ (this file) |
| 8 | Failure analysis                | `report/failure_analysis.md`          | ✓ |

## Evidence + code (`report/evidence/`)

| File               | Role                                                     |
|--------------------|----------------------------------------------------------|
| `interference.py`  | Core replication code (NumPy). 180 LoC.                  |
| `run.log`          | stdout from the run, showing 17/17 standard-gate matches |
| `results.json`     | Machine-readable table of all numeric probes             |

## Intermediate data (`work/`)

| File                             | Role                              |
|----------------------------------|-----------------------------------|
| `paper.txt`                      | `pdftotext -layout` of paper.pdf  |
| `paper_plain.txt`                | plain `pdftotext` of paper.pdf    |

## Additional extraction sources (`extraction/`)

| File                       | Role                                           |
|----------------------------|------------------------------------------------|
| `marker.md`                | Marker-schema fallback with core equations     |
| `nougat.mmd`               | Nougat-schema fallback with all core equations |
| `pdftotext_layout.txt`     | Raw pdftotext layout dump used as ground truth |

## Traces of exact match points

- Standard-gate matches: `run.log` shows 17 lines with `[MATCH]` tag.
- Beam-splitter matches: 6 lines with `[MATCH]`.
- Tensor-identity matches: 16 lines with `[MATCH]`.
- Grover n=8: `I(full)=254.0101` vs paper `≈ 2^n - 2 = 254`.
- Teleportation: `I = 6.000000` exact vs paper `I = 6`.

Reproducibility: `cd report/evidence && python3 interference.py` gives an
identical `results.json` byte-for-byte (only NumPy versions ≥ 1.20 required;
no RNG, no external services).
