# PROGRESS — Kernel-based Active Subspaces (Romor et al. 2020)

**Target paper:** Romor, Tezzele, Lario, Rozza (2020/2022),
"Kernel-based active subspaces with application to computational fluid dynamics
parametric problems using the discontinuous Galerkin method."
arXiv:2008.12083 · DOI: 10.1115/1.4054756

**Workspace:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/kernel-active-subspaces/`
**Progress JSON:** `~/.openclaw/workspace/memory/subagent-progress/kernel-active-subspaces.json`

## Plan

1. ✅ Create workspace + PROGRESS skeleton.
2. ✅ Openness confirmed: ATHENA = MIT (LICENSE.rst inspected), all Python
   deps permissive (BSD/MIT), no proprietary code or data.
3. ✅ Installed ATHENA in a py3.11 venv on CherryRd (uv + pip;
   `setuptools<80` pin needed because GPyOpt still imports `pkg_resources`).
4. ✅ Test problems chosen:
   - **Exp 1:** Radial cosine ridge `cos(||x||^2)` (canonical KAS sanity test
     from paper §4 / ATHENA Tutorial 6).
   - **Exp 2:** Parametric Poisson on `(0,1)^2` with 5-D KL log-diffusion
     and mean-u QoI (substitute for HopeFOAM DG; disclosed in REPORT.md §3).
   - **Exp 3:** Same Poisson but nonlinear QoI
     `log(∫|∇u|²) + 0.5*(s_1² + s_3²)` — stresses KAS.
5. ✅ Linear AS vs Kernel AS implemented via ATHENA's
   `ActiveSubspaces` and `KernelActiveSubspaces` with RFF feature map
   (`distr="laplace"`, `n_features=400-1000`).
6. ✅ Eigenvalue and sufficient-summary plots generated; held-out test
   RMSE computed at reduced dims r=1,2,3 for the PDE cases.
7. ✅ REPORT.md + README.md written with claim-by-claim table (5/6 strongly
   agree, 1/6 nuanced), friction tags (incl. ATHENA CV bug), and limitations.

## Status

- 2026-05-28 11:56 CDT — workspace created, PROGRESS skeleton written.
- 2026-05-28 12:01 CDT — verified ATHENA = MIT, installed in py3.11 venv.
- 2026-05-28 12:05 CDT — ran exp 1 first pass; found ATHENA CV bug; rewrote with
  explicit held-out tuning.
- 2026-05-28 12:15 CDT — exp 1 PASSES (linear-AS 0.697 vs kernel-AS 0.320, 2.18×).
- 2026-05-28 12:16 CDT — exp 2 (parametric Poisson, mean-u QoI) honest negative
  result for KAS — response is nearly affine so linear AS already optimal.
- 2026-05-28 12:17 CDT — exp 3 (nonlinear QoI on Poisson) KAS edges linear AS at
  r=1 (0.137 vs 0.159), AS catches up at r=2,3.
- 2026-05-28 12:22 CDT — REPORT.md + README.md written. COMPLETE.
