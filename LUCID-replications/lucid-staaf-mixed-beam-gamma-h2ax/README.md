# Replication: Staaf et al. 2012 — Mixed-Beam γ-H2AX Foci

LUCID replication of *Gamma-H2AX foci in cells exposed to a mixed beam of X-rays
and alpha particles* (Staaf et al., **Genome Integrity** 3:8, 2012).
DOI: [10.1186/2041-9414-3-8](https://doi.org/10.1186/2041-9414-3-8).

**TL;DR:** REPLICATED (PARTIAL), 7/10. RBE values, additivity prediction, and
the headline "large-foci delay" finding (Fig 5B) are all recovered from
digitized figure data, to within ~5% on values and ~10% on slopes. See
[REPORT.md](REPORT.md) for full details.

## Reproduce

```bash
cd code/
python3 replicate.py        # ~1 second; emits results/ and figures/
```

Requires only `numpy`, `scipy`, `matplotlib`.

## What's here

| File | Purpose |
|---|---|
| `REPORT.md` | Full replication report with verdict |
| `PROGRESS.md` | Stepwise progress log |
| `staaf2012.pdf` / `staaf2012.txt` | Original paper + text extract |
| `data/digitized_data.py` | All figure points visually digitized from PNG renders |
| `code/replicate.py` | Linear fits, RBE, additivity check, large-foci delay test, plots |
| `results/replication_results.json` | Machine-readable replication output |
| `figures/*.png` | Replicated dose-response, kinetics, and Fig 5 delay plots |

## Key results

| Claim | Reported | Replicated |
|---|---|---|
| RBE_α (total IRIF, slope ratio) | 0.76 ± 0.52 | **0.74 ± 0.19** ✅ |
| RBE_α (large foci, slope ratio) | 2.54 ± 1.11 | **2.41 ± 1.13** ✅ |
| α particles per nucleus, 0.27 Gy / 60 s | 3.57 ± 0.68 | **3.40 ± 0.65** ✅ |
| Additivity for total IRIF (all 3 mixed doses) | within SD | **within SD** ✅ |
| Large-foci delay: obs LF area << pred at 0.5 h | p<0.001, ~50% deficit | **~50% deficit recovered** ✅ |

## Caveats

* **No tables, no supplementary data**: all numerical inputs were digitized
  from figures using a vision model. ~5–10% uncertainty on point values.
* P-values in our delay test are larger than the paper's (no raw per-experiment
  data available for paired tests), but effect sizes match.
* No author contact, no paid endpoints, all data public per LUCID gates.
