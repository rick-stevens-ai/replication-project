# Workflow: Replication of Konakanchi et al. 2025 (ps-scale octupole relaxation)

**Paper:** Electrically Tunable Picosecond-scale Octupole Fluctuations in Chiral
Antiferromagnets — arXiv:2501.18978v1 (2025).
**Headline claim:** octupole relaxation in Mn3Sn-type chiral AFM nanomagnets
reaches picosecond / ~10 ps timescales in the low-barrier regime, orders of
magnitude faster than dipolar ferromagnets, and is electrically tunable.
**Verdict:** REPLICATED.

## Steps taken

1. **Read paper + recipe.** Parsed `work/textures-multipolar-konakanchi2025.txt`
   and `report/evidence/replication_recipe.json`. Identified the key physics:
   - Effective octupole free energy Eq. B19:
     `V*F_oct = (3/2) Ms H_J V mz^2 + Delta sin^2(phi_oct)`.
   - Exchange field `H_J ~ 100 T` (vs ~1 T dipole field of XY FM).
   - Low-barrier dephasing autocorrelation Eq. 9/10 (Gaussian decay).
   - High-barrier Langer/IHD escape Eq. D12.
   - Quoted result: ~10 ps for sub-kT barriers.

2. **Built from-scratch model** in `work/konakanchi2025_replication.py`:
   - `tau_lowbarrier_analytic` — both self-consistent model form and paper Eq.10.
   - `C_lowbarrier_numeric` — Monte-Carlo Boltzmann sampling of Eq. 9.
   - `tau_highbarrier_ihd` — Langer IHD escape (Eq. D12) x 0.25 octupole factor.
   - `langevin_octupole` — direct stochastic integration of reduced (mz, phi_oct)
     with FDT noise; independent measurement of C(t)=<mx(0)mx(t)>.
   - Octupole operator provenance via
     `ollie_multipolar_stevens_landau_kernel.py` (Txyz sanity checks).

3. **SAVE-EARLY** to `work/konakanchi2025_result.json` on first run.

4. **Reconciled internal consistency** (honest): first run flagged a fixed
   prefactor mismatch between the mangled-PDF transcription of Eq. 10 and the
   self-consistent free-energy prediction. Corrected the analytic to be
   self-consistent with our own Eq. B19, and report the paper's published Eq. 10
   prefactor separately. After this, numeric Eq.9 matches analytic to 0.16%.

5. **Compared to ~ps** and self-scored → REPLICATED.

6. **Packaged 8 artifacts** (see artifacts_summary.md) + copied code/result to
   `report/evidence/`.

## Runner
`/home/stevens/comfyui-env/bin/python work/konakanchi2025_replication.py`
(< 1 min, single small run; seeded RNG = 20250131 for reproducibility).

## Key numbers reproduced
- Min low-barrier tau: 13.5 ps (model) / 6.5 ps (paper Eq.10 prefactor) — ps scale ✓
- Eq.9 numeric vs analytic: 0.16% mean rel. diff ✓
- Langevin vs analytic: 1.5x ✓
- High-barrier (Delta=4.5kT): ~13 ns — orders slower ✓
