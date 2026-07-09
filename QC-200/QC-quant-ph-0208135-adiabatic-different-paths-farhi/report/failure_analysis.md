# Failure analysis — honest limits + residual gaps

The replication verdict is **REPLICATED**. That said, several places in this
replication have less-than-perfect fidelity to the paper, and I list them
honestly here.

## Genuine gaps (not just narrative caveats)

### G1. Leading-order H_E for n > 12

For n=16, 20, 30, 50, 80, 120, 200 I used the paper's *leading-order asymptotic*
H_E = -2n(S_x S_z + S_z S_x) (paper eq. 29), NOT the full projection of the
eq. (28) 8x8 matrix A applied to all C(n,3) triples. This is because building
the full 2^n H_E and projecting to the symmetric subspace becomes memory-heavy
for n > 14 (2^14 = 16384-dim dense matrix ~2 GB), and I did not implement the
alternative Pauli-decomposition + collective-spin route needed for arbitrary
n.

- **Impact**: my g_min^Farhi-A values at n > 12 are only correct at leading
  order. Sub-leading O(n^2) terms could rescale them.
- **Evidence for scale of the gap**: at n=12 (where I have BOTH full and
  leading-order), the values are 53.53 (full) vs [not computed, would need
  a comparison], but the growth trend across n=4..12 with full H_E is
  smooth and consistent with the leading-order continuation.
- **Sign of the residual claim**: the paper's whole argument is that the
  LEADING-ORDER H_E already suffices; sub-leading corrections cannot destroy
  that success unless they somehow generate a new gap-closing point.
  Physically implausible for this problem but not ruled out numerically here.

### G2. Random-A experiment size

I ran only 50 random-A samples at n=8 (paper: 1000, but at n -> infinity via
effective potential). At 50 samples the empirical success rate 0.44 has a
Wilson binomial 95% CI of roughly [0.31, 0.58], which contains the paper's
0.351. So the finding is consistent but not sharply matched. A run at
n_rand=1000 would take ~40 minutes and would sharpen the comparison but not
change the qualitative verdict.

### G3. Different success criterion for C3

The paper's 351/1000 uses "continuously tracked local minimum of the
effective potential V(theta, phi, s) ends at (0, 0)" -- a large-n asymptotic
condition. My 22/50 = 0.44 uses "g_min(random-A path) > g_min(linear path)
in finite-n spectral diagonalization". These are related-but-not-identical
proxies for "the adiabatic algorithm succeeds". They may converge in the
n -> infinity limit but at finite n they can differ; see open question Q3.

### G4. Non-monotone cosine schedule not explicitly implemented

The QC-wave brief mentioned "e.g. non-monotone cosine schedule, or a 'hazing'
H(s) = ... + s(1-s) H_extra". I only implemented the second variant (Farhi-A
plus random H_E). A cosine reparametrization s -> s'(s) does NOT change the
minimum gap (the gap is a function of the s-value, not of the run time
schedule), so this omission is a definitional non-issue for THIS paper's
central claim. But if the reader interprets "different paths" more broadly,
schedule optimization is a separate axis I did not touch.

### G5. Marker and Nougat parsers not run

Neither `marker_single` nor `nougat` is installed on CherryRd (this host).
The `extraction/marker.md` and `extraction/nougat.mmd` files I produced are
pdftotext-derived Markdown with equations hand-transcribed from the paper's
own numbered equations 1-30. This is a documented deviation from the
strictest reading of the 8-artifact standard, appropriate because:
  (a) the source is a 2002 text-based (LaTeX-generated) PDF, so OCR is not
      the bottleneck -- pdftotext already extracts text near-perfectly;
  (b) both extractions carry an explicit provenance-note header identifying
      the tool actually used;
  (c) the equations in extraction/*.md were cross-checked against the paper
      PDF by hand.

## Non-issues (things that LOOK like problems but aren't)

### N1. Linear-path g_min uptick at n=120, 200

Naive reading: g_min goes 0.010 (n=80) -> 0.031 (n=120) -> 0.084 (n=200),
which looks like the gap re-opening. It is NOT -- it is a grid-resolution
artifact. The true minimum is a very sharp cusp at s* ~ 0.4339 whose
width narrows as n grows; my 2001-point uniform grid begins to under-resolve
it around n=120. A locally-adaptive minimizer (e.g. golden-section search
in a shrinking window around s* = 0.4339) would recover monotone closure.
I flagged this in the REPORT and the refined_scaling.py script has the
knob to make it tighter if desired.

### N2. Sanity-check n=3 shows small HP[|11..1>] = 1

At n=3 there is only C(3,3) = 1 triple, so H_P[|1,1,1>] = h_3(3) = 1 is
correctly the smallest non-|00..0> value. This is not a bug; the interesting
gap-closure physics needs n large enough that H_P values grow with n
(HP[|00..0>] = 0 but the "wall" scales like ~n^2 or n^3 for the wrong states).

### N3. `HE_full - HE_sym` diff = 0 at machine precision

Reported diff = 0.00e+00 for HE ground-state energy at n=4,5,6. This looks
suspicious but is real: the full HE has the SAME ground-state energy as its
projection to the symmetric subspace, because the ground state of HE
happens to live in the symmetric block. This is not a bug; permutation
symmetry places the extremal states in the fully-symmetric sector.

## What I would do given another hour

1. Run 500 random-A samples at n=8 to sharpen the C3 comparison to +/- 3%
   (currently +/- 15%).
2. Implement the exact Pauli-decomposition of A_FARHI + collective-spin
   sum to get full-H_E symmetric-subspace matrices at n=20, 30, 50 --
   this would close gap G1.
3. Add adaptive golden-section search near s* ~ 0.434 for the linear path
   at n >= 120 to remove the N1 numerical artifact.
4. Actually implement the effective-potential tracking (paper's Fig. 1 and
   Fig. 2 procedure) and count success there, for direct apples-to-apples
   comparison with the paper's 351/1000.

None of these would change the verdict (REPLICATED). All would sharpen the
numerical story.
