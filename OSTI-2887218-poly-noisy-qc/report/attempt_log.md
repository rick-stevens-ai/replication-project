# Attempt log — OSTI 2887218

All timestamps CDT, 2026-07-05.

- **18:07**  Read WAVE_BRIEF_2026-07-01.md. Assigned target = OSTI 2887218 (Schuster–Yin–Gao–Yao, "A Polynomial-Time Classical Algorithm for Noisy Quantum Circuits", *Phys. Rev. X* 15, 041018, 2025). Created target dir; no existing report.
- **18:08**  Fetched paper via `ssh uicgpu` (needed `~/env.sh` for proxy). 1.2 MB PDF saved. Confirmed with `file` = PDF v1.4, 31 pages.
- **18:09**  Attempted the `pdf` tool for extraction — blocked by (a) OpenClaw sandbox path restriction on Dropbox and (b) Anthropic API credit exhaustion; the tool errored on all three back-ends including gemini-3-flash and gpt-5.5 (extract plugin disabled). Fallback: `pdftotext -layout`, 2227 lines, clean.
- **18:10**  Read paper text; confirmed it is a PURE THEORY paper.  3 figures are all schematics; NO numerical benchmarks; NO code/data availability statement.  Grep for github/zenodo/repository: nothing.
- **18:11**  Designed replication plan: implement Algorithm 1 (Pauli-path truncation for uniform depolarizing noise) from scratch, verify convergence against exact density-matrix Kraus simulation on brick-wall 1-D random circuits, and test the paper's two quantitative predictions ((V2) higher γ → smaller truncation error at fixed ℓ; (V3) #paths poly(n) at fixed ℓ).
- **18:12**  Wrote first version of `replication.py`. Built dense 4^n × 4^n Pauli transition tables — for n = 6 this materialised 4096 × 64² matrices ~ 128 MB and the numpy contractions took > 10 min. Killed via `process` but discovered the remote python did NOT die (killing SSH session ≠ killing the child process on the remote box). Recovered by `ssh uicgpu 'kill -9 <pid>'`. **LESSON**: `process kill` only kills the SSH driver; for remote heavy jobs, always track remote PID separately.
- **18:15**  Rewrote to LOCAL 2-qubit factorisation. `two_qubit_transition_table(U)` is 16 × 16 ≤ 4 KB and per-layer DP factorises across independent gates. Runtime for the full experiment drops to < 30 s.
- **18:19**  First good run: Algorithm 1 saturates at 799 non-zero end states but does NOT match exact simulation at ℓ = max — residual error ≈ 8 % of exact value at γ = 0.05. Something was wrong with the algorithm's damping / endian / channel convention.
- **18:20**  Debugged systematically:
    1. Verified `state_pauli_coeffs_comp` reconstructs |x⟩⟨x| exactly (all 8 basis states, err = 0).
    2. Wrote `min_verify.py`: n = 2, d = 1, γ = 0 → Alg 1 at ℓ ≥ 3 hits the exact value at machine precision. So Alg 1 for γ = 0 was correct.
    3. Wrote a direct Heisenberg evolution and confirmed exact ≠ Alg 1 for γ > 0.
    4. Wrote a full-dimension `alg1_full` that avoids the factorisation. Still disagreed → not a factorisation bug.
    5. Wrote `schrod_pauli.py`: do Schrödinger evolution entirely in Pauli basis, applying damping `e^{-γ·w[P]}` per Pauli component after each layer. Result: `0.60215` — matches Alg 1 exactly, but exact_expectation gives `0.53541`.
    6. **Realised the bug**: my `apply_local_depolarizing_all` used Kraus `p = 1 − e^{−γ}` with the standard `(1−p) ρ + (p/3)(XρX+YρY+ZρZ)` form. That gives eigenvalue on non-I Paulis of `1 − 4p/3`, NOT `e^{−γ}`. Paper's channel is `D(ρ) = e^{−γ} ρ + (1−e^{−γ}) tr(ρ) I / 2`, which in the standard Kraus form corresponds to `q = (3/4)(1 − e^{−γ})`, not `p = 1 − e^{−γ}`.
- **18:22**  Fixed the Kraus rescaling in `apply_local_depolarizing_all`.
- **18:22**  Re-ran verify: at ℓ ≥ 4 for n = 4 d = 3, `|Alg1 − exact| < 5 × 10^{−16}` (machine precision) at every γ. V1 SUCCESS.
- **18:23**  Ran full experiment: V1 (convergence table for γ ∈ {0.05,…,0.8}), V3 (n = 3, 4, 5, 6, 8, 10 poly-scaling). All numerics consistent.
- **18:25**  Ran additional RMS-over-ensemble experiment (12 random circuits per (γ, ℓ)) to reproduce the paper's actual guarantee — the *average-case* error bound of Theorem 1. Result: RMS error is a strictly monotone decreasing function of γ at every ℓ and a strictly monotone decreasing function of ℓ at every γ. V2 SUCCESS on the paper's actual statistical claim.
- **18:29**  Copied artifacts back to Dropbox target dir.
- **18:30**  Launched nougat OCR on paper.pdf on uicgpu (in conda env `nougat`) — running in background.
- **18:32**  Wrote REPORT.md, brief.md, attempt_log.md, artifact_harvest.md, open_questions.json, workflow.md, failure_analysis.md, artifacts_summary.md, and REPORT.tex.

## Bugs I hit and their root cause

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| B1 | Remote python survives after `process kill` | `process kill` only kills the local SSH driver; remote process orphans | `ssh <host> 'kill -9 <pid>'` |
| B2 | Alg 1 at ℓ = max ≠ exact | `apply_local_depolarizing_all` used Kraus `p = 1−e^{-γ}` giving eigenvalue `1−4p/3` on Paulis, not `e^{-γ}` | Rescale `q = 3/4 · (1−e^{-γ})` |
| B3 | Alg 1 amplitude table transposed | Computed `U P U†` (Schrödinger) when paper's `a_{PQ}` requires `U† P U` (Heisenberg) | Swapped `U ↔ U†` in `two_qubit_transition_table` |
| B4 | Alg 1 iterated layers forward but paper indexes t = 1..d in REVERSE (observable→state) | `layers` list order vs Heisenberg time-order | Iterate `reversed(layers)` |
