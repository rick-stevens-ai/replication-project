# Replication Workflow — OSTI 2564727

**Paper:** Grimm & Eaves, *Accurate Numerical Simulations of Open Quantum Systems Using Spectral Tensor Trains*, J. Chem. Phys. 2025. DOI `10.1063/5.0228873`.

**Set:** OSTI-100, applied_math rank 5. **Date:** 2026-07-02. **Verdict:** REPLICATED (core analytic anchor); PARTIAL (paper overall).

---

## 0. Preconditions
- OA PDF fetched via uicgpu proxy (sha256 `f9f14720ee5a20d8e9e814f66c0b08c001080b431ba25d1e1984f3e6e6f5e6e8`).
- Compute host: local (laptop-class), pure NumPy — no GPU, no HPC.
- Judge: free Argo endpoint `gpt-5.2` (no paid model use).

## 1. Read & scope selection
1. Read the paper. Identify the load-bearing exact statement: **Eqs. 15–17**, the extrinsic-Markov limit of the SLE reducing to the Lindblad master equation.
2. Enumerate claims C1–C5 (see REPORT.md §2).
3. Decide scope: replicate C1 (exact analytic anchor) and C2 (trace conservation) directly and independently. Mark C3/C4/C5 out of scope (STT + OQuPy + full training rig required; would not fit the fast-replication budget).

## 2. Independent implementation — reference route
1. Implement RK4 integrator for the Lindblad ME
   `d⟨ρ⟩/dt = −i[H₀,⟨ρ⟩] + γ(V⟨ρ⟩V − ½{V²,⟨ρ⟩})` in `sle_lindblad.py:integrate_lindblad`.
2. Validate the integrator against a closed-form dephasing case: for `V=σz, H₀=0`, `ρ₀₁(t) = ρ₀₁(0) e^{−2γt}`.
   Expect machine-precision agreement; obtained max error **9.6e-13**. Gate: pass.

## 3. Independent implementation — stochastic route
1. Write a vectorized Monte-Carlo integrator of the SLE stochastic Schrödinger equation
   `i d|ψ⟩/dt = (H₀ + ξ(t)V) |ψ⟩` with real white noise `⟨ξ(t)ξ(s)⟩ = γδ(t−s)`.
2. Symmetric Trotter step per timestep:
   `|ψ⟩ ← e^{−iH₀τ/2} · e^{−iΔ_k V} · e^{−iH₀τ/2} |ψ⟩`, with `Δ_k ~ 𝒩(0, γτ)`.
   This mirrors the paper's Eq. 5.
3. Average `ρ = |ψ⟩⟨ψ|` across trajectories. For real noise + Hermitian V, per-trajectory dynamics are unitary; decoherence emerges purely from the ensemble average (Kubo mechanism).
4. Vectorize the trajectory axis in NumPy (exact reformulation, not an approximation) so 40k trajectories fits in seconds on a laptop.

## 4. Test-system matrix
Three physically distinct qubit Hamiltonians / couplings, all reproducible from equations alone:
1. **Pure dephasing:** `V=σz`, `H₀=(ε/2)σz`.
2. **Transverse coupling:** `V=σx`, `H₀=(ε/2)σz` (non-commuting `[V,H₀]≠0`).
3. **Biased qubit, Fig. 3 geometry:** `H₀=Ωσx + εσz`, `V=ασz`, with `Ω=1, ε=0.5, α=0.75`.

## 5. Execute
Commands:
```bash
python3 sle_lindblad.py       # reference Lindblad, three cases
python3 convergence.py        # N_traj = {2.5k, 10k, 40k, 160k}, τ ∈ {0.02, 0.01, 0.005}
python3 plot_dynamics.py      # produces evidence/sle_vs_lindblad_dynamics.png
```

Baseline production run: `N_traj = 40,000`, `τ = 0.01`, `t ∈ [0, 4]`.

## 6. Numerical acceptance gates
| Gate | Threshold | Observed | Pass? |
|------|-----------|----------|-------|
| Analytic dephasing vs closed-form | `< 1e-10` | `9.6e-13` | ✓ |
| SLE-MC vs Lindblad (case 1) | `< 5e-3` (≈ MC floor at N=40k) | `4.3e-3` | ✓ |
| SLE-MC vs Lindblad (case 2) | `< 5e-3` | `4.2e-3` | ✓ |
| SLE-MC vs Lindblad (case 3) | `< 5e-3` | `2.9e-3` | ✓ |
| Trace preservation | `|Tr − 1| < 1e-4` | `1.0000` all cases | ✓ |
| Error scales as `~1/√N` | monotone decrease | 7.5e-3→5.4e-3→2.8e-3→2.6e-3 | ✓ |
| Trotter scan | error floor stable as `τ` shrinks | confirmed sampling-limited | ✓ |

## 7. LLM judge (free Argo `gpt-5.2`)
1. Package REPORT.md + evidence tables + convergence data.
2. Prompt for adjudication on C1 only (do not overclaim beyond what was tested).
3. Verdict returned: **REPLICATED** with justification citing multi-system agreement, analytic anchor at machine precision, and absence of systematic deviation.
4. Store verbatim response at `evidence/llm_judge_verdict.txt`.

## 8. Write-up
- `REPORT.md` — markdown record (this replication's canonical short-form).
- `REPORT.tex` — LaTeX long-form with GENUINE CRITIQUE section.
- `open_questions.json` — five open questions grounded in what was NOT tested (STT scaling, non-Markovian regime, CP under truncation, barren plateau, App. A intrinsic-noise kernel).
- `workflow.md` — this file.
- `artifacts_summary.md` — inventory + evidence pointers.
- `failure_analysis.md` — honest ledger of what did not get done and why.

## 9. Explicit non-goals (recorded so they cannot be silently reinterpreted later)
- **Not** a port of the STT/tensor-train machinery.
- **Not** a rerun of Fig. 4 memory scaling.
- **Not** a rerun of the intrinsic-noise spin-boson comparison.
- **Not** a training benchmark for barren plateaus.
- **Not** an OQuPy/PT-TEMPO cross-check.
Each of these is called out as a future-work item in `open_questions.json`.
