# Biochemical DSB-repair model for mammalian cells in G1 and early S phases of the cell cycle

LUCID100 Wave-1 replication slot **10** (master rank 41, Tier A, score 19).

## Paper

- **Title:** Biochemical DSB-repair model for mammalian cells in G1 and early S phases of the cell cycle
- **Authors:** R. Taleei, H. Nikjoo
- **Affiliation:** Radiation Biophysics Group, Department of Oncology-Pathology, Karolinska Institute, Stockholm
- **Year / venue:** 2013 / Mutation Research/Genetic Toxicology and Environmental Mutagenesis 756(1-2):206-212
- **DOI:** [10.1016/j.mrgentox.2013.06.004](https://doi.org/10.1016/j.mrgentox.2013.06.004)  ·  **PMID:** 23792210
- **OA status:** **CLOSED** (Elsevier paywall, no PMC/preprint, no Karolinska open repo). Source PDF listed in `LUCID100_SOLID_MASTER_QA.tsv` is actually the Qi et al. 2021 supplement (which cites this paper) — the master TSV link is mislabelled. See `PROGRESS.md` §"State after first pass" for the correction.

## What is in this folder

| File | What it contains |
|---|---|
| `README.md` | This file. |
| `PROGRESS.md` | Run log & open blockers. |
| `FIRST_PASS_REPORT.md` | Verdict, claim-by-claim acceptance table, limitations. |
| `artifacts/ARTIFACT_MANIFEST.md` | Inventory of all evidence used. |
| `artifacts/pubmed_abstract.txt` | Cached PubMed abstract + editorial comment refs. |
| `artifacts/semantic_scholar.json` | S2 record (citations, refs, OA status). |
| `artifacts/unpaywall.json` | Unpaywall record confirming closed access. |
| `artifacts/SHA256SUMS.txt` | SHA-256 of every artifact/code/result/figure file. |
| `code/taleei_nikjoo_2013_minimal.py` | Minimal independent compartmental-ODE reimplementation (9 states, NHEJ + MMEJ, G1/early-S). Smoke driver included. |
| `results/smoke_summary.json` | JSON with WT/Artemis-def/Lig4-def/Lig3-def/0.5-2-4 Gy snapshots. |
| `figures/fig_smoke_kinetics.png` | Two-panel summary plot. |
| `logs/`  | (Empty; smoke output written to stdout, captured in this README's "Reproducibility" block.) |

## Quick reproduce

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_WAVE1_LAUNCH_QA/lucid100-biochemical-dsb-repair-model-for-mammalian-cells-in-g1-and-early-s-phases-
python3 code/taleei_nikjoo_2013_minimal.py
# -> writes results/smoke_summary.json + figures/fig_smoke_kinetics.png
```

Requires only `numpy`, `scipy`, `matplotlib` (already in CherryRd's `python3`). No GPU, no HPC.

## Verdict

> **PARTIAL** — qualitative kinetic behaviour reproduced (biphasic WT, dose-linear, Artemis-def residual, Lig4 KO ≈ 95% unrepaired, MMEJ-only-loss ≲ 10%, high-complex-DSB slowdown). **No claim-by-claim Figure agreement** because the paper PDF is paywalled and we are not allowed to contact the authors. Next-step list in `FIRST_PASS_REPORT.md` §8.

## Cross-references inside the LUCID workspace

- **`lucid-slow-fast-nhej/`** — Qi et al. 2021 NHEJ ODE replica. Same kinetic skeleton; the parameter values used here are the values that group also adopts.
- **`lucid-medras-mc/`** — McMahon Medras Monte Carlo (independent NHEJ implementation), useful sanity comparison.
- **`lucid-dsb-repair-history-review-triage/`** — Berthel 2019 DSB-repair history review; already triaged as no-go.
