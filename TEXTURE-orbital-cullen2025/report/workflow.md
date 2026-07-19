# Workflow --- Cullen 2025 (arXiv:2509.20436v3) conventional-Kubo replication

## Paper
Cullen, Wang & Culcer, *Orbital Hall effect in spin-3/2 hole-doped semiconductors
and its implications for orbitronics*, arXiv:2509.20436v3 [cond-mat.mes-hall], 18 Jun 2026.
System: bulk p-type **Ge** (also Si, GaAs, InAs, InSb). Method: modern theory of orbital
magnetisation on the Luttinger--Kohn--Bir--Pikus valence-band Hamiltonian, **with quantum
corrections to the orbital current**.

## Method class & compute routing
Model-Hamiltonian / k.p + intrinsic (Berry-curvature) Kubo. Small 4x4 matrices on a 3D
k-grid --> CPU, ran locally. No GPU / cluster needed (41^3 grid finishes in ~2.4 s).

## Tools / versions
| Tool | Version / path | Role |
|------|----------------|------|
| Python | `/home/stevens/comfyui-env/bin/python` | run kernel |
| numpy | 2.3.5 | linear algebra (`eigh`) |
| pdftotext (poppler) | `/usr/bin/pdftotext` | extraction fallback (marker/nougat absent) |
| marker | NOT installed | would produce extraction/marker.md (prose) |
| nougat | NOT installed | would produce extraction/nougat.mmd (math) |
| pdflatex | not required on host | REPORT.tex ships as source, compiles off-host |

## Pipeline executed
1. **Acquire** --- PDF already in paper dir (`textures-orbital-cullen2025.pdf`).
2. **Parse** --- `pdftotext` reading-order + `-layout` text (marker/nougat unavailable).
3. **Extract recipe** --- `replication_recipe.json` (already present): 4x4 spherical + full
   6x6 Luttinger, headline ~10^3 (hbar/e) Ohm^-1 cm^-1, no public code.
4. **Build** --- from-scratch `work/ohe_spherical.py`: spherical Luttinger H0 (Eq. 2),
   analytic k-gradients, spin-3/2 J matrices, orbital current j^{Lz}_x = 1/2{Lz,vx},
   conventional interband Kubo sum. **Quantum corrections deliberately NOT built** (scope).
5. **Run** --- coarse-first SAVE-EARLY: N=21 -> 31 -> 41 at EF=10 meV, plus N=41 EF=5 meV.
   Save JSON after every grid size. Verify k_max > k_F^{hh} (grid encloses hole pocket).
6. **Compare** --- converged sigma_conv ~= 49 (hbar/e) Ohm^-1 cm^-1 vs paper total ~10^3;
   reconciled via paper Fig. 2 (quantum corrections dominate; conventional is sub-dominant).
7. **Report** --- this 8-artifact package.

## Physics-verification re-run (packaging discipline)
Before packaging, the kernel was re-executed live (2026-07-19) to confirm the stale JSON:
`compute(31, 4.0e8, 10.0)` returned **49.9217**, identical to the saved `N31_EF10` value.
`k_F^{hh} = 2.762e8 m^-1 < k_max = 4.0e8 m^-1` --> grid covers Fermi surface. Number trusted.

## Convergence
| N | sigma_conv (hbar/e Ohm^-1 cm^-1) |
|---|----------------------------------|
| 21 | 48.30 |
| 31 | 49.92 |
| 41 | 49.41 |
Drift < 3% across N=21/31/41 => converged.

## Effort estimate
- Physics build + run (prior session): ~1 h (small matrices, fast convergence).
- Packaging (this pass): ~45 min (extraction interims + REPORT.tex with hand-transcribed
  equations + open_questions + failure analysis + evidence copy + validation).
- To CLOSE the headline gap (future): build Delta j1,2,3 quantum corrections + 6x6 model,
  estimated multi-day (the covariant-derivative modern-theory-of-orbital-magnetisation machinery).

## Verdict
**PARTIAL** --- Coverage 5/10, Agreement 5/10. Right observable, conventional term only;
core single-particle physics (spherical bands, finite Berry curvature under inversion
Omega_i = -(k_i/k^3)J_z, right order for the conventional piece) reproduces; the ~10^3
headline needs the unbuilt quantum corrections.
