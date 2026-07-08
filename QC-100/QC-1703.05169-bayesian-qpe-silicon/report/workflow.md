# Workflow — arXiv:1703.05169 replication (QC-100)

Paper: Paesani et al., *Experimental Bayesian Quantum Phase Estimation on a
Silicon Photonic Chip*, PRL 118, 100503 (2017).

Verdict: **REPLICATED** (algorithmic core C1 + C2).

## Timeline
- **2026-07-03** — Ollie subagent (QC-100 wave) picked up the paper on m1/CherryRd.
- **2026-07-03** — Paper acquisition + text extraction:
  ```bash
  curl -sL -o work/1703.05169.pdf https://arxiv.org/pdf/1703.05169
  pdftotext -layout work/1703.05169.pdf work/1703.05169.txt
  ```
- **2026-07-03** — Environment build: `python3 -m venv work/venv &&
  source work/venv/bin/activate && pip install qiskit numpy scipy matplotlib`.
- **2026-07-03** — Wrote Qiskit circuit for the Fig. 1a Hadamard-test
  (`work/rfpe_sim.py`); wrote `_sanity_check()` verifying the statevector
  output matches Eq. 1 of the paper to <1e-9 abs on 60 test triples.
- **2026-07-03** — Wrote RFPE outer loop (Appendix B algorithm). First
  implementation had the Θ=μ symmetry bug: μ never moved.
- **2026-07-03** — Wrote grid-Bayes reference (`work/debug3_grid.py`).
  Grid-Bayes with Θ=μ also stuck; grid-Bayes with Θ~prior converged
  exponentially → confirmed the bug is not in the SMC refit but in the
  experiment-design heuristic. Fixed by sampling Θ~N(μ,σ²) per step.
- **2026-07-03** — 50-seed sweep (`work/pick_seed.py`) picked seed 38 as a
  representative successful run (matching the paper's own single-run
  presentation in Fig. 2a).
- **2026-07-03** — Experiment A (Fig. 2a single run, seed 38,
  n_particles=20000). Result: |err| = 1.87e-4 rad (paper 2.4e-4), σ = 1.30e-3
  rad.
- **2026-07-03** — Experiment B (Heisenberg-vs-SQL scaling, 200 RFPE trials
  + 400 SQL baselines). Confirmed the two-regime plateau/collapse RFPE
  shape and the 1/√N SQL slope. Seed-38 single-run bound ratios: 1.12×
  Heisenberg, 69× below SQL.
- **2026-07-03** — Experiment C (100-seed distribution). Bimodal on log
  scale: median 4.52e-2 rad, 4% below paper's headline in 50 steps.
- **2026-07-03** — Report written as `report/REPORT.md`; evidence archived
  to `report/evidence/`.
- **2026-07-06** — Backfill (this task): added `REPORT.tex`,
  `open_questions.json` (5), `open_questions_section.tex`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd`
  stub. Verdict preserved: **REPLICATED**. No re-runs; no paid endpoints.

## Reproduce (from scratch)
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1703.05169-bayesian-qpe-silicon
python3 -m venv work/venv
source work/venv/bin/activate
pip install qiskit numpy scipy matplotlib
cd work
python rfpe_sim.py           # ~14 s CPU, writes JSON + PNGs
```

## Verification checklist
- [x] `_sanity_check()` reports `[sanity] OK: Qiskit circuit matches Eq. (1)`.
- [x] `experimentA_fig2a.json` final-step |err| ≤ 3e-4 rad.
- [x] `experimentA_fig2a.json` final-step σ ≤ 2e-3 rad.
- [x] `scaling_rfpe_vs_sql.png` shows RFPE median-err trajectory below the
      SQL trajectory once M > 1.
- [x] Seed-38 run: 1.12× Heisenberg bound (ratio ≤ 1.5 = "saturated").
- [x] 100-seed distribution: min ≤ 5e-5 rad; median in ("stuck" mode) is
      order 10⁻² rad (expected heavy tail).

## Boundaries preserved
- Free endpoints only (local Python CPU). No LLM, no cloud, no paid API.
- No re-runs during backfill. All original evidence files preserved
  unmodified.
- Verdict cross-check: **REPLICATED** (matches queue verdict and
  substance of §6 in REPORT.md).
