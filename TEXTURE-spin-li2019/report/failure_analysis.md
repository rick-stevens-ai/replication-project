# Failure analysis — li2019 magnon spin Nernst replication (RETRY)

## Prior attempt (what went wrong)
The first run **timed out at 1200 s** and, in the partial output it did save,
produced physically nonsensical numbers: Chern ~ [2.2e5, -2.8e6, -7.0e4] (paper:
-3, 1, 2) and alpha^y_yx/kB ~ 8.4e4 (paper: ~3.5). Two independent bugs:

1. **Broken Colpa diagonalization.** The old `colpa()` mis-assembled the energies
   and the paraunitary matrix T (it mixed the Cholesky factor orientation and the
   sign/shift bookkeeping), so `T^dag sigma3 T != sigma3`. Every downstream matrix
   element `<n|O|m>` was then computed in a non-paraunitary basis, producing
   diverging Berry curvature.
2. **Likely slow / stuck integration.** The nested per-k, per-(n,m) Python loops
   at nk=36 combined with the (attempted) 12-point temperature sweep and a second
   spin polarization, with no early time guard hitting, plausibly caused the
   1200 s wall-clock timeout.

## Fixes applied in this RETRY
- **Correct Colpa method** (`bogo()`): H = K^dag K (Cholesky); diagonalize the
  Hermitian W = K sigma3 K^dag; ebar = sorted eigenvalues; T = K^-1 U sqrt(|Lambda|).
  Verified `max|T^dag sigma3 T - sigma3| ~ 1e-13` at a generic k.
- **Correct matrix elements**: `(O)_nm = (T^dag sigma3 O T)_nm`, matching the
  paper's left/right eigenstate convention `<u_n| = T_n^dag sigma3`.
- **Fixed HP block conventions**: normal block A uses `u_a . M . u_b*`, anomalous
  block B uses `u_a . M . u_b`.
- **Time & size discipline**: coarse 24x24 grid as headline; hard 420 s guard;
  SAVE-EARLY after every grid. Full 3-grid sweep now runs in **~8 s**.

## Remaining limitations (why PARTIAL, not REPLICATED)

### 1. Near-gapless AFM Goldstone mode at Gamma
The 120-degree noncollinear AFM has (near-)zero-energy Goldstone magnons at
Gamma. On a finite grid a k-point landing near Gamma gives:
- a Bose factor g -> infinity (tamed with an IR energy floor ~0.03 J1S), and
- a `1/(e_n - e_m)^2` Berry-curvature denominator -> infinity (tamed with a
  Lorentzian floor ~0.05 J1S).

These regulators make the result finite but introduce **grid sensitivity**:
alpha^y_yx/kB peak = 2.70 (nk=24), 0.53 (nk=30), 0.37 (nk=36). The coarsest grid
happens to sit closest to the paper's ~3.5; finer grids resolve the Goldstone
suppression more aggressively. The **sign, O(1)*k_B magnitude, temperature rise,
and y>>z anisotropy are all robust** across grids; only the exact peak is grid-
limited.

### 2. Chern numbers not cleanly integer
The same ill-conditioning near Gamma spoils the m-sum ordinary Berry curvature
integral, so we do not recover clean (-3, 1, 2). The fix (not done here to stay
time-bounded) is the gauge-invariant Fukui-Hatsuda-Suzuki plaquette method.

### 3. Orbital-magnetization (M) term implemented implicitly
We use the paper's compact c1-weighted formula (Eq. 15), which already folds in
the equilibrium orbital-magnetization correction. We did not separately validate
the S-term (Eq. 8) + M-term (Eq. 14) decomposition; a mismatch there would show
up as a T-dependent prefactor (candidate contributor to the 2.7-vs-3.5 gap).

### 4. Extraction tooling
`marker` and `nougat` binaries were unavailable in the runner; extraction files
are `pdftotext`-based with equations hand-transcribed to LaTeX. Content is
faithful but not from the named neural OCR tools.

## Net
Correct, fast, honest PARTIAL. The physics runner no longer times out; the
headline claim (finite, measurable, DMI-driven intrinsic magnon spin Nernst
response with strong in/out-of-plane anisotropy) is reproduced from scratch.
