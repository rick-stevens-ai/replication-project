# Artifacts Summary — QC-100 W3 · LCU / Multi-Product Formulas

## On-Disk Inventory

### Top level
- `REPORT.md` — original human-readable replication report (kept in place, load-bearing).
- `paper.md` — extracted paper summary / key equations.
- `replicate.py` — the replication driver (numpy + scipy.linalg.expm; Lemma 2 circuit,
  $S_1$/$S_2$ product formulas, Richardson MPFs, order-slope fits, near-unitarity).
- `results.json` — machine-readable output of `replicate.py` (source of every number in
  `REPORT.md`).

### `report/` (added by backfill 2026-07)
- `REPORT.tex` — LaTeX version of REPORT.md with an expanded, honest Critique section
  and `\input{open_questions_section.tex}` at the end.
- `open_questions.json` — bare JSON list of 5 open-question objects
  (`q`, `basis`, `next_steps`).
- `open_questions_section.tex` — same content as `open_questions.json`, formatted as a
  LaTeX section for direct inclusion.
- `workflow.md` — how the replication was produced end-to-end.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what this replication does NOT establish.

### `extraction/`
- `nougat.mmd` — stub (Nougat not run; see `workflow.md`).

## Provenance
- Numeric claims in `REPORT.md` / `REPORT.tex` all trace to `results.json`, which is
  produced deterministically by `replicate.py`.
- LaTeX Critique in `REPORT.tex` and `failure_analysis.md` add editorial content beyond
  the original REPORT.md — both files are honest about the boundary between "verified
  numerically" and "asserted in the paper but not re-run here."
- No re-runs or new numerics were performed during backfill; the underlying `results.json`
  is untouched.

## Verdict (preserved from REPORT.md)
**REPLICATED** — Coverage 8/10, Agreement 10/10. Lemma 2, Theorem 3, MPF order lift,
coefficient normalization, and near-unitarity all verified to machine precision on 1–2
qubit test problems. Not exercised: asymptotic gate-count constants, $S_4$ baseline
comparison, larger-$n$ scaling, physically-motivated Hamiltonians, noise.

## Headline-Exercised Test
The paper's headline is: **LCU + Richardson-MPF beats Suzuki-Trotter formulas in error
scaling for Hamiltonian simulation.** The load-bearing sub-claims (the LCU circuit
correctness, the κ definition, the raised convergence order) are all directly numerically
exercised in this replication and match theory to machine precision / two decimal orders.
The extra headline claim about asymptotic *gate-count constants* is not independently
re-derived, but the *mechanism* (order lift) that produces it is.
