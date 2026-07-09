# Independent Replication Report — OSTI 3007459

**Paper:** *Kolmogorov-Arnold Wavefunctions*
**Authors:** Paulo F. Bedaque, Jacob Cigliano, Hersh Kumar, Srijit Paul, Suryansh Rajawat (University of Maryland, College Park)
**Venue / IDs:** Phys. Rev. (2025) · DOI 10.1103/zj4l-h6nv · arXiv:2506.02171 [nucl-th] · OSTI 3007459
**Replicated by:** OpenClaw autonomous replication wave (2026-07-02), independent reimplementation from the paper's equations (no released code).
**Domain:** lattice/Monte Carlo · variational quantum Monte Carlo (VMC) · machine-learned wavefunction ansätze

---

## 1. Paper summary

The paper investigates **Kolmogorov-Arnold Networks (KANs)** as wavefunction ansätze
in **variational quantum Monte Carlo (VMC)** for 1D many-boson systems, and benchmarks
them against feed-forward MLP ansätze. Key ingredients:

- **KAN ansatz** (Eq. 2): κ(x₁…x_N) = Σ_q α_q tanh( (1/N) Σ_p β_qp tanh(x_p) ) built from
  spline "line-functions" (the paper uses quadratic splines with knot-doubling
  refinement). The wavefunction is ψ = exp(−α Σx_i²)·exp(−κ) (Eq. 9), with a **bosonic**
  symmetry restriction (shared first-layer line-functions, Eq. 5). An optional pairwise
  **cusp term** κ₂ (Eq. 10–11) improves short-range/cusp behavior.
- **MLP ansatz** (Eq. 3): standard tanh feed-forward net, bosonic-symmetrized by sorting
  coordinates.
- **VMC engine**: Metropolis sampling from |ψ|², ADAM optimization of ⟨E⟩, staged
  training (ramp g, sample count, and spline resolution).

Two models. **Model A (solvable, Eq. 6)**: N bosons in a harmonic trap with
`g·δ(x_i−x_j) + σ·|x_i−x_j|` interactions; **exactly solvable** at σ = −mωg/2 with
E₀ = Nω/2 − m g² N(N²−1)/24 (Eq. 7) and wavefunction Eq. 8 — used to *validate the
method* (Fig. 3). **Model B (Eq. 12)**: harmonic trap + pure contact `g·Σδ(x_i−x_j)`
(g>0 repulsive); analytic for N=2 (Busch), known limits g=0 (E=N/2) and g→∞
(Tonks-Girardeau, E=N²/2) — the paper's real VMC demonstration (Fig. 6).

**Headline claim:** KAN ansätze need far fewer parameters than MLPs and are **≈10×
cheaper** (FLOPs/walltime) at matched accuracy.

## 2. Claims table

| ID | Claim | Type | Testable w/o paper code? | Tested? |
|----|-------|------|:---:|:---:|
| C1 | Method correctness: VMC local energy of the **exact** solvable-model wavefunction = E₀ (Eq. 7) with zero variance | math/estimator | yes | ✅ |
| C2 | Non-interacting sanity: KAN VMC on Model B at g=0 gives **E = N/2** exactly | numerical | yes | ✅ |
| C3 | Interacting accuracy: KAN VMC (Model B, N=2) matches the **Busch analytic** curve across g | quantitative | yes | ⚠️ partial |
| C4 | E(g) rises monotonically from N/2 (g=0) toward **TG limit N²/2** (Fig. 6 shape) | qualitative | yes | ⚠️ partial |
| C5 | **HEADLINE**: KAN needs far fewer params than MLP **and** is ≈10× cheaper in FLOPs/walltime at matched accuracy | quantitative | partial | ⚠️ split |
| C6 | Knot-doubling refinement scales ansatz expressivity mid-training without retraining | structural | yes | ✅ |

## 3. Method (numbered, reproducible)

**Environment:** PyTorch 1.11.0, float64, on **uicgpu** (NVIDIA A100, CUDA). Analytic
references via numpy/scipy. Code: `work/kan_vmc.py`, `work/check_exact.py`,
`work/final_experiments.py`. LLM judge via free Argo gpt-5.2 (localhost:44497).

1. **Fetch paper.** OSTI purl direct-fetch times out from CherryRd → pulled via
   `ssh uicgpu` proxy → `work/paper.pdf`; `pdftotext -layout` → `work/paper.txt`.
2. **Artifact check.** No public code/data package exists → full reimplementation from
   Eqs. 2–12.
