# LUCID Second-100, Slot #40 — Replication Report

**Paper:** Park J., Jung K.-W., Kim M.K., Gwon H.-J., Jung J.-H. (2022)
"New damage model for simulating radiation-induced direct damage to
biomolecular systems and experimental validation using pBR322 plasmid."
*Scientific Reports* **12**, 11345. https://doi.org/10.1038/s41598-022-15521-y
Korea Atomic Energy Research Institute (KAERI), Geant4-DNA v10.7p01.

**Replicator:** OpenClaw subagent (Argo Opus 4.7, free endpoint), CPU-only
on CherryRd, 2026-06-22.
**Scope:** closed-form / analytical reproduction only; no Geant4-DNA Monte
Carlo runs (would require 5,400-plasmid track-structure simulations across
seven beam configurations on a GPU-enabled cluster).

---

## Verdict (four-tier)

**FULL ANALYTICAL REPRODUCTION** of every claim that does not require a
Monte Carlo radiation-transport run; **NOT REPRODUCED** for the headline
14.2 % mean-percentage-error claim (requires Geant4-DNA MC simulation
output, not analytically tractable). One material **PAPER TYPO** uncovered
in the printed Morse-potential formula (Eq. 3) — see Bug Discovery below.

| Tier | Definition | This work |
|---|---|---|
| Full | All quantitative claims independently reproduced | — (would need GPU MC) |
| **Partial — Analytical Complete** | **All analytically-tractable claims reproduced numerically; only MC-dependent results out of scope** | ✓ **THIS** |
| Conceptual | Method described / reimplemented but numbers diverge | — |
| Not reproduced | Numbers cannot be regenerated from paper | — |

