# PROGRESS — Brahme 2024 LUCID100 backfill (slot 60 / paper rank 91)

Timeline (America/Chicago, 2026-06-09):

- 14:46 — Subagent task received. Source-of-truth row located at rank 91 (Wave 6, candidate_curated, tier B, score 13).
- 14:47 — Folder created: `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-brahme-radiobio-optimization-review`.
- 14:47 — `paper.pdf` fetched from Gavin Publishers OA URL (4.69 MB, PDF 1.7). MD5/SHA not computed (single source, manifest captures size).
- 14:47 — `pdf` tool failed: Anthropic credit exhausted, Gemini model unknown, OpenAI extract plugin off. Fell back to `pdftotext -layout` → `paper.txt` (2,159 lines). Sufficient.
- 14:48 — Structural scan: 38 figures, 0 numbered tables, no Methods, no Data Availability, no Code Availability. Single-author review/perspective in suspect venue (Gavin / *Annals of Case Reports*).
- 14:48 — Equation harvested: **Eq (1) `P+ = PB − PI + δ(1−PB)PI`, δ ≈ 0.2** (text near l. 693 and l. 1028).
- 14:48 — Replication assessment:
  - Figure digitization → POSSIBLE but each figure is a replot of Brahme's own earlier work; replicating *the figure* would not validate any new claim. NOT VALUABLE.
  - LQ refit / cell-survival refit → NOT_FEASIBLE: no numerical data points in the paper; original data lives in refs [1-3, 23, 45].
  - LDHS dose-response refit → NOT_FEASIBLE same reason.
  - **P+ / Eq (1) toy smoke** → FEASIBLE in <100 lines of Python. Selected as smoke target.
- 14:49 — `smoke/p_plus_smoke.py` implemented (numpy + matplotlib). Poisson-sigmoid PB and PI; sweep δ ∈ {0, 0.2, 1}; γC penalty case to mimic Figures 15/18.
- 14:49 — Smoke executed clean on CherryRd (CPU-only, <1 s). Outputs:
  - `figs/p_plus_smoke.png` (171 KB, 4-panel) — wrote OK
  - `figs/p_plus_smoke.csv` (71 KB, 1001 rows) — wrote OK
- 14:49 — Numerical results recorded:

  ```
  D50_T=60 Gy, gamma_C(low LET)=3, gamma_C(high LET)=1.8
  D50_N=70 Gy, gamma_N=4
  delta=0.00  -> P+_max=0.503 at D*=62.9 Gy
  delta=0.20  -> P+_max=0.512 at D*=63.1 Gy
  delta=1.00  -> P+_max=0.554 at D*=63.9 Gy
  high-LET, delta=0.2 -> P+_max=0.474 at D*=61.4 Gy
  ```
  Interpretation:
  - δ → 1 (statistical independence) *raises* the headline P+ because the residual-injury term `(1−PB)PI` is reinterpreted as a *bonus* under independence. This is exactly Brahme's point that δ = 1 is unrealistically optimistic; clinically, correlated tumor benefit and normal-tissue injury (δ ≈ 0.2) is the right regime.
  - Reducing γ_C from 3.0 to 1.8 (mimicking the high-LET microdosimetric penalty in Figures 15/18) drops peak P+ by ~3.8 pp and shifts D* down by ~1.7 Gy — qualitatively the direction Brahme reports for neutron/carbon vs photon/lithium.
- 14:50 — `README.md`, `artifacts/MANIFEST.md`, this `PROGRESS.md`, and `FIRST_PASS_REPORT.md` written.
- 14:50 — Subagent-progress JSON record written to `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-slot60-brahme-2024.json`.

## Compute / cost
- All work on CherryRd, CPU-only. No heavy compute. No paid endpoints contacted. No author contact.

## Blockers encountered
- `pdf` tool unusable (Anthropic billing + Gemini name + OpenAI plugin all failed). Worked around with `pdftotext`.

## Status
- **FIRST_PASS COMPLETE — NO_GO_REVIEW_ONLY with smoke supplement.**
