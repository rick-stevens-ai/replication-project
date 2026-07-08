# Non-climate PDE batch 2 launch — 2026-05-28 11:56 CDT

Rick: "wow.. lets pick some more papers to replicate"

First wave completed 5/5:
- FLUPS
- APBS
- Optimized Schwarz Helmholtz
- VQAPoisson
- LLNL MARL-AMR

## Batch 2 targets

1. `kernel-active-subspaces` — Romor/Tezzele/Rozza kernel active subspaces for CFD/DG; open ATHENA (MIT), HopeFOAM/OpenFOAM, open/generated datasets.
2. `amr-vs-mr-euler` — Deiterding/Domingues/Gomes/Schneider AMR-vs-MR compressible Euler; Carmen repo open access, AMROC open access; license caution.
3. `vlasov-poisson-dg-hermite` — Bessemoulin-Chatard/Filbet DG/Hermite Vlasov–Poisson; open paper, independent open implementation.
4. `modified-pnp` — Ma/Xu/Zhang modified Poisson–Nernst–Planck with hard-sphere/Coulomb correlations; open paper, independent implementation.
5. `lowrank-vlasov-poisson` — Einkemmer/Lubich low-rank projector-splitting Vlasov–Poisson; open paper, independent implementation. Replacement for Gmunu (repo not found).

## Rules
- Skip climate.
- Open data/open source only.
- If no author code, independent implementation is fine but must be stated.
- Free LLM endpoints only (`argo/argo:claude-opus-4.7`).
- Early checkpoints: PROGRESS.md + progress JSON within 10 minutes.
- Output dirs under `~/Dropbox/REPLICATE-PROJECT/PDE-replications/<slug>/`.
