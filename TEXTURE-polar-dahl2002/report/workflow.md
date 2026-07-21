# Workflow — textures-polar-dahl2002 (Dahl 2002, cond-mat/0211693)

## 1. Acquire
Old-style arXiv id requires the bare-id URL form:
```
curl -sL https://arxiv.org/pdf/cond-mat/0211693 -o dahl2002.pdf
```
Result: 327 KB, header `%PDF-1.2` — valid.

## 2. Parse
```
pdftotext dahl2002.pdf work/textures-polar-dahl2002.txt   # 1317 lines
```

## 3. Recipe
Identified paper type = critical review / phenomenology (no simulation in paper).
Selected ONE testable headline — Dahl's loop-width-vs-frequency diagnostic
(parsed lines 201–206) — recorded in `report/evidence/replication_recipe.json`.

## 4. Physics (from scratch)
Built `code/dahl2002_lgd_tdgl.py`: a 0D Landau–Ginzburg–Devonshire polarization
model, F(P)=½aP²+¼bP⁴+⅙cP⁶−E(t)P, evolved by overdamped TDGL /
Landau–Khalatnikov dynamics. Drove with E(t)=E0·cos(ωt) and measured P–E loop
width (coercive field) vs. ω for a double-well (a<0, bistable) and a single-well
nonlinear-lossy potential (a>0). Provenance: LGD form + LK update adapted from
`ollie_tdgl_phasefield_polar_skyrmion_kernel.py` (Ollie).
Runner: `/home/stevens/comfyui-env/bin/python`. Runtime ~1.7 s.
SAVE-EARLY: `work/dahl2002_result.json` written after each frequency.

## 5. Compare + score
Low-frequency switching window (ω≤0.2): double-well loop-area slope = −0.02
(frequency-independent ✓), single-well lossy slope = +1.06 (∝ frequency ✓).
Double-well retains Ec≈0.42 as ω→0; lossy Ec≈0.009 (~40× smaller). Matches
Dahl's prediction quantitatively → REPLICATED.

## 6. Artifacts (8)
extraction/marker.md, extraction/nougat.mmd, report/REPORT.tex,
report/open_questions.json, report/workflow.md, report/artifacts_summary.md,
report/failure_analysis.md, plus evidence copies (result JSON + code + figure +
recipe).

## 7. Re-judge
`judge_verdict.py` with argo:claude-opus-4.5, njudges=1 (see artifacts_summary).
