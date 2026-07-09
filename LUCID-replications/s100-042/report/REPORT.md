# s100-042 — Replication Report

**Paper:** Mokari M., Alamatsaz M.H., Moeini H., Taleei R. (2018).
*A Simulation Approach for Determining the Spectrum of DNA Damage Induced by Protons.*
**Journal / DOI:** Physics in Medicine & Biology (IOP) — `10.1088/1361-6560/aad7ee`
**LUCID rank:** 42
**Harvested PDF:** `_harvest/pdfs/042__10-1088-1361-6560-aad7ee.pdf`
**Working dir:** `s100-042/`
**Reproduction script:** `code/reproduce.py`
**Evidence log:** `evidence/reproduce.log`

---

## TL;DR Verdict
**Coverage = 6/10 · Agreement = 8/10**
SPOT-CHECK level reproduction (full Geant4-DNA MC engine on uicgpu required for a true run).
Four of five internal-consistency audits PASS; one Table 2 column inconsistency surfaces a
paper-side reporting issue but does not invalidate the headline yields.

One-line summary: **Geant4-DNA proton DNA-damage spectra; arithmetic & classifier reproduce; engine-blocked otherwise.**

---

## 1. What the paper claims (precise reproducible claims)

### 1a. Method (Geant4-DNA v10.3)
- **Geometry:** 432-nucleotide (216 bp, 73.44 nm) B-DNA segments parsed from a PDB file, scattered
  µ-randomness style inside a 100-nm-radius water sphere, with an isotropic point proton source
  at the sphere center.
- **Physics:** Geant4-DNA elastic, ionization, excitation, Auger cascades. Electron tracking cut-off **7.4 eV**.
- **Chemistry stage:** simulated up to **1 ns** using `TimeStepAction`; only OH• is treated as DNA-active.
- **Strand-break rules:**
  - **Direct:** SB registered when ΣE in one sugar–phosphate volume ≥ **E_ssb = 17.5 eV**.
  - **Indirect:** OH• inside a (8 + 2.3) nm-diameter cylinder around a 2.3 nm DNA cylinder produces a
    SB at the nearest sugar/phosphate with probability **P_OH = 0.13**.
- **Damage formation:** post-process Python algorithm classifying each segment per Nikjoo et al.
  with a **10 bp clustering window** into NB, SSB, SSB+, 2SSB, DSB, DSB+, DSB++.
- **Cell normalization:** 22 chromosomes × 245 Mbp/chr = **5.39 Gbp/cell**.
- **Energy range:** primary protons at **0.5, 1, 2, 10, 20 MeV** (LET∞ = 39.7, 24.2, 13.9, 3.4, 1.9 keV/µm).
- **Statistics:** number of events raised from 10³ to **5×10³** following Nikjoo's recipe.

### 1b. Headline quantitative results
**Table 2 — relative damage frequencies (%), and yields (per Gy·Gbp).**

| E (MeV) | LET (keV/µm) | NB    | SSB   | SSB+ | 2SSB  | DSB   | DSB+ | DSB++ | Y_SSB | Y_DSB |
|---------|--------------|-------|-------|------|-------|-------|------|-------|-------|-------|
| 0.5     | 39.7         | 26.59 | 29.26 | 4.06 | 17.42 | 10.27 | 7.70 | 4.68  | 39.05 | 7.80  |
| 1       | 24.2         | 37.92 | 31.16 | 3.52 | 13.75 | 7.59  | 4.90 | 1.18  | 50.92 | 7.77  |
| 2       | 13.9         | 50.44 | 30.34 | 2.59 | 9.93  | 4.67  | 1.76 | 0.28  | 62.74 | 6.36  |
| 10      | 3.4          | 63.29 | 27.35 | 1.57 | 5.19  | 2.10  | 0.47 | 0.03  | 73.45 | 4.30  |
| 20      | 1.9          | 67.92 | 25.27 | 1.10 | 3.95  | 1.50  | 0.25 | 0.01  | 75.15 | 3.50  |

**Table 5** adds Y_SSB / Y_DSB in (Gy·cell)⁻¹ using the 5.39 Gbp/cell normalization
and a second yield computation derived from Σ n(E,y) · P(E,y)/y (Charlton 1989).

**Headline claim (DSB vs LET, Fig. 3):** Y_DSB rises from ~3.5 Gy⁻¹Gbp⁻¹ at 1.9 keV/µm to ~7.8 at 39.7 keV/µm,
with rolloff above ~25 keV/µm, in good agreement with Belli 1998 and Campa 2005 experiments and
broad agreement with Meylan et al. Geant4-DNA fibroblast simulation.

---

## 2. What I actually reproduced (SPOT-CHECK)

