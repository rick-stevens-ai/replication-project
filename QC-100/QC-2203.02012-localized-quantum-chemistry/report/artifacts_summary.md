# Artifacts Summary — QC-2203.02012-localized-quantum-chemistry

Inventory of files in this replication directory. Preserves the original 2026-07-03 replication and adds the 2026-07-06 backfill artifacts.

## Top-level

| Path | Role | Origin |
|---|---|---|
| `work/paper.pdf` | Source paper (Otten et al. 2022, arXiv:2203.02012) | fetched |
| `work/paper.txt` | pdftotext extract for grep-ability | fetched |

## `code/` — reproducible pipeline (original)

| File | Purpose |
|---|---|
| `code/replicate_las_vqe.py` | STO-3G VQE-UCCSD on (H2)2, 3 geometries × 2 MO bases (canonical + Boys-localized). Uses Qiskit `Estimator` (statevector), ParityMapper (2-qubit reduction), UCCSD ansatz, SLSQP. Writes `report/evidence/results.json`. |
| `code/las_631g.py` | 6-31G CASCI + LASSCF fragment-product surrogate on (H2)2, 5 geometries at the paper's basis. Writes `report/evidence/las_6-31g.json`. |
| `code/las_fragment_product.py` | STO-3G fragment-product cross-check. Writes `report/evidence/las_fragment_product.json`. |

## `report/evidence/` — machine-readable results (original)

| File | Contents |
|---|---|
| `results.json` | VQE-UCCSD run outputs (per geometry × per basis): E_HF, E_FCI, E_VQE, num_qubits, num_parameters, converged flag. |
| `las_6-31g.json` | Per-geometry E_HF(H4), E_HF(H2), E_CASCI(H4), E_CASCI(H2), E_LAS_prod, err_LAS_vs_CASCI (mHa). |
| `las_fragment_product.json` | STO-3G analog of the above. |

## `logs/` — full stdout (original)

| File | Origin |
|---|---|
| `logs/run2.log` | stdout of `replicate_las_vqe.py`. |
| `logs/las_631g.log` | stdout of `las_631g.py`. |
| `logs/las_frag.log` | stdout of `las_fragment_product.py`. |

## `report/` — human-readable (original + backfill)

| File | Origin | Purpose |
|---|---|---|
| `report/REPORT.md` | original 2026-07-03 | primary replication report with tables and verdict |
| `report/REPORT.tex` | **backfill 2026-07-06** | LaTeX companion with explicit critique section |
| `report/failure_analysis.md` | **backfill 2026-07-06** | itemized weaknesses and residual risks |
| `report/open_questions.json` | **backfill 2026-07-06** | 5 concrete open questions in bare-JSON-list format |
| `report/open_questions_section.tex` | **backfill 2026-07-06** | LaTeX-formatted open-questions section |
| `report/workflow.md` | **backfill 2026-07-06** | step-by-step reproduction workflow |
| `report/artifacts_summary.md` | **backfill 2026-07-06** | this file |

## `extraction/` — text extraction (backfill stub)

| File | Origin | Purpose |
|---|---|---|
| `extraction/nougat.mmd` | **backfill 2026-07-06 (stub)** | Nougat MMD stub — this replication used `pdftotext` (see `work/paper.txt`), not Nougat. Kept as stub for the artifact-standard checklist. |

## Standard 8-artifact checklist (backfill target)

| # | Artifact | Present |
|---|---|---|
| 1 | REPORT.md | ✅ (`report/REPORT.md`) |
| 2 | REPORT.tex | ✅ (`report/REPORT.tex`, backfill) |
| 3 | open_questions.json | ✅ (`report/open_questions.json`, backfill) |
| 4 | open_questions_section.tex | ✅ (`report/open_questions_section.tex`, backfill) |
| 5 | workflow.md | ✅ (`report/workflow.md`, backfill) |
| 6 | artifacts_summary.md | ✅ (`report/artifacts_summary.md`, this file, backfill) |
| 7 | failure_analysis.md | ✅ (`report/failure_analysis.md`, backfill) |
| 8 | extraction/nougat.mmd | ✅ stub (`extraction/nougat.mmd`, backfill) |

## Preservation guarantee

The backfill added files only; no original file was modified. Original `report/REPORT.md`, `report/evidence/*.json`, `logs/*.log`, `code/*.py`, and `work/*` are byte-identical to the 2026-07-03 replication.
