# Image-Based Modeling Reveals Dynamic Redistribution of DNA Damage into Nuclear Sub-Domains

LUCID100 Wave 1 replication scoping brief — **slot 1** (parallel launch).

## Full citation

> Costes SV, Ponomarev A, Chen JL, Nguyen D, Cucinotta FA, Barcellos-Hoff MH (2007)
> Image-Based Modeling Reveals Dynamic Redistribution of DNA Damage into Nuclear
> Sub-Domains. **PLoS Computational Biology 3(8): e155.**
> doi:[10.1371/journal.pcbi.0030155](https://doi.org/10.1371/journal.pcbi.0030155)
>
> Affiliations: (1) Life Sciences Division, Lawrence Berkeley National Laboratory;
> (2) NASA Johnson Space Center; (3) Universities Space Research Association.
> Corresponding author: svcostes@lbl.gov.
> Funding: NASA grant T6275W, NASA Specialized Center for Research in Radiation Health Effects.
> License: Creative Commons Public Domain declaration.

LUCID100 master row: rank 32, Tier A, score 20, theme = DNA repair / DDR;
radiation quality / RBE; computational model / simulation. Worktype declared
as `simulation/model replication`. QA decision: KEEP.

## Source links

- Open-access PLOS Comp Biol article page:
  <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0030155>
- DOI landing: <https://doi.org/10.1371/journal.pcbi.0030155>
- LUCID local PDF copy: `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/562673694980c38e3d8d259f7bdc174125865bbe.pdf`
- Mirror inside this replication folder: `artifacts/paper.pdf`
  (sha256 `edcd8410573f9f6d50450207d1a8cadd77d851bb11684f92c501af0e865f4729`).

## Code / data / supplement availability

- **Code:** none released. The Methods section explicitly says
  "All image manipulation and analysis were done with Matlab (MathWorks) and
  DIPimage (image processing toolbox for Matlab, Delft University of Technology,
  The Netherlands)." No public repository (GitHub, SourceForge, Zenodo, lab
  page) is cited. Foci detection is described as
  "in-house image algorithm."
- **Supplementary files:** none. There is no Protocol S1, Table S1, Figure S1,
  Dataset S1, or Video S1 referenced in the paper. The PLOS article page also
  lists no supplementary downloads.
