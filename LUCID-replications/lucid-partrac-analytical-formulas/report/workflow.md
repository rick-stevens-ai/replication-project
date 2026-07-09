# Workflow — PARTRAC Analytical Formulas Replication

## Goal
Reproduce the analytical yield formulas in Kundrát et al., *Sci Rep* 10:15775 (2020),
"Analytical formulas representing track-structure simulations on DNA damage induced by
protons and light ions at radiotherapy-relevant energies," from the paper text alone.

Explicit non-goals for this pass:
- Do NOT rerun the underlying PARTRAC Monte Carlo (closed code, unavailable).
- Do NOT independently re-derive coefficients from raw MC points (points not published).
- Do NOT alter published Table 1 / Table 2 entries.

## Inputs
- `source-paper.md` — cached paper text, treated as authoritative.
- Table 1 (SB/SSB fit coefficients) and Table 2 (DSB / DSB clusters / DSB sites fit
  coefficients) as transcribed from the paper.
- Equations 1 and 2 as printed in the paper.

## Steps executed

1. **Identity check.** Compared task DOI (`10.3390/cancers11020205`) with the on-disk
   source. On-disk source is `10.1038/s41598-020-72857-z`. Logged as friction tag F8
   and proceeded against the on-disk source.

2. **Formula transcription.** Encoded Eq. 1 (SB/SSB) and Eq. 2 (DSB family) into
   `code/formulas.py`, treating `N.A.` parameters exactly as the paper prescribes
   (drop the corresponding term).

3. **Parameter transcription.** Copied Tables 1 and 2 verbatim into
   `code/parameters.py`, keyed by (ion, damage class).

4. **Curve regeneration.** `code/run_replication.py` sweeps LET over each ion's
   fitted range (log-spaced, 200 points) and evaluates SB, SSB, DSB, DSB cluster and
   DSB site yields. Outputs written to `results/yield_grid.csv` and summary values
   for the paper's headline low-LET baselines to `results/summary.json`.

5. **Figure regeneration.** Matplotlib scripts reproduce the fit-line curves shown in
   Figs. 1–4 of the paper (fig1_sb, fig2_dsb, fig3_dsb_sites, fig4_dsb_sites_components).
   Raw PARTRAC symbol overlays are omitted because the underlying MC points are not
   available.

6. **Headline audit.** Ten paper-level claims scored REPLICATED / PARTIAL / BLOCKED
   in `REPORT.tex`. Two headline low-LET numbers (SB≈170, SSB≈156, DSB≈6.8–7)
   confirmed to match to the transcribed p1 coefficients.

7. **Anomaly logging.** During evaluation the H-proton DSB-site row was observed to
   grow without bound past its fitted range because Table 1's overkill parameters
   are `N.A.`, in tension with the paper's ~15 sites/Gy/Gbp peak claim. Logged as an
   open question rather than silently patched.

## Compute footprint
- CPU-only, ~seconds on m1. No GPU, no network, no MC.

## Reproducibility
- All code is deterministic; no random seeds required.
- Re-running `python code/run_replication.py` regenerates `results/` and `figures/`.

## What a full replication would additionally require
- PARTRAC source or a public reimplementation.
- The raw simulation-point tables behind Figs. 1–5 (per ion, per damage class,
  per LET).
- An independent chromatin geometry consistent with the paper's fibre model, or
  a documented substitution.
