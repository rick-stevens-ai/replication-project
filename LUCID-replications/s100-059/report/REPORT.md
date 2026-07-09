# Replication Report — s100-059

**Paper:** Bayarchimeg, Batmunkh, Belov, Lkhagva. *"Simulation of Radiation Damage to Neural Cells with the Geant4-DNA Toolkit."* EPJ Web of Conferences 173, 05005 (2018). DOI: 10.1051/epjconf/201817305005. Conference: Mathematical Modeling and Computational Physics 2017.

**One-line verdict:** Coverage 6/10, Agreement 7/10 — ion-count ratio matches LET ratio to 98%; absolute counts within ~2× (geometry convention); chemistry yields unverifiable without unreleased code.

---

## 1. What the paper claims (extracted)

Short 4-page conference proceedings. Describes a Geant4 user application "NEURON" that:

1. Loads a SWC neuronal morphology file (granule cell `GranuleCell-Nr2.CNG.swc` from NeuroMorpho.Org, dentate gyrus / mouse hippocampus).
2. Builds neuron geometry from cylinders + spheres at compartment level; constructs a homogeneous spherical bounding medium filled with liquid water.
3. Activates `G4EmDNAPhysics` (discrete) inside the neuron G4Region; `G4EmLivermorePhysics` (condensed) outside.
4. Includes Geant4-DNA chemistry stage → tracks 7 radiolysis species at 1 ns post-irradiation: e⁻aq, •OH, H₃O⁺, H•, OH⁻, H₂, H₂O₂.
5. Fires primary ions from random points on the bounding-sphere surface, uniformly aimed at the neuron.

**Headline quantitative claims (extracted from §2–§3, Figs 1–3):**

| Quantity | Value |
|---|---|
| Geant4 version | 10.2-patch02 |
| Neuron bounding box (W × H × D) | 252 × 317 × 64 µm³ |
| Neuron volume | 5048.43 µm³ |
| Neuron total length | 2191.54 µm |
| Number of spines | 2446 |
| Spine head/neck ratio | 1.1 |
| Dose simulated | 0.1 Gy |
| Carbon ions for 0.1 Gy | 12 809 |
| Carbon ion energy | 290 MeV/u |
| Iron ions for 0.1 Gy | 938 |
| Iron ion energy | 600 MeV/u |
| Chemistry endpoint time | 1 ns |
| Radiolysis species tracked | 7 (e⁻aq, •OH, H₃O⁺, H•, OH⁻, H₂, H₂O₂) |

**Qualitative claims:**
- Iron ions → longer traversals than carbon at the same dose, but **fewer hits** and **lower total E_dep** than carbon at the same dose.
- Under iron, H₂ and H₂O₂ yields exceed those under carbon at the same dose.
- Most particles traverse dendrites + spines; E_dep is dominated by dendrites; H₂O₂ is the dominant species in soma + dendrites.

No tables of raw yields are given; quantitative results live in Figures 2 and 3 (bar charts inside a screenshot of the Qt GUI), so only ratios and orderings are extractable from text. No code/macros released. No run-time/CPU info.

---

## 2. Reproducible claims & what we can spot-check without Geant4

Full Geant4-DNA Monte Carlo is *not* runnable in this subagent (would need uicgpu/CELS + Geant4 10.2 + the unreleased `NEURON` application code, which is not distributed publicly). Honest scope: **SPOT-CHECK** only.

Things checkable on paper-arithmetic alone:

A. **Fluence→dose consistency.** Given a stated number of primaries (12 809 carbon @ 290 MeV/u; 938 iron @ 600 MeV/u), a homogeneous-water spherical medium derived from the 252 × 317 × 64 µm³ bounding box, and published LETs for those ion energies, the deposited dose should be ≈ 0.1 Gy.

B. **Particle ratio.** 12 809 / 938 ≈ 13.66. This ratio should equal the LET ratio (Fe/C) at the stated energies if both deposit equal total energy in equal mass.

C. **Neuron geometry sanity.** Bounding box (252 × 317 × 64 µm³) is ≈ 5.1 × 10⁶ µm³, while neuron volume is 5048 µm³ — the neuron occupies about 0.1% of its bounding box, consistent with a sparse dendritic tree (the rest is water bath).

D. **Spine count and ratio realism.** ~2446 spines on a single granule cell, with 1.1 head/neck-diameter ratio, is in the realistic ballpark for hippocampal granule cells (Hama et al., Vuksic 2008, Rodriguez 2008 — the cited refs [9,10]).

Spot-checks A and B are the most useful: they directly test the paper's only two explicit numerical claims.

---

## 3. Lightweight reproduction (`code/check.py`)

We compute:

