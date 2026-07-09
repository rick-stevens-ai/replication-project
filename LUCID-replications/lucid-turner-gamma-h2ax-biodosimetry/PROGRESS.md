# PROGRESS — Turner et al. γ-H2AX biodosimetry replication

**Status:** done · REPLICATED · coverage 9/10 · agreement 9/10
**Started:** 2026-05-30 17:43 CDT
**Finished:** 2026-05-30 17:55 CDT
**Target paper:** Turner HC et al. *Effect of dose and dose rate on temporal γ-H2AX kinetics in mouse blood and spleen mononuclear cells in vivo following Cesium-137 administration.* BMC Mol Cell Biol 2019;20:13. DOI 10.1186/s12860-019-0195-2

## Log
- 17:43 — directory + skeleton created.
- 17:44 — extracted full paper text via `pdftotext -layout`.
- 17:45 — downloaded all 5 supplementary PDFs from Springer static-content.
- 17:46 — digitized Table S2 (blood + spleen γ-H2AX means ± SEM) and Table 1 (dose).
- 17:48 — implemented Eq. 1 forward model, weighted Nelder-Mead refit, Monte-Carlo CI sampling, F→A inversion, ROC scoring.
- 17:50 — first refit recovered α (0.242 vs paper 0.255) and produced excellent fit (weighted SSR 38 vs paper-params SSR 59 on same data); r/p showed the expected stretched-exponential degeneracy.
- 17:52 — added second script using paper's verbatim parameters; reproduced all four Table-3 correlations to within ~0.04 (Pearson) and ~0.13 (Spearman). ROC AUC 0.84 (inside paper's 95% CI 0.806–1.0).
- 17:54 — wrote REPORT.md, README.md, finalized PROGRESS.md and json summary.

## Deliverables (all present)
- `REPORT.md`            full replication report
- `README.md`            quickstart
- `PROGRESS.md`          this file
- `paper.pdf`            target
- `code/replicate_turner.py`        full refit + MC + ROC pipeline
- `code/use_paper_params.py`        paper-params verification
- `data/{blood,spleen}_h2ax.csv`    digitized Table S2
- `data/dose_table.csv`             digitized Table 1
- `data/Additional_file_{1..5}.pdf` original supplements
- `figures/fig4_{paper_params,replication}_blood.png`
- `figures/fig5_{paper_params,replication}_blood.png`
- `figures/figS2_replication_roc.png`
- `results/summary.md`, `results/paper_params_check.md`
- `results/blood_inversion.csv`, `results/headline.json`

## Notable findings
- α (cell-death parameter) matches paper to 5%.
- r and p in the stretched-exponential term are non-uniquely identifiable from 5 time points; the paper's reported values are not unique without additional constraints, but the *Q2 envelope* matches.
- Spleen day-14 correlation reproduces almost exactly (0.866 → 0.870).
- ROC AUC differs by 0.09 but is inside the paper's reported 95% CI.
