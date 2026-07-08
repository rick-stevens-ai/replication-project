# Failure Analysis — QC-2206.12780 (Gidney pair-measurement pentagon surface code)

This document is the honest counterweight to the REPLICATED verdict. It
enumerates precisely what was **not** established, what shortcuts were
taken, and where the current replication is thinnest.

## 1. Independent reimplementation — NOT DONE

**Fact:** The `pentagonal_sharp`, `chao`, and `honeycomb` Stim circuits used
in Experiment B are the paper's own published circuits from Zenodo 6626417.
We did not reimplement any of them.

**Implication:** The 5-pair-measurement ZX decomposition of the 4-body
stabilizer, the Cairo-tiling scheduling, the detector definitions, and the
noise-model wiring are all **as constructed by Gidney**. Any correctness
error in the construction (misplaced detector, wrong Pauli frame, dropped
noise instruction, off-by-one in the schedule) would pass silently through
our decoder step, and we would still report a clean pentagon > chao
ordering — because both circuits are Gidney's.

**What genuine reimplementation would require:**
1. Re-derive the 5-pair decomposition from the 4-body stabilizer via ZX
   (or via an independent circuit-synthesis method).
2. Re-schedule the pair measurements on the Cairo pentagonal tiling.
3. Re-define detectors and observable stabilizers from scratch.
4. Compare our ideal-noise-free circuits to Gidney's at the gate level.
5. Then re-run the noise-swept Monte-Carlo.

None of that was done. The replication is a **decoder-level** replication,
not a **construction-level** one.

## 2. Numeric threshold NOT reproduced

**Claim in paper (C1):** chao threshold ≈ 0.2%, pentagon threshold ≈ 0.4%.

**What we did:** verified the ordering pentagon > chao at a fixed 12-point
$(d,p)$ grid.

