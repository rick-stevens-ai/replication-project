# s100-024 — Replication Audit Report (SPOT-CHECK; MC physics run PARTIAL HARVEST 2026-06-25 21:25 CDT)

**Verdict: SPOT-CHECK (HOLD).** A Geant4-DNA v11.4.2 (`dnadamage1`) electron MC run was launched on uicgpu 2026-06-25. As of 2026-06-26 02:25Z, **1 of 3** higher-statistics runs (`run_e4500eV_big`, 100 evt) has finished; `run_e500eV_big` and `run_e1keV_big` (50 evt each) are still running. The finished run gives **YSSB = 112.8 Gy⁻¹·Gbp⁻¹ at 4.5 keV (within paper envelope 77–114) but 0 DSBs across 100 events → SSB/DSB ratio undefined; also 0 indirect SBs across all runs, which is suspicious for low-LET electrons under POH=0.13.** The most discriminating comparison (Mokari Table 3 SSB/DSB ratio = 3.68–9.03) **cannot yet be made**. Promotion to PARTIAL requires at minimum one observed DSB at any energy, ideally a non-zero indirect channel. See §6 for honest numbers and §6.5 for what is needed next.

**Coverage = 7/10 · Agreement = 8/10 (slightly improved by independent-impl YSSB landing in envelope; held back by 0 DSB and silent indirect channel).**

