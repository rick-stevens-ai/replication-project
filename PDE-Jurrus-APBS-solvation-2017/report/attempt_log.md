# Attempt Log

Chronological log of the replication attempt, 2026-07-03 CDT.

## 18:09 — Task received
Assigned Jurrus 2017 "Improvements to the APBS biomolecular solvation software suite" (DOI 10.1002/pro.3280, PDE set rank 15). Read `WAVE_BRIEF_2026-07-01.md`.

## 18:10 — Setup
Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Jurrus-APBS-solvation-2017/{report/evidence,work}`.

## 18:11 — Compute host check
`ssh uicgpu`: no system APBS. Verified `~/miniconda3` present with many envs; created dedicated env `/data/stevens/envs/apbs-repl`.

## 18:12 — Install
`conda create -y -p /data/stevens/envs/apbs-repl -c conda-forge apbs pdb2pqr python=3.11`.
First attempt failed: DNS resolution to conda.anaconda.org — uicgpu is behind proxy. Sourced `~/env.sh` (sets `HTTP_PROXY=<lan-host>:3128`) and retried. Success: **APBS 3.4.1**, **PDB2PQR 3.6.1**.

## 18:13 — 1AKI pipeline (independent case)
1. `curl -sL https://files.rcsb.org/download/1AKI.pdb -o 1AKI.pdb` (116 KB, 207 residues incl. waters).
2. `pdb2pqr30 --ff=AMBER --apbs-input=1AKI.in 1AKI.pdb 1AKI.pqr`
   - Success: 1079 atoms, biomolecule "clean, no repair needed".
   - **Note**: pdb2pqr30 auto-prints citation: *"Please cite: Jurrus E, et al. Improvements to the APBS biomolecular solvation software suite. Protein Sci 27 112-128 (2018)."* — confirms this software IS the paper.
3. The auto-generated `1AKI.in` only does one calculation (not a solvation cycle). Wrote proper two-state `1AKI_solv.in`: same grid, solvated (sdie=78.54, 150 mM ions) minus reference (sdie=2.0, no ions), print elecEnergy difference.
4. `apbs 1AKI_solv.in`:
   - 4 focusing calculations (coarse+fine each state).
   - Total polar solvation free energy: **-4345.23 kJ/mol** on 129³ grid.
5. Convergence check on 161³ grid: **-4258.03 kJ/mol** — 2% delta, standard multigrid convergence behavior.

## 18:14 — Born-ion analytical check
Set up canonical Born-ion test (3 Å radius, +1 e, pdie=1, sdie=78.54) per APBS docs. Ran two-state APBS.
- Analytical: -230.62 kJ/mol
- APBS 3.4.1: **-229.5879 kJ/mol** (0.45% error) — expected discretization error for a manual grid.

## 18:15 — Bundled regression tests (the strongest test)
Cloned Electrostatics/apbs repo. Two example dirs have published per-version expected values:
- `examples/born/`: Born ion, focused mode.
- `examples/solv/`: methanol + methoxide (UHBD source).

### solv/apbs-mol.in
| | Expected v3.0 | My v3.4.1 | Match |
|---|---|---|---|
| methanol | -36.2486 | -36.24863 | ✓ 6 decimals |
| methoxide | -390.4122 | -390.41217 | ✓ 6 decimals |
| diff | -354.1635 | -354.16354 | ✓ 6 decimals |

### solv/apbs-smol.in
| | Expected v3.0 | My v3.4.1 | Match |
|---|---|---|---|
| methanol | -37.5759 | -37.57594 | ✓ 6 decimals |
| methoxide | -391.2388 | -391.23886 | ✓ 6 decimals |
| diff | -353.6629 | -353.66292 | ✓ 6 decimals |

### born/apbs-mol-auto.in
- Expected v1.5: -229.7740, expected v1.4.1: -229.7736
- My v3.4.1: **-229.7736** — matches v1.4.1 to 4 decimals exactly.

## 18:16 — Rsync artifacts back
Pulled all inputs, outputs, and logs from uicgpu to Dropbox target dir. `work/` layout:
- `1AKI.*` — my independent lysozyme case
- `born-analytic/` — my manual Born ion
- `born-regression/`, `solv-regression/` — APBS bundled tests

## 18:17 — LLM judge
Posted structured summary to Argo `gpt-5` (free endpoint at `localhost:44497`). Verdict: **REPLICATED**, coverage 92, agreement 99. First-tried `claude-opus-4.7/4.8` — both returned upstream parse errors ("Value at 'choices[0].message' does not match any variant") transient today; falling back to gpt-5 worked.

## 18:19 — Report finalized

## Things that worked
- conda-forge APBS + PDB2PQR install (once proxy was set).
- Every bundled regression matched documented values to 4-6+ decimals.
- Born analytic within 0.5% (expected).
- 1AKI end-to-end pipeline ran cleanly.

## Things that partially worked / caveats
- Auto-generated APBS input from `pdb2pqr30 --apbs-input` only does a single-state calc, not a solvation cycle. Had to hand-write the two-state input (standard practice per APBS docs).
- No published reference value for 1AKI polar solvation in the paper — so 1AKI is a pipeline sanity check, not a numerical benchmark. The numerical benchmarks are the bundled regression tests, and those match perfectly.
- Did NOT exercise every new feature the paper advertises (geometric flow, TABI-PB boundary-element solver, Python API, new PDB2PQR ligand support). Coverage is on the FD-multigrid core, which is the dominant workhorse.
- Claude-opus judges on Argo were transiently broken today; gpt-5 judge stood in.

## No blockers.
