# PROGRESS — Acheva et al. 2017 (3D organotypic skin / NF-κB / COX-2)

- **Target.** Acheva A, Schettino G, Prise KM. *Pro-inflammatory signaling in a
  3D organotypic skin model after low LET irradiation — NF-κB, COX-2
  activation, and impact on cell differentiation.* Front Immunol 8:82 (2017).
  DOI: 10.3389/fimmu.2017.00082.
- **PDF.** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/909f825af8f0e6cbcc2d321d52daab6e756845f1.pdf`
  (archived in this folder as `source.pdf`).
- **Output dir.** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-skin-inflammation-nfkb-cox2/`

## Timeline

| Time (CDT) | Step |
|---|---|
| 18:09 | Spawned, scaffolded `code/`, `results/`, `figures/`, status=running |
| 18:10 | Archived PDF locally, extracted full text with `pdftotext -layout` |
| 18:11 | Triage — confirmed paper is wet-lab dominant; identified Figs 1, 2, 7 as the only quantitative bar-chart targets and Methods Eq for 2^-ΔΔCT as auditable equation |
| 18:12 | Rendered all 14 pages at 200 dpi; digitized Figs 1, 2A/B, 7A/B via vision pass |
| 18:13 | Wrote `code/digitized_figures.py` with means/SEMs/N |
| 18:14 | Wrote `code/replicate_stats.py` — synthetic samples preserving mean+SEM, scipy.stats.tukey_hsd, scipy.optimize.curve_fit 4PL, 2^-ΔΔCT identity check |
| 18:15 | Ran analysis; all four reported Fig 1 stars recovered qualitatively; PGE2 fold-change 6.4× vs claimed 6.5×; sc-236 IC50 = 16.8 µM; Bay 11-7085 IC50 = 3.8 µM |
| 18:15 | Wrote `code/make_figures.py`, regenerated overlay PNGs |
| 18:16 | Wrote `README.md`, `REPORT.md`, this file; status=done |

## Verdict

**SPOT-CHECK** — coverage 3/10 (paper is mostly wet-lab), agreement on audited
content 9/10. See `REPORT.md` for details.

## Deliverables

- `README.md` — repo overview, how-to-reproduce, honesty disclaimer
- `REPORT.md` — full verdict, what we replicated, what we did not, observations
- `PROGRESS.md` — this file
- `source.pdf` — local archive of the open-access paper
- `code/digitized_figures.py`
- `code/replicate_stats.py`
- `code/make_figures.py`
- `results/spotcheck_results.json`
- `figures/fig1_digitized_overlay.png`
- `figures/fig2_dose_response_fits.png`
- `figures/fig7_pge2_overlay.png`
- `figures/pages/p-01.png … p-14.png` — 200 dpi page renders used for digitization
- `figures/extracted/img-000.png … img-006.png` — raw figure images from pdfimages
