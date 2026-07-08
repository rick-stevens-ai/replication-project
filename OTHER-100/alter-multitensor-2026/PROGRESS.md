# PROGRESS — Alter et al. 2026 multitensor / NBL replication (method-side)

**Track:** Free, my-side, parallel to the author-data ask
(`draft-email-to-orly.md`). The point of this track is to have the
math + survival pipeline ready and verified, so that when Datasets 1–3
arrive we can immediately run the numeric replication.

**Workdir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/alter-multitensor-2026/`
**Python:** local venv `.venv/` (python 3.14.6, numpy 2.5.0, scipy 1.18.0,
lifelines 0.30.3). No system-python pollution.

---

## What's built

* `code/gsvd_reference.py`
  * `gsvd(D1, D2)` — Alter-Brown-Botstein / Van Loan GSVD via stacked QR
    + thin CS decomposition implemented elementarily on top of
    `scipy.linalg.svd` (we deliberately avoid `scipy.linalg.cossin`,
    which only accepts square inputs in scipy 1.18). Returns U1, U2,
    c, s, V with `D1 = U1 diag(c) V^T`, `D2 = U2 diag(s) V^T`, `c² + s² = 1`,
    V invertible (NOT orthonormal — this is the correct general-GSVD
    convention). Columns are sorted by ratio `c/s` ascending so the
    "first" column is most-exclusive-to-D2 and the "last" column is
    most-exclusive-to-D1, matching the paper's antisymmetric convention.
  * `ho_gsvd([D1, D2, ..., DN])` — Higher-order GSVD (Ponnapalli et al.
    2011, PLoS ONE) via eigendecomposition of the balanced average
    `S = (1/(N(N-1))) sum_{i<j} (A_i A_j^{-1} + A_j A_i^{-1})`,
    A_i = D_i^T D_i. Uses `eigh` on `(S + S^T)/2` when S is numerically
    symmetric (correctly handles the all-eigenvalues-equal-to-1 case)
    and `np.linalg.eig` otherwise. Returns U_i, Sigma_i, V, V^{-1},
    and the eigenvalues of S (Thm 2: all real, all ≥ 1).
  * `antisymmetric_patterns(result)` — returns `(k_first, k_last)`
    indices into the GSVD result that correspond to the paper's
    `u1,1` and `u1,101` patterns.
  * `classify_patients(arraylet)` — sign-based two-class patient
    classifier.
  * `combine_predictors(arraylet_first, arraylet_last)` — three-class
    "Tumor DNA 1+101" combined predictor (low / mid / high by joint
    sign).
* `code/test_gsvd.py` — 10 unit tests on synthetic data with known
  structure: reconstruction, c²+s²=1 invariant, U-orthonormality,
  planted-shared-subspace recovery (V columns parallel to the planted
  V_true up to sign), planted-antisymmetric-pattern recovery (the
  exclusive-to-D1 column is correctly identified and its patient
  classification matches the planted ±1 sign pattern ≥ 95%),
  HO-GSVD reconstruction on N=3, eigenvalue lower bound ≥ 1
  (Ponnapalli Thm 2), HO-GSVD recovers the common subspace when all
  matrices share the same Gram, HO-GSVD N=2 matches the classical GSVD
  by exact reconstruction.
* `code/survival_stats.py` — KM medians, log-rank (multi-group), Cox
  univariate (HR, 95% CI, Wald P), Harrell's C. Uses `lifelines` when
  installed (preferred), with SciPy fallback implementations of all
  four for environments without it. Aggregated `report()` dict returns
  everything needed to score against Table I.
* `code/fetch_target_nbl.md` — GDC + dbGaP data-acquisition recipe for
  TARGET-NBL WGS + RNA-Seq, with a per-row honest mapping of which of
  the paper's pre-processed profiles can be reconstructed from public
  sources and which cannot.

---

## Tests — actual output

`.venv/bin/python code/test_gsvd.py` (just re-run):

```
[PASS] gsvd_reconstruction_square
[PASS] gsvd_csq_invariant
[PASS] gsvd_U_orthonormal
[PASS] gsvd_planted_shared_subspace
[PASS] gsvd_antisymmetric_pattern_recovery
[PASS] combine_predictors_labels
[PASS] ho_gsvd_reconstruction_three
[PASS] ho_gsvd_eigenvalues_lower_bound
[PASS] ho_gsvd_recovers_common_subspace
[PASS] ho_gsvd_n2_matches_gsvd_subspace

