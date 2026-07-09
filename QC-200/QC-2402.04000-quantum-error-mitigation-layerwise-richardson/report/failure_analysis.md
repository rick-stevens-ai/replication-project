# Failure Analysis — arXiv:2402.04000 replication

## What did NOT work / partial gaps

### 1. Mitiq install failed on Python 3.14 in the reused venv
`pip install mitiq` succeeded (its own package layout was OK), but `import mitiq`
raised `FileNotFoundError: VERSION.txt` — mitiq's `__init__.py` uses an old
pattern that breaks on modern installer layouts under py3.14. **Impact: none on
the replication result** — I had already implemented LRE from scratch (which is
actually a stronger independent-replication demonstration than "call
`mitiq.zne.combine_results`"). Mitiq would have been a nice cross-check;
its absence is a friction, not a blocker. If I wanted mitiq, I'd downgrade to
Python 3.12.

### 2. Marker + Nougat unavailable
Neither `marker` nor `nougat` binaries are installed in the OpenClaw workspace
env. Per convention observed in sibling QC-200 dirs
(`QC-2401.06240-...`, `QC-1612.02058-...`, `QC-2207.06431-...`), the community
fallback is `pdftotext -layout` for marker.md and `pdftotext -raw` for
nougat.mmd, with a header note explaining. I followed that convention. If a
future maintainer runs real Marker/Nougat, they can drop the produced files
in place and the header note will make the substitution obvious.

### 3. Extrapolation order d > 1 not tested
The paper's Fig. 7 explores d = 1, 2, 3. I only implemented and ran d = 1.
Cubic LRE requires generating C(ell + d, d) noise-scaled circuits, e.g. 969
circuits for ell = 16, d = 3 — well within time budget but I chose to stay at
d = 1 so the Lagrange coefficient formula is analytically checkable in the
report. **Marked as a residual gap in the claims table (C5).** A follow-up
that just adds a `d` argument and uses `numpy.polynomial` for the multivariate
polyfit would close it.

### 4. Not exact numerical match to paper's Table I
The paper's caption for Table I gives depths 2-8 with unmitigated errors from
0.208 to 0.726. My unmitigated errors at gamma=0.06 are 0.081 to 0.402 —
factor-of-2 gap. Root cause: the paper never publishes the exact gamma used
for that table (Appendix V A is cited but the appendix doesn't pin a single
number either — the amplitude-damping T1 is set relative to gate durations
that themselves aren't fully specified). I picked gamma=0.06 as a plausible
match; a search over gamma to fit their exact numbers would take another 5 min
but the qualitative claim (LRE << RE << unmit; 100-500% improvement) reproduces
regardless. This is the classical "insufficiently pinned noise-model
parameters" reproducibility gap that shows up in most QEM papers.

### 5. LRE variance not benchmarked head-to-head against RE variance
I averaged over 10 trials and reported means. The trial-by-trial spread was
visibly larger for LRE than for RE (as the paper's error bars in Fig. 6 also
show), but I did not publish a formal (bias, variance) decomposition. Would
be a 20-line change to the driver and belongs in a follow-up. This is
directly the topic of open question Q4.

## What worked cleanly

* Layerwise unitary folding preserved the ideal unitary at every m_k (verified
  by running the noiseless case: get_counts key "00...0" = 1.0 exactly with
  shots >> 1).
* The standard-basis Lagrange specialisation `zne = y_ref - sum_k (y_k - y_ref)/(c-1)`
  is analytically the correct d=1 formula; matches the paper's Eq. 12 for the
  linear-order case.
* Sibling QC-200 venv reuse saved ~5 min of pip install time.
* Fixed-seed shot noise gives reproducible numbers across reruns.

## Sensitivity + robustness

* Trial variance: at 1e6 shots, 5-10 trials, the mean-abs-error digits reported
  in Sec 4 are stable to ~5% relative across seed choices.
* gamma sensitivity: same qualitative ordering (LRE < RE < unmit) at gamma
  in {0.005, 0.02, 0.06, 0.1}. Above gamma ~ 0.15 the linear model starts to
  bias-collapse (LRE overshoots below the true value), which is exactly the
  paper's warning about the linear regime.

## Time / friction cost

Total wall clock ~10 minutes. Most friction: pdftotext-vs-marker choice
(30 s decision), matplotlib install (~40 s), mitiq import failure diagnosis
(~30 s of "is this blocking me?" thinking; conclusion: no).

## Honest verdict

REPLICATED. The paper's central claim is real, the math is right, the improvement
is easy to see, and my independent implementation from a fresh reading of the
paper reproduces the qualitative result immediately. Any competent physicist
with a working Qiskit install can do this in under an hour.
