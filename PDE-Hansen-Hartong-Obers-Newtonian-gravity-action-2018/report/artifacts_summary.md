# Artifacts summary

Paper: Hansen, Hartong, Obers — "Action Principle for Newtonian Gravity"
(PRL 122, 061106, 2019; arXiv:1807.04765).
Directory: `PDE-Hansen-Hartong-Obers-Newtonian-gravity-action-2018/`.

---

## Primary sources
| File | Purpose |
|---|---|
| `paper.pdf` (staged on uicgpu at `~/replicate/hansen-newtonian-2018/`) | Original PRL preprint v2, md5 `15ce60ac1e1db7a0889275cb6b9a5220` |
| `paper.txt` | `pdftotext -layout` dump, 46,265 B / 422 lines |

## Verification scripts (`work/`)
| Script | Function |
|---|---|
| `verify_algebra.py` | Builds structure constants for type-II TNC algebra from paper eq. (11); auto-antisymmetrising bracket helper; exhaustive Jacobi scan at d=2,3,4; ideal/quotient checks |
| `verify_metric_compat.py` | Generic TTNC background (arbitrary lapse A(x^μ) and m_μ(x^μ), δ^{ij} spatial metric); checks ∇̄τ = 0, ∇̄h = 0, torsion identity of paper eq. (2); d=2,3 |
| `verify_poisson_reduction.py` | Flat NC background, m_μ = Φ δ_μ^0; symbolic Γ̄ and Ricci; verifies Poisson coefficient (d-2)/(d-1) at d=2,3,4 |

## Raw evidence (`report/evidence/`)
| File | Content |
|---|---|
| `algebra_output.txt` | Full stdout of Jacobi scan (5,420 triples total across d=2,3,4; 0 failures) |
| `metric_compat_output.txt` | Full stdout of ∇̄τ, ∇̄h, torsion checks (149 assertions total; 0 failures) |
| `poisson_output.txt` | Full stdout of Γ̄, Ricci, Poisson reduction at d=2,3,4; 0 failures |
| `judge_prompt.txt` | Neutral prompt sent to both LLM judges |
| `judge_response_gpt5.json` | Argo GPT-5 verdict: REPLICATED, 70% coverage |
| `judge_response_argo_claude-opus-46.json` | Argo Claude Opus 4.6 verdict: REPLICATED, 62% coverage |

## Reports (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Primary human-readable replication report (~14 KB) |
| `REPORT.tex` | LaTeX version + dedicated "Genuine critique" section |
| `open_questions.json` | 5 truly open research questions (grounded, not derivable from paper) |
| `workflow.md` | Stage-by-stage workflow reconstruction |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | What went wrong mid-replication, how it was resolved, lessons |

---

## Quantitative totals
- **Total symbolic assertions**: ~5,600 across all three test scripts.
- **Total failures**: 0.
- **Dimensions covered**: d = 2, 3, 4 (algebra); d = 2, 3 (metric compatibility); d = 2, 3, 4 (Poisson).
- **Jacobi triples verified**: 220 (d=2) + 1140 (d=3) + 4060 (d=4) = 5,420.
- **Metric-compatibility checks**: 9 + 27 + 9 (d=2) + 16 + 64 + 24 (d=3) = 149.
- **LLM judges**: 2, both free (Argo).
- **Elapsed replication time**: ~10 minutes on uicgpu single-thread.
- **Cost**: $0 (all uicgpu compute + Argo endpoints).

## Verdict
**REPLICATED.** All three testable core claims of the paper independently verified
by exhaustive symbolic computation; 2 free-endpoint LLM judges converge on
REPLICATED with exact agreement and very-high confidence.

## Untested items (honest bound of replication)
- Full variational derivation of eqs. (16–21) from paper eq. (12).
- Full gauge invariance of eq. (12) under type-II transformations of eq. (10).
- Derivation of type-II TNC from 1/c² expansion of GR (companion arXiv:1905.13723).
- Matter coupling beyond static point mass.
- Higher-derivative / boundary-term ambiguities of eq. (12).

The *result* of the crucial derivation (Poisson equation) IS tested;
only the derivation *path* is unverified.
