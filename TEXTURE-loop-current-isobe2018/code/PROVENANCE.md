# PROVENANCE

## Paper
Isobe, Yuan, Fu, "Unconventional Superconductivity and Density Waves in Twisted
Bilayer Graphene," Phys. Rev. X 8, 041041 (2018); arXiv:1805.06449v2.

## Shared-kernel provenance and SCOPE DECISION
- Shared kernel consulted: `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
  (a kagome tight-binding + Peierls-flux loop-current/Chern kernel built for
  Fernandes-Birol-Ye-Vanderbilt arXiv:2502.16657).
- **Read first, as required.** Verdict: **NOT reusable for this paper's core.**
  Isobe-Yuan-Fu 2018 is a *hot-spot patch RG* model for twisted bilayer
  graphene near the n=2 Van Hove filling. It has no tight-binding lattice,
  no Peierls flux, no Bloch Hamiltonian, no Berry curvature / Chern number.
  The kernel's `KagomeModel`, `chern_number`, `bond_current_and_charge`,
  `triangle_flux_from_config` machinery is out of scope and was NOT imported.
- Only the *conceptual* link (interaction-driven density-wave/SC selection from
  couplings, cf. the kernel's `patch_leading_channel` Box-2 selector) carries
  over; Isobe uses a quantitatively different 9-coupling one-loop RG which we
  re-implemented from the paper's Eqs. (9)-(24).
- This is an honest OUT-OF-SCOPE flag for the kagome loop-current kernel, and a
  faithful in-scope replication of the paper's actual computational core.

## Code written for this replication
- `isobe2018_rg.py` — RG beta-functions Eqs.(9)-(15), interaction strengths
  Eqs.(17)-(23), RPA divergence Eqs.(16)/(24), SciPy RK45 integrator.
- `run_checks.py` — 5 machine-checkable claim tests; writes work/results.json
  and work/rg_flow_and_phase.png.

## Equations transcribed from the paper (source of truth)
Eqs. (9)-(15) RG flow; (16),(24) RPA susceptibility; (17)-(23) V_eta channel
interaction strengths; Sec III B-C selection statements; Fig. 4 phase diagram.

All numeric outputs are computed at runtime. No figure values were transcribed.
