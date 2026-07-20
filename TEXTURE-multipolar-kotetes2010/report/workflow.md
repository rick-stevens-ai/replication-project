# Workflow — kotetes2010 replication

## Goal
From-scratch replication of the self-consistent mean-field theory of the chiral
hidden order in URu2Si2 (Kotetes, Aperis & Varelogiannis, Phil. Mag. 2010).

## Steps executed

1. **Read recipe + kernel + paper.**
   - `report/evidence/replication_recipe.json` → method=mean-field, targets
     (T_HO=17.5 K, Delta2=1.55 meV, Bc1=33.5 T, Bc2=41 T).
   - `ollie_multipolar_stevens_landau_kernel.py` → reusable Landau/mean-field idiom.
   - `work/textures-multipolar-kotetes2010.txt` → extracted the full physics from
     Appendices A–D: order parameter, dispersion, Berry curvature (B1), orbital
     moment (B2), field-split bands (B3), free energy (C1), gap equations (C2),
     Landau reduction (D). All material params (t, mu, muB, a, V', V'') read from
     Eq. C1 text.

2. **Built from-scratch solver** `work/kotetes2010_mft.py`:
   - `bands_and_free_energy(D1,D2,T,B)` — assembles eps(k), the two d-wave
     harmonics, E(k), Berry-curvature skyrmion density → orbital moment m_z, the
     four field-split bands E^B, and the free-energy functional F/v (Eq. C1).
   - `solve_point(T,B)` — minimizes F over (Delta1,Delta2) with multi-restart
     Nelder-Mead (self-consistency equivalent to C2).
   - `main()` — zero-field T-sweep, low-T B-sweep, phase boundary T_HO(B).
   - `landau_module()` — Appendix D reduction: field-induced Delta1 and
     field-enhanced To(B)=To+(g^2/a1)B^2.
   - Provenance: imports the shared kernel and credits it in the header.

3. **SAVE-EARLY.** First coarse solve written to `work/kotetes2010_result.json`
   after the initial run (before field sweep / Landau were finalized).

4. **Debugging.**
   - Fixed `exp` overflow in the log(1+exp) term via clipped softplus.
   - Caught an unphysical orbital prefactor (ORB~2.4e18 from a unit-conversion
     slip) that blew Delta2 up to 1e20 in the field sweep; reset ORB=0.010 meV/T
     (topology-scale, per the paper's statement that magnitude is not crucial).

5. **Compared & scored** (comparison + self_score blocks appended to result JSON):
   zero-field within 14–21%, field-induced chirality + Tc-enhancement matched in
   structure; metamagnetism/transport out of scope. Verdict PARTIAL.

6. **Packaged 8 artifacts** (see artifacts_summary.md). Copied result JSON + solver
   + kernel into `report/evidence/`.

## Runner
`/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).
Full run: ~8 s coarse (24x24 grid). `--fine` flag → 40x40.

## Reproduce
```
cd work && /home/stevens/comfyui-env/bin/python kotetes2010_mft.py
```
