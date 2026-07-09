# Replication Workflow — Figueiras et al. (2018), Split-Step BPM for Schrödinger

Paper: EJP 39 (2018) 055802, DOI 10.1088/1361-6404/aac999.
Mode: **from-scratch independent reimplementation**; authors' shipped code library not consulted.
Environment: CherryRd (Darwin, CPU-only). Python 3.14.6, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8.

## Stages

### 1. Paper ingestion
- Downloaded PDF; recorded sha256 `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`.
- Extracted the dimensionless TDSE (eq. 1) and the split-step Lie update (eq. 2 / steps I–V).
- Built a **claims table** (C1–C4): solver + norm conservation, integer-s Pöschl-Teller reflectionless scattering (Fig 1), bright soliton + collision (Fig 2), and first-order O(dt) accuracy.

### 2. Solver implementation (`work/bpm.py`)
- `BPM1D` / `BPM2D` classes with uniform periodic grid.
- Angular wavenumbers `k = 2π · fftfreq(N, dx)`.
- One time step:
  1. potential kick in position space: `ψ ← exp(-i·dt·V) ψ`
  2. forward FFT
  3. kinetic phase in Fourier space: `ψ̂ ← exp(-i·dt·k²/2) ψ̂`
  4. inverse FFT
  5. advance `t ← t + dt`
- Nonlinear branch: `V(ψ) = κ |ψ|²` (focusing NLSE: κ = −1).
- FFTs only; no third-party PDE library.

### 3. Convention pinning
- Reconciled the paper's kinetic factor `exp(i·dt·(2πk)²/2)` (FFT convention where Laplacian eigenvalue is −(2πk)²) with the angular-wavenumber convention `exp(-i·dt·k²/2)`.
- Verified by requiring the free case to reproduce the exact analytic Schrödinger propagator (matches to ~1e-14). Signs pinned.

### 4. Analytic-first validation
- **Test 1** — Free Gaussian (`test1_free_gaussian.py`): compare to exact free propagator of a minimum-uncertainty Gaussian. Check IC match, full-field L2 at T=8, group velocity (COM = x₀ + k₀T), Gaussian spreading law σ(T) = √(a₀²/2 · (1 + (T/a₀²)²)).

### 5. Paper-phenomenon reproduction
- **Test 3** — Reflectionless scattering (`test3_reflectionless.py`): broad Gaussian packet on `V = -s(s+1)/cosh²x`; reflected fraction from Fourier partition `∫|ψ̂(k<0)|² / ∫|ψ̂|²` after packet clears the well. Tested s ∈ {1, 2, 3, 10}.
- **Test 3d** — Closed form (`test3d_verify_formula.py`): derived `R(k,s) = sin²(πs) / (sinh²(πk) + sin²(πs))` using √(1+4s(s+1)) = 2s+1, proving R=0 iff s ∈ ℤ; numerical confirmation at ~1e-32 for integer s.
- **Test 4** — Bright soliton (`test4_soliton.py`): single soliton vs exact eq. (5); two-soliton head-on collision (pre/post peaks and norm).

### 6. Accuracy order
- **Test 5** — Self-convergence (`test5_order_selfconv.py`): Cauchy self-convergence on the nonlinear soliton (non-commuting operators → genuine Lie error). Successive dt-halving L2 differences → observed orders 1.0005 / 1.0002 / 1.0001.

### 7. Discarded / honest negatives
- **`test3c`** (stationary-Schrödinger ODE scattering integrator) was numerically unstable for *odd* integer s (spurious R ≈ 0.44) because reflectionless case requires cancellation of an exponentially growing mode. **Discarded**; replaced by closed-form Test 3d. Documented in REPORT.md §5 as an explicit replication-side failure.

### 8. Figure production (`make_figs.py`)
- `evidence/fig1_reflectionless_s10.png` (reproduces paper Fig 1).
- `evidence/fig2_soliton_collision.png` (reproduces paper Fig 2).

### 9. Evidence capture
- Raw numerical results → `evidence/evidence_test{1,3,3d,4,5}.json`.
- Judge outputs → `evidence/evidence_judges.json`.

### 10. Multi-judge assessment
- Three Argo free-endpoint judges at temperature 0: argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1.
- Coverage matrix: each judge scored C1–C4 individually.
- Result: unanimous **REPLICATED**, full C1–C4 coverage per judge.

### 11. Verdict + reporting
- REPORT.md (canonical narrative + claims/results tables).
- REPORT.tex (typeset version + genuine-critique section).
- open_questions.json (five open questions grounded in what was NOT tested).
- artifacts_summary.md, failure_analysis.md, workflow.md (this file) — reproducibility artifacts.
- WAVE_RESULT one-line emitted for wave-level aggregation.

## Execution commands (run from `work/`)
```
python3 test1_free_gaussian.py
python3 test3_reflectionless.py
python3 test3d_verify_formula.py
python3 test4_soliton.py
python3 test5_order_selfconv.py
python3 make_figs.py
```

## Key design choices
- **Analytic-first**: exact free propagator before any paper-specific test — this is what caught the sign-convention issue and gave a 1e-14 floor to trust downstream results against.
- **Closed-form scattering coefficient** instead of relying on the ODE integrator, because reflectionless integer-s is a delicate exact-cancellation condition and the wavepacket measurement + closed form together are stronger evidence than either alone.
- **Cauchy self-convergence on the nonlinear soliton** for the O(dt) claim, because the operator non-commutativity there is what actually generates the Lie splitting error — a linear or free-field test would be misleadingly clean.
- **Kept the failed `test3c` in the workflow record**, not silently dropped, so provenance is honest.
