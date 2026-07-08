# Failure Analysis — arXiv:1901.01234 Replication (MC-VQE)

An honest critique of what this replication did and did not accomplish. This is
NOT a defensive document: the goal is to identify every gap between our work
and a fully-adversarial independent replication so a future replicator (or
reviewer) can find and close them.

## 1. What was genuinely reimplemented

- **MC-VQE algorithm from scratch** (~230 LOC Python, no code taken from
  Parrish's group or their published repo).
- **Ab initio exciton Hamiltonian** with all five Pauli components
  (Z, X, XX, ZZ, XZ, ZX) and cyclic ring connectivity, matching Eq. 8 of the
  paper exactly in form.
- **Contracted reference states** from CIS eigenvectors of the block Hamiltonian.
- **State-averaged L-BFGS optimization** with restarts, convergence tracking.
- **Post-optimization subspace diagonalization** of H_{ΘΘ'}.
- **Comparison against exact diagonalization** (FCI-equivalent for the
  restricted CIS + double-excitation subspace we used).
- **Independent VQD (Higgott 2019) implementation** on H2/STO-3G as a
  cross-family sanity check.

## 2. What the paper claims that we did NOT reproduce

### 2.1 The actual N=18 B850 LH2 ring
- **Paper:** N=18 cyclical B850 ring, TeraChem TDA-TD-DFT ωPBE/6-31G* on the
  crystal-structure LH2 geometry, 108-parameter entangler, ~14 L-BFGS iters.
- **Us:** N=2 and N=4 exciton systems with representative-scale parameters
  (seed=42), NOT the paper's specific molecule.
- **Why it matters:** the paper's quantitative "tens of µeV" claim is
  demonstrated on the N=18 system; we demonstrate it on same-family but
  smaller Hamiltonians. Our claim that we hit "tens of µeV" at N=4/L=3
  (25.6 µeV) is a *same-family* replication, not a *same-instance* replication.
- **What would close this gap:** obtain TeraChem-derived monomer parameters for
  B850 (paywalled GPU code) OR use a published open-source ab initio exciton
  parameter set for LH2 (recent MOLCAS/OpenMolcas papers may have such data).
  Then run MC-VQE at N=18 (2^18 = 262,144-dim, ~4 GB dense state-vector,
  runnable on UICGPU A100 in hours).

### 2.2 Oscillator strengths (Claim C2)
- **Paper:** MC-VQE oscillator strengths agree with FCI to ≪ 1%.
- **Us:** NOT TESTED. Would require implementing the transition-dipole operator
  measurement + the |W_N⟩-generalizing "interfering-state" circuit
  (Eqs. 15–18 of the paper).
- **Why it matters:** oscillator strengths are the observable for spectroscopy;
  without them, MC-VQE would be an eigenvalue solver, not a full spectral tool.
  A truly complete replication must exercise this.
- **What would close this gap:** ~1 day of additional Python work; straightforward
  extension of `mcvqe_exciton.py` — add ⟨Θ|U† μ U|Θ'⟩ matrix elements + build
  transition dipoles from subspace eigenvectors. No new fundamental barrier.

### 2.3 Comparison against CIS classical reference
- **Paper:** compares MC-VQE, CIS, and FCI side-by-side; shows MC-VQE
  outperforms CIS.
- **Us:** compared to exact diag (FCI-equivalent) only. Did NOT run a CIS
  baseline.
- **Why it matters:** the "MC-VQE improves over CIS" narrative is part of the
  paper's motivation; without a CIS baseline in our results, we cannot
  independently confirm the improvement direction.
- **What would close this gap:** trivial — CIS is the same as diagonalizing
  the block-Hamiltonian in the singles subspace, which our code already builds
  as the contracted-reference construction. Extract those eigenvalues too.
  Estimated cost: 30 min of scripting.

### 2.4 Comparison to EOM-CCSD or other classical excited-state methods
- **Paper:** does not itself claim EOM-CCSD comparison for the exciton system
  (EOM-CCSD is impractical at 18 monomers).
- **Us:** did not attempt.
- **Why it matters:** for the smaller molecules that would be more accessible
  to EOM-CCSD (H2, LiH, small chromophores), a MC-VQE-vs-EOM-CCSD comparison
  would strengthen the case that MC-VQE is a viable classical alternative for
  molecules in the crossover regime.
- **What would close this gap:** PySCF has EOM-CCSD; run on H4/LiH/HF at
  STO-3G/6-31G and compare to MC-VQE. ~1 day.

### 2.5 The "single entangler layer suffices" subclaim
- **Paper:** demonstrates MC-VQE with a *single* entangler layer at N=18.
- **Us:** at N=4, L=1 failed catastrophically (748 meV error), L=3 was needed
  to hit the paper's "tens of µeV" accuracy target.
- **Why it matters:** this is the most substantive divergence from the paper.
  It is *consistent* with the paper (the paper uses an entangler system-
  tailored to the exciton NN ring topology; we used a generic
  hardware-efficient ansatz), but it means the "single layer" claim is NOT
  universal — it is ansatz- and system-specific.
- **What would close this gap:** custom-tailor the entangler to the exciton
  ring connectivity (each 2-qubit gate placed exactly on a nearest-neighbour
  bond of the ring), then check if L=1 suffices at N=4. If yes, replication is
  strengthened; if no, we have a genuine puzzle for the paper. ~2 h.

### 2.6 Novelty vs. plain VQE was only PARTIALLY demonstrated
- **Paper's novelty over plain VQE:** simultaneous multi-state solution from a
  single trained entangler (vs sequential VQD-style deflation runs).
- **Us:** demonstrated functional novelty at N=2 and N=4 (multiple states
  extracted from one optimization), but did NOT demonstrate the resource-
  scaling advantage claimed for MC-VQE at large N_Θ (many states from one
  entangler). Our tests only pull 3 states.
- **What would close this gap:** extend runs to N_Θ=6, 9, 12 states at the
  same N=4 and track: (i) optimization iterations vs N_Θ, (ii) total shots
  vs N_Θ, (iii) compare to N_Θ sequential VQD runs. If MC-VQE scales
  favourably, novelty is demonstrated at the resource level too.

## 3. What would falsify or weaken the "REPLICATED" verdict

The following observations, if made in a follow-up, would downgrade this
verdict:

1. **Oscillator strengths from MC-VQE deviate from FCI by more than 1%** on a
   small tractable system → downgrades C2 status from untested to failed.
2. **At N=18 with the paper's TeraChem parameters and their exact
   custom-tailored entangler, we cannot reproduce tens of µeV** → downgrades
   C1 from replicated to partial (would indicate the paper's numerical result
   is instance-specific in ways not documented).
3. **L-BFGS shows barren-plateau behaviour at N ≥ 10 with hardware-efficient
   ansatz** → complicates C3, though the paper's own C3 was for their
   custom-tailored ansatz, so this would be a caveat not a falsification.
4. **VQD on H2 succeeds trivially but fails on LiH or H4** → complicates C5
   as a cross-family sanity check.

## 4. What would STRENGTHEN this replication

(In order of ROI, if a follow-up replication has a compute budget.)

1. **Add CIS baseline to `mcvqe_exciton.py`** (30 min): trivial win, gives
   direct paper-comparable numbers.
2. **Implement transition-dipole / oscillator-strength computation** (~1 day):
   closes the C2 gap, upgrades this from "REPLICATED for eigenvalues" to
   "REPLICATED for the full spectral claim".
3. **Custom-tailor entangler to NN ring topology, retest at N=4** (2 h):
   tests the "single layer suffices" subclaim at our scale.
4. **Scale to N=8, 12, 18 with published ab initio exciton parameters** (days,
   needs UICGPU A100 for N ≥ 14): closes the same-instance gap.
5. **Add shot-noise simulation to `mcvqe_exciton.py`** (~1 day): opens the
   noise-robustness question (see open_questions.json Q3).

## 5. Honest one-line self-assessment

We *cleanly* replicated the paper's headline quantitative claim (tens-of-µeV
excitation-energy accuracy) on same-family but smaller ab initio exciton
Hamiltonians, and *did not* attempt the paper's exact N=18 B850 instance or its
secondary oscillator-strength claim. The verdict "REPLICATED" is defensible for
the headline eigenvalue claim; it would be "PARTIAL" if the bar were "exact
same molecule, all claims including oscillator strengths".