The full Monte Carlo (Geant4-DNA v10.3 with a 216-bp PDB B-DNA + chemistry + 5×10³ events at each
of 5 energies + µ-randomness sampling of N DNA segments) is not feasible inside this subagent. The
engine is available on `uicgpu` (see `TOOLS-COMPUTE.md` — Geant4-DNA standard build site).
I therefore performed **five non-MC audits** in `code/reproduce.py` that do not require running
the physics but exercise the *reported numbers* and the *post-MC damage-classification logic*:

| # | Audit                                                                 | Result |
|---|-----------------------------------------------------------------------|--------|
| 1 | Table 2 row-sums close to 100% AND SSBc / DSBc match stated definition | **PARTIAL** (see §3) |
| 2 | Table 3 worked-example: 100–150 eV bin → 1.39 SSBall, 0.16 DSBall/event | **PASS** |
| 3 | Table 5 yield-from-distribution for 2 MeV: recompute Σ n(E,y)P(E,y)/y  | **PASS** |
| 4 | Table 5 (Gy·Gbp)⁻¹ × (22×245 Mbp/1000) → (Gy·cell)⁻¹ all 5 energies     | **PASS** |
| 5 | Python re-implementation of the Fig. 2 / Nikjoo classifier (8 cases)   | **PASS** |

### 2a. Numbers from my run
```
(2) 100–150 eV bin: SSBall = 2663, DSBall = 315
    per-event SSBall = 1.392  (paper: 1.39)   ✓
    per-event DSBall = 0.165  (paper: 0.16)   ✓

(3) Y_SSB(2 MeV) recomputed = 61.93 (Gy·Gbp)^-1   [paper col-4: 62.72,  Δ -1.3%]   ✓
    Y_DSB(2 MeV) recomputed =  6.15 (Gy·Gbp)^-1   [paper col-5:  6.38,  Δ -3.6%]   ✓

(4) 5.39 Gbp/cell × Y_(Gy·Gbp)^-1 → Y_(Gy·cell)^-1 for all 5 energies:
    every entry matches paper Table 5 to ≤ 0.01%   ✓

(5) Classifier reproduces NB, SSB, SSB+, 2SSB (same-strand & opposite-strand), DSB, DSB+, DSB++ ✓
```

Audit (3) is the strongest single check: starting from the paper's own Table 3 (event
counts) and Table 4 (P(E,y) hit densities) I recover Y_SSB and Y_DSB at 2 MeV to within
~3%, which is consistent with the bin-midpoint approximation the paper itself flags as
the cause of small discrepancies between cols 2,3 and cols 4,5 of Table 5. This confirms
the data-processing pipeline downstream of the MC is **internally consistent**.

Audit (4) is the strongest unit check: the cell-normalization factor 5.39 Gbp/cell is the
*only* thing connecting the (Gy·Gbp)⁻¹ and (Gy·cell)⁻¹ columns, and every entry agrees
exactly. So the cell-level numbers are simply the per-Gbp numbers ×5.39 with no hidden
correction.

Audit (5) reproduces the *algorithmic* part the paper says was written in Python — the
post-MC classifier. This is the half of the simulation I *can* actually rerun, and it
behaves identically to the spec.

---

## 3. Discrepancy / paper-side issue (Audit 1)

The paper's Table 2 caption defines:
> *complex damage has been defined as SSBc (= SSB+ + 2SSB) and DSBc (= DSB+ + DSB++).*

But arithmetically the columns disagree with the literal definition:

| E (MeV) | SSB+ + 2SSB | SSBc (paper) | DSB+ + DSB++ | DSBc (paper) |
|---------|-------------|--------------|--------------|--------------|
| 0.5     | 21.48       | 42.33        | 12.38        | 54.63        |
| 1       | 17.27       | 35.66        | 6.08         | 44.45        |
| 2       | 12.52       | 29.19        | 2.04         | 30.42        |
| 10      | 6.76        | 19.81        | 0.50         | 19.40        |
| 20      | 5.05        | 16.67        | 0.26         | 14.65        |

I tested several other hypotheses (2× weighted; (100 − NB − SSB); SSB+ + 2SSB + DSB; per-SB
fraction) — none fits all five rows. **The reported SSBc and DSBc columns are inconsistent
with the stated formula and with each other.** Possible explanations: (a) the columns are
yields in undocumented units rather than percentages, (b) the caption formula is mis-stated
and the actual formula counts something else (perhaps weighted by SBs per cluster *plus*
indirect-direct double counting), (c) a transcription / typesetting error.

This does **not** invalidate Table 5 or Figure 3 (which use Y_SSB and Y_DSB columns that
I *did* verify), but it does mean a downstream user cannot rebuild the SSBc/DSBc columns
from the published frequencies, and any work building on those complexity percentages must
flag this. It is a **6/22-rule reproducibility blocker for the complexity-fraction claim**
specifically.

