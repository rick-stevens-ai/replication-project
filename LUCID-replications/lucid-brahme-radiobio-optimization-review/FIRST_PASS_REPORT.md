# FIRST PASS REPORT — Brahme 2024 (DOI 10.29011/2574-7754.101625)

LUCID100 max-rate backfill, Wave 6 / slot 60 (paper rank 91 in master TSV).

## Verdict
**NO_GO for a substantive replication.** The paper is a single-author review / perspective in a Gavin Publishers journal (*Annals of Case Reports*), with **no new data, no new experiments, no code, no supplementary, and no numerical tables**. All 38 figures are conceptual or replots of the author's prior publications (refs [1-3, 5-6, 19-21, 23, 34, 45, 51-55]). There is nothing in the paper that can be *replicated*; one could only *re-render* the author's own previously published figures, which would not constitute a meaningful validation.

A **smoke artifact is provided** that re-implements the only equation the paper writes down explicitly (Eq. (1), the complication-free-cure formula `P+ = PB − PI + δ(1 − PB) PI`) and qualitatively reproduces two textual claims the paper makes about it.

## Reproducibility audit
| Item | Available? | Notes |
|---|---|---|
| Methods section | No | No experimental or simulation methods. |
| Data availability statement | No | No data set deposited or linked. |
| Code availability | No | No code or repository. |
| Supplementary material | No | None linked. |
| Numeric tables | No | Only one tabular insert inside Figure 15 (γC, σD/D̄, RBE per modality), no parameter table. |
| New experimental result | No | Single illustrative IVPA PET-CT case (Fig 11) — no patient data shared. |
| Independently-named equations with parameters | **1** | Eq. (1) with δ ≈ 0.2. |
| Cell-survival model parameters (LQ / RCR / RHR) | No | Parameters live in cited Brahme refs [1-3, 23, 34, 45]. |
| Figures original vs replots | All replots / schematic | None original to this paper. |
| Predatory venue concern | **Yes** | Gavin Publishers / *Annals of Case Reports* widely flagged. |

## What was done
1. Located source row in `LUCID100_SOLID_MASTER_QA.tsv` (rank 91, Wave 6, tier B, score 13, status `candidate_curated`).
2. Created folder `lucid-brahme-radiobio-optimization-review/` under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/`.
3. Fetched OA PDF from Gavin Publishers; extracted text (`pdftotext -layout`).
4. Scanned all 38 figure captions and the equation lines; cataloged into `artifacts/MANIFEST.md`.
5. Decided **NO_GO for figure/table/dose-response replication**, but **GO for an Eq. (1) smoke** because the equation is unambiguously stated.
6. Implemented `smoke/p_plus_smoke.py` (numpy + matplotlib, <200 lines). Uses canonical Brahme/Källman Poisson-derived sigmoid for PB and PI, and Eq. (1) for P+ across δ ∈ {0, 0.2, 1}.
7. Ran it. Outputs in `figs/`:
   - `p_plus_smoke.png` — 4-panel: inputs, P+ vs δ, low-LET vs high-LET P+, peak P+ and optimum D* as a function of δ.
   - `p_plus_smoke.csv` — full dose grid for reuse.

## Smoke numerical results
- D50_T = 60 Gy, γ_C (low LET) = 3.0, γ_C (high LET) = 1.8
- D50_N = 70 Gy, γ_N = 4.0

| Scenario | Peak P+ | Optimum dose D* |
|---|---|---|
| δ = 0.0  (Brahme's "additive" caricature) | 0.503 | 62.9 Gy |
| δ = 0.2  (Brahme's clinical estimate)     | 0.512 | 63.1 Gy |
| δ = 1.0  (statistical independence)       | 0.554 | 63.9 Gy |
| δ = 0.2, low γ_C = 1.8 (high-LET penalty) | 0.474 | 61.4 Gy |

Interpretation, in the paper's own framing:
- The δ = 1 (statistically-independent) form *looks* better numerically because it reabsorbs the residual-injury term `(1 − PB) PI` as a bonus rather than a cost. Brahme explicitly calls this clinically over-optimistic and prefers δ ≈ 0.2 as the realistic regime. The smoke reproduces the *direction* of his Eq. (1) commentary (l. 693, l. 1028 of the manuscript text).
- Halving the tumor dose-response slope γ_C (mimicking the high-LET / microdosimetric-heterogeneity penalty he stresses in Figures 13–18) drops the peak P+ by ~3.8 percentage points and pulls the optimum dose down — qualitatively the photon-vs-neutron / carbon contrast he describes.

These are *qualitative* reproductions of the *formalism*. They do **not** validate any clinical claim, because no patient-level data are shared.

## Recommended QA retag
Move row 91 from `candidate_curated` to **`NO_GO_REVIEW_ONLY`** (or the project's equivalent disposition). Rationale:
1. Review/perspective paper with no new data, no methods, no code.
2. Predatory venue (Gavin Publishers, *Annals of Case Reports*) — replication value is low irrespective of content.
3. All claims are restatements of Brahme refs [1-3, 5-6, 19-21, 23, 34, 45, 51-55]; if any of those are in the LUCID100 master, the primary refs are the right targets.
4. The Eq. (1) smoke deliverable is preserved so the slot is not "wasted" — it documents the formalism and gives a reusable P+/TCP/NTCP toy for other LUCID slots.

## Blockers
- Internal `pdf` tool failed (Anthropic billing + Gemini name + OpenAI extract plugin all unavailable). Worked around with `pdftotext`; no upstream blocker for the task.

## Next actions
- None required for this paper. If another slot wants to replicate the *underlying* RHR / RCR survival model with actual data, the right entry points are Brahme refs [1-3, 23, 45]; identify them in the master TSV and consider promoting them.
- Optionally extend the P+ smoke into a tiny `lucid-utils` helper for any future LUCID slot that needs a quick TCP/NTCP/P+ check; the current `p_plus_smoke.py` is already standalone.
