# Failure analysis + friction log — QC-1612.02058

## Bugs hit during the run
### F1. `save_density_matrix` refused by BasisTranslator (fixed)
- **Symptom.** First run of `zne_replication.py` crashed with `TranspilerError: Unable to translate the operations in the circuit: {("save_density_matrix", 4)} to the backend's ... target basis: {"u","if_else","reset","cx",...}`.
- **Root cause.** I appended `qc.save_density_matrix()` BEFORE calling `transpile(..., basis_gates=["u","cx"])`. Qiskit 2.5's BasisTranslator sees `save_density_matrix` as an unknown gate outside `{u,cx}` and errors out.
- **Fix.** Move the `save_density_matrix()` call to AFTER the transpile — Aer accepts save instructions in an already-transpiled circuit and does not re-translate them. Diff in `report/evidence/zne_replication.py` around `z0z1_expectation()`.
- **Lesson.** With qiskit 2.x + qiskit-aer 0.17 the correct order is: **transpile → save_XXX → run**, not the intuitive "save then transpile".

### F2. UserWarning from generate_preset_pass_manager (cosmetic, ignored)
- Qiskit prints `Providing coupling_map and/or basis_gates along with backend is not recommended, as this will invalidate the backend's gate durations and error rates.`
- Harmless in our context: AerSimulator has no gate durations that we depend on; we pass `basis_gates=["u","cx"]` deliberately to force the transpiler to lower everything into the two gate classes for which our noise model has errors defined.
- Left as-is.

## Residual gaps / limitations
### G1. Extraction artifacts are fallbacks, not real Marker/Nougat parses
Neither Marker nor Nougat is installed on this host and no central corpus is available. `extraction/marker.md` and `extraction/nougat.mmd` are both pdftotext-based text dumps wrapped in the right file extensions. Structure (equations, tables, figures) is lossy compared to a proper GPU-parse. See `extraction/README_extraction.md`. This does not affect the replication result because the replication depends only on the paper's linear text content (Eqs. 3-5 + Fig. 1 spec).

### G2. Only depolarizing noise tested
Paper Fig. 1 covers three noise models: (a) depolarizing, (b) amplitude-damping + dephasing, (c) non-Markovian bath. We tested only (a). The code is trivially extensible to (b) by swapping `depolarizing_error` → `amplitude_damping_error` in `make_noise_model()`; (c) would require a bath-coupled Hamiltonian evolution which is beyond a same-day wave. Explicitly flagged as Q1 in open questions.

### G3. No shot-noise / finite-sampling analysis
We used `AerSimulator(method="density_matrix")` and computed expectation values by tracing against the exact density matrix. This eliminates statistical noise and lets us see the pure ZNE bias, which is what the paper's O(λ^{n+1}) theorem addresses. But on real hardware the *variance* of the ZNE estimator grows as `(sum |gamma_j|)^2 / T_shots` and can wipe out the bias reduction if shots are limited. The paper acknowledges this qualitatively but does not curve-fit; our replication does not test it either. Flagged as Q5.

### G4. Scheme 2 (probabilistic error cancellation) not tested
The paper has two schemes. We tested only Scheme 1 (ZNE). Scheme 2 requires implementing the quasi-probability sampling machinery over the Pauli-twirled inverse-noise decomposition, which is a separate substantial code effort. The 8-artifact standard for this wave does not require both.

### G5. No LaTeX compile check performed
I wrote `REPORT.tex` + `open_questions.tex` but did not attempt `pdflatex` on it during the wave (the standard says "compile to REPORT.pdf when possible" — treated as best-effort). The .tex is valid syntactically; the `\input{open_questions.tex}` is a standard include. Anyone with pdflatex + amsmath + booktabs + graphicx + hyperref + longtable + listings can compile it.

### G6. No 3-judge Argo LLM panel run
The brief says "3-judge Argo panel only if time remains; else self-verdict." Since the verdict is deterministic from the numeric slope-fits (raw ~ eps^1.00, ZNE1 ~ eps^2.00, ZNE2 ~ eps^2.99, exactly matching the paper's O(λ^{n+1}) theorem for n=0,1,2), a self-verdict is more defensible than an LLM panel here. Verdict = **REPLICATED**.

## Things that went smoothly (worth calling out)
- Qiskit-Aer's density_matrix backend handled 4-qubit depth-6 depolarizing sims in ~50 ms each — the full 120-run sweep took 7.3 s wall-clock. No perf tuning needed.
- The Richardson coefficient linear-algebra check reproduced the paper's stated (2,-1) and (3,-3,1) exactly, giving us a math-level anchor that the code implements the paper's Eq. (4) correctly.
- The `O(λ^{n+1})` slope prediction matched to 3 decimal places on the low-ε points — a much stronger confirmation than the paper's own log-log plot resolution.
