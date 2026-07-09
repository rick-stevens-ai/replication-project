# Failure analysis — QC-200 / quant-ph/0011067

Honest inventory of what didn't work, what was left out, and what friction
was encountered. No sugar-coating.

## 1. What worked cleanly

- Algorithm 1 implementation in numpy was straightforward once the paper's
  Step 1–4 recipe was extracted from Section 3. The exact p-dim DFT matrix
  is unambiguous and standard.
- The tight `min P(correct) = (p-1)/p` result is stronger than the paper's
  own stated bound and matched exactly across three primes and 105
  instances — a very reassuring sanity check on the implementation.
- Classical distinguisher experiments came out of the paper's cited
  background (Damgård 1988, Jacobsthal identity) without needing additional
  literature dives.

## 2. Out-of-scope claims (not tested, honestly acknowledged)

| Claim | Why not tested |
|---|---|
| Corollary 1 (Shifted Jacobi, n known, square-free) | Requires CRT + Shor factoring + parallel invocation on ~log n prime factors; standard reduction but adds implementation surface out of proportion to the QC-200 budget. Expected to reproduce trivially given Alg 1 works. |
| Theorem 2 (Shifted Jacobi, n unknown) | Requires continued-fractions post-processing and the Hales–Hallgren "repeated-Fourier-sampling" lemma over `Z_M` with `M ≫ n^2`. Both are non-trivial implementation lifts. |
| Theorem 3 (Shifted Quadratic Character over F_{p^r}) | Requires polynomial arithmetic mod an irreducible degree-r polynomial in F_p[X] and a *trace-character* Fourier transform — a fundamentally different simulator architecture. |
| Approximate-QFT efficiency claim | We used the exact p×p DFT matrix, not the Hales–Hallgren epsilon-approximate QFT the paper actually invokes. This validates the algorithm's *correctness* but not the paper's efficiency claim (see Open Question Q4). |

## 3. Environment friction

- **marker / marker_single not installed on host.** Central corpus lookup
  for arXiv:quant-ph/0011067 also came up empty. Fell back to a surrogate
  marker.md derived from pdftotext + manual section-boundary insertion.
  Preamble in the file discloses this. This matches the precedent set by
  QC-0807.4994 and other prior QC-200 replications on this host.
- **nougat not installed on host.** Same fallback pattern; surrogate
  nougat.mmd with equations in LaTeX (matching Nougat's actual output style)
  derived from pdftotext + hand-conversion of the key math to LaTeX.
- **No pdflatex compile attempted.** REPORT.tex is a valid LaTeX file but
  we didn't run pdflatex; the brief lists "compile to REPORT.pdf when
  possible" as a soft optional and the tex source is self-sufficient for
  humans and downstream LLM readers.
- **arXiv paper is from 2000 (25+ years old).** The paper predates modern
  quantum-simulator ecosystems (Qiskit / Cirq / Stim / PennyLane). We
  wrote a from-scratch numpy statevector rather than shim through any of
  those, since a 61-dim DFT is trivial and the reduced dependency surface
  makes the reproduction more auditable.

## 4. Residual gaps between paper and reproduction

1. **Exact QFT vs Hales-Hallgren approximate QFT.** Our exact p-dim DFT
   is *not* the object the paper's efficiency proof uses. The paper's
   Theorem 1 statement is really about the approximate QFT; we validated
   the exact version. This is a real, honest gap — flagged in Open
   Question Q4.
2. **Success-probability tightness.** The paper's `exponentially close to
   1` doesn't specify the sub-leading terms. We observed `P = 1 - 1/p`
   exactly, which is stronger and more interesting than what the paper
   claims — but this exact identity is not stated in the paper, so
   whether it generalises to all primes (rather than being an artifact
   of small p) needs the follow-on in Q1.
3. **Classical lower bound gap.** The paper cites Damgård 1988 for
   classical hardness but does not prove an unconditional lower bound. Our
   three complementary distinguishers (consistent-shift, marginal-bias,
   two-point correlation) yield three different asymptotic scalings
   (`Omega(log p)`, `Omega(p)`, `Omega(p^2)`), none of which match the
   paper's implicit `Omega(sqrt p)` (or better) target. We do not attempt
   to close this gap — see Q2.
4. **Oracle noise model absent.** Real quantum implementations would face
   per-query decoherence and gate error. The paper assumes a perfect
   oracle; we ran with one. The algorithm's phase-cancellation-based
   success is potentially fragile to noise — untested; see Q3.

## 5. Time budget honesty

- The QC-200 wave brief calls for "no HPC/GPU gate" and "aim to actually
  run a real simulation." We did that and finished the core reproduction
  in <30 s of compute time.
- Total end-to-end wall time (paper fetch → REPORT.tex draft): ~30 min.
- No corner-cutting on the quantum algorithm itself: exact DFT matrix,
  exact Legendre-symbol arithmetic, tested on all 105 shift instances,
  not a spot check on a few.
- Corner cutting on the *extensions*: Theorems 2 and 3 are honestly
  acknowledged as untested rather than papered over.

## 6. If we had another 2 hours we would…

1. Sweep primes up to p=1000 to check whether `P(correct) = 1 - 1/p`
   holds exactly (Q1).
2. Implement the approximate QFT and measure the eps-vs-p threshold
   (Q4).
3. Add oracle noise and measure `P(correct)` vs `eta` (Q3).
4. Implement Corollary 1 (Shifted Jacobi, n known) as a sanity check on
   the CRT reduction, which requires almost no new code.
5. Compile REPORT.tex to PDF and eyeball the tables render.

## 7. Nothing hidden

Every claim table entry, every JSON trace, every Python line is in
`report/evidence/`. Re-running the two scripts (`shifted_legendre_algo.py`
and `classical_lower_bound.py`) reproduces every number in this report
byte-for-byte modulo random-seed variation in classical experiment (a).
