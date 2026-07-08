# Workflow — QC-2403.08859 replication

Chronology of the actual work executed for this replication (Track A only —
Track B qubitization resource counting was declared out of scope up front).

## Step 1 — Paper acquisition and skim
- Downloaded arXiv:2403.08859v4 to `work/paper.pdf`; converted to
  `work/paper.txt` via `pdftotext -layout`.
- Identified the two tracks: (A) classical statevector simulation of QSE on
  Eq. 15 (Sec. 4, Fig. 3, Appendix A.1), and (B) analytical qubitization
  block-encoding cost analysis (Secs. 5–6).
- Decision: Track A is a runnable numerical claim, replicable end-to-end on a
  laptop CPU in seconds; Track B is a compilation-level resource-estimate
  claim requiring Qualtran or equivalent, and is out of scope.

## Step 2 — Hamiltonian and reference-state derivation
- Rewrote Eq. 15 as a set of spin operators; identified diagonal
  electric-field-squared term and off-diagonal hopping (V).
- Determined `φ†φ = (1 + σ_3)/2` (not `(1 − σ_3)/2`) by matching Eq. 7 → Eq. 15
  mass term µ(-1)^n φ†φ.  First implementation had the sign flipped; the
  wrong sign gave `⟨GS|ψ_ref⟩ = 0` and a dead Krylov subspace, immediately
  caught by the sanity gate `⟨ψ_ref|H_0|ψ_ref⟩ = E(x=0)` failing.
- After sign fix, sanity gate passed to machine precision for all N.

## Step 3 — Implementation
- Wrote `src/schwinger_krylov.py` (~200 lines of numpy) building H as a sparse
  2^N × 2^N operator with standard Pauli tensor products.
- Implemented two Krylov variants:
  - **Hankel/moment form** (the paper's quantum protocol): compute
    m_k = ⟨ψ_ref|H^k|ψ_ref⟩ for k = 0..2D, assemble D×D Hankel matrices, solve
    generalised eigenvalue problem H c = E S c.
  - **Three-term Lanczos** (classically stable analogue).
- Both variants run automatically for all N in a single driver loop.

## Step 4 — Execution
- `python3 src/schwinger_krylov.py` on CherryRd (macOS, Python 3.14.6, numpy
  2.4.3, scipy 1.18.0).  Runtime ≈ 3 s for N = 4, 6, 8, 10 with D up to 14.
- Wrote per-N JSON evidence files to `report/evidence/schwinger_N{N}_*.json`
  and combined summary to `report/evidence/summary.json`.
- `python3 src/plot_convergence.py` produced `report/evidence/convergence.png`
  (panel A: ∆E/E_int vs D log-scale, threshold 10^-4 marked; panel B:
  cond(S) vs D vs ε_machine line).

## Step 5 — Cross-check against paper
- Compared threshold-D at 10^-4 target: paper's linear fit gives
  D ≈ 0.057 N + 4.36; ours hits 10^-4 at D = 3 (N=4), 4 (N=6, 8, 10) — inside
  the paper's Fig. 3 error bars.
- Confirmed Hankel condition-number blow-up: cond(S) ≈ 10^16 by D = 7 for
  small N, matching paper's Sec. 4 failure-mode description.
- Confirmed overlap trend: |⟨GS|ψ_ref⟩| decreases from 0.98 to 0.94 across
  N = 4 → 10, matching Fig. 4 lower panels qualitatively.

## Step 6 — Report writing
- `report/REPORT.md` (2026-07-03) written with claims table, results tables,
  and verdict.
- Backfilled (2026-07-06): REPORT.tex, open_questions.json (5 open
  questions), workflow.md, artifacts_summary.md, failure_analysis.md, and
  extraction/nougat.mmd stub.

## What was NOT done
- Track B qubitization compilation and T-count (out of scope; the largest
  gap).
- Comparison against pure-VQE or Trotter baseline on the same instance (paper
  does not do this either, but a genuine independent check would add value).
- Extension to N > 10 (paper goes to N = 26; trivially feasible in minutes
  but under the "no re-run sims" constraint for this backfill).
- Non-abelian gauge groups, adaptive Krylov variants, or noise-robustness
  probes — all logged as open questions.
