# Method Extraction — peng2022

**Paper:** Spin-orbital-angular-momentum-coupled quantum gases (Peng et al., arXiv:2209.07051) — review/perspective on SOAM coupling in ultracold atoms
**Texture class:** orbital (spin–orbital-angular-momentum coupling in cold-atom quantum gases)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; large 148 KB review-length text)

> NOTE: This paper is a **review article** on spin-OAM-coupled (SOAM) ultracold quantum gases (Raman-coupled BECs carrying atomic OAM), NOT a condensed-matter orbital-Hall single-result paper like the other 7. Its "claims" are the surveyed phenomena; replication means reproducing the representative theory models it collects (Gross-Pitaevskii / single-particle Raman-coupling Hamiltonians), not one flagship calculation.

## 1. Central Claims (representative, review-level)

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Two Raman/LG (Laguerre-Gaussian) beams imprint OAM ±ℓħ and couple internal spin to atomic center-of-mass OAM → SOAM-coupling single-particle Hamiltonian with angular gauge field. | yes | **yes** (single-particle + GPE) |
| C2 | SOAM-coupled BEC ground states exhibit angular stripe / vortex / coreless (spin-texture) phases as a function of Raman coupling Ω, detuning δ, and interaction; phase diagram. | yes | **yes** (Gross-Pitaevskii mean-field) |
| C3 | Elementary excitations / roton-like spectra and collective modes of the SOAM-coupled gas (Bogoliubov). | yes | **yes** (Bogoliubov–de Gennes) |
| C4 | Experimental realizations (⁸⁷Rb, ²³Na BECs) confirm the angular-stripe/vortex phases. | yes (experimental) | **no** (cold-atom lab) |

(Because it is a review, C1-C3 are compiled from the surveyed literature rather than a single new result. Exact per-figure numbers vary by cited source.)

## 2. Method Class
**Analytic + model-Hamiltonian / mean-field (Gross-Pitaevskii equation, GPE) + Bogoliubov.** Single-particle SOAM Hamiltonian in cylindrical coordinates; interacting ground states via imaginary-time GPE; excitations via BdG. No DFT, no lattice DMFT — this is cold-atom BEC many-body mean-field.

## 3. Computational Recipe
- **Single-particle SOAM Hamiltonian:** H0 = p²/2M + V_trap(r) + Raman coupling Ω(r) e^{±i2ℓφ} that couples |↑⟩↔|↓⟩ while transferring 2ℓħ of OAM (LG-beam angular phase). Yields spin-dependent effective angular gauge potential / angular SOC.
- **Interacting ground state:** two-component Gross-Pitaevskii equations, i ħ ∂_t ψ_σ = [−ħ²∇²/2M + V + Raman + g_σσ'|ψ_σ'|²]ψ_σ; solve by **imaginary-time propagation** (split-step Fourier / finite difference on a 2D r-φ grid) to get angular-stripe / vortex / coreless ground states.
- **Excitations:** linearize → Bogoliubov–de Gennes eigenproblem for the collective/roton spectra.
- **Codes/packages:** none mandated. Standard tools: GPELab, XMDS, or custom split-step Fourier (numpy/CUDA). Parameters vary per surveyed system: coupling Ω, two-photon detuning δ, OAM charge ℓ, trap ω, s-wave scattering lengths a↑↑,a↓↓,a↑↓ (⁸⁷Rb / ²³Na values).
- **Key parameters:** atom species (⁸⁷Rb, ²³Na), trap frequency, Ω/E_recoil, δ, ℓ (typically 1-2), grid resolution in (r,φ).

## 4. Replication Feasibility
- **Tractable in hours (2D GPE) on CPU/GPU.** A representative SOAM-coupled BEC ground-state phase diagram (C1,C2) is a standard 2-component imaginary-time GPE on a 2D grid — well within reach. A parameter sweep over (Ω, δ) to reproduce the angular-stripe→vortex transition is embarrassingly parallel.
- BdG excitation spectra (C3) add a sparse eigenproblem per point — modest.
- **Because it's a review, pick ONE canonical model** (e.g. the Raman-LG SOAM-coupled ⁸⁷Rb BEC angular-stripe phase) as the replication target rather than "the paper" as a whole. Experimental confirmations (C4) infeasible.
- GPE benefits from GPU (split-step FFT) but a 2D grid is fine on CPU too.

## 5. Compute Recommendation
- **Host: uicgpu (GPU-accelerated split-step FFT GPE)** if doing fine 2D/3D sweeps, else **nuc13 (CPU)** for a single 2D phase diagram. Rough ask: 1 GPU (or 8-16 CPU cores), hours for a ground-state phase diagram + BdG spectrum at a few points.
- **Recommended host: nuc13 for a first pass; uicgpu if scaling to 3D or fine sweeps.**

## Notes / flags
- **FLAG (scope):** peng2022 is a **review/perspective**, not a single-computation research paper. It fits the "orbital texture" theme (atomic OAM ↔ spin) but its replication target must be *chosen* (one representative SOAM-BEC GPE model), not mechanically reproduced. Recommend the intake owner (Ollie) confirm whether a full replication is intended or whether a single representative model calc suffices.
- marker.md is clean and large (148 KB) — text fully readable; no Nougat pass needed. Equation-heavy sections survived pdftotext.
