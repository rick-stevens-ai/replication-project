# apbs-pb — APBS Poisson-Boltzmann Replication

Honest open-data, open-source replication of the canonical examples and test suite
shipped with the APBS biomolecular electrostatics package (Jurrus et al., *Protein
Science* 2017/2018; https://github.com/Electrostatics/apbs).

**Headline result:** APBS 3.4.1 (conda-forge) reproduces 213 of 215 bundled
reference values bit-for-bit on macOS, and recovers the analytical Born-ion
solvation free energy to within 0.7 % across multigrid and adaptive-FEM solvers.

See `REPORT.md` for the full claim-by-claim table, evidence, and limitations.

## Quick start

```bash
conda create -n apbs -c conda-forge apbs=3.4.1 -y
conda activate apbs
git clone --depth 1 https://github.com/Electrostatics/apbs.git
cd apbs/tests

# Run the full PB / FEM / apolar test categories
for t in born actin-dimer-auto alkanes FKBP solv ionize hca-bind \
         ion-protein point-pmf; do
  python apbs_tester.py -e "$(which apbs)" -t "$t"
done

# Or run individual examples by hand
cd ../examples/born
apbs apbs-mol-auto.in   # → Global net ELEC energy = -2.2977e+02 kJ/mol
                        # vs analytical -230.62 kJ/mol (0.37 % error)
```

## What's here

| File / dir   | What                                                          |
|--------------|---------------------------------------------------------------|
| `REPORT.md`  | Full replication report (license, coverage, limits, evidence) |
| `PROGRESS.md`| Time-stamped activity log                                     |
| `apbs-src/`  | Shallow `git clone` of `Electrostatics/apbs`                  |
| `logs/`      | Raw stdout from every test/example run                        |
| `results/born/` | Born-ion PQR + analytical convergence table              |

## Coverage / agreement score

**213 / 215 = 99.07 %** of in-scope PB test checks pass bit-for-bit against
documented references. The 2 misses are an upstream Python-3.12 file-mode bug in
the test *harness* and would have exercised MPI-parallel code paths that the
conda binary cannot run anyway.

## Friction tags

`install:trivial-conda` · `data:bundled-open` · `numerics:bit-identical` ·
`physics:agrees-analytical-0.4pct` · `mpi:not-in-conda-package` ·
`harness:py312-rU-bug`

## License

The APBS source under `apbs-src/` is BSD‑3‑style (Battelle/PNNL et al., 2010-2022).
This replication's documents/scripts are CC0 — re-use freely.
