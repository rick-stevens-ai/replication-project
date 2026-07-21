# Artifacts Summary & Self-Score — lund2021

## Verdict: REPLICATED (coverage broadened from k=0 resonance to full k-resolved bands)

## Artifacts (8)
1. `extraction/marker.md` — extraction interim + key physics.
2. `extraction/nougat.mmd` — MMD header + abstract/equations.
3. `report/REPORT.tex` — full replication report (LaTeX).
4. `report/open_questions.json` — 5 questions + next_steps.
5. `report/workflow.md` — end-to-end method.
6. `report/artifacts_summary.md` — this file.
7. `report/failure_analysis.md` — limitations & failure modes.
8. `report/evidence/lund2021_result.json` + `report/evidence/lund2021_lswt.py`
   — results JSON and from-scratch code (plus `replication_recipe.json`).

## Results vs claim
| Claim element | Paper | This replication | Match |
|---|---|---|---|
| Three spin-wave bands | yes | 3 LSWT bands + 3 uniform modes | ✅ |
| Mutually orthogonal polarizations | x,y,z | eigenvectors = x̂,ŷ,ẑ; ortho err 0.0 | ✅ |
| In-plane doublet + out-of-plane singlet | ω0^x=ω0^y≠ω0^z | 0.9487, 0.9487, 1.0954 | ✅ |
| Resonance-freq formula √(4K1a2/a1²) | analytic | numeric = formula (exact) | ✅ |
| Freq ratio √(K2/K1)=√(2K/(Kz+K)) | analytic | 1.15470 = 1.15470 | ✅ |
| Kagome zero-energy flat band (bonus) | (known physics) | std 1.5e-8, mean 1.5e-8 | ✅ |
| **Finite-k: 3 distinct bands across BZ** | (k=0 claim) | 24×24 grid; flat @0.557 + 2 disp. | ✅ |
| **Finite-k polarization purity** | (x/y/z at k=0) | 0.99–1.00 at Γ, mean 0.79 over BZ | ✅ |
| **Band topology / thermal Hall** | (not in paper) | κ_xy=0 by symmetry (no DMI); bounded | ✅ |

## Self-score
- **Coverage: 8/10.** Reproduced the core checkable physics of the kagome
  application (band count, polarizations, resonance frequencies), the
  bonus flat-band check, AND — new in this pass — the **full k-resolved band
  structure with eigenvector polarization projection** across a 24×24 BZ
  (mean purity 0.79, 0.99–1.00 at Γ) plus a **Berry-curvature / thermal-Hall
  bound** (κ_xy=0 by symmetry, degeneracy diagnostic). This broadens
  coverage from the k=0 resonance to the full band picture the paper's Fig.
  2b invokes. Not covered numerically end-to-end: the full Onsager/
  spin-pumping transport chain (Eqs. 17–18, ISHE voltage) — analytic
  derivations verified structurally, not simulated.
- **Agreement: 9/10.** Every checkable quantity matches: polarizations
  exactly orthogonal at k=0 (err 0.0), frequency ratio exact, flat band at
  zero (Heisenberg) / 0.557 JS (with anisotropy); the finite-k polarization
  smoothly generalizes the k=0 x/y/z picture. Slight honesty deduction: the
  raw single-band FHS Berry flux is ill-defined at the in-plane band
  touchings (reported transparently as artifact, with the correct physical
  κ_xy=0 established by symmetry).

## Note on scope
The task brief anticipated flat-band/Dirac/thermal-Hall character. The
actual lund2021 paper is a **spin-pumping** paper; its "three bands" are k=0
resonance modes. We replicated the paper's real claim AND independently
confirmed the kagome flat band from full LSWT, covering both interpretations.
