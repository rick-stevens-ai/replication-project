# Replication workflow — Suzuki et al. arXiv:1904.10246 (MLAE)

## Environment
- Host: CherryRd (macOS Darwin 25.3.0, Python 3.14.6)
- Key libs: `qiskit`, `qiskit-aer`, `numpy`, `scipy`
- Runtime: ~4.5 min single-thread CPU for full sweep (17 (schedule, M) points × 100 trials each)
- No paid endpoints used; entirely local classical simulation

## Steps executed (2026-07-03)
1. **Paper ingestion.** arXiv PDF read; central claim identified as three
   scaling slopes in Fig. 2 right column at a = 1/48.
2. **From-scratch reimplementation.** Wrote `code/mlae_replicate.py`:
   - Circuit builder: `A = R_y(2θ_a)`, `Q = -A S_0 A^† S_χ` with `S_χ = Z`,
     `S_0 = XZX`, on a single qubit.
   - Sampler: real shot-based execution on `qiskit-aer.AerSimulator`, not
     analytic `sin²` probabilities. Shots counted from `result.get_counts()`.
   - Estimator: joint MLE via fine brute-force grid on θ ∈ (0, π/2) with
     N=4096 grid points, then `scipy.optimize.minimize_scalar` polish in
     the winning bracket.
   - Sweep driver: three schedules (Classical / LIS / EIS) × M-lists,
     100 trials per point, RMSE across trials.
   - Slope fitter: `numpy.polyfit(log10(Nq), log10(RMSE), 1)`.
3. **One optimization applied.** Memoized `transpile()` in an LRU cache keyed
   by `(θ_a, m)`. Zero physics change (the transpiled circuit is a pure
   function of the inputs). Effective per-shot rate: ~5/s → ~150/s.
4. **Verification.**
   - Ran sweep; recorded raw counts + per-trial estimates.
   - Wrote per-point RMSE + slopes to `report/evidence/results.json`.
   - Compared slopes to paper's Fig. 2: Classical −0.516 vs −0.50; LIS
     −0.727 vs −0.76; EIS −0.930 vs −0.95. All Δ < 0.04.
   - Head-to-head at Nq ≈ 5×10⁴: EIS RMSE 5×10⁻⁵ vs classical
     extrapolation 6×10⁻⁴ (~10× tighter). Matches paper's practical claim.
5. **Reporting.** REPORT.md written (2026-07-03). Backfill 2026-07-05:
   REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md,
   failure_analysis.md, and extraction stub added.

## What was NOT done (deliberate, budget/scope)
- Canonical QAE (QPE-based) reimplementation for head-to-head comparison
- Noise-model sweeps
- Multi-amplitude sweep (only a = 1/48)
- MLE miss-rate characterization
- Comparison to Iterative QAE, Faster QAE
- Real-hardware run

See `failure_analysis.md` and `open_questions.json` for the honest bounds
on this replication.

## Reproducing this run
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1904.10246-amplitude-estimation-no-pe/
python3 code/mlae_replicate.py 2>&1 | tee logs/main.log
# Reads: (none)
# Writes: report/evidence/results.json, logs/main.log
```

## Data provenance
Every number in `REPORT.md` §3 comes from `report/evidence/results.json`,
which was written by `code/mlae_replicate.py` from real `qiskit-aer` shot
counts on 2026-07-03. No fabrication, no post-hoc editing.
