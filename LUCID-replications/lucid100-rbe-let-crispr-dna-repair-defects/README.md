# LUCID100 #63 — RBE/LET in CRISPR-edited DNA-repair-defective cells

**Paper.** Guerra Liberal FDC, Parsons JL, McMahon SJ. *"Most DNA repair defects do not modify the relationship between relative biological effectiveness and linear energy transfer in CRISPR-edited cells."* **Medical Physics** 51(1):591–600, 2023 (issued online 2023-09-27).
**DOI.** [10.1002/mp.16764](https://doi.org/10.1002/mp.16764) · **PMID** 37753877 · **License:** CC-BY 4.0 (hybrid OA).
**LUCID100 rank/wave.** #63, Wave 4, Tier A, priority 15.
**Worktype.** simulation/model replication.

## TL;DR

CRISPR-Cas9 RPE-1 knockouts of TP53, ATM, DCLRE1C (Artemis), BRCA1, LIG4, and PRKDC (DNA-PKcs) were exposed to X-rays, low-LET protons (~2.5 keV/µm, mid-SOBP), high-LET protons (~10 keV/µm, distal end), and 241Am alpha particles (129.3 keV/µm). Clonogenic survival was fit to the linear-quadratic (LQ) model; RBE was computed from mean inactivation dose (MID) ratios; sensitizer enhancement ratio (SER) was the WT/KO MID ratio. 53BP1/γH2AX foci kinetics were fit to single-exponential decay. Headline conclusion: **RBE scales approximately linearly with LET (per-genotype R² ≈ 0.99), and most repair defects do _not_ modify the RBE/LET slope**, with the exception of LIG4 KO where overkill at high LET depresses RBE.

## Folder layout

```
artifacts/
  paper_birmingham_submitted.pdf      # Birmingham OA mirror (publishedVersion)
  paper_birmingham.txt                 # pdftotext output, used for digitization
  crossref.json, openalex.json         # bibliometadata
  rbemodels_upstream/                  # sjmcmahon/RBEModels (same senior author)
    RBEModels.py                       # 13 phenomenological proton RBE/LET models
    rbeAnalysis.py                     # analysis driver
data/
  paper_reported_rbe.csv               # RBE and SER values transcribed from paper text/Fig 2
  paper_reported_let.csv               # LET values per radiation quality
scripts/
  smoke_rbe_let_fit.py                 # minimal LQ + MID + RBE-vs-LET regression smoke
  upstream_models_demo.py              # plots Carabe/McNamara/Wedenberg RBE(LET) vs paper WT
figures/
  smoke_rbe_vs_let.png
  upstream_models_vs_paper_wt.png
docs/
  FIRST_PASS_REPORT.md                 # verdict + reproducibility ledger
PROGRESS.md
README.md
```

## Sources of truth

- Source-of-truth manifest: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` row 63.
- Primary artifact (OA submitted version): University of Birmingham institutional repo `https://pure-oai.bham.ac.uk/ws/files/207466192/mp.16764.pdf`.
- Authoritative final version (gated by Cloudflare to bots): `https://onlinelibrary.wiley.com/doi/full/10.1002/mp.16764` — human download recommended for SI.
- Upstream code (same senior author, _not cited in this paper_ but topically aligned): https://github.com/sjmcmahon/RBEModels (4 KB, two Python files, no LICENSE), https://github.com/sjmcmahon/Medras-MC (used in sibling LUCID100 replication).

## Data/code availability per paper

> "All data generated or analyzed during this study are included in this published article and its supplementary information file."

No GitHub, Zenodo, OSF, Dryad, or figshare repository is referenced. No statistical software code is released (Prism 9 used for fitting). The supplementary information file (which holds the per-cell 53BP1 % repair table and the survival data tables) is hosted on Wiley behind the same Cloudflare gate that blocks automated retrieval; it must be retrieved manually for full-fidelity replication.

## Status

See `docs/FIRST_PASS_REPORT.md` and `PROGRESS.md`.
