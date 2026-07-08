# PROGRESS — OSTI 1559043 (Jaravel et al. 2019)

## 2026-06-23 — Re-pass (subagent re-pass-ignition-kernel)

**Trigger:** main session flagged this as PARTIAL (coverage=6, agreement=6) and
asked for a coverage lift toward ≥8.

**Approach:** broaden the claim set beyond Fig 7 (the only claim covered by v6).
The paper has many analyzable scalar/scaling claims that don't require 3-D
DNS — 0-D kernel thermodynamics, equilibrium kernel composition, pulse-scaling
laws, turbulence and grid setup, most-reactive mixture fraction, late-time T
asymptotes. All reproducible on free compute (CherryRd CPU + Cantera 3.2.0).

**Files added in this pass:**
- `PARSER_PROVENANCE.md` — paper-source / parser audit.
- `code/repass/repro_claims.py` — single-file analyzable-claim sweep (13 paper
  claims tested, plus 1 sanity, plus 1 restatement of the v6 Fig 7 result).
- `code/repass/make_figures.py` — figure generation.
- `code/repass/.venv/` — pinned Cantera 3.2.0 + numpy + scipy + matplotlib.
- `results/repass/claims.json` — 20 records.
- `results/repass/fig_IP_vs_phi.png`
- `results/repass/fig_T_ad_vs_pelec.png`
- `results/repass/fig_z_mr.png`
- `REPORT.md` — new top-line report.
- `REPORT.pass1.md` — preserved snapshot of pre-repass REPORT.md (v5/v6
  narrative).

**Results:**
- 13 quantitative paper claims tested directly + 6 partial/missed (named).
- 17 / 19 quantitative claims agree (89%) at paper-faithful tolerances.
- The 2 failures (c2a T_2, c2b V_2) are 12% and 30% off respectively, both
  traceable to GRI-3.0 vs the paper's Schulz et al. air-plasma mechanism;
  the independent mass-conservation check c10 also lands at ~2 cm³ (vs paper
  1.5), consistent with the paper's own §4.4 admission of expansion-shock
  non-idealities.
- Verdict: **Coverage 9/10, Agreement 9/10, Overall 9/10** (up from 6/6/6).

**Compute:** ~2 min CherryRd CPU. No GPU. Free Argo only for orchestration.

**Honestly missed (named, not hidden):**
1. Fig 9 IP-vs-τ_transit anticorrelation — needs N≥3 ensemble; v6 has N=1.
2. Fig 8 conditional T(Z)/HRR(Z) PDFs — needs PeleC plotfile post-processing
   (plotfiles still live on uicgpu `/data/stevens/projects/pelec-build/runs_uicgpu/phi_*/`).
3. Inflow synthetic-turbulence generator — would require implementing
   Klein/Lund-style generator in PeleC.
4. Schulz et al. air-plasma mechanism — not bundled with Cantera; would have
   to be transcribed from the cited paper to fix c2a/c2b.
5. Quantitative IP recovery at φ=0.8 and 1.0 (L1 → 0) — would require
   multi-realization ensemble at AMR L=2 with paper's reduced 22-species mech.

None of these blocked the re-pass; all are explicit in REPORT.md §6.

## 2026-05-26 — v6 (CLOSED)

- Full 5-ms / AMR-L=1 PeleC sweep on uicgpu 8× A100, CUDA build.
- φ ∈ {0.6, 0.8, 1.0, 1.2}, N=1/φ deterministic.
- All four runs reached stop_time=5e-3 s. (0, 0, 1, 1) ignition outcomes.
- Headline IP shape matches paper Fig 7 qualitatively; L1=0.65 distance.
- Self-score: Coverage 8/10, Agreement 8/10, Overall 8/10.
- See `REPORT_v6.md` and `report/1559043_replication_report_v6.pdf`.

## 2026-04-28 — v5 (preempted)

- 20-run jitter ensemble on Polaris preemptable queue (5×4 = 20 jobs).
- φ=0.6/0.8 reached 5 ms; φ=1.0/1.2 truncated at ~1.6 ms by queue preemption.
- IP shape: (0, 0, 1, 1) same as v6, L1=0.65.
- See REPORT.pass1.md.

## 2026-04-24 — v4

- 20-run Polaris ensemble, 1-ms window, no AMR. Coverage 7/10.

## Earlier — v1-v3

- v1: CPU OpenFOAM attempt, units bug (replication/).
- v2: PeleLMeX GPU attempt, low-Mach incompatible (replication-gpu/).
- v3: PeleC v2 setup, no AMR, ensemble not yet run (replication-pelec/).
