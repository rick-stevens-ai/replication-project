# Artifact Harvest

Every public artifact pulled for this replication.

| # | Artifact | Source / URL | Size | Notes |
|---|---|---|---|---|
| 1 | APBS 3.4.1 binary + libraries | conda-forge `apbs` (installed to `/data/stevens/envs/apbs-repl` on uicgpu) | env ~1 GB | Poisson-Boltzmann solver; installed via `conda create -c conda-forge apbs pdb2pqr python=3.11` |
| 2 | PDB2PQR 3.6.1 | conda-forge `pdb2pqr` (same env) | ~10 MB | Adds hydrogens, assigns AMBER/PARSE/CHARMM force-field charges/radii; itself cites the paper on invocation |
| 3 | APBS source tree | `git clone https://github.com/Electrostatics/apbs` (main branch, shallow) | ~50 MB | For the bundled `examples/` regression suite with published per-version reference values |
| 4 | Born-ion regression test | `apbs/examples/born/` (files: `apbs-mol-auto.in`, `apbs-smol-auto.in`, `README.md`, `pmf.dat`) | ~20 KB | Canonical test: 3 Å sphere +1 e, analytical answer -230.62 kJ/mol; README documents APBS results v0.1.8..v3.0 |
| 5 | Methanol/methoxide solvation test | `apbs/examples/solv/` (files: `apbs-mol.in`, `apbs-smol.in`, `methanol.pqr`, `methoxide.pqr`, README, UHBD comparison) | ~100 KB | Source is UHBD (Baker-lab predecessor); README lists documented APBS results back to v0.1.8 |
| 6 | 1AKI hen egg-white lysozyme structure | `https://files.rcsb.org/download/1AKI.pdb` (RCSB PDB) | 116 KB | 129-residue soluble protein, 1.5 Å X-ray structure |
| 7 | 1AKI PQR (my run) | Generated locally via `pdb2pqr30 --ff=AMBER --apbs-input=1AKI.in 1AKI.pdb 1AKI.pqr` | 154 KB | Protonated + AMBER FF assigned; 1079 atoms, 207 residues |
| 8 | APBS logs (my run) | `work/1AKI_solv.log`, `work/1AKI_solv_fine.log`, `work/solv-regression/*.log`, `work/born-regression/*.log` | ~8 KB each | Full multigrid solver output with per-calculation energies |
| 9 | Paper reference | https://doi.org/10.1002/pro.3280 (Protein Science, open access) | ~2 MB PDF | Not re-downloaded; well-known and pdb2pqr30 emits the citation on every invocation |

Nothing paywalled or missing.
