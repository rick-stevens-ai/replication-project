# Failure analysis — quant-ph/0301023 replication

Even though the overall verdict is **REPLICATED**, the following friction / gaps
are worth being honest about:

## Actual failures during the run

### F1. `marker-pdf` install failed (PEP-668)
- **Attempted:** `pip3 install --user marker-pdf`.
- **Failed with:** externally-managed-environment error (PEP-668) on the host
  Python 3.13, and no pre-existing `marker` conda env on this machine (there is
  a `nougat` env, but not `marker`).
- **Workaround:** used `pdftotext` (poppler) to produce
  `extraction/marker.md` and prefixed it with a header explaining it is a
  text-only fallback of the same PDF, not a true marker parse. Nougat still ran
  and produced the true `.mmd` LaTeX-preserving parse.
- **Residual gap:** the marker.md file lacks figure/table structural markup and
  section headers a real marker parse would emit. For this specific paper
  (theory paper with no figures — only equations and one algorithm box), this
  is a minor loss; nougat.mmd covers the LaTeX-heavy content.

### F2. First simulator run was too slow
- **Symptom:** initial version used `scipy.linalg.expm(-1j * H * dt)` on the
  full 256×256 complex matrix inside the T-loop. Timed out at the 300 s bash
  timeout. (Later measurement showed ~226 ms per expm call, so 3140 calls =
  ~11 min minimum.)
- **Fix:** replaced with (a) Hermitian eigendecomposition propagator
  `V exp(-i Λ dt) V†` (~5× faster), and (b) 2D-invariant-subspace projection
  (span of `|+^n⟩` and `|ψ_target⟩` is `H(s)`-invariant and contains the initial
  state, so all dynamics can be done exactly as 2×2 unitaries). New wall = 15 s.
- **Verified equivalence** to full 256-dim dynamics: `‖ψ_2d − ψ_full‖ = 1.7e-14`,
  fidelity difference 3.8e-15.
- **Residual:** none — the shortcut is a mathematical identity, not an
  approximation.

## Modeling / scope gaps (things NOT reproduced)

### G1. Dense projector `H_1 = I − |ψ⟩⟨ψ|` is not row-sparse
- The paper's Sparse Hamiltonian Lemma requires row-sparse row-computable H
  for efficient simulation. Our `H_1` is dense in the computational basis
  (a rank-1 perturbation of I, but every entry is nonzero for a general `|ψ⟩`).
- We did NOT construct the sparse surrogate that would let the actual paper's
  algorithm run on real hardware. Our numerics correctly test the adiabatic-
  evolution mechanism given the ideal `H_1`, but do NOT test that `H_1` itself
  is efficiently simulatable. (Open question Q2 in `open_questions.json`.)

### G2. Dense initial `H_0 = I − |+^n⟩⟨+^n|` instead of local transverse field
- More natural / physical choice would be `H_0 = ∑_i (I − X_i)/2` (Farhi-style
  Grover initial Hamiltonian, 1-local, sparse, same ground state). We used the
  dense projector for symmetry with `H_1`. Behavior along the path COULD differ
  under the local `H_0` — we did not check. (Open question Q3.)

### G3. Adiabatic exponent uncertainty
- Observed scaling of `t_needed` vs `1/gap_min` in our C2 scan is closer to
  `1/gap²` than `1/gap³`. Standard rigorous adiabatic bound is `1/gap³`; the
  friendlier `1/gap²` holds under smoothed schedules (Jansen-Ruskai-Seiler).
  We used the linear schedule s(k) = k/T, so the observed `1/gap²` may be
  luck-of-the-2D-block or genuine — we did not fit the exponent nor sweep to
  larger n. (Open question Q4.)

### G4. Only 4 distributions, only n=8
- We tested uniform, Bernoulli(0.3), half-uniform coset, and a two-peak SD
  distribution — all on n=8 qubits (256 dim). The paper's SZK-relevant
  distributions include DLPc, quadratic residuosity, closest-vector-in-a-
  lattice (§2.4-2.6), and bipartite-perfect-matchings (§8). None of the
  paper's specific SZK-complete instances were reproduced, only the generic
  mechanism on synthetic SZK-flavored distributions.

### G5. Fidelity plateau at ~0.997 for the sharpest distribution
- Experiment D (two-peak, `overlap=0.454`) plateaus at `F ≈ 0.9972` and does
  NOT approach 1 as T grows (in fact drops slightly from F(T=10)=0.998 to
  F(T=200)=0.9972). This is a real numerical observation we did not fully
  explain — could be endpoint discretization (`s_k = k/T` never = 1 exactly, so
  we never propagate under the exact `H_1`), or diabatic transition amplitude
  within the 2D block, or Landau-Zener leakage near s=1/2. (Open question Q1.)

### G6. No end-to-end SZK-decider benchmark
- We verified Claim 1's inner-product identity (`<ψ_0|ψ_1> = F(p_0,p_1)`) to
  machine precision but did NOT actually stand up the full SZK-decision
  procedure (two parallel adiabatic runs + coherent Hadamard test +
  O(log 1/δ) reps). That's a natural next step but was out of scope for a
  one-shot QC-200 replication. (Open question Q5.)

## What would close each gap

| Gap | To close |
|-----|----------|
| F1 (marker) | Install marker-pdf into a fresh conda env (`conda create -n marker python=3.11 && pip install marker-pdf`) or use OpenClaw's central marker corpus if the paper appears there. |
| G1 (sparse H_1) | Build H_check via phase-estimation on the Q-sampling circuit U_p and rerun on n=8..12; verify same gap. |
| G2 (local H_0) | Replace H_0 with sum-of-transverse-field; redo experiments; report gap-scan. |
| G3 (adiabatic exponent) | Extend n to 12/14, fit `t_needed = A/gap^α` explicitly with 3 schedules. |
| G4 (only 4 dists) | Add DLPc, QR-flavored, and small bipartite-matching instances. |
| G5 (plateau) | Analytic 2×2 diagonalization + boundary-vanishing schedule ablation. |
| G6 (end-to-end SZK) | Build the two-adiabatic-runs + Hadamard-test decider; test on synthetic yes/no SD instances with α=3/4, β=1/4. |

## Honest bottom line

The replication is legitimately **REPLICATED** for the operational core the
paper claims (C1, C2, C3), on real numpy statevector arithmetic with an
independently-verified 2D-subspace exact propagator. The **structural
complexity-theoretic claims** (Theorems 1, 2, 5) rest on that operational
core plus complexity arguments we did not re-derive. The gaps above are
scope-management (this is a one-shot replication of a paper that could
easily justify a semester of follow-on numerics), not evidence of a broken
result.
