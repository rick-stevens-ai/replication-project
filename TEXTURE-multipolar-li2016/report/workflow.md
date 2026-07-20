# Workflow — li2016 replication

## Goal
Independently reproduce the headline mean-field claim of Li, Wang & Chen (2016):
at (Jx,Jy,Jz)=(-1,-0.2,-0.5), theta=pi/3 the DO-doublet triangular-lattice model
has a **ferro-octupolar (FO)** ground state with transition To=1.5|Jx| and a
**non-divergent** chi_zz.

## Steps executed
1. **Read** paper text (`work/textures-multipolar-li2016.txt`) + prepped recipe
   (`report/evidence/replication_recipe.json`). Identified: reduced Hamiltonian
   (Eq. 4), Tx=octupole / Ty,Tz=dipole, octupolar-wave (Eq. 5), NN vectors, z=6.
2. **Built** from-scratch runner `work/li2016_replication.py`:
   - Classical energy minimization: uniform (Q=0) + 3-sublattice ansatze, 40k restarts.
   - Single-site mean-field Tc: 1 = z|Jx| chi_site(T), chi_site=(1/4)/T => To=z|Jx|/4.
   - chi_zz(T) with octupolar molecular field gapping the transverse dipole channel.
   - Octupolar-wave dispersion via Eq. 5 along G-M-K-G.
   - Ix-surface phase slice (7x7 grid).
3. **Ran** with `/home/stevens/comfyui-env/bin/python`. SAVE-EARLY to
   `work/li2016_result.json` on first solve.
4. **Compared** the 4 sub-claims; all pass. Scored honestly.
5. **Packaged** 8 artifacts (extraction x2, report x6) + copied evidence.

## Provenance
Reused `ollie_multipolar_stevens_landau_kernel.py`:
`spin_matrices` (pseudospin-1/2 operators), `thermal_susceptibility`
(fluctuation formula), `landau_transition_temperature` (MF Tc estimator).

## Compute
Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).
Runtime: seconds. Target: nuc13-CPU class.

## Key results
| quantity | value |
|---|---|
| GS spin (uniform) | (0.500, 0.001, 0.002) — pure octupole Tx |
| To computed | 1.500 |Jx| (exact vs paper) |
| chi_zz max | 2.5 (finite, no divergence) |
| octupolar-wave min gap | 1.90 |
| Ix-surface FO fraction | 43/49 grid points |

**Verdict: REPLICATED.**
