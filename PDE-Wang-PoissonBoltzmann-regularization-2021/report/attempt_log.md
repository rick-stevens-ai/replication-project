# Attempt Log — Wang/Alexov/Zhao 2021 PB regularization replication

Host: CherryRd (macOS). Replicator: subagent, 2026-07-01.

## 1. Setup
- Read WAVE_BRIEF_2026-07-01.md. Skimmed sibling PDE replications; closest exemplar is
  `PDE-replications/apbs-pb` (also Poisson-Boltzmann; APBS software paper).
- Created target dir `PDE-Wang-PoissonBoltzmann-regularization-2021/{report/evidence,work}`.

## 2. Paper acquisition
- Resolved DOI 10.3934/mbe.2021072 -> aimspress.com landing page (HTTP 200).
- NOTE: task's title string ("finite element/difference method") differs from the actual
  published title ("...with a smooth solute-solvent boundary"). Same DOI, same paper —
  the method is finite *difference* (central FD), not FEM. Proceeded with the real paper.
- Downloaded OA PDF: /aimspress-data/mbe/2021/2/PDF/mbe-18-02-072.pdf (22.9 MB, 36 pp).
- pdftotext -layout -> paper.txt (1833 lines). Extracted all governing equations and
  Tables 1–7 verbatim (large figures made the file too big for the native PDF tool's
  10 MB limit, so used text extraction + targeted reads).

## 3. Method extraction (the exact PDE we must solve)
- Diffuse-interface dielectric: ε(r) = S(r)ε_i + (1−S(r))ε_e, ε_i=1, ε_e=80.   (Eq 2.1)
- Nonlinear PB (Eq 2.2); paper VALIDATES numerically with the LINEARIZED PB (Eq 2.15).
- κ² = 8.486902807 * I  Å⁻²  (I in molar; I=0.15 M default).
- Dual decomposition: u = u_C + u_RF ; ε = ε_i + ε̂.
- Coulomb/Green: u_C = G(r) = (e_c²/k_BT) Σ_j q_j / (ε_i |r−r_j|)   (Eq 2.6).
- Regularized LPB for reaction field (THE equation we discretize):
    −∇·(ε∇u_RF) + (1−S)κ² u_RF = ∇ε·∇G − (1−S)κ² G,  in Ω     (Eq 2.16)
    u_RF = u_b − G  on ∂Ω,  with u_b the Debye-Hückel Dirichlet BC (Eq 2.4).
- Discretization: 2nd-order central FD, Eq (2.17)-(2.19); ∇ε by central diff of nodal ε.
  Sparse N³×N³ system solved by biconjugate-gradient (we use scipy BiCGSTAB).
- Free energy (regularization): E = ½ k_BT Σ_j q_j u_RF(r_j), unit kcal/mol (Eq 2.22),
  u_RF at charge centers by linear interpolation.
- Trilinear comparison: distribute q_j to 8 cell corners as fractional charges Q; solve
  Eq(2.15) directly for u_TL and Poisson (κ=0) for u0; E = ½k_BT Σ q_j (u_TL−u0)(r_j).

## 4. Test case (analytic, primary target = Table 1)
- One atom at origin, VdW radius 2. Analytic tanh-like surface (Eq 4.1): r_i=2, r_e=5,
  k=6, s_i=1, s_e=0. Domain: cube symmetric about origin. N=11,21,31,41,51,101,201,401
  with h chosen so charge center is a grid node (paper: h=2,1,0.6667,0.5,0.4,0.2,0.1,0.05).
- One-charge: q1=1 at (0,0,0). Two-charge: q1=q2=1 at (±1.475,0,0).
- Targets: Table 1 Regularization col -> limit ≈ −65.66 (1q) and ≈ −303.8 (2q) kcal/mol;
  trilinear col non-convergent/over-estimating.
- Secondary analytic check: σ→0 SAS Born energy for r=3.5 sphere = −46.8447 kcal/mol.

## 5. Implementation & runs
- work/pb_reg.py : from-scratch NumPy/SciPy solver (grid, ε, S, G, ∇ε·∇G source,
  Dirichlet BC, sparse assembly, BiCGSTAB), both regularization and trilinear.
- work/born_analytic.py : closed-form Born/Kirkwood ion energy for the σ→0 check.
- Ran N=11..201 locally; N=401 (6.4e7 unknowns) offloaded to uicgpu (8×A100 host, but
  solve is CPU sparse) — see attempt notes below for actual runtime/where run.
- Results written to report/evidence/*.json and compared to paper tables in REPORT.md.

## 6. Two critical numerical lessons (root-caused during the run)
- FIRST attempt used the conservative divergence form + numerical grad(eps): gave
  ~10-13% too-negative energies (N=41 -73 vs paper -64.7) and a non-flat convergence.
- FIX 1: switch to the paper's EXACT non-divergence expanded discretization (Eq 2.17):
  -eps*Lap(u) - grad(eps).grad(u). Immediately closed most of the gap.
- FIX 2: use ANALYTIC grad(eps) = (eps_i-eps_e) dS/dr * rhat for the analytic tanh surface
  (paper states all source terms incl. grad(eps) are analytic there). N=41 -> -66.57,
  N=51 -> -66.48, flat convergence matching the paper's pattern.
- Verified units end-to-end: Coulomb constant 332.06371 reproduces the paper's analytic
  Born SAS energy -46.8447 EXACTLY (born_analytic.py).
- Compute: N<=51 local (CherryRd, seconds). N=101/201 on uicgpu (255-core), plain BiCGSTAB
  NO_ILU (spilu on 1e6+ nodes was the real bottleneck -> disabled it). N=101 ~32s,
  N=201 ~440-460s each. spilu(ILU) removed for large N; env NO_ILU=1.

## 7. Findings (final; full numbers in REPORT.md)
- One-charge reg energies: N=201 -65.88 vs paper -65.62 (0.40%). Converges to paper limit.
- Two-charge: N=101 -305.36 vs paper -305.15 (0.07%); N=201 -303.33 vs -304.12 (0.26%).
- Trilinear reproduced as strongly grid-dependent / non-convergent (paper's motivation);
  absolute trilinear magnitudes differ (source bookkeeping under-specified) -> directional.
- Born analytic limit -46.8447 confirmed to 4 decimals.
- Protein/compound/salt tables (4,5,6,7): OUT OF REACH (charges/PQR/rMIB refs not distributed).
- LLM-judge (Argo gpt-5.2, free, x2 passes, high confidence): PARTIAL.
- FINAL VERDICT: PARTIAL (solid) -- core analytic claim independently reproduced; broader
  application tables not reproducible from the publication alone.
