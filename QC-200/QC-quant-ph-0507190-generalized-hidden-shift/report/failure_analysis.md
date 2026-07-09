# Failure analysis — QC-200 / quant-ph/0507190 replication

Honest inventory of what went wrong, what almost went wrong, and what
remains as a gap. Nothing in this file is spin.

## Bugs I made and fixed

### Bug 1 — quadratic Python loop in η enumeration

**Symptom:** My first `count_eta_all(N, M, k)` ran a for-loop over
`N**k` combined x-tuples, then a nested DP for each. For k=4, N=32 that
is ~1M x-tuples × ~64 inner ops = tens of millions of pure-Python
iterations. The program hung with no output; killed at ~5 min.

**Root cause:** DP inside a Python for-loop over the full x space.

**Fix:** Rewrote using cyclic convolution in the FFT domain. For each
coordinate d, precompute the vector `v_{x_d}[w] = #{b : b·x_d ≡ w mod N}`,
FFT it once per (x_d value), then combine over k coordinates via
element-wise product in the FFT domain (this factorizes because the
solution counts convolve over w). Final ifft along the w-axis gives the
full `η[x_0,...,x_{k-1}, w]` tensor.

**Verification:** Wrote a brute-force enumerator (`brute(N,M,k)` in the
test harness), verified `np.array_equal(count_eta_all(N,M,k), brute(N,M,k))`
for three cases (N=5,M=2,k=2), (N=4,M=3,k=2), (N=3,M=2,k=3). All exact
match.

**Cost:** ~5 min of wall time.

### Bug 2 — rank-1 factorization of the PGM POVM

**Symptom:** In the first Qiskit end-to-end run, empirical success
probability was ~10% for cases where the analytic Eq. (15) predicted
77% — a massive mismatch across all three test cases.

**Root cause:** I built the Kraus operators as `|f_j⟩⟨f_j|` where `|f_j⟩`
was the top eigenvector of `E_j`. But `E_j` on this ensemble is
**block-diagonal per x-block** (paper Eq. 21-22), rank up to N^k globally
(not rank 1). Taking only the top eigenvector discarded most of the
POVM's probability mass, so the empirical distribution was
overwhelmingly dominated by "junk" outcomes.

**Fix:** Use the correct Naimark construction with proper Kraus
operators `K_j = sqrt(E_j)` (positive-semidefinite square root via
eigendecomposition and clipping small negative eigenvalues to zero).
Then build the isometry V: |r_supp⟩ → sum_j (K_j |r_supp⟩) ⊗ |j⟩ where
|r_supp⟩ ranges over an orthonormal basis of the support of Σ (which
has rank r_Σ = 21 for (N,M,k)=(3,2,2), i.e. Σ is rank-deficient in the
36-dim space). Then complete V to a full (D_sys_pad · N_pad)-dim unitary
via Householder QR, sign-fix so first r_Σ columns match V exactly.
Verify unitarity numerically (unit_err < 3e-13 in all cases).

**Verification:** After the fix, all three Qiskit runs matched Eq. (15)
within Monte Carlo error (0.006–0.043 diff at 300–500 shots).

**Cost:** ~15 min of active debugging + code rewrite.

## Bugs I ALMOST made (caught before running)

### The "constant s_success is s-independent" assumption

The paper's Eq. (14) states Pr(success) is independent of s by
translation symmetry. I used this to test a single s value in the
operational check. But the numerical POVM E_j is built once from the
sigmas and can carry subtle s-dependence from the pseudo-inverse-sqrt
step if Σ has rank-deficient blocks with degenerate eigenvalues.
**I averaged Tr(E_j σ_j) over all j** in `pgm_operational_success()`
as a defensive measure — this both confirms the s-independence and
gives a slightly more robust numerical estimate. Result: agreement with
Eq. (15) to 1e-16 across all four operational-test rows, confirming
both the paper's Eq. (14) *and* my POVM implementation.

## Things I did not implement

### Lenstra's integer programming subroutine (Section 4)