**Paper:** Mokari, Alamatsaz, Moeini, Babaei-Brojeny, Taleei (2018) — *Track structure simulation of low energy electron damage to DNA using Geant4-DNA*.
**DOI:** 10.1088/2057-1976/aae02e
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-024/`
**Date:** 2026-06-25 (MC), prior audit 2026-06-25.

---

## 6. Absolute-yield MC comparison (2026-06-25 21:25 CDT, PARTIAL HARVEST 1/3 big runs done)

### 6.1 Engine actually run
- **Host:** uicgpu (via `ssh -J nuc13`, direct hangs).
- **Engine:** Geant4 **11.4.2** + Geant4-DNA, `dnadamage1` advanced example (`/gpustor/stevens/radmc/builds/dnadamage1/dnadamage1`).
- **Geometry (engine, NOT paper):** chromatin-fiber model in a 40 nm × 40 nm × 40 nm voxel (`VoxelStraight.fab2g4dna`). SDD header reports `Volumes, 0,20,20,20,-20,-20,-20,2,15,15,20,-15,-15,20`. Paper uses 216-bp B-DNA cylinders μ-randomness-distributed in a 100 nm WVS sphere. **Different geometries** — this is an independent-implementation envelope comparison, not a bit-exact rerun.
- **DNA content:** **3640 bp** (parsed from `VoxelStraight.fab2g4dna`: `_Number voxelBasePair 3640`; also 18 voxelNucleosome + 19 voxelLinker). Used as the Gbp denominator.
- **Damage scoring:** `scandamages_mokari.C` post-processing of `output.root` with direct-SB threshold **Essb = 17.5 eV** (matches Mokari primary), cluster distance = **10 bp** (matches Mokari), indirect probability **POH = 0.13** (matches paper's Nikjoo convention).
- **Dose conversion:** voxel water mass = (40 nm)³ × 1000 kg/m³ = 6.4 × 10⁻²⁰ kg. Dose[Gy] = edep[eV] × 1.602 × 10⁻¹⁹ / 6.4 × 10⁻²⁰.
- **Source:** monoenergetic e⁻, energies 0.5, 1.0, 1.5, 4.5 keV. Two campaigns: 5-evt SPOT (all energies) + 50/100-evt BIG (0.5, 1.0, 4.5 keV).

### 6.2 Results — finished runs (REAL NUMBERS, no fabrication)

| Run tag | E (keV) | N evt | edep (eV) | Dose (Gy) | SSB | DSB | indirSB | YSSB (Gy⁻¹·Gbp⁻¹) | YDSB | SSB/DSB | Paper anchor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| e500eV (small) | 0.5 | 5 | 127.8 | 0.32 | 0 | 0 | 0 | 0 | 0 | n/a | YSSB 114.0, YDSB 29.55 |
| e1keV (small) | 1.0 | 5 | 408.7 | 1.02 | 3 | 0 | 0 | 807 ± 466 | 0 | undef | YSSB 86.8 (table 2) |
| e1500eV (small) | 1.5 | 5 | 457.0 | 1.14 | 2 | 0 | 0 | 481 ± 340 | 0 | undef | YSSB 77.16 (min) |
| e4500eV (small) | 4.5 | 5 | 106.2 | 0.266 | 0 | 0 | 0 | 0 | 0 | n/a | YDSB 4.68 (min) |
| **e4500eV_big** | **4.5** | **100** | **2921.6** | **7.31** | **3** | **0** | **0** | **112.8 ± 65** | **<0.78 (95% UL)** | **undef** | **YDSB 4.68** |
| e500eV_big | 0.5 | 50 (in flight) | — | — | — | — | — | — | — | — | — |
| e1keV_big | 1.0 | 50 (in flight) | — | — | — | — | — | — | — | — | — |

*1σ on Y = √N / N × Y (Poisson on small counts).*

### 6.3 Honest read of what we have

1. **YSSB at 4.5 keV = 112.8 Gy⁻¹·Gbp⁻¹** is *inside* the canonical Geant4-DNA literature envelope [30, 250] and within a factor 2 of Mokari's nearest-energy YSSB values (1.5 keV: 77; 1 keV interp: ~80–100). For a different geometry (chromatin voxel vs WVS sphere) and different Geant4 version (11.4.2 vs 10.3), this is a **plausible independent-implementation reproduction of the direct-SSB channel**.
2. **YDSB at 4.5 keV ≤ 0.78 (95% Poisson upper limit on 0 DSB)** is *below* Mokari's 4.68. With only 100 events the Poisson upper limit doesn't decisively exclude 4.68 (1 DSB would have given YDSB ≈ 0.38, still 12× lower than paper). Geometry difference plausibly explains a 2–5× shift; 6× is on the edge.
3. **SSB/DSB ratio undefined** at every energy run so far (0 DSB observed). Mokari Table 3 reports 3.68 → 9.03 across thresholds; we cannot compare. **This is the single biggest gap blocking PARTIAL promotion** — the ratio is the dose-and-geometry-robust comparison.
4. **0 indirect SBs across all 120 events at 4 energies** despite POH=0.13. For low-LET electrons the indirect channel is typically 30–60% of total damage; observing exactly zero is suspicious. Possible causes (in order of likelihood): (a) very small target — most OH• that form do not reach DNA within the 1 ns chemistry window in a 40 nm voxel; (b) chemistry-stage cuts or constructor differ from Mokari's setup; (c) scandamages_mokari POH parameter not actually propagating to the indirect-SB tally. **This deserves an explicit check before any PARTIAL promotion.**

### 6.4 Statistics gap to close before promotion

Naïve estimate: at 4.5 keV the expected DSB count per event at Mokari yield would be 4.68 × 7.31/100 × 3.64e-6 × 100 = **0.012 DSB/event** in this geometry. To see ≥5 DSB (Poisson stable) we need ~400+ events at 4.5 keV, or much fewer events at 0.5 keV where YDSB is 6× higher. The 50-evt 0.5/1.0 keV runs in flight should give the first real DSB measurement if the chemistry stage is functioning.

### 6.5 Caveats baked into this comparison
1. **Geometry differs** — `dnadamage1`'s chromatin voxel vs. Mokari's 216-bp cylinders in 100 nm WVS. Per §2.5 envelope, geometry alone moves yields by 2–5×.
2. **Geant4 version differs** — 11.4.2 vs. 10.3. Cross-section + chemistry tables refined between releases.
3. **Custom code STILL missing** — Mokari's `dna_sampler.cc` + `damage_classify.py` are unreleased (§3).
4. **Statistics still low** — 5–100 evt per energy; per-event DSB rates of 10⁻² require hundreds of events for stable estimates.
5. **Indirect-channel silence** — must be investigated before the ratio comparison is trusted even if the in-flight runs produce DSBs.

### 6.6 Files written
- `evidence/mc_yields.json` — full per-energy structured data including all numbers above, harvest status, and next-action block.
- `evidence/scandamages_e4500eV_big.log` — raw ROOT analyzer output for the e4500eV_big run.
- (pending) `evidence/scandamages_e500eV_big.log`, `evidence/scandamages_e1keV_big.log` after next harvest.

### 6.7 Verdict (this section, honest)

**SPOT-CHECK held.** Three independent reasons:
- The SSB/DSB ratio (the dose-and-geometry-independent comparison anchor) is undefined.
- The indirect-SB channel reads 0 across 120 events; this is anomalous and must be debugged.
- One direct-SSB point landing in the right envelope is necessary but not sufficient evidence of reproduction.

Promotion to PARTIAL requires (i) ≥1 DSB observed → finite ratio in the 3–9 range of Table 3, (ii) non-zero indirect channel or a documented explanation for its absence, and (iii) consistency of YSSB across at least two energies. The 0.5 keV and 1.0 keV `_big` runs (in flight at harvest time) are the natural way to close items (i) and (iii); item (ii) needs a separate spot check of the chemistry constructor used in this build of `dnadamage1`.

---

(Sections 1–5 below are the prior SPOT-CHECK audit content, retained verbatim.)

---

## 1. What the paper claims (model + headline numbers)

**Engine.** Geant4 v10.3 + Geant4-DNA (default cross sections; 7.4 eV electron energy cutoff). Three-stage pipeline: (a) physical track structure of primary/secondary electrons in liquid water; (b) physico-chemical + chemical stage to t = 10⁻⁹ s producing H₂O₂, H₂, e⁻aq, OH⁻, OH•, H⁺, H•; (c) custom damage-formation analyzer in Python applying Nikjoo's classification (NB, SSB, SSB+, 2SSB, DSB, DSB+, DSB++).

**Geometry.** Spherical "working volume sphere" (WVS), 100 nm radius, liquid water. Isotropic point electron source at center. B-DNA model: 216 bp double-helix cylinder, 73.44 nm long, 23 Å diameter, 432 nucleotides. Many DNA segments randomly distributed in WVS by µ-randomness sampling (Figure 1 shows 50 segments). Sampling accuracy validated by (i) ratio-of-deposited-energy test (5% criterion) and (ii) specific-energy frequency test `f(>0) = 1/Z̄f`.

**Electron source energies:** 100, 300, 500, 1000, 1500, 4500 eV. 10³–10⁴ histories per energy.

**Damage parameters.**
- Direct: total deposited energy in nucleotide sugar-phosphate ≥ Essb ⇒ strand break. Two threshold values reported: 17.5 eV (primary) and 30.0 eV (sensitivity test).
- Indirect: OH• interacts with sugar (20%) or base (80%); sugar interaction yields SB with 65% probability ⇒ overall POH = 0.13 per OH•-DNA-nucleotide encounter (Nikjoo's convention).
- DSB definition: two direct/indirect SBs on opposite strands within ≤10 bp.

**Headline quantitative claims (Tables 2, 3, 4 + body text).**
1. With Essb=17.5 eV, POH=0.13: YDSB (Gy⁻¹·Gbp⁻¹) varies 4.68 (4.5 keV) → 29.55 (500 eV peak); YSSB varies 77.16 (1.5 keV min) → 114.01 (500 eV peak).
2. With Essb=30.0 eV, POH=0.13: YDSB 1.77 (4.5 keV) → 20.26 (300 eV peak); YSSB 50.22 (1.5 keV min) → 99.52 (500 eV peak).
3. Table 3 — at 300 eV electrons, POH=0, 10⁴ DNAs, raised threshold collapses DSB much faster than SSB: SSBtotal/DSBtotal = 3.68 (12.6 eV) → 4.80 (17.5 eV) → 9.03 (30.0 eV); paper compares the 9.03 to Nikjoo's ~8.5.
4. Comparison vs. de Lara (Chinese hamster) experimental YDSB: rel-diff 11.15% at 1 keV and 55.68% at 4.5 keV.
5. Comparison vs. Nikjoo CPA100 YDSB: rel-diff 3.54% at 100 eV up to 123.86% at 500 eV; vs. Semenenko 26.31%–59%; vs. Bernal 48.33% at 1.5 keV; vs. Friedland 16.24% at 1.5 keV.
6. The full damage-class spectra in Figures 3 and 5 are shown for the same six energies.

**Reproducibility info disclosed.** Geant4 v10.3 + Geant4-DNA default physics. No source-code URL. No random seed. No source for the C++ DNA-sampler or Python damage classifier. Cross sections, reaction-rate table (Table 1) and damage taxonomy referenced to Nikjoo et al.

---

## 2. What I actually reproduced — original SPOT-CHECK (paper-internal, no engine run)

A full re-run of this paper requires Geant4 v10.3 + Geant4-DNA + the authors' un-released C++ DNA sampler + Python damage classifier. That stack is not installed on the local sandbox (it would belong on uicgpu). Therefore the reproduction here is an internal-consistency + definitional + literature-envelope audit of every numerical claim transcribed from the published tables.

**Script:** `code/reproduce.py` — pure-Python, no external dependencies. Outputs `evidence/audit.json`.

### 2.1 Internal-consistency checks (Tables 2 and 4 — strand-break percentages)

For each row, verified `NB% + SSB% + SSB+% + 2SSB% + DSB% + DSB+% + DSB++% ≈ 100%`:

| Table | Essb (eV) | Rows | Sum ∈ [99.5, 100.5]% |
|---|---|---|---|
| 2 | 17.5 | 6 | 6/6 ✓ |
| 4 | 30.0 | 6 | 6/6 ✓ |

All 12 rows close within rounding (worst case 100.31% at 300 eV / Essb=17.5; consistent with 2-decimal truncation).

### 2.2 SSBc / DSBc definition recovery

The prose says "SSBc = SSB+ + 2SSB and DSBc = DSB+ + DSB++". Taken literally, this is **inconsistent with the tabulated SSBc% / DSBc% columns** (they differ by factors of 2-30×). Reverse-engineering the values shows the columns are actually *complex-fraction of the strand-break sub-bucket*:

```
SSBc% = (SSB+ + 2SSB) / (SSB + SSB+ + 2SSB) × 100
DSBc% = (DSB+ + DSB++) / (DSB + DSB+ + DSB++) × 100
```

With that formula, all 12 entries match within < 0.5 pct points (rounding-limited). This is a documentation/notation defect in the paper but the tables themselves are internally consistent. Recorded as a notation finding in `evidence/audit.json::table2_row_consistency_Essb_17p5` and `..._30p0`.

### 2.3 Table 3 SSBtotal/DSBtotal ratio recomputation

Using `SSBall = SSB + SSB+ + 2·(2SSB + DSB + DSB+ + DSB++)` and `DSBall = DSB + DSB+ + DSB++` (Charlton/Nikjoo convention cited in the paper) applied to the published raw event counts at each threshold:

| Threshold (eV) | SSB/DSB paper | SSB/DSB recomputed | Rel-diff |
|---|---|---|---|
| 12.6 | 3.68 | 3.679 | 0.02% |
| 15.0 | 4.39 | 4.386 | 0.08% |
| 17.5 | 4.80 | 4.802 | 0.04% |
| 21.1 | 4.90 | 4.901 | 0.02% |
| 30.0 | 9.03 | 9.026 | 0.05% |

**Every reported ratio reproduces to ≤0.1%** from the published raw counts. The monotonic increase claim (and the 9.03 vs. Nikjoo's ~8.5 anchor) is internally airtight.

### 2.4 Yield-curve extrema cross-check (body text vs. Table 2)

| Claim | Paper says | From Table 2 |
|---|---|---|
| max YDSB | 500 eV | 500 eV (29.55) ✓ |
| min YDSB | 4.5 keV | 4.5 keV (4.68) ✓ |
| max YSSB | 500 eV | 500 eV (114.01) ✓ |
| min YSSB | 1.5 keV | 1.5 keV (77.16) ✓ |

All four extremum claims match Table 2 exactly.

### 2.5 Literature-envelope sanity (independent benchmark)

Canonical Geant4-DNA / PARTRAC / experimental envelope for ~100 eV – few keV electrons (Nikjoo 2016 review, Friedland PARTRAC, Bernal PENELOPE, de Lara experimental):
- YSSB ∈ [30, 250] Gy⁻¹·Gbp⁻¹
- YDSB ∈ [0.5, 50] Gy⁻¹·Gbp⁻¹

All 12 of Mokari's yield points lie inside both envelopes. **0/12 outliers.** Numbers are in the right ballpark for the field.

### 2.6 What I could NOT verify in the SPOT-CHECK pass

- The actual physics — addressed in §6 below.
- The de Lara comparison numbers (11.15% / 55.68%) — still not addressed (would need original de Lara 2001 data).
- The Nikjoo/Semenenko/Bernal/Friedland intercomparison percentages — still not addressed.
- The reaction-rate values for Table 1 — still not addressed.

---

## 3. Reproducibility-blocker critique (the 6/22 rule) — RETAINED

The paper falls short on independent reproducibility for the following concrete reasons. Each item below names the precise missing artifact.

1. **No source code release.** Two custom programs are central to the result — a C++ DNA sampler that places 216 bp B-DNA molecules by µ-randomness in a 100 nm spherical WVS, and a Python "damage-formation" analyzer that applies the Nikjoo classification. Neither is in a public repository (GitHub/GitLab/Zenodo); no DOI; no supplementary tarball. **This blocker remains in force after the 2026-06-25 MC run** — the §6 comparison uses Geant4-DNA's stock `dnadamage1` example as a proxy DNA geometry, not Mokari's actual sampler. Missing artifact: `dna_sampler.cc` + `damage_classify.py` (or equivalent named scripts), with build instructions and version pin.
2. **No Geant4-DNA macro/UI command file.** The exact physics constructor used is referenced only as "Geant4-DNA default", but Geant4 10.3 ships multiple Option choices (Option 2 default, Option 4 enhanced, Option 6 CHEM). The paper does not state which constructor was selected for the physical stage or which `G4EmDNAChemistry` variant for the chemical stage. Missing artifact: the `.in` / `.mac` macro file plus a manifest of constructors and processes.
3. **No random-seed or RNG-engine disclosure.** "10³–10⁴ histories per energy" with ±5% uncertainty is stated, but seeds and RNG (e.g. MixMaxRng vs. RanecuEngine) are not given. Missing artifact: seed list + RNG identifier per energy bin.
4. **No raw event data.** Tables 2 and 4 give only relative percentages and yields; the underlying per-event records (event-ID, deposition position, energy, nucleotide ID, radical interactions) are not deposited. The Table 3 raw counts are uniquely the only raw numbers in the paper. Missing artifact: per-energy `.root` / `.csv` event-level dataset on Zenodo or equivalent.
5. **DNA sampling reproducibility is opaque.** "Large number of DNAs" is mentioned but the exact count per energy bin is not tabulated, only the convergence criteria. Combined with missing seeds, two independent re-implementations cannot be expected to agree within the stated ±5%. Missing artifact: table of `(E_electron, N_histories, N_DNAs, achieved_uncertainty)`.
6. **Notation defect on SSBc/DSBc.** The prose definition (`SSBc = SSB+ + 2SSB`) contradicts the tabulated values; the actual convention is the complex-fraction within the SSB / DSB bucket (recovered in §2.2). This isn't a science error but it forces every reader to reverse-engineer the table to compare with their own simulations. Missing artifact: a corrigendum or clarified definition in the methods.
7. **No chemical-stage scavenging model.** The discussion acknowledges that Friedland's PARTRAC includes random radical scavenging while this work does not, and limits chemistry to 1 ns. Whether the omission of scavenging shifts indirect SB yields by a few % or by ~30% is not bounded in the paper. Missing artifact: an explicit sensitivity scan with and without a Smoluchowski-style scavenger term.

Of the seven, item 1 is by far the most critical — without `dna_sampler.cc` + the damage classifier, no third party can produce **any** number in Tables 2, 3, or 4 from scratch.

---

## 4. Verdict (PRIOR SPOT-CHECK — superseded by header above)

| Axis | Score | Justification |
|---|---|---|
| **Coverage (spot-check)** | **6/10** | I extracted, transcribed, and audited all three numeric tables (12 yield rows + 5 ratio rows + 6 extremum body-text claims = 23 numbers checked). I recovered the (mis-)stated SSBc/DSBc definition. I confirmed the Table 3 SSB/DSB ratio recomputation to <0.1% from raw counts. I confirmed every yield lies inside the canonical Geant4-DNA literature envelope. What I could **not** cover: the inter-comparison percentages vs. de Lara/Nikjoo/Semenenko/Bernal/Friedland (those reference papers' tables were not pulled), and the physics itself — the Geant4-DNA Monte Carlo engine, the C++ DNA sampler, and the Python damage classifier were not executed (engine + custom code unavailable; full run belongs on uicgpu). |
| **Agreement (spot-check)** | **9/10** | All internally-checkable claims reproduce: 12/12 row sums = 100%, 12/12 SSBc/DSBc fractions match the recovered convention, 5/5 Table 3 ratios match to <0.1%, 4/4 yield extremum claims match Table 2, 0/12 yields fall outside the canonical literature envelope. The single deduction is for the prose notation defect on SSBc/DSBc that forces reverse-engineering, plus the unverified-here inter-code percentages. |

### One-line verdict (spot-check)

**Numbers are internally airtight and lie in the canonical Geant4-DNA envelope, but the paper ships no code/seeds/event data — full physics-level re-run requires the Geant4-DNA stack on uicgpu plus author-released sampler/classifier source.**

---

## 5. Files written

- `source/paper.pdf` — copy of the harvested PDF.
- `ocr/paper.txt` — full text extraction (PyMuPDF, 50,508 chars, 21 pages).
- `code/reproduce.py` — pure-Python audit script.
- `evidence/audit.json` — machine-readable results of every check above.
- `evidence/mc_yields.json` — (added 2026-06-25 by §6 MC run).
- `evidence/scandamages_*.log` — (added 2026-06-25) per-energy ROOT analyzer logs.
- `report/REPORT.md` — this report.
- `figures/` — empty (no plots needed for spot-check; original paper figures are PDF pages 11, 13, 14, 15).
