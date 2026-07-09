# Workflow — Turner 2019 γ-H2AX Biodosimetry Replication

## Pipeline (as executed)

1. **Ingest paper + supplements.** `paper.pdf` (1.36 MB) + Additional_file_{1..5}.pdf
   (five supplements, all open-access from BMC Mol Cell Biol).
2. **Digitize tables to CSV.**
   - `data/blood_h2ax.csv` (25 rows) ← Additional file 2, Table S2 (blood).
   - `data/spleen_h2ax.csv` (25 rows) ← Additional file 2, Table S2 (spleen).
   - `data/dose_table.csv` (20 rows) ← main-text Table 1.
   Values are group-mean fluorescence ± SEM (n=8/point); individual mouse
   fluorescences are NOT published.
3. **Forward evaluation with paper's verbatim parameters.**
   `python3 code/use_paper_params.py` → prints weighted SSR (59.1 blood) and
   writes `figures/fig4_paper_params_blood.png`, `figures/fig5_paper_params_blood.png`,
   `results/paper_params_check.md`.
4. **Independent refit + Monte-Carlo inversion + ROC.**
   `python3 code/replicate_turner.py` (~30 s) →
   - Weighted Nelder-Mead refit of (k, α, r, p) on blood + spleen means.
   - 30,000 MC parameter draws; 16 accepted inside joint 95% CI.
   - F→A inversion by numeric root-find for each accepted draw.
   - Pearson/Spearman per time window; ROC low-vs-high classifier.
   - Writes: `results/summary.md`, `results/blood_inversion.csv`,
     `results/headline.json`, `figures/fig4_replication_blood.png`,
     `figures/fig5_replication_blood.png`, `figures/figS2_replication_roc.png`.

## Tools / versions

- Python 3.11 (macOS system + conda `sci` env).
- numpy 1.26, scipy 1.11 (`optimize.minimize` Nelder-Mead; `stats.pearsonr`,
  `stats.spearmanr`, `optimize.brentq` for F→A inversion).
- matplotlib 3.8 for figures.
- No GPU. No paid endpoint. No external data download. No author contact.
- Runtime end-to-end: **~30 s** on M-series MacBook.

## Data provenance

- 100% public. BMC Mol Cell Biol Vol. 20 Article 13, open-access CC-BY.
  DOI 10.1186/s12860-019-0195-2.
- All 5 supplements (Additional_file_1..5.pdf) live in `data/`.
- Paper PDF sha256: `6c72c427da495edd70062c0edb8fd350f6e5f0810d5cfdd1f26a4d910edc5b8e`.

## Work estimate

- **Human effort (as executed):** ~4 hours (2 h digitize supplements +
  2 h implement/verify Eq. 1 fitter and MC inversion).
- **Compute:** ~30 s total on laptop, no GPU.
- **Backfill effort (this pass, 2026-07-06):** ~10 min — paper re-read
  + LaTeX report + honest critique + 5 open questions. No re-run of sims.

## Reproducer (canonical)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-turner-gamma-h2ax-biodosimetry/
python3 code/use_paper_params.py    # ~2 s, verbatim-params reproduction
python3 code/replicate_turner.py    # ~30 s, full refit + MC + ROC
# Outputs: results/summary.md, results/headline.json, figures/*.png
```

Zero external dependencies at run time. Every input is in `data/`.

## What backfill did NOT do

- Did not re-run the simulator (per Rick's 2026-07-06 rule on this pass).
- Did not compute new figures; existing PNGs in `figures/` are preserved.
- Did not fabricate individual-mouse variance data that the paper does
  not publish.
- Did not run a GPU-based nougat parse of paper.pdf; a stub with sha256
  is placed at `extraction/nougat.mmd` for parser bookkeeping only.
