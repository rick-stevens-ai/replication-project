# Artifacts Summary — oh2026 (arXiv:2605.21124)

**Paper:** "Observation of spin-free interatomic orbital angular momentum in a chiral crystal" (Oh et al.)
**Verdict:** REPLICATED (model headline — chirality-locked itinerant OAM to machine precision)

## Inventory

### Compute (pre-existing, not regenerated)
- `work/reproduce.py` — self-contained pure-NumPy reproduction (~1 s CPU).
- `work/results.json` — machine-readable verdicts + paper_value vs reproduced.
- `work/COMPUTE_NOTES.md` — model description, self-verdict table, chirality convention, out-of-scope notes.
- `work/figs/bands.png` — 3-band structure of the RH helical chain.
- `work/figs/oam_texture.png` — bands colored by L_Itin_x (sign texture tracks dE/dk).
- `work/figs/chirality_flip.png` — L_Itin_x RH vs LH (mirror-image, opposite sign).

### Report (this phase)
- `report/REPORT.tex` (+ `REPORT.pdf` if compiled) — full write-up: summary, claims table, method, results, critique, open questions, verdict.
- `report/open_questions.json` — 5 grounded open questions (Q1–Q5).
- `report/workflow.md` — environment + step-by-step reproduction.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — what reproduced, what is out of scope, the chirality-transform bug lesson.
- `report/method_extract.md` — pre-existing method extraction (claims C1–C5, feasibility).

## Key numbers
| Quantity | Value |
|---|---|
| Bands | 3 (nondegenerate) |
| Bandwidth | 4.0 t |
| Frac. BZ split (01 / 12) | 0.995 / 0.9975 |
| OAM sign-match (per band) | 1.0 / 1.0 / 1.0 |
| \|corr(L, dE/dk)\| (per band) | 0.998 / 0.999 / 1.000 (mean 0.999) |
| Chirality flip corr | 1.00 |
| Frac. k-points flipped | 1.00 (100%) |
| Wall time | 1.082 s |

## Claim-level outcome
- **C1** 3-band chiral-chain structure — REPRODUCED (Y)
- **C2a** L_Itin_x locks to sign(dE/dk) — REPRODUCED (Y)
- **C2b** L_Itin_x flips with chirality (CIOS) — REPRODUCED (Y)
- **C2/C5** DFT+Wannier bulk-Te OAM magnitudes — OUT OF SCOPE
- **C3** CD-ARPES — OUT OF SCOPE (beamline)
- **C4** SARPES — OUT OF SCOPE (beamline)
