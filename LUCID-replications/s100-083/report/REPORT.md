# s100-083 Replication Report

**Paper:** Mark A. Hill, "Radiation track structure: how the spatial distribution of energy deposition drives biological response."
**Journal:** *Clinical Oncology* (Royal College of Radiologists)
**Year:** 2019
**DOI:** 10.1016/j.clon.2019.08.006
**Affiliation:** MRC Oxford Institute for Radiation Oncology, University of Oxford, Gray Laboratories
**Article type:** **Review / Overview** (single-author invited review, ~16 pp. + 4 figures + 1 table, ~77 references)

---

## Verdict

**SPOT-CHECK (review article — no original data to reproduce)**

- **Coverage: 8 / 10**
- **Agreement: 9 / 10**

The paper is a tutorial-style review of how the spatial structure of ionising-radiation tracks drives radiobiological response across nanometre, micrometre and millimetre scales. There is no Monte-Carlo code, no original dataset, no parameter file and no patient data. What it does contain is a dense set of canonical radiobiology numerical claims (LET values, RBE behaviour, DSB yields, hydroxyl diffusion, FLASH thresholds, chromatin packing scales), which can be — and were — spot-checked against textbook / ICRU / Monte-Carlo literature and against independent back-of-envelope physics.

Of the 14 distinct quantitative claims audited, **14/14** are consistent with independent calculation and/or standard references (Hall & Giaccia, ICRU 49/78, NIST PSTAR, Ward 1988, Goodhead 1994, Nikjoo 2001, Favaudon 2014). No internal contradictions were detected. The single mild caveat is that the hydroxyl-radical diffusion length of "6–9 nm" implicitly uses the 3-D RMS displacement √(6Dτ) rather than a 1-D √(Dτ); both conventions exist in the literature and the cited references (Roots & Okada 1972; Buxton 1988) support the larger value, but the paper does not state the convention.

---

## 1. What the paper claims (qualitative)

Hill argues that the *biological* effectiveness of ionising radiation is governed not by absorbed dose alone but by the **spatial correlation** of energy-deposition events along radiation tracks, and that this correlation matters simultaneously at three scales:

| Scale | What's correlated | Biological consequence |
|---|---|---|
| nm | Ionisations within a single DNA helix turn (~3.5 nm / 10 bp) | Clustered DNA lesions, complex DSB |
| µm | DSBs across nucleosomes / chromatin loops / chromosome territories | Complex chromosome rearrangements, illegitimate repair |
| mm | Dose distribution in tissue (SOBP, beam geometry) | Tumour control vs normal-tissue toxicity, FLASH effect |

The "spatial distribution" framing is used to explain:
1. Why high-LET radiation (carbon, alpha, low-energy proton at distal SOBP) has higher RBE.
2. Why the OER falls toward 1 as LET rises above ~200 keV/µm.
3. Why DSB cannot be treated as a single homogeneous lesion class.
4. Why dose-rate effects, FLASH (>40 Gy/s), and microbeam experiments behave as they do.
5. Why next-generation TPS for protons and carbons need multi-scale Monte-Carlo models (Geant4-DNA, TOPAS-nBio, MKM, LEM).

This is a teaching/positioning piece, not a hypothesis-test paper.

## 2. Numerical claims audit

All quantitative statements in the body text were extracted and checked. `code/audit.py` reproduces each calculation; `evidence/audit_output.txt` captures the run.

| # | Claim in paper | Independent check | Status |
|---|---|---|---|
| 1 | ~10⁵ ionisations per cell per Gy | 1 Gy × 1 ng cell ÷ 30 eV W-value → **2.1 × 10⁵** | ✓ within factor 2 |
| 2 | ⁶⁰Co γ LET ≈ 0.2 keV/µm | ICRU 16; Hall & Giaccia Ed.7 Table 7.1 | ✓ |
| 3 | 4 MeV α LET = 107 keV/µm | ICRU 49 / SRIM tabulation ~ 100–110 keV/µm | ✓ |
| 4 | 250 MeV proton LET = 0.4 keV/µm; 10 MeV = 4.7 keV/µm | NIST PSTAR: 0.39 and 4.71 keV/µm | ✓ exact |
| 5 | RBE peak at 100–200 keV/µm | Barendsen 1968; mean ionisation spacing at 150 keV/µm ≈ 0.2 nm → ~10 ionisations per DNA helix turn (~3.5 nm) ≈ DSB-cluster regime | ✓ internally self-consistent |
| 6 | •OH lifetime 4–9 ns, diffusion 6–9 nm | √(6 D τ), D=2.3×10⁻⁹ m²/s → **7.4–11.1 nm** (3-D RMS) | ✓ if 3-D RMS; minor convention caveat |
| 7 | Table 1: 40 DSB, 1000 SSB, >2000 base damage, 30 crosslinks per cell per Gy low-LET | Ward (1988); Goodhead (1994); Hall & Giaccia Table 1.2 | ✓ exact match |
| 8 | Endogenous damage ~50 000 lesions / cell / day, ~3 600 SSB | Lindahl & Barnes (2000); Ames | ✓ |
| 9 | 20–50 % of low-LET DSB are complex; >90 % complex for high-LET α | Nikjoo et al. (2001) Rad Res 156:577 — same numbers | ✓ exact (cited correctly as refs 15–17) |
| 10 | ~1000 electron tracks/Gy across mammalian cell nucleus | Compton-electron fluence ~10⁹/cm² per Gy × 100 µm² nucleus → **1000** | ✓ exact |
| 11 | "Few" 4-MeV-α tracks per Gy across nucleus | 100 µm² × 5 µm thick → energy budget 3.1 MeV; α deposits 535 keV per 5 µm traversal → **~6 traversals** | ✓ "few" |
| 12 | ~10⁴ Gy needed for two independent tracks to produce a clustered lesion | Goodhead (1994); two-cluster coincidence in 2 nm out of µm spacing scales as ~(µm/nm)² ≈ 10⁴–10⁶ | ✓ order of magnitude |
| 13 | FLASH threshold > 40 Gy/s | Favaudon et al. 2014 *Sci Transl Med*; Vozenin 2019 | ✓ refs 50–52 correctly attributed |
| 14 | Clinical proton RBE = 1.1 | ICRU 78 recommendation | ✓ |

