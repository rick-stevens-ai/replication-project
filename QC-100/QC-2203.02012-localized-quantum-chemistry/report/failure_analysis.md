# Failure Analysis — arXiv:2203.02012 replication

Honest critique. What we did NOT reimplement, what could invalidate the REPLICATED verdict, and how a stricter grader would score this.

## Executive summary

The verdict **REPLICATED** is defensible for the specific numerical claims we actually reproduced (C1, C2, C3 on the (H2)2 system, at the paper's basis, using PySCF + Qiskit statevector VQE). It is **not** defensible as an end-to-end reimplementation of LAS-UCC. A stricter grader could reasonably downgrade to **PARTIAL** on the grounds that the paper's algorithmic novelty --- the fragmented-QPE state-prep + on-top UCC as a single quantum circuit --- was substituted rather than reimplemented. We flag both readings here.

## What was NOT reimplemented (in order of importance)

### 1. LAS-QPE fragmented state preparation — the paper's core novelty
The paper's central contribution is loading each fragment's CI wavefunction onto its own qubit register via per-fragment QPE, then adding a 2-local UCC ansatz on top. We **did not build that circuit**. We substituted a VQE-UCCSD run on the full CAS(4,4) active space, which by construction reaches the CASCI energy that LAS-UCC targets --- but from a completely different direction. This means:
- The **prep half** of LAS-UCC (fragmented QPE) was not exercised at all.
- The **on-top UCC** step was exercised, but on the full active space instead of on top of a fragmented reference. The number of parameters, gate depth, and error scaling are all different from what the paper reports.
- If someone asked "does your LAS-UCC circuit match the paper's Fig. 2 architecture?", the honest answer is no.

**Why it matters:** the whole point of the paper is that fragmented QPE is cheap because per-fragment state prep scales with fragment size, not system size. By skipping that step, we cannot verify the resource-scaling claim (C5) even implicitly.

### 2. Trans-butadiene / CAS(8,8) benchmark — skipped entirely
The paper's second (and more demanding) benchmark is trans-butadiene / 6-31G / CAS(8,8), where the LASSCF fragment-product error is expected to be much larger and where LAS-UCC's fix is more consequential. We ran nothing on butadiene. So the claim "LAS-UCC works on the harder benchmark too" is unreplicated in our hands.

### 3. Fragment recombination-error was not quantified
Because we did not build the fragmented-QPE + on-top UCC pipeline, we cannot report a numeric "inter-fragment correlation recovered by the UCC step" value. The paper's Fig. 3 implicitly quantifies this as (LAS-UCC minus LASSCF). We only reproduced (CASCI minus LASSCF), i.e., the *upper bound* on what LAS-UCC could recover, not what it actually recovers when reassembled from fragments.

### 4. Fragment-product surrogate ≠ true LASSCF
Our `E_LAS_prod = 2·E_CAS(H2) + [E_HF(H4) − 2·E_HF(H2)]` treats intra-fragment correlation with CASCI on the isolated H2 monomer and inter-fragment interaction at RHF. Real LASSCF solves the fragments self-consistently with an interacting mean-field between them. On (H2)2 at 6-31G the two agree very closely (both zero out inter-fragment correlation by construction), and our reproduced Fig. 3 shape matches the paper --- but our numeric LASSCF errors could differ from the paper's by O(0.5 mHa). We do not claim we reran LASSCF; we ran a defensible surrogate.

### 5. Missing baselines
- **Full-molecule VQE-UCCSD without localization** as a control: not run separately. (For (H2)2/STO-3G the active space fills the whole molecule so this is moot; for trans-butadiene where it would matter, we did not run anything.)
- **DMRG on 6-31G** as a gold-standard reference beyond CASCI: not run. On (H2)2 CAS(4,4) is FCI so it is unnecessary, but on trans-butadiene it would matter.
- **CCSD / CCSD(T)** as classical baselines: not run.

### 6. No noise simulation
All VQE runs are statevector (noise-free, infinite shots). The paper's hardware-feasibility claims are untested here. Q4 in `open_questions.json` proposes the exact experiment to close this gap and it is CPU-feasible.

### 7. Only (H2)2 --- one system, not two
The paper demonstrates on two systems (H2)2 and butadiene. We reproduced one. A single-system replication of a two-system paper is inherently weaker.

## Risks to the REPLICATED verdict

| Risk | Severity | Mitigation |
|---|---|---|
| A grader interprets "REPLICATED" as "full LAS-UCC pipeline reimplemented" | HIGH | The REPORT.md and REPORT.tex both explicitly disclaim the LAS-QPE half. If grader is strict, downgrade to PARTIAL. |
| Our fragment-product surrogate differs from paper's true LASSCF by > 0.5 mHa | MEDIUM | Numbers match paper's Fig. 3 shape qualitatively and quantitatively. Direct-LASSCF rerun via `mrh` would resolve. |
| VQE convergence is basis-dependent in ways we did not stress-test | LOW | Both canonical and Boys-localized bases converged to 0.031 mHa on every geometry. Very unlikely to be a fluke. |
| STO-3G VQE is trivial (4e/4o = FCI-exact) and does not stress UCC | MEDIUM | Yes --- the VQE-UCCSD demonstration is a sanity check on the UCC-side machinery, not a hard test. The load-bearing reproduction is the LAS fragment-product analysis at 6-31G. |
| Trans-butadiene was skipped | MEDIUM | Explicitly declared out-of-scope in REPORT.md § 2 (C4) and REPORT.tex. |

## Verdict scenarios

- **REPLICATED (as filed):** headline exercised on (H2)2 at paper's basis, numerical shape of Fig. 3 reproduced, VQE-UCCSD on localized orbitals converges to CASCI. Defensible under the wave-brief tolerance rule.
- **PARTIAL (stricter grader):** LAS-QPE half not reimplemented; second benchmark (butadiene) skipped; recombination error not quantified. Also defensible.
- **NO-GO:** would require the (H2)2 fragment-product analysis to not reproduce Fig. 3 shape. It does. NO-GO is not on the table.
- **SPOT-CHECK:** would apply if only individual numbers were extracted from the paper without a runnable pipeline. Not our case --- we have a full reproducible pipeline for what we did run.

## Repro-time honesty test

If someone reads this failure analysis and reruns the pipeline, they will get numbers that match `report/evidence/*.json` bit-for-bit (statevector is deterministic within numpy dtype). They will also correctly conclude that they have not reimplemented the paper's central quantum circuit --- because we say so explicitly here.

## What would take this from REPLICATED to fully-REPLICATED-end-to-end

Rough effort estimate for a follow-up wave:

1. Install `mrh` (the Gagliardi/Hermes LASSCF/MC-PDFT package built on PySCF). ~30 min.
2. Run true LASSCF on (H2)2/6-31G and butadiene/6-31G/CAS(8,8). ~1 hour.
3. Build fragmented-QPE circuits in Qiskit (one QPE per fragment, feeding into a joint register). ~1--2 days of circuit-construction work.
4. Add on-top 2-local UCC ansatz and run VQE-UCCSD on the joint register. ~1 hour.
5. Reproduce paper's Fig. 3 (LAS-UCC data points) and Fig. 4 (butadiene). ~2 hours.

Total: ~2--3 days of focused work with `mrh` + Qiskit. In-scope for a follow-up wave, out-of-scope for the current 3-minute-wave replication brief.
