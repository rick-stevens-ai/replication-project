# LUCID Replication — Qi et al. 2021 (Slow/Fast NHEJ)

Open independent replication of:

> Qi Y, Warmenhoven JW, Henthorn NT, Ingram SP, Xu XG, Kirkby KJ, Merchant MJ.
> **Mechanistic Modelling of Slow and Fast NHEJ DNA Repair Pathways Following
> Radiation for G0/G1 Normal Tissue Cells.** *Cancers* **2021**, *13*, 2202.
> doi:10.3390/cancers13092202

The original work uses **DaMaRiS** — a Geant4-DNA-based Monte Carlo agent
simulation with spatial CTRW sub-diffusion of DSB ends.

**2026-05-28 cleanup:** DaMaRiS *is* public; it has been ported to TOPAS-nBio
and lives at `github.com/topas-nbio/TOPAS-nBio` under `damaris/` and
`examples/damaris/`. The public DaMaRiS parameter files and example damage
input are cached in `artifacts/damaris/`. The paper's MDPI supplement (Tables
S1–S4, Figs S1–S8) is also cached in `artifacts/mdpi-supplement/`. What
*does* remain author-on-request is the raw in vitro foci/PFGE/comet data
used to fit Table 1 — those datasets were not aggregated in any public
repository.

This repository contains:

```
code/
  nhej_model.py          # SciPy ODE compartmental model (Model A & B)
  experimental_data.py   # Hand-digitised data from Figs 3, 4, 7
  figures.py             # Generates the three replication figures
logs/                    # Stdout from runs
results/                 # (figures + metrics live in figures/)
figures/
  fig_repair_kinetics_wt.png
  fig_deficient_cells.png
  fig_state_decomposition.png
  metrics.json           # Reduced-chi-square style metrics per figure
PROGRESS.md
REPORT.md
artifacts/
  damaris/                # public TOPAS-nBio DaMaRiS files (cached 2026-05-28)
  mdpi-supplement/        # cancers-13-02202-s001.zip + extracted PDF (cached 2026-05-28)
  nhej_semantic_scholar.pdf
README.md
```

## Run

```
cd code
python3 figures.py
```

Pure SciPy/NumPy/Matplotlib. CPU. Whole pipeline runs in <2 s.

## Replication scope

- **Reproduced (qualitative):** Model A (Parallel) plateaus with residual
  unrepaired DSBs at late times; Model B (Entwined) decays close to zero by
  24 h. Artemis-deficient B retains a clear residual; XLF-deficient B
  shows slowed repair. Pathway topology, all rate constants, and pathway
  branching probabilities follow the published Table 1.
- **NOT reproduced (data on request / spatial Monte Carlo):** DSB-end
  CTRW diffusion, gamma-H2AX foci spatial undercounting, full damage-input
  SDD geometry, the heterochromatin/euchromatin spatial chromatin model,
  Figure 5 (residual vs LET — requires LET-dependent damage input from
  Henthorn et al. track-structure model, not available openly), all
  per-cell-line χ²/DF statistics in Tables S1-S3.

See `REPORT.md` for the claim table, scoring, and limitations.
