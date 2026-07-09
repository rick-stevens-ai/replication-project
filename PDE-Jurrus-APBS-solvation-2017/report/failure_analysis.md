# Failure analysis — Jurrus 2017 APBS replication

Verdict on the parent replication is **REPLICATED**. This document does
the opposite: it catalogs the things that did *not* work, were not
tested, or have residual concerns — the honest-limitations log that
accompanies the successful headline result.

## 1. Hard failures during the run
None. Every attempted step completed:
- conda-forge env created cleanly
- `apbs` and `pdb2pqr30` invoke without error
- all four bundled regression inputs (`apbs-mol-auto.in`,
  `apbs-mol.in`, `apbs-smol.in`, manual Born) returned finite numeric
  energies
- 1AKI PDB2PQR → APBS pipeline finished at both grid resolutions

No timeouts, no OOMs, no solver-divergence warnings.

## 2. Numerical residuals (things that "worked" but with caveats)

### 2.1 Born-ion 0.37 % / 0.45 % discretization gap
- Bundled `apbs-mol-auto.in` returned **−229.7736** vs analytical
  **−230.62** — a 0.37 % underestimate.
- Manual tutorial input returned **−229.59** — a 0.45 % underestimate.
- Both errors are the expected sign (finite-difference dielectric
  boundary blurring reduces the magnitude of the Born energy).
- Concern: the paper's own regression README treats −229.7740 as a
  reference value without discussing that it is 0.37 % away from the
  analytical answer. Reproducibility to 6+ decimals on the same input
  does not mean the answer is *converged*.

### 2.2 1AKI 2 % grid-refinement gap
- 129³ → **−4345.23 kJ/mol**
- 161³ → **−4258.03 kJ/mol**
- Δ ≈ 87 kJ/mol ≈ 2 % of the polar solvation.
- Normal MG-auto behavior, but non-trivial: production use would need
  at least one more refinement level and Richardson-style extrapolation
  before treating any single-grid 1AKI number as converged.

### 2.3 LPBE only
All tests were run with the linearized PBE. The paper explicitly
advertises improvements for highly-charged systems (nucleic acids,
membranes) where nonlinear PBE is required and Newton-iteration
convergence becomes a real concern. That regime is entirely untested
here. (See `open_questions.json` Q1.)

## 3. Paper-claimed features that were NOT exercised (scope gaps)

| Claim | Reason for skip | Risk if wrong |
|---|---|---|
| C6 TABI-PB boundary-element solver | Requires alternate solver build path (`--enable-bem`) not in the conda-forge binary; would need source build. | Medium — this is an advertised paper contribution; TABI-PB accuracy vs MG-auto on shared benchmarks remains uncharacterized in this replication. |
| C7 Geometric-flow non-polar solvation | Same — alternate build path. | Medium — advertised contribution; not exercised. |
| C8 Python API | Out of scope for a single-run subagent. | Low — thin API wrapper over the tested solver core; unlikely to fail independently, but "unlikely" is not "verified". |

Recording these as scope gaps, not failures. A depth-first follow-up
replication would build APBS from source with `bem` and `geoflow`
enabled and compare the three solver backends head-to-head on a shared
benchmark set.

## 4. Methodological caveats

### 4.1 Single-machine, single-compiler, single-BLAS
- All numbers come from **one** conda-forge binary on **one** Linux host
  (uicgpu, x86_64).
- No cross-platform confirmation (no macOS/ARM, no source build against
  a different LAPACK).
- Risk: platform-dependent numerical drift is not surfaced. Historically
  APBS multigrid is highly deterministic, but this replication does not
  actively demonstrate that.

### 4.2 No comparison to explicit-solvent MD
- The implicit-solvent premise of PBE is not tested against a matched
  TIP3P/OPC free-energy-perturbation reference on a shared molecule
  set (e.g. Mobley FreeSolv).
- Risk: reproducing APBS's internal numbers is not the same as
  demonstrating APBS's *utility*. The continuum-vs-explicit gap is a
  live concern in the field and is untouched here. (See
  `open_questions.json` Q2.)

### 4.3 LLM-judge concurrence is confirmatory, not independent
- Argo `gpt-5` judge reported coverage 92, agreement 99.
- The judge saw the same evidence pack the writer assembled. It
  confirmed that the writeup is *internally consistent*.
- It did not, and cannot, provide independent scientific validation.

### 4.4 Single conformation for 1AKI
- Polar solvation was computed on a single crystallographic
  conformation. Real applications need ensemble averaging over an MD
  trajectory. Single-snapshot vs snapshot-averaged variance is
  uncharacterized here. (See `open_questions.json` Q5.)

## 5. Judge / adversary-mode disagreements
None recorded. The judge's 92 / 99 numbers indicate high agreement on
both coverage and correctness. Absence of dissent is itself a mild
caveat — a genuinely adversarial reviewer would probably push harder
on §3 (scope gaps) and §4.2 (no explicit-solvent comparison).

## 6. Reproducibility risks (things that could break next time)
- **conda-forge channel drift:** future APBS builds may bump multigrid
  parameters or coordinate rounding, producing off-by-last-digit changes
  in the regression numbers.
- **PDB2PQR force-field parameter revisions:** `--ff=AMBER` today is not
  guaranteed to be byte-identical to the AMBER parameterization used by
  the paper. 1AKI energies could shift by tens of kJ/mol on parameter
  updates.
- **PDB header updates:** RCSB occasionally re-releases PDB files with
  micro-adjustments; 1AKI atom coordinates are stable but not
  contractually frozen.
- Mitigation: pin the APBS + PDB2PQR versions used here (3.4.1 and
  3.6.1) in the conda-lock file inside `work/` if / when a follow-up
  replication is scheduled.

## 7. Summary
- **Zero hard failures.**
- **Two numerical residuals** (Born 0.37–0.45 %, 1AKI 2 % grid gap),
  both expected and both explainable.
- **Three unexercised paper contributions** (TABI-PB, geoflow, Python
  API) recorded as scope gaps.
- **Four methodological caveats** (single-platform, no MD comparison,
  judge confirmatory, single-conformation).
- **Overall:** the REPLICATED verdict stands, but the scope of that
  verdict is the FD-multigrid solvation core of APBS. The paper's
  "improvements" narrative (new solvers, coupling, GPU/MD-adjacent
  workflows) is only partially covered.
