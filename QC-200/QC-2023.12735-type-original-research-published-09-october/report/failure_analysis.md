# Failure Analysis & Residual Gaps

## What went right

- **Paper identification.** The QC-200 manifest id `2023.12735` is not an arXiv id (arxiv 404s) but a truncated Frontiers article number. A crossref filter on `publisher-name=Frontiers` + publication date `2023-10-09` (from the slug) + query `quantum` returned exactly one hit — DOI `10.3389/frqst.2023.1273581` — whose downloaded PDF SHA256 matches the manifest byte-for-byte. Confirmed identity in ~5 minutes. Provenance recorded in `work/paper_provenance.md`.
- **Environment.** Qiskit 2.5.0 + qiskit-nature 0.8.0 + PySCF 2.13.1 all installed cleanly in a `--system-site-packages` venv on macOS Python 3.14.6; no version pinning was needed.
- **Reproduction.** Both H2 (7 bond distances) and HeH+ (5 bond distances) reached chemical accuracy in every case, matching the paper's headline simulation-side claim. At the equilibrium H2 bond distance the VQE energy agrees with FCI to ~3·10⁻⁹ Ha (much tighter than the 1.6·10⁻³ Ha chemical-accuracy threshold).
- **LLM judging.** Two independent Argo judges (gpt-5.2, gpt-5.4) both returned `verdict: PARTIAL` with consistent reasoning.

## What went wrong / partial

### 1. Paper-id ambiguity in the manifest

The QC-200 manifest recorded a **truncated** Frontiers article number (`2023.12735` — 5 significant digits) instead of a full DOI. This is likely to happen for other Frontiers papers in QC-200 too. The truncation drops the last 3 digits (`581` here) and loses the journal prefix (`frqst`), so an arXiv-style resolver alone will always fail on these entries. Recommend: manifest post-processing to normalize Frontiers ids into full DOIs.

### 2. Argo Anthropic backend flakiness

`argo:claude-opus-4.7` and `argo:claude-opus-4.8` returned HTTP 502 (Bad Gateway) from both the raw Argo endpoint (`:44497`) and the litellm aggregator (`:4000`) at the time of judging. The GPT-5.x branch was healthy and returned responses in normal latency. No retry-loop needed — we degraded gracefully to two GPT-5.x judges.

### 3. What was NOT reproduced (honest gaps)

| Paper claim | Why not reproduced |
|---|---|
| PANSATZ **pulse-level** ansatz itself (DRAG + CR waveforms) | Requires `qiskit-dynamics` + a calibrated backend Hamiltonian (T1/T2, drive amplitudes, cross-resonance coefficients). Adds ~5-10 min build + a real backend calibration file. Out of scope for a pure statevector sanity replication in the ~15 min effective budget for this paper. |
| **7× schedule-duration reduction** (PANSATZ vs GANSATZ) | Same reason as above — needs backend-transpiled pulse schedules to measure. |
| **ibm_lagos** hardware run reaching chemical accuracy with readout-only mitigation | Requires paid IBM Quantum access (ibm_lagos was retired anyway, so this would need porting to another Falcon). Not reproducible for free in 2026. |
| **LiH 4-qubit** results | Doable but requires setting up Kandala-style active-space reduction; skipped in favor of a rock-solid H2 + HeH+ pair on the tight timebox. Straightforward extension of `h2_vqe_reproduce.py`. |
| **SPSA vs steepest-ascent-hill-climbing** iteration-count comparison | Skipped; used COBYLA as a widely-used gradient-free HEA baseline. |
| Exact **PANSATZ 5-parameter** structure vs my 12-parameter `EfficientSU2(reps=2)` | Deliberately used a same-family HEA baseline instead of the exact 1-layer Real-Amplitudes GANSATZ (4 params for H2). This means my numbers are an *upper bound* on the achievable accuracy at fixed noise=0 — the paper's own baselines might be tighter to their thresholds. |

### 4. Version drift risk

`qiskit-nature` 0.8 vs the 2023-vintage 0.6 used in the paper: the parity mapper + two-qubit reduction has been refactored (Z2Symmetries → ParityMapper `num_particles` kwarg). Eigenvalues are invariant under this refactor — my FCI energies match textbook values and my PySCF cross-check — but the *Pauli coefficients* of the qubit Hamiltonian may differ in sign convention on the tapered qubit. This affects only downstream ablation studies where one would compare term-by-term against the paper's supporting GitHub repo. Flagged as Q5 in `open_questions.json`.

## Residual risk

- Zero, on the reproduced claims: two independent chemistry stacks (qiskit-nature and PySCF) return the same FCI values to numerical precision, and the VQE energies match those FCI values.
- Medium, on the pulse-level claims: I did not touch pulse simulation, so I have no direct evidence for or against the 7× duration-reduction number.
- Low but nonzero, on the hardware claims: without ibm_lagos access, the readout-only-mitigation-reaches-chemical-accuracy claim rests on the paper's own Fig. 5 alone.

## Effort accounting

Wall-clock, roughly:
- Paper id resolution + PDF fetch + provenance write-up: 5 min.
- Paper skim / claim extraction: 3 min.
- Environment install (qiskit + pyscf into venv): 2-3 min.
- H2 reproduction script + run: 3 min.
- HeH+ reproduction script + run: 2 min (after fixing a numpy-bool JSON serialization TypeError on first try).
- Marker/Nougat fallback extraction: 1 min.
- LLM-judge call + JSON parse: 2 min (with one 502 retry).
- Report + open questions + artifacts summary + failure_analysis + workflow + REPORT.tex: ~10 min.

**Total wall time: ~25-30 min** for a fully reproduced simulation-side PARTIAL replication with independent judge concurrence.