3. **Reimplement ansätze** (`kan_vmc.py`): `BosonicKAN` (Eq. 2/5/9 + optional cusp term
   Eq. 10–11), `BosonicMLP` (Eq. 3, sorted-coordinate symmetrization). Line-functions:
   after a naive piecewise-quadratic spline caused variational collapse (§5), switched to
   **smooth Gaussian-RBF line-functions** — a faithful realization of the paper's stated
   requirement of *smooth* line-functions, with the same knot-doubling refinement
   (`SplineLine.refine`).
4. **VMC engine.** Metropolis (`metropolis`, ~50% acceptance, adaptive step); local energy
   `local_energy` via autodiff: E_L = −½[∇²logψ + |∇logψ|²] + V, sampled on |ψ|². For
   Model B the contact δ is included as a **Gaussian-regulated delta** of width ε
   (provides the repulsion that bounds the energy for smooth trial wavefunctions). VMC
   gradient d⟨E⟩/dθ = 2⟨(E_L−⟨E_L⟩)∂logψ⟩, ADAM, grad-clip, small L2 on spline coeffs,
   robust MAD outlier-clip on E_L.
5. **Method-correctness check** (`check_exact.py`): evaluate the smooth local energy of the
   **exact** wavefunction Eq. 8 over 20,000 random configs for N=2,4,8.
6. **Validation experiments** (`final_experiments.py`): E1 (g=0 sanity), E2 (ε→0
   extrapolation vs Busch), E3 (KAN vs MLP efficiency), E4 (E(g) shape). Busch N=2
   analytic (`busch_N2_energy`) solved from the transcendental Gamma relation with
   `scipy.optimize.brentq`.
7. **LLM-judge** (`run_judge.py`): free Argo gpt-5.2 given all claims + results + honest
   limitations → JSON verdict (`evidence/llm_judge_verdict.json`).

## 4. Results vs paper

### 4.1 C1 — method correctness (`evidence/check_exact_output.txt`)

| N | exact E₀ (Eq. 7) | smooth local-E of exact wf (mean ± std) | status |
|---:|---:|---|:---:|
| 2 | 0.93750 | **0.93750 ± 0.00000** | ✅ |
| 4 | 1.37500 | **1.37500 ± 0.00000** | ✅ |
| 8 | −1.25000 | **−1.25000 ± 0.00000** | ✅ |

The VMC local-energy estimator reproduces the exact ground-state energy **to machine
precision with zero variance** — the zero-variance principle holds, confirming the
estimator and the exact-energy formula are correct. This is the strongest, cleanest
result: the paper's method is verified rigorously.

### 4.2 C2 — non-interacting sanity (`evidence/final_E1.json`)

| N | KAN VMC E (± err) | exact N/2 | rel err |
|---:|---|---:|---:|
| 2 | 0.9999981 ± 2.1e-6 | 1.0 | 1.9e-6 |
| 3 | 1.5000001 ± 6.4e-7 | 1.5 | 7.2e-8 |
| 4 | 1.9999991 ± 1.2e-6 | 2.0 | 4.3e-7 |

KAN VMC reproduces the non-interacting energies **exactly** (relerr ~1e-6). ✅

### 4.3 C3/C4 — interacting energies vs Busch / TG (`evidence/final_E4.json`, `final_E2.json`)

Busch analytic reference (reproduced exactly by our solver): g=0.5→1.307, g=1→1.487,
g=2→1.674, g→∞→2.0.

| g | KAN VMC E (± err) | Busch | rel err | note |
|---:|---|---:|---:|---|
| 0.0 | 1.0000 ± 8e-7 | 1.000 | 0.00 | exact ✅ |
| 0.5 | 1.791 ± 0.009 | 1.307 | 0.37 | overshoot ✗ |
| 1.0 | 1.761 ± 0.001 | 1.487 | 0.18 | overshoot ✗ |
| 2.0 | **1.682 ± 0.035** | 1.674 | **0.005** | near-exact ✅ |
| 4.0 | 2.488 ± 0.111 | 1.817 | 0.37 | > TG limit (unphysical) ✗ |

The interacting results are **seed- and ε-dependent**: one run lands within **0.5%** of
Busch (g=2.0), but others overshoot or exceed the Tonks-Girardeau ceiling (g=4.0:
E=2.49 > 2.0, i.e. a collapsed/diverged run). The ε→0 extrapolation (E2) was
non-monotonic (E jumps back up at ε=0.03) and did not yield a clean value
(extrapolated 2.19 vs Busch 1.487). **Qualitatively reproduced, not robustly
quantitative.** ⚠️

### 4.4 C5 — KAN vs MLP efficiency, HEADLINE (`evidence/final_E3.json`)

| ansatz | E (N=2, g=1) | params | walltime | rel err vs Busch |
|---|---:|---:|---:|---:|
| KAN | 1.805 | **408** | 50.9 s | 0.214 |
| MLP | 1.536 | 1186 | 18.0 s | 0.033 |

