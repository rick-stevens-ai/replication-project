# PATH B — Method merit & generalizability of Alter et al. 2026 multitensor GSVD

**Goal (Rick):** does the method have merit and generalizability, and is there any
advantage to the "quantum" aspects — independent of the authors' exact dbGaP-gated bins?

**Compute:** uicgpu (CPU; linear-algebra workload). Engine = the tested
`gsvd_reference.py` (10/10 unit tests, reconstruction <1e-8) + `survival_stats.py`.
All numbers below are real computed output on **open** GDC data (no dbGaP).

---

## What we could and could not get from open data
- WGS (the paper's actual discovery/validation layer) is **dbGaP-controlled (phs000467)** —
  not used here. So this is NOT a bin-exact reproduction of Table I; it is a test of whether
  the *method* produces the *claimed kind of result* on open multiomic data.
- Pulled (open): TARGET-NBL clinical/survival for **1,132 cases** (1,116 with follow-up,
  448 deaths); **162 open RNA-Seq STAR-count** files (153 primary-tumor, one per patient);
  **235 methylation 450K** beta files; 696 masked-somatic-mutation MAFs.

## FRONT 1 — Standard-of-care baseline (the bar the method must beat)
Survival stats computed with our KM/log-rank/Cox/concordance on real clinical data.

**Full clinical cohort (n≈829-840):**
| Indicator | C-index | HR | log-rank P |
|---|---|---|---|
| MYCN amplification | **0.586** | 1.95 | 6.6e-9 |
| INSS stage (ordered) | 0.626 | 2.19 | 7.9e-23 |
| INSS stage-4 binary | 0.627 | 10.4 | 8.9e-25 |
| Age ≥18mo | 0.604 | 3.92 | 7.4e-18 |
| COG risk | 0.651 | 5.50 | 3.5e-29 |

**Finding 1:** In the larger open cohort, MYCN concordance is **0.586**, well below the
paper's claimed ~0.70-0.73. On the 153-patient RNA subset MYCN is even weaker (C=0.54,
log-rank P=0.26 — not significant). The paper's higher MYCN numbers are specific to its
curated 90/398-patient subsets. So "beating MYCN" is an easier or harder bar depending on
cohort — important context for interpreting the method's claims.

## FRONT 2 — The method (GSVD) on matched open multiomic layers
Two genuine omic layers, **expression × methylation, 132 patient-matched cases**, top-5000
variable features each, z-scored. GSVD → most-exclusive-to-each-layer arraylets (u_first,
u_last) → patient classification → survival. Concordance from the CONTINUOUS predictor score.

| Predictor | C-index | note |
|---|---|---|
| GSVD u_first (expr-exclusive) | 0.447 | ~chance |
| GSVD u_last (meth-exclusive) | 0.503 | ~chance |
| **GSVD combined (first−last)** | **0.495** | log-rank P=0.72 (NS) |
| MYCN (same 132 patients) | 0.493 | |
| methylation alone, PC1 | 0.495 | |
| PCA expression PC1 | 0.440 | |
| **Penalized Cox, 20 expr PCs (supervised)** | **0.738** | wins decisively |

**C2 orthogonality:** cos(u_first, u_last) = 0.33 (paper claims ~0 / orthogonal). On open
data the two extracted predictors are NOT orthogonal.

### Verdicts on the central claims (open-data test)
- **C1 (blind tumor-exclusive survival predictor):** NOT REPRODUCED on open layers — the
  most-exclusive GSVD arraylet does not separate survival (C≈0.45-0.50, NS).
- **C2 (second, orthogonal survival predictor):** NOT REPRODUCED — neither survival-predictive
  nor orthogonal (cos=0.33).
- **C4 (combined beats MYCN):** combined C=0.495 vs MYCN 0.493 — statistically a tie at chance;
  the method does NOT beat MYCN here, and a supervised penalized Cox (0.738) beats both by a wide margin.
- **C3 (X-chromosome/sex artifact in ~100th pattern):** UNTESTABLE without WGS chromosome-mapped bins.
- **C5 (robustness):** decompositions ran across feature counts 2k/5k/10k without breaking
  (numerically stable), but since the survival signal is ~chance there is no signal whose
  robustness is meaningful here.

