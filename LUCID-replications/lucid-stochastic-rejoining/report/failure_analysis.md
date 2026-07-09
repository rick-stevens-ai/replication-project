# Failure Analysis — lucid-stochastic-rejoining

Honest critique of what did NOT work, where the reproduction is thin, and what residual
uncertainty remains behind the STRONG headline verdict. This is not a whitewash.

## 1. Where the reproduction is genuinely strong

Before enumerating gaps: the mean-behaviour reproduction is genuine. The
$L^\ast$ threshold, biphasic kinetics, $k_3$ regime split, and secondary
$L^\ast/m$ jump all reproduce with quantitative agreement using an independent
reimplementation from paper equations only. That is not in dispute.

## 2. Variance IS reported — but no formal CIs

**Good:** Unlike master-equation or deterministic-ODE reproductions, our Gillespie SSA
naturally exposes per-trajectory variance. Every REPASS-1 claim quotes std or
(max$-$min) spread from 150 runs per point (C12) or 30 runs per grid cell (C11).

**Gap:** We do NOT compute formal 95% confidence intervals. We do NOT bootstrap.
The "2.95× std ratio" and "3.20× spread ratio" at C12 are point estimates without
error bars on the ratio itself. A rigorous statistical claim would use a bootstrap CI
on the ratio and report whether the 95% CI excludes 1.0 (it almost certainly does,
but we did not verify).

**Recommended fix:** Add a `code/repass1/bootstrap_ci.py` that resamples the raw
per-run T-values from C12 and reports 95% CI on the std ratio. Estimated effort: 1 h.

## 3. Misrejoining probability: inherited from paper, not stress-tested

**Gap:** The paper's misrejoining is folded into fragment-class transitions (short pairs
→ residue $R$, mixed → residue $r$). Our reimplementation adopts these class labels
but does NOT independently fit a misrejoining probability against wet-lab aberration
data (e.g. dicentric frequency vs dose).

**Consequence:** The claim "mis-rejoining is enhanced under high-LET" is reproduced
STRUCTURALLY (via C8 + C5) — it is a logical consequence of shorter fragments $\Rightarrow$
more residues formed $\Rightarrow$ more Ku-blocked ends per fragment — but NOT
quantitatively cross-checked against experiment. If the paper's residue-formation rules
were rewritten (e.g. mixed pairs also succeed sometimes), the biological punchline could
weaken without any of our tests catching it.

**Recommended fix:** Score joins by (source-chromosome, target-chromosome, orientation)
tuples and translate to a dicentric-frequency prediction; compare to Cornforth-Bedford
or Loucas 2013 dose-response curves. This is Q5 in open questions. Estimated effort: 8 h.

## 4. C10 discrepancy: honestly flagged, not analytically resolved

We measured recruit count $\approx 2.58 M_T$ in the long-only regime, disagreeing with
the paper's stated $2 M_T$. We argued (§10 of REPORT.md) that the paper's number is an
informal upper bound because bound Ku is released on the $X^E + X^E \to X$ join
reaction, forcing re-recruitment on intermediates. We hand-waved a $4 M_T - 4$
deterministic upper bound.

**Gap:** We did NOT derive the exact expected recruit count analytically. The true
expected number could be computed as a sum over trajectory tree probabilities weighted
by recruit-count per branch, but we chose not to do that work. Consequently, we cannot
say definitively whether 2.58 is the correct expectation or an artifact of finite
sample size (150 runs). We could not distinguish a paper typo from a rigorous but
tighter closed-form value like $8/3 \cdot M_T \approx 2.67 M_T$.

**Recommended fix:** Write out the coupled ODE for expected recruit count vs time and
solve numerically; compare against SSA at 10× the sample size. Estimated effort: 4 h.

## 5. C11 axis asymmetry: real, but weakly characterised

Pearson correlations of 0.39 (r1) vs 0.89 (r2) reveal Fig 3(d)'s surface is strongly
$r_2$-dominated. We flagged this as a paper-side omission but did not go deeper.

**Gap:** We did NOT test whether the asymmetry survives at higher M_T (our grid used
M_T=40). If asymmetry weakens with larger M_T, the paper's symmetric-looking Fig 3(d)
might be plotted at a different M_T where the effect is closer to symmetric.

