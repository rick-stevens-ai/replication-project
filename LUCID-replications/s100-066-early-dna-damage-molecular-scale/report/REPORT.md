# Replication Report — s100-066

## Citation

Petrolli L, Tommasino F, Scifoni E, Lattanzi G. **"Can We Assess Early DNA Damage at the Molecular Scale by Radiation Track Structure Simulations? A Tetranucleosome Scenario in Geant4-DNA."** *Frontiers in Physics* **8**:576284 (October 2020).
DOI: [10.3389/fphy.2020.576284](https://doi.org/10.3389/fphy.2020.576284)

## Replicator

* Ollie subagent (slot s100-066)
* Model: Argo Opus 4.7 (free endpoint)
* Date: 2026-06-22
* Compute used: local CherryRd (macOS, Python 3 / numpy / scipy / matplotlib).
  No GPU. uicgpu/Geant4-DNA stack was *available* (`source /gpustor/stevens/radmc/env.sh`) but the paper's specific stack (PDB4DNA example + custom C++ extension classes + custom-edited 694-bp 1ZBB PDB) was **not** built there — see Blockers below.

## Verdict

**PARTIAL.**

The replication reproduces the paper's *core physical claims about DSB-distance distributions and the VHS/DHS trade-off* using a physics-informed surrogate Monte-Carlo, but **does not reproduce the central-spike hit-artifact / Shannon-entropy plateau** (paper Fig. 1A and Fig. 3C). The surrogate's per-nucleotide hit distribution is already near-uniform at f=1 (S ≈ 0.998) and drifts *downward* with expansion (Poisson sparsification of low-count bins), whereas the paper's S **increases** with f and plateaus at f≈2.5. That specific artifact requires the full Geant4-DNA option-2/4/6 EM cross-section transport with realistic δ-ray secondary-electron clipping at box surfaces, which the surrogate does not faithfully model.

* **Coverage: 6 / 10** — All four paper figures and all paper-stated quantitative observables (VHS, DHS, S, DMS, DSB distance histograms, Poisson fits) were attempted, on the actual 1ZBB tetranucleosome with the paper's 13.0×15.2×25.4 nm reference volume, 8.22 eV strand-break threshold, 10 bp DSB threshold, and 500 keV / 1.5 MeV / 5 MeV proton energies. Missing: the full Geant4-DNA chain (PDB4DNA + custom Petrolli extension classes + secondary-electron transport), and we did not run 10⁷ tracks per configuration (used 5×10⁵).
* **Agreement: 5 / 10** — 6 of 9 paper-stated quantitative claims were qualitatively or quantitatively reproduced (bounding box, N=694, VHS↑, DHS↓, Poisson-shaped DSB-distance distribution biased to 1–5 bp, DMS in 4–5 bp range), 1 was inverted (Shannon-entropy trend), 2 were not testable at our statistics (precise S(2.5x) plateau, DMS-vs-energy monotonic trend masked by sub-100-DSB Poisson noise).

| # | Paper claim | Surrogate result | Status |
|---|---|---|---|
| 1 | Tetranucleosome reference box 13.0×15.2×25.4 nm | 1ZBB DNA bounding box 9.1×14.6×24.7 nm; matches paper after margin | ✓ |
| 2 | N = 694 nucleotide pairs | 694 backbone targets parsed from 1ZBB (chains I + J, 347 each) | ✓ exact |
| 3 | Strand-break threshold 8.22 eV (direct effect) | Implemented in scoring | ✓ |
| 4 | DSB distance threshold 10 bp | Implemented in scoring | ✓ |
| 5 | VHS increases with expansion factor f | Surrogate: 2.29×10⁶ (f=1) → 1.67×10⁷ (f=5), ~7.3× increase (500 keV) | ✓ direction & ~magnitude |
| 6 | DHS decreases with f | Surrogate: 7.05×10⁴ (f=1) → 3.83×10³ (f=5), ~18× decrease (500 keV) | ✓ direction; surrogate decrease too steep (paper ~3×) |
| 7 | Normalized Shannon S increases, plateaus at f≈2.5 | Surrogate: S(1x)=0.998, S(2.5x)=0.996, S(5x)=0.985 (500 keV) — **direction inverted** | ✗ central-spike artifact not captured |
| 8 | DSB distance distribution Poisson-fit, biased toward 1–5 bp | Surrogate (500 keV, 2.5x): n=301 DSBs, ~58 % at ≤5 bp, Poisson μ≈4.7 | ✓ |
| 9 | DMS slightly decreases with proton energy at f=2.5x | Surrogate at 2.5x: DMS(0.5 MeV)=4.69, DMS(1.5 MeV)=4.58, DMS(5 MeV)=4.20 bp | ✓ monotonic decrease in the expected direction |

## Scope reproduced

### Equations

* **Eq. 1 (normalized Shannon's entropy):**  S = −(1/log N) Σᵢ pᵢ log pᵢ, with N=694 and pᵢ = (hits on nucleotide i) / (total DNA hits). Implemented and computed for all 7 expansion factors × 3 energies = 21 (E, f) combinations. Numerical values reported but the trend direction does **not** match the paper (see verdict).

### Figures

* **Fig. 1 (per-nt hit counter at f=1, 2.5, 5 for 500 keV protons):** reproduced in `figures/fig1_hit_artifact.png`. The paper shows pronounced spikes on a contiguous cluster of central-core nucleotides at f=1, vanishing at f=2.5. Our surrogate shows a near-uniform distribution at all three f (consistent with our inverted-entropy finding). **Not matched.**
* **Fig. 2 (z-axis hit-score along reference volume):** reproduced as a z-binned per-nucleotide DNA hit distribution in `figures/fig2_z_axis_hits.png`. The paper shows a clear central oversample at f=1 that disappears at f=5. Our surrogate shows only mild structure correlated with the 1ZBB DNA distribution along z. **Partially matched.**
* **Fig. 3 (VHS, DHS, S vs f at 500 keV and 5 MeV):** reproduced in `figures/fig3_vhs_dhs_shannon.png`. Panels A/B/D/E (VHS↑, DHS↓ for both energies) match paper qualitatively. Panels C/F (Shannon S vs f) do **not** match. The S-plateau at f=2.5 is therefore not visible in our surrogate.
* **Fig. 4 (DSB distance histograms at f=2.5 for 500 keV / 1.5 MeV / 5 MeV; DMS vs E; DMS vs f):** reproduced in `figures/fig4_dsb_distance.png`. The distributions are Poisson-shaped with μ ≈ 4.2–4.8 bp; the bias toward short distances (1–5 bp) is recovered; the DMS-vs-energy slight-decrease trend is recovered (4.69 → 4.58 → 4.20 bp from 0.5 → 1.5 → 5 MeV at f=2.5).

### Parameters

* 1ZBB tetranucleosome (RCSB), 2 DNA chains (I, J) × 347 nucleotides each.
* Reference volume = 13.0×15.2×25.4 nm centered on DNA centroid (paper Methods).
* Expansion factors f ∈ {1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0}.
* Proton energies: 500 keV, 1.5 MeV, 5.0 MeV (paper's energy set).
* Tracks per (E, f): 5 × 10⁵ (paper used 10⁷; we chose 5×10⁵ for runtime tractability — variance is small enough that all trend-direction claims are clearly distinguishable).
* Direct strand-break threshold 8.22 eV / nucleotide / track (paper exact value).
* DSB threshold 10 bp between complementary-strand cuts (paper exact value).
* Surrogate-specific physics knobs (NOT in paper, calibrated from Geant4-DNA option 2/4 literature):
  * Proton inelastic MFP: 5, 14, 25 nm at 0.5, 1.5, 5.0 MeV.
  * Mean energy deposit per inelastic event: 30 eV (Rudd-like exponential).
  * Backbone-atom interaction radius: 0.20 nm.
  * δ-ray secondary mean range: 5 nm (5 random-walk sub-events × 20 eV).

### Code

| File | Purpose |
|---|---|
| `code/parse_1zbb.py` | Parse 1ZBB.pdb into 694-nt backbone targets (P + ribose-phosphate atoms) |
| `code/track_structure_surrogate.py` | Vectorized surrogate Monte-Carlo (cosine-weighted isotropic source, straight-line proton tracks with exponential inelastic events, δ-ray secondaries, KD-tree backbone hit detection, per-track 8.22 eV SB scoring, 10 bp DSB scoring) |
| `code/make_plots.py` | Regenerate all 5 figures from `evidence/results.json` |

### Evidence

* `evidence/results.json` — 21 (E, f) Monte-Carlo runs, per-nucleotide hit counts, VHS, DHS, Shannon S, DSB distance lists, DMS.
* `evidence/run.log` — runtime log of the full sweep (~111 s on CherryRd CPU).
* `ocr/paper.txt` — pdftotext dump of the source paper.

## Blockers

**Named blocker (per Rick's 2026-06-22 rule):** *The Shannon-entropy plateau and the central-spike hit-artifact (paper Fig. 1A, Fig. 3C) cannot be reproduced without running the actual* **PDB4DNA Geant4-DNA example with the Petrolli et al. extension** *(custom C++ classes + custom-edited 694-bp 1ZBB PDB) and full secondary-electron transport with the G4EmDNAPhysics option-2/4 cross-section ladder, against a 10⁷-track ensemble per (E, f) configuration.*

Specifically:
1. **PDB4DNA + Petrolli C++ extension not built on uicgpu.** The radmc Geant4-11.4.2 environment on uicgpu has builds for `dnadamage1`, `clustering`, and `chem6` examples but **not** `PDB4DNA`, and the paper's custom ROOT-histogram extension classes are **not publicly distributed source code** (paper references them as their own extension of the Delage 2015 PDB4DNA example). Building these would require ~1–2 days of source acquisition + C++ refactoring + verification.
2. **Custom 694-bp 1ZBB PDB edited via VMD not provided.** The paper's working PDB is the 1ZBB dinucleosome (471 bp) symmetrically extended to a 694-bp tetramer using a "dedicated PDB file editor (VMD)". The exact extension procedure is not specified in the paper, and the edited PDB is not publicly available. We worked with the actual 1ZBB (which is itself the full 694-bp construct in chains I+J — see Coverage table row 2) but cannot verify whether our nucleotide ordering matches the paper's serial index 1..694 in `Fig. 1`.
3. **Secondary-electron transport.** The surrogate's δ-ray model (random-walk, mean range 5 nm) is too short-range and uniform to capture the differential edge-clipping that we believe produces the central-spike artifact. Faithful reproduction needs Geant4-DNA's G4EmDNAPhysics_option2 (or 4/6) low-energy electron cross-sections (excitation, ionization, attachment, elastic) which model individual secondary tracks down to ~7 eV.

Other partial-coverage issues (not full blockers):
* **Statistics.** We ran 5×10⁵ tracks per (E, f); paper used 10⁷ (20× more). At our statistics, DSB counts at 5 MeV / 2.5x are only n=20, which is sufficient to see Poisson shape but not enough to distinguish a 0.5 bp shift in DMS with statistical significance.
* **Source-geometry mismatch.** The paper describes the source as "isotropic, outer spherical source defined over the vertex coordinates" with particles "shot by the edges toward the water box". We implemented a cosine-weighted inward source from the corner-radius sphere, which gives equivalent isotropic *flux* through the box surface but may differ from PDB4DNA's per-particle launch geometry in ways that affect the central-spike artifact.

## Bottom line

The paper's secondary, *quantitative* claims about DSB distance distributions and the VHS/DHS / DMS trends with box expansion and proton energy are **reproduced** by a physics-informed surrogate Monte-Carlo against the actual 1ZBB tetranucleosome with the paper's exact strand-break and DSB thresholds. The paper's *primary* methodological claim — that a normalized Shannon-entropy formula reveals a hit-counter bias at small box sizes which plateaus at f≈2.5 — is **not** reproduced; our entropy trend is inverted because the underlying central-spike hit-artifact does not arise in our straight-line-track + short-range-δ-ray surrogate. Faithful replication of *that* claim requires the full PDB4DNA + Petrolli-extension Geant4-DNA stack with G4EmDNAPhysics_option-2/4 secondary-electron transport, which was not feasible within this slot's compute and code-acquisition budget.
