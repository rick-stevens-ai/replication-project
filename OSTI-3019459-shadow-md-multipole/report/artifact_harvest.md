# Artifact Harvest — OSTI-3019459

## Paper PDF
- URL: https://www.osti.gov/servlets/purl/3019459
- File: `work/osti_3019459.pdf`
- Size: 4,099,550 bytes
- Fetched: 2026-07-02 via uicgpu proxy (direct SSL fetch succeeded, no 403)
- SHA256: (unnecessary — LA-UR-25-29120 is the canonical preprint identifier)

## Journal record
- Journal: J. Chem. Phys. 164, 064118 (2026)
- DOI: 10.1063/5.0307700
- Published online: 2026-02-12

## Code artifact
- Repo: https://github.com/lanl/sedacs
- Path checked out: `work/sedacs/` (full clone, 100+ commits)
- Head commit at fetch: `9f041c9 remove old scf example for sedacs-latte interface`
- Relevant files:
  - `src/sedacs/cheq/shadow_solver.py` (189 lines) — monopole-only shadow QEQ solver (Newton-Krylov / linearized closed-form)
  - `src/sedacs/cheq/charge_solver.py` (80 lines) — reference (non-shadow) QEQ solver
  - `examples/cheq_md/run_MD.py` (485 lines) — full shadow-MD driver for water using hippynn NN potentials + PME long-range Coulomb + QEQ solver
- **Flexible-multipole (dipole) extension code from the 2026 paper is NOT public in SEDACS as of 2026-07-02.** The paper's Data Availability statement says "will be made available" — future work.

## Pre-trained models (in SEDACS repo)
- `examples/cheq_md/model_data/best_checkpoint.pt` — hippynn short-range NN
- `examples/cheq_md/geo_data/water_{6540,10008,25050,52320}.pdb` — 4 water systems (6.5k–52.3k atoms)
- `examples/cheq_md/geo_data/NVT_300K_water_{...}.pt` — pre-equilibrated NVT states

## Not harvested
- Paper's exact 3 test systems (acetamide-in-water, 93/162/263 atoms) — NOT in the released repo. They can be constructed from PDB/CIF sources but the associated MATLAB/Python prototype code for the flexible-multipole ChEQ+dipole model was not released with the paper.
- Supplementary material (referenced in paper as containing pseudocode) — not attempted; irrelevant to numerical claim replication.
