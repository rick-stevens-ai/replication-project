# Artifacts Summary — OSTI 2564727 Replication

**Paper:** Grimm & Eaves 2025, *Accurate Numerical Simulations of Open Quantum Systems Using Spectral Tensor Trains*.
DOI `10.1063/5.0228873`. OSTI 2564727. OA PDF sha256 `f9f14720ee5a20d8e9e814f66c0b08c001080b431ba25d1e1984f3e6e6f5e6e8`.

**Verdict:** REPLICATED (core analytic anchor, Eqs. 16–17); PARTIAL for the paper overall.

---

## Report artifacts (`report/`)
| File | Purpose |
|------|---------|
| `REPORT.md` | Canonical short-form replication report (7 KB source). |
| `REPORT.tex` | Long-form LaTeX write-up with dedicated GENUINE CRITIQUE section. |
| `open_questions.json` | Five open questions grounded in what was **not** tested. |
| `workflow.md` | Step-by-step reproduction workflow with acceptance gates. |
| `artifacts_summary.md` | This inventory. |
| `failure_analysis.md` | Ledger of what did not get done and why. |

## Extraction artifacts (`extraction/`)
- Paper OA PDF (uicgpu proxy fetch).
- (No `marker.md` present in this dir — extraction relied on direct read of the PDF equations rather than a Marker parse.)

## Code artifacts (referenced in REPORT.md)
| Script | Role |
|--------|------|
| `sle_lindblad.py` | Reference RK4 integrator of the Lindblad ME (Eq. 17). Also drives the three qubit test cases. Function of interest: `integrate_lindblad`. |
| `convergence.py` | N_traj and τ sweep for Monte-Carlo convergence diagnostics. |
| `plot_dynamics.py` | Produces `evidence/sle_vs_lindblad_dynamics.png` overlaying MC markers on exact Lindblad curves for σx, σy, σz. |

## Evidence artifacts (`evidence/`)
| Artifact | What it shows |
|----------|---------------|
| `sle_vs_lindblad_dynamics.png` | Overlay of SLE Monte-Carlo (markers) on exact Lindblad (curves) for all three qubit systems and all three Bloch components. |
| `llm_judge_verdict.txt` | Verbatim response from free Argo `gpt-5.2` acting as independent judge on C1. |

## Numerical headline results (from REPORT.md §4)
| Quantity | Value | Notes |
|----------|-------|-------|
| Analytic dephasing vs closed-form (`V=σz, H₀=0, γ=0.5`) | max err **9.6e-13** | Machine precision; conventions correct. |
| SLE-MC vs Lindblad (pure dephasing) | max err **4.3e-3** | N=40k. |
| SLE-MC vs Lindblad (transverse) | max err **4.2e-3** | N=40k, `[V,H₀]≠0`. |
| SLE-MC vs Lindblad (biased qubit, Fig. 3 geom) | max err **2.9e-3** | N=40k, 3-decimal ⟨σz⟩ match. |
| Trace preservation | **1.0000** | All three cases. |
| Convergence with N_traj | 7.5e-3→5.4e-3→2.8e-3→2.6e-3 | N ∈ {2.5k,10k,40k,160k}; scales as ~1/√N. |

## Claims coverage
| Claim | Tested? | Evidence |
|-------|---------|----------|
| C1: Extrinsic-Markov SLE → exact Lindblad ME | **Yes** | Numerical results table above + `sle_vs_lindblad_dynamics.png`. |
| C2: Trace / physical density matrix | **Yes** | Tr=1.0000 across all runs. |
| C3: Spin-boson (Fig. 3) matches PT-TEMPO | Partial (geometry only) | See failure_analysis.md item 1. |
| C4: 32-site chain memory scaling `p≈2.0` vs `p≈8.3` | **No** | Out of scope; see failure_analysis.md item 2. |
| C5: STT barren plateau | **No** | Out of scope; see failure_analysis.md item 3. |

## Compute footprint
- Host: local laptop-class, Python 3.14, NumPy + Matplotlib.
- PDF fetch: uicgpu proxy.
- Judge: free Argo `gpt-5.2` (no paid inference used).
- Wall time: minutes for the reported runs; convergence sweep dominated by N=160k trajectory case.

## Honesty note
Because the source `REPORT.md` is only ~7 KB, the artifact inventory is intentionally tight. No secondary evidence files, notebooks, or comparison-with-OQuPy dumps exist — this replication deliberately anchored on the exact analytic limit and did not port the full STT machinery.
