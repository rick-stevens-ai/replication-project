# Failure analysis — QC-1802.00171-accelerated-vqe

Honest critique of what this replication does and does not establish. The
verdict (REPLICATED) is defended below, and the boundaries are drawn where
they belong.

## 1. What is actually verified

- **C1 (VQE / H₂/STO-3G).** VQE energies match FCI (which is exact for
  2 electrons in a minimal basis) to sub-µHartree at every one of the 10 bond
  lengths tested (max |ΔE| = 0.0016 mHa, mean 0.0003 mHa, ~1000× tighter than
  chemical accuracy). The equilibrium value E_{R=1.401} = −1.13727 Ha matches
  the community-standard reference to five decimals. This is a **strong** check
  of the paper's chemistry test-bed.
- **C2, C3 (α-QPE / RFPE Fig. 5).** Median Bayes-risk r_k = σ_k traces produce
  a fan whose ordering in α is correct (larger α ⇒ smaller final r_k), whose
  log-slopes on k ∈ [10, 60] increase monotonically with α (from −0.019 at
  α=0 to −0.099 at α=1, i.e. ~5× steeper), and whose α=1 curve achieves
  ~7–8 bits of precision in 60 iterations (near-exponential, matching the
  O(log 1/ε) scaling). The fan sits within the envelope of the paper's Fig. 5
  right panel.

## 2. What is **not** verified — the honest gaps

### 2.1 Acceleration is not head-to-head timed vs baseline VQE

The paper's headline claim is *acceleration* — a wall-time or shot-count
advantage over standard (α=0) VQE. This replication does not test that
directly. It reproduces:

- the analytical **ingredient** that supports acceleration (α-QPE Bayes-risk
  shrinks faster in log-slope with larger α — verified, C2/C3), and
- the **cost-side scaffolding** of standard VQE (H₂/STO-3G to chemical
  accuracy — verified, C1),

but it never composes them into a wall-time / shot-count comparison. In
fairness, **the paper itself does not present such an end-to-end run either**
— it argues via the analytical scaling N = O(1/ε^{2(1-α)}), depth = O(1/ε^α).
So this replication is faithful to the paper's evidence base, but neither the
paper nor the replication has actually shown, on a real molecular
Hamiltonian, that α > 0 beats α = 0 in total shots to chemical accuracy.
This gap is the top item in `open_questions.json`.

### 2.2 Convergence to the correct energy was checked only in the VQE-only leg

C1 checks that VQE energies match FCI. C2/C3 check that the Bayesian
posterior variance shrinks. What is **not** checked is whether an
α-QPE-driven expectation subroutine, plugged into the outer VQE loop, would
converge the molecular energy correctly — because that composed pipeline was
never run. Composition-level pathologies (prior widening between VQE outer
iterations, rejection-filter acceptance-rate collapse at deep coherent M,
variance leakage into the classical optimiser) are all plausible in principle
and are unaddressed.

### 2.3 Hardware regime was not tested

The paper implicitly targets fault-tolerant or near-term quantum hardware with
enough coherence to run M_k = ⌈1/σ_k^α⌉ coherent applications of the unitary.
This replication ran **only** noiseless statevector VQE (C1) and noiseless
numpy RFPE (C2/C3). No decoherence model, no gate infidelity, no readout
error, no shot noise on the VQE ingredient. Every claim about the acceleration
under realistic hardware is untested here. Under strong noise the α → 1
regime is expected to fail first (that's exactly the regime with the deepest
coherent circuits), so there should be a noise-dependent optimal α* < 1 that
this replication cannot locate.

### 2.4 C4 (analytical formula overlay) was not attempted

The paper's Eqn. A16 provides an analytical form for the mean/median r_k
under the α-QPE update. We did not evaluate it and did not overlay it on the
numerical RFPE traces. The qualitative agreement in C2/C3 (log-slope ordering,
near-exponential α=1 behaviour) is a weaker check than a numerical-vs-analytical
residual would have been.

### 2.5 C5 (end-to-end α-VQE) was not attempted

This is the composition that would upgrade the verdict from "ingredients
reproduce" to "the paper's headline replicates end-to-end". It is out of scope
for a single-wave replication and is the natural next-step follow-up.

### 2.6 Fixed hyperparameters

- Only 1 seed used (42 for VQE, 1802 for RFPE). Sensitivity to seed is not
  characterised, though C2/C3 are 200-trial ensemble medians so seed variance
  should be small.
- Only 1 particle count (600) — matching the paper's caption, but no
  sensitivity sweep. If the paper's acceleration is fragile to particle count
  the replication would not detect it.
- Only 1 optimiser (Adam, lr=0.1). Optimiser choice sensitivity is question 5
  in `open_questions.json`.
- M_k clipped to 10^7 — this clip is never reported to have activated in our
  runs, but it's a silent-truncation trap worth checking.

## 3. What would falsify the verdict

- A finding that the C1 VQE energies do not match FCI at some bond length —
  would falsify C1 and would very likely be a bug in the environment.
- A finding that the C2/C3 fan of median r_k curves is not monotonic in α or
  that α=1 log-slope is not steeper than α=0 log-slope — would falsify the
  paper's Fig. 5 headline. Neither was observed.
- An end-to-end composition experiment (question 1) showing that α > 0
  actually **costs more** shots than α = 0 for real molecules would not falsify
  this replication (which was faithful to the paper's evidence base), but
  would falsify the paper's promised utility.

## 4. Summary honest verdict

The paper's numerical claims *as stated in the paper* reproduce; the
paper's *promise* (acceleration in practice for chemistry) is neither
confirmed nor refuted by this replication because the paper itself does not
run the composed experiment. Verdict remains **REPLICATED** on the paper's
own evidence base, with the acceleration promise explicitly flagged as
end-to-end untested. See `open_questions.json` for the five specific
next-step probes.
