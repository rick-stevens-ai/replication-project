# Artifacts summary — OSTI 1974586

Every file produced or consumed by this replication, with role and provenance.

## Source artifact (fetched)
| Path | Role | Provenance |
|---|---|---|
| `extraction/1974586.pdf` | OA source PDF | `https://www.osti.gov/servlets/purl/1974586`, MD5 `131ff7c062bfb6993df7c222f7aaae49`, fetched via `ssh uicgpu` proxy (CherryRd `curl` timed out) |
| `extraction/1974586.txt` | Layout-preserved text | `pdftotext -layout` on uicgpu (poppler); born-digital → no OCR needed |

## Compute scripts (work/)
| Path | Role |
|---|---|
| `work/replicate_tfim.py` | C1/C2/C3 free-fermion vs. dense-spin cross-check + C4 QAOA scan (single script, two entry points). Deterministic linear algebra; seeded Nelder-Mead for QAOA restarts. |
| `work/symmetry_averaging.py` | C5 mechanism test: two antiphase KW-related error signals, sin(φ/2) suppression identity, sweep over residual mismatch φ. |

## Evidence artifacts (report/evidence/)
| Path | Role | Consumed by |
|---|---|---|
| `report/evidence/results.json` | Per-L free-fermion + dense-spin energies, ff-vs-dense residual, error vs -4/π | REPORT.md §4 (C1/C2/C3 table); REPORT.tex |
| `report/evidence/symmetry_averaging_results.json` | Per-φ single-obs max err, averaged max err, orders reduced | REPORT.md §4 (C5 table); REPORT.tex |
| `report/evidence/run.log` | Raw stdout/stderr from replicate_tfim.py + symmetry_averaging.py | Provenance / rerunnability audit |
| `report/evidence/judge_verdict.txt` | Argo LLM-judge (`argo:gpt-5.2`) verdict (PARTIAL, concurring) | REPORT.md §6 assessment |

## Report artifacts (report/)
| Path | Role |
|---|---|
| `report/REPORT.md` | Canonical Markdown replication report — source of truth |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section (this backfill) |
| `report/open_questions.json` | 5 truly-open follow-up questions (non-Abelian generalization, mid-circuit-measurement trade-off, non-Markovian noise resilience, QITE coupling, fault-tolerant encoded critical-model simulation) |
| `report/workflow.md` | Deterministic reproducible pipeline (this backfill) |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest failure log + not-reproduced scope + provenance risks (this backfill) |

## Not produced (deliberate scope)
| Would-be artifact | Why absent |
|---|---|
| `work/dmera_matchgate_circuit.py` | C6 — full DMERA matchgate optimization pipeline. Requires paper's appendix circuit parameters + a full matchgate contractor. Out of scope for reference-physics replication. |
| `report/evidence/dmera_energy_scaling.json` | C6 — `exp(-4.89 D)` scaling curve. Would follow from the missing DMERA pipeline. |
| `report/evidence/dmera_translational_kw_average.json` | C7 — full 4-orders combined-averaging magnitude. Requires actual DMERA observable output, not the trig-identity mechanism check. |

## Numeric ground-truth items claimed (from REPORT.md)
- Infinite-volume `E/L = -4/π ≈ -1.2732395447` reproduced to `abs err 1.3e-13` at L=2×10⁶.
- Free-fermion vs dense-spin agreement: `‖ff - dense‖ < 1e-13` for L ∈ {4, 8, 12} (best: 8.9e-16 at L=4).
- CFT `1/L²` finite-size scaling: err(64) = 1.3e-4 → err(256) = 8.0e-6 → err(1024) = 5.0e-7.
- QAOA L=8 residuals: rel err 5.8e-2 (p=1), 2.9e-2 (p=2), 1.9e-2 (p=3), 4.0e-13 (p=4 = L/2, exact).
- KW-averaging suppression: 2.12 orders at φ=1°, 1.82 orders at φ=2°, 1.42 orders at φ=5° (analytic `|sin(φ/2)|`).

## Tool / environment fingerprint
- Python 3, NumPy 2.x, SciPy — CPU only.
- pdftotext (poppler) via uicgpu.
- Argo proxy `localhost:44497`, model `argo:gpt-5.2` (free endpoint).
- No paper source code, no author-supplied data files used beyond the analytic target -4/π and Eq. (3) of the paper.
