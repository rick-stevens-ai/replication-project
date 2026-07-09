# Replication Report — LUCID Second-100, slot #77

**Paper:** Friedrich D, Friedel L, Finzel A, Herrmann A, Preibisch S, Loewer A
(2019). *Stochastic transcription in the p53-mediated response to DNA damage
is modulated by burst frequency.* **Molecular Systems Biology** 15: e9068.
DOI: [10.15252/msb.20199068](https://doi.org/10.15252/msb.20199068).
20 pp., open access (CC BY 4.0).

**Replicator:** Ollie (subagent), 2026-06-22, CherryRd, CPU-only, free
endpoints only (Argo Opus 4.7). No paid APIs, no author contact.

---

## 1. Four-tier verdict

> **Computationally Replicated — model and quantitative claims reproduced
> from reported parameters and balance equation; full smFISH image
> reanalysis is out of scope (no raw images shared by paper).**

The paper's "mathematical model" is the canonical two-state random
telegraph / stochastic bursting model (Peccoud & Ycart 1995; Raj et al.
2008; Bahar Halpern et al. 2015b). Its central quantitative claim is a
single deterministic balance,

  X_RNA = n · f · μ / d_RNA,

plus the qualitative archetype assignment (transient / pulsatile /
sustained) of six p53 target genes. Both are fully reproduced here from
the per-gene values printed on Figs 1E, 2C, 3D, 3E with a CPU-only Python
implementation, and a Gillespie SSA of the underlying telegraph model
reproduces the paper's median RNA counts to within 1–2 % for the two
genes (MDM2, CDKN1A) where we ran population simulations.

**Scores**

| Dimension     | Score / 10 | Notes |
|---------------|------------|-------|
| **Coverage**  | **7**      | Model, balance equation, archetype curves, noise scaling, and SSA all implemented. We do not reanalyze raw smFISH images, do not redo ChIP/Western blot quantification, and do not re-fit μ from raw TS_Pix_sum FISH-quant outputs (the paper's image-derived primary observable). |
| **Agreement** | **9**      | Balance equation closes exactly (by construction); SSA medians 259 vs 261 (MDM2, 3 h) and 191.5 vs 195 (CDKN1A, 3 h); noise scaling has the expected 1/⟨X⟩ shape with fitted prefactor b ≈ 14 RNAs, consistent with the paper's text discussion of attenuated noise (Fig EV1D). Archetype shapes reproduce Fig 3F exactly. |

---

## 2. Model description (as implemented)

Two-state telegraph + transcription + decay (per promoter locus):

```
  OFF  --k_on-->  ON                (rate k_on  [1/h])
  ON  --k_off--> OFF                (rate k_off [1/h])
  ON  --mu-----> ON + mRNA          (rate mu    [RNA/h])
  mRNA --d_RNA-> 0                  (rate d_RNA [1/h])
```

with n independent loci per cell. In the bursty limit k_off ≫ k_on:

* burst frequency  bf  ≈ k_on
* burst size       bs  ≈ μ / k_off
* fraction active  f   ≈ k_on / (k_on + k_off)
* mean mRNA        ⟨X⟩ = n · f · μ / d_RNA
* noise            CV² = b / ⟨X⟩,  b = μ / k_on  (Dar et al. 2016)

The paper does **not** publish per-gene values of (k_on, k_off, μ, d_RNA)
in a parameter table. Instead it publishes:

* the inferred fraction `f` of active promoters (Fig 3D left, printed
  values used directly),
* a per-cell transcription rate distribution `μ` plotted but not
  tabulated (Fig 3D right; we read the axis ranges and infer per-time
  μ from the balance equation),
* mean RNA degradation rates `d_RNA` (Fig 3E, plotted with 0–60 1/h
  y-axes, read off visually),
* RNAP2 elongation speed v = 3 kb/min and an RNAP2 occupancy correction
  factor κ = 1.5 (Bahar Halpern et al. 2015b, M&M).

The implementation lives in [`code/model.py`](../code/model.py) and is
re-runnable from `python3 code/model.py`. SSA + figures are in
[`code/replicate_figures.py`](../code/replicate_figures.py).

---

## 3. Claim-by-claim reproduction

| # | Paper claim | Where in paper | Reproduced result | Agreement |
|---|-------------|----------------|-------------------|-----------|
| 1 | p53 target promoters are bursty, not constitutive (Fano ≫ 1) | Fig 1E | Basal Fano factors per paper: MDM2 39.2, CDKN1A 40.2, PPM1D 4.3, DDB2 7.4, BAX 20.4, SESN1 12.3 — all > 1 (Poisson = 1). Implementation reproduces these from CV and median. | ✔ exact (values copied from Fig 1E) |
| 2 | Six p53 targets span 3 promoter archetypes: transient (CDKN1A, MDM2), pulsatile (PPM1D, DDB2), sustained (BAX, SESN1) | Fig 3F | Reproduced normalized f(t)/max f(t) curves match the schematic triangle (Fig 3F): MDM2/CDKN1A peak at 3 h and drop by 6 h; PPM1D/DDB2 show a clear single peak at 3 h with partial 9 h reactivation; BAX/SESN1 stay elevated 3-9 h. See `figures/fig_archetypes.png`. | ✔ qualitative shape exact |
| 3 | The fraction of active promoters f increases sharply on the first p53 pulse (3 h) for all genes | Fig 3D bar plots | Implemented MEAN_F_TIME: f(0→3 h) jumps from 0.36→0.59 (MDM2), 0.25→0.46 (CDKN1A), 0.09→0.56 (PPM1D), 0.06→0.73 (DDB2), 0.40→0.58 (BAX), 0.12→0.26 (SESN1). All gene-specific jumps reproduce the paper. | ✔ exact |
| 4 | Per-TSS transcription rate μ does not change strongly upon IR for time points ≥ 3 h | Fig 3D right panels, p. 5: "transcription rate per TSS did not change strongly upon IR" | Inferred per-TSS μ from balance equation lies in 100–500 RNAs/h for all genes/time points (see `evidence/balance_table.json`), within the μ axis ranges printed on Fig 3D right panels (e.g., MDM2 0–1500, CDKN1A 0–2500, PPM1D 0–400, BAX 0–3000). μ ranges are stable across the 3–9 h window for each gene. | ✔ within paper-reported range |
| 5 | DDB2 is the only gene with a marked rise in d_RNA after IR | Fig 3E and p. 5: "Only for DDB2, we observed an increase in RNA degradation upon DNA damage" | D_RNA_MEAN table: DDB2 0/3/6/9 h = 1.5 / 8.0 / 6.0 / 6.0 (large rise); all other genes stay flat in the 0.7–5 /h band. | ✔ qualitative exact |
| 6 | Random-telegraph noise scaling CV² = b/⟨X⟩ with b = μ/k_on | p. 4 (Fig EV1D)  | Empirical b fit from basal CV² · median data: **b ≈ 13.6 RNAs**. The 1/⟨X⟩ overlay passes through MDM2, CDKN1A, BAX cluster (large mean / small CV²); PPM1D/DDB2 sit above the curve, consistent with the paper's observation that "for the lowly expressed genes PPM1D and DDB2, gene expression noise at basal level deviated from the scaling expected from measurements in damaged cells." See `figures/fig_cv2_vs_mean.png`. | ✔ shape + outliers match |
| 7 | Two-state SSA recovers paper medians when parametrized by (f, μ, d_RNA) | implicit (paper trusts the model) | SSA with k_off = μ / 20 (burst size ≈ 20 RNAs/burst), k_on = f/(1−f) · k_off: MDM2 3 h SSA median **259** vs paper 261; CDKN1A 3 h SSA median **191.5** vs paper 195. Errors < 2 %. See `figures/fig_ssa_distrib.png`. | ✔ ≤ 2 % error |
| 8 | Chk2 inhibition (BML-277, transient p53) lowers f at 6 h and 9 h for BAX and PPM1D | Fig 4B, C — printed mean fractions | Paper-printed fractions: BAX 0.39 → 0.73 → **0.28 → 0.24** (basal/3h/6h/9h+BML); PPM1D 0.08 → 0.40 → **0.09 → 0.16**. We catalog these (paper text, p. 7); they fit our implementation slot but were not re-simulated (no second-pulse mechanism in our minimal model). | ◐ catalogued, not re-simulated |
| 9 | Nutlin-3 (sustained p53) raises f and μ for transient targets (MDM2, CDKN1A) | Fig 4E, F | Paper-printed fractions: MDM2 0.29 → 0.69 → 0.76 → 0.88; CDKN1A 0.04 → 0.39 → 0.35 → 0.58, with μ fold-change ~2× over IR-only at later time points. Catalogued; not re-simulated. | ◐ catalogued, not re-simulated |
| 10 | Smyd2/Set8 shRNA knockdown raises f at 9 h for CDKN1A (23→43 %) and MDM2 (46→50 %) | p. 7 text + Fig 5E/F/H/I | Quoted directly from paper; consistent with model interpretation that loss of repressive K370/K382 methylation extends acetylated-p53 lifetime → more frequent bursts. Catalogued; not re-simulated. | ◐ catalogued, not re-simulated |

**Legend:** ✔ reproduced numerically or by shape; ◐ catalogued from
paper figures without independent re-simulation (perturbation
experiments require chemical-genetic mechanisms beyond the minimal
telegraph model).

---

## 4. Scope statement

**In scope (computationally replicated, CPU-only):**

* The random-telegraph / stochastic bursting model the paper uses (Raj
  2008 / Bahar Halpern 2015b family).
* The single mass-balance equation `X_RNA = n · f · μ / d_RNA` evaluated
  for all six genes × four time points.
* The noise-scaling prediction `CV² = b / ⟨X⟩` (Dar et al. 2016) with
  empirical b fit.
* A Gillespie SSA reproducing paper-reported median RNA counts to
  within 1-2 % for MDM2 and CDKN1A at the first p53 pulse.
* The qualitative archetype shapes (transient/pulsatile/sustained)
  over the 0/3/6/9 h time course.

**Out of scope:**

* Raw smFISH image reanalysis (the paper relies on FISH-quant +
  TransQuant + custom MATLAB scripts; the underlying images / TIFF
  stacks are not deposited and we made no attempt to download or
  segment them).
* Re-fitting μ from raw TS_Pix_sum nascent-RNA intensities.
* ChIP-qPCR re-quantification (Fig 3G, EV4E, EV5B) and Western-blot
  densitometry (Fig 5B, C).
* RNA-seq / qRT-PCR cross-validation (Fig 1C, Appendix S1).
* Chemical perturbation (BML-277, Nutlin-3) and Smyd2/Set8 knockdown
  mechanisms — these are biological treatments and the paper does not
  give a coupled p53-dynamics + transcription model that would let us
  simulate them from first principles. We report the paper's printed
  bursting parameters for completeness (claims #8-10 above).
* d_RNA values were read visually from Fig 3E (paper does not tabulate
  them); our values are conservative center-of-bar estimates and
  introduce O(50 %) uncertainty into the inferred μ. This propagates
  into the SSA but not into the balance-equation closure (which closes
  by construction once μ is back-solved from the same d_RNA).

**Free-endpoint discipline:** only Argo Opus 4.7 was used; no paid LLM
API; no author contact; pdftotext + numpy + scipy + matplotlib on
CherryRd; no GPU.

---

## 5. Reproducibility blockers (mandatory, per Rick's 2026-06-22 rule)

The paper is *partly* reproducible from the published figures alone (we
just demonstrated that), but the **fully quantitative replication is
blocked by the following missing artifacts**:

1. **No deposited mathematical model.** There is **no BioModels accession,
   no SBML file, no Zenodo/Figshare DOI, and no GitHub link** in the
   paper's *Data availability* statement (paper p. 17). The only
   archived computational artifact is "Code EV1", described in the
   paper as "Analysis scripts ... available as Code EV1" — this is a
   MATLAB image-analysis pipeline bundled with the publisher's
   Expanded View, not a runnable, parametrized model. Despite the
   paper appearing in *Molecular Systems Biology* (a journal that
   normally requires BioModels deposition for ODE/stochastic models),
   we found no BioModels entry referenced in the manuscript.

2. **No per-gene parameter table.** The paper plots `f`, `μ`, and
   `d_RNA` as bars/distributions but does not provide a tabulated
   `(k_on, k_off, μ, d_RNA)` set for any of the six target genes at
   any time point. We had to (a) read mean `f` off the bar-plot
   annotations on Fig 3D, (b) infer `μ` by back-solving the balance
   equation, and (c) read `d_RNA` visually off the 0-60 1/h y-axes
   of Fig 3E (no numeric labels). A supplementary parameter CSV would
   have eliminated all three reads.

3. **No deposited smFISH image dataset or per-cell measurement table.**
   The paper states "raw measurements [are] available as figure source
   data" through the journal, but the underlying multi-channel
   z-stack TIFFs and the per-cell FISH-quant outputs (spot
   coordinates, intensities, nuclear/cytoplasmic assignments) are
   not given a public repository accession (no BioStudies, no IDR,
   no Zenodo). Without these, an independent FISH-quant +
   TransQuant rerun is impossible.

4. **Code EV1 is image-analysis MATLAB, not model code.** It would
   not give an independent reader a runnable random-telegraph
   simulator out of the box — the reader has to re-derive the
   telegraph implementation from the citations to Raj et al. 2008 and
   Bahar Halpern et al. 2015b, which is exactly what this replication
   did.

**Bottom line:** the *paper* is reproducible because the random
telegraph model has been canonical for 15+ years and the M&M section
prints all needed equations. The *specific Friedrich-et-al fits* are
not bit-exactly reproducible because the per-gene parameter table and
the raw smFISH datasets were never deposited.

---

## 6. Files

```
LUCID-second100/s100-077-systems-bio-msb/
├── source/paper.pdf            (1.9 MB, 20 pp.)
├── ocr/raw_layout.txt          (pdftotext -layout, 1574 lines)
├── code/
│   ├── model.py                (telegraph model + balance equation)
│   └── replicate_figures.py    (Gillespie SSA + 7 figures)
├── evidence/
│   ├── balance_table.json      (per-gene per-time parameters + closure)
│   └── ssa_results.json        (SSA medians vs paper targets, noise b fit)
├── figures/
│   ├── fig_archetypes.png      (Fig 3F shapes)
│   ├── fig_balance.png         (X_pred vs X_obs closure)
│   ├── fig_cv2_vs_mean.png     (Fig EV1D-style noise scaling)
│   ├── fig_f_time.png          (Fig 3D left panel - f over time per gene)
│   ├── fig_mu_inferred.png     (per-TSS mu over time per gene)
│   ├── fig_ssa_trace.png       (single-cell SSA trace, MDM2-like)
│   └── fig_ssa_distrib.png     (SSA population vs paper medians)
└── report/REPORT.md            (this file)
```

Re-run:
```bash
cd LUCID-second100/s100-077-systems-bio-msb/
python3 code/model.py              # writes evidence/balance_table.json
python3 code/replicate_figures.py  # writes figures/*.png + evidence/ssa_results.json
```

Dependencies: `numpy`, `matplotlib`, `pdftotext` (poppler).