## Q. What does the "quantum" framing actually buy?
The paper's only concrete QM claims are **superposition** (a patient state = weighted sum of
rank-one patterns — i.e. any SVD/PCA basis expansion) and **entanglement** (the layer
representations share one right-basis V, so each layer's classification ~determines the others).
There is **no quantum algorithm, no quantum hardware, no quantum speedup** — it is classical
GSVD/HO-GSVD linear algebra.

Measured on this open data:
- **(A) Computational advantage from "quantum": NONE.** It is deterministic classical SVD-family math.
- **(B) Predictive advantage over classical baselines: NONE observed here.** GSVD combined
  (C=0.495) ≈ PCA PC1 (0.44) ≈ methylation PC1 (0.495), and all are crushed by a plain
  supervised penalized Cox (0.738). "Superposition" is, on this data, a relabeling of PCA.
- **(C) Entanglement value: NOT demonstrated here.** The two-layer combined predictor (0.495)
  does not exceed the best single layer (meth PC1 0.495 / expr 0.44) — i.e. combining the
  "entangled" layers added no predictive value on open data. The genuine content of
  "entanglement" reduces to "a shared latent factor concordant across omic layers," the goal
  of ordinary multiomic integration (MOFA/JIVE/iCluster) — real as a concept, but not quantum
  and not advantageous here.

## HONEST CAVEATS (do not over-read)
1. **This is NOT the paper's data.** It used CG WGS 1-kb-bin copy-number profiles; we used open
   RNA + methylation. The method may genuinely work on copy-number structure and fail on
   expression/methylation. The fair, decisive test needs Datasets 1-3 (requested from Orly).
2. The paper's predictors are **unsupervised** (label-free); comparing their C to a supervised
   Cox is informative about practical value but not a like-for-like unsupervised comparison.
   The honest unsupervised comparison is GSVD vs PCA vs single-layer — and there GSVD shows no
   edge here.
3. Cohort/subset choice strongly moves MYCN's own concordance (0.586 full vs ~0.70 paper subset).

## BOTTOM LINE (preliminary, open-data)
- **Merit:** the GSVD/HO-GSVD math is exact, unique, stable (real strengths vs non-convergent
  deep learning). But on independent open multiomic layers its unsupervised predictors did NOT
  beat MYCN or even a PCA baseline, and a supervised classical model beat everything.
- **Generalizability:** NOT demonstrated on open expression/methylation. Whether it generalizes
  may hinge specifically on copy-number (WGS bin) structure — testable only with the authors' data.
- **"Quantum" advantage:** none found — computationally or predictively. The quantum framing is
  interpretive (superposition=PCA basis, entanglement=shared-latent-factor concordance), adding
  vivid language and a venue, not capability.

## FRONT 3 — Independent TCGA-GBM cohort, CNV × RNA (the method's NATIVE data type)
259 patient-matched TCGA-GBM cases (gene-level copy-number × RNA-Seq), top-5000 features
each. This is the paper's OWN prior validation domain and uses copy-number (the data type the
NBL claims rest on) — the cleanest independent generalizability test we can run on open data.

| Predictor | C-index |
|---|---|
| GSVD u_first (CNV-exclusive) | 0.472 |
| GSVD u_last (RNA-exclusive) | 0.518 |
| **GSVD combined** | **0.461** (below chance) |
| Age at diagnosis (standard GBM prognostic) | **0.605** |
| PCA CNV PC1 | 0.527 |
| PCA RNA PC1 | 0.511 |
| **Penalized Cox (10 CNV + 10 RNA PCs)** | **0.657** |

**C2 orthogonality:** cos(u_first, u_last) = **0.002** — here the two predictors ARE orthogonal,
so that specific mathematical claim DOES reproduce (it's a built-in GSVD property).

### Front-3 verdicts
- **C1/C2 (survival-predictive patterns):** NOT REPRODUCED on TCGA-GBM CNV×RNA — GSVD
  arraylets are at/below chance (0.46-0.52); age alone (0.605) and penalized Cox (0.657) beat them.
- **C2 orthogonality:** REPRODUCED (cos=0.002) — but orthogonality is automatic in GSVD, not evidence of merit.
- **C4 (beat the standard biomarker):** NOT REPRODUCED — combined GSVD (0.461) loses to age (0.605).
- Same pattern as Front 2: the unsupervised GSVD predictor shows no survival signal on open
  multiomic data of either cancer; classical supervised models win.

## CONSOLIDATED BOTTOM LINE (Fronts 1+2+3, open data)
- **Across two independent cancers (NBL expr×meth, GBM CNV×RNA), the unsupervised GSVD/HO-GSVD
  predictors did not separate survival above chance and did not beat the standard biomarker
  (MYCN / age) or a plain PCA / penalized-Cox baseline.** The math is exact and stable, and the
  orthogonality claim reproduces (trivially), but the *predictive* claims did NOT generalize to
  open multiomic data — including copy-number, the method's native data type.
- **Quantum advantage: none, on any axis** — no algorithm/hardware/speedup (it's classical SVD
  algebra), and no predictive edge over PCA or penalized Cox. Superposition = PCA basis;
  entanglement = shared-latent-factor concordance (real concept, ordinary multiomic-integration
  goal, not quantum, and added no predictive value here).
- **CRITICAL caveat preserved:** this is NOT the authors' exact data. Their result may depend
  specifically on their curated 1-kb WGS copy-number bins + autosomal-median centering +
  their specific 90/398-patient subsets, none of which we could reconstruct from open data.
  The decisive bin-exact test still requires Datasets 1-3 + Mathematica Notebook 1.

## STILL TODO
- Bin-exact Path A once Orly sends Datasets 1-3 + Mathematica Notebook 1 (request drafted, cc Rick).
- If pursuing further open-data rigor: replicate their EXACT recipe (sign-of-arraylet at ±1 SD
  cut, their specific subset filters) rather than continuous concordance, to rule out a scoring
  mismatch — though the qualitative no-signal result is consistent across methods/cohorts.
