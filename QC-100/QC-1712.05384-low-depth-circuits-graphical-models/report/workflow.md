# Workflow: End-to-End Reproduce Recipe

Paper: arXiv:1712.05384 (Boixo, Isakov, Smelyanskiy, Neven — 2017).
Host: CherryRd (macOS, laptop CPU). Verdict: REPLICATED (C1–C4 scaling claims).

## 0. Prerequisites
- Python 3.14+ (used 3.14.6).
- Fresh venv strongly recommended (isolates numpy+opt_einsum versions).
- ~50 MB disk for sweep JSON + figures.
- Runtime: full 70-config sweep completes in **~90 seconds** on a laptop CPU.

## 1. Fetch paper + one-time setup
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1712.05384-low-depth-circuits-graphical-models
# arXiv PDF + text extract already staged in work/1712.05384.{pdf,txt}
mkdir -p report/evidence
python3 -m venv .venv
source .venv/bin/activate
pip install numpy==2.5.0 opt_einsum==3.4.0 networkx==3.6.1 matplotlib==3.11.0
```

## 2. Sanity checks (fast, ~5 s each)
```bash
cd src
python smoke.py     # 6-config TN ≡ SV check on tiny circuits
python smoke2.py    # broader multi-seed TN ≡ SV check
```
Both must exit with `all_close = True` (machine-precision agreement).

## 3. Main sweep (~90 s)
```bash
python tn_sim.py --out ../report/evidence/sweep.json
```
Writes 70 JSON records, one per (grid, depth) config, each containing:
- `tn_amp_real`, `tn_amp_imag`, `sv_amp_real`, `sv_amp_imag`
- `max_abs_diff` (should be < 1e-16)
- `contraction_width` = log2(largest_intermediate)
- `opt_cost_flops`
- `n`, `l_min`, `d`, `wall_time_tn`, `wall_time_sv`

## 4. Analysis
```bash
python analyze.py  | tee ../report/evidence/analysis.txt
python analyze2.py | tee ../report/evidence/analysis2.txt
```
- `analysis.txt`: per-grid width/bound/flops table + monotonicity check.
- `analysis2.txt`: correctness recap, width/bound ratio stats
  (min 0.333, median 0.667, mean 0.810, max 2.000), per-grid log-linear fits
  for `log2(FLOPs) ~ a·d + b`, TN-vs-2^n ratios at fixed depths, wall-clock
  crossover counts.

## 5. Figures
```bash
python plots.py
```
Produces:
- `report/evidence/fig4_analog_width_vs_depth.png` — direct analog of the
  paper's Fig. 4 (width vs depth, all grids, `min(d·ℓ,n)` bound overlaid).
- `report/evidence/tn_vs_statevector_ratio.png` — classical-savings
  crossover: TN_FLOPs / 2^n vs n, for d ∈ {2,4,6}.

## 6. Validation gates (pass criteria for REPLICATED verdict)
- **C1** correctness: `max(max_abs_diff) < 1e-15` across all 70 configs.
  Observed: 3.42e-17.
- **C2** width bound: `width / min(d·ℓ, n) = O(1)` (max ≤ 2) across all
  configs. Observed max 2.0 (at shallowest 1D case), median 0.667.
- **C3** exponential-in-depth: per-grid log-linear slope of
  `log2(FLOPs)` vs `d` is positive, monotonically increasing with `ℓ_min`,
  and bounded above by `ℓ_min + O(1)`. Observed: 0.36–1.06.
- **C4** crossover: `TN_FLOPs / 2^n < 1` at `d=2` for at least one
  `n ≥ 10`. Observed: ratio 0.95 at n=10, 0.024 at n=16.

## 7. What is NOT reproduced (out of scope, honest)
- **C5** (paper Fig. 3, `7×8` depth 30 and larger): requires ~day-long
  QuickBB run + 128 GB RAM; not attempted. See `failure_analysis.md`.
- **Head-to-head vs cotengra / quimb / qFlex / hybrid Schr-Feynman**: not
  done. See open_questions.json Q2.
- **Noise extension**: not attempted. See open_questions.json Q1.
- **Byte-identical match to Google/QuickBB reference implementation**: our
  TN structure was independently built from the paper's description and
  verified against statevector, but was NOT diffed against the original
  code (which is not published in the paper's repo).

## 8. Rerun-from-scratch time budget
- Environment setup: ~2 min.
- Sanity checks: ~10 s.
- Main sweep: ~90 s.
- Analysis + plots: ~5 s.
- **Total**: ~4 minutes end-to-end on a laptop.

## 9. Failure modes seen during original run
- On Python 3.13, `opt_einsum` 3.3.0 had a `PathInfo.largest_intermediate`
  attribute bug on trivial 1-tensor networks (n=1, d=0); upgraded to 3.4.0
  to fix.
- Early circuit generator applied random 1Q gates to ALL qubits every
  layer, over-counting gate cost by 2×; fixed by gating on
  "touched-by-prior-2Q" per the paper's Sec IV.
- opt_einsum wire-name symbol collisions at n>26 required moving to
  `opt_einsum.get_symbol(k)`.
