# LUCID replication — Turner et al. 2019, γ-H2AX biodosimetry of internal 137Cs

Replication of:

> Turner HC, Lee Y, Weber W, Melo D, Kowell A, Ghandhi SA, Amundson SA,
> Brenner DJ, Shuryak I. **Effect of dose and dose rate on temporal γ-H2AX
> kinetics in mouse blood and spleen mononuclear cells in vivo following
> Cesium-137 administration.** *BMC Mol Cell Biol.* 2019;20:13.
> [DOI: 10.1186/s12860-019-0195-2](https://doi.org/10.1186/s12860-019-0195-2)

**Verdict: REPLICATED · Coverage 9/10 · Agreement 9/10.**
See [`REPORT.md`](REPORT.md) for the full write-up.

## TL;DR

The authors built a closed-form γ-H2AX kinetics model
`F = b + k·A·t·exp(-α·A + 1 - (1+r·t)^p)`
and a Monte-Carlo procedure that inverts measured γ-H2AX fluorescence and
post-injection time into estimated injected 137Cs activity. They report
Pearson r = 0.857 (2–3 d window), AUC = 0.93 for low-vs-high activity
classification.

We rebuilt the model and the Monte-Carlo inversion from scratch in Python
using only the open-access paper and its 5 supplementary PDFs (digitized
Tables S2 and 1). We reproduce:

- The forward γ-H2AX kinetics curves (Fig. 4) — weighted SSR = 59 with the
  paper's verbatim parameters, residuals comparable to data SEMs.
- All four Pearson/Spearman correlations from Table 3 within ≈ 0.04 / 0.13.
- The spleen day-14 result essentially exactly (Pearson 0.866 → 0.870).
- ROC AUC = 0.84–0.85, inside the paper's 95 % CI (0.806–1.0).
- α (cell-death rate, MBq⁻¹) within 5 % of the paper's value.

The (r, p) pair of the stretched-exponential is non-uniquely identifiable
from 5 time points — both the paper's and our values give equivalent fits.

## Quick start

```bash
python3 code/use_paper_params.py    # forward + inversion using paper params
python3 code/replicate_turner.py    # full refit + MC + ROC pipeline
```

Outputs land in `figures/` and `results/`.

## Layout

| Path | Contents |
|------|----------|
| `paper.pdf` | The target paper |
| `data/Additional_file_{1..5}.pdf` | All 5 supplements (downloaded from Springer) |
| `data/{blood,spleen}_h2ax.csv` | Digitized Table S2 |
| `data/dose_table.csv` | Digitized Table 1 (committed dose & dose rate) |
| `code/replicate_turner.py` | Full refit + Monte-Carlo + ROC + figures |
| `code/use_paper_params.py` | Forward eval using paper's verbatim parameters |
| `figures/` | Replicated Fig. 4, Fig. 5, Fig. S2 (paper params and refit versions) |
| `results/` | Numerical summary tables (md + json) and per-point predictions |
| `REPORT.md` | Full replication report with side-by-side numbers |
| `PROGRESS.md` | Timestamped progress log |

## License / provenance

The paper and its supplements are published under CC BY 4.0
(http://creativecommons.org/licenses/by/4.0/). Replication code is original.
