# Artifacts Summary

| Path | Bytes | Description |
|------|------:|-------------|
| `paper.pdf` | 113,185 | arXiv:quant-ph/0012055 v2 (14 Mar 2001), 4 pages |
| `extraction/paper_text.txt` | 32,649 | pdftotext -layout output, 315 lines |
| `extraction/marker.md` | 5,206 | Marker-parsed markdown (copied from central corpus / sibling dir) |
| `extraction/nougat.mmd` | 3,124 | Nougat-style LaTeX mmd (copied from central corpus / sibling dir) |
| `work/toffoli_eq5.py` | 8,672 | First Eq. (5) replication with sweep over K, N_ph, oscillator state |
| `work/toffoli_eq5_v2.py` | 4,660 | Prefactor + tau-scale sweep to falsify parameter-guess |
| `work/toffoli_eq5_v3.py` | 5,613 | Multi-target comparison (literal vs Toffoli vs Toffoli+correction) |
| `work/toffoli_eq5_v4.py` | 3,893 | Typo hypothesis test: `+1/(32K) → -σx3/(32K)` |
| `work/eq6_and_grover.py` | 5,317 | Eq. (6) Fourier identity + Eq. (10) UG + full Grover search |
| `work/grover_trajectory.py` | 2,358 | Grover P(x₀) vs k for n=3..6, x₀=all-ones |
| `work/grover_debug.py` | 1,982 | Debug of Uf σz convention |
| `work/cnot_multibit.py` | 5,806 | Cⁿ-NOT via direct exp and Eq. (6) product form |
| `work/cnot_action_fid.py` | 3,269 | Permutation-fidelity metric for Cⁿ-NOT |
| `work/ghz_states.py` | 3,257 | GHZ via Jy², N=2..7 |
| `report/evidence/eq5_toffoli_results.json` | ~4 kB | Full K × N_ph × osc-state sweep results |
| `report/evidence/eq5_target_comparison.json` | ~600 B | Fidelity vs literal / Toffoli / Toffoli+correction |
| `report/evidence/eq5_typo_hypothesis.json` | ~300 B | Confirmed: `-σx3/(32K)` gives exact Toffoli |
| `report/evidence/eq6_grover_results.json` | ~4 kB | Eq. (6), Eq. (10), Grover-search full data |
| `report/evidence/grover_trajectory.json` | ~5 kB | Grover P(x₀) vs k, n=3..6 |
| `report/evidence/cnot_multibit_results.json` | ~1 kB | Cⁿ-NOT fidelities |
| `report/evidence/cnot_permutation_fidelity.json` | ~1 kB | Permutation-fidelity results |
| `report/evidence/ghz_states.json` | ~2 kB | GHZ generation via Jy² |
| `report/evidence/llm_judge.txt` | ~4 kB | LLM-judge verdict prompt + response (Argo Opus 4.7) |
| `report/REPORT.md` | 17,662 | Full narrative report with claims table |
| `report/REPORT.tex` | 8,808 | LaTeX section-by-section report |
| `report/brief.md` | (see below) | 1-paragraph replication summary |
| `report/attempt_log.md` | (see below) | Chronological what-I-did-what-worked log |
| `report/artifact_harvest.md` | (see below) | Public-artifact URLs and checksums |
| `report/workflow.md` | 4,609 | Workflow + tools + effort estimate |
| `report/artifacts_summary.md` | this file | Artifact inventory |
| `report/failure_analysis.md` | 5,412 | Failure modes and gap enumeration |
| `report/open_questions.json` | 6,468 | 5 open questions in the required {q, basis, next_steps} format |

## Provenance notes
- All Python source files were written by this replicator; no code was copied from any GitHub repository or reference implementation.
- The `extraction/marker.md` and `extraction/nougat.mmd` files were copied verbatim from a pre-existing sibling directory (`QC-quant-ph-0012055-multi-bit-gates-quantum-computing/`), which had been processed earlier for the same paper. This is the "pull from central corpus if parsed" path specified in the operating brief.
- All numerical fidelities in the report are directly readable from the evidence JSON files; no cherry-picking.
- No LLM code generation was used for the physics code; only for the final verdict pass.