**What we did NOT do:** fit a threshold. The 12 points do not straddle
either pair-measurement threshold cleanly (the paper's thresholds are at
0.2% and 0.4%; our lowest $p$ is 0.001, above chao's threshold estimate but
below pentagon's, and above the 0.4% pentagon threshold estimate). No
$d$-scaling analysis beyond $d\in\{5,7\}$ was performed. Extracting
threshold numerically requires $d\geq 9$, finer $p$ grids near the crossover,
and a proper crossing-point fit.

**Consequence:** C1's numerical part (0.2%, 0.4%) is **unverified**. Only
C1's ordering content is verified.

## 3. Canonical rotated-surface-code baseline comparison is QUALITATIVE

**What we did:** Experiment A recovers a ~1% MWPM threshold on Stim's
built-in `surface_code:rotated_memory_x` with uniform depolarizing noise.
Verdict-critical fact: this is materially above 0.4% pentagon threshold.

**Shortfall:** The noise model in Experiment A (uniform circuit-level
depolarizing on Stim's canonical rotated surface code) is **not** the same
noise model as in Experiment B (Gidney's specific pair-measurement noise on
his pair circuits). Cross-noise-model threshold comparison is qualitative,
not quantitative. The ``pair measurement costs ~half order of magnitude of
threshold'' story is *consistent* with our numbers but not *proven* by
them.

## 4. Connectivity / logical-per-physical trade-off NOT QUANTIFIED

**Claim in paper (C2):** teraquop footprint at $p=0.1\%$: pentagon ≈ 3000
qubits, chao ≈ 6000, honeycomb ≈ 1000.

**What we did:** nothing on this claim.

**Why:** teraquop-footprint numbers require distance sweeps up to $d\sim 19$,
Bayesian log-linear extrapolation of LER curves down to $10^{-12}$, and
proper uncertainty quantification. This is orders of magnitude more compute
than a spot-check window and was explicitly deferred.

**Consequence:** the physical-qubit-per-logical-qubit trade-off vs
canonical rotated surface code is **not verified**. The main
practical-motivation part of the paper is *taken on trust* here.

## 5. Low-$p$ crossover NOT TESTED

**Claim in paper (C3):** below $p\approx 0.03\%$, chao eventually beats
pentagon (bidirectional hook errors in pentagon).

**Why untested:** at $p<0.03\%$ and $d\geq 9$, LERs are $\sim 10^{-5}$ or
lower per shot — needs $\sim 10^{7}$–$10^{9}$ shots per point to resolve
above statistical noise. Not reachable in this window.

**Consequence:** the paper's own subtle caveat is unverified. If the
reader takes the ordering result at face value, they may miss this
regime shift.

## 6. Decoder choice inflates absolute LER

Our decoder is uncorrelated `pymatching` MWPM; the paper's is Fowler's
correlated internal MWPM. Uncorrelated is strictly weaker: it ignores
error-correlation structure that correlated MWPM exploits.

**Observed:** at low $p$, our LERs are ~2× the paper's; at moderate $p$,
~1.1×. This is the expected signature. But the gap means our absolute
numbers are **not usable** as an independent quantitative check on the
paper's absolute LERs — only on ordering.

## 7. Pair-measurement primitive as a native operation is ASSUMED

The paper (and our replication) charges one noise event per pair
measurement. Real hardware implements a pair measurement as a decomposed
sub-circuit (H + CNOT + MZ + reset), each step with its own error. Whether
any physical platform can actually deliver the assumed noise budget for
pair measurements is a physics question outside this simulation-level
work.

## 8. Statistical uncertainty NOT properly reported

Every LER cell in Experiment B is 20,000 shots. Where the observed LER is
~5e-3, the binomial standard error is roughly sqrt(0.005 × 0.995 / 20000)
≈ 5e-4 — about 10% of the point value. We report point estimates only, no
error bars. For the ordering headline this is fine (ratios are 0.25–0.90,
huge relative to statistical uncertainty), but for absolute agreement with
the paper the uncertainty is nontrivial and unreported.

## 9. Random seed NOT controlled across families

Each `stim.CompiledDetectorSampler(seed=…)` call uses a per-family seed but
the seeds are not documented per row in the JSON evidence. Full seed
provenance would require re-running with logged seeds. Not blocking for
Monte-Carlo statistics but a small hygiene gap.

## 10. What is honestly established

**Exactly one thing, sharply:** using an independent MWPM decoder on the
paper's own Stim circuits, `pentagonal_sharp` has strictly lower LER than
`chao` at all 12 tested $(d,p)$ points, with absolute LERs consistent with
the paper's within the known correlated-vs-uncorrelated decoder gap, and
the baseline unitary rotated surface code recovers its canonical ~1%
threshold.

**That is a legitimate but narrow replication.** It is not a from-scratch
reimplementation. It is not a numeric threshold reproduction. It is not a
teraquop-footprint reproduction. It is not a demonstration of the low-$p$
crossover. It does not vet the pair-measurement primitive against
hardware. It does not report error bars.

## 11. Recommended next replication passes (priority order)

1. **Numeric threshold fit** — add $d\in\{9,11\}$ at $p\in\{0.001, 0.002,
   0.003, 0.004\}$ for both chao and pentagon families. Fit thresholds.
   Verify 0.2% vs 0.4% (or refute).
2. **Independent circuit reimplementation** — re-derive the 5-pair ZX
   decomposition and independently construct the pentagon Stim circuit.
   Diff against Gidney's circuit gate-by-gate.
3. **Biased-noise sweep** (Open Question 1) — the most policy-relevant
   follow-up for hardware relevance.
4. **Teraquop extrapolation** — the actual practical claim (C2). Requires
   real GPU-scale sim budget.
5. **Low-$p$ crossover check** (C3) — the paper's own caveat, worth
   confirming or refuting.

## 12. Verdict boundary

The REPLICATED verdict applies **only** to the headline ordering claim
(pentagon LER < chao LER at matched (d, p) on identical circuits, decoded
independently). Any broader reading — "the paper's numbers are all
correct", "pentagon is production-ready", "teraquop numbers hold" — is
**not** supported by this replication and should be treated as unverified.
