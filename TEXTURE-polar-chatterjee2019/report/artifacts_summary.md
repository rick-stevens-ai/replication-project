# Artifacts Summary — Chatterjee 2019 (arXiv:1908.00986)

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Replication code | `code/chatterjee2019_replication.py` | Radial O(3)/CP¹ winding-1 skyrmion relaxation; BP baseline; Δ(B) sweep; R(B). |
| 2 | Results JSON | `work/results.json` | Per-claim expectation/reproduced/match/note; all arrays (b, Δ_sk, Δ_obs, sizes, R). |
| 3 | Figure: profile | `figs/skyrmion_profile.png` | Relaxed θ(r) and n_z(r); BP comparison. |
| 4 | Figure: Δ vs B | `figs/delta_vs_B.png` | Skyrmion vs electron channels + non-monotonic observable min-envelope. |
| 5 | Figure: R vs B | `figs/R_vs_B.png` | Non-monotonic magnetoresistance R(B)/R(0) ~ exp(Δ/2T). |
| 6 | Report (LaTeX) | `report/REPORT.tex` | Full write-up. |
| 7 | Report (PDF) | `report/REPORT.pdf` | Compiled report. |
| 8 | Open questions | `report/open_questions.json` | 5 questions (q/basis/next_steps). |
| + | Workflow | `report/workflow.md` | Step-by-step method + reproduce command. |
| + | Failure analysis | `report/failure_analysis.md` | Bugs (2× BP factor, trapz, unphysical draft), limitations. |
| + | Metadata | `META.json` | status + verdict. |

## Headline numbers reproduced
- **Claim 1 (skyrmion energy):** Belavin-Polyakov baseline **E = 12.537** vs
  topological target **4πρ_s = 12.566** → **0.24 % error**; scale-invariant
  across λ∈{5,10,20,40}. Relaxed finite skyrmion (b=0.02, K=0.02): E=21.19,
  size≈4.1. **REPRODUCED (quantitative).**
- **Claim 2 (non-monotonic gap / MR):** relaxed skyrmion channel Δ_sk(b) has an
  **interior minimum at b≈0.125** (46.8 → 16.96 → 19.74). Observable R(B)/R(0)
  has an **interior peak at b≈0.064** (1.0 → 14.6 → 10.3). **Non-monotonic
  magnetoresistance REPRODUCED (qualitative trend);** absolute field/energy
  scale not predicted (needs HF inputs) → PARTIAL on quantitative side.

## Verdict
**STRONG PARTIAL / REPLICATED (analytic argument).** The sigma-model skyrmion
energetics are reproduced quantitatively (BP bound to <1 %), and the central
qualitative prediction — non-monotonic activation gap Δ(B) and hence
non-monotonic magnetoresistance from skyrmion transport — is reproduced. Full
self-consistent Hartree-Fock of the continuum model (absolute units) is
explicitly out of scope.
