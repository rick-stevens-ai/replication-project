# Replication Report — arXiv:1808.00128

**Paper:** *Simulation of quantum circuits by low-rank stabilizer decompositions*
Sergey Bravyi, Dan Browne, Padraic Calpin, Earl Campbell, David Gosset, Mark Howard.
*Quantum* 3, 181 (2019). arXiv:1808.00128v2.

**Set:** QC-100 · **Replicator:** OpenClaw subagent (Ollie) · **Date:** 2026-07-03
**Verdict: REPLICATED** — the paper's cleanest exact headline number, the stabilizer
extent **ξ(CCZ) = 16/9**, was reproduced *to machine precision from first principles*
by brute-force computation over the full 3-qubit stabilizer set, and cross-checked
three independent ways. Supporting analytic + algorithmic claims also reproduced.

---

## 1. Paper summary

The paper develops the theory of **stabilizer rank** χ and **stabilizer extent** ξ,
and a suite of classical simulators for Clifford + (few non-Clifford) circuits whose
runtime scales as `2^{α·m}` in the non-Clifford count m (times poly(n)), not `2^n`.
Central quantities:

- **Stabilizer fidelity** `F(ψ) = max_φ |⟨φ|ψ⟩|²` over stabilizer states φ.
- **Stabilizer extent** `ξ(ψ) = min ‖c‖₁²` over decompositions `ψ = Σ cα φα`.
- For a **Clifford magic state**, `ξ(ψ) = 1/F(ψ)` (Prop. 2).
- Sum-over-Cliffords simulation cost `Õ(δ⁻² · Πⱼ ξ(Vⱼ))` (Eq. 14).

Flagship exact values the paper derives:
`ξ(CCZ)=ξ(|CCZ⟩)=16/9` (Eq. 31), `ξ(R(θ))=(cos(θ/2)+tan(π/8)sin(θ/2))²` (Eq. 28),
`α = −2log₂cos(π/8) ≈ 0.23` (Eqs. 6/13).

## 2. Claims table

| ID | Claim | Type | Testable on CPU? | Tested here? | Result |
|----|-------|------|------------------|--------------|--------|
| C1 | **ξ(CCZ) = ξ(\|CCZ⟩) = 16/9** (Eq. 31) | exact number | ✅ (brute force over 1080 stab states) | ✅ | **MATCH (exact)** |
| C2 | \|CCZ⟩ is a Clifford magic state ⇒ ξ = 1/F, and F(\|CCZ⟩) achieved by \|+++⟩ (Prop. 2) | exact | ✅ | ✅ | **MATCH (exact)** |
| C3 | Eq. (30) 8-term Clifford decomposition of CCZ, ‖c‖₁ = 16/9 | exact | ✅ | ✅ | **MATCH** |
| C4 | ξ(T)=ξ(R(π/4)) closed form (Eq. 28) = 1/F(\|T⟩), rank-2 T=aI+bS | exact | ✅ | ✅ | **MATCH (3 ways, exact)** |
| C5 | α = −2log₂cos(π/8) ≈ 0.23 (T-count scaling exponent) | number | ✅ | ✅ | **MATCH (0.2284 → 0.23)** |
| C6 | Sum-over-Cliffords: U=ΣcⱼKⱼ (all Clifford) reproduces exact output; sampled k≪2^t → O(δ) error (Sec. 2.3.2) | algorithm | ✅ (small circuit) | ✅ | **MATCH (exact all-branch; O(δ) sampled)** |
| C7 | \|H^m⟩ sparse product-stabilizer decomposition, error decays with kept terms k (Eq. 7, Ref [11]) | algorithm | ✅ | ✅ | **MATCH (exact recon at k=2^m; monotone decay)** |
| C8 | Exact ranks χ(T^m)=1,2,3,4,5,7 then jump to 12 at m=7 (Ref [14]) | number | ✗ (full stab-rank search ≈ supercomputer per paper) | ✗ | not attempted (recorded as target) |
| C9 | 50-qubit QAOA / 40-64 T-gate Hidden Shift laptop simulations (χ~10⁶) | headline demo | partially (scale-limited) | ✗ (out of scope for minutes-scale run) | not attempted |

## 3. Method (exact, reproducible)

Tools: Python 3.14, **numpy 2.5.0** in `work/venv`. No paid endpoints; pure CPU.

```
cd QC-1808.00128-low-rank-stabilizer-decomposition
python3 -m venv work/venv && work/venv/bin/pip install numpy
work/venv/bin/python src/verify_extent.py      # C1–C5, C7-analytic  -> evidence/verify_extent_results.json
work/venv/bin/python src/verify_soc_sim.py     # C6 (corrected)       -> evidence/exp2_soc_corrected.json
work/venv/bin/python src/stabilizer_rank_sim.py# C7 H-state + alpha    -> evidence/exp1_*.json, verify_scaling.json
```

