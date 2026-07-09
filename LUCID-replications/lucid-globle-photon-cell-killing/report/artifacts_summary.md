# Artifacts summary — GLOBLE photon cell-killing

Paper: Herr et al. 2014, PLoS ONE 9(1):e83923 (GLOBLE model). DOI 10.1371/journal.pone.0083923.
Verdict: **REPLICATED** (equation/parameter level, all 17 cell lines) — Claim 7 empirical overlay **BLOCKED (F2)**. Coverage 9/10, Agreement 9/10.

## 8-artifact standard status
| # | Artifact | File | Status |
|---|---|---|---|
| 1 | Original PDF | `artifacts/paper.pdf` (md5 4b7d8f78…) | present |
| 2 | Marker text | `paper.md` (Marker/Nougat-style, sha cb54cfea…) + `PARSER_PROVENANCE.md` | present (canonical merge lacks this DOI; local extraction used) |
| 3 | Nougat text | `extraction/nougat.mmd` | **stub** — no GPU parse; sha256 pointer recorded |
| 4 | LaTeX report | `report/REPORT.tex` (+ `open_questions_section.tex`) | present |
| 5 | Open questions | `report/open_questions.json` (5 × q/basis/next_steps) + `## Open Questions` in report | present |
| 6 | Workflow | `report/workflow.md` | present |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | present |
| 8 | Failure analysis | `report/failure_analysis.md` | present |

## Headline numerical results (traces)
- Claim A: ε_i < ε_c for 22/22 param sets; split-dose median HLT_i = 0.458 h (= paper exactly). → `results/repass/claim_A_table2.json`
- Claim B: 17/17 cell lines monotone dose-rate survival (>80 panels). → `results/repass/claim_B_dose_rate_all.json`, `figures/repass/dose_rate_all_cell_lines.png`
- Claim C: 5/5 split-dose lines recover. → `results/repass/claim_C_split_dose_all.json`
- Claim D: 11/11 dose-rate + 11/11 split-dose HLT_i match Table 2. → `results/repass/claim_D_table3.json`
- Claim E: high-DR max|Δln L| = 1.46e-2; low-DR = 1.02e-2 (tol 0.05). → `results/repass/claim_E_limits.json`
- Claim F: Eq.(8) identity, max rel err 2.80e-3. → `results/repass/claim_F_alpha_taylor.json`
- Pass-1: Fig-4 GLOBLE/LQ max|ΔG| ≈ 0.0019; Fig-6 LL plateau 2.41 h fit vs 0.60 h predicted.

## Preserved originals (untouched this pass)
REPORT.md, REPORT.pass1.md, PROGRESS.md, README.md, PARSER_PROVENANCE.md,
code/, results/, figures/, artifacts/.

## Friction tags
F1 (no author code), F2 (raw experimental points not distributed — blocks Claim 7),
F3 (Supplement File S1 missing), F8 (Fig-4 caption ε_i inconsistent with Eq. 8).