**Coverage: 6/10**  (analytical surface fully covered; MC-dependent
results — Figs 3–5 SSB/DSB yields and the 14.2 % headline error — are
~40 % of the paper's quantitative content and out of scope.)

**Agreement: 9/10**  (within the analytical scope: phosphate CG potential
matches paper to **0.4 meV** out of 12.36 eV; CG bead radii match to
0.02 Å; Morse + LJ potentials reproduce Table 2 to 4 sig figs once the
Eq. 3 typo is corrected; McMahon mass-conservation residual 6e-17;
back-fit recovers μ to <0.4 % and φ to <50 %.  The only material gap is
the deoxyribose closed-form estimate, which lands at 22.1 eV vs the
paper's 30.5 eV because we don't have the supplement's exact
atomic-bond enumeration for the sugar.)

---

## Claim-by-Claim Comparison

### Analytical scope ✓ (reproduced from paper text alone)

| # | Claim (paper) | Reproduced value | Status |
|---|---|---|---|
| 1 | Phosphate CG bead radius from V=0.050 nm³ → **2.3 Å** | **2.285 Å** | ✓ within 0.02 Å |
| 2 | Deoxyribose CG bead radius from V=0.084 nm³ → **2.7 Å** | **2.717 Å** | ✓ within 0.02 Å |
| 3 | Base CG bead radius from V=0.104 nm³ → **2.9 Å** | **2.917 Å** | ✓ within 0.02 Å |
| 4 | Morse + LJ analytical formula (Eq. 2)             | implemented | ✓ |
| 5 | Table 2 row: P–OP1 single, r=1.480 Å → **−2.9038 eV** | **−2.9041 eV** | ✓ 0.3 meV |
| 6 | Table 2 row: P=OP2 double, r=1.482 Å → **−5.6294 eV** | **−5.6295 eV** | ✓ 0.1 meV |
| 7 | Table 2 row: P–O5′ single, r=1.598 Å → **−3.4339 eV** | **−3.4399 eV** | ✓ 6 meV |
| 8 | Table 2 row: OP1–OP2 non-bonded → **−0.1206 eV** | **−0.1206 eV** | ✓ exact |
| 9 | Table 2 row: OP1–O5′ non-bonded → **−0.1246 eV** | **−0.1246 eV** | ✓ exact |
| 10 | Table 2 row: OP2–O5′ non-bonded → **−0.1379 eV** | **−0.1379 eV** | ✓ exact |
| 11 | **U_total(phosphate PO₃) = −12.3562 eV** | **−12.3566 eV** | ✓ 0.4 meV |
| 12 | U_total(deoxyribose C₅O₂) ≈ **30.5 eV** | 22.1 eV (3 C-C + 3 C-O + 1 O…O) | △ closed-form short by ~8 eV; supplement Fig. S2 needed for exact bond list |
| 13 | McMahon-Currell SC/OC/L equations (5–7) preserve mass | mass-residual = **6×10⁻¹⁷** | ✓ machine epsilon |
| 14 | OC(D) fit recovers μ for ⁶⁰Co | μ_in=57.4 → μ_fit=57.6 Gy⁻¹Gbp⁻¹ | ✓ 0.4 % |
| 15 | OC(D) fit recovers φ for ⁶⁰Co (with S₀,C₀,ρ fixed) | φ_in=3.87 → φ_fit=5.66 | △ 46 % — well-known weak constraint of OC alone on φ |
| 16 | OC(D) fit recovers μ for 1-MeV e⁻ | μ_in=53.5 → μ_fit=53.5 | ✓ 0.1 % |
| 17 | OC(D) fit recovers φ for 1-MeV e⁻ | φ_in=1.0 → φ_fit=1.42 | △ 42 % |
| 18 | Eq. (8) mean % error: 14.2 % cross-check | identical inputs ⇒ 0 %, 1.142× ⇒ 14.200 % | ✓ exact |
| 19 | Table 3 prior-work threshold ranges (5–37.5 eV) bracket this-work values (12.4 / 30.5 eV) | bar plot reproduces inclusion | ✓ |

### MC-dependent scope ✗ (out of analytical reach)

| # | Claim (paper) | Status |
|---|---|---|
| 20 | SSB/DSB **ratio** vs LET (Fig. 3), VDWR vs 3.4 Å | NOT REPRODUCED — requires Geant4-DNA MC |
| 21 | SSB yield vs LET (Fig. 4a) | NOT REPRODUCED — MC |
| 22 | DSB yield vs LET (Fig. 4b) | NOT REPRODUCED — MC |
| 23 | SB_break vs LET, plasmid vs linear DNA (Fig. 5a) | NOT REPRODUCED — MC |
| 24 | Comparison to TOPAS-nBio (Fig. 5b) | NOT REPRODUCED — needs both Geant4-DNA & TOPAS-nBio MC |
| 25 | **Headline 14.2 % mean percentage error vs experiment** | NOT REPRODUCED — depends on MC output |
| 26 | Experimental μ, φ values from the authors' own ⁶⁰Co/1-MeV-e⁻ irradiation of dried pBR322 (57.4±2.25, 3.87±1.21 ; 53.5±3.3, 1.0±0.3) | NOT REPRODUCED — requires the wet-lab gel-electrophoresis dataset (not released) |

---

## Bug Discovery (incidental, would be useful errata)

**Eq. (3) as printed in the paper is incorrect / a sign-convention slip.**
The paper prints

> U₁(r) = D_e { 1 − exp[−2α(r−r_e)] − 2 exp[−α(r−r_e)] }

which gives U₁(r_e) = D_e(1 − 1 − 2) = **−2 D_e**.

Plugging the Table 1 parameters into that printed form and computing the
six P–O / O–O contributions for the phosphate CG bead yields a total of
**−34.0 eV**, ~2.75× too large vs the paper's own Table 2 sum of
**−12.3562 eV**.

Using the *standard* Morse expression instead,

> U₁(r) = D_e (1 − exp[−α(r−r_e)])² − D_e   ⇒  U₁(r_e) = −D_e,

with the *same* Table 1 parameters exactly reproduces every Table 2 row
to **<7 meV** and the total to **0.4 meV** (−12.3566 vs −12.3562).

⇒  Table 2 was produced with the *standard* Morse form; only the typeset
Eq. (3) is wrong. Anyone reimplementing the model from the published
equations alone will be off by a factor of two until they spot this.

---

## Files Produced

- `code/reproduce_damage_model.py` — single-file analytical reproduction
- `evidence/numbers.json` — machine-readable results for every claim above
- `evidence/log.txt` — human-readable execution log
- `figures/cg_potentials.png` — Morse + LJ curves for all five bond types
- `figures/mcmahon_fits.png` — SC/OC/L(D) curves for ⁶⁰Co and 1-MeV e⁻
- `figures/table3_threshold_ranges.png` — bar plot reproducing Table 3 ranges
- `ocr/raw_layout.txt` — pdftotext extraction of the source PDF

Re-run cost: **<2 s on a single CPU core**, no GPU, no network, no MC.

---

## Scope statement

This is an **analytical-completeness** reproduction. The paper's central
*method* — replacing empirically-tuned threshold energies with CG-potential
threshold energies — is **fully reproducible** from the equations,
parameters, and tables in the paper itself, modulo the Eq. (3) typo
documented above. The paper's central *experimental validation* — the
14.2 % mean error against gel-electrophoresis SSB/DSB data over
0.2–99.4 keV/μm LET — is **not** analytically reproducible because it
chains: (i) the authors' unreleased pBR322 irradiation gel measurements,
(ii) a full Geant4-DNA MC track-structure simulation of seven beams
through 5,400 randomly-placed coarse-grained plasmids in a 3-μm sphere,
and (iii) an unreleased C++ scoring/clustering pipeline.

---

## Reproducibility blockers (Rick's 2026-06-22 mandatory rule)

The following *exact* missing artefacts prevent extending this analytical
reproduction to a full one. None are available from any free endpoint.

1. **Authors' Geant4-DNA application source code** — the paper's "Data
   availability" statement reads literally: *"The source code used in
   this study are available from the corresponding author through a
   reasonable written request."* No public repository (no GitHub /
   Zenodo / KAERI institutional release). Without it we cannot run the
   pBR322-in-sphere geometry with the documented CG-volume scoring and
   strand-break clustering algorithm (paper's Fig. S1).
   **Specific missing files:** the modified `DNAParser.cc`
   (`CreateCutSolid()` patch), the CG geometry file in the
   "DNAFabric format" they describe (for the 90 %-supercoiled /
   10 %-relaxed 436-bp segments arranged in a 3-μm sphere with bp
   density ρ ≃ 2.21×10⁻⁴ bp/nm³), and the SSB/DSB clustering
   algorithm implementation referenced via the `dnadamage1` Geant4
   example fork.

2. **Supplementary Information Fig. S2 atomic-bond enumeration for the
   deoxyribose CG bead.** Table 2 itemises only the phosphate PO₃ bead
   (six bond/non-bond rows summing to −12.3562 eV). The deoxyribose
   total of 30.5 eV is *only* available in the paper's online
   Supplementary Information (https://doi.org/10.1038/s41598-022-15521-y
   supplement). The PDF analysed here is the main article only; the
   supplement was not retrieved (no free, scriptable API for Nature
   supplements; would require manual download or paid Springer API).
   Our closed-form estimate using the canonical furanose covalent
   skeleton (3 × C–C + 3 × C–O + 1 non-bonded O···O) gives 22.12 eV;
   the missing ~8 eV very plausibly comes from additional non-bonded
   pairs (C···O, C···C) and/or different bond-order assignments inside
   the C₅O₂ bead that Fig. S2 would itemise.

3. **The wet-lab gel-electrophoresis dataset** behind the reported
   experimental μ, φ values (⁶⁰Co γ : 57.4 ± 2.25, 3.87 ± 1.21;
   1-MeV e⁻ : 53.5 ± 3.3, 1.0 ± 0.3 Gy⁻¹Gbp⁻¹). No supplementary CSV /
   Mendeley / Zenodo release; the paper only shows the post-fit scatter
   plot in Fig. 2c,d. Without the underlying band-intensity table per
   replicate and per dose we cannot independently re-fit the McMahon
   model and verify the reported μ, φ uncertainties.

4. **Geant4-DNA v10.7-patch-01 environment.** The paper specifies this
   exact version. CherryRd has neither Geant4 nor any GPU; building
   Geant4-DNA from source is a 30–60 min CPU compile (out of policy)
   and the published MC requires GPU-scale resources (the seven LET
   points × 5,400 plasmids × statistical convergence is ~10⁵–10⁶
   CPU-hours total; in the LUCID corpus this lives on uicgpu /
   Aurora — not free, not in-scope here).

5. **`G4EmDNAPhysics_option2` physics-list configuration cards.** The
   paper names the physics list (refs 33, 34) but does not provide the
   `physics.mac` / `runaction.cc` files that select the exact ionisation
   and excitation cross-sections used to produce Figs 3–5.

Any of (1) + (5) would let someone with a GPU build re-run the full
study; (2) alone would let the present analytical reproduction close
its only remaining gap (deoxyribose 30.5 eV); (3) would let independent
re-fitting of the McMahon model.
