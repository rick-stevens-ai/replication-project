# Artifacts Summary — QC-1910.02719 Cai Hubbard HVA

## Report artifacts (`report/`)

| File | Purpose |
|------|---------|
| `REPORT.md` | Full narrative replication report (markdown, source of truth) |
| `REPORT.tex` | LaTeX version of the report with critique section (added by backfill) |
| `workflow.md` | Reproduction workflow, environment, and step-by-step commands (backfill) |
| `open_questions.json` | 5 concrete open follow-ups as bare JSON list `{q, basis, next_steps}` (backfill) |
| `open_questions_section.tex` | LaTeX-formatted version of the 5 open questions (backfill) |
| `failure_analysis.md` | Honest critique — what was quoted vs. regenerated, what was skipped (backfill) |
| `artifacts_summary.md` | This file (backfill) |

## Evidence artifacts (`report/evidence/`)

| File | Contents | Origin |
|------|----------|--------|
| `formula_check.json` | Closed-form evaluations of `N_1q(V)`, `N_2q(V)`, `T(V)` at `V ∈ {4,6,9,12,16,20,25,30,36,49}` and headline `V=25` cross-check vs. paper | `code/formula_check.py` |
| `hubbard_small_runs.json` | `openfermion` build + `count_qubits` + exact-diag `E_0` for 2×2 (V=4) and 2×3 (V=6) | `code/hubbard_vqe_small.py` |
| `hubbard_vqe_runs.json` | End-to-end HVA VQE runs at V∈{4,6}, p∈{1,2,3}: `{E_start, E_VQE, E_0, rel_err}` | `code/hubbard_vqe_run.py` |
| `hva_gate_counts.json` | Combinatorial primitive counter (undercounts by `≈ 4√V·L` boundary-`Z` bookkeeping) | `code/count_hva_gates.py` |
| `judge_argo.json` | Single-model Argo (`argo:gpt-5.1`) judge verdict | `code/judge_argo.py` |

## Code artifacts (`code/`)

| File | Role |
|------|------|
| `formula_check.py` | Evaluates the Appendix A2 closed-form gate-count and runtime formulas at multiple V; cross-checks V=25 headline. |
| `hubbard_vqe_small.py` | Builds the real Hubbard Hamiltonian via `openfermion.hamiltonians.fermi_hubbard`, Jordan-Wigner it, measures qubit count and exact-diag ground state. |
| `hubbard_vqe_run.py` | Runs a first-order Trotter HVA-VQE at V=4 and V=6 for p=1..3 with L-BFGS-B, reports converged energy vs. exact. |
| `count_hva_gates.py` | Combinatorial primitive counter from the swap-network — kept in the repo as an honest artefact (undercounts boundary Z-rotations vs. closed form). |
| `judge_argo.py` | Passes all evidence JSON to the local Argo proxy and returns a structured judge verdict. |

## Extraction artifact (`extraction/`)

| File | Purpose |
|------|---------|
| `nougat.mmd` | Nougat-style Markdown extraction of the paper's key formulas and headline values, provided as a stub for downstream text-mining (backfill) |

## Paper source (`work/`)

| File | Purpose |
|------|---------|
| `1910.02719.pdf` | arXiv paper source (v4, 1 July 2020) |
| `1910.02719.txt` | `pdftotext -layout` output |
| `1910.02719.raw.txt` | `pdftotext -raw` output (formulas readable) |

## Artifact-count audit (backfill deliverable)

The 7 new backfill artifacts (REPORT.tex, open_questions.json, open_questions_section.tex,
workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd) bring the
directory to the 8-artifact standard (REPORT.md was pre-existing).
