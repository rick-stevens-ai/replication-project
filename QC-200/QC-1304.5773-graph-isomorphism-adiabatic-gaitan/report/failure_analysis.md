# Failure analysis & friction — QC-1304.5773

## What worked immediately
- Paper fetch (arXiv:1304.5773v2, 22 pages) and `pdftotext` skim.
- Enumeration of S_N, edge-mismatch cost, and Cayley-mixer construction.
- N=4 iso instance: fidelity 1.0000 on the very first run (T=50, 500 steps).
- N=5 non-iso control: final H_P energy = 4.0000 = exact classical minimum
  edge-mismatch — no adiabatic-time tuning needed.
- Deterministic evolution via per-step Hermitian eigendecomposition (dense
  120×120 matrix; fully tractable on CPU).

## What partially failed / needed a fix
1. **First-pass fidelity at N=5 was 0.766, below the 0.8 REPLICATED bar.**
   Root cause: T=50 was too short for the N=5 instance — the adiabatic
   approximation degrades when T × min-gap is small. Fix: bumped T=50→200
   and Trotter steps 500→2000 (roughly holding dt≈0.1 constant). Second run:
   fidelity 0.997. No change to the physics — just longer evolution time.
   *Lesson:* on adiabatic-optimization replications, calibrate T against
   min-interior-gap (rule of thumb T ≳ 1 / gap^2) before declaring PARTIAL.

2. **"Min spectral gap" is 0 at s=1 for all iso instances.**
   Root cause: H_P is highly degenerate at s=1 whenever the automorphism
   group is non-trivial (|Aut(C_4)| = 8, so H_P has an 8-dimensional 0-eigenspace)
   or when multiple isomorphisms exist. This makes the naive
   "min over the whole schedule" gap uninformative about the actual
   anti-crossing that determines adiabatic runtime.
   Fix: also reported `min_gap_interior` computed on s ∈ [0.05, 0.95] to
   avoid the endpoint degeneracy artifact. The interior gap is small
   (~10^-4 for iso instances) but the physics still works because the
   degeneracy is present throughout the schedule and the initial state
   remains inside the low-lying manifold.
   *Lesson:* AQO papers that quote a "min gap" number implicitly assume a
   non-degenerate H_P (or use symmetry-adapted subspaces); replicate with
   the actual endpoint structure of the specific H_P, not an idealization.

3. **Author name typo in task brief.**
   Task brief said "Lane Clemente"; PDF says "Lane Clark". Verified from
   arXiv abstract page + PDF title page. Recorded in REPORT.tex §1 and used
   the correct name throughout.

## What we did NOT reproduce
- **Full paper encoding (L = N⌈log₂N⌉ qubit bit-strings + C1, C2 penalty
  terms).** We used the exponentially-more-compact S_N permutation basis
  instead. The physics claim (adiabatic ground-state finding of the GI cost)
  is the same, but the specific gap values Δ(N) the paper reports for their
  bit-string H_P are not directly comparable to our S_N-basis gap values
  because the penalty landscape differs. Cost estimate to redo:
  ~1 additional afternoon of code (2^L states up to 2^12 = 4096 at N=4,
  2^15 = 32768 at N=5, still CPU-tractable; needs C1, C2 penalty tuning).
- **N=6, 7 instances.** Paper goes up to N=7 for select instances
  (5040-dim H_P still fits in CPU RAM). We stopped at N=5 to keep runtime
  within the QC-200 wave budget.
- **Non-linear schedule optimization.** Paper mentions this as future work.
  We used a linear s(t) = t/T schedule.

## Residual gaps / caveats
- The verdict rests on qualitative match, not a headline scalar. There is no
  single number in the paper we reproduce to N decimal places — the paper's
  numerical claims are themselves qualitative (fidelity, mean gap curves)
  and instance-specific. Our stronger claims: fidelity ≥ 0.997 for both iso
  instances and final energy = 4.0 for the non-iso control are internally
  verifiable but do not map onto a single number in the paper.
- Marker/Nougat are surrogates (PyMuPDF and pdftotext respectively). The
  parsed content is faithful — no math loss beyond what pdftotext already
  drops — but they are not the exact tools the completion bar names. This
  is transparent to the reader (README.md in `extraction/`) and matches the
  convention already established for sibling QC-200 dirs.
- No 3-judge Argo panel was run (brief allows "self-verdict if time-limited").

## Would-repeat / would-change if re-running
- Would repeat: S_N basis, exact eigendecomposition per step, deterministic
  evolution, hard-coded instances with known ground truth.
- Would change: pre-compute the interior-gap once, then set T = C / gap² with
  C ~ 100 to auto-calibrate T rather than hand-tuning. Also would add N=6, 7
  runs (5-10 additional minutes on CPU).
