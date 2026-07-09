# Parser Provenance — apbs-pb

**Pass:** Re-pass (2026-06-23)

## Source artifact

No canonical paper-PDF parse was needed for the re-pass. The replication
target is a *software paper* (Jurrus et al. 2017, Protein Sci 27(1):112-128,
DOI 10.1002/pro.3280); the claims that drive the replication are not in the
PDF prose but in:

1. `apbs-src/examples/*/README.md` — per-example, per-version reference
   solvation/binding energies and force values, maintained by the APBS
   authors back to APBS 0.1.8 (~2004).
2. `apbs-src/tests/test_cases.cfg` — machine-readable reference numerics
   used by the formal `apbs_tester.py` regression harness.
3. `apbs-src/examples/born/pmf.dat` — Born-ion analytical-vs-numerical
   convergence table.

These are the same files the paper itself cites as the regression record
of every released version.

## "Parser" used

For the re-pass, the "parser" is the **APBS executable itself** plus the
**bundled per-example READMEs**, read with `read`/`grep`/`cat` from the
shallow `git clone --depth 1 https://github.com/Electrostatics/apbs.git`
that was retained in `apbs-src/`. No PDF-to-text conversion step was
performed — the reference values are in the repository, not the PDF.

Reference per-example READMEs consulted in this re-pass:

- `examples/pka-lig/README.md` (UHBD comparison ligand binding)
- `examples/ion-pmf/README.md` (Im et al. force-decomposition reference)
- `examples/protein-rna/README.md` (Garcia-Garcia/Draper ionic-strength
  table for protein-RNA binding, full 18 ionic strengths)
- `examples/born/pmf.dat` (analytical Born convergence with radius)
- `examples/born/README.md` (per-version Born energies)
- `examples/helix/README.md` (membrane protein with explicit dielectric map)
- `examples/{bem,pbam,pbsam-gly,geoflow,pygbe}/README.md` (sub-solver
  feature checks — confirms negative results in the conda binary)

## Tooling

- APBS binary: `apbs 3.4.1` from conda-forge channel, env
  `/Users/stevens/opt/anaconda3/envs/apbs`, executable compiled
  2026-01-30. `apbs --version` reports `APBS 3.4.1`.
- Python harness: stock CPython in the `apbs` env (used only for
  `apbs_tester.py` from `apbs-src/tests/` in pass 1; re-pass uses the
  raw binary directly).
- All numerical comparisons in the re-pass are byte-stable text parsing
  of `apbs` stdout `Global net energy` lines and `pmf.dat`.

## No fabrication policy

Every numeric value in `REPORT.md` is either (a) lifted verbatim from a
per-example README in the cloned repo or (b) produced by re-running APBS
3.4.1 here. Lines in REPORT.md tagged with a file path under
`logs/repass/` or `results/repass/` reference a stored log/output from
this re-pass.
