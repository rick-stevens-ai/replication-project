# Workflow — Tobias et al. 2013 replication

## Pipeline

1. **Triage & source acquisition**
   - Fetch paper PDF from PLOS ONE (CC-BY, open access).
   - Fetch all 6 supplements (Figures S1–S4 TIFFs, Table S1 DOC, File S1 DOC).
   - Extract body text via `pdftotext -layout` → `source.txt`.
   - Convert the two supplement DOCs to text via macOS `textutil`.
   - Convert Figure TIFFs → PNG for later digitization.
   - Provenance recorded in `PARSER_PROVENANCE.md`.

2. **Claim enumeration**
   - Manually read paper + supplements; enumerate every testable claim
     (arithmetic, ODE-model, tabular, wet-lab) in `CLAIMS.md`.
   - Tag each: `COV` (covered in pass-1), `NEW` (added in re-pass), or
     `BLOCKED` (unreproducible without unpublished artifact).

3. **Model re-implementation**
   - Re-implement the 9-reaction / 13-species ODE system from File S1
     specification alone (no reference to prior code) in
     `code/lucid_model.py`.
   - Use every published parameter as-is; no re-fitting.
   - Integrator: `scipy.integrate.solve_ivp(method='LSODA',
     rtol=1e-8, atol=1e-3, max_step=1.0)`.

4. **Figure reproduction**
   - `code/figure11_replication.py` reproduces the four panels of
     Figure 11 → `figures/figure11_replication.png`.
   - `code/quantitative_check.py` compares model output to digitized
     Fig-S1 points (panels A and L) → `results/quantitative_check.json`.
   - `code/figure_overlay.py` visualizes model+data overlay.

5. **Extended claim scripts (re-pass, 2026-06-23)**
   - `c3_dsb_fluence_arithmetic.py`  → A3
   - `c4_diffusion_arithmetic.py`   → A4, A5, A6
   - `c5_tableS1_trends.py`         → C1, C2, C3
   - `c6_model_extended_claims.py`  → B5, B6, B7, B8
   - `c7_mdc1_diffusive_influx.py`  → B9
   - Each script writes JSON under `results/cN_*.json` for
     resume-safety.

6. **Report assembly**
   - `REPORT.md` (Markdown), `REPORT.tex` (LaTeX, this pass).
   - `open_questions.json` + `open_questions_section.tex` for
     LaTeX inclusion.

## Tools / versions

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | model + scripts |
| numpy | 1.26 | arrays |
| scipy | 1.11 | LSODA integration, Spearman ρ |
| matplotlib | 3.8 | figure generation |
| pdftotext | poppler 24.x | body text extraction |
| textutil | macOS built-in | DOC → text |
| ImageMagick `convert` | 7.1 | TIFF → PNG |
| LaTeX (pdflatex) | TeX Live 2024 | report typesetting |

No GPU used. No network required for the replication scripts themselves
(paper + supplements fetched once, stored under `source.pdf` and
`supplements/`). No seeded RNG dependence.

## Work estimate

- Triage + supplement collection: 0.5 h
- Claim enumeration + `CLAIMS.md`: 1.5 h
- Model re-implementation (`lucid_model.py`): 3 h
- Figure-11 reproduction script: 1 h
- Digitization + quantitative check: 1 h
- Re-pass extended claim scripts (6 files): 3 h
- Report writing (Markdown + LaTeX pass): 2 h
- Backfill pass (this): 0.5 h
- **Total: ~12.5 h** for one competent replicator.

## Reproducer (one-shot)

From the dir root:

```bash
# 1. Regenerate the headline figure
python code/figure11_replication.py

# 2. Regenerate quantitative check
python code/quantitative_check.py

# 3. Regenerate all re-pass claim JSONs
python code/c3_dsb_fluence_arithmetic.py
python code/c4_diffusion_arithmetic.py
python code/c5_tableS1_trends.py
python code/c6_model_extended_claims.py
python code/c7_mdc1_diffusive_influx.py

# 4. Overlay
python code/figure_overlay.py

# 5. Rebuild LaTeX report
cd report/
pdflatex REPORT.tex
pdflatex REPORT.tex  # 2nd pass for cross-refs
```

Total wall-clock on a modern laptop: **~3 minutes**.

## Free-endpoint hygiene

No LLM / no paid API was called in producing the numerical results.
Any LLM-assisted writing (this backfill report) used the Argo proxy
`localhost:44497` (key `stevens`, free per Rick's 2026-05-26 standing
rule) exclusively.
