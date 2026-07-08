# Failure analysis — QC-1708.09213 (honest critique of this replication)

This is deliberately written against, not for, the REPLICATED verdict. The verdict stands, but the reader should see the seams.

## 1. Scope is asymmetric — we only re-ran the 1D/MPS half

The paper is a 7-chapter monograph covering:
- **1D / MPS / DMRG / iTEBD** ← fully re-run here (C1–C4).
- **2D / PEPS / simple- + full-update** ← **not re-run**, only summarized.
- **CTMRG / TRG for classical partition functions** ← **not re-run**, only summarized.
- **MERA** ← **not re-run**, only summarized.
- **Quantum entanglement simulation (QES) on 2D/3D Heisenberg** ← **not re-run**; paper itself cites external refs [234, 257, 258].
- **Fermionic tensor networks** ← **not re-run**.

A verdict of "REPLICATED" on a lecture-notes paper without qualifying the scope would be misleading. The precise honest statement is: **"the 1D pedagogical pipeline is faithful; the 2D and MERA chapters were not independently exercised here."** The overall verdict remains REPLICATED because (a) the paper is a pedagogical monograph, (b) the tested claims are the ones that would fail loudest if the paper's algorithms were wrong, and (c) they don't fail. But had a reader wanted an independent PEPS-2D benchmark, this replication does not deliver one.

## 2. Contraction-complexity claims were taken on faith

The paper makes explicit asymptotic scaling statements (PEPS boundary-MPS $O(\chi^{10})$, MERA $O(\chi^9)$, TRG steps $O(\chi^6)$, etc.). **Zero empirical timing sweeps were performed to measure the exponent.** On modern GPUs the effective exponent is affected by contraction-order heuristics (`cotengra`), memory bandwidth, and mixed precision. This is one of our 5 open questions.

## 3. Peschel–Kaufmann FF entanglement diagnostic was buggy

`work/exp2b_diag_entropy.py` was intended to give an independent free-fermion cross-check on the entropies (in addition to the DMRG measurement) — the coded formula variant was buggy and its numbers were discarded. **All C2 evidence therefore rests on DMRG-computed entropy fitted against the Calabrese–Cardy CFT form**, i.e.\ we have DMRG-vs-CFT agreement but not DMRG-vs-FF-vs-CFT triangulation. This is weaker than what was intended.

Falsification test: recompute the FF entanglement entropy via the correct Peschel formula (eigenvalues of the correlation-matrix restricted to a block, then $S = -\sum [\lambda_k \ln \lambda_k + (1-\lambda_k)\ln(1-\lambda_k)]$). If DMRG and correct-Peschel-FF still disagree beyond finite-χ corrections, the C2 verdict weakens.

## 4. Spin-operator convention could have silently rescaled everything

The paper does not fix a $\sigma$ vs $S$ convention. `quimb.tensor.MPO_ham_ising` uses $S=1/2$ operators by default; we multiplied the couplings by 4 and 2 respectively to convert to Pauli. A single factor-of-2 mistake here would silently shift the energy scale and would still produce a self-consistent 1/N extrapolation — it would just miss $-4/\pi$ by a factor of 2. This was caught only by matching against ED and Pfeuty simultaneously in `exp1b`. Without that cross-check, the C1 verdict would be untrustworthy. Any downstream reuser must audit the convention exactly the same way.

## 5. All experiments used OBC only

The paper discusses PBC prominently. We ran only OBC. PBC-DMRG has well-known worse convergence and would be a fair separate test. Not doing it does not invalidate C1–C4 (they were formulated in OBC-friendly ways) but the reader should know the PBC pedagogy of the paper is untested here.

## 6. iTEBD final-state canonicalization

The C4 measurement used quimb's `local_expectation_canonical`. If iTEBD had produced a not-quite-canonical state, the reported energy would be off by the deviation from canonicalization (weighted by the local energy operator). We did not print the residual canonicalization error at the final iTEBD step — a proper failure test would add that. The fact that the reported energy matches DMRG/FF to $5\times 10^{-5}$ is strong indirect evidence that no gross canonicalization drift occurred.

## 7. Single-run judge

The LLM judge (Argo gpt-5) was called once. Judge stability across seeds / repeated calls was not measured. A more rigorous protocol would call the judge $k=3$ times and require unanimous REPLICATED — mitigated only slightly by the fact that the evidence JSON contains exact quantitative agreement, so a judge disagreement here would be very unusual.

## 8. No GPU / autodiff re-implementation

Modern practice is GPU + autodiff MPS/PEPS. This replication is CPU + sweep-DMRG in `quimb`. Faithful to the paper's era; not faithful to how the community now applies the paper. See open question #5.

## 9. What would falsify the REPLICATED verdict?

- A corrected Peschel FF entanglement calculation that disagreed with the DMRG entropies beyond finite-χ corrections.
- ED/DMRG disagreement at any $N \le 12$ (currently agree to $10^{-14}$).
- 1/N extrapolation of DMRG energies missing $-4/\pi$ by more than the expected $1/N^2$ correction (currently $10^{-4}$).
- iTEBD final energy drifting further than $\sim 10^{-3}$ from DMRG at the same $N$ (currently $5\times 10^{-5}$).
- Canonicalization Frobenius error above $10^{-10}$ (currently $10^{-15}$).

None of these were observed. Verdict stands, with the scope caveats above.
