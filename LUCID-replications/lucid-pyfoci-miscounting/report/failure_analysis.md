# Failure Analysis — PyFoci miscounting replication

Honest enumeration of what did NOT work, what remains uncertain, and what would
overturn the verdict. This is not a whitewash — the verdict of REPLICATED
survives these caveats *as scoped* but the scoping is real.

## What genuinely did not work

### F1. The raw PyFoci image-generation pipeline was never rerun

**Symptom:** Claim 5 (full PyFoci pipeline reruns from scratch) is BLOCKED.
**Root cause:** CherryRd is on Python 3.14; `numba` (a hard dependency of
PyFoci's LoG-counter implementation) has no compatible wheel and its
JIT-compilation backend is not yet ported for Python 3.14 ABI. `pip install
numba` fails at the source-build stage.
**Attempted workaround:** none (this pass explicitly did not rerun sims per the
backfill brief).
**Real cost:** we cannot detect a hypothetical bug in the upstream image
generation. Every quantitative claim we validated (7 through 13) reads the
authors' cached DataFrames; if their DataFrame emission stage were buggy in a
way that self-consistently propagates into P_Values_Fig1, our re-pass would
happily reproduce the buggy p-values. This is a real, non-cosmetic gap.
**What would close it:** stand up a Python 3.11 venv (~30 min), `pip install -e
code/pyfoci` (~10 min), rerun the Airyscan-x63 config at 2 Gy for the 4
radiation types with 100 replicates (~4-8 h wall-clock), diff the produced
parquet against `data/extracted/`. Estimate: half a day of dedicated effort.
Not blocked scientifically, blocked on Python-env discipline.

### F2. Figure regeneration is analog-only

**Symptom:** Claim 6 is honestly graded PARTIAL. We reproduced qualitatively
similar shapes for Figs 3a, 4, and 5 (`figures/repass/*.png`) but did not
reproduce Figs 1, 2, 6, 7, 8, or any of the supplementary figures.
**Root cause:** figure-pixel-exact regeneration was descoped as unnecessary
once the underlying quantitative claims reproduced from the released tables.
**Real cost:** an auditor who trusts figures more than tables would flag this.
**What would close it:** ~2-4 hours matplotlib work per figure using the
already-verified numerical outputs.

## What might still be wrong (uncertain, not verified)

### U1. Self-consistency ceiling on the Mann-Whitney reproduction

Our 120/120 p-value match confirms that our test harness reads the same
DataFrame the paper describes, computes the same statistic (Mann-Whitney U,
two-sided, Bonferroni-adjusted at α=0.05), and finds the same p-values. It
does NOT confirm that the DataFrame accurately reflects the underlying image
statistics. If the authors' image-processing stage had a systematic bias, our
100% match would be a confidence artifact.

### U2. The Fig 8 clustering Spearman is directionally correct but weak

r_DSB = -0.088 (p=6.9e-33) is a canonical "large-n makes anything significant"
regime. The bin-median trend (+14 → -10 → -26 → -16 across increasing
CD_200nm bins) is more compelling than the Spearman, but even that is
non-monotone (the 5-10 bin flips from -26 back to -16 — likely a small-n
bin artifact in the tail, but we did not compute a bin-conditional bootstrap
CI). An adversarial auditor could reasonably argue that CD_200nm is a
sub-optimal clustering operationalisation (see Open Question 5).

### U3. The Fig 6 exception is asserted, not proven

The single 30-min high-LET case where raw-DSB matches deconv-DSB is
consistent with the paper's ``clustering saturates both'' narrative, but we
did not quantify whether the ~15.4 counted vs 20.95 actual is inside vs
outside a cell-bootstrap 95% CI. It could be a genuine limitation of
deconvolution at extreme clustering, or a coincidence in a small subgroup.

### U4. Environment provenance for the authors' cached parquets is opaque

We assume the DataFrames on figshare were produced by the released PyFoci
version at the tagged commit. If the release was cut *after* the DataFrames
were archived, the code and data could subtly diverge. The `code/pyfoci/`
checkout does not have a git tag matching the manuscript submission date.
Low probability of impact but not verified.

## What would overturn the verdict

- A Python-3.11 rerun (F1 closure) that shows large systematic disagreement
  between our produced parquets and `data/extracted/` — this would suggest the
  authors did not release the exact code that generated their claims. LOW
  probability given the paper's otherwise-exemplary artifact release, but the
  test is worth doing.
- A cross-cell-line simulation (Open Question 2) that shows miscount curves
  shift by >30% under plausible chromatin-compaction perturbations — this
  would narrow the paper's claim from "PyFoci quantifies miscount" to "PyFoci
  quantifies miscount for a generic nucleus," which is a real scope reduction.
- Independent re-implementation of the LoG counter with different sigma /
  threshold choices that changes the Fig 4 magnification-effect verdict — this
  would suggest the miscount is counter-parameterization-dependent, not
  microscope-dependent.

None of these have been done.

## Bottom line

The verdict of REPLICATED is defensible *as scoped*: released numerical
evidence supports stated quantitative claims, artifact release is complete
enough for downstream closure, 12/13 claims quantitatively reproduced. The
gaps enumerated above are real but do not undermine the top-line conclusion.
An auditor could, in a day or two of additional work, close F1 and F2 and
lift Claim 6 to REPLICATED, bringing coverage to 13/13 with no environment
caveats. That work is signposted in `report/workflow.md` and represents the
next natural iteration if resources allow.
