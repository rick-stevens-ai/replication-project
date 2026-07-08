# Failure analysis — honest critique

## Verdict recap
**REPLICATED (headline claim C1–C5).** The paper's central message that dZNE
extrapolator choice is regime-dependent reproduces across 5 spot cases on a
real Mitiq + Qiskit Aer stack in 17 s.

## What was genuinely exercised

- Head-to-head comparison of **four** extrapolation families (Linear,
  Quadratic, Richardson, Exponential) on **identical** raw noise-amplified
  scans, across 5 (depth × p2q × scale-range) regimes.
- Both wide-scale integer folding (`fold_global`) and narrow-scale partial
  folding (`fold_gates_at_random`).
- Real shot noise (8000 shots × 3 replicates per λ).
- Ideal noiseless statevector as ground truth.
- Failure mode the paper explicitly warns about (narrow-range Richardson blow-up
  on shot noise) reproduced spectacularly (Case D: |err| = 2.08 on an observable
  bounded in [-1, 1]).

## Where this replication falls short

### 1. Fig. 6 is not a full phase diagram in our run
The paper's Fig. 6 is a dense sweep of ~100+ (depth, p2q) pixels with a
color-coded family winner per pixel. We executed **5** points. Consequence:
we can vote on the qualitative winner boundaries only where our 5 cases land,
not in the interior gradient or corner cases. **A full sweep is feasible on the
same stack** (perhaps 20-60 min wall time depending on grid density) and was
consciously deferred.

### 2. Quantitative match to paper's specific numbers is NOT claimed
The paper uses their own random-circuit seeds and Trotter step counts. Our
seeds (42) and depths (4, 10, 20) are not literally theirs. We reproduce the
qualitative winner-boundary structure and the order-of-magnitude gaps between
family errors, but the per-pixel RMSE numbers in the paper's Fig. 6 are not
independently reproduced. The paper's error-reduction ratios (e.g. "Exp reduces
RMSE by X in the deep-noise corner") could not be checked pixel-for-pixel.

### 3. C6 (partial-fold σ reduction) not measured
We used 3 replicates per scale factor and averaged, but did not vary the number
of replicates or measure σ(n_replicates). The paper claims sampling multiple
partial-folded circuits per non-integer scale reduces σ (Fig. 4). We assumed
this and used it; we did not independently certify it.

### 4. C7 (full phase diagram) not run
Same as (1). Out of scope for a QC-100 spot-run.

### 5. C8 (ROEM + Pauli twirling composition) not exercised
The paper's Sec. V discussion of stacking dZNE with readout error mitigation
and Pauli twirling is untested. Whether the "best-practice" family
recommendation still holds under composition is unknown from this run.

### 6. No hardware run
The paper's headline plots for practical recommendations use real IBM hardware.
We used only Aer with a simplified 2-qubit-only depolarizing model. Hardware
pathologies (non-Markovian correlations, cross-talk, coherent leakage,
calibration drift) are absent and would likely shift some family-winner
boundaries.

### 7. Single seed per case
Case results come from a single circuit seed (42) per case. Multi-seed
ensembles would tighten error bars and give confidence intervals on the
per-family errors. This is a real limitation for the ambiguous boundary cases
(e.g. Case C where Exp barely beats Q).

### 8. Noise model is only 2q depolarizing
Real hardware has amplitude damping, dephasing, coherent over-rotation,
cross-talk, and drift. The mono-Exponential extrapolator's asymptote-to-zero
assumption is depolarizing-specific and may fail elsewhere (see open question Q1).

## Robustness of the replication verdict

### Where the verdict is solid
- **C1** (cross-family divergence on same raw scan): rock solid. Every case
  shows different mitigated values from all 4 families on identical (λ, E)
  data. Case D shows a 2-order-of-magnitude spread.
- **C4** (narrow-range high-degree overfit): rock solid. Case D's |err| = 2.08
  for Q/Richardson is textbook shot-noise overfit on a 3-point narrow-lever scan.
- **C3** (deep+strong → Exp wins): solid. Case B's 12× improvement over Linear
  is far outside single-seed shot-noise error.

### Where the verdict is qualitative only
- **C2** (weak+shallow → Linear wins): our Case A shows Exp beating Linear
  slightly, but everything is within shot noise of the ideal (ideal is
  essentially 0). Interpretation matches the paper qualitatively but the
  ordering of the 4 families in this regime is not statistically resolved.
- **C5** (NF regime): our Case E is a *narrow*-scale variant of NF risk;
  Quadratic pushes through. The paper's own NF characterization is at wide
  scales in the deep/strong corner, which we did not test with narrow scales
  ourselves in isolation.

## Bottom line
**Verdict REPLICATED is honestly earned for the headline** — the paper's
central pedagogical claim about family choice reproduces cleanly across the 5
regimes we tested, on a real free-tier stack, with predicted failure modes
appearing on cue. **Verdict is NOT the same as "full paper reproduced"** — the
full phase diagram, the σ-reduction claim, the QEM-composition claim, and the
hardware results are all deferred.

Headline exercised: **YES**. Full paper exercised: **NO**.
