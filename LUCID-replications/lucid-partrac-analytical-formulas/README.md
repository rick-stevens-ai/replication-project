# LUCID Replication — PARTRAC analytical DNA-damage formulas

This directory contains an analytical/figure-level replication of the paper represented by `source-paper.md`:

> Kundrát et al. 2020, *Scientific Reports* 10:15775, DOI `10.1038/s41598-020-72857-z`.

**Note:** the original task DOI (`10.3390/cancers11020205`) points to a different Cancers review. The markdown content is unambiguously the Kundrát Scientific Reports paper, so the replication uses the source content as truth and flags the DOI mismatch in `REPORT.md`.

## Scope

This is **not** a rerun of PARTRAC. PARTRAC is not public/runnable here. Instead, this implements the published analytical formulas and transcribed fitted parameters from Tables 1–2, then reproduces LET-dependent yield curves and headline numerical checks.

## Files

- `REPORT.md` — audit report and verdict
- `PROGRESS.md` — chronology and blockers
- `source-paper.md` — cached source markdown
- `code/formulas.py` — Eq. 1 and Eq. 2 implementations
- `code/parameters.py` — manually transcribed Table 1/2 parameters
- `code/run_replication.py` — driver for results and figures
- `results/summary.json` — headline checks
- `results/yield_grid.csv` — computed yield grid
- `results/table_excerpts.txt` — source excerpts for formulas/table context
- `figures/*.png` — reproduced analytical curves

## Rerun

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-partrac-analytical-formulas
python3 code/run_replication.py
```

Expected runtime: <10 seconds on laptop CPU.

Python dependencies: `numpy`, `matplotlib`.
