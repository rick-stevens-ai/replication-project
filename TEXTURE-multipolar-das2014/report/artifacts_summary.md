# Artifacts summary — Das (2014) SODW replication

All paths absolute under
`/home/stevens/textures-100/corpus/textures-multipolar-das2014/`.

## The 8 deliverable artifacts
1. **extraction/marker.md** — full paper text, `INTERIM: pdftotext fallback`
   header (marker unavailable in this environment).
2. **extraction/nougat.mmd** — same text as `.mmd`, `INTERIM: pdftotext fallback`
   header (nougat unavailable in this environment).
3. **report/REPORT.tex** — LaTeX replication report: claim, method (Eqs. 2/7/10),
   results table, PARTIAL assessment, kernel credit.
4. **report/open_questions.json** — exactly 5 questions, each
   `{question, why_it_matters, next_step}`, plus a top-level `next_steps` array.
5. **report/workflow.md** — end-to-end workflow + reproduce command + results table.
6. **report/artifacts_summary.md** — this file.
7. **report/failure_analysis.md** — the 502-interrupted prior run, the collapsed-gap
   bug, the fix, and remaining physics gaps.
8. **report/evidence/** — copied result JSON + from-scratch code:
   - `report/evidence/sodw_meanfield.py` — the mean-field solver.
   - `report/evidence/das2014_result.json` — full numerical output.
   - `report/evidence/replication_recipe.json` — the recipe (pre-existing).

## Primary result
- `work/das2014_result.json` (SAVE-EARLY canonical copy; mirrored to evidence/).

## Headline numbers (model vs paper)
- Delta0 = 6.15 meV (paper 5-10 meV) ✓
- Th_model = 17.9 K (paper 17.5 K) ✓ (close)
- Vc ~ 0.30 eV (paper V ~ 0.6 eV) ~ right order ✓
- FS spectral-weight loss ~6% (paper ~40%) ✗ under-reproduced
- Entropy release ~0.006 kB ln2 (paper ~24% R ln2) ✗ under-reproduced
- Zeeman Bc ~106 T (paper ~35 T) ✗ overshoot (static estimate)

**Verdict: PARTIAL** — gap magnitude + Th + interaction scale reproduced; extensive
FS/thermodynamic fractions and the field scale require the DFT Fermi surface
(scoped out).

## Credit
`ollie_multipolar_stevens_landau_kernel.py` (Ollie multipolar Stevens/Landau kernel).