Key procedure for the headline (C1/C2):
1. **Enumerate all n-qubit stabilizer states** by BFS over the Clifford group
   (generators H_i, S_i, CNOT_{i,j} acting on |0…0⟩), deduping up to global phase.
   Recovered counts **6 (n=1)** and **1080 (n=3)** — matches the known formula exactly,
   validating the enumerator.
2. Build `|CCZ⟩ = CCZ|+++⟩`. Compute `F = max_φ |⟨φ|CCZ⟩|²` over all 1080 states.
3. Report `ξ = 1/F` and compare to 16/9; check `|+++⟩` overlap equals F.
4. Independently: verify Eq. (30)'s 8 Clifford operators reproduce the CCZ diagonal
   shape and give ‖c‖₁ = 8·(2/9) = 16/9.
5. For T: solve `T = a·I + b·S` exactly (a=1−b, b=(e^{iπ/4}−1)/(i−1)); check
   reconstruction, `(|a|+|b|)²`, Eq. (28) closed form, and `1/F(|T⟩)` all agree.

## 4. Results vs paper

| Quantity | Paper | This replication | Δ |
|----------|-------|------------------|---|
| ξ(CCZ) = 1/F(\|CCZ⟩) | 16/9 = 1.7777778 | **1.7777778** (F = 0.5625 = 9/16) | **0.0** |
| \|+++⟩ overlap with \|CCZ⟩ (= F) | = F (Prop. 2) | 0.5625 (= F exactly) | 0.0 |
| ‖c‖₁ of Eq. (30) \|CCZ⟩ decomp | 16/9 | 1.7777778 | 0.0 |
| ξ(T) = ξ(R(π/4)) | (cos π/8 + tan π/8 · sin π/8)² = 1.1715729 | **1.1715729** (3 independent methods) | ~1e-16 |
| T = aI+bS reconstruction err | exact | 1.1e-16 | machine ε |
| α = −2log₂cos(π/8) | ≈ 0.23 | **0.228447** | rounds to 0.23 |
| # stabilizer states n=1 / n=3 | 6 / 1080 | 6 / 1080 | 0 |
| Sum-over-Cliffords (all branches) vs statevector ⟨Z₀⟩, t=2..10 | exact equality | max err **1.7e-15** | machine ε |
| Sampled SoC (k≪2^t) ⟨Z₀⟩ error | O(δ) | 0.01–0.08 at k~10²  | consistent |

Evidence files (`report/evidence/`):
- `verify_extent_results.json` — C1–C5 (headline numbers), stab-state counts.
- `exp2_soc_corrected.json` — C6, corrected sum-over-Cliffords vs statevector.
- `exp1_H_decomposition.json`, `verify_scaling.json` — C7 H-state sparsification + α.
- `exp3_stab_rank_table.json` — C8 target values (not re-derived; see note).
- `exp2_runtime_scaling_SUPERSEDED_buggy_T_coeffs.json` — an earlier draft SoC run
  that used the **wrong** single-T coefficients `a=(1+e^{iπ/4})/2`; kept only for
  audit trail. Superseded by `exp2_soc_corrected.json` (correct exact solve). Do not
  cite the superseded file.

## 5. Verdict & justification

### REPLICATED

The single most-checkable exact headline number of the paper — the stabilizer extent
**ξ(CCZ) = 16/9** — was reproduced **exactly (Δ = 0.0)** by an independent, first-
principles brute-force computation: enumerate all 1080 three-qubit stabilizer states,
maximize the overlap with |CCZ⟩, obtain F = 9/16, hence ξ = 1/F = 16/9. Two further
independent routes (the |+++⟩-maximizer property of Prop. 2, and the ‖c‖₁ of the
explicit Eq. 30 Clifford decomposition) give the same value. The companion exact
number ξ(T) = 1.171573 reproduces to machine precision three independent ways, the
scaling exponent α = 0.2284 rounds to the paper's 0.23, and the underlying
sum-over-Cliffords decomposition reproduces exact statevector expectation values to
machine precision (with the k≪2^t importance-sampled version showing the promised
O(δ) accuracy). The stabilizer-state enumerator was validated against the known
6/1080 counts.

Not attempted (out of minutes-scale CPU scope, honestly flagged): the full
exact-rank search χ(T^m) (paper itself notes it required heavy compute), and the
flagship 50-qubit QAOA / 40–64-T-gate Hidden-Shift demonstrations at χ~10⁶. These
are performance demonstrations, not the analytic claims; the analytic backbone that
makes them possible (ξ values + the sum-over-Cliffords decomposition) is what we
verified, and it holds exactly.

**Confidence: high.** The core reproduced quantity is a closed-form rational number
matched to zero error via a method independent of the paper's derivation.

---
*All computations CPU-only, numpy 2.5.0. No external/LLM inference used for the
numerical results; free-endpoint policy respected.*
