# Artifact Harvest — Wang/Alexov/Zhao 2021 PB regularization

## Primary artifact: the paper (open access)
- **DOI:** 10.3934/mbe.2021072
- **Publisher landing:** http://www.aimspress.com/article/doi/10.3934/mbe.2021072 (HTTP 200)
- **OA PDF:** http://www.aimspress.com/aimspress-data/mbe/2021/2/PDF/mbe-18-02-072.pdf
  - size: 22,942,681 bytes (22.9 MB), 36 pages, PDF 1.5
  - local: `work/paper.pdf`; extracted text `work/paper.txt` (pdftotext -layout, 1833 lines)
  - License: AIMS Press, "2021 The Author(s)" — open access.
- Title (as published): "On regularization of charge singularities in solving the
  Poisson-Boltzmann equation with a smooth solute-solvent boundary"
  (the wave task's "finite element/difference method" string is a paraphrase; same DOI).

## Code / data availability
- **No public code or data repository** is provided by the paper (no GitHub/Zenodo/SI
  code link). The method is fully specified by equations in the text, so replication is
  from-scratch reimplementation (this is the norm for this math-bio numerical PDE paper).
- Protein PDB IDs referenced (Tables 5,6,7): 1AHO, 1C75, 1J0P, 1TG0, 1X8Q, 1CBN, 1G6X,
  1IQZ, 1IUA, 1L9L, 1M1Q, 1NWZ, 1OK0, 1TQG, 1VB0, 1VBW, 1W0N, 1X6X, 1XMK, 1ZUU, 1ZZK
  (protein set); complexes 1EMV, 1BRS, 4HTC, 1JTG, 1AVA, 1A3N, 1BEB. These require
  CHARMM force-field charges/radii + PQR generation + GCS + rMIB reference values that
  are NOT distributed; the protein/salt tables are therefore out of reach for exact
  numeric replication and are treated as SPOT-CHECK (structures are public in the PDB).

## Self-produced artifacts (this replication)
- `work/pb_reg.py`      — first solver (explicit Python assembly; both reg + trilinear).
- `work/pb_reg2.py`     — vectorized sparse solver (primary); nondiv scheme = paper Eq(2.17),
                          analytic grad(eps) for the analytic tanh surface.
- `work/born_analytic.py` — closed-form Born/Kirkwood energy; reproduces paper's
                          analytic SAS value -46.8447 kcal/mol EXACTLY (Coulomb const 332.06371).
- `report/evidence/reg2_1charge_nondiv.json` — one-charge convergence table (N=11..201).
- `report/evidence/reg2_2charge_nondiv.json` — two-charge convergence table (N=11..201).
- `report/evidence/born_check.txt`           — analytic Born validation output.
- `report/evidence/born_val.log`             — solver->sharp-interface Born limit check.

## Compute
- Small N (11..51): local, CherryRd (macOS), seconds each.
- N=101, 201: uicgpu (8xA100 host; solve is CPU sparse BiCGSTAB, 255 cores, no paid endpoints).
- No LLM inference used for numerics. LLM-judge (Argo, free) used only for final verdict.
