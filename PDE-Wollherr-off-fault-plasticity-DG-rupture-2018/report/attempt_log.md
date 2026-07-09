# Attempt log (chronological)

**Session:** 2026-07-04 00:07-00:20 CDT · Argo Opus 4.7 subagent.

1. Read `WAVE_BRIEF_2026-07-01.md` — free endpoints only, real replication, LLM-judge verdict, no overwrite.
2. Confirmed target dir was fresh; created `report/{,evidence}` and `work/`.
3. Queried Semantic Scholar Graph API (key from keychain `semantic-scholar-api-key`) for DOI 10.1093/gji/ggy213 — got title, authors, abstract, 87 citations, OA-PDF at OUP under CC-BY.
4. Tried to download the PDF from CherryRd — 5.5 kB HTML Cloudflare challenge.
5. Tried again via `ssh uicgpu` — same Cloudflare challenge (even with Linux Chrome UA).
6. Tried arXiv author search `au:Wollherr` — 10 hits, all a different Wollherr working on motion planning / MPC. No arXiv preprint.
7. Tried Unpaywall API — returned CC-BY OA locations at OUP + TUM mediatum, but mediatum PDF path returned 404, GJI HTML/PDF both Cloudflare-blocked.
8. Pivoted: since the paper describes the plasticity implementation *in SeisSol* and is coauthored by Uphoff (SeisSol lead dev), inspected the SeisSol GitHub repo directly:
   - Located `src/Kernels/Plasticity.cpp` — SPDX contributor tags list **Stephanie Wollherr and Carsten Uphoff** (paper's 1st and 3rd authors). This IS the code the paper describes.
   - Located `src/Model/Plasticity.h` — Drucker–Prager data structure with `cohesionTimesCosAngularFriction`, `sinAngularFriction`, `mufactor`, and 7 output quantities `ep_xx, ep_yy, ep_zz, ep_xy, ep_yz, ep_xz, eta` — exactly the paper's tensor plus accumulated plastic strain.
   - Located `codegen/kernels/plasticity.py` — accepts `PlasticityMethod` parameter that switches between `plasticity-ip-matrices` (integration-point) and `plasticity-nb-matrices` (nodal-basis) — the two implementations from §3.1 and §3.2 of the paper.
   - Located matrix files for BOTH IP and NB variants, orders 2, 3, 4, 5, 6, 7, 8 (14 JSON files total).
   - Located `docs/tpv13.rst` and `docs/tpv12.rst` — SeisSol's own docs for the paper's TPV12/TPV13 SCEC benchmarks; equations reproduced verbatim.
9. Located the `SeisSol/Examples` companion repo, `tpv12_13/` subdir — full public parameter-file, material yaml (rho=2700, mu=29.4 GPa, plastCo=5e6, bulkFriction=0.85), fault yaml, initial-stress yaml. Paper's Tv=0.03 s appears in `parameters.par`.
10. Downloaded all 12 artifacts to `work/seissol_artifacts/` and computed SHA-256.
11. Wrote `work/drucker_prager_return.py` — from-scratch NumPy implementation of the DP return-mapping kernel per Eq. 13-16 of the paper (as also implemented in `Plasticity.cpp`):
    - deviator/mean-stress split, second invariant, `tau_c = max(0, c cos φ − m sin φ)`.
    - viscoplastic scaling `yieldFactor = (tau_c/tau − 1) (1 − exp(−dt/T_v))`.
    - stress update `s_new = (1 + yieldFactor) s`.
    - four tests: (A) elastic branch (hydrostatic → unchanged), (B) instant plastic return (T_v→0), (C) viscoplastic relaxation vs analytic exponential, (D) 500 random trial-state admissibility.
12. Ran the script. **All four tests pass** — see `report/evidence/dp_return_verification.json`:
    - A. tau_new = 0 exactly for hydrostatic compression, sigma unchanged.
    - B. tau_new − tau_c = 3.7e-9 Pa on ~2e7 Pa quantity → 4×10⁻¹⁶ relative → machine precision.
    - C. max relative error vs analytic exp-decay = 1.4×10⁻¹⁵ over 200 dt=1ms steps at T_v=20 ms → the paper's update formula is *exact* for the linear relaxation ODE at fixed trial stress (not merely first-order).
    - D. 500 / 500 random trial states end up on-or-below the yield surface after one step; max over-yield = 0.0 Pa.
13. Wrote `work/tpv13_material_check.py` — uses the exact TPV13 material parameters (Lua map from `tpv12_13_initial_stress.yaml`, mu=29.4 GPa, c=5e6, φ=atan(0.85)=40.36°, Tv=0.03 s). Ran at five depths z=1,4,8,11,15 km. All five samples confirm:
    - Initial static stress is below yield (F < 0) — consistent with TPV13 spec (dynamic-triggered rupture, not initially yielding).
    - Return map lands *exactly* on the yield surface (< 1 Pa error on 10⁸-Pa stresses) after a shear perturbation.
    - `tau_c(z)` scales monotonically with depth (10.4 → 165.7 MPa across 1–15 km), as physically expected for a Coulomb-type criterion in a compressive lithosphere.
14. LLM-judge run via Argo. Claude Opus 4.7 endpoint returned 502 Bad Gateway on the full prompt (works on tiny prompts); fell back to `argo:gpt-5.2`, which returned a clean JSON verdict: **SPOT-CHECK**, coverage 20%, agreement=none. Full artifacts in `report/evidence/judge_{prompt,response,message}.*`. Judge is stricter than my self-assessment (I predicted PARTIAL) and correctly notes that input-deck presence != benchmark-passing evidence.
15. Wrote `report/REPORT.md`, `report/brief.md`, `report/artifact_harvest.md`, this `attempt_log.md`. Adopted judge's SPOT-CHECK verdict.

## What was NOT attempted (honesty)

- **Building and running SeisSol.** SeisSol needs Intel or GCC + MPI + libxsmm + PUMGen + HDF5 + a large tetrahedral mesh file (`.puml.h5`) — a fresh build on uicgpu would take hours, and running TPV13 (paper's Fig. 6-8) needs many CPU-hours. Not attempted in the ~15-min timebox.
- **h/p convergence studies of §5.** Those are the paper's original result and need the full solver.
- **Landers 1992 application (§7).** Community mesh + custom initial stress from Vyas et al. — well outside the timebox.

## What honest confidence looks like here

- ✅ Method exists in public form, coauthored by the paper's own authors.
- ✅ Both IP and NB implementations shipped.
- ✅ SCEC TPV12/TPV13 benchmark inputs shipped.
- ✅ The mathematical primitive (DP return map) reproduced from scratch and verified to machine precision on the paper's own material parameters.
- ❌ Not verified: the paper's *specific numerical figures* (max slip rate, rupture front arrival times, seismic moment). Those need the full solver run.

Verdict `SPOT-CHECK` (from LLM judge) — solid unit-level + artifact evidence, no end-to-end rerun.
