# Independent Replication — Figueiras et al. (2018): Split-Step (BPM) Solver for the Schrödinger Equation

**Paper:** E. Figueiras, D. Olivieri, A. Paredes, H. Michinel, *"An open source virtual laboratory for the Schrödinger equation,"* European Journal of Physics **39** (2018) 055802. DOI: [10.1088/1361-6404/aac999](https://doi.org/10.1088/1361-6404/aac999). Open Access (CC-BY 3.0, IOP).

**Set:** PDE-100 · **Family:** Schrödinger / nonlinear Schrödinger (NLSE) — *previously uncovered in the set.*

**Replication mode:** Fully independent from-scratch reimplementation of the split-step Fourier (beam-propagation-method) scheme using only numpy FFTs. The authors' supplementary code library was **not** downloaded or consulted; the solver was written directly from the paper's equations. Correctness was validated against **closed-form analytic solutions first**, then the paper's headline phenomena and stated accuracy order were reproduced.

---

## 1. Paper summary

The paper presents a simple, educational Python library that integrates the dimensionless time-dependent Schrödinger equation

> **eq. (1):**  i ∂ψ/∂t = −½ ∇²ψ + V ψ   (1D or 2D; V may depend on ψ → nonlinear)

with a **first-order split-step Fourier (Lie-splitting) method**, paper **eq. (2)**:

> ψ(x, t+dt) = 𝓕⁻¹[ e^(−i·dt·k²/2) · 𝓕[ e^(−i·dt·V) ψ(x,t) ] ]

realized as steps I–V (potential kick in position space → FFT → kinetic phase in Fourier space → IFFT → advance t). It demonstrates the method on linear examples (reflectionless Pöschl-Teller scattering, barriers, double wells, 2D vortex/Gaussian beams) and nonlinear examples (bright solitons, soliton collisions, filamentation, BEC/Gross-Pitaevskii vortex precession). It states the scheme conserves ∫|ψ|² for real V and is **first-order accurate, error O(dt)**.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|----|-------|------|-----------|---------|--------|
| **C1** | Split-step Fourier algorithm (eq. 2) integrates the TDSE; norm ∫\|ψ\|² conserved for real V | numerical method | Yes | ✅ | **Reproduced** — exact vs analytic free propagator (L2 ≈ 1e-14); norm conserved to ≈1e-13 |
| **C2** | V = −s(s+1)/cosh²x is reflectionless (T=1, R=0) for integer s (Fig 1: s=10) | physics claim | Yes | ✅ | **Reproduced** — split-step: R≈1e-8, T=1.000000 for s=10,1,2,3; exact closed form R=0 iff s∈ℤ |
| **C3** | Bright soliton (eq. 5) of focusing cubic NLSE (κ=−1) propagates undisturbed; two solitons collide and emerge unchanged (Fig 2) | physics claim | Yes | ✅ | **Reproduced** — peak 1.00007 (exact 1), COM exact, field L2 vs eq-5 ≈7e-4; collision peaks preserved to 1e-4 |
| **C4** | Scheme is first-order, error O(dt) | accuracy claim | Yes | ✅ | **Reproduced** — self-convergence orders 1.0005 / 1.0002 / 1.0001 |

## 3. Method (independent implementation)

**Environment:** CherryRd (local, Darwin), CPU only. Python 3.14.6; numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8.
**Paper PDF sha256:** `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`.

1. **Solver `work/bpm.py`** — `BPM1D`/`BPM2D` classes. Uniform periodic grid; angular wavenumbers `k = 2π·fftfreq(N,dx)`; kinetic propagator `exp(−i·dt·k²/2)` (Laplacian → −k²). One step = potential kick (position) → FFT → kinetic phase (Fourier) → IFFT (paper eq. 2 / steps I–V). Nonlinear term supplied as V(ψ)=κ|ψ|². No third-party PDE solver; FFTs only.
2. **Test 1 — analytic-first, free Gaussian** (`test1_free_gaussian.py`): compared to the exact free Schrödinger propagator of a minimum-uncertainty Gaussian. Verified IC match (8e-17), full-field L2 vs analytic at T=8, group velocity (COM = x₀+k₀T), and Gaussian spreading law σ(T)=√(a₀²/2·(1+(T/a₀²)²)).
3. **Test 3 — reflectionless scattering** (`test3_reflectionless.py`): broad Gaussian packet incident on V=−s(s+1)/cosh²x; reflected fraction = ∫|ψ̂(k<0)|²/∫|ψ̂|² after the packet clears the well.
4. **Test 3d — exact closed form** (`test3d_verify_formula.py`): derived R(k,s)=sin²(πs)/(sinh²(πk)+sin²(πs)) [using √(1+4s(s+1))=2s+1], proving R=0 iff s is an integer, and numerically confirming (1e-32 for integer s).
5. **Test 4 — bright soliton** (`test4_soliton.py`): single-soliton vs exact eq. (5); two-soliton head-on collision, comparing pre/post peaks & norm.
6. **Test 5 — order** (`test5_order_selfconv.py`): Cauchy self-convergence on the nonlinear soliton (non-commuting operators → genuine Lie error); successive-halving L2 differences.

Run commands: `python3 test1_free_gaussian.py`, `... test3_reflectionless.py`, `... test3d_verify_formula.py`, `... test4_soliton.py`, `... test5_order_selfconv.py`, `... make_figs.py`.

## 4. Results vs paper

| Quantity | Paper | This replication | Agreement |
|---|---|---|---|
| Norm conservation (real V) | conserved (stated) | \|norm−1\| ≈ 1e-13 (all runs) | ✅ exact to roundoff |
| Free-propagation accuracy | (implicit; exact for V=0) | L2 vs analytic ≈ 1e-14; σ(T) to 12 digits | ✅ |
| Reflectionless, integer s (Fig 1, s=10) | T=1, R=0 | R≈2.6e-8, T=1.000000 (s=10); R=0 exactly (closed form) | ✅ |
| Bright soliton shape (eq. 5) | undisturbed propagation | peak 1.00007 (exact 1), field L2 ≈ 7e-4 over T=15 | ✅ |
| Two-soliton collision (Fig 2) | emerge unchanged | peaks 1.0 → 0.99989 (≤1e-4 change), norm 4.0000 | ✅ |
| Order of accuracy | first order, O(dt) | observed order 1.0005, 1.0002, 1.0001 | ✅ |

Figures reproduced: `evidence/fig1_reflectionless_s10.png` (Fig 1), `evidence/fig2_soliton_collision.png` (Fig 2). Raw numbers: `evidence/evidence_test{1,3,3d,4,5}.json`.

## 5. Internal consistency / notes

- The paper writes the kinetic factor as `exp(i/2·dt·(2πk)²)` under an FFT convention where the Laplacian eigenvalue is −(2πk)²; with an angular-wavenumber grid this is `exp(−i·dt·k²/2)`. Signs must be mutually consistent; we pinned them by requiring the free case to reproduce the exact analytic propagator (it does, to 1e-14). No inconsistency in the paper — just a convention that must be tracked.
- The paper's stated norm conservation and first-order accuracy both hold quantitatively.
- **Honest negative:** an auxiliary stationary-Schrödinger ODE scattering integrator (`test3c`) was numerically unstable for *odd* integer s (spurious R≈0.44) due to the reflectionless case requiring exact cancellation of an exponentially growing mode; it was **discarded** and replaced by the exact closed form (Test 3d). This does not affect any paper claim — the split-step wavepacket (Test 3) and the closed form both confirm reflectionless behavior for integer s.

## 6. Multi-judge assessment (free Argo endpoints, temperature 0)

| Judge | Verdict | Coverage |
|---|---|---|
| argo:gpt-5.2 | REPLICATED | C1,C2,C3,C4 |
| argo:gemini-2.5-pro | REPLICATED | C1,C2,C3,C4 |
| argo:gpt-4.1 | REPLICATED | C1,C2,C3,C4 |

Unanimous. (Raw: `evidence/evidence_judges.json`.)

## Verdict
**Verdict:** REPLICATED

The split-step Fourier (BPM) method for the linear and nonlinear time-dependent Schrödinger equation was independently reimplemented from scratch and validated against exact analytic solutions (free Gaussian propagation to ~1e-14, norm conservation to ~1e-13). All four testable claims were reproduced quantitatively: reflectionless integer-s Pöschl-Teller scattering (split-step R≈1e-8 / closed-form R=0), bright-soliton propagation and shape-preserving collision (peaks preserved to 1e-4), and first-order O(dt) temporal accuracy (observed order 1.000). Three independent free-endpoint LLM judges unanimously scored REPLICATED with full C1–C4 coverage.

WAVE_RESULT set=PDE-100 paper=Figueiras2018-Schrodinger-BPM-splitstep(DOI:10.1088/1361-6404/aac999) verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/PDE-Figueiras-Schrodinger-BPM-splitstep-2018 one_line=From-scratch split-step Fourier TDSE/NLSE solver reproduces reflectionless integer-s Poschl-Teller scattering, bright-soliton propagation+collision, norm conservation (~1e-13), free-propagation accuracy (~1e-14), and first-order O(dt) accuracy; 3/3 free judges REPLICATED.
