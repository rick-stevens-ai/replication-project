# Progress — Matsuya et al. 2019 (LUCID100 W1 slot 3)

## 2026-06-09 — Ollie first-pass (subagent)

### What I tried

1. **Located the campaign record** in `LUCID100_SOLID_MASTER_QA.tsv` (rank 34, Wave 1, KEEP).
2. **Mirrored the main PDF** from `Dropbox/XFER/LUCID-replication-targets/` into the project dir as `paper.pdf` (sha256 captured in `ARTIFACT_MANIFEST.md`).
3. **Extracted main text** with `pdftotext -layout` → `paper.txt` (701 lines, all references and Table 1 captured cleanly).
4. **Scraped the article landing page** at nature.com to locate the supplementary file URL (no `web_fetch` cookies issue once we used the rendered landing HTML).
5. **Downloaded supplement** `41598_2019_45960_MOESM1_ESM.pdf` (1.7 MB, sha256 in manifest) from `static-content.springer.com`, extracted text → `supplement/supplement.txt` (420 lines).
6. **Searched both PDFs** for code/data deposit pointers: `grep -i (github|zenodo|figshare|availab|reposit|source code)` — confirmed **none exist**. The paper relies on Table 1 + Eqs (1)–(10) for full model specification.
7. **Implemented the IMK forward model** from the published equations in `src/imk_model.py`:
   - `gamma_from_yD()` — domain-energy conversion using yD/(ρπr_d²).
   - `lea_catcheside_F()` — Eq (3a), with Taylor expansion for numerical stability at small (a+c)T.
   - `survival_TE_continuous()` — Eq (2).
   - `survival_TE_fractions()` — Eq (1), arbitrary dose-time profile (vectorized cross-term sum).
   - `survival_NT()` — Eq (5).
   - `survival_total_*()` — Eq (6) combining TE × NT for in-field / out-of-field cells.
   - Table 1 parameter datasets `AGO_MF, AGO_UF, DU145_MF, DU145_UF`.
8. **Smoke-tested the model** (`python3 src/imk_model.py`): F factor recovers correct limits (F→1 at small (a+c)T, F→0 at large), single-dose survivals are in physically reasonable ranges, and all three central qualitative claims (protective effect, reduced SLDR in AGO MF, similar DU145 MF/UF) are reproduced numerically.
9. **Regenerated figures** (`python3 src/reproduce_figures.py`): saved `figures/fig3_dose_response.png`, `figures/fig4_dose_rate.png`, plus CSV dumps in `data/`.
10. **Wrote** `README.md` (overview, citation, claims, acceptance criteria, layout, run instructions), `ARTIFACT_MANIFEST.md` (provenance, hashes, scope decision), and `REPORT.md` (first-pass verdict).

### Acceptance results

All six first-pass acceptance criteria (A1–A6) pass. See `REPORT.md` and `README.md` for the numeric table.

### Next actions

- **(Wave 2, optional)** Digitize experimental data points from Figs 2–6 using WebPlotDigitizer; add χ² comparison against regenerated curves.
- **(Wave 2, optional)** Independent MCMC parameter refit on the digitized data; check Table 1 reproducibility within stated s.d.
- **(Wave 2, optional)** Add Fig 5 (split-dose vs Ghita 2015) and Fig S5/S7/S8 (clinical dose-delivery regimens, scattered-photon TE-only check, McGarry 2011 cross-check) regenerations. The forward model already supports arbitrary dose-time profiles via `survival_total_fractions`.
- **(Wave 2, blocked unless author contact authorised)** No raw clonogenic counts or flow-cytometry data are publicly accessible, so a true wet-data re-analysis is impossible without contacting the authors. Per task instructions we did **NOT** contact authors.

### Compute

All work was local on CherryRd. No heavy compute was needed — the forward model runs in <1 s for the entire Fig 3 + Fig 4 grid. No job plan required.
