# Workflow — QAOA reachability deficits replication

## Timeline (2026-07-03)
1. **Read paper (~30 min).** arXiv:1906.11259, focus on Fig. 1 (top panel, 3-SAT n=6) as the headline testable claim.
2. **Extract testable claim.** C1: reachability deficit f(p,α,n) monotone non-decreasing in α, non-increasing in p, strictly positive at high α for fixed shallow p.
3. **Design minimal replication.** n=6 (fits in 64-dim statevector), α ∈ {0.5,1,2,3,5,7,10}, p ∈ {1,2,4} (lower than paper's 15/25/35 to fit CPU budget — deliberate scope reduction).
4. **Write QAOA engine from scratch** (`code/qaoa_reachability.py`, ~150 lines NumPy). No Qiskit/PennyLane, everything auditable in one file.
5. **Write smoke tests** (`code/smoke.py`): clause-truth table, plus-state expectation of H_SAT, mixer unitarity. All 3 pass.
6. **Run main sweep.** 7 α × 3 p × 15 instances × 4 restarts = 1260 optimizations. ~515 s wall on CherryRd. Seed 20260703.
7. **Post-process** (`code/plot_results.py`): CSV summary + Fig. 1 analog + monotonicity assertions.
8. **Write REPORT.md** with verdict, numeric table, comparison to paper Fig. 1.

## Backfill (2026-07-06)
9. Read REPORT.md (already at `report/REPORT.md`).
10. Wrote REPORT.tex with genuine honest critique (density transition qualitative-only; p ≤ 4 vs paper's 15/25/35; small n_instances; single n; no comparison against modern QAOA variants; no optimizer robustness check).
11. Enumerated 5 truly-open questions with concrete next-step probes.
12. Wrote open_questions_section.tex, artifacts_summary.md, failure_analysis.md, nougat.mmd stub.

## Compute
- CPU only, CherryRd (macOS, Python 3.14.6, numpy 2.5.0, scipy 1.18.0).
- No LLM, no paid API, no GPU.
- Total wall time: ~9 min sweep + ~1 s tests.

## What was NOT done (and why)
- Larger n (paper uses n up to 12): CPU budget for the wave; 2^12=4096 dim would push per-sweep time from 9 min to ~2 hr, and we wanted 7 waves in QC-100.
- Deeper p (paper uses 15/25/35): each doubling of p ~doubles the optimizer's parameter space and its cost. p=4 was the largest we could sweep in <10 min.
- C2/C3/C4 (paper's Figs 2/3/4): out of scope for a qualitative headline replication.
- Optimizer robustness cross-check (COBYLA vs L-BFGS-B vs BOBYQA): flagged as Q1 in open_questions.

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1906.11259-qaoa-reachability-deficits
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib
python code/smoke.py                 # 3 unit tests
python code/qaoa_reachability.py     # main sweep
python code/plot_results.py          # figure + CSV
```