---

## 4. What is NOT reproducible from the paper alone

This is the place a future runner on `uicgpu` would have to fill in to reproduce
Table 2 / Figure 3 / Figure 4 from scratch. **Missing artifacts** (the precise
6/22 list):

1. **B-DNA PDB file** — the paper says they "extracted the position of the atoms of a 216 bp
   long double helix B-DNA from a PDB file" but never names the PDB ID, source, sequence,
   or provides a deposit. A reader cannot reconstruct the exact atom positions used to
   define the 2.3-nm DNA cylinder or the sugar/phosphate volumes for E_ssb thresholding.
2. **The Python damage-formation script** — referenced in Methods as the classifier that
   produces Table 2 / Fig. 2; not deposited. (My `classify_segment()` reimplements it
   from the figure but cannot be byte-equivalent without the source.)
3. **µ-randomness sampling N** — the paper says they found "an optimized number of DNAs"
   that met the 5% Z̄_f⁻¹ vs f(>0) criterion, but does not give that N. The total damage
   counts therefore cannot be re-normalized exactly.
4. **Geant4-DNA macro / physics-list flags** — only "Geant4 version 10.3" + "default
   processes" are named. Which `G4EmDNAPhysics_optionN` constructor (option0 vs option2
   vs option4) was used materially changes the cross-section set; not specified.
5. **Chemistry-stage configuration** — `TimeStepAction` is referenced but the exact
   `G4DNAChemistry*` builder, scavenger model toggles, and OH• diffusion coefficient
   choice are not given. (The paper *does* state no explicit scavenger model and 1 ns
   chemistry, which is enough to constrain the choice, but not to reproduce byte-for-byte.)
6. **Per-event simulation seed / output dataset** — 5×10³ events × 5 energies = 25,000
   primaries. No raw output / energy-deposit list is deposited, so independent re-binning
   of Table 3 / Table 4 is impossible.
7. **Definition of SSBc / DSBc** — see §3.
8. **Per-segment cylinder geometry tolerance** — the (8 + 2.3) nm cylinder is given
   geometrically but the orientation of each sampled DNA inside the 100 nm water sphere
   is not described; an isotropic orientation distribution is implied but not stated.

If those eight items were deposited (PDB file + macro + classifier `.py` + raw events
JSON), a third party with Geant4-DNA on `uicgpu` could reproduce Table 2 directly.

---

## 5. Reasoning for the grades

### Coverage = 6/10
- ✓ I extracted the full method, identified all key parameters (E_ssb, P_OH, 10 bp window,
  216 bp segment, 100 nm water sphere, 1 ns chemistry, 22 chr × 245 Mbp).
- ✓ I reproduced four downstream / arithmetic claims (Table 3 worked example, Table 5 yield
  formula at 2 MeV, Table 5 unit conversion for all 5 energies, Fig. 2 classifier).
- ✗ I did not (and cannot here) run Geant4-DNA. The MC stage that *generates* Table 2
  is the actual scientific computation, and I only audit its outputs, not regenerate them.
- ✗ I did not regenerate Figure 3 (DSB-yield-vs-LET comparison plot) because the comparison
  data from Nikjoo / Friedland / Meylan / Frankenberg / Belli / Campa are external curves
  not tabulated in this paper.
- Net: an honest middle grade for an MC-engine-dependent paper.

### Agreement = 8/10
- All four audits that *could* succeed did succeed, with errors ≤3.6% on the yield
  recomputation (and the paper itself attributes that residual to mid-bin energy choice).
- The unit-conversion check is exact to ≤0.01%.
- The classifier matches all eight category definitions.
- The single discrepancy (Table 2 SSBc/DSBc columns) is a *paper-side* internal
  inconsistency, not a disagreement with my analysis. I document it transparently.

### MANDATORY 6/22 verdict
The paper is **partially reproducible**. The published numbers are self-consistent in
Tables 3, 4, and 5 and the cell-yield conversion. The MC stage is blocked by missing
artifacts (#1, #2, #3, #4, #5, #6 above). The complexity-class column (Table 2 SSBc/DSBc)
is blocked by the §3 inconsistency. Anyone wanting to *use* the complexity fractions
should request the authors' PDB file and Python classifier first.

---

## 6. Files produced
- `source/paper.pdf` — local copy of the harvested PDF
- `code/reproduce.py` — five-audit reproduction script (Python 3, no deps)
- `evidence/reproduce.log` — full stdout from the script
- `report/REPORT.md` — this file

Run: `python3 code/reproduce.py`

---

*Subagent s100-042 · model argo:claude-opus-4.7 · 2026-06-25*
