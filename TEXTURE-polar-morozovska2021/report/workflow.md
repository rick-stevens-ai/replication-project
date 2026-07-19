# Workflow --- morozovska2021 (arXiv:2104.00598, flexon domain-wall chirality)

## Task type
Computational replication (PACKAGING pass). The physics was already reproduced
(`work/morozovska2021_result.json` + `work/flexon_1d.py`); this pass builds the
8-artifact deliverable bar and verifies the evidence.

## Pipeline
`acquire (done) -> parse -> extract-recipe (done) -> build (done) -> run/verify -> package -> report`

1. **Acquire** --- PDF already present (`textures-polar-morozovska2021.pdf`) +
   reading-order text (`textures-polar-morozovska2021.txt`).
2. **Parse / extract** --- `pdftotext -layout` (prose) and `pdftotext` (reading
   order) into `extraction/marker.md` and `extraction/nougat.mmd`. Real
   `marker`/`nougat` binaries are NOT installed on this host; the pdftotext
   interims carry honest NOTE headers + hand-transcribed LaTeX equations
   (Eq. 1a-1g) so the math artifact still carries the math.
3. **Build** --- from-scratch 1D two-component LGD wall solver
   (`work/flexon_1d.py`), reimplemented from the paper's Eq. 1f Lifshitz
   invariant (NOT author code; the paper is a 3D FEM with no public code).
4. **Run / verify** --- re-ran the solver live on 2026-07-19; output matched the
   saved JSON to all quoted digits (P_e(F=0.3) = -0.3479736987570781; odd
   residual 4.52e-5; P_e(0)=1.9e-12; sign_flip/grows/saturates all True).
5. **Package** --- REPORT.tex, open_questions.json, workflow.md,
   artifacts_summary.md, failure_analysis.md; result JSON + solver copied to
   report/evidence/.
6. **Validate** --- JSON parse-check on every .json artifact; `find` sweep to
   confirm all 8 artifacts present.

## Physics model (what was built)
Independent 1D Landau-Ginzburg-Devonshire 180-degree domain wall with a
flexoelectric Lifshitz invariant `F(Px Pz' - Pz Px')` (DMI-like antisymmetric
gradient coupling). Two components: axial P_z, transverse "Bloch" P_x. The
crucial ingredient is a transverse anisotropy K>|a| that makes the F=0 wall a
pure Ising wall, so F is the ONLY chirality source. Solved by Landau-Khalatnikov
overdamped relaxation on an 801-point grid.

## Tools / versions
| Tool | Version / status |
|------|------------------|
| Python | `/home/stevens/comfyui-env/bin/python` |
| numpy | 2.3.5 |
| pdftotext (poppler) | present (`/usr/bin/pdftotext`) |
| marker | NOT installed (pdftotext interim used) |
| nougat | NOT installed (pdftotext interim used) |
| pdflatex | NOT installed (REPORT.tex ships as source) |

## Effort estimate
- Physics (already done, prior session): ~1-2 h to build + tune the 1D solver,
  with the K-anisotropy trick being the key insight (without K, F=0 spuriously
  gives a chiral wall).
- Packaging (this pass): ~30-45 min, mechanical.

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-polar-morozovska2021/work/flexon_1d.py
```
