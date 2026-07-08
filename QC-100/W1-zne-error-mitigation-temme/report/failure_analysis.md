# Failure Analysis — QC-100 / W1 (Temme, Bravyi, Gambetta 2017; ZNE)

Honest critique of what this replication does and does not establish.
Written to complement — not soften — the top-level `REPORT.md`.

## 1. What was NOT independently reproduced

### 1.1 Paper's specific circuit + noise model

The paper's headline experimental figure is a small IBM-Yorktown
superconducting-qubit demonstration in which a specific two-qubit
observable is measured under the *device's actual* noise channel
(amplitude damping + dephasing + crosstalk + coherent errors, extracted
via gate-set tomography). **We did not run that.** We ran a 2-qubit Bell
circuit under a symmetric depolarizing channel — a friendlier, more
symmetric, and provably-polynomial-in-`c` noise process. The
methodological claim of the paper survives; the *experimental* claim
does not, because we tested against a different (easier) noise model.

### 1.2 Paper's quoted mitigated numbers

The paper reports specific hardware-mitigated expectation values with
residual errors around `1e-2`. Our Richardson result is `~1e-16`
(machine precision), which is *not* a match to the paper's hardware
numbers — it is what the algorithm would give in an idealized universe
where the noise is exactly polynomial in the stretch factor. We are
therefore *not* claiming quantitative agreement with the paper's
hardware table; we are claiming the algorithm behaves as the paper says
it will on a controlled input. This distinction is important and easy
to miss.

The realistic figure of merit from our run is the
**linear-extrapolation** result: **22x reduction** in expectation-value
error at `p0 = 0.02`. That is the number to compare against future
non-idealized reruns.

### 1.3 Baseline comparison — done

A no-mitigation baseline (`c=1` raw noisy expectation value) was
measured for every reported point, and reduction factors are always
quoted against it. This is the correct comparison. There is no
implicit tuning against a hidden baseline.

### 1.4 Richardson quantitative claim — held only in the polynomial regime

The paper's Richardson claim is order-by-order bias cancellation:
`k` scale points cancel the leading `k-1` orders in `lambda_0`. Our
base-rate sweep (five `p0` values over `16x` dynamic range) confirms
this exactly in the polynomial regime — raw error is linear in `p0`,
Richardson-`k` collapses to numerical zero at every base rate. The
sweep does NOT test the assumption failure mode (non-polynomial
noise), where the paper's own numbers imply Richardson would leave
residual error of order `1e-2`. So the claim is confirmed only under
the idealization the simulator provides.

## 2. Where we cut corners

- **No sampling noise.** The density-matrix simulator computes expectation
  values analytically. On real hardware the shot budget interacts with
  ZNE (Richardson amplifies variance of the estimator by a factor that
  grows quickly with the number of scale points). We did not measure
  that variance blowup.
- **No unitary folding.** We implemented noise amplification as
  `p_eff(c) = c * p0`, not as `G -> G G^dagger G`-style unitary folding.
  Real hardware ZNE uses folding, which introduces coherent-error
  residuals we did not model.
- **PEC entirely omitted.** Half the paper's empirical content is
  absent. The verdict correctly reflects this via Coverage = 6/10.
- **No `extraction/nougat.mmd`.** The paper was ingested manually into
  `paper.md` at replication time; a Nougat re-extraction was not run.
  The `nougat.mmd` file in this backfill is a stub explaining that
  status, not an actual Nougat output.

## 3. What would flip the verdict from PARTIAL to REPLICATED

Any single one of the following would meaningfully upgrade the verdict:

1. Reproduce the ZNE result under a **non-polynomial** noise model
   (amplitude damping + coherent single-qubit rotation error) and show
   Richardson still gives a well-defined error reduction. This tests
   the paper's real-world claim, not just the algebra.
2. Add a **PEC** implementation (even a small one-qubit demonstration
   with a documented quasi-probability decomposition of an ideal gate
   into noisy implementable operations). This closes the second half
   of the paper's methodological contribution.
3. Run on **real hardware** (IBM Q free tier, or any noisy backend)
   and reproduce the paper's ordering: mitigated < unmitigated by a
   factor of a few. This closes the experimental gap.

Because none of these were done, PARTIAL is the correct verdict.

## 4. Verdict cross-check

**Verdict preserved: PARTIAL.** The queue metadata initially said
REPLICATED, but a substance check against the headline-exercised rule
finds:
- Headline algorithmic claim (Richardson-extrapolated bias reduction):
  **exercised on a simplified simulator, matches qualitatively.**
- Headline experimental claim (hardware-observed reduction of expectation-
  value error on a real superconducting device): **not exercised at all.**
- PEC (second methodological pillar): **not exercised.**

Only one of the paper's two methodological pillars was independently
reimplemented and only in an idealized noise regime, so PARTIAL is the
faithful verdict. Marking this as REPLICATED would misrepresent the
strength of the reproduction to any downstream reader.
