# Failure Analysis — Figueiras 2018 Split-Step BPM Replication

Failures, near-misses, and honest limits from this replication. Written to be a lookup for future-you, not a triumphal narrative. Grounded in what REPORT.md actually reports.

---

## F1. `test3c` stationary-Schrödinger ODE integrator was unstable for odd integer s (DISCARDED)

**Symptom.** Spurious reflection coefficient R ≈ 0.44 for odd integer s in the auxiliary stationary-Schrödinger ODE scattering integrator, contradicting the true reflectionless behavior.

**Root cause.** The reflectionless integer-s Pöschl-Teller case requires exact cancellation of an exponentially growing mode in the two linearly-independent asymptotic solutions of the stationary equation. A generic BVP/IVP ODE shooter cannot maintain that cancellation to enough digits — the growing mode leaks in and produces a spurious R.

**Fix.** Discarded `test3c` entirely. Replaced with:
- **Test 3d** (closed form): derived `R(k,s) = sin²(πs)/(sinh²(πk) + sin²(πs))` using √(1+4s(s+1)) = 2s+1, proving R=0 iff s ∈ ℤ (numerical ~1e-32 for integer s).
- **Test 3** (split-step wavepacket): direct time-domain scattering measurement via Fourier partition, giving R ≈ 2.6e-8 for s=10 (roundoff-limited, not physics-limited).

**Impact on verdict.** None — the paper's reflectionless claim (C2) is confirmed by two independent methods. The failed integrator only affected an auxiliary sanity path.

**Lesson.** For reflectionless / bound-state-embedded-in-continuum problems, don't rely on a generic ODE shooter — either use a time-domain wavepacket + Fourier partition, or derive the closed-form scattering coefficient. This is a family-of-problems lesson, not a paper-specific one.

**Kept in the record?** Yes — REPORT.md §5 explicitly documents this negative rather than hiding it.

---

## F2. Sign / FFT-convention trap in the kinetic propagator (CAUGHT EARLY)

**Symptom.** Naïvely applying `exp(i·dt·(2πk)²/2)` (paper literal) with a `numpy.fft.fftfreq` grid can give a phase with the wrong sign vs the intended Schrödinger evolution.

**Root cause.** The paper writes the kinetic factor under a "cycles-per-length" FFT convention where the Laplacian eigenvalue is −(2πk)². With an angular-wavenumber convention `k = 2π · fftfreq(N, dx)`, the correct factor is `exp(-i·dt·k²/2)`. Two conventions collide silently.

**Fix.** Pinned by requiring the free case (V=0) to reproduce the exact analytic Schrödinger propagator of a minimum-uncertainty Gaussian. Once the pin passed to ~1e-14 in L2, the convention was correct.

**Impact.** None on the final result — caught before any physics test. But this is the class of failure that would silently corrupt a downstream user of the paper who copied the formula literal into an angular-k FFT code.

**Lesson.** Analytic-first validation with a nonzero group velocity + measurable spreading is what distinguishes right-sign from wrong-sign; static tests (norm) are insensitive to it. Always test on a case where a wrong sign would visibly manifest.

---

## F3. First-order accuracy is only tested by Cauchy self-convergence, not a manufactured solution (LIMITATION)

**Symptom.** None observed — observed order 1.0005 / 1.0002 / 1.0001 matches paper claim.

**Limit.** The rate comes from self-convergence on the nonlinear soliton, not from comparison to a manufactured or higher-order reference. If both the coarse and fine grids shared a systematic error unrelated to dt (e.g. from spatial truncation), Cauchy self-convergence could miss it.

**Mitigation used.** The nonlinear soliton has non-commuting kinetic/potential operators, so genuine Lie splitting error dominates and is what self-convergence measures. Spatial error is separately made small by using a large periodic box relative to the soliton support.

**Deferred.** A Strang (second-order) reference or manufactured-solution error prefactor was not measured. Open in open_questions.json Q2.

---

## F4. Reflection metric is Fourier-partition, not asymptotic S-matrix (LIMITATION)

**Symptom.** None — the metric matches the closed-form R quantitatively for broad Gaussian packets.

**Limit.** The reflection is measured as `∫|ψ̂(k<0)|² / ∫|ψ̂|²` after the packet clears the well. This is a good proxy but is not, strictly, the asymptotic scattering coefficient — a fully rigorous measurement would use position-space windows far from the potential and project onto outgoing plane-wave states.

**Impact on verdict.** None; the closed form (Test 3d) is what carries the reflectionless claim rigorously, and the wavepacket agrees to ~1e-8.

**Deferred.** Transmission-phase (δ(k,s)) extraction not attempted. Open in open_questions.json Q3.

---

## F5. 2D headline demonstrations were not exercised at paper-figure fidelity (SCOPE GAP)

**Symptom.** Not a numerical failure; a coverage gap.

**Detail.** The `BPM2D` class was implemented in `bpm.py`, but the paper's 2D demonstrations (vortex/Gaussian beams, filamentation, GP vortex precession) were not each reduced to a per-figure quantitative comparison. The verdict REPLICATED is scoped to C1–C4 as tabulated.

**Impact on verdict.** REPLICATED is honest for C1–C4 but does not certify every figure in the paper. Called out in REPORT.tex Genuine Critique.

**Deferred.** Open in open_questions.json Q1.

---

## F6. Judge diversity is limited (METHODOLOGY LIMIT)

**Symptom.** Three-judge unanimous REPLICATED across argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1.

**Limit.** All three judges are Argo endpoints and share frontier-model training-data lineage. Unanimous agreement across related models is weaker evidence than disagreement-resolved agreement across truly independent judge families. This is project-wide.

**Impact on verdict.** Low for this paper — the underlying numerical claims are exact-analytic-validated (1e-14 free propagator, closed-form R=0), so judges are corroboration rather than the primary evidence.

**Deferred.** Judge-diversity improvements are project-scope, not paper-scope.

---

## F7. No performance / usability benchmark against the authors' shipped library (SCOPE GAP)

**Symptom.** Not measured.

**Limit.** The paper positions the library as an open-source educational tool. Our from-scratch reimplementation does not benchmark runtime, memory, or API ergonomics against the shipped library. Our claim is scoped to numerical correctness, not to whether the library succeeds as a pedagogical artifact.

**Impact on verdict.** None — verdict is about the paper's numerical claims, not its pedagogical claims.

---

## Summary
Two real failures during the run: F1 (discarded `test3c` — documented and superseded by two independent working paths) and F2 (sign convention — caught early via analytic-first design, before any physics test). Everything else is a scope/methodology limit honestly recorded, not a bug. Final verdict REPLICATED is scoped to C1–C4 and rests primarily on exact-analytic agreement (free propagator ~1e-14, closed-form reflectionless R=0), with LLM judges as corroborating evidence.
