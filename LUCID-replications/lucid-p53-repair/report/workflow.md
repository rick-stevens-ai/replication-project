# Workflow — LUCID p53 / DNA-damage-repair replication

## Timeline

| Date | Actor | Step |
|---|---|---|
| 2026-05-28 morning | Ollie (subagent) | Retrieved LUCID paper PDF (open access, MDPI IJMS 23:11323); attempted supplement download from `/article/.../s1` → HTTP 403 |
| 2026-05-28 morning | Ollie | Retrieved Hat 2016 (PLOS Comp Biol) S1 Text with full reaction list, rate laws, rate constants (Tables A/B/C) |
| 2026-05-28 midday | Ollie | Wrote `code/p53_model.py` — 27-species ODE, Hat 2016 parameters verbatim; three degradation constants raised (`g6, g9, g19`) to compensate for omitted buffering chain |
| 2026-05-28 midday | Ollie | Wrote `code/run_experiments.py` — two-stage integration (24 h warmup + 600 s IR pulse + 72 h observation), doses ∈ {2, 4, 6, 8} Gy, `M ∈ {0.14, 0.5}` Gy |
| 2026-05-28 afternoon | Ollie | Generated `figures/fig4_timecourses_M0p5.png`, `fig4_timecourses_M0p14.png`, `fig5_TGFb_vs_dose.png`, `fig6_apoptosis_surrogate.png`; wrote `results/summary.json` |
| 2026-05-28 evening | Ollie | Recovered LUCID supplement via MDPI static CDN (`mdpi-res.com` path); `/s1` was bot-gated, not paywalled. Cached at `artifacts/mdpi-supplement/`. Cross-checked Tables S1–S3 against Hat 2016 |
| 2026-05-28 late | Ollie | Wrote `REPORT.md` with claim-by-claim table, coverage 6/8 qualitative, verdict PARTIAL |
| 2026-07-06 | Kukla (backfill subagent) | Backfilled `report/` bundle (this file, REPORT.tex, open_questions, artifacts_summary, failure_analysis) and `extraction/nougat.mmd` stub. No simulations re-run |

## Compute path

- CPU only, single MacBook (CherryRd, macOS 25.3.0, Python 3.14).
- SciPy 1.13 `solve_ivp` with LSODA (stiff/non-stiff switching for the mixed-timescale p53/Mdm2 loop).
- ~6 s wall-clock for all 4 figures.
- No GPU, no allocation, no paid endpoint.

## Tool chain

- **Model source:** independent Python transcription from Hat 2016 S1 Text; LUCID supplement used as cross-check only.
- **Solver:** SciPy LSODA (default rtol=1e-6, atol=1e-9; a few species need atol scaling).
- **Plotting:** Matplotlib 3.x, PNG output only.
- **PDF retrieval:** `curl` + user-agent header for MDPI static CDN.

## Reproduction recipe

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-p53-repair
python3 code/run_experiments.py
# outputs land in figures/ and results/summary.json
```

Tested with Python 3.14, NumPy 2.x, SciPy 1.13, Matplotlib 3.x.

## Handoff notes

- The `report/` bundle is the queue-standard artifact set; the top-level `REPORT.md` remains authoritative for narrative.
- The `artifacts/mdpi-supplement/extracted/ijms-1905291-supplementary.pdf` copy of LUCID's Tables S1–S3 is the cross-check anchor for anyone re-deriving the reaction set.
- Upgrading PARTIAL → REPLICATED requires the Bogdał 2013 Gillespie apoptosis gate (see open_questions.json Q1).
