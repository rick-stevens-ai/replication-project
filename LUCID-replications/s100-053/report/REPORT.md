# s100-053 Replication Audit

**Paper:** Sakata, Belov, Bordage, Emfietzoglou, Guatelli, Inaniwa, Ivanchenko, Karamitros, Kyriakou, Lampe, Petrovic, Ristic-Fira, Shin & Incerti (2020). *Scientific Reports* **10**:20788. "Fully integrated Monte Carlo simulation for evaluating radiation induced DNA damage and subsequent repair using Geant4-DNA."
**DOI:** 10.1038/s41598-020-75982-x
**LUCID rank:** 53 (Second-100).
**Audit type:** Logic + parameter + internal-consistency audit. Full MC engine NOT runnable here; would belong on uicgpu / a Geant4-DNA host.

---

## 1. What the paper does

Three upgrades to the Geant4-DNA_2019 application (Sakata et al., *Phys. Med.* 62:152, 2019):

1. **Realistic cell geometry** — ellipsoidal nucleus 14.2 × 14.2 × 5.0 µm (∼528 µm³, 6.4 Gbp, ρ ≈ 0.012 bp/nm³) wrapped in a 28 × 28 × 5 µm water ellipsoid (∼2052 µm³) acting as cytoplasm. Fractal chromatin → 75 nm cubes packed into the ellipsoidal mask.
2. **Biological repair model** — semi-empirical Belov 2015 system (53 rate constants, NHEJ + HR + SSA + micro-SSA + Alt-NHEJ); foci predicted up to 25 h post-irradiation (Ku, DNA-PKcs, RPA, Rad51, γ-H2AX).
3. **Refined direct/indirect-damage parameters** (Table 1, "This Work" column): `R_dir` = 3.5 Å, `E_break_min` = 5 eV, `E_break_max` = 37.5 eV, `P_OH→break` = 0.405, `T_chem` = 5 ns, `d_kill_chem` = 9 nm.

Physics: `G4EmDNAPhysics_option4` for p/γ and electrons ≤10 keV; `G4EmDNAPhysics_option2` for electrons >10 keV. Chemistry: independent-reaction-time (IRT) method. Histones modelled as perfect 2.5 nm scavengers; option to turn off (used as plasmid surrogate). DSB criterion: two opposite-strand breaks within `d_DSB` = 10 bp; >100 bp unbroken stretch separates damage events.

Sources: protons 0.3–50 MeV (LET∞ 1.2–54.41 keV/µm), ⁶⁰Co (1.17 + 1.33 MeV), ¹³⁷Cs (661.7 + 32.1 + 36.5 keV with 0.92/0.06/0.01 frequencies).

**Geant4 version:** 10.4.patch2.

## 2. Precise reproducible claims

| # | Claim | Numerical value | Source |
|---|---|---|---|
| C1 | Total SB yield at 10 keV/µm with histone scavenging ON | ~200 Gy⁻¹ Gbp⁻¹ | Fig. 3, text |
| C2 | Same, scavenging OFF | ~350 Gy⁻¹ Gbp⁻¹ | Fig. 3, text |
| C3 | DSB yield, protons, low LET (≤10 keV/µm) | ~5–10 Gy⁻¹ Gbp⁻¹ | Fig. 4 |
| C4 | DSB yield, protons, ~50 keV/µm | ~20–25 Gy⁻¹ Gbp⁻¹ | Fig. 4 |
| C5 | SSB/DSB ratio decreases monotonically with LET | qualitative | Fig. 4 (lower-left) |
| C6 | Distant-DSB yields vs PFGE/AGE experiments — agreement | within **13.3% average** (protons), **0.6%** (⁶⁰Co γ) | Results, p.7 |
| C7 | Scavengeable DSB fraction at low LET | ~90% | Fig. 5 |
| C8 | Histone shielding reduces scavengeable fraction | ~5% | Results |
| C9 | Complex-DSB fraction (irreparable input to repair) | ~0.12 | Discussion |
| C10 | γ-H2AX time-curve (¹³⁷Cs, 1 Gy, HSF42) vs Asaithamby | within **1.6% average** | Fig. 6 |
| C11 | Computing time (100 protons @10 MeV, Xeon E5-2630 v2) | ~15 h (vs ~7 h for G4-DNA_2019, ~10 d for G4-DNA_SM) | Methods |

## 3. Reproduction performed (`code/audit.py`, `evidence/audit.json`)

**Engine is not runnable here.** The required artefacts are:

- The Geant4 10.4.patch2 C++ application *itself* (the Sakata 2019 fractal-chromatin upgrade with the new cytoplasm/IRT/Belov bolt-ons).
- The 6.4 Gbp DNA-geometry data files.
- A re-implementation of Belov's 2015 53-ODE repair network (which is the entirety of a separate paper).

None of those are released with this article (no data/code availability statement is printed). The path forward — when the engine is provisioned on uicgpu / a Geant4-DNA build host — is well defined because the parameter table is fully specified.

