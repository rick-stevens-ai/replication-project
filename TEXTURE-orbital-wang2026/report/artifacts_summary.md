# Artifacts Summary — wang2026 (arXiv:2607.15228)

**Verdict:** PARTIAL

## Inventory

### Extraction
- `extraction/marker.md` — full paper text (pdftotext fallback), incl. complete
  Supplemental Material (slave-spin renormalization S1-S4, susceptibility S5-S8,
  RKKY S9-S14). Self-contained recipe except for Ref[49] hoppings.

### Method
- `report/method_extract.md` — claims C1-C5, method class, computational recipe,
  feasibility, compute recommendation (nuc13 CPU).

### Compute (already run — NOT recomputed in this phase)
- `work/reproduce.py` — pure-NumPy J_perp-J1-J3-J1' bilayer model: Luttinger-Tisza
  ordering vector, J3/J1 sweep, linear spin-wave dispersion.
- `work/results.json` — per-claim reproduced values:
  - C3: Q = (0.509, 0.509)π  (paper 0.508π) — MATCH
  - C4: J3/J1 = 2.42, Q shifts monotonically — MATCH (qualitative)
  - C5: 2 branches — MATCH; acoustic softening 0.023 meV at 0.509π — MATCH;
        bandwidth 172.9 meV vs paper ~80 meV — NO MATCH (2.16x).
- `work/dispersion.json` — acoustic_meV[], optical_meV[], kdist[], path labels.
- `work/figs/spinwave_dispersion.png` — acoustic+optical branches, softening at Q.
- `work/figs/Q_vs_J3overJ1.png` — ordering vector vs J3/J1 (frustration trend).
- `work/figs/luttinger_tisza_map.png` — J(q) landscape, minimum on (q,q) diagonal.

### Report (this phase)
- `report/REPORT.tex` (+ `REPORT.pdf` if pdflatex available) — paper summary,
  claims table C1-C5 (paper vs reproduced vs match), method, results table,
  per-claim worked/didn't, honest critique (bandwidth 2.16x convention gap +
  C1/C2 out-of-scope), Open Questions Q1-Q5, VERDICT PARTIAL.
- `report/open_questions.json` — 5 grounded open questions with basis + next_steps.
- `report/workflow.md` — env (numpy/scipy, CPU ~min) + pipeline.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — the bandwidth factor-2 convention gap and the
  Ref[49]-hoppings out-of-scope analysis.

## Trace (provenance chain)
paper PDF (arXiv:2607.15228)
  -> extraction/marker.md (pdftotext)
  -> report/method_extract.md (C1-C5 identified; C1/C2 flagged needing Ref[49])
  -> work/reproduce.py (self-contained subset C3/C4/C5 from stated J*S values)
  -> work/results.json + work/dispersion.json + work/figs/*.png
  -> report/{REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md}

## Reproduced vs paper (headline)
| Claim | Paper | Reproduced | Match |
|---|---|---|---|
| C3 ordering Q | 0.508π | 0.509π | YES |
| C4 J3/J1 dominance + Q shift | >1, monotonic | 2.42, monotonic | YES |
| C5 two branches | ac+opt | 2 | YES |
| C5 acoustic softening at Q | yes | 0.023 meV @ 0.509π | YES |
| C5 bandwidth | ~80 meV | 172.9 meV | NO (2.16x) |
| C1/C2 slave-spin + RKKY | — | out of scope (needs Ref[49]) | N/A |
