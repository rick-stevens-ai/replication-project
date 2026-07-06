# First-pass replication report — Costes et al. 2007 (PCBI e155)

**Paper:** Costes SV, Ponomarev A, Chen JL, Nguyen D, Cucinotta FA,
Barcellos-Hoff MH (2007) *Image-Based Modeling Reveals Dynamic
Redistribution of DNA Damage into Nuclear Sub-Domains*.
PLoS Computational Biology 3(8): e155.
doi:[10.1371/journal.pcbi.0030155](https://doi.org/10.1371/journal.pcbi.0030155)

**LUCID100 slot:** Wave 1, slot 1 (rank 32, Tier A, score 20).

**Verdict:** **PARTIAL-SCOPE / methods sanity reproduced — full
quantitative replication NO-GO from artifacts alone.**

## TL;DR

- The paper deposited **no code, no data, and no supplementary
  files**. The pipeline is a closed Matlab + DIPimage in-house
  implementation, layered on top of the upstream Ponomarev–Cucinotta
  NASA HZE-track / random-walk chromosome model (refs 18-24), which
  was also never publicly released.
- The *mathematical* core of the paper — equations (3), (4), and the
  DNA-density-weighted Monte Carlo reshuffle in (1)-(2) — is fully
  specified and small. I reimplemented all of it from scratch in
  ~300 lines of NumPy and verified that the four behaviour
  signatures the paper relies on (dense ⇒ R_dna > 1, edge ⇒
  R_grad > 1, dim ⇒ R_dna < 1, uniform-in-mask MC ⇒ R ≈ 1)
  all hold on a synthetic nucleus.
- That is enough to **declare the estimators correctly understood
  and re-implemented**. It is *not* enough to reproduce any of the
  biological claims (Tables 1-3, Figures 4-9), which require either
  the closed HMEC-184 microscopy dataset (not public) or a
  reimplementation of the Ponomarev–Cucinotta DSB-track model
  (5-10 days of focused work, deferred).

## What was looked for

| Artifact class | Searched where | Outcome |
|---|---|---|
| Public code repo | paper text (grep `github|sourceforge|repository|download|http|software|website`); PLOS article landing page; web search | **none**; web search blocked by DuckDuckGo bot-check, but paper text only names Matlab + DIPimage + "in-house image algorithm" |
| Supplementary files (PLOS) | paper text (grep `Protocol S|Figure S|Table S|Dataset S|Video S|supplement`); PLOS landing page | **none referenced**; PLOS landing page lists no supplementary downloads |
| Microscopy raw data | Methods section | **not deposited** — HMEC-184 + HeLa-H1.2-GFP, in-house Zeiss + Hamamatsu |
| PFGE / HZE-track inputs | refs [18-24] | **not deposited** — Ponomarev–Cucinotta NASA-internal codes, only their fit parameters / formulae are in the cited Math Biosci, Radiat Res, Int J Radiat Biol papers |
| 3-D rendering | Methods section | commercial Bitplane Imaris |

## What was built (Tier-0)

`code/rdna_rgrad_smoke.py` (pure Python 3, numpy + matplotlib only):

1. `synthetic_nucleus()` — circular DAPI cartoon: smooth euchromatin
   background + N random Gaussian heterochromatin blobs. Not the
   Ponomarev random-walk model; deliberately simple, to exercise
   the estimators only.
2. `r_dna(dna, foci, mask)` — Eq. (3) of Costes 2007.
3. `r_grad(dna, foci, mask)` — Eq. (4), with conservative inner
   mask (3-px erosion) matching the paper's 0.48 µm inward contour.
4. `reshuffle_foci(dna, mask, n)` — Eqs. (1)-(2): sample n pixel
   locations with probability proportional to DAPI density.
5. `pick_topk_pixels` — hand-place foci on densest, sharpest-edge,
   and dimmest pixels to reproduce Fig 6's three cases.
6. `along_track_distances` — Fig 3-style 1-D distance histogram
   along a horizontal line through the synthetic nucleus.

Runtime: ~1 second on CherryRd. No GPU, no paid endpoints.

## Sanity results (Tier-0 acceptance criteria)

From `artifacts/smoke_results.json` (RNG seed 20260609):

| Expected behaviour | Measured value | Pass? |
|---|---:|---|
| foci on dense DAPI ⇒ R_dna > 1 | **5.03** | ✅ |
| foci on dense DAPI ⇒ R_grad ≲ R_dna | 3.44 < 5.03 | ✅ |
| foci on DAPI edges ⇒ R_grad > 1 | **5.46** | ✅ |
| foci on dim DAPI ⇒ R_dna < 1 | **0.26** | ✅ |
| MC uniform-in-mask ⇒ R_dna ≈ 1 | **1.02 ± 0.18** | ✅ |
| MC uniform-in-mask ⇒ R_grad ≈ 1 | **1.02 ± 0.23** | ✅ |
| MC density-weighted ⇒ R_dna > 1 | **2.30 ± 0.36** | ✅ |
| MC density-weighted ⇒ R_grad > 1 | **2.21 ± 0.27** | ✅ |
| Along-track distance histogram is right-skewed (Poisson-like) | mean 9.55 px, median 4 px, n=3400 | ✅ qualitatively (see `figs/fig3_style_distance_hist.png`) |

The paper's Table 2 reports R_dna = 1.10 ± 0.10 and R_grad = 1.09 ±
0.26 for simulated pRIF on their nuclei. Our 2.3 / 2.2 are larger
because our synthetic DAPI blobs have much higher dynamic range than
real DAPI (we did not match the Ponomarev random-walk packing
contrast). What matters is the **sign and the > 1 inequality**, which
matches; quantitative matching is a Tier-1 task.

## What this pass does NOT do

- Does NOT validate any biological claim. The conclusion "RIF
  concentrate at chromatin interfaces" depends on **real** RIF
  images, which are not available.
- Does NOT reproduce Table 1, 2, or 3 numerically.
- Does NOT reproduce the kinetic curves in Figures 4, 5, 7, 8.
- Does NOT reproduce co-localization analysis (Figure 9).
- Does NOT implement the Ponomarev–Cucinotta random-walk chromosome
  packing or the 1 GeV/amu Fe amorphous-track DSB generator. Those
  are needed for Tier-1.

## Blockers

1. **Data:** HMEC-184 and HeLa-H1.2-GFP imaging stacks are not in
   any public repository. Author contact is forbidden in this pass.
2. **Upstream code:** the NASA HZE-track and random-walk chromosome
   model from Ponomarev & Cucinotta 2006 (refs 22, 24) is not
   publicly released. It would need to be reimplemented from the
   formulae in those papers (Math Biosci 159 (1999) 165, Int J
   Radiat Biol 82 (2006) 293, Radiat Meas 41 (2006) 1075). Doable
   but multi-day.
3. **Search:** DuckDuckGo bot-detection blocked the web search step
   that would otherwise have looked for a Costes-lab successor
   release (e.g. RadFoci / BioImageXD); the in-paper text contains
   no such pointer and the PLOS article page lists no supplementary
   files, so this is unlikely to change the verdict.
4. **Compute:** none. Smoke runs in ~1 s. Tier-1 would still fit on
   CherryRd CPU. No GPU job plan needed.

## Recommendation

- File this paper as **partial-scope reproduced (methods sanity)** in
  the LUCID100 ledger.
- If a future slot wants to push to Tier-1, the unit of work is
  "reimplement Ponomarev–Cucinotta 2006 random-walk chromosome
  packing + amorphous Fe-track DSB sampler in Python; drive
  `rdna_rgrad_smoke.py`'s estimators against the result; aim to
  reproduce Table 2 within ±0.10 and Table 1 frequencies within
  ±30 %."
- Do **not** attempt Tier-2 (real-data) without a public
  substitute dataset; do not contact the authors.

## Evidence (paths)

- `artifacts/paper.pdf`  (sha256 `edcd8410573f9f6d50450207d1a8cadd77d851bb11684f92c501af0e865f4729`)
- `artifacts/manifest.json`
- `artifacts/smoke_results.json`
- `code/rdna_rgrad_smoke.py`
- `figs/fig6_cartoon.png`
- `figs/fig3_style_distance_hist.png`
- `figs/mc_reshuffle_box.png`
- `text/paper.txt`
- `README.md`
- `PROGRESS.md`

— Ollie, subagent slot 1, 2026-06-09 12:55 CDT.