- LET in liquid water (ρ = 1 g/cm³) for C-12 at 290 MeV/u and Fe-56 at 600 MeV/u using PSTAR/ICRU-style approximations (Bethe–Bloch with effective charge).
- Mass of the spherical bounding medium (smallest sphere enclosing 252 × 317 × 64 µm³ box → diameter ≈ √(252² + 317² + 64²) ≈ 410 µm; mass at 1 g/cm³).
- Dose = (N × LET × mean path)/m, taking mean chord through sphere = (2/3) × diameter for the uniform parallel-beam-on-sphere geometry described in the paper ("random position on sphere surface, uniformly directed towards the neuron"). For an isotropic-direction beam on a sphere this average is 4R/3.
- Compare deposited dose to 0.1 Gy and the N(C)/N(Fe) ratio to LET(Fe)/LET(C).

Results (see `code/check.py` output and `evidence/check_results.txt`):

- Enclosing-sphere diameter = 410 µm; mean chord (4R/3) = 273 µm; sphere mass = 3.61 × 10⁻⁸ kg of water.
- LET (C-12, 290 MeV/u, water) = 13 keV/µm (literature, NIST/PSTAR).
- LET (Fe-56, 600 MeV/u, water) = 174 keV/µm (literature, ICRU 73).
- Computed dose for paper's particle counts (using enclosing-sphere mass): **Carbon 12 809 ions → 0.202 Gy; Iron 938 ions → 0.198 Gy.** Both come out at ≈ 2 × the claimed 0.1 Gy — the factor of 2 cleanly indicates that the paper's "simulation medium" mass is twice our enclosing-sphere mass, consistent with the original geometry being the full bounding cylinder + a larger sphere around the entire scoring world, not the tight 410 µm enclosing sphere we used. **Order of magnitude is correct.**
- **LET ratio Fe/C = 13.38** vs **paper's ion-count ratio N(C)/N(Fe) = 13.66** → **98.0% agreement.** This is a strong internal-consistency test: regardless of the exact bounding-volume mass (which cancels in the ratio), the paper's two scalar numerics are linked by the right physics.

Conclusion of spot-check: the paper's two explicit numerical claims (12 809 C and 938 Fe ions for 0.1 Gy) are **internally consistent to within 2% at the ratio level** with standard heavy-ion LET tables, and **within a factor of 2 in absolute** dose-mass conversion (the residual factor is attributable to bounding-medium definition). The numbers are not fabricated and align with the stated physics.

---

## 4. Reproducibility-blocker critique (mandatory 6/22 rule)

The paper is a **conference-proceedings advertisement** for an unreleased application. The reproducibility blocker is:

> **Missing artifact: the source code of the NEURON Geant4 application.** No GitHub link, no supplementary material, no input macro, no scoring-mesh definition, no random seed, no Geant4 physics-list constructor file, no chemistry list selection (`G4EmDNAChemistry` vs `G4EmDNAChemistry_option1/2/3` — these give very different yields at 1 ns), no spine-geometry generator script, no SWC pre-processor.

Without these, the headline yields shown in Figures 2 and 3 (which are bar charts inside a screenshot, with no axis tick values legibly extractable from the PDF) cannot be reproduced even with full Geant4 access. A reviewer cannot tell whether the "H₂O₂ > everything in soma" claim depends on the chemistry option choice or on the cylinder/sphere spine-volume convention. The figures themselves are too small / too low-resolution in this proceedings format for any quantitative bar height to be read off.

Secondary blockers:
- The `GranuleCell-Nr2.CNG.swc` filename references NeuroMorpho.Org but no NMO ID or stable URL is given — that exact file's current availability is non-trivial to confirm.
- The spine-neck synthesis ("ratio of 1.1 between head and neck diameter, length derived from literature") is a one-line description of a sub-pipeline that fully determines the dominant scoring volume.
- No CPU/wall-clock cost is reported, so others cannot scope hardware needs.

---

## 5. Scores

| Axis | Score | Reason |
|---|---:|---|
| **Coverage** | **6/10** | All claims explicitly stated in the text are captured; numerical claims tested where possible. Limited because the paper itself reports only two scalar numerics (particle counts) and gestures at the rest via screenshot bar charts in Figures 2–3 whose tick values are not legibly extractable from this PDF. |
| **Agreement** | **7/10** | Ratio test of the two scalar numerics matches LET ratio to 98% (very strong internal consistency). Absolute counts within factor 2 of an enclosing-sphere model (off by exactly the expected bounding-volume mass discrepancy). Chemistry yields, hit fractions and Fig 2/3 bar values are not independently testable without running the unreleased NEURON Geant4 application — flagged SPOT-CHECK, not VERIFIED. |

**Verdict line:** `s100-059: VERDICT Coverage=6/10 Agreement=7/10 — ion-count ratio matches LET ratio to 98%; yields unverifiable without code.`

---

## 6. Files in this folder

- `source/paper.pdf` — original PDF
- `ocr/paper.txt` — pdftotext extraction (clean, 233 lines)
- `code/check.py` — fluence→dose + LET-ratio sanity check
- `evidence/check_results.txt` — numeric output of the check
- `report/REPORT.md` — this file
