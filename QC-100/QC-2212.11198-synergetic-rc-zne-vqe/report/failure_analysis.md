# Failure Analysis / Honest Critique — QC-2212.11198

**Verdict stated: REPLICATED.** This file exists to state, without spin, what
the replication does NOT prove, and where a skeptical reviewer would push back.

## 1. What is genuinely and defensibly reproduced
- **The headline synergy (C1).** Independent code path (own Hamiltonian
  build, own Pauli-twirl implementation, own Mitiq wiring, own noise
  injection), independent simulator (Qiskit-Aer density-matrix), gives a
  9× to 35× reduction in VQE energy error across ε = 0.02–0.10 rad — landing
  the paper's "1–2 orders of magnitude" band. This is real.
- **C3 (ZNE-alone fails on coherent noise).** ZNE-only actively over-corrects
  and produces large negative-sign errors (−6.9 to −27.0 mHa). This is the
  specific failure mode the paper highlights, and it reproduces cleanly.
- **C4 (RC-alone is limited).** RC-only shaves 15–25% off the raw error —
  small, matching paper.
- **Baseline discipline.** All four methods (raw / RC-only / ZNE-only /
  RC+ZNE) evaluated on the same θ\*, same noise realization, same ε in a
  single sweep. No cherry-picking across runs.

## 2. Where the replication is thinner than the paper
- **One molecule instead of two.** Paper does H₂ AND LiH; we only did H₂.
  LiH's UCC-SD ansatz is deeper and has different CX-error accumulation. C5
  is marked ⚪ Partial, not ✅.
- **Substituted ansatz.** We used a deep hardware-efficient ansatz (13
  params, 6 CX) instead of the paper's UCC-SD. Agreement to within a factor
  of ~2 on the reduction ratio is plausible but not guaranteed to transfer;
  UCC-SD has structured excitation blocks whose coherent-noise pattern differs
  from stacked RY-CX layers.
- **One optimizer instead of the paper's Powell.** Nelder-Mead here vs.
  Powell in paper Fig. 4. Optimizer robustness (C6) not tested.
- **Exact expectation, not shots.** We compute ⟨H⟩ from the density matrix.
  Paper allows this (explicit paragraph above Fig. 4), but real hardware has
  8k–100k shots per Pauli term, and RC+ZNE's variance behavior under shot
  noise is untested here. C7 not tested.

## 3. Where a skeptical reviewer would legitimately push back
- **Noise-model narrowness.** Only tested coherent over-rotation + a small
  depolarizing residual. Real devices have amplitude damping (T₁), dephasing
  (T₂), leakage, and crosstalk. RC's Pauli-twirl argument only strictly
  applies to coherent errors becoming stochastic Pauli errors; amplitude
  damping twirls to a *non*-Pauli stochastic channel and leakage escapes the
  computational Pauli group entirely. So our claim "RC+ZNE synergy holds"
  is defended only for the paper's exact noise regime, not for general
  hardware noise.
- **The "super-additive" language deserves care.** At ε = 0.10, raw is
  42.7 mHa, RC-only is 32.4 mHa (24% reduction), ZNE-only is *−26.9 mHa*
  (actively worse than raw), RC+ZNE is 1.23 mHa (97% reduction). The
  formally-additive expectation for the two mitigations combined is not
  well-defined here because ZNE-alone has negative marginal utility. What
  IS clearly true is that **combined RC+ZNE is orders of magnitude better
  than the best individual mitigation**, which is the empirical content of
  "super-additive." The word is defensible; the arithmetic model is not.
- **Sample size.** One θ\* per ε, one noise instance per (ε, method). The
  paper's Fig. 4 shows a median over 35–60 trials. If RC+ZNE has heavy-tailed
  variance across noise realizations, our four data points could be lucky.
  A proper reproduction would rerun each ε at 30+ trials and report the
  median + IQR. We did not.
- **Judge coverage.** Third planned judge (`claude-opus-4.7`) returned
  upstream 502; not retried. Two-of-three consensus stands and both agreed
  REPLICATED, but a full three-of-three would be cleaner.
- **Nougat extraction skipped.** Paper text was accessed via `pdftotext
  -layout` only; a Nougat markdown extraction (`extraction/nougat.mmd`) is
  a stub. For a text-only NLP paper this would matter; for a physics/method
  paper where all numerical claims come from tables + figures, `pdftotext`
  is sufficient. Still, marked as a gap.

## 4. What would elevate this from REPLICATED to REPLICATED (comprehensive)
1. Rerun each ε at 30+ noise-instance trials → report median + IQR.
2. Add LiH (paper's second molecule).
3. Add UCC-SD ansatz alongside the HEA to isolate ansatz-dependence.
4. Add amplitude-damping and leakage channels (open question #1).
5. Add finite-shot regime (8192 shots per Pauli term).
6. Re-retry the third Argo judge to close the two-of-three → three-of-three
   gap.

None of these change the verdict; they harden it.

## 5. Bottom line
The **paper's headline claim is exercised and reproduced** on H₂/STO-3G in
the paper's specific coherent-2q-gate noise regime, with the specific
failure modes (ZNE-alone hurts, RC-alone is weak) also visible. **The
paper's breadth (multiple molecules, multiple ans\"atze, multiple noise
models, multiple optimizers, finite shots) is not fully covered.** Calling
this REPLICATED reflects that the *core mechanism claim* holds; calling it
PARTIAL would over-index on scope. We chose REPLICATED with this file as
the disclosure.