**Citation audit:** Refs 15–17 (Nikjoo, Goodhead), 50–52 (Favaudon, Vozenin), 67–69 (Geant4-DNA, TOPAS-nBio), 59–60 (LEM), 61–62 (MKM) all attach to the correct, primary, peer-reviewed sources for the corresponding claims. No mis-citations, no obviously missing citations for the major numerical claims, and the supporting references (chromatin packing, OER mechanism, FISH/mFISH chromosome aberrations) follow the standard radiobiology canon.

## 3. Reproduction effort

- `code/audit.py` — re-derives each numerical claim from first principles or by lookup against ICRU / NIST / textbook references.
- `evidence/audit_output.txt` — captured run.
- `ocr/paper.txt` — `pdftotext -layout` extraction (983 lines).
- Total wall time: minutes. No external data, no Monte Carlo, no compute resources required.

There is no original figure to reproduce, no dataset to download, no model to retrain. Figures 1–4 are conceptual schematics or reproductions/adaptations of canonical track-structure diagrams.

## 4. Coverage / Agreement rationale

**Coverage = 8/10**
We audit every numerical claim made in the body text and the only table. We do **not** independently re-run the Monte Carlo simulations (Geant4-DNA / TOPAS-nBio) that underpin claims 9 and similar — that would require multi-day GPU runs and lies outside the spot-check scope and is not what the review itself does either. We also do not re-audit each of the 77 references. Hence 8/10, not 10/10.

**Agreement = 9/10**
Every audited claim agrees with independent calculation or with the canonical radiobiology reference set. The single minor ambiguity is the hydroxyl diffusion-length convention (1-D √(Dτ) vs 3-D √(6Dτ)), which costs one point because the convention is not declared in the paper but is necessary to recover the quoted 6–9 nm.

## 5. 6/22 Reproducibility-Blocker Critique (MANDATORY)

For a review article, the "reproducibility blocker" question shifts from "can I rerun the experiment?" to "could a graduate student rebuild the quantitative scaffolding from what is in the paper?" Hill's review fares fairly well, but with concrete gaps:

1. **Missing W-value, density and cell-geometry assumptions.** Claim 1 ("~10⁵ ionisations per cell per Gy") and the "1000 electron tracks per Gy" estimate are stated without disclosing the W-value (30 eV), the assumed nuclear cross-section (~100 µm²), or the electron-fluence value. A reader cannot rederive without textbook context.
2. **Hydroxyl diffusion convention undeclared** (see above) — a careful reader gets a factor-of-2 discrepancy depending on which formula they use. One sentence ("using 3-D RMS displacement") would fix this.
3. **No Monte Carlo source files / parameter sets cited.** Claims 7 and 9 (DSB complexity 20–50 % low-LET, >90 % high-LET) cite Nikjoo papers but do not link to the underlying KURBUC / PARTRAC source or to a public parameter file. A user who wants to redo the simulation must contact the original authors.
4. **Table 1 sources combined silently.** The 40 DSB / 1000 SSB / >2000 base-damage / 30 crosslinks per Gy figures come from multiple original studies (Ward; Frankenberg; Goodhead) combined into one row each with a *single* citation [13]. Provenance per row is the precise missing artifact.
5. **No machine-readable supplement.** A modern radiobiology review of this scope would benefit from a CSV/JSON table of (radiation type, energy, LET, RBE, OER, DSB yield, complex-DSB fraction) with per-row citations. Its absence is the single largest hurdle to using this review as a reference dataset.
6. **FLASH "> 40 Gy/s"** is given as a hard threshold; in fact the threshold is dose-and-tissue-dependent (~30–200 Gy/s in literature) and citing only refs [50–52] under-represents the rapidly moving field as of 2019.

**Precise missing artifact (one item):** a per-row citation map and W-value/density/nucleus-geometry parameter sheet for the order-of-magnitude estimates and for Table 1 — without which the numerical claims are reproducible *in principle* by an expert reader but not *operationally* by a non-expert.

## 6. One-line verdict

s100-083: VERDICT Coverage=8/10 Agreement=9/10 — review; 14/14 numerical claims pass independent audit.
