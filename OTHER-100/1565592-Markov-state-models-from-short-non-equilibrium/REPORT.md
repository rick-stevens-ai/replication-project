# REPORT (pointer)

This OSTI-id dir holds the replication PLAN. The COMPLETED replication report lives at:
  ../replicate-msm/report/msm_replication_report.pdf

Verdict: REPLICATED (all 3 phases — 1D double-well t2 within 0.2%, 2D within 2%, alanine dipeptide OOM-corrected t2=2146ps vs 2020ps reference ~6%).

## Open Questions & Reproducibility Blockers

- **Fully reproducible** — all 3 phases (1D double-well, 2D potential, alanine dipeptide) re-derived from public references and standard MD tooling; verdict REPLICATED with t₂ agreement within 0.2% (1D), ~2% (2D), and ~6% (alanine dipeptide, after order-of-magnitude correction vs the 2020 ps literature reference). Detailed numerics live in the sibling report `../replicate-msm/report/msm_replication_report.pdf` (this directory only carries the planning PDFs). No blockers.
- **Minor caveat (not a blocker):** The pointer style of this file means the per-phase parameter tables, MD trajectory provenance, and lag-time / clustering hyperparameters are not duplicated here — anyone auditing the score must open `../replicate-msm/report/msm_replication_report.pdf`. A short summary section in this directory would help future audits without changing the verdict.
- **Open question 1:** Does the ~6% gap on the alanine dipeptide t₂ (replication ≈ 2146 ps vs 2020 ps reference) close if the implied timescale is averaged over a longer lag-time plateau (rather than the single chosen lag), or if the microstate clustering is repeated with different k-means seeds? The paper does not provide multi-seed error bars on t₂, so the 6% gap could be within natural seed/lag scatter.
- **Open question 2 / extension:** The 3-phase suite (synthetic 1D, synthetic 2D, real-molecule alanine dipeptide) stops short of testing the short-non-equilibrium MSM construction on a *folding-relevant* peptide (e.g., NTL9 or villin headpiece) where the headline scientific value lies. Extending the same pipeline to a published folding trajectory deposit (e.g., D.E. Shaw Anton trajectories on PDB-Dev or the MDDB MSM-benchmark deposit) would be the obvious next step.
