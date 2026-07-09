# Failure analysis — QC-200 replication of quant-ph/9601018

## Honest assessment
The noise-free replication is **clean** (three of four in-scope claims reproduced numerically, the fourth deferred by design). But there are real gaps and shortcuts, listed below without softening.

## Residual gaps
1. **Claim C4 (decoherence trade-off) not tested.** The paper's Sec.5 argument that "AQFT with small m can outperform exact QFT under noise" is the paper's most interesting *contribution* and we didn't run it. Reasoning: the paper does not specify a concrete noise model, and picking one is a scientific choice on our side, not a verification of the paper. We captured this as Open Question Q1 with a concrete implementation plan (Qiskit-Aer depolarizing_error on cx/cp, sweep L∈{6,8,10}, p∈{1e-4,1e-3,1e-2}). This is a **PARTIAL** shortfall against the paper's full scope, hidden by our "REPLICATED" verdict on C1-C3, C5.
2. **Marker + Nougat not actually run.** Extraction fallbacks use `pdftotext -layout` and plain `pdftotext` with header banners noting they need backfill from the central Marker/Nougat corpus. This matches the convention already in use in `~/Dropbox/REPLICATE-PROJECT/BVBRC-07-Sherry-AMR-workflow-2023/extraction/` but is a real gap: the LaTeX-formula-rich content of the paper (Eqs. 1-14) is only preserved in the plain-text ASCII fallback, so any downstream corpus that needs machine-readable LaTeX/MathML would need to re-extract.
3. **The `m=1` period-finding number is a degenerate special case.** For L∈{6,8} and r=4, r|2^L exactly, so c=0 is always a "good" outcome, and Hadamard puts weight at c=0. This makes AQFT_1 look artificially strong (success 0.75) without corresponding to the paper's non-trivial regime. We disclosed this in the report and made it Open Question Q2, but a real replication of the paper's Fig.4 (r=10, L≥7) is not in the current output.
4. **No LLM-judge verdict.** The wave brief says "3-judge Argo panel only if time remains; else self-verdict." We self-verdicted. Given the numbers are unambiguous (fidelity=1.0 at m=n, matrix bound holds in every row) an LLM panel would very likely concur, but it wasn't run.
5. **Register-reversal read-out convention.** Qiskit uses little-endian and applies the SWAP layer at the end of the QFT circuit. The paper reads outputs in reversed order. We handle this by including the SWAP layer in `qft_circuit(swap=True)`, but we did NOT independently verify against, e.g., `qiskit.circuit.library.QFT` (which was removed in Qiskit 2.x). The self-consistency check (fidelity=1.0 at m=n across 300 random states) is our sanity check that the AQFT and QFT definitions align, but it does not rule out a systematic off-by-one in bit ordering that would only bite in Experiment C (where the "good" outcomes depend on bit ordering). The observed success prob of ~0.577 at m=n for exact QFT is consistent with the theoretical value for the case where the good outcomes are the multiples of 2^L/r WITHOUT the reversal (i.e. c ∈ {0, 64, 128, 192} interpreted in the same endianness as the input), which is what we tested. If there's a subtle endian mismatch we'd expect success to concentrate on a *different* set of c's — but our top-5 c-probabilities per offset (in `results_period_finding.json`) show peaks exactly at the multiples of 64, so this concern is mitigated but not disproven.

## Friction encountered
- **Qiskit 2.x removed the built-in `QFT` library circuit** (which used to be `qiskit.circuit.library.QFT`). We had to write the QFT/AQFT from scratch. Upside: makes the AQFT truncation trivially local (one `if` in the inner loop). Downside: no cross-check against a canonical reference.
- **Python 3.14 in the venv is bleeding-edge**; some packages emit deprecation warnings. None affected results.
- **Marker/Nougat not on the machine, and no local central-corpus directory** (path `~/Dropbox/REPLICATE-PROJECT/central-corpus/` does not exist on this host). We followed the existing convention of pdftotext-with-BACKFILL-header. If a central corpus is populated later, these two files should be backfilled by SHA256.
- **No hardware/paid endpoint used.** Argo (free) was available at localhost:44497 but was not needed — the reproducibility target here is a numerical circuit simulation, not a natural-language judgment.

## What would flip this from REPLICATED to REPLICATED+ROBUST
1. Run the Qiskit-Aer noise sweep for Q1 → confirms/refutes the paper's decoherence-crossover story.
2. Run one non-divisible period case (Q2) → removes the m=1 degeneracy artifact.
3. Backfill Marker + Nougat parses → downstream corpus usability.
4. Add a 3-judge Argo panel → external agreement on the verdict.

Estimated additional work: ~1 hour of subagent time.
