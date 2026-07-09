# Artifacts summary — Jurrus 2017 APBS replication

Inventory of what was produced, where it lives, and what it proves.

## Paper metadata
- **Title:** *Improvements to the APBS biomolecular solvation software suite*
- **Authors:** E. Jurrus, D. Engel, K. Star, …, N.A. Baker
- **Venue:** *Protein Science* 27(1):112–128
- **Year:** 2017/2018
- **DOI:** https://doi.org/10.1002/pro.3280
- **Citations (S2):** 2,081

## Software identity (installed)
| Package  | Version | Source        |
|----------|---------|---------------|
| APBS     | 3.4.1   | conda-forge   |
| PDB2PQR  | 3.6.1   | conda-forge (`pdb2pqr30`) |
| Python   | 3.11    | conda-forge   |

Both binaries self-cite Jurrus 2018 on invocation — software identity is
inline with the install.

## Compute
- Host: `uicgpu` (Linux x86_64)
- Solver mode: single-CPU multigrid (MG-auto)
- GPU: not used (not needed for this suite)

## Directory layout
```
~/Dropbox/REPLICATE-PROJECT/PDE-Jurrus-APBS-solvation-2017/
├── report/
│   ├── REPORT.md              (canonical replication writeup)
│   ├── REPORT.tex             (LaTeX version + genuine critique section)
│   ├── open_questions.json    (5 grounded open questions)
│   ├── workflow.md            (chronological reproducible workflow)
│   ├── artifacts_summary.md   (this file)
│   └── failure_analysis.md    (residuals, non-tested paths, judge caveats)
├── extraction/                (paper text extraction stub)
└── work/                      (raw command traces, inputs, outputs)
```

## Numerical artifacts

### A. Bundled regression suite (from APBS source `examples/`)

| Test | Documented | Reproduced | Match |
|---|---|---|---|
| `born/apbs-mol-auto.in` (v1.5)          | −229.7740 | **−229.7736**  | 4 decimals |
| `born/apbs-mol-auto.in` vs analytical    | −230.62   | −229.7736       | 0.37 % |
| `solv/apbs-mol.in` methanol (v3.0)      | −36.2486  | **−36.24863**   | 6+ decimals |
| `solv/apbs-mol.in` methoxide (v3.0)     | −390.4122 | **−390.41217**  | 6+ decimals |
| `solv/apbs-mol.in` diff (v3.0)          | −354.1635 | **−354.16354**  | 6+ decimals |
| `solv/apbs-smol.in` methanol (v3.0)     | −37.5759  | **−37.57594**   | 6+ decimals |
| `solv/apbs-smol.in` methoxide (v3.0)    | −391.2388 | **−391.23886**  | 6+ decimals |
| `solv/apbs-smol.in` diff (v3.0)         | −353.6629 | **−353.66292**  | 6+ decimals |

### B. Manual Born-ion analytical check
| Quantity | Value |
|---|---|
| Closed-form Born (z=+1, R=3 Å) | −230.62 kJ/mol |
| APBS 3.4.1 (manual grid)       | −229.59 kJ/mol |
| Absolute error                 | 1.03 kJ/mol |
| Relative error                 | 0.45 % |

### C. Independent case (1AKI lysozyme, my run)
| Grid   | Polar solvation ΔG (kJ/mol) |
|--------|-----------------------------|
| 129³   | −4345.23 |
| 161³   | −4258.03 |
| Δ (grid refinement) | ~2 % |

Paper does not publish a 1AKI reference value; this test verifies the
PDB2PQR → APBS pipeline end-to-end and returns physically reasonable
numbers for a 129-residue soluble protein at 150 mM NaCl.

## Claims coverage
- **Core FD-multigrid claims (C1–C5):** fully covered.
- **Newer feature claims (C6 TABI-PB, C7 geoflow, C8 Python API):** not tested.
- **Judge cross-check:** Argo `gpt-5`, coverage 92, agreement 99.

## External artifacts referenced (all public, all fetched fresh)
- APBS source: `https://github.com/Electrostatics/apbs`
- 1AKI PDB: `https://files.rcsb.org/download/1AKI.pdb`
- APBS docs: `https://apbs.readthedocs.io/using/examples/solvation-energies`

## Command-trace files under `work/`
- `born_out.txt` — bundled Born regression run
- `mol_out.txt`, `smol_out.txt` — bundled methanol/methoxide runs
- `born_manual_out.txt` — manual Born analytical-check run
- `1AKI_129.txt`, `1AKI_161.txt` — 1AKI two-grid runs
- Input decks: `born/born.in`, `1AKI_solv.in`, `1AKI_solv_fine.in`
- PQR file: `1AKI.pqr` (PDB2PQR product)

## Verdict
**REPLICATED** — see `REPORT.md §5` and `REPORT.tex` for justification.
Final line:
```
WAVE_RESULT set=PDE paper=Jurrus-2017-APBS verdict=REPLICATED
dir=~/Dropbox/REPLICATE-PROJECT/PDE-Jurrus-APBS-solvation-2017/
one_line=APBS 3.4.1 + PDB2PQR 3.6.1 reproduce bundled regression tests
to 6+ decimals; Born analytical 0.45%; 1AKI pipeline OK
```
