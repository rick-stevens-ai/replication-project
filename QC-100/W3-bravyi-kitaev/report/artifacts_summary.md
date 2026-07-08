# Artifacts Summary — QC-100 W3 Bravyi-Kitaev

## Top-level (original W3 run — preserved as-is)
| File | Purpose | Evidence it carries |
|---|---|---|
| `REPORT.md` | Original replication report | Human-readable summary of every check performed and the REPLICATED verdict. |
| `paper.md` | Paper reading notes | Extracted Pauli coefficients (Eqs. 79/80) and encoding definitions used by `replicate.py`. |
| `replicate.py` | Independent numpy reimplementation | Reproduces β_n, π_n, P/U/F sets, JW and BK operators, H2 Hamiltonians, spectra, and Trotter-step gate counts. |
| `results.json` | Machine-readable results | Every number cited in the report is a field here — makes the claims auditable. |

## `report/` (backfill, 2026-07-06)
| File | Purpose |
|---|---|
| `REPORT.tex` | TeX version of the report with a genuine critique section explicit about what was and was not exercised. |
| `open_questions.json` | Five truly-open questions with concrete next steps (bare JSON list). |
| `open_questions_section.tex` | TeX version of the same. |
| `workflow.md` | Step-by-step method, environment, and what was skipped. |
| `artifacts_summary.md` | This inventory. |
| `failure_analysis.md` | Honest critique — gaps, caveats, and open holes. |

## `extraction/` (backfill)
| File | Purpose |
|---|---|
| `nougat.mmd` | Extraction stub (no full nougat pass performed on the source PDF in this backfill). |

## Headline evidence chain
1. `replicate.py` builds β_n from scratch → matches paper's binary-grouping recipe.
2. `replicate.py` derives P/U/F → passes structural invariants (update sets odd-only, flip sets empty for even j).
3. Anticommutation exact to 0.0 (JW and BK) → algebraic correctness.
4. BK and JW H2 spectra agree to 4.4e-16 → encoding-independent physics recovered (kills the bit-ordering bug class).
5. Trotter-step gate counts: **BK 30 sq / 44 CNOT, JW 46 sq / 36 CNOT** — match paper **exactly**.
6. Locality vs n: JW {3,7,15,31,63}, BK {2,3,4,5,6} — O(n) vs O(log n) reproduced with exact functional form, not just scaling.

## Verdict
**REPLICATED.** Headline exercised: gate counts match digit-for-digit and cross-encoding spectra match to machine precision — the two strongest possible tests the paper supports.
