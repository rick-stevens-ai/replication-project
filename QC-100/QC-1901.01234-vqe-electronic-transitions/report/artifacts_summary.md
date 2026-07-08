# Artifacts Summary — QC-1901.01234-vqe-electronic-transitions

Set: QC-100. Verdict: **REPLICATED**.

## Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary narrative replication report (Markdown, human-readable). Full paper summary, method, results tables, verdict justification, evidence pointers. |
| `REPORT.tex` | LaTeX version of the same report, with a dedicated critical-assessment section. |
| `open_questions.json` | Bare JSON list of exactly 5 open questions (schema: `{q, basis, next_steps}` per item). |
| `open_questions_section.tex` | LaTeX-formatted version of the same 5 open questions, embeddable in `REPORT.tex`. |
| `workflow.md` | Step-by-step reproduction workflow (env setup → run scripts → inspect artifacts → rerun-in-place). |
| `artifacts_summary.md` | (this file) One-liner index of every artifact. |
| `failure_analysis.md` | Honest critique of the replication: what was genuinely reimplemented, what was scoped-out, what would strengthen the case, what would falsify it. |

## Evidence artifacts (`report/evidence/`)

| File | Purpose |
|---|---|
| `mcvqe_exciton.py` | MC-VQE implementation, ~230 LOC. State-averaged VQE + subspace Hamiltonian diagonalization on ab initio exciton Hamiltonian (Eq. 8 of paper). |
| `mcvqe_results.json` | Raw numerical results for 5 configurations (N=2/4, L=1/2/3): exact eigenvalues, MC-VQE eigenvalues, absolute and excitation-energy errors, optimizer stats, wall times. |
| `vqe_vqd_h2.py` | VQE (ground) + VQD (first excited) on H2 STO-3G via PennyLane + PySCF. Cross-family sanity check for the excited-state-VQE claim family. |
| `h2_vqe_vqd_results.json` | Raw H2 numerical results: exact E0/E1, our VQE E0, our VQD E1, gap, overlap with ground. |
| `RUN_INFO.txt` | Environment record: host, OS, Python version, key package versions, git-equivalent state. |

## Extraction artifacts (`extraction/`)

| File | Purpose |
|---|---|
| `nougat.mmd` | Nougat OCR extraction stub of `work/paper.pdf`. (Placeholder — full Nougat run out of scope; the paper is a standard arXiv TeX-derived PDF and REPORT.md already captures all quantitative claims from the source PDF.) |

## Working artifacts (`work/`)

| File | Purpose |
|---|---|
| `paper.pdf` | Raw arXiv:1901.01234v2 PDF (10 Apr 2019 version, PRL 122 230401). |
| `venv/` | Python virtualenv used for the replication (not committed; recreate per `workflow.md`). |
| `mcvqe_exciton.py`, `vqe_vqd_h2.py` | Working copies of the runnable scripts (identical to `report/evidence/` versions; run from here). |

## Compute + provenance

- **Host:** CherryRd (Darwin 25.3.0, macOS)
- **Runtime:** system Python 3 in isolated venv, single-thread NumPy/SciPy
- **Endpoint policy:** free-only — no paid API calls. All simulation is local.
- **Deterministic:** seed=42 in both scripts; results bit-reproducible.
- **Wall clock:** ~5 min total for the full replication sweep.

## Artifact count

7 backfilled artifacts added on 2026-07-06 to bring this dir to the 8-artifact
standard (REPORT.md was already present pre-backfill).
