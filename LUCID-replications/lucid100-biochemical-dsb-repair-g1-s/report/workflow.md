# Workflow — Taleei & Nikjoo 2013 Biochemical DSB Repair Replication (Pass 2)

## Pipeline

1. **Metadata retrieval.** EuropePMC + S2 record for DOI 10.1016/j.mrgentox.2013.06.004 → `evidence/europepmc.json`. Openness verified: paywalled (`isOpenAccess:N`, `openAccessPdf.status="CLOSED"`).
2. **Parser fallback (no PDF body).** Elsevier paywall + Cloudflare 1020 on companion routes → substituted Belov 2015 INIS preprint E19-2014-39 (already on local disk from sibling `lucid100-belov-dsb-repair-pathways-slot66/`). Extracted Table A.1 (rate constants) and Table A.2 (LET-dependent complex-fraction) via `pdftotext` → `evidence/companion-papers/belov2015_extracted_text.txt`.
3. **Claim enumeration.** 10 claims (C1–C10) extracted from abstract + inferred pass-gates; documented in Pass-2 REPORT.md.
4. **Model implementation.** 12-compartment mass-action ODE in Python; extends Pass-1 9-compartment skeleton with 3 heterochromatin compartments (`DSB_h, Ku_h, Syn_h`). File: `code/repass/taleei_nikjoo_2013_repass.py`.
5. **Simulation runs.** All 6 Pass-2 claims (C5–C10) executed on single CherryRd Apple-Silicon CPU core with SciPy LSODA. Outputs to `results/repass/*.csv/*.json`.
6. **Comparators.** Digitised Beucher 2009 / Kuhne 2000 / Riballo 2004 (WT + CJ179) from `lucid-slow-fast-nhej/code/experimental_data.py` (ultimately Qi et al. 2021 Figs 3a/3b/7a).
7. **Reporting.** Per-claim table + quantitative pass-gates in REPORT.md; visual overview `figures/repass/repass_overview.png`.

## Tools / Versions

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.x (system) | ODE integration + reporting |
| NumPy | (managed venv) | numerics |
| SciPy | (managed venv, `solve_ivp` / LSODA) | stiff ODE solver |
| matplotlib | (Agg backend, no GUI) | figures |
| pdftotext (poppler) | system | Belov 2015 PDF extraction |
| EuropePMC REST | live | metadata |
| S2 Graph API | live (S2_API_KEY from Keychain) | openness check |
| curl / wget | system | fetch attempts |

## Work Estimate (actual)

| Phase | Wall time |
|---|---|
| Pass 1 metadata + parser fallback | ~10 min |
| Pass 1 model implementation (9-compartment) | ~15 min |
| Pass 1 writeup | ~10 min |
| Pass 2 model extension (+3 het compartments, C5–C10) | ~20 min |
| Pass 2 simulations (all 6 claims) | ~1.5 s CPU |
| Pass 2 writeup | ~25 min |
| **Total wall time** | **~1.5 h human-time, ~2 s compute** |

Compute: single CPU core on CherryRd Mac Studio (Apple Silicon). No GPU, no cloud, no paid endpoint, no author contact, no journal-side PDF.

## Reproducer

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-biochemical-dsb-repair-g1-s/

# Verify metadata (requires S2_API_KEY in env)
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.mrgentox.2013.06.004?fields=openAccessPdf,isOpenAccess" \
  -H "x-api-key: $S2_API_KEY"

# Pass-2 simulation (all 6 claims C5-C10)
python code/repass/taleei_nikjoo_2013_repass.py

# Outputs land in:
#   results/repass/c5_artemis_kinetics.csv
#   results/repass/c6_let_dependence.csv
#   results/repass/c7_data_fit_chi2.json
#   results/repass/c8_heterochromatin_kinetics.csv
#   results/repass/c9_mass_conservation.json
#   results/repass/c10_sensitivity.csv
#   figures/repass/repass_overview.png

# All pass-gates re-verifiable by eyeballing REPORT.md tables against results/repass/*.
```

## Dependencies

- Belov 2015 INIS preprint PDF: mirrored at `evidence/companion-papers/belov2015_inis_iaea.pdf` for self-contained provenance (originally at `../lucid100-belov-dsb-repair-pathways-slot66/artifacts/`).
- Digitised experimental data: `../lucid-slow-fast-nhej/code/experimental_data.py`.

## Non-Reproducible Elements

- The paper PDF body is paywalled at Elsevier. Rate constants come from Belov 2015 Table A.1, not the paper's own Table 1. This is a permanent one-step-removed provenance gap barring interlibrary loan or author contact.
