# Artifacts summary — QC-1708.09213

Root: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1708.09213-lecture-notes-of-tensor-network-contractions/`

## Report artifacts (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Human-readable canonical report (numerical tables, judge JSON, verdict). |
| `REPORT.tex` | LaTeX rendering of the same report (compilable standalone). |
| `open_questions.json` | Machine-readable list of 5 open questions, each with basis + concrete next_steps. Bare JSON list of 5 objects (no wrapper). |
| `open_questions_section.tex` | LaTeX rendering of the 5 open questions, `\input`-ed by `REPORT.tex`. |
| `workflow.md` | Pipeline diagram + step-by-step description of what was actually executed. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest critique of what was **not** re-run, what could be wrong, and what would falsify the REPLICATED verdict. |

## Work artifacts (`work/`)  — populated by the original replication run
| File / dir | Purpose |
|---|---|
| `.venv/` | Python 3.11 virtualenv (quimb 1.14.0, numba 0.62.1, numpy, scipy). |
| `exp1_dmrg_tfim_energy.py` | DMRG on TFIM h=1 OBC, N=20/40/60/80, χ=32; 1/N extrapolation to −4/π. |
| `exp1b_check_ed_small.py` | ED vs Pfeuty FF vs DMRG cross-check for N=6..12. |
| `exp2_entanglement_scaling.py` | DMRG entropies at every bond, fit slope×log(chord) → c. |
| `exp2b_diag_entropy.py` | Peschel–Kaufmann attempted FF entropy formula (BUGGY, kept for provenance). |
| `exp2c_ed_entropy.py` | ED entropy for N=10..16 as fit-method cross-check. |
| `exp3_canonical_form.py` | Left-canonicalization orthogonality check + Schmidt truncation vs `∑_{k>χ}σ_k²`. |
| `exp4_itebd_tfim.py` | Second-order iTEBD imaginary-time, N=64, χ=32, dτ=0.05, T=8, Neel init. |
| `llm_judge.py` | Sends evidence JSON to Argo `argo:gpt-5` (localhost:44497); records per-claim + overall verdict. |
| stdout logs | Raw run outputs used to populate the numeric tables in `REPORT.md`. |

## Extraction (`extraction/`)
| File | Purpose |
|---|---|
| `nougat.mmd` | Nougat OCR stub (see note in that file). |

## Verdict
**REPLICATED** (see `REPORT.md` §6 for full justification and `failure_analysis.md` for critique).

## Cross-check summary (evidence that verdict is not vapor)
- DMRG vs FF: rel err ≤ 10^{-11} across N=20..80 (C1).
- ED vs FF vs DMRG at N=6..12: agree to 10^{-14} (C1 sanity).
- Central charge c: monotone → 0.5 (0.5326 → 0.5169 → 0.5047 for N=32, 64, 128), (C2).
- Canonical-form ‖∑A†A − I‖ ≤ 10^{-15}; truncation err = ∑σ² to 6 digits (C3).
- iTEBD vs FF at N=64: 5×10^{-5} per site (C4).
- Argo gpt-5 judge: per-claim REPLICATED, overall REPLICATED.
