# Failure Analysis — QC-200 replication of arXiv:2401.06240

Honest inventory of the friction hit during this replication.

## 1. pyqsp `PolySign.generate(chebyshev_basis=True)` is broken
**Symptom:** `UnboundLocalError: cannot access local variable 'scale' where it is not associated with a value`.

**Root cause:** in `pyqsp/poly.py` around line 466, the `PolySign.generate`
method returns `pcoefs, scale` on the `chebyshev_basis=True` branch, but
`scale` is only assigned inside the `if ensure_bounded and return_scale`
branch of the earlier `if/else`.  When callers do not pass
`return_scale=True`, `scale` is never defined but is still referenced in
the `return`.

**Workaround:** bypassed `PolySign.generate` entirely and built the
Chebyshev interpolant of `erf(kappa*x)` directly via
`PolyTaylorSeries().taylor_series(func=lambda x: erf(kappa*x),
degree=d, max_scale=0.9, chebyshev_basis=True)`, mirroring
`pyqsp/sym_qsp_min_example.py` verbatim.

**Cost:** ~10 min of head-scratching + one code refactor.

## 2. `method="laurent"` phase-factor solver blows up on high-degree sign approximants
**Symptom:** `CompletionError: Completion Failed. Input F = [...huge numbers...]`.

**Root cause:** the `laurent`-method (older, root-finding-based) requires
monomial-basis input, but the monomial coefficients of a degree-11+
Chebyshev truncation of `erf(kappa*x)` span 5+ orders of magnitude and
overflow the completion routine's numerical stability.

**Workaround:** switched to `method="sym_qsp"` (symmetric-QSP Newton
solver, Dong-Meng-Whaley-Lin 2021).  Accepts Chebyshev-basis coefs,
converges in 5-8 iterations to residual <1e-12 for all target degrees
we tested (up to 41).

**Cost:** ~10 min of trying to normalise/rescale before realising the
right fix was a different solver entirely.

## 3. QSP CONVENTION BUG — real-vs-imaginary channel
**Symptom:** After switching to sym_qsp and verifying my QSVT circuit
matched pyqsp's own `SymmetricQSPProtocol.gen_unitary` at machine
precision, the "polynomial value" I was extracting from `Re[U[0,0]]`
was wrong — max err ~0.4 instead of ~0.

**Root cause:** the widely-repeated QSVT statement "Re[U[0,0]] = P(x)"
is convention-dependent and is FALSE for the Wx convention with odd-
parity target polynomials.  Specifically, the Wx signal operator has
imaginary off-diagonal entries `i*sqrt(1-x^2)`; applying an odd number
of them multiplies the target real polynomial by `i^(odd)`, so it lands
in the imaginary channel of `U[0,0]` rather than the real one.  This is
even flagged with a "sym_qsp real component means little" comment in
`pyqsp/response.py` line 258 — but that comment is easily missed and
the pyqsp docs do not clearly say "for odd parity, read Im[U[0,0]]".

**How I found it:** built a debug script (`work/debug_convention.py`)
that computes `pyqsp.SymmetricQSPProtocol.gen_unitary` on a scalar N=1
input and compares element-by-element to my `qsvt_unitary` output.
Perfect match — proving my circuit was right, my READ-OUT was wrong.
Then plotted `Im[U[0,0]](x)` vs. the target Chebyshev polynomial on a
dense sample of x, and they matched to machine precision.

**Fix:** read `Im[U_Phi[0,0]]_ii` (not `Re[...]`) for odd-parity
targets.  All 5 experiments then pass at 1e-16.

**Cost:** ~30 min — the biggest single time sink in this replication.
This is a strong signal for open question Q2.

## 4. Non-normal / QEVE path NOT exercised
The paper's core novelty is (a) non-Hermitian eigenvalue processing and
(b) the Chebyshev history-state generation subroutine that underlies it.
Neither is exercised in this replication.  We restricted to the paper's
own Hermitian-reduction "consistency" claim (QEVT ≡ QSVT on Hermitian
inputs, up to polylog factors), which the paper itself calls out
explicitly (Sec 1.4, ~line 1154).  This is why our verdict is PARTIAL,
not REPLICATED.

Building a non-Hermitian test would require:
- Implementing the block encoding of the (padded) `I + L^2 - 2*L*alpha*A`
  operator from Theorem 1.
- Implementing (classically simulating) a quantum linear system solver
  or at least an inverse via `numpy.linalg.solve` on the encoded matrix.
- Reconstructing the Chebyshev history state from the LSS output.
- Applying the Faber-basis QEVT sequence and verifying eigenvalue-wise
  action.

That is a multi-day effort minimum. It is captured in open question Q5.

## 5. Small residual: pyqsp version undetectable
`import pyqsp; pyqsp.__version__` raises AttributeError — no version
string is exported.  We recorded `pyqsp = git-latest, no __version__`
in the workflow. Not blocking but should be filed upstream.

## 6. Extraction fallbacks
Marker and Nougat were not installed in this environment (they require
torch + heavy vision-transformer weights, out of scope for the "free
endpoints only" constraint).  Both extraction artifacts use
`pdftotext` fallbacks (layout mode for the Marker slot, raw reading-
order for the Nougat slot), with an explicit disclaimer header.  This
mirrors the pattern used in other QC-200 replications
(e.g. QC-0808.0369, QC-0807.4994).

## Summary
Zero cascading failures.  Every failure mode above was diagnosed and
worked around within the replication window.  Final result: 5/5
experiments PASS at machine precision.  Total dead-end debugging time:
~50 min (items 1--3 above).
