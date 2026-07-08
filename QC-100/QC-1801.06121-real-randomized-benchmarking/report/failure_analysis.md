# Failure & Critique Analysis — arXiv:1801.06121 replication

**Scope of this document.** An honest audit of what this replication did
NOT establish, gaps between what the paper claims and what we tested, and
places where the verdict `REPLICATED` should be read with caveats.

## Overall verdict caveat
The verdict `REPLICATED` is defensible for the tractable single-qubit
operational core (group enumeration + decay-law fits under real-diagonal
noise), but the more theoretically interesting claims of the paper — the
sensitivity of real RB to chirality / $T$-type errors, and the orthogonal
2-design property for $n \geq 2$ — are corroborated only indirectly or
not at all.

## Specific gaps

### G1 — Fitting formula not independently rederived
- **Paper claims.** $F(m) = A + b^m B + c^m C$ (eq. 41/43) with closed-form
  fidelity formulas (eq. 34, 35) derived from the orthogonal-2-design
  twirl.
- **What we did.** Adopted the formulas as given; fit them to simulation
  output.
- **What we did not do.** Rederive the twirl integrals; verify the
  coefficient prefactors from first principles.
- **Impact.** Medium. If the paper's derivation is wrong (it isn't — well
  reviewed) the fit still succeeds because the functional form is right;
  but a stronger replication would carry the derivation independently.

### G2 — Only real-diagonal noise tested
- **Paper claims.** Real RB isolates the real-error component and is
  sensitive to chiral / $T$-type errors that standard RB averages away.
- **What we did.** Injected $p_X = p_Z = p/2$, $p_Y = 0$ — the "friendliest"
  channel for the theory.
- **What we did not do.** Inject $Y$-component noise, coherent
  $\exp(-i\theta Y)$ rotations, non-Markovian noise, amplitude damping, or
  any $T$-error surrogate.
- **Impact.** Large. This is the single biggest gap. The paper's main
  practical selling point (chirality sensitivity) was not exercised at all.
  See open question #1.

### G3 — Chirality / $T$-error sensitivity NOT DEMONSTRATED
- **Paper claims.** Real RB and standard RB disagree on chiral errors in a
  characterizable way; the disagreement can be used as a diagnostic.
- **What we did.** Nothing. Both protocols were only exercised on the
  channel where they should agree (once you strip out the $Y$-averaging).
- **What we did not do.** Provide any evidence of the disagreement claim.
- **Impact.** Large. The single most novel physical claim of the paper is
  untested in this replication.

### G4 — No comparison against standard Clifford RB under a chiral channel
- **What we did.** Compared them under a real-diagonal channel and
  confirmed the numeric offset ($f = 0.9737$ vs $b = 0.9795$).
- **What we did not do.** Show that the offset changes non-trivially in
  the presence of a chiral vs achiral error at matched infidelity.
- **Impact.** Medium-large; couples with G2 and G3.

### G5 — Small-$n$ / small-$M$ bias untested
- **What we did.** Reported one-shot fit estimates with SEM from
  `scipy.optimize.curve_fit`.
- **What we did not do.** Bootstrap; check bias by repeating the whole
  experiment many times; check bias in $\hat b$ as $M$ shrinks; check
  bias from finite sequence-length range $m \leq 150$.
- **Impact.** Small on the qualitative story, potentially medium on any
  claim about uncertainty quantification.

### G6 — 2-design property only tested indirectly
- **What we did.** Inferred the 2-design property held because the
  predicted decay law fit.
- **What we did not do.** Directly compute the twirl-average
  $\int_{\mathcal{C}} U^{\otimes 2} \rho (U^\dagger)^{\otimes 2}\,dU$ and
  compare to the orthogonal-group Haar twirl.
- **Impact.** Small for $n = 1$ (theorem well-established), medium if one
  wanted to extend to $n \geq 2$ with confidence.

### G7 — Multi-qubit and $[[4,2,2]]$ scope not touched
- **Paper motivation.** Benchmarking fault-tolerant gates in codes without
  transversal full Clifford, e.g.\ $[[4,2,2]]$.
- **What we did.** Nothing at $n \geq 2$.
- **What we did not do.** Enumerate the two-qubit real Clifford group;
  build a stabilizer-code simulation; test the two-branch fit in a
  regime where $c \ne 0$.
- **Impact.** Large for the paper's applied motivation; expected for a
  QC-100 single-qubit wave.

### G8 — Sequence-count budget is small
- **What we did.** $M = 30$ (baseline) and $M = 10$ (efficiency).
- **What we did not do.** Push to $M = 100$+; measure the point at which
  reduced-sequence real RB starts to visibly degrade.
- **Impact.** Small; the C5 efficiency claim was verified at one budget
  ratio.

## Confidence table (self-assessed)

| Claim | Status | Confidence |
|-------|--------|------------|
| C1: $|\mathcal{C}(1)_{\text{real}}| = 8$ | Verified | 100% |
| C2: $|\mathcal{C}(1)_{\text{complex}}| = 24$ | Verified | 100% |
| C3: Real-RB decay single-exponential under real-diag.\ noise | Verified | 95% |
| C4: Real-RB $b \ne$ standard-RB $f$ for real-diag.\ noise | Verified | 95% |
| C5: Efficiency claim (same precision at $8/24$ sequence ratio) | Verified | 85% |
| C6: 2-design for all $n$ | Not directly tested | 60% (theorem trusted) |
| C7: $[[4,2,2]]$ code-space application | Not attempted | n/a |
| **Chirality sensitivity (paper's flagship physical claim)** | **NOT TESTED** | **0%** |

## What would upgrade this from REPLICATED to STRONGLY REPLICATED
1. Run the matched-infidelity chiral-vs-achiral experiment (open question #1).
2. Enumerate the $n = 2$ real Clifford group and run bi-exponential fits
   (open question #2).
3. Bootstrap the fits and report bias.
4. Directly compute the 2-design twirl for $n = 1, 2$ and compare to the
   orthogonal Haar twirl.

Until then, the replication is honest at the operational $n = 1$ level and
should not be over-claimed as a validation of the paper's physical
sensitivity story.
