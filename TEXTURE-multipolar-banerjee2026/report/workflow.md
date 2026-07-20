# Workflow — Replication of banerjee2026 (OIFE / Floquet multipolar)

## Objective
Reproduce, from scratch, the headline claim: circularly polarized light (CPL)
induces an effective static field `h_m` that couples linearly to the magnetic
octupole `T_xyz` (octupolar inverse Faraday effect, OIFE), via a Floquet
Schrieffer-Wolff / van Vleck high-frequency expansion of a driven
Hubbard-Kanamori model on edge-sharing octahedra (4d^2/5d^2 Mott insulator).

## Steps executed
1. **Read** paper text (`work/textures-multipolar-banerjee2026.txt`) and recipe
   (`report/evidence/replication_recipe.json`). Located the effective
   Hamiltonian Eq.(4), the pseudospin normalization Eq.(2), the analytic Floquet
   coupling formulas Eqs.(6a-6f), and representative parameters (tpd=1.5, t2=0.25,
   U-tilde=3.0, Delta_c=5.0 eV, Omega~100 THz~0.414 eV, cutoff p=7).
2. **Build pseudospin** (`replicate_banerjee2026.py::pseudospin_check`): projected
   normalized Stevens operators (O22/4sqrt3, Txyz/2sqrt3, O20/12) onto the Eg
   doublet {(|Jz=2>+|Jz=-2>)/sqrt2, |Jz=0>} and verified the full SU(2) algebra
   [s_a,s_b]=i eps s_c. Reused `ollie_multipolar_stevens_landau_kernel.py` for the
   angular-momentum + Stevens operator machinery.
3. **Evaluate Floquet couplings**: implemented Eqs.(6a-6f) with scipy Bessel
   functions `jv`, Floquet-index sums constrained to n+l+m=0, cutoff p=7.
   Computed J_eff, Gamma^(3), h_m over a zeta sweep [0,4].
4. **van Vleck demo**: constructed CPL drive V(t) on the doublet with circular
   components V_{+/-1}, computed [V_-1,V_+1]/Omega, and showed the induced static
   correction lies in the sigma_y (octupole) channel.
5. **SAVE-EARLY**: wrote `work/banerjee2026_result.json` after pseudospin + one
   coarse coupling point, then overwrote with the full sweep + claim checks.
6. **Claim checks**: (i) h_m proportional to Gamma^(3) [ratio 9/8]; (ii)
   anisotropy Gamma^(3)/J_eff grows with zeta; (iii) h_m ~ zeta^2 at small drive
   (helicity origin); (iv) induced field is octupolar (sigma_y).
7. **Package**: extraction/ (marker.md, nougat.mmd via pdftotext interim),
   report/ (REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md,
   failure_analysis.md), evidence/ (result JSON + code + kernel).

## Runner
`/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0). Total
runtime < 1 s; grids intentionally small (41-point zeta sweep, p=7 Floquet
sums). Well under the 5-min target.

## Reproduce
```
cd /home/stevens/textures-100/corpus/textures-multipolar-banerjee2026/work
/home/stevens/comfyui-env/bin/python replicate_banerjee2026.py
```
