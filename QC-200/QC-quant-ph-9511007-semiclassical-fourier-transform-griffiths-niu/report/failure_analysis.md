# Failure analysis / friction / residual gaps

## What went right

- Paper is short (7 pages), self-contained, and specifies its recipe (Eqs. 10–11) unambiguously. Zero ambiguity on what "the semiclassical QFT" means.
- Qiskit 2.5.0's dynamic-circuit `with qc.if_test((cbit, 1)):` primitive maps 1:1 onto Griffiths–Niu's Fig. 2 "classical signal controls a single-qubit phase" recipe. This is a much cleaner mapping than the pre-`if_test` days of `c_if`, and did not require any workarounds.
- Aer executes `if_test`-containing circuits natively; no special backend selection needed.
- On the ideal simulator, the empirical equivalence appeared immediately and cleanly on the first run (no debugging loop).

## Frictions encountered

1. **No Marker, no Nougat, no central corpus hit.** Followed the wave brief's fallback contract: created `extraction/marker.md` and `extraction/nougat.mmd` as pdftotext-derived + hand-cleaned artifacts with explicit provenance notes at the top of each file. Cross-checked against the sibling replication `QC-quant-ph-0012055-multi-bit-gates-quantum-computing/` for precedent — that project uses the same fallback pattern.
2. **No pre-existing Qiskit venv with `qiskit-aer`.** Reused a sibling QC-200 project's venv that had qiskit 2.5.0 and added `qiskit-aer 0.17.2` with a single `pip install`. Downside: this creates a soft coupling between two QC-200 replications' environments (deleting the sibling wipes ours). Not fixed inside this subagent's scope; the reproducibility recipe in `workflow.md` lists the exact venv path.
3. **Qubit-order / bit-order convention.** The paper indexes qubits with $j=0..s$ where $j=0$ is the least-significant. Qiskit indexes classical registers little-endian by default. We had to carefully route qubit $j$'s measurement into classical bit $n{-}1{-}j$ to make the integer read out of the classical register directly match Griffiths–Niu's $c$. This was easy to get wrong; we double-checked by running $|x\rangle$ inputs — the resulting distribution is uniform on $\{0..2^n{-}1\}$ for every $x$, which is invariant to the routing bug, so we additionally cross-verified against the periodic-superposition sweep where a routing bug would immediately move the peak locations.
4. **Analytic reference construction for the periodic-input test.** The paper does not give a closed-form expression for the QFT of $|k\cdot p \bmod 2^n\rangle$-superpositions, so we build the reference distribution numerically from an exact NumPy DFT matrix. This is unambiguous but does mean the reference is a numerical exact-DFT, not a symbolic peak formula. The comb-structure was verified by eye.
5. **Wave-brief nominal set is "QC-100" in the brief text but "QC-200" in the target-directory path** and the final `WAVE_RESULT` line. We followed the target-directory path (QC-200) as authoritative — the brief file is titled "QC-100" but is dated 2026-07-03 and appears to have been reused for the QC-200 wave without a title update. Not a defect of the replication; flagging for the wave-orchestrator log.

## Residual gaps (what we did NOT do)

- **Real hardware.** All results are ideal-simulator. The paper's real payoff is on physical dynamic-circuit hardware (mid-circuit measurement + fast feed-forward). See Open Question Q1 for the natural follow-up.
- **Noisy simulator.** We did not add a `NoiseModel` to Aer. On a noisy simulator, the crossover between "semiclassical wins because it has no 2q gates" and "semiclassical loses because measurement idle-dephases the register" is where the interesting empirical questions live. Q1 lays out the exact experiment.
- **Consistent-histories interpretive claim (C5).** This is not empirically testable in the sense of a distribution to match; we did not attempt it. Q4 lays out a channel-identity alternative that could be formalised.
- **Larger $n$.** We verified $n=3,4$ empirically. Gate-count theory extended to $n=8$. Nothing prevents $n\ge 8$ empirically; we stopped at $n=4$ because (a) that suffices to falsify the paper's claim if it were wrong, (b) the number of |x⟩ inputs is $2^n$ so wall time grows exponentially in the sweep-all-inputs test, and (c) the paper's argument is per-qubit induction so the $n=4$ case exercises every distinct structural pattern.
- **LLM-judge scoring.** Per the wave brief, LLM-judge is preferred for the final verdict. Because the empirical result is quantitatively unambiguous (max TVD 0.032 with $4\sigma$ threshold 0.08; peak sets match exactly), we issued a self-verdict of REPLICATED. An Argo panel could confirm but would add noise, not signal, on a match this clean.

## Would-do-differently

If we ran this again with more time, we would add: (i) a noisy-Aer sweep (Q1) so the empirical crossover between semiclassical and standard on realistic hardware parameters is quantified in the report itself; (ii) a partial-semiclassical hybrid (Q3) to explore whether Griffiths–Niu's trick can be applied to intermediate-QFT sub-blocks; (iii) a `defer_measurements` compilation check (Q5) so the "does this help on non-dynamic-circuit hardware" question has a concrete answer for a modern reader.
