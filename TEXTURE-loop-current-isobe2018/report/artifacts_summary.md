# Artifacts summary

## Files
- `code/isobe2018_rg.py` — RG core (Eqs. 9-24), SciPy integrator.
- `code/run_checks.py` — 5 claim tests; writes work/results.json + figure.
- `code/PROVENANCE.md` — paper + shared-kernel provenance + scope decision.
- `work/results.json` — computed pass/fail + metrics for all 5 claims.
- `work/rg_flow_and_phase.png` — RG flow (cf. Fig 4c) + critical-scale vs nesting.
- `extraction/marker.md` — extraction method + extracted equations/claims.
- `report/REPORT.tex` (+ REPORT.pdf) — writeup.
- `report/open_questions.json` — 5 open questions.

## Claim results (computed)
| # | Claim | Metric | Verdict |
|---|-------|--------|---------|
| 1 | Eq.9: g14,g24,g44 do not flow | max|dg_i4/dy| = 0.0 over 500 random states | PASS |
| 2 | Sym dens-dens, no exch: MF no SC, RG makes d/p-SC | MF V_dSC=V_pSC=0; min V_dSC(RG) = -137 (<0) | PASS |
| 3 | Nesting d1->0: g22 grows, g42 shrinks | g22 0.5->6.6; g42 0.5->-43.5 | PASS |
| 4 | Weak nest->SC, strong->DW; Q- dominates Q0 | d1-=0.05 -> d-SC; d1-=0.45 -> CDW-; d1-=0.15,d2-=0.45 -> CDW- | PASS |
| 5 | No exch degeneracies s=f,d=p,CDW-=SDW-; exch lifts | deg=0 (all three); lifted d/p=0.8, CDW/SDW=1.2 | PASS |

**Total: 5/5 machine-checkable claims reproduced.**

## Scope note
The kagome loop-current shared kernel is OUT OF SCOPE for this paper's hot-spot
RG core and was deliberately not imported (see PROVENANCE.md / failure_analysis.md).
