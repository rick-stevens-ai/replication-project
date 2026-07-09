# lucid-dna-repair-kinetics-doserate-rbe

Independent replication of:
> Liew, H. et al. *Impact of DNA Repair Kinetics and Dose Rate on RBE
> Predictions in the UNIVERSE.* Int. J. Mol. Sci. 23, 6268 (2022).
> [doi:10.3390/ijms23116268](https://doi.org/10.3390/ijms23116268)

See `REPORT.md` for the verdict and the full numeric comparison.

## Requirements
- Python ≥ 3.10
- numpy, matplotlib  (`pip install numpy matplotlib`)

## Reproduce

```bash
cd code/
# 1. R_TD50(dose-rate) — Table 3 / Fig 4 left panel (rat spinal cord)
python3 fig4_left_rtd50.py            # ~5 min on a 2024 laptop
python3 plot_rtd50.py                 # makes ../figures/fig4_left_RTD50_replication.png

# 2. Saturation gain vs dose — Table 2 (DU145, photon-only lower bound)
python3 fig12_photon_trend.py         # ~2 min
```

All numerical outputs land in `../results/*.json`; logs in `../results/*.log`.

## What's in here

- `code/universe_photon.py` — core: independent re-implementation of the
  UNIVERSE photon-only repair-kinetics sub-model from Liew et al. 2022,
  Sec 5.2 and Eq 5. Pure NumPy. ~14 kB, ~350 LOC.
- `code/fig4_left_rtd50.py` — reproduces the R<sub>TD50</sub>(dose-rate)
  factor (Table 3 4th column, Fig 4 left panel) and prints the rate-by-
  rate comparison vs the paper.
- `code/fig12_photon_trend.py` — reproduces the photon-only piece of the
  Table 2 saturation-gain trend (2, 6, 12, 24 Gy).
- `code/plot_rtd50.py` — overlay plot.

## What is NOT in here, and why

- **Ion-beam side (Kiefer–Chatterjee track structure, proton/helium RBE).**
  The paper does not print the K<sub>p</sub> normalization constant
  for Eq 8, nor the Friedrich-2015 LET-dependent DSB-yield boost (cited
  but not written). N<sub>dom</sub> is not printed either (I assume 3200).
- **FLUKA Monte-Carlo HIT beamline SOBP geometry** for Fig 4 middle/right
  and Fig 5. Closed and proprietary to HIT.

A fuller replication would require collaboration with the authors or
access to ref [9] (Liew 2021 IJROBP) code and HIT beamline files.

## Verdict (one-liner)

**PARTIAL REPLICATION. Strong quantitative agreement (<1.3 % MAD) on the
photon-side R<sub>TD50</sub> claim that this paper introduces; full SOBP
RBE benchmark not reproducible from paper alone (closed Monte Carlo).**