- **Microscopy data (RIF / DAPI):** not deposited. Cells are HMEC-184
  (Stampfer 1985) passage 7-10 and HeLa transfected with H1.2-GFP (Hendzel
  lab gift, Th'ng et al. 2005). Imaging at LBNL with a Zeiss Axiovert
  epifluorescence microscope + ORCA AG Hamamatsu camera at 0.16 µm/px.
- **Monte Carlo / PFGE inputs:** the "DSB-along-track" generator and the
  random-walk chromosome packing come from Ponomarev & Cucinotta 2006 (Radiat.
  Meas. 41:1075-1079) and earlier Sachs/Ponomarev refs [19-23]. These
  upstream codes were never publicly released either.
- **3-D rendering:** done in Bitplane Imaris (commercial; <http://www.bitplane.com/>).

Net result: this is a **closed-pipeline 2007 paper**. No artifacts have been
deposited in any public repository known to web search. The replication target
must therefore be a **methods reimplementation against the paper's mathematical
definitions**, not a bit-exact rerun.

## Target claims / figures

The central biological claim is that radiation-induced foci (RIF) for
γH2AX, ATMp, and 53BP1 do **not** spatially track the DNA-density-weighted
random distribution that DSB physics predicts. They preferentially occur in
**lower-DNA-density regions** and at the **interface between high- and
low-density regions** of the nucleus, within 5–30 min after exposure to
both high-LET (1 GeV/amu Fe, NSRL/BNL) and low-LET (¹³⁷Cs γ-rays) radiation.

Quantitative anchors that any replication should reproduce:

| # | Source | Quantity | Reported value |
|---|--------|----------|----------------|
| Table 1 | real | γH2AX RIF density along Fe track, 4.5 min post-IR | 0.69 ± 0.03 foci/µm |
| Table 1 | real | ATMp RIF density along Fe track, 4.5 min post-IR | 0.82 ± 0.05 foci/µm |
| Table 1 | real | 53BP1 RIF density along Fe track, 4.5 min post-IR | 0.76 ± 0.03 foci/µm |
| Table 1 | real | γH2AX RIF / nucleus, 1 Gy Cs, 30-60 min | 15.9 ± 0.5 |
| Table 1 | sim | DSB / nucleus, 1 Gy low-LET | 38.1 ± 5.9 |
| Table 1 | sim | pRIF / nucleus, 1 Gy low-LET | 37.0 ± 5.5 |
| Table 1 | sim | pRIF along Fe track | 0.73 ± 0.22 foci/µm |
| Table 2 | sim | R_dna for simulated pRIF (HZE) | 1.10 ± 0.10 |
| Table 2 | sim | R_grad for simulated pRIF (HZE) | 1.09 ± 0.26 |
| Table 2 | sim | R1/R2 (pRIF vs reshuffled pRIF) | 0.98 ± 0.07 (R_dna), 0.99 ± 0.26 (R_grad) |
| Table 3 | real | γH2AX R_dna measured / predicted, 4.5 min, low-LET | 0.98 ± 0.008 |
| Table 3 | real | γH2AX R_grad measured / predicted, 4.5 min, low-LET | 1.06 ± 0.003 |
| Fig 4 | real | correlation between measured & reshuffled distance distributions, 4.5 → 30 min | 0.6 → 0.45 |
| Fig 5 | real | same correlation across 4.5, 11.5, 31.5, 61.5 min, all markers | decreasing |
| Fig 9 | real | γH2AX–53BP1 co-localization, 1 GeV/amu Fe, 1-4 vs 5-10 min | 44 % → 64 %, p=0.01 |

Figures, from the paper:

- Fig 1 — synthetic vs real RIF images (Fe and Cs).
- Fig 2 — cartoon of along-track foci reshuffling Monte Carlo.
- Fig 3 — distance distribution between consecutive pRIF along simulated Fe tracks; pRIF vs DSB vs reshuffled.
- Fig 4 — measured γH2AX distance distribution at 4.5 and 35 min, vs reshuffled prediction.
- Fig 5 — correlation between measured and reshuffled distance distributions across time, all markers.
- Fig 6 — illustration of R_dna / R_grad on hand-placed foci (dense, edge, dim).
- Fig 7 — measured R_dna and R_grad across time for Fe exposure, all markers, with a 3-D rendering.
- Fig 8 — same for low-LET radiation, with orthogonal cross-section and 3-D rendering.
- Fig 9 — γH2AX–53BP1 and ATMp–53BP1 co-localization across time, both radiation qualities.
- Fig 10 — control: 5 Gy X-ray HeLa-H1.2-GFP, no global chromatin decondensation.

## Acceptance criteria

Because no artifacts were deposited, full bit-exact replication is impossible.
We define three replication tiers and the criteria for each:

**Tier 0 — methods sanity (this pass).** Independent Python reimplementation
of equations 3 and 4 (R_dna, R_grad) and the DNA-density-weighted Monte
Carlo reshuffle. On a synthetic nucleus with hand-placed foci:

- foci on dense DAPI ⇒ R_dna > 1, R_grad ≲ 1
- foci on DAPI edges ⇒ R_grad > 1
- foci on dim DAPI ⇒ R_dna < 1
- uniform-in-mask MC ⇒ R_dna ≈ 1, R_grad ≈ 1
- density-weighted MC ⇒ R_dna > 1, R_grad > 1 (because dense regions also have stronger gradients)

These are mathematical identities of the estimators; passing only confirms
the implementation is correct, not the biology. **This pass is complete and
passes — see `artifacts/smoke_results.json`.**

**Tier 1 — synthetic-data full pipeline.** Reimplement the
Ponomarev–Cucinotta DSB-along-track generator from refs [20, 22, 24] (random
walk of chromosomes, amorphous track structure for 1 GeV/amu Fe), apply
the 0.16 µm Gaussian PSF, run R_dna / R_grad and distance-distribution
analyses on ~200 synthetic nuclei. Targets: reproduce Table 1's pRIF
frequencies (0.73 foci/µm for Fe, ~37/nucleus for Cs) within 30 % and
Table 2's R values within 0.10. **Not started.**

**Tier 2 — real-data replication.** Requires access to the original
HMEC-184 imaging stacks, which are not public. Would need either author
contact (forbidden in this pass) or a sufficiently close substitute
dataset (e.g. RadFoci / BioImageXD tutorial data, the OpenAIRE-deposited
Costes-lab successor datasets). **Out of scope for this pass.**

## Artifact harvest checklist

- [x] Source PDF saved locally and hashed (`artifacts/paper.pdf`).
- [x] Full text extracted (`text/paper.txt`).
- [x] PLOS article landing page checked for supplementary files — none found.
- [x] Code repository searched — none cited in the paper, web search blocked
      by bot-detection at search time (DuckDuckGo bot-check); paper itself
      lists Matlab + DIPimage only and no public release.
- [x] Public data accession searched — none cited.
- [x] Environment plan: pure-Python smoke uses numpy / scipy / matplotlib only.
      Tier 1 would additionally use scikit-image; Tier 2 also Bio-Formats /
      python-bioformats. No CUDA needed. CherryRd CPU-only is sufficient.
- [x] Acceptance metrics defined (see above).
- [x] Blockers listed: see `FIRST_PASS_REPORT.md` and `PROGRESS.md`.

## Execution checklist

- [x] Smoke test / minimal calculation (`code/rdna_rgrad_smoke.py`, runs in seconds).
- [ ] Tier 1 synthetic-pipeline run (deferred — needs reimplementation of
      Ponomarev–Cucinotta track / random-walk chromosome model).
- [ ] Tier 2 real-data run (blocked — no public microscopy data).
- [x] Figures regenerated for the Tier-0 demo (`figs/`).
- [x] Logs, hashes, environment captured (`artifacts/manifest.json`).
- [x] `FIRST_PASS_REPORT.md` written.
- [x] Progress JSON updated under OpenClaw memory.

## Files

- `artifacts/paper.pdf` — local mirror of the PLOS paper.
- `artifacts/manifest.json` — file-level manifest with sha256 hashes.
- `artifacts/smoke_results.json` — numeric outputs of the Tier-0 demo.
- `text/paper.txt` — pdftotext extraction used for grep/quote.
- `code/rdna_rgrad_smoke.py` — Tier-0 reimplementation: R_dna, R_grad,
  density-weighted Monte Carlo reshuffle, Figure 6 cartoon, Figure 3-style
  distance histogram. Pure Python 3, no GPU, ~1 second wall time on CherryRd.
- `figs/fig6_cartoon.png` — Fig 6-style demo: dense / edge / dim foci on a synthetic nucleus.
- `figs/fig3_style_distance_hist.png` — Fig 3-style along-track distance histogram.
- `figs/mc_reshuffle_box.png` — Monte Carlo control: density-weighted vs uniform reshuffle.
- `FIRST_PASS_REPORT.md` — verdict + evidence.
- `PROGRESS.md` — running log.

## Initial abstract / notes

Several proteins involved in the response to DNA double-strand breaks (DSB)
form microscopically visible nuclear domains (foci) after ionizing radiation.
RIF are believed to mark DSB locations. The authors compared the spatial
distribution of 53BP1, ATMp, and γH2AX RIF in cells irradiated with high-LET
(1 GeV/amu Fe) and low-LET (¹³⁷Cs γ-rays) radiation. Monte Carlo simulations
of DSB in synthetic nuclei (geometrically described by a complete set of human
chromosomes) produced the expected DNA-weighted random / Poisson distributions.
Real RIF distributions deviated from this prediction within 5 min after
exposure, preferentially locating at the interface between high- and low-DNA
density regions. The deviation was strong for γH2AX and 53BP1 up to 30 min,
and only present at 5 min for ATMp. The authors interpret this as evidence
for "repair centers" in mammalian cells.
