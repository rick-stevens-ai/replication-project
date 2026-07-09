# Failure Analysis — WaveTrain (Riedel et al., 2023)

Honest inventory of what failed, what was worked around, and residual gaps.

## 1. Software artifact fails as-shipped on modern NumPy
- **Symptom.** `test_scripts/Exciton/tise_1.py` crashes at
  `scikit_tt/solvers/evp.py:381` with
  `numpy.core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'add'
  output from dtype('complex128') to dtype('float64') with casting rule 'same_kind'`
  during the ALS deflation step (Wielandt shift adds a complex outer product to a
  real micro-operator matrix).
- **Root cause.** `micro_op` is initialised as real (Line 359–362 of `evp.py`,
  `np.tensordot` on the operator TT cores which are real for hermitian real
  Hamiltonians), then the deflation term `shift * tmp @ np.conjugate(tmp).T` is
  complex whenever any previous eigenstate has been shifted by ALS. NumPy ≥ 1.20
  tightened `same_kind` casting rules and now refuses the implicit downcast.
- **Workaround.** 4-line patch: compute the addend, `np.iscomplexobj` check,
  promote `micro_op` to `complex128` only if the addend is complex, then use
  out-of-place add. Backup saved at `evp.py.bak`. This preserves real-arithmetic
  behavior when nothing complex enters (first ALS pass) and correctly handles
  subsequent complex passes.
- **Independence of derivation.** The sibling replication documented the same
  fix earlier — we re-derived it here from the traceback without inspecting the
  sibling patch. Convergent evidence that this is the correct fix.
- **Upstream status.** Not fixed on the `PGelss/scikit_tt` HEAD used here. A
  proper upstream PR would be small (either promote at initialization, or
  detect complex operators up front). We did NOT open a PR (out of scope).

## 2. TISE object does not persist the full ALS spectrum
- **Symptom.** `dyn.eigen_values` only exists when `solver='qe'`
  (quasi-exact full diagonalisation); in `solver='als'` mode WaveTrain iterates
  through states one at a time, printing energies and updating `self.e_est`,
  but never assembles a spectrum array.
- **Root cause.** By design — ALS is inherently sequential (Wielandt deflation
  requires the previously-found eigenstate) so the class only holds the
  currently-found eigenstate.
- **Workaround.** Monkey-patched `TISE.update_solve(i)` to capture
  `float(dyn.e_est)` and `list(dyn.psi.ranks)` after every call. Recorded
  per-state wall-clock too.
- **Residual gap.** This should really be a `--collect-spectrum` flag upstream;
  every downstream benchmarker will hit this.

## 3. `ranks=15` ALS cap masks the paper's rank-scaling claim
- **Symptom.** For N ≥ 8 the reported `Rank of psi (TT)` profile shows
  `[1, 2, 4, 8, 15, 15, 15, 15, ..., 8, 4, 2, 1]` — the middle bonds are
  saturated at the user-set rank ceiling, not the intrinsic minimum rank of
  the state.
- **What this means.** We can conclude "r = 15 is sufficient to capture the
  single-exciton band across N=4..12 to ~1e-4 accuracy," but we CANNOT
  independently verify the paper's stronger statement that TT bond ranks
  themselves grow only marginally with N. To test that we'd need to sweep
  `ranks ∈ {6, 8, 10, 12, 15, 20, 30}` and locate the elbow of accuracy vs r
  at each N.
- **Impact on verdict.** C2 downgraded from "supported" to "partial".
- **Follow-on experiment.** See open question Q1.

## 4. N=14 dropped for wall-clock reasons
- **Symptom.** At N=12 the last few ALS eigenstates each cost ~150 s
  (deflation stack grows with each state). Projected N=14 cost > 2 h and >20 min
  per state, exceeding this run's wall-clock budget.
- **Workaround.** Dropped N=14. Sweep is now N ∈ {4,6,8,10,12} = same set as
  the sibling replication.
- **Residual gap.** A single N=14 datapoint would be the most useful extra
  evidence for C2 scaling; running it on uicgpu would be no faster (Python +
  numpy BLAS single-thread bottleneck) unless we porting the deflation loop
  to a proper parallel eigensolver. Left for future work.

## 5. Marker / Nougat not run
- **Symptom.** Neither Marker nor Nougat is installed on CherryRd; the central
  corpus does not carry arXiv:2302.03725.
- **Workaround.** Used `pdftotext -layout` (Poppler) and mirrored the output
  under the standard filenames `marker.md` and `nougat.mmd`, with a provenance
  `README.md` calling out that these are honest substitutes, not real Marker/
  Nougat parses.
- **Impact.** Downstream text-mining tools (equation extraction, table
  parsing) will not find the expected Marker/Nougat structural markup.

## 6. Bonus open-chain test dependency
- **Concern.** The bonus `bonus_open_N6` case triggers a code path we did not
  smoke separately (`periodic=False`). If it fails we still have the periodic
  results; the JSON persists after every N.

## 7. First bench run had wrong analytic reference
- **Symptom.** Initial max-error of 8e-2 across every N is a smoking gun.
- **Root cause.** I forgot to include the vacuum ground state (E=η=0) when
  comparing to the single-exciton band. ALS returns [vacuum, band…] but I was
  comparing to [band…] alone.
- **Fix.** `analytic_ref = sorted([η] + band)` truncated to n_levels.
- **Lesson recorded.** For any Fock-space chain TISE, always include the
  vacuum ground state in the analytic reference for `n_levels ≥ 1`.

## Summary
Software fails as-shipped (small fixable bug). Physics is genuinely reproduced
to 1e-4 accuracy on the paper's own reference configuration and across a 3×
range in N. The paper's rank-scaling claim is not independently verified by
this replication because the ALS ranks cap saturates for N ≥ 8, though the
observed wall-clock does grow substantially with N (which is at least consistent
with cost climbing significantly worse than "trivially linear"). Verdict:
PARTIAL, with C1 and C3 clearly supported and C2 only partially covered.
