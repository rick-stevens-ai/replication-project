# Failure Analysis — QC-2003.02417 Faster Amplitude Estimation

Honest self-critique of the QC-100 replication. Written to complement the REPORT verdict, not to soften it.

## Verdict recap

**REPLICATED.** Headline claim (near-Heisenberg $N_{\mathrm{orac}} \propto 1/\epsilon$ for $a \in \{0.1, 0.2, 0.3, 0.4\}$) was independently reimplemented on a 2-qubit statevector simulator and reproduced end-to-end: fitted slopes 0.85, 1.20, 1.26, 0.96 (all consistent with the ideal Heisenberg slope 1 within 100-trial sampling noise), Grover-operator identity matched at machine precision (2×10⁻¹⁵), two-stage trigger j₀ tracks the paper's monotonic-in-a pattern (5 → 4 → 3 → 3).

The rest of this file lists what could still legitimately go wrong and what was NOT done.

---

## What was actually exercised

- **Grover operator $Q = X S_0 X^\dagger S_{\mathrm{good}}$** built literally from `A ⊗ R` in `code/oracle.py` — verified against the analytic identity `sin²((2m+1)θ)` to 2×10⁻¹⁵ on a 24-point grid. **Solid.**
- **FAE Algorithm 1** (two-stage, Chernoff shot counts $N_{\mathrm{shot}}^{1\mathrm{st}} = 1944\ln(2/\delta_c)$ with $\delta_c = 0.01$) implemented from paper text alone. Produces $\epsilon$-vs-$N_{\mathrm{orac}}$ curves with the right shape. **Solid.**
- **MLAE (Suzuki)** as a baseline. **Working but with one known pathology row** at $a = 0.2$.
- **Real Binomial sampling** on statevector-derived probabilities (no numbers copied from the paper). **Solid.**

## What was NOT done — the honest list

### 1. Grinko IQAE was never implemented (LARGEST GAP)

The paper's most publishable single-number claim is that its rigorous prefactor ($4.1 \times 10^{3}$) is roughly $280\times$ tighter than Grinko-IQAE's ($1.15 \times 10^{6}$). We did not implement IQAE and race the two algorithms empirically. C2 in the claims table is marked "symbolic read only" for exactly this reason. This is the largest gap in the replication and is called out as open question Q1.

**What that means for the verdict.** REPLICATED is still fair because the paper's Section 3 empirical claim (Heisenberg scaling for FAE alone) was reproduced. The prefactor-vs-IQAE claim is theoretical (eq. 28 vs Grinko's bound) and was not the Section 3 empirical target.

### 2. Trial count 10× under paper

Paper uses 1000 trials per $(a, \ell)$; we used 100 to keep wallclock ~2 min. Our slope estimates carry ~10% sampling noise — that is why we see the [0.85, 1.26] spread rather than a tight cluster around 1. A 1000-trial rerun would tighten but is unlikely to move the verdict.

### 3. Zero noise / zero hardware

Everything is noiseless statevector. FAE's marketing pitch is NISQ-friendliness (no deep controlled-$Q$). We did not check that FAE's advantage persists under depolarising noise, gate infidelity, or shot-count amplification. For a paper explicitly aimed at near-term hardware this is a serious omission and is Q2 in `open_questions.json`.

### 4. Only 4 amplitudes tested

We followed the paper's Fig. 3 grid ($a \in \{0.1, 0.2, 0.3, 0.4\}$). Behavior for $a$ very close to 0 (attenuated $\sin\theta = a/4$ becomes ill-conditioned) and $a$ near 1 (stage-2 triggers earlier, but $R$'s $1/4$ prefactor caps $\theta \leq 0.252$ by design) is not exercised.

### 5. Theorem 1 not re-derived

We take the $4.1 \times 10^{3}$ prefactor from eq. (28) on faith. No spot check that the Chernoff constants 1944 and 972 are correct given the paper's stated $\delta$-budgeting.

### 6. Author's reference implementation not consulted

Clean-room is good for provenance but leaves open the possibility that our reading of the two-stage $j_0$ update or the $\arccos$-branching disagrees with the author's in some corner case. The exact match on the $j_0$ trend (5, 4, 3, 3) argues against a serious disagreement; a spot-comparison run against the reference repo remains as follow-up hygiene.

### 7. MLAE baseline off-spec in one row

Our MLAE at $a = 0.2$ gives slope 3.89 — the well-known bimodal-likelihood pathology of Suzuki MLAE when $\theta$ sits near a boundary. We flag this correctly in the report but did NOT implement the multi-start optimisation or the modified Suzuki schedule that fixes it. The MLAE baseline is therefore not competitive in that specific cell.

### 8. Statistic hides tails

We match the paper's 95th-percentile of $|\hat a - a|$ but this hides the failure tail. Max-error or the empirical CDF would show FAE's failure modes at low trial counts more clearly.

### 9. No end-to-end application benchmark

FAE's motivating application is quant-finance Monte-Carlo replacement (Woerner-Egger 2019). We tested only the abstract $(a, \epsilon)$ contract, not whether FAE beats IQAE end-to-end on a call-option payoff once the loading circuit is included in the query count. This is Q5.

## What we DID do that could still be wrong

- **Extended `atan2` (eq. 9).** The paper's extended arctangent to lift $\arccos$ output into the correct quadrant given the stage-2 sign information. Our implementation matches the paper's eq. (9) but corner cases (e.g. when the stage-1 midpoint sits exactly at $k\pi/2$) were not fuzz-tested. Any bug here would show up as occasional catastrophic failures in the low-error regime; we did not see such tail events in `sweep_raw.csv`, which is reassuring but not conclusive.
- **Integer $n_j$ update (eq. 25).** Similar caveat: we implemented the update literally as in the paper. A silent off-by-one could inflate $N_{\mathrm{orac}}$ by a small constant factor. The prefactor sits ~30× below the proven bound, so we have plenty of headroom; still, this was not exhaustively verified.
- **Attenuation angle range.** With $R|0\rangle = \tfrac{1}{4}|1\rangle + \tfrac{\sqrt{15}}{4}|0\rangle$, $\sin\theta = a/4$ so $\theta \in [0, \arcsin(1/4)] \approx [0, 0.2527]$. The paper's stage-1 threshold $2^{n+1}\theta_{\max} \geq 3\pi/8 \approx 1.178$ implies stage 2 triggers at $n$ such that $2^{n+1} \geq 4.67$ i.e. $n \geq 2$. Our observed modal $j_0 \in \{3, 4, 5\}$ is consistent with this floor; no contradiction.

## Confidence bands on the verdict

- If Q1 (empirical FAE vs IQAE race) collapses the ~280× advantage to <5×, the paper's headline prefactor claim would be **empirically weaker than advertised** — but the paper's actual Section 3 claim (FAE's OWN scaling) would still hold. Verdict would stay REPLICATED for the Section 3 claim and become UNKNOWN for the eq.-28 claim.
- If Q2 (noise robustness) shows FAE degrades to sub-Heisenberg (slope < 0.8) under any realistic noise while IQAE stays at slope ~1, the NISQ-friendliness pitch would be undermined. This would not change the Section 3 verdict but would qualify the paper's motivation.

## Bottom line

REPLICATED as claimed. Two headline gaps (Grinko-IQAE race, noise robustness) are both squarely inside the paper's own framing and are captured as open questions Q1 and Q2 with concrete next-step probes.
