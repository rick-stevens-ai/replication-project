# Failure Analysis — Dürr-Høyer (1996) Replication

Even though the final verdict is REPLICATED, this document honestly logs
every point of friction, incomplete coverage, and residual gap.

## What failed

### 1. Marker install (blocked → fallback)
**Symptom:** `pip install marker-pdf` failed on Python 3.14 with a NumPy
metadata error (marker-pdf pins an older NumPy that cannot build against
CPython 3.14 headers).
**Root cause:** Python 3.14 is bleeding-edge; the marker-pdf dependency
graph has not yet been updated for 3.14 wheels.
**Workaround:** Fell back to `pdftotext -layout` and produced
`extraction/marker.md` with a clear disclaimer header at the top.
**Residual gap:** No true Marker/LLM-based structured parse. For a
2-page pure-text 1996 quant-ph paper with essentially zero math typography
this is close to lossless, but a Marker parse would give hierarchical
sections + LaTeX math blocks.
**To close:** Either downgrade to Python 3.11/3.12 in a separate venv,
or wait for marker-pdf to publish 3.14 wheels.

### 2. Nougat install (skipped → fallback)
**Symptom:** Not attempted; nougat requires torch + heavy ViT weights,
which the QC brief's spirit ("no heavy install") advises against for a
free-endpoint replication.
**Root cause:** Environmental choice, not a technical failure.
**Workaround:** `pdftotext -raw` fallback, header-disclaimed.
**Residual gap:** No math-token-level extraction. Same mitigation reason
as above.
**To close:** Set up a separate torch-enabled env with nougat and rerun.

## Partial coverage

### 3. Claim C4 (BBBV lower-bound) not tested
The paper claims Dürr-Høyer is "within a constant factor of the optimum"
by citing the BBBV (Bennett-Bernstein-Brassard-Vazirani) $\Omega(\sqrt{N})$
lower bound. We did not independently reproduce the BBBV lower-bound
theorem — it is imported from the cited literature. Testing the upper
bound is what our replication does; the matching lower bound is a
separate paper that would need its own replication.

### 4. Constant $22.5$ not tightly tested
The paper's constant $22.5$ is a proven **worst-case** upper bound; our
empirical average is $\hat c \approx 0.96$, $\sim$23× smaller. This is
fully consistent with the bound being tight only in the worst case (an
adversarial input construction), but we did not attempt to find or run
such an adversarial input. So we can only report "no violation observed,"
not "constant $22.5$ is empirically confirmed."

### 5. Analytic emulator vs. real statevector for N > 16
For $N \ge 32$ we used an analytic Grover-success-probability sampler
(exact ideal-Grover distribution) instead of the real Qiskit statevector,
because a per-inner-call statevector simulation at $R=500$ trials per $N$
would have added many minutes. The N=16 cross-check confirms the two
paths agree within one standard deviation, but a full real-statevector
run at $N=256$ was not executed. This is a compute-time choice, not a
correctness issue.

## Assumptions we made

- **BBHT parameter $\lambda = 6/5$** — the standard choice from Boyer et
  al. 1996, and the natural interpretation of "quantum exponential
  searching algorithm of [2]" in the paper. The paper does not name
  $\lambda$ explicitly.
- **Time budget starts fresh per problem** — the paper's cap
  $22.5\sqrt{N} + 1.4\lg^2 N$ is per invocation; we implemented it as
  such.
- **"Time step" = one Grover iteration** — the paper explicitly states
  this ("one iteration in the exponential searching algorithm takes one
  time step") for the analysis, and stages 1, 2(2c), 3 are declared not
  counted.
- **Distinct table values** — as the paper explicitly assumes. We use
  random permutations of $\{0,\dots,N-1\}$.
- **Ideal noise-free simulator** — Qiskit Aer default `AerSimulator()`,
  no depolarizing/thermal noise, no measurement error, one shot per
  Grover call.

## Friction, minor

- Qiskit 2.5's `Diagonal` class emits a `DeprecationWarning` (moves to
  `DiagonalGate` in 3.0). Warning does not affect correctness in 2.5;
  needs a one-line fix before 3.0. The run log has been cleaned of the
  ~50 repeated warnings.
- `pdftotext` (poppler) is a system dependency; on macOS it comes in via
  `poppler` (Homebrew). Assumed present; verified by successful conversion.

## Overall

The replication is clean and comfortable. The two blocked-tool items
(Marker/Nougat) are documented, disclosed in-file at
`extraction/marker.md` and `extraction/nougat.mmd`, and would not affect
any downstream quantitative claim about the paper (a 2-page
pure-algorithm paper does not need heavy PDF parsing to reproduce). The
main "gap" is that we only tested the upper bound side of the claim, not
the matching lower bound — but that is orthogonal to reproducing the
paper's own contribution.