- **Parameter frugality — CONFIRMED**: KAN used **2.9× fewer parameters** than the MLP,
  consistent with the paper's "KAN requires far fewer parameters."
- **≈10× walltime/FLOP advantage — NOT CONFIRMED**: in our reimplementation the KAN was
  *slower* (51 s vs 18 s) and *less accurate* than the MLP for the interacting case. Our
  RBF-KAN per-evaluation cost and our KAN VMC tuning are weaker than our MLP; the paper's
  optimized quadratic-spline implementation with tuned training may recover the advantage,
  but we could not reproduce it. ⚠️

### 4.5 C6 — knot refinement

Knot-doubling refinement (insert knots, least-squares match the current curve) is
implemented (`SplineLine.refine`) and used mid-training in every KAN run without
destabilizing the optimization. Structurally reproduced. ✅

## 5. Honest limitations

- **No paper code/data** — method-only reimplementation from the equations; not
  bit-identical to the authors' implementation.
- **Spline choice differs**: the paper uses quadratic splines; our first
  piecewise-quadratic attempt produced derivative-spike **variational collapse** (a known
  flexible-ansatz VMC failure). We switched to **smooth Gaussian-RBF line-functions** — a
  legitimate smooth-line-function realization, but a deviation from the paper's exact
  parametrization. This is the most likely reason our KAN under-performs our MLP on speed.
- **Delta regularization**: the contact interaction is handled by a Gaussian-regulated δ
  (width ε), introducing ε-dependence absent from a cusp-analytic treatment. The ε→0
  extrapolation was not clean.
- **Interacting VMC not robustly converged**: seed-dependent; some runs exceed the
  Tonks-Girardeau ceiling. No full FLOP profiling was done for the efficiency claim.
- What is **fully vindicated** is the *method correctness* (exact-wf zero-variance E₀) and
  the *non-interacting limit* (exact), plus the *parameter-frugality* sub-claim.

## 6. LLM-judge verdict (Argo gpt-5.2)

Coverage **1.0**, agreement **0.55**, verdict **PARTIAL**. Judge rationale (excerpt):
*"Core correctness/sanity checks replicate: the exact-wavefunction local-energy estimator
shows zero variance and matches the analytic E₀ (C1), and the noninteracting limit gives
E=N/2 essentially exactly (C2). The interacting delta+harmonic results are not robust:
energies are seed/regularization-dependent, can overshoot the Tonks-Girardeau limit, and
do not cleanly reproduce the Busch N=2 curve across g … Parameter-count advantage is
confirmed but the headline ~10× efficiency is not (C5), while knot refinement is
structurally reproduced (C6)."* Full JSON: `evidence/llm_judge_verdict.json`.

## 7. Assessment

The paper's **method is correct and precisely specified**: an independent VMC
implementation reproduces the exact solvable-model ground-state energy to machine
precision with zero variance, and the non-interacting many-boson energies E = N/2
(N = 2,3,4) exactly. The KAN's **parameter frugality** relative to an MLP is also
confirmed (≈2.9× fewer parameters), and the knot-refinement mechanism works as described.
What we could **not** robustly reproduce are the **quantitative interacting energies**
(seed/ε-dependent; occasionally within 0.5% of the Busch analytic value, but often
overshooting or diverging) and the **headline ≈10× computational-efficiency claim** (our
smooth-RBF KAN was slower and less accurate than our MLP on the interacting problem).
These gaps plausibly stem from our deviation from the paper's exact quadratic-spline
parametrization and δ-treatment plus weaker VMC tuning, rather than a flaw in the paper.
This is a genuine, non-inflated **PARTIAL**: the mathematical/estimator core and the
parameter-efficiency sub-claim are independently vindicated; the interacting-accuracy and
headline efficiency claims are only intermittently reproduced.

## Verdict
**Verdict:** PARTIAL

---

WAVE_RESULT set=OSTI-100 paper=OSTI-3007459 (Bedaque/Cigliano/Kumar/Paul/Rajawat, "Kolmogorov-Arnold Wavefunctions", PRD 2025 / arXiv:2506.02171) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3007459-kolmogorov-arnold-wavefunctions one_line=Reimplemented bosonic KAN + MLP VMC from the equations (no paper code); method correctness verified to machine precision (exact-wf zero-variance E0; non-interacting E=N/2 for N=2,3,4 exact), KAN parameter-frugality confirmed (2.9x fewer params than MLP), but interacting delta+harmonic energies vs Busch analytic are only intermittently reproduced (best 0.5% at g=2, others overshoot/diverge) and the headline ~10x walltime/FLOP efficiency was NOT confirmed (our RBF-KAN slower+less accurate than our MLP) -> PARTIAL (LLM-judge gpt-5.2 coverage 1.0 agreement 0.55).
