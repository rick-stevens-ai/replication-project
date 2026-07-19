# Workflow — Fukami/Sato 2026 (arXiv:2605.18009) theory replication

## Objective
Reproduce, at the reduced-dynamical-model level, the multi-rotational
spin-orbit-torque (SOT) switching mechanism of a Mn3Sn-type noncollinear
antiferromagnet, and its headline fingerprint: a switching-threshold current
that is nearly independent of pulse duration (a plateau), contrasted with a
conventional single-domain switch.

## Steps executed
1. **Read** `report/method_extract.md` to fix scope: THEORY only, low-dim
   stochastic LLG ODE, CPU-only, numpy/scipy. Did not re-derive physics.
2. **Wrote** `code/fukami2026_replication.py`:
   - Reduced order-parameter equation
     `alpha_eff dphi/dt = -dU/dphi + tau_SOT(j) + xi(t)`,
     `U = -K6 cos(6 phi) - h_z cos(phi - phi_H)`.
   - Euler-Maruyama integrator with FDT thermal noise
     (`noise_amp = sqrt(2 alpha_eff kBT dt)`).
   - Pulse-then-relax protocol; records peak turns, net rotation, final well.
   - Conventional uniaxial control model (`U = -Ku cos(2 phi)`) with the same
     drive/noise for contrast.
3. **Experiment 1** — rotations vs current amplitude j (15 j-values, 60 traj).
4. **Experiment 2** — threshold-j vs pulse duration (7 durations, 80 traj)
   for both AFM and conventional models; thresholds at P>=0.5 (consistent
   criterion) and P>=0.9 (reliable) reported.
5. **Scored** three claims honestly; saved `work/results.json` incrementally.
6. **Figures** to `figs/`: rotations_vs_j, threshold_vs_duration (plateau vs
   decline), phi_trace_multirotation.
7. **Artifacts**: REPORT.tex/pdf, open_questions.json, workflow.md,
   artifacts_summary.md, failure_analysis.md, META.json update.

## Key modelling decisions (and why)
- **Overdamped single-angle reduction**: the 120-degree triangular order rotates
  coherently, so one collective angle phi suffices for the mechanism.
- **Deterministic depinning current** `j_dep = 6*K6`: the maximum anisotropy
  restoring torque; a pure current-amplitude condition -> origin of the plateau.
- **Switch criterion evolution** (documented in failure_analysis.md): moved from
  "final state != initial" (corrupted by the 5/6 random-final-state saturation
  of a six-fold potential) to "escaped initial well past the first saddle",
  which isolates the depinning condition.
- **Honest scoring**: the AFM plateau is *near*-flat, not perfectly flat (weak
  thermal foot). Scored as a quantitative CONTRAST (conventional decline is
  2.18x steeper) rather than demanding a mathematically flat line.

## Reproduce
```
cd TEXTURE-spin-fukami2026
python3 code/fukami2026_replication.py    # ~200 s, CPU-only
# outputs -> work/results.json, figs/*.png
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
Deterministic seed `RNG_SEED=20260718`.

## Budget
Wall time ~200 s per full run (well under the 1200 s cap). Ensembles 60-80
trajectories/point.
