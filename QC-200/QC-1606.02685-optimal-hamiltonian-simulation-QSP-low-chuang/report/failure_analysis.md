# Failure analysis — arXiv:1606.02685

## What was NOT reproduced (residual gaps)

### G1. Claim C4 (ancilla-projection success probability -> 1) untested
The paper's success-probability analysis (Section III of the PRL and
its Supplement) uses oblivious amplitude amplification to boost the
QSP projector success. Testing this end-to-end requires a full QSP
compiler that produces the phase sequence for the Bessel-weighted
polynomial, then measures the ancilla-projected fidelity. We only
verified the polynomial-realization (the "inside of the box"), not
the outer amplitude-amplification wrapper.

### G2. Claim C5 (end-to-end sparse-oracle query complexity) untested
The headline `O(t d ||H||_max + log(1/eps)/loglog(1/eps))` bound is
denominated in sparse-oracle queries, not in matrix-vector multiplies.
We simulated in dense-matrix land, so we cannot report a query count
comparable to the paper's Table I / Fig 2. Fixing this would require
implementing a sparse-oracle model + a full QSP-based simulator; that
is an order of magnitude more work than the classical numerics we did.

### G3. Weak drift in the fitted slope a(t) for C2
The linear fit `K_min = a(t) x + b(t)` yielded a(t) = 1.67, 1.85, 2.31,
3.24 at t = 1, 2, 5, 10 — a monotone drift. Two interpretations, and
we cannot distinguish them here:
- (a) A genuine sub-log pre-factor drift that the O-notation absorbs.
- (b) A finite-precision artifact: since we can only measure epsilon
  down to ~1e-16, our fits at small t are effectively picking up the
  double-precision floor as a data point, biasing the slope down.
Verifying which requires mpmath at extended precision (see open_questions Q1).

## Friction points (things that slowed the run)

### F1. Marker/Nougat unavailable, no cached parses
Neither `marker_single` nor `nougat` was installed on the CherryRd
host, and the central `~/Dropbox/REPLICATE-PROJECT/*/extraction/`
corpus had parses only for BVBRC papers, not QC-200 entries. Installing
Marker (needs GPU + heavy deps) would eat the entire time budget for
one artifact whose downstream consumers can just as well read the
pdftotext version. Chose to document the fallback explicitly with a
banner at the top of each file rather than block on the install. This
is the same tradeoff another QC-100 replication would face; may be
worth batching a Marker/Nougat corpus refresh on uicgpu.

### F2. `find /` command started for tool discovery ran long
Initial `find / -name marker_single` was going to search the whole
filesystem. Killed it after ~40 s once `pip show` had already
confirmed neither is installed. Trivial lesson: prefer `pip show <pkg>`
first, `find` last.

## Things that WORKED unexpectedly well

- The Chebyshev-recurrence + Bessel-J_k series converged to machine
  precision at K = 15 for t = 1, K = 20 for t = 2, K = 25 for t = 5.
  The paper's asymptotic bound was not even close to being the binding
  constraint at these small t.
- The trivial all-zeros phase sequence in the Wx convention realizes
  T_d(x) exactly (up to numerical roundoff). This is the cleanest
  possible demonstration of the QSP mechanism, and it worked at 1e-16
  on the first attempt — the paper's mechanism is that clean.
- SciPy's `scipy.linalg.expm` and `scipy.special.jv` gave numerically
  clean gold standards; no need to hand-roll Padé approximants.

## What a follow-on run would fix
1. Install pyqsp / QSPPACK and use its Remez completion to compile
   phases for the Bessel-weighted polynomial, closing the C4 gap.
2. Repeat the K_min scan in mpmath at 128-bit precision with eps down
   to 1e-30 to distinguish the two Q1 interpretations.
3. Add a sparse-oracle simulator wrapper to instrument true query
   counts and produce a QSP-vs-Trotter query-vs-error tradeoff plot on
   a Heisenberg-XXZ chain (n = 8-12 sites).
4. Batch-install Marker + Nougat once on uicgpu and populate the
   central extraction corpus for QC-200 so this fallback isn't needed
   for every future QC replication.