10/10 tests passed
```

All reconstruction tests hit `< 1e-8`. The planted-subspace test
confirms |cos(V_recovered, V_planted)| = 1 - O(1e-15) per column. The
antisymmetric-pattern recovery test recovered the planted ±1 patient
sign pattern with 100% agreement (well above the 95% threshold).

`.venv/bin/python code/survival_stats.py` (synthetic two-group sanity
check, n=60, all events observed, mean survival 5.0 vs 1.5):

```
               label: synthetic_two_group
             n_total: 60
            n_events: 60
              groups: [(0, 30, 30, 3.777), (1, 30, 30, 1.119)]
        logrank_chi2: 19.4008
          logrank_df: 1
           logrank_p: 1.059610262479097e-05
              cox_hr: 3.8343
              cox_ci: (2.0392, 7.2096)
          cox_wald_p: 3.0214328364415298e-05
         concordance: 0.6271
              engine: lifelines
```

For sanity: the paper's combined-predictor target is HR 4.0, CI 2.0-8.1,
log-rank P 2.3e-5, C = 0.80. Our synthetic two-group sanity hit HR 3.83,
CI 2.04-7.21, log-rank P 1.06e-5 in roughly the same ballpark, which is
purely a wiring check — it does NOT claim replication. The concordance is
low (0.63) because the predictor is binary and noisy; the real predictor
is continuous, so a higher C is expected once we run on the actual data.

---

## What's blocked on author data

The **single biggest blocker** for numeric replication is the exact bin
coordinate set used for the 2,831,960 (tumor) and 2,831,959 (blood) 1-kb
WGS bins. Without that, we can't reproduce D1 / D2 in the paper's
feature ordering even from raw TARGET-NBL CG BAMs, so the GSVD's
`V[:, k]` arraylets will not numerically match `u1,1` / `u1,101` even if
the math is identical. The 10,354 / 10,475 validation-bin subset has the
same issue. **All three of these are inside Dataset 1 + Dataset 2 from
Orly, which she explicitly offers on request.**

Secondary blockers (less critical, mostly recomputable from public TARGET
data):

* The 71-patient × 15,393-transcript RNA-Seq whitelist (the
  transcript-filter threshold isn't stated).
* The mapping of the 90 patients used in Table I's full-label
  univariate-Cox row vs the full 101.
* Mathematica Notebook 1 — would give us the author's exact algorithm
  steps for the segmentation / CBS labeling of u1,k arraylets (Dataset
  3), which is needed for the genomic interpretation step but NOT for
  the survival-statistics replication.

Survival metadata (`days_to_death`, `days_to_last_follow_up`,
`vital_status`, INSS stage, age, MYCN amplification, COG risk, MKI,
ploidy, histopathology) is **fully public** through the GDC API for the
TARGET-NBL project — see `code/fetch_target_nbl.md` query (a). So the
"standard-of-care comparator" rows of Table I (MYCN, INSS, etc.) are
reconstructable today without any author data, given just the barcode
lists.

---

## Repo layout after this turn

```
alter-multitensor-2026/
├── PROGRESS.md                 (this file)
├── brief.md
├── draft-email-to-orly.md
├── paper-landing.html
├── source/                     (paper PDF lives here)
├── evidence/
├── .venv/                      (local scipy/numpy/lifelines)
└── code/
    ├── gsvd_reference.py       (GSVD + HO-GSVD + pattern selection)
    ├── test_gsvd.py            (10/10 passing)
    ├── survival_stats.py       (KM / log-rank / Cox / Harrell C)
    └── fetch_target_nbl.md     (GDC + dbGaP data-acquisition recipe)
```
