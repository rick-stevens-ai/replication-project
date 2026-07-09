# Brief — OSTI 2552927 (NeuroSEM)

**Paper:** Shukla et al., *NeuroSEM: A hybrid framework for simulating multiphysics
problems by coupling PINNs and spectral elements*, CMAME **433**, 117498 (2025;
OSTI 2552927; 2024 preprint on OSTI). Authors from Brown / Imperial / PNNL, PI
G.E. Karniadakis.

**Idea.** Couple a physics-informed neural network (PINN) surrogate for one field
(e.g. temperature `T` or velocity `u`) into the high-order spectral element solver
Nektar++, so that data-rich regions are handled by PINNs and the rest of the
Rayleigh–Bénard / Navier–Stokes domain is solved by SEM. Three coupling modes
(A: PINN→T + SEM→u; B: PINN→u + SEM→T; C: PINN provides BCs for a subdomain
cutout). Applied to (i) cavity RBC at Ra=1e4/1e5/1e6, (ii) unsteady flow past a
cylinder, (iii) real PIV horseshoe-vortex data.

**Why this replication.** The authors released their PINN code, trained
checkpoints (JAX/Equinox `.eqx` + PyTorch traced `.pt`), SEM reference solutions
on ~300k quadrature points, and real PIV data on GitHub
(`ZongrenZou/NeuroSEM`, commit `b5f027a`, 111 MB). That lets an independent
party recompute the PINN-surrogate L2 errors against the shipped SEM reference
without re-running Nektar++ — the closest artifact-level test of the reported
Table 1/2 numbers achievable without a full high-order CFD stack.
