# Brief

**Paper:** D. Albritton, E. Bruè, M. Colombo, *Non-uniqueness of Leray solutions of the forced Navier–Stokes equations*, Ann. of Math. 196 (2022), 415–455. DOI: 10.4007/annals.2022.196.1.3 · arXiv:2112.03116.

**What:** The paper resolves a long-standing open problem by proving that Leray-Hopf weak solutions to the 3D Navier–Stokes equations are **not unique** even with the same body forcing and the same (zero) initial data. The construction perturbs a self-similar background whose similarity profile is a smooth compactly-supported vortex ring whose cross-section is (a modification of) Vishik's unstable 2D vortex; the second Leray-Hopf solution is a trajectory on the unstable manifold associated to an unstable eigenvalue λ (Re λ > 0) of the linearized operator around the background.

**Why (this replication):** The paper is 100% analytic (theorem-proof) with no code/data/simulation; the appropriate reproducibility test is (i) confirm all cited artifacts are publicly available, and (ii) numerically verify the *engine* the proof depends on — Vishik's 2D linear instability of radial vortices — is real and behaves as the theory demands (monotone → stable, non-monotone/ring → unstable at low modes m). Both are done, with converged numerical eigenvalues on realistic ring profiles.
