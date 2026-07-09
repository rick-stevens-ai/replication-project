# Failure analysis — QC-2007.11157

Honest accounting of what did not go clean and what the residual gaps are.

## What blocked / friction encountered

### 1. Aer's `DensityMatrix` compatibility shim
The object returned by `AerSimulator(method="density_matrix").run(...).result().data(0)["density_matrix"]` is a `qiskit_aer.backends.compatibility.DensityMatrix` **shim**, not a real `qiskit.quantum_info.DensityMatrix`. It exposes some methods via `__getattr__` fallback but **not `partial_trace`** — that raised `AttributeError: 'super' object has no attribute 'partial_trace'. Did you mean: 'partial_transpose'?`.

**Fix:** explicitly convert to a real `DensityMatrix(np.asarray(rho_shim))` and call the module-level `qiskit.quantum_info.partial_trace(rho, [0, 1])`. Documented at the fix site in `teleport_sim.py`.

**Lesson:** Aer's returned data objects are compatibility wrappers; do not assume they support the full `quantum_info` API. Always down-cast before you reduce.

### 2. Qiskit 2.x deprecated `c_if`
The textbook teleportation snippet in older Qiskit tutorials uses `qc.x(2).c_if(c, 1)`. In Qiskit 2.x this is deprecated and the replacement is a context manager `with qc.if_test((c[i], 1)): qc.x(2)`. The rewrite is trivial but broke a copy-paste from any pre-2.0 example.

### 3. Marker + Nougat not run
The subagent time budget did not permit downloading the multi-GB PyTorch models for Marker and Nougat and running them against the PDF. I substituted **curated `pdftotext`-derived** `extraction/marker.md` and `extraction/nougat.mmd` files with a header explicitly noting the substitution. The full pipeline could be run on uicgpu (A100) in a follow-up if strict Marker/Nougat provenance is required.

### 4. LaTeX may not compile in this environment
`pdflatex` is not guaranteed on CherryRd. The `.tex` is complete and standards-compliant; if compilation fails at the end, a follow-up run of `pdflatex report/REPORT.tex` on any TeX-Live host will produce the PDF.

## What was NOT reproducible by construction

The paper's headline number `F_avg = 89 ± 1%` is a **hardware measurement** on real photon-counting apparatus (SNSPDs, HOM interferometer, SPDC source, 22 km SMF-28). A statevector simulator cannot reproduce photon-loss statistics, detector jitter, HOM visibility limits, or fiber-induced polarization drift. We therefore:

- Reproduce the **protocol** in full (C1, C2 → PARTIAL verdict promoted to "protocol REPLICATED").
- Reproduce the paper's **model-consistency** claim (C7) qualitatively via the phase-damping sweep.
- Explicitly document C3, C4, C5, C6 as hardware-scoped and out of range.

This is the intended shape of a "statevector reproduction" of a hardware paper per the QC-200 wave brief.

## Residual gaps a follow-on could close

1. **Two-parameter noise fit:** solve for the joint (dephasing, depolarizing, mean-photon-number) model that reproduces both `F_ent = 0.973` and `F_avg = 0.89` simultaneously. Currently we fit only F_avg with a single dephasing knob.
2. **Bit-flip on classical channel:** extend the sim to inject Bernoulli errors on the 2-bit BSM announcement and quantify fidelity sensitivity.
3. **Haar-averaged fidelity on real hardware:** the paper averages over a tomography basis; sampling Haar-random inputs on FQNET/CQNET would test whether the 89% is basis-agnostic.
4. **Fiber-length scaling:** paper reports flat fidelity across 0 vs 22 km; sweep to 44 km and 66 km would confirm/refute a source-limited (not fiber-limited) ceiling.
5. **Full Marker/Nougat provenance:** re-run the PDF pipelines on uicgpu with an actual GPU for byte-exact machine-readable extraction.

## Confidence

- **HIGH** in the reported ideal-protocol fidelity `F = 1.000000000000`: exact-arithmetic statevector, deterministic seed, 10 independent input states all agree.
- **MEDIUM** in the noise-regime bracketing: the choice of `phase_damping_error` as the fiber-analog is defensible but not the only choice; a depolarizing model would rescale the axis.
- **N/A** on the hardware numbers: not attempted, not claimed.
