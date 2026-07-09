# Workflow — Cordoni 2023 (Entropy 25:1322) LUCID replication

## Paper

- Cordoni F. G., *On the Emergence of the Deviation from a Poisson Law in Stochastic Mathematical Models for Radiation-Induced DNA Damage: A System Size Expansion*, **Entropy 25 (2023) 1322**.
- DOI: [10.3390/e25091322](https://doi.org/10.3390/e25091322).
- Local copy: `artifacts/paper.pdf`.

## Set / provenance

- Set: **LUCID** (LUCID-100 replication corpus)
- Corpus source markdown: `uicgpu:/data/stevens/lucid-corpus-extracted/LUCID-papers/b60a4945a319af54.md`
- Replicator: Ollie (OpenClaw subagent, depth 1)
- Host: CherryRd (macOS, 2024 Apple silicon)
- Replication date: 2026-05-29
- Backfill date: 2026-07-06 (this report)
- Verdict: **REPLICATED** — preserved from the original REPORT.md; not re-evaluated in this backfill.

## What kind of paper this is

- **Theoretical.** Analytic derivation (van Kampen system-size expansion of the GSM² master equation) plus small-scale numerical illustration (three figures, single parameter set).
- No author code released; *Data Availability* states "No new data have been created."
- Consequence for replication: pure math + implement-from-equations + Monte-Carlo cross-check.

## Workflow (chronological)

1. **Paper ingest** (`b60a4945a319af54.md` from LUCID corpus).
2. **Manual equation extraction** — Eqs. 1 (MME), 6 (rescaled clustering rate), 11 (deterministic MKM ODEs), 14 (linear FPE), 16 (moment ODEs), 18 (integral identity for c_vv), 22 (OU representation), 23 (non-truncated FPE).
3. **Implementation** — `code/gsm2_model.py`:
   - Direct-method Gillespie SSA for the three-reaction CTMC.
   - LSODA integrator for the mean-field ODE (Eq. 11).
   - Joint mean-field + moment ODE for (c_ξξ, c_ξv, c_vv) (Eq. 16).
   - Euler-Maruyama on 3010-point sub-grid for OU sample paths (Eq. 22), Cholesky of the diffusion matrix.
4. **Driver script** — `code/run_replication.py`:
   - 20,000 SSA paths, 20,000 OU paths, 301 time points on t ∈ [0, 1.5] a.u.
   - Parameters exactly matched to paper Sec. 4: x0=100, y0=0, r=4.0, a=0.1, b_tilde_K=0.01.
   - Seeds: SSA `rng(20260529)`, OU `rng(420)`.
5. **Numerics dump** — `results/histogram_summary.json`, `results/moments_vs_time.csv`, `results/summary.json`.
6. **Figures** — `figures/fig1_histograms.png` (three t-slices, X and Y marginals, LNA overlay), `figures/fig2_moments_vs_time.png` (means and covariance trajectories), `figures/fig3_sample_paths.png` (SSA vs OU paths).
7. **Claim table** — hand-audited 13 claims (A1-A2, B1-B8, C1-C4).
8. **Verdict + REPORT.md** — REPLICATED, 13/13 verified.
9. **Backfill (this report)** — 2026-07-06:
   - `report/REPORT.tex` (full LaTeX report with honest critique)
   - `report/open_questions.json` + `report/open_questions_section.tex` (5 truly-open questions, grounded in paper re-read)
   - `report/workflow.md` (this file)
   - `report/artifacts_summary.md`
   - `report/failure_analysis.md`
   - `extraction/nougat.mmd` (stub; corpus markdown already exists)

## Tools / versions

| Tool | Version | Notes |
|---|---|---|
| Python | 3.11 | CherryRd system Python |
| NumPy | ≥ 1.17 (PCG64 default BitGenerator) | seeds are stable |
| SciPy | ≥ 1.10 | `scipy.integrate.solve_ivp` (LSODA) |
| Matplotlib | 3.x | figures |
| No LLM used in the numerics phase | — | pure CPU code |
| Argo (localhost:44497, key=`stevens`) | — | only used for the backfill prose (this report), FREE endpoint |

**Compute:** CherryRd only. No GPU. No HPC.

## Work estimate

| Phase | Approx. time |
|---|---:|
| Read paper, extract equations | ~2 h |
| Implement SSA + ODEs + OU | ~3 h |
| Drive + tabulate + plot | ~1 h |
| Original REPORT.md writing | ~1 h |
| **Original replication total** | **~7 h wall** (2026-05-29) |
| Backfill (this batch, 6 report files + 1 extraction stub) | ~1 h wall (2026-07-06) |
| **Grand total** | **~8 h human wall** |

**Cost:** \$0 throughout (local CPU + free Argo endpoint).

**Wall-clock runtime of the full replication script:** ~11 s on 2024 iMac (Gillespie phase dominates at ~7 s).

## Reproducer

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-stochastic-poisson-dna-damage/
python code/run_replication.py
```

Regenerates:
- `results/summary.json`
- `results/moments_vs_time.csv`
- `results/histogram_summary.json`
- `figures/fig1_histograms.png`
- `figures/fig2_moments_vs_time.png`
- `figures/fig3_sample_paths.png`

Bit-identical outputs on NumPy ≥ 1.17 (PCG64 default; seeds 20260529 for SSA, 420 for OU).

## Reproducer for the LaTeX report

```bash
cd report/
pdflatex REPORT.tex
pdflatex REPORT.tex     # second pass for TOC / cross-refs
```

Requires: TeX Live 2023+ (any standard `pdflatex` with `amsmath`, `booktabs`, `hyperref`, `longtable`).

## What was NOT done in this backfill (out of scope by design)

- No re-run of `run_replication.py` (Rick's rule: preserve existing results).
- No new parameter sweep (Q1-Q5 next-steps are proposals, not executions).
- No GPU parse of paper.pdf (corpus markdown already exists at `uicgpu:/data/stevens/lucid-corpus-extracted/LUCID-papers/b60a4945a319af54.md`; the extraction stub points at that + the SHA-256 of the local paper.pdf).
- No hcodex / hclaude / paid endpoint calls. Only local CPU + free Argo.