**Gap:** We used a 6×6 grid (36 points, 30 runs each = 1080 SSA runs). The paper's
Fig 3(d) resolution is not stated but likely finer.

**Recommended fix:** Rerun C11 at M_T ∈ {40, 80, 160, 320} to check M_T-dependence of
axis asymmetry. Estimated effort: 2 h (embarrassingly parallel).

## 6. C7 deferred: wet-lab calibration missing

The paper's most externally-verifiable claim — quantitative match to Asaithamby et al.
2011 53BP1 foci kinetics for iron ions — is deferred because those data are only in
Fig 4 scatter form (not tabulated). We reproduced the model's own kinetic shape as
C7-revisit but did NOT anchor the absolute time axis to wet-lab measurements.

**Consequence:** We cannot confirm the paper's biological time scale is right. The
kinetics have the right shape; whether they match real 53BP1 dissolution half-lives
of ~30 min / ~6 h under 1 GeV/u Fe is untested.

**Recommended fix:** WebPlotDigitizer on Asaithamby 2011 Fig 4 green points → fit our
model's τ_fast and τ_slow to match those numbers; report residuals. Estimated effort: 3 h.

## 7. Well-mixed spatial assumption inherited wholesale

The paper's rate law $k_2/V$ assumes fragments and Ku are well-mixed in nuclear volume
V. Real DSB endpoints diffuse only ~0.5 μm²/s and are confined to chromosome
territories. If diffusion is limiting, the paper's whole $L^\ast$ machinery could be an
artifact of the well-mixed assumption.

**Gap:** We did NOT stress-test this. We reproduced the paper faithfully, including its
spatial simplification. Whether the $L^\ast$ jump survives a spatially-resolved model
is an OPEN scientific question (Q4 in open questions), not a replication question.

## 8. Author code unavailable — cannot byte-verify

Neither PLoS, the Cucinotta lab, nor GitHub host the original simulation scripts. Our
reimplementation is from the paper's equations only.

**Gap:** We cannot rule out that some quantitative subtleties (the 2.58 vs 2 recruit
count, the r1 vs r2 axis asymmetry) reflect implementation choices we made differently
from the authors. Emailing Cucinotta (the corresponding author) for the original scripts
would let us cross-check.

**Note:** This is not a failure per se — independent reimplementation is stronger
evidence of reproducibility than a byte-for-byte code re-run. But we should acknowledge
that some paper-side vs implementation-side ambiguities cannot be resolved without
author code.

## 9. Numerics

**Small potatoes but real:** We use a linear-scan weighted-choice sampler ($O(N)$ per
event). Adequate for $M_T \leq 50$ (paper's largest tested case), inadequate for
$M_T \geq 500$. If a reviewer asked "does the $L^\ast$ threshold survive at $M_T=1000$?",
we would need to first swap in a priority queue or tree-based sampler.

## 10. What the STRONG verdict does NOT mean

The STRONG label means: the paper's stated claims reproduce with quantitative agreement
within the paper's stated scope, using our independent implementation.

STRONG does NOT mean:
- The biological narrative is confirmed against wet-lab data (C7 deferred).
- The mis-rejoining $\to$ chromosome-aberration $\to$ cell-death chain is quantified
  (Q5 open).
- The well-mixed assumption is validated (Q4 open).
- The paper is bug-free (we found a paper-side simplification at C10 and axis
  asymmetry at C11).
- All implementations would agree with ours (author code unavailable; cannot
  byte-verify).

## 11. Residual uncertainty summary

| Concern | Severity | Confidence in verdict |
|---------|----------|-----------------------|
| No formal CIs on ratios | low | STRONG survives |
| Misrejoining not fit to wet-lab | medium | STRONG in-scope only |
| C10 not analytically resolved | low | PARTIAL correctly flagged |
| C11 axis asymmetry undercharacterised | low | PARTIAL correctly flagged |
| C7 deferred (foci data not digitized) | medium | DEFERRED correctly labeled |
| Well-mixed spatial assumption | medium | inherited from paper, out of scope |
| Author code unavailable | low | intrinsic to any independent replication |
| Numerics scale to M_T=50 only | low | matches paper's own scope |

**Bottom line:** the reproduction is honest and STRONG within scope. The chief
weaknesses are (a) no formal CIs, (b) misrejoining not fit to wet-lab, (c) no
spatial geometry. These are all scope limits, not replication failures.
