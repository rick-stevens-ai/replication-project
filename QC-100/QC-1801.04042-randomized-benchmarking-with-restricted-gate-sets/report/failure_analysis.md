# Failure Analysis / Honest Critique — QC-1801.04042

**Verdict stands: REPLICATED.** But an honest replication requires listing what was NOT tested, where the evidence is weaker than it looks, and what a determined critic would attack.

## 1. Things that were genuinely independently implemented ✅
- Random-walk sampling of the real-Clifford and CNOT+Pauli subgroups (Stim tableau composition of {H, CNOT, X, Y, Z} or {CNOT, X, Y, Z} with walk_len=60).
- Gate-independent Pauli noise insertion (`DEPOLARIZE1(p_dep)`, `Z_ERROR(p_z)`) after every sampled group element.
- Ideal recovery gate computed via `stim.Tableau.inverse()`.
- Non-linear least-squares fit of `f(m) = A·λ^m + B` from single-shot binomial survival.
- Bootstrap error bars (300 resamples over 250 sequences) for the load-bearing cases.
- All theory formulas transcribed from paper's Eqs. in §III.A / §III.B and re-derived from Pauli-block partition; not copy-pasted from any reference code (no reference code exists — this appears to be the first published-scale numerical verification).

## 2. Formula tautology to watch for
Under **symmetric depolarizing noise** every non-identity Pauli receives equal weight → per-block error mass p_i / N_i is uniform → all block eigenvalues λ_1 = λ_2 = λ_3 = λ_4 collapse to a single value = the standard-Clifford λ = 1 - p·4^n/(4^n-1). So the four "symmetric" experiments (Exps 1, 2, 3a, 3b) do NOT independently probe the block structure — they only verify that the sampling and fitting pipeline gives correct standard-RB λ regardless of which subgroup was sampled. Reader should not overweight the four-way agreement in §4.1 of REPORT.md as evidence of multi-exponential physics.

The **actual load-bearing evidence** is the asymmetric pure-Z experiment in §4.2, where the same physical noise gives λ_1 = 1 (flat) from |00⟩ and λ_2 = 0.94672 ± 0.00758 (theory 0.94720) from |++⟩. This is the test that could have failed and did not.

## 3. What was NOT tested (honest scope)

### 3a. n=2 only
The paper's formulas are stated for arbitrary n. Only n=2 tested here. At n=3,4 the block-size asymmetry (4^n+2^n)/2 vs (4^n-2^n)/2 diverges more; multi-exponential residuals from mildly asymmetric noise become more visible. Not simulated. Runtime, not any theoretical obstacle.

### 3b. Pauli noise only
`DEPOLARIZE1` and `Z_ERROR` are Pauli channels; both fit inside the paper's gate-independent-Pauli-noise assumption. Real hardware error is roughly half coherent (over-rotations, cross-talk); the restricted subgroups lack the full 2-design property that lets standard Clifford RB Pauli-approximate coherent errors. Whether the block eigenvalue formulas survive small R_z(θ) coherent errors is UNKNOWN from this work. Would need a density-matrix (non-stabilizer) simulator or noisy_unitary path.

### 3c. Random-walk uniformity is empirical
Subgroup sampling uses random walks of 60 generator applications. Stationary distribution of these walks is the uniform distribution on the subgroup (walks are ergodic on the connected Cayley graph), but the **mixing time** was not formally bounded. Justification is empirical: fitted λ matches twirled-theory value → subgroup was sufficiently mixed. A formal spectral-gap analysis, or direct enumeration+uniform sampling of the finite subgroup, would strengthen this. At n=2 the real-Clifford subgroup has order 1152 and CNOT+Pauli has order 384 — both enumerable, but not done here.

### 3d. Gate-dependent noise unmodeled
The paper's scalar-block-eigenvalue framework assumes each subgroup element has the SAME error channel (gate-independent). Real hardware often has gate-dependent noise (e.g. CNOT ~10× noisier than single-qubit). This would replace scalar λ_i with a distribution over λ's, and block eigenvalues become effective averages. Untested here.

### 3e. Statistical resolution
Low-stats (N_seq=60) runs have σ_λ ≈ 0.01. The 0.006–0.011 gaps between fit and theory in §4.1 of REPORT.md are within this noise floor — we cannot resolve any sub-1σ physics from those runs, and the hi-stats reruns confirmed the gaps were sampling, not systematic.

### 3f. No external cross-check
Nobody else has (to our knowledge) numerically verified the Brown-Eastin formulas. No second independent codebase exists to compare against. Our numerics could share a common bug with our theory transcription — the two are independent within our workflow but not against the wider field. The pure-Z asymmetric test partly mitigates this because the prediction (λ_1=1 exactly) is a hard falsifier, but does not fully substitute for external replication.

## 4. What could still be wrong
- **If theory transcription is wrong** the fit-vs-theory agreement is spurious. Mitigation: two of us re-derived p_i = N_i·p/(4^n-1) independently and got the same block sizes; the standard-Clifford formula λ = 1 - p·4^n/(4^n-1) matches Magesan-Gambetta-Emerson 2011 verbatim; the |++⟩ prediction λ_2 = 1 - p·4/3 = 0.9472 was pre-registered before running the asymmetric test.
- **If random-walk walks are too short** at some n the fitted λ would drift off theory. Empirically at n=2, walk_len=60 gave <1σ agreement — no evidence of insufficient mixing, but not formally ruled out for higher n.
- **If Stim's `Z_ERROR` semantics differ** from the standard "with prob p_z, insert Z" the pure-Z prediction would fail. Cross-checked against Stim docs and against hand-derivation of the |++⟩ RB curve for a single-gate case.

## 5. What would make this stronger
Ordered by cost:
1. Enumerate the n=2 real-Clifford (order 1152) and CNOT+Pauli (order 384) subgroups; sample uniformly instead of walking. Removes 3c entirely. ~1 day of Stim work.
2. Extend to n=3 with same walk-based sampling; report fit-vs-theory table. Removes 3a. ~1 day.
3. Add coherent-error stress test (Qiskit statevector for n=2 tractable). Addresses 3b. ~2 days.
4. Character-RB layered on top (see `open_questions.json` Q3): resolves all block λ's from a single initial state, a genuinely more discriminating test than the paper's protocol.
5. Compare to a second independent implementation if one appears in the literature.

## 6. Bottom line
The replication is honest about scope: closed-form claims at n=2 under Pauli noise are verified; the asymmetric pure-Z test provides genuinely independent evidence of the block-selection prediction to 0.06σ. Everything outside that scope (higher n, coherent errors, gate-dependent noise, formally uniform subgroup sampling) is untested. The paper's central theoretical contribution stands under the conditions actually tested.