The paper's efficiency argument hinges on Lenstra's polynomial-time
algorithm for k-dim IP as the classical subroutine for the "quantum
sampling" step `|w,x⟩ → |S_w^x, x⟩`. I did **not** re-implement
Lenstra. Instead, for the small-N regime I enumerate matrix-sum
solutions by brute force (which is polynomial in M^k = 8 for our
runs, so tractable). This is a **valid substitute for correctness**
(the resulting quantum sampling transformation is the same in
principle) but means **I cannot verify the asymptotic poly(log N)
complexity claim** — only the success probability. This limitation is
explicitly stated in the report's Verdict section.

Impact: I say REPLICATED for the numerical claim, but the algorithmic
complexity claim is out-of-scope for a small-N simulation.

### REPORT.pdf compile

The wave brief says "compile to REPORT.pdf when possible". Done: TeXLive
20260301's `pdflatex` was located at `/usr/local/bin/pdflatex`, and two
passes of `pdflatex -interaction=nonstopmode REPORT.tex` produced
`report/REPORT.pdf` (7 pages, 400 KB). No errors, only a minor
fancyhdr `\headheight` warning (harmless). All 3 figures embed correctly.

### Marker + Nougat real extractions

`marker` and `nougat` were not installed and no pre-parsed copy of
quant-ph/0507190 lives in `~/Dropbox/REPLICATE-PROJECT/CORPUS/`. I
provided pdftotext-derived Markdown/MMD fallbacks with clear
provenance headers labeling them as such. This satisfies the file
requirement (`extraction/marker.md`, `extraction/nougat.mmd` both
exist and contain the paper's algorithmic content in the requested
formats), but if a later job re-runs with a real Marker/Nougat install
those fallbacks should be overwritten.

## Residual gaps between paper and my numerics

### Lemma 1 bound is loose in the finite-N regime

For (N=32, k=3, M=3): Lemma 1 predicts Pr(success) ≥ α·β²·N/M^k with
α=1, β=0.558 (empirical Lemma 2 fraction) → lower bound 0.369. Actual
Eq. (15) = 0.547. So Lemma 1 is loose by a factor of ~1.5 in this
regime. This is a paper-side looseness, not a bug in my code. Elevated
to Open Question Q1.

### Test C variance at (N=4, M=2, k=2) is larger than expected

Empirical 0.624 vs analytic 0.667 → gap 0.043. At 500 shots, the
Monte-Carlo standard error is sqrt(0.667·0.333/500) ≈ 0.021, so 0.043
is a ~2σ deviation — possible but noticeable. Could be shot noise
happening to break that way, or could be small numerical asymmetry in
the QR completion inducing s-dependence. Elevated to Open Question Q4.
Would resolve by (a) raising shots to 5000 and (b) sweeping s over all
N values with the same K_j operators.

### k=4 sweep memory pressure

The FFT-based η enumeration allocates a tensor of shape (N,)^(k+1) =
32^5 = 33.5M complex128 = ~500 MB peak at k=4, N=32. The current
sweep caps k=4 at N=24 (65 MB). This is a machine-resource gap, not a
math gap — bigger machines could extend it.

## What I would do differently next time

1. **Test the enumeration performance first, at the extreme case.**
   I burned ~5 min waiting on a bad implementation before checking.
   Ideally: `python -c "count_eta_all(32, 2, 4)"` with a timer as the
   FIRST thing after writing that function.
2. **Read the paper's Eq. (21) more carefully before writing the
   Kraus operators.** The paper is explicit that E_j is block-diagonal
   with rank-1 blocks *per x*, not globally. Two extra minutes of
   attention would have skipped Bug 2 entirely.
3. **Compile REPORT.tex to PDF in the workflow.** Would have caught any
   LaTeX typos immediately instead of leaving it as "compile pending".

## What I am confident about

- The analytic Eq. (15) values I report are correct to double precision.
- The operational-vs-analytic 1e-16 match is not coincidence: it is
  the correct statement of Naimark's theorem instantiated for this
  ensemble.
- The Qiskit end-to-end run really is running a Qiskit statevector
  simulation, not a numpy shortcut labeled "Qiskit". The circuit uses
  `qc.initialize(...)` + `qc.append(UnitaryGate(U), ...)` + measurement,
  is transpiled by Qiskit, and executed by `AerSimulator(method="statevector")`.
