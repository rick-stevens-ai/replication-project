# Failure Analysis — Stier et al. 2017 replication

Honest log of what broke, the root cause, and the fix. Every one of these
produced a wrong or nonsensical result before diagnosis.

## F1 — Berg-Lüscher Q returned exactly 0 for a genuine skyrmion (CRITICAL)
- **Symptom:** every smooth, analytically-Q=±1 texture (tanh core,
  Belavin-Polyakov, compact linear profile) evaluated to `Q_total = 0`, with
  huge cancelling positive/negative content (Qpos ~ 6–11). Early "dynamics"
  then reported |Q| ~ 100–770.
- **Root causes (two, compounded):**
  1. **Periodic boundaries.** Computing the plaquette solid angle with
     `np.roll` (periodic) on a localized skyrmion in a uniform background makes
     the wrap-around edge carry a compensating +Q that exactly cancels the core
     -Q → net 0.
  2. **Mis-oriented second triangle.** The two triangles per plaquette were
     wound oppositely (`T1=(s,sx,sxy)`, `T2=(s,sxy,sy)`), so `tri1 = -tri2` and
     they cancelled (verified: tri1=-2.07, tri2=+2.07).
- **Fix:** open boundaries (slice `[:-1,:-1]` etc., no wrap) **and** both
  triangles wound the same way: `T1=(s,sx,sxy)`, `T2=(sxy,sy,s)`. Validated
  against a non-vectorised reference loop (Q = ±1.0000) and against the uniform
  state (Q = 0 exactly).
- **Lesson:** always validate a topological-charge estimator on (a) the uniform
  state (must be 0) and (b) an analytic Q=±1 texture (must be integer) BEFORE
  trusting any dynamics. A distributed Qpos on a smooth field is a red flag.

## F2 — `roll` acted on the vector-component axis, not the spatial axes
- **Symptom:** after fixing F1, a tuned driving regime produced pairs; but with
  the *correct* spatial axes the same parameters did nothing. The exploratory
  scripts had used `np.roll(a, d, 0)` on a (3,N,N) field, rolling the component
  axis for the first shift.
- **Root cause:** exchange/DMI stencils were computed on the wrong axis, so the
  "physics" that looked like pair creation was partly an artifact.
- **Fix:** `roll` on spatial axes `(-2,-1)`, works for both scalar (N,N) and
  vector (3,N,N) fields. Re-derived the real DMI-stabilisation threshold
  (D≈0.7 at B=0.25) with correct stencils.

## F3 — Precessional LLG (RK4) numerically unstable / spin-turbulence blow-up
- **Symptom:** with correct axes, driven runs blew up to Q ~ ±100–2000; the
  nearest-neighbour gradient saturated at ~1.9–2.0 (checkerboard / antiparallel
  neighbours everywhere).
- **Root cause:** the exchange term `2A∇²n` makes the precessional LLG stiff;
  explicit RK4 is unstable unless dt is small. dt=0.05, 0.01, even 0.005 all
  blew up at A=1.
- **Fix:** (a) dt ≤ 1.5e-3 for the precessional integrator; (b) prepare stable
  states and perform damped annihilation with the **dissipative** update
  `dn = -n×(n×B_eff) dt`, which is unconditionally stable (energy gradient
  descent) and gave clean Q=-1 relaxation (gradient ~0.003).

## F4 — Seeded fluctuation is re-absorbed in the DMI-stabilised regime
- **Symptom:** in the clean skyrmion regime (D=0.75, B=0.25), a Gaussian
  fluctuation + strong current did not nucleate a pair (Q stayed 0); pair
  creation only occurred as multi-pair turbulence when over-driven.
- **Root cause:** adiabatic advection `(v_s·∇)n` preserves topology on a smooth
  field; genuine de-novo nucleation requires either lattice-scale
  singular events (over-driving, which is noisy) or thermal fluctuations.
- **Resolution (scope decision, documented honestly):** demonstrate the pair's
  net-zero charge by explicitly *initialising* a Sk-ASk pair, and put the
  dynamical emphasis on the paper's decisive step — damping-driven asymmetric
  annihilation → net ΔQ. De-novo nucleation from noise is left as open
  question #1 (needs a Langevin thermal field + instability-boundary scan).

## F5 — Soft Gaussian masks destroyed one partner's winding
- **Symptom:** building the pair with overlapping Gaussian masks gave total
  Q=-1 (not 0): the left skyrmion evaluated to Q≈0 because the second mask
  overwrote it and the soft edges spoiled the winding.
- **Fix:** hard radial masks (`r < cut`) with sufficient separation. Verified
  left=+1, right=-1, total=0.

## F6 — Charge-centroid separation metric read 0 (wrong axis)
- **Symptom:** EXP-A reported sep_initial=0 for partners visibly 44 cells apart.
- **Root cause:** with `indexing='ij'`, the partners were separated along axis 1,
  but the centroid was weighted along axis 0.
- **Fix:** compute full 2D centroids; track both the along-axis distance and the
  perpendicular (skyrmion-Hall) split. Also aligned the STT drift axis with the
  separation axis.

## Net outcome
After F1–F6, all three sub-claims reproduce cleanly and robustly: pair Q=0 at
creation, current-driven motion + opposite Hall deflection, and ASk annihilation
→ net ΔQ=-1. The only genuinely *partial* items are de-novo nucleation from
noise (F4) and full current-driven unbinding of a bound pair (EXP-A separation).
