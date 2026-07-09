# Failure analysis — Treeby & Cox (2010) k-Wave replication

**Overall verdict.** REPLICATED. There were no showstopper failures — the paper's numerical kernel reproduced cleanly. This document is the honest development-time record: bugs found, scope decisions, and residual known limits.

## 1. Development bugs found and fixed

### 1.1 First-timestep leapfrog centering bug (fixed)
**Symptom.** Initial C1 run showed a k-space L2 error floor at O(Δt) — around 10⁻³ to 10⁻⁵ — instead of the expected machine-precision O(10⁻¹⁵). Plain PSTD showed the same qualitative behavior, so it wasn't the κ correction.
**Root cause.** The very first velocity update was applied with the full Δt. But in a staggered leapfrog with u at half-integer times, the first velocity sample lives at t = +Δt/2, not t = +Δt. Given u(0) = 0, the first velocity update must integrate from 0 to Δt/2 — i.e. use Δt/2, not Δt. Using full Δt permanently miscenters every subsequent velocity sample by Δt/2 and injects an O(Δt) phase error that never decays.
**Fix.** Special-case the first velocity step to use Δt/2. All subsequent steps use full Δt. Verified: C1 error immediately dropped to 10⁻¹⁵. Same fix corrected C2 and C3.
**Lesson.** Even a "standard staggered leapfrog" as described in the paper's prose can hide a subtle initial-condition-centering trap. A d'Alembert smoke test on 1D catches this in a single script — always cross-check against a closed-form analytic before trusting a "spectral" error number.
**Log location.** `work/attempt.log`.

## 2. Scope decisions (deliberate non-tests, not failures)

The paper has 5 identifiable claims; 3 are numerical/testable (C1, C2, C3) and 2 are toolbox-level (C4 PAT reconstruction, C5 heterogeneous/PML). We declared C4 and C5 out-of-scope for this replication and were explicit about that in Section 2 of `REPORT.md`.

| Claim | Test status | Rationale |
|---|---|---|
| C1 (temporal dispersion) | Tested, replicated | Fundamental to the paper's core claim. |
| C2 (analytic comparison) | Tested, replicated | Directly falsifiable vs closed-form Hankel. |
| C3 (2 PPW spectral accuracy) | Tested, replicated | Directly measurable. |
| C4 (PAT reconstruction) | **Not tested** | Toolbox-engineering-level; built on the same kernel as C1-C3. Would require imaging metrics (PSNR / structural similarity) and phantom design — a separate project. |
| C5 (heterogeneous, PML) | **Not tested** | Real production regime of k-Wave. Too large for a kernel-replication scope, and the paper's κ derivation assumes a single reference c₀. Enumerated as `open_questions.json` OQ2. |

**This is a limit on the *scope* of the "REPLICATED" verdict, not a failure to replicate.** The kernel that C4/C5 are built on top of is exactly what we verified.

## 3. Residual honest caveats (from GENUINE CRITIQUE)

### 3.1 "Unconditional stability" is homogeneous-only
Our CFL sweep showed machine-precision error to CFL=5, but only in a homogeneous, dispersion-free, smooth-Gaussian setting. In heterogeneous media κ = sinc(c₀·Δt·|k|/2) uses a single reference c₀ and the exactness is lost. The paper is explicit about this, but the phrase "arbitrarily large time steps" is easy to misread. Flagged in REPORT.tex GENUINE CRITIQUE §2.

### 3.2 Disk PSA "error" is caustic sampling, not scheme error
Our C2b L2 self-convergence numbers (0.20 → 0.13 → 0.08) look bad next to C2a's 10⁻⁵. This is not a scheme failure — it is the well-known 2D-caustic singularity at r = c₀·t + R that no finite scheme can resolve without a smoothing kernel. The physical wavefront position on the finest grid is accurate to sub-Δx (miss = 0.033 mm on a 0.033-mm grid). Flagged in REPORT.tex GENUINE CRITIQUE §3.

### 3.3 Judge audit does not fully close the loop
The Argo GPT-4o judge cross-checks coverage and honesty but does not (and cannot) numerically re-derive our error tables. It is a writeup-consistency audit, not a numerical replication of our replication. Recorded in `evidence/judge_response.txt`.

## 4. What could still fail (open questions, enumerated in open_questions.json)

These are honest gaps between "kernel replicates" and "toolbox works as sold":
- **OQ1**: fractional power-law absorption stability with κ.
- **OQ2**: heterogeneous / sharp-interface Gibbs behavior.
- **OQ3**: GPU / multi-node scaling limits (global FFT per step).
- **OQ4**: elastic-wave extension (two intrinsic wave speeds vs single κ).
- **OQ5**: comparison vs modern high-order FDTD and DG methods for PAT accuracy.

Any of these could produce a genuine failure at scale that a homogeneous kernel test can't detect.

## 5. Confidence assessment

- **Kernel-level correctness**: high. Three independent tests against exact / self-convergent references all at machine precision or physically-explained residuals.
- **Independence**: high. Kernel written from paper equations only, in Python from scratch, no k-Wave code consulted.
- **Coverage vs paper's advertised production regime**: partial. Homogeneous/lossless only.
- **Overall verdict**: REPLICATED at the level the paper's numerical claims live; scope of the verdict is clearly documented.
