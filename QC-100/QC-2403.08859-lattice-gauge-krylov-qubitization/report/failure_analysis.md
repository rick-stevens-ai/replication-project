# Failure analysis — honest critique of this replication

This document exists specifically to state, without softening, what this
replication does NOT establish about arXiv:2403.08859. The paper has two
distinct claims; only one was exercised.

## 1. Track B (qubitization resource count) — the big miss

The paper's most engineering-consequential claim is Sec. 5–6: a qubitization
block-encoding of the Schwinger Hamiltonian with $\tilde O(N)$ gate cost, an
asymptotic improvement over prior $\tilde O(N^2)$ LCU compilations, and
associated shot-count extrapolations to N = 100, 1000, 10000 lattice sites
(Sec. 4.3).

**Nothing here verifies any of that.** No compilation was done; no T-count
was computed; no PREPARE/SELECT decomposition was independently rederived.
The asymptotic argument in the paper is plausible and internally consistent
on inspection, but internal-consistency reading is not verification. A
genuine independent check requires a resource estimator (Qualtran, Azure QRE,
or hand-compiled LCU counting) applied to Eq. 15 at concrete N. The
crossover N at which $\tilde O(N)$ actually beats $\tilde O(N^2)$ (constants
and log factors matter a lot) is unknown from this replication.

**Impact on verdict:** If judged only on Track B, this replication would
score NO-GO (nothing verified). If judged only on Track A, REPLICATED. The
whole-paper judgment is closer to PARTIAL. We adopt REPLICATED here because
the wave brief's headline-exercised rule points at Track A's Fig. 3 as the
one reproducible experimental number, and that IS quantitatively reproduced.

## 2. No baseline comparison

A rigorous check of a "Krylov + qubitization is better than X" claim
requires demonstrating X on the same instance and showing Krylov wins. This
was not done. Neither pure-VQE (with a plausible ansatz), nor first- /
second-order Trotter evolution, nor a naive imaginary-time QITE was run on
the same Eq. 15 instance for side-by-side comparison. The paper itself does
not do this comparison — it argues from information-theoretic and
gate-count grounds — but a replication that adds no baseline of its own
inherits the paper's silence on the question. This is a real limitation.

## 3. Instance coverage

We ran N = 4, 6, 8, 10. The paper's Fig. 3 goes to N = 26. The larger the N,
the more informative the D-vs-N linear fit. Extending to N = 12, 16, 20
would be trivial (seconds to minutes of CPU) and would tighten the check on
the paper's slope estimate D ≈ 0.057 N + 4.36 versus the actual measured
slope. Not done under the "no re-run sims" backfill constraint.

## 4. Track A caveats

Even inside Track A, several things were not exercised:

- **No shot-noise simulation.** The paper's Fig. 4 upper panels study QSE
  performance with simulated Bernoulli shot noise on the moments; we
  reproduced only the noiseless limit. The claim that the Hankel-form
  ill-conditioning is the *dominant* failure mode over shot noise at
  practically relevant sample budgets was not independently checked.
- **No non-abelian check.** The Schwinger model is U(1). The paper's
  generality claims (that the block-encoding technique generalises to
  richer gauge groups) are not exercised for SU(2) or SU(3).
- **Sign-convention gotcha.** The first implementation had the
  ϕ†ϕ ↔ σ_3 sign flipped, giving ⟨GS|ψ_ref⟩ = 0 and a dead Krylov space.
  This was caught by the sanity gate `⟨ψ_ref|H_0|ψ_ref⟩ = E(x=0)` failing,
  and fixed in one iteration. That the paper's conventions require careful
  attention to sign is worth flagging: a reader trying to reproduce this
  from Eqs. 7 and 15 alone can plausibly get the sign wrong and see nothing
  work.

## 5. Extraction / OCR

`extraction/nougat.mmd` is a stub — no Nougat run was performed. The
Hamiltonian and reference state were re-derived from the pdftotext-layout
dump plus direct reading of the PDF equations, not from Nougat's LaTeX
extraction. This is fine for a physics paper with clean typeset equations
but would be a real gap for a paper with heavy in-text formulas that must
be OCR'd for downstream automated re-derivation.

## 6. What would flip the verdict

To upgrade the whole-paper verdict from PARTIAL to REPLICATED-strong:
- **Track B compilation:** Qualtran / Azure QRE compilation of PREPARE/SELECT
  for Eq. 15 at N = 10, 20, 50, 100, with T-count vs naive-LCU baseline.
- **Baseline comparison:** VQE (hardware-efficient ansatz, COBYLA optimiser)
  and second-order Trotter on the same instance; report ground-state energy
  error at matched wall-clock or gate budget.
- **Higher N in Track A:** N = 12, 16, 20, 26 to tighten the D-vs-N slope
  check.
- **Shot-noise sweep:** add simulated shot noise to the Hankel form and
  reproduce Fig. 4 upper panels.

Each of these is bounded work (day to week of CPU + engineering), not a
research programme. They just weren't done here.
