# LUCID Replication — Ulyanenko et al. 2019

Replication of: **Ulyanenko et al., "Formation of γH2AX and pATM Foci in Human Mesenchymal
Stem Cells Exposed to Low Dose-Rate Gamma-Radiation"**, *Int. J. Mol. Sci.* 2019, **20**,
2645. doi:10.3390/ijms20112645

**Verdict:** REPLICATED — Coverage 8/10, Agreement 9/10. See [`REPORT.md`](REPORT.md).

## Quickstart

```bash
python3 code/digitize_from_tables.py     # recover absolute foci data from Tables 1-3
python3 code/make_figures.py             # reproduce Figures 1, 2, 3, 4
```

Outputs land in `results/digitized_tables.json` and `figures/*.png`.

## Key result

All three linear regression equations stated in the paper are reproduced to ≥3 decimal
places by re-fitting absolute foci data that we algebraically recovered from the I_REL and
K coefficient tables. The recovery is internally consistent (5 independent estimates of
the control mean agree to within ±0.1 foci/cell) and externally validated (refitted
intercepts and slopes match the paper).

Original data: `source.pdf`; extracted text: `source.txt`.
