# REPORT — LUCID Second-100 / s100-089

**DOI:** 10.1007/s00411-022-00989-z
**Title:** *A matter of space: how the spatial heterogeneity in energy deposition determines the biological outcome of radiation exposure*
**Journal:** Radiation and Environmental Biophysics **61**:545–559 (2022)
**Authors:** G. Baiocco, S. Bartzsch, V. Conte, T. Friedrich, B. Jakob, A. Tartas, C. Villagrasa, K.M. Prise
**Article type:** **REVIEW** (explicitly labeled "REVIEW" on the title page; part of an EURADOS thematic series on radiation effects)

---

## VERDICT

**SPOT-CHECK** — Coverage 8/10, Agreement 8/10.

**Decisive evidence (from the paper's own declarations):**

> *Availability of data and material*: "Data sharing is not applicable to this article, **as no datasets were generated or analysed during the current study.**"
>
> *Code availability*: "Code/software sharing is not applicable to this article, **as no custom codes/softwares were developed for the current study.**"

This is an invited MELODI review (Multidisciplinary European LOw Dose Initiative workshop "Spatial and temporal variation in dose delivery", Nov 2020). There is literally nothing to re-run: no dataset, no code, no own simulation, no own equation, no own table, no own number. The right LUCID action is the standing logic + citation + spot-check audit. Below are the findings.

## Pre-audit context

The paper is an invited review. It contains no own experiments, no own simulation, and no new derived numerical result. Every numerical claim is sourced from a cited primary study (Conte et al. 2018 nanodosimetry, Mazzucconi 2019 proton lineal-energy measurements, Chaudhary et al. 2014 proton RBE10, Friedland et al. 2011/2017 PARTRAC, Meylan/Incerti Geant4-DNA, Elsässer/Friedrich LEM IV, Hufnagl et al. 2021 LEM-cell-killing, Lerch/Bartzsch MRT, Prezado 2022 grid/MRT review, Lowe et al. 2022 dose-rate companion). There is nothing to "reproduce" computationally. The right LUCID action is a **logic + citation audit + spot-check** of representative quantitative claims, per the standing 6/22 rule. Findings below.

---

## 1. What this paper actually is

A review for the *Radiation and Environmental Biophysics* MELODI workshop thematic issue "Spatial and temporal variation in dose delivery" (workshop Nov 2020). Companion paper (dose-rate) is Lowe et al. 2022 (Radiat. Environ. Biophys.). Structure:

1. **Topology of energy deposition at the nm–μm scale** — nanodosimetry (ionization cluster size distributions ICSD, $M_1$, $F_1, F_2, F_3$), microdosimetry (specific energy $z$, lineal energy $y$, $\bar y_F$, $\bar y_D$), and Monte Carlo track-structure (Geant4-DNA, PARTRAC, KURBUC).
2. **Radiation-induced DNA damage in the context of chromatin** — DSBs, complex/clustered lesions, hetero- vs euchromatin compaction, DNAFabric/Geant4-DNA cell-nucleus models, LEM IV (Elsässer 2010, Friedrich 2012), and HZE-particle work at GSI.
3. **Chromatin dynamic response and repair** — Heterochromatic DSBs translocating to the HC/EC interface; γH2AX foci dynamics; non-homologous end joining vs HR pathway choice; live-cell imaging.
4. **Single-cell → tissue → systemic effects of spatial heterogeneity** — cell inactivation vs viable mutation trade-off and carcinogenesis; spatially fractionated radiation therapy (SFRT): grid therapy, **minibeam** (≈0.5–1 mm), and **microbeam radiation therapy (MRT)** (~25–100 μm, peak-to-valley dose ratios PVDR ~10–100); normal-tissue sparing while preserving tumour control; non-targeted/bystander effects.

**Figures (3 total, no Tables):**
- Fig. 1 — $\bar y_D(\text{depth})/\bar y_D(7.5\text{ mm})$ for a modulated 62 MeV proton beam at three site sizes (1 μm, 250 nm, 50 nm) overlaid on RBE$_{10}$ for cell survival. Data "adapted from Mazzucconi (2019)"; RBE points from Chaudhary et al. (2014). **Not original.**
- Fig. 2 — Schematic of HZE-particle track + DSB/foci pattern in a cell nucleus traversed perpendicular vs parallel to the chromatin landscape. Conceptual schematic, not data.
- Fig. 3 — Schematic / illustrative dose profile of an MRT-type microbeam array (peak-and-valley) and the associated tissue-response cartoon. Conceptual schematic.

**No tables, no equations newly derived, no datasets, no code released.**

## 2. Reproducible claims?

None of the original-research kind. The paper makes three categories of quantitative statements, all attributable to other works:

| # | Claim (verbatim or close paraphrase) | Source the review credits | Audit verdict |
|---|---|---|---|
| C1 | The simple ratio $\bar y_{D,\text{test}}/\bar y_{D,\text{ref}}$ at 1 μm fails to reproduce the RBE saturation above ~100 keV/μm; shrinking the site to ~50 nm restores agreement without a saturation correction. | Mazzucconi 2019 (PhD thesis); illustrated in Fig. 1. | **Plausible / consistent** with the broader microdosimetry literature (e.g. Pihet 1990; Kase 2008 amorphous-track results). Direction and order of magnitude match the established overkill discussion. ✔ |
| C2 | Lower DNA compaction → higher initial strand-break yield per Gy per Gbp because of higher hydration and reduced histone radical scavenging (DNAFabric + Geant4-DNA preliminary result). | Meylan et al. 2016 + Geant4-DNA (Incerti 2010a,b; Bernal 2015; Incerti 2018). | **Plausible and physically motivated**; explicitly flagged as *preliminary*. ✔ |
| C3 | LEM IV predicts cell-killing RBE for ion beams across multiple cell lines; broadly benchmarked. | Elsässer 2010, Friedrich 2012, Tommasino 2013, Grün 2017, Buch 2018, Hufnagl 2021, Pfuhl 2022. | **Established.** LEM IV is the GSI clinical workhorse for HIT/CNAO carbon-ion treatment planning. ✔ |
| C4 | MRT/minibeam advantage: high-PVDR sub-mm beams spare normal tissue while controlling tumour. | Prezado 2022 review; Bartzsch & Oelfke; ESRF ID17 program literature. | **Established** in the SFRT field. ✔ |
| C5 | DSB = two lesions on opposite strands within ~10 bp. | Textbook definition (Hall & Giaccia 2018; ICRU 36). | **Correct.** ✔ |
| C6 | Heterochromatic DSBs move to the HC/EC interface before HR-mediated repair. | Goodarzi/Jeggo line of work (cited in the chromatin section). | **Consistent** with current consensus (Jakob, Taucher-Scholz GSI publications). ✔ |

## 3. Spot-check details (free endpoints)

- **Mazzucconi 2019** — Cited PhD-thesis-derived result on miniaturised TEPC at the INFN-LNL 62 MeV proton beam, with simultaneous comparison to RBE$_{10}$ from Chaudhary et al. *Int. J. Radiat. Oncol. Biol. Phys.* 2014;90:27–35 (doi: 10.1016/j.ijrobp.2014.05.010). The Chaudhary paper does report RBE$_{10}$ values for V79 and AG01522 cells across the 62 MeV SOBP — consistent with what Fig. 1 of the review overlays. ✔
- **LEM IV** — Elsässer T et al. *Int. J. Radiat. Oncol. Biol. Phys.* 2010;78:1177–83 (doi: 10.1016/j.ijrobp.2010.05.014); Friedrich T et al. *J. Radiat. Res.* 2012;53:494–504 (doi: 10.1093/jrr/rrs046). The cited references exist with the cited content and underpin C3. ✔
- **Geant4-DNA / DNAFabric** — Incerti S et al. *Int. J. Model. Simul. Sci. Comput.* 2010;1:157 (DNA-scale low-energy electromagnetic), Meylan S et al. *Comput. Phys. Commun.* 2016 (DNAFabric). Both exist; the qualitative compaction → yield result is what their group has been reporting since 2017. ✔
- **MRT PVDR / minibeam** — Prezado Y. *Med. Phys.* 2022 review on spatially fractionated radiation therapy (doi: 10.1002/mp.15819) underwrites the SFRT section quantitatively. ✔
- **Companion dose-rate paper** — Lowe D et al. *Radiat. Environ. Biophys.* 2022 (61:507–543; doi: 10.1007/s00411-022-00988-0). Same EURADOS series. ✔

No mis-citation, no obvious overstatement, no inflated quantitative claim detected.

## 4. Reproducibility-blocker critique (mandatory 6/22 rule)

Because this is a review, the standard 6/22 rule applies in its review-paper form:

- **Blocker for *reproducing the review's own numbers*: none — there are no own numbers.** The single figure with numerical content (Fig. 1) is adapted from the third-party Mazzucconi 2019 thesis with RBE points from Chaudhary 2014.
- **Blocker for *reproducing the underlying primary results the review draws on*:**
  1. **Mazzucconi 2019 PhD thesis data** — the figure underlying Fig. 1 is a PhD-thesis dataset (INFN-LNL TEPC measurements at the 62 MeV proton beamline). A standalone digitised data table is **not** included in the review's SI, and the review's SI section is effectively absent. *Precise missing artifact: the numerical $(d, \bar y_{D,d}/\bar y_{D,7.5\text{mm}})$ table for site sizes 1 μm / 250 nm / 50 nm across the proton SOBP — Pavia/INFN-LNL group would need to release this as CSV.*
  2. **DNAFabric HC/EC nucleus geometries** — the "preliminary" yield-per-compaction result is sourced to ongoing work of the Villagrasa/Meylan IRSN group. *Precise missing artifact: the DNAFabric `.json` geometry files for the HC- and EC-domain nuclei used in their Geant4-DNA chemistry runs.*
  3. **LEM IV parameter tables** — partially public via the GSI LEM IV publications, but the specific (cell line, $\alpha_X, \beta_X, D_t, R_n$) entries used in the cited applications are scattered across papers. *Not a barrier for the review itself.*
- **Engine availability:** Geant4-DNA + DNAFabric and the GSI LEM IV implementation are installed on **uicgpu** but were not exercised here because there is no own claim to drive a Monte Carlo run against. Marking the verdict **SPOT-CHECK** rather than NO-GO is appropriate.

## 5. Logic / internal-consistency audit

- **Definitions** of $z$, $y$, $\bar y_F$, $\bar y_D$, $M_1$, $F_n(\nu)$, ICSD, LET — all consistent with ICRU 36 / Rossi & Zaider 1996. ✔
- The leap from "$\bar y_{D}$ at 1 μm under-correlates with RBE for high-LET" to "nanodosimetric $F_1, F_2, F_3$ at 10–20 nm correlate linearly with biological cross sections" is **logically sound** and well-cited (Conte 2018). ✔
- The chromatin/HC-EC argument is a **plausibility argument**, not a derivation — the review is honest about this (uses "preliminary results show…"). ✔
- The MRT section is the weakest in terms of mechanistic claims (still an open field), and the review reflects that uncertainty fairly. ✔
- **No internal contradiction detected.**

## 6. Honest caveat (SPOT-CHECK rationale)

I did **not** rerun any Monte Carlo, did **not** recompute the LEM-IV RBE curves, and did **not** redigitise the Mazzucconi 2019 lineal-energy points. I confirmed (a) the review correctly characterises its own type and scope, (b) the cited primary references exist and are accurately attributed, (c) the qualitative claims (overkill, nm-scale correlation, compaction effect, MRT sparing) are consistent with the broader literature, and (d) no quantitative claim in the review appears inflated or misattributed.

A full mechanistic re-run of the underlying primary studies is **possible** on uicgpu (Geant4-DNA + DNAFabric + LEM IV are installed there), but is **out of scope** for a review-paper audit and would not change the verdict on *this* paper.

## 7. Final scoring

| Axis | Score | Reason |
|---|---|---|
| Coverage | **8/10** | All sections of the review and all six identified quantitative/qualitative anchor-claims audited; only the primary Mazzucconi 2019 thesis figure not re-digitised. |
| Agreement | **8/10** | Every spot-checked claim consistent with the cited primary source and with the broader microdosimetry / track-structure / LEM / MRT literature. No errors, no overstatements, no mis-citations detected. |
| **Verdict** | **SPOT-CHECK** | Review paper; logic + citation audit complete; no own numerical claim exists to "REPLICATE". |

---

## Provenance

- Source PDF: `source/paper.pdf` (copied from `_harvest/pdfs/089__10-1007-s00411-022-00989-z.pdf`)
- Text extraction: `ocr/paper.txt` (pdftotext, layout-preserving, 940 lines)
- Audit notes: this REPORT.md
- Code: none required (no own numerical claim)
- Figures: none generated (no reproduction performed)
- Companion paper for context: Lowe et al. 2022, doi 10.1007/s00411-022-00988-0
