# Non-climate PDE batch launch — 2026-05-28 09:41 CDT

Rick approved: "lets do it" after openness audit.

## Operational rules
- Skip climate papers.
- Use only open data and open-source programs/dependencies.
- If a target lacks same-paper open code, proceed only as an independent open-source reimplementation with fully specified analytic/synthetic data, and mark that clearly.
- Do not contact authors.
- Do not use paid model endpoints for subagents; use free Argo/ALCF/CELS only.
- Write all outputs under `~/Dropbox/REPLICATE-PROJECT/PDE-replications/<slug>/`.
- Progress files under `~/.openclaw/workspace/memory/subagent-progress/<slug>.json`.

## Approved adjusted targets
1. FLUPS unbounded Poisson solvers — PASS open source.
2. APBS Poisson–Boltzmann — PASS open source.
3. Kernel active subspaces CFD/DG — PASS open stack.
4. ToyotaCRDL VQAPoisson — PASS open source.
5. AMR vs Multiresolution Euler via Carmen/AMROC — PASS with license caution.
6. LLNL MARL-AMR — PASS; replaces Foucart Deep-RL-AMR as strict-open RL-AMR target.
7. Optimized Schwarz Helmholtz — independent open-source reimplementation.
8. DG/Hermite Vlasov–Poisson — independent open-source reimplementation.
9. Modified Poisson–Nernst–Planck — independent open-source reimplementation.
10. Replacement slot: demote Gmunu until repo found; candidate replacement to be chosen after first wave if needed.

## First-wave launch plan
Start five in parallel:
- flups-poisson
- apbs-pb
- marl-amr
- optimized-schwarz-helmholtz
- vqapoisson

Second wave after first status:
- kernel-active-subspaces
- amr-vs-mr-euler
- vlasov-poisson-dg-hermite
- modified-pnp
- replacement slot / Gmunu repo hunt