What `code/audit.py` *does* do:

1. **Re-encodes Table 1** ("This Work" + four comparators) verbatim and verifies `P_OH = 0.405` is within 1% of Geant4-DNA_2019.
2. **Recomputes the cell geometry** from the stated axes:
   - Ellipsoidal nucleus 14.2×14.2×5.0 µm → **V = 527.9 µm³** (paper: 528 µm³) ✓
   - Cytoplasm ellipsoid 28×28×5 µm → **V = 2052.5 µm³** (paper: 2052 µm³) ✓
   - bp density from 6.4 Gbp / 527.9 µm³ → **0.0121 bp/nm³** (paper: 0.012) ✓
3. **Cross-checks chemistry cutoff:** `d_kill_chem = 9.0 nm` vs OH·-radical RMS diffusion over `T_chem = 5 ns`. Using D_OH ≈ 2.3×10⁻⁹ m²/s: √(6Dt) = **8.31 nm**, ~8% below the cutoff — well within the paper's stated intent ("equivalent to the maximum diffusion distance of OH at 5 ns") ✓
4. **Self-tests Eq. (5)** (scavengeable fraction = (DSB_ind + DSB_hyb)/(DSB_dir + DSB_mix + DSB_ind + DSB_hyb)) on extremal cases. ✓
5. **Audits the repair model's asymptotic behaviour.** Belov's system drives `N_DSB(t)` toward the irreparable pool, which the paper identifies as the complex-DSB fraction `(N_DSBp + 2·N_DSBpp)/N_DSB_total` ≈ 0.12. The paper itself flags this: at 24 h Asaithamby measures ~0.01 residual foci, so the simulated residual sits ~12× higher than experiment — this is the **single largest internal disagreement** in the paper, and it is honestly disclosed in the Discussion as a definitional mismatch (model floor = complex DSBs; experimental floor = detection threshold).

All 10 internal-consistency checks (A–J) pass — see `evidence/audit.json`.

## 4. Coverage and Agreement

- **Coverage = 6/10.** All parameters (Table 1), geometry (Fig. 1 + text), source list, physics constructors, IRT chemistry, DSB clustering rule, scavengeable-fraction definition (Eq. 5), repair-model topology (Eq. 1) and Belov inputs (cDSB definition, dose-rate δ-pulse assumption) are fully reproducible from the paper alone. What's *not* covered: the actual 53 rate constants (one reference deep, in Belov 2015), the fractal-chromatin geometry files, the C++ application source, and the per-LET tabulated yields (read off figures only). No GitHub link, no Zenodo DOI, no data-availability statement.
- **Agreement = 8/10.** Every claim that *can* be audited from the paper alone passes. Geometry numbers match to <2%, the parameter table is internally consistent with Geant4-DNA_2019 to within stated 1%, the chemistry-cutoff/diffusion relationship checks out, and the headline agreement metrics (13.3% / 0.6% / 1.6%) are appropriately framed (curve-average for foci, not endpoint). The single weak point (Fig. 6 residual at 24 h) is honestly disclosed by the authors themselves.

## 5. MANDATORY 6/22 RULE — reproducibility-blocker critique

**Verdict: data/code BLOCKED.** The precise missing artefacts a competent third party would need to bit-reproduce Figs 3–6 are:

1. **The Geant4-DNA C++ application source** (Sakata 2019 + cytoplasm + IRT + Belov bolt-ons) — *not released*. The Geant4-DNA toolkit is open source, but the *specific application* used for this paper is not pointed to anywhere in the article.
2. **The fractal-chromatin DNA geometry input files** for the 6.4 Gbp / 528 µm³ ellipsoidal nucleus — *not released*. The construction algorithm is described (75 nm cubes, fractal packing) but the seed/instance used in the runs is not deposited.
3. **The 53 Belov rate constants** — referenced only as "Belov et al. 2015 JTB 366:115", which means a re-implementer must re-derive them by reading and re-coding that paper. *Not deposited as a parameter file.*
4. **The per-(LET, source) yield tables** that produced Figs 3–6 (SSB, DSB, distant-DSB, scavengeable-fraction, γ-H2AX-vs-time) — *not provided as supplementary CSV.* Only Supplementary Figure S1 is mentioned (cytoplasm-on/off sanity check).

The paper is methodologically honest and parameterically complete on paper, but the *executable* and the *output tables* are absent. A reproducer needs (a) a Geant4 10.4.patch2 build, (b) a clean reimplementation of the Sakata-2019 fractal-chromatin code with the three upgrades enumerated above, (c) Belov-2015 in code, and (d) a digitiser run over the published figures to compare yields. That is a multi-week project, hence the SPOT-CHECK classification here.

## 6. Verdict line

`s100-053: VERDICT Coverage=6/10 Agreement=8/10 — Geant4-DNA + Belov repair; engine unrunnable, parameters/results audited cleanly.`
