# Artifacts Summary — arXiv:1710.01022

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1710.01022-variational-quantum-optimization-moll-ibm/`

## Required 8 artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` (also `work/paper.pdf`) | ✅ present | fetched from `https://arxiv.org/pdf/1710.01022` |
| 2 | Marker parse | `extraction/marker.md` | ✅ present (fallback) | Marker not installed; pdftotext-derived Markdown with parse-provenance note |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ present (fallback) | Nougat not installed; hand-typed LaTeX-form mirror of key equations |
| 4 | Detailed report | `report/REPORT.tex` | ✅ present | full section-by-section LaTeX; REPORT.pdf compile attempted (see failure_analysis.md) |
| 5 | Open questions | `report/open_questions.json` + REPORT.tex §Open Questions | ✅ present | 5 grounded Q&A per QC brief §6 |
| 6 | Workflow | `report/workflow.md` | ✅ present | end-to-end recipe + tool versions |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ present | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ present | honest gap list |

## Evidence artifacts (real simulation outputs)

| Path | Contents |
|---|---|
| `report/evidence/qaoa_p1.py` | QAOA-p=1 numpy statevector reproduction, 60 COBYLA restarts × 3 graphs |
| `report/evidence/qaoa_p1_results.json` | numeric results: (n, edges, MaxCut, ⟨C⟩_QAOA, r, meets_0.6924) for n = 6, 8, 10 |
| `report/evidence/qaoa_p1.log` | stdout of the qaoa_p1.py run |
| `report/evidence/vqe_h2.py` | VQE-H₂ numpy statevector reproduction, 40 COBYLA restarts on 6-parameter RY+CZ ansatz |
| `report/evidence/vqe_h2_results.json` | numeric results: (E_NR, E_exact_elec, E_exact_total, E_vqe_elec, E_vqe_total, gap_mHa, chem_accuracy_reached_vs_FCI_lit) |
| `report/evidence/vqe_h2.log` | stdout of the vqe_h2.py run |

## Intermediate work

| Path | Contents |
|---|---|
| `work/paper.pdf` | mirror of arXiv PDF (5.7 MB) |
| `work/paper.txt` | pdftotext reflow (1808 lines) |
| `work/paper_layout.txt` | pdftotext -layout mode (1488 lines) |

## Environment

| Path | Contents |
|---|---|
| `.venv/` | Python 3 virtualenv, numpy 2.5.1 + scipy 1.18.0 |

## Verdict (headline)

**REPLICATED** — both testable claims (C1 QAOA-p=1 on 3-regular graphs ≥ 0.6924; C2 VQE-H₂ ground-state convergence) reproduced by direct numpy simulation. QAOA-p=1 gave r = 0.849 / 0.815 / 0.818 on n=6/8/10 graphs. VQE-H₂ reached the exact eigenvalue of the specified 2-qubit tapered Hamiltonian to 0.00 mHa; 6.1 mHa offset vs. literature FCI attributed to Hamiltonian coefficient truncation (documented, non-algorithmic).

## SHA/size fingerprint (as-of write)

Run `find . -maxdepth 3 -type f -not -path './.venv/*' -not -path './work/paper*' | xargs shasum` for a full manifest if needed.
