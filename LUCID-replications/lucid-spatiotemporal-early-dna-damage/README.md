# lucid-spatiotemporal-early-dna-damage

Replication of the kinetic model from:

> Tobias F, Löb D, Lengert N, Durante M, Drossel B, Taucher-Scholz G, Jakob B (2013).
> *Spatiotemporal Dynamics of Early DNA Damage Response Proteins on Complex DNA Lesions.*
> PLOS ONE 8(2): e57953. doi:10.1371/journal.pone.0057953  (CC-BY)

## TL;DR

The paper has a fully-specified ODE-based kinetic model of the early DDR
(MRN/ATM/H2AX/MDC1) with 9 reactions and ~10 rate constants. The Supporting
Information S1 gives all numerical parameters. I re-implemented the model in
Python from scratch and reproduce the paper's Figure 11 plus all four
headline qualitative claims, with ~9% signal-RMS and ~20% τ½-RMS quantitative
agreement against digitized data points.

**Verdict: REPLICATED (numerical-model component). Agreement 8/10. Coverage 7/10.**

See `REPORT.md` for the full write-up.

## Quick start

```bash
cd code
python3 lucid_model.py           # smoke test of the ODE model
python3 figure11_replication.py  # reproduce paper Figure 11
python3 quantitative_check.py    # quantitative agreement table
python3 figure_overlay.py        # model vs digitized data
```

Dependencies: `numpy`, `scipy`, `matplotlib`.

## Layout

- `source.pdf` — paper PDF (CC-BY)
- `supplements/` — all 6 PLOS supplements (downloaded from open-access URL)
- `code/` — the model and analysis scripts
- `figures/` — generated comparison plots
- `results/` — JSON outputs of the numerical comparison
- `PROGRESS.md` — stage log
- `REPORT.md` — full replication report

## What is *not* replicated

The wet-lab beamline microscopy and FRAP experiments themselves. Those would
require heavy-ion beam time at GSI Darmstadt and the raw image stacks are
not published. The replication is limited to the closed-form numerical model
the paper specifies in its supplement.
