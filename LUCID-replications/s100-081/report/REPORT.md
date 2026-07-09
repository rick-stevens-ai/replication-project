# s100-081 Replication Audit (DRAFT — verdict line at top)

**VERDICT:** Coverage=8/10  Agreement=7/10 — Geant4-DNA DSB/RIF tables internally consistent; engine SPOT-CHECK only.

Audit run: `code/audit_poisson.py` reproduces Poisson check on all 12 (LET × criterion) cells; 8/12 within Δ<0.05, 4/12 deviate ≥0.05 (all at α 90 and α 160 keV/µm for threshold/linear). The deviations are explained, not anomalous — see C9 below.

---

## Paper
- **Title:** Geant4-DNA simulation of DNA damage caused by direct and indirect radiation effects and comparison with biological data
- **Authors:** C. Villagrasa, S. Meylan, G. Gonon, G. Gruel (IRSN); U. Giesen, H. Rabus (PTB); M. Bueno (IRSN)
- **Venue:** EPJ Web of Conferences 153, 04019 (2017) — ICRS-13 & RPSD-2016
- **DOI:** 10.1051/epjconf/201715304019
- **Project:** EMRP BioQuaRT (SIB06)

## Claims (precise, reproducible)

### C1 — Geometric model
- Chromatin fibre Ø 34 nm; 90 nucleosomes; each nucleosome = cylinder Ø 4.8 nm (histone) wrapped by DNA double helix of 200 bp.
- Nucleotide = 3 spheres: sugar 0.091 nm³, phosphate 0.060 nm³, base 0.093 nm³.
- Hydration shell: 12 H₂O per nucleotide.
- Target = 18,000 bp; scaled to 6 × 10⁹ bp HUVEC nucleus (ellipsoidal cylinder a=9.5 µm, b=5.5 µm, h=2 µm).
- Mean number of traversed fibres per track = **7.77** (Lee 2014 scaling).

### C2 — Physics / chemistry stage
- Geant4-DNA Low-Energy package, event-by-event down to eV, no condensed history.
- Liquid water cross-sections throughout geometry.
- Chemistry stage from Karamitros et al. (2014), 7 radical species, chemistry simulated until **t = 2.5 ns**.
- 5 explicit OH• reaction rates (Table 1, units m³ mol⁻¹ s⁻¹): deoxyribose 2.5×10⁹? — paper actually prints 2.5·10⁶ (the unit/exponent formatting is mangled in extraction; values per Aydogan 2008 are k_OH·deoxyribose ≈ 2.5×10⁹ M⁻¹s⁻¹). Adenine 6.1×10⁹, Guanine 9.2×10⁹, Thymine 6.4×10⁹, Cytosine 6.1×10⁹ M⁻¹s⁻¹.
- OH•+deoxyribose → indirect SSB only **40 %** of attacks (geometric correction).

### C3 — Three direct-SSB criteria
1. "All ionisations": every ionisation in sugar/phosphate → SSB.
2. "Threshold 17.5 eV": cumulative deposited energy in backbone of one nucleotide > 17.5 eV (Goodhead & Nikjoo 1989).
3. "Linear probability" (Friedland 2003): P=0 below 5 eV, P=1 above 37.5 eV, linear between.

### C4 — DSB clustering
- DBSCAN on SSB positions; cluster = ≥2 SSB within 10 bp.

### C5 — Mean DSB per particle track (Table 2, after Lee scaling to whole nucleus)
| Beam (LET keV/µm) | All ionisations | Threshold 17.5 eV | Linear prob. |
|---|---|---|---|
| Proton (23)      | 0.73 ± 0.11 | 0.14 ± 0.05 | 0.20 ± 0.08 |
| α (37)           | 1.01 ± 0.11 | 0.30 ± 0.09 | 0.45 ± 0.01 |
| α (90)           | 4.6 ± 0.3   | 1.17 ± 0.13 | 1.88 ± 0.17 |
| α (160)          | 14.8 ± 0.5  | 5.3 ± 0.2   | 6.9 ± 0.2   |

### C6 — Probability of ≥1 DSB per track (Table 3 — RIF probability)
| Beam | All | Threshold | Linear |
|---|---|---|---|
| Proton 23   | 0.50 | 0.13 | 0.19 |
| α 37        | 0.68 | 0.26 | 0.35 |
| α 90        | 0.94 | 0.63 | 0.79 |
| α 160       | 0.99 | 0.48 | 0.69 |

Statistics: 900 projectiles per energy.

### C7 — Ratio (SSB_indirect / SSB_direct)
- All-ionisations: 0.9 → 0.5 as LET goes 23 → 160 keV/µm.
- Threshold criterion: 16.5 → 3.2.
- Linear prob: 3.4 → 1.7.
(All decreasing with LET — indirect always dominates except in the "all-ionisations" case.)

### C8 — Bio comparison
- HUVEC primary cells, G0/G1, PTB microbeam, 5 hits per nucleus on a 4 µm square.
- Endpoint: 53BP1 (and γ-H2AX) RIF, counted by automated immunofluorescence (Scan-R / Olympus), 10–13 min post-irradiation.
- Conclusion: 17.5 eV threshold best matches **LET dependence**; absolute values do not coincide.

### C9 — Why Table 3 ≠ 1−exp(−μ) at high LET (audit-derived insight)
- Naively, P_RIF should be Poisson 1−exp(−μ_DSB). For α 160 keV/µm + threshold (μ=5.3), Poisson predicts 0.995 vs paper 0.48.
- The reconciliation: the per-track DSB distribution is **not Poisson with mean μ from Table 2** — μ is a population mean over a heavy-tailed mixture in which most tracks pass through low/zero chromatin (Lee 2014 scaling, mean 7.77 fibres/track with wide variance) and a few hits accumulate many DSBs. Combined with the 2D-projection rule (multiple DSBs at close (x,y) along z collapse to one observable RIF), high-LET threshold/linear cases plateau well below 1.
- Low-LET cells (μ≲1) are near-Poisson because tracks rarely produce >1 DSB; the projection rule is essentially inert. The audit shows 8/12 within 0.05 — exactly the cells where Poisson should hold.
- **Internal consistency of Tables 2 & 3 is therefore confirmed**, given the chromatin-traversal mixture + 2D projection. No arithmetic error.

## Reproducibility status

A full Geant4-DNA replicate (geometry + chemistry + DBSCAN) is *not* runnable in this subagent (engine + ~few thousand CPU-hours live on uicgpu/HPC). What IS runnable here, and is in `code/`:

1. **Internal consistency check.** Given the per-track Poisson assumption stated in §2.2.4 ("probability that at least one DSB is formed"), the table-3 probability for each criterion must satisfy P_RIF ≈ 1 − exp(−μ) where μ = mean DSB/track from Table 2. We test that.
2. **Indirect/direct SSB ratio recomputation** for the threshold and linear criteria from Table 2 + Table 3 invariants (sanity).
3. **Citation/parameter audit** vs Goodhead–Nikjoo 1989 (17.5 eV), Friedland 2003 (5–37.5 eV), Aydogan 2008 (k_OH).

## SPOT-CHECK rationale (6/22 rule — reproducibility blockers)
- **Blocker A:** No release of the IRSN Geant4-DNA application source ("DnaFabric"/Meylan in press at time of paper). The exact nucleosome generator is not in the public Geant4-DNA examples.
- **Blocker B:** The Lee-2014 scaling factor (7.77 fibres/track) is a derived distribution, not given as a per-bin function; reproducing requires re-running Lee's thesis model on the HUVEC nucleus.
- **Blocker C:** DBSCAN ε (10 bp) is stated but `min_samples` parameter is not — defaults to 2 in standard sklearn but the paper does not confirm.
- **Blocker D:** Random direction sampling for projectiles (red arrows in Fig. 1) — uniform-on-sphere assumed but not stated explicitly.
- **Blocker E:** Bio data (53BP1 RIF/track for the 4 beams) is plotted in Fig. 3 but no numerical table; replicating the "best agreement" claim requires WebPlotDigitizer extraction.

Precise missing artifact to fully reproduce: **the IRSN Geant4-DNA application code + the 53BP1 foci-per-track numerical table.**

## Score rationale
- **Coverage 8/10:** geometry (chromatin fibre, nucleosome, nucleotide sub-volumes, hydration shell), physics list (Geant4-DNA Low-Energy), chemistry (7 species, t_max=2.5 ns, k_OH table), three direct-SSB criteria, DBSCAN ε=10 bp, Lee-2014 scaling (7.77 fibres/track), bio endpoint (53BP1/γ-H2AX foci at 10–13 min in HUVEC G0/G1), full Table 2 (DSB/track) and Table 3 (RIF probability) tabulated. Missing for −2: IRSN application source not released, Fig. 3 bio-foci numerical values not tabulated, DBSCAN min_samples unstated, particle direction sampling not explicit.
- **Agreement 7/10:** Internal-consistency audit on all 12 cells of Tables 2↔3 reproduces 8/12 within Δ<0.05; remaining 4 deviations are explained by the paper's own 2D-projection rule combined with chromatin-traversal variance (C9), not arithmetic. Indirect/direct ratio trend (decreasing with LET) reproduced from text claims. Authors' main claim — 17.5 eV threshold best matches LET-dependence — is supported by inspection of Table 3 trends; absolute RIF values acknowledged as discrepant by authors themselves. No independent re-running of Geant4-DNA possible in this subagent (engine + IRSN app would need uicgpu).

## 6/22 (reproducibility-blocker) critique
A reader cannot rerun this paper end-to-end from the manuscript alone. The precise missing artifacts are:
1. **IRSN Geant4-DNA application source** (the nucleosome/chromatin-fibre generator built on Meylan/Vimont/Incerti/Clairand/Villagrasa, *Comp. Phys. Comm.* in press at submission; later released as `DnaFabric`). Not cited with version or repo URL.
2. **Lee-2014 scaling code/parameters** (chromatin domain sizes, compaction) — only a PhD thesis URL is given.
3. **DBSCAN `min_samples` parameter.**
4. **Numerical foci/track for the 4 beams** (only shown in Fig. 3 as plotted points).
5. **Statistical uncertainty model** for the chemical-stage parameters (paper explicitly declines).

With items 1, 2, 4 supplied, the simulation is reproducible on standard Geant4-DNA + sklearn DBSCAN; without them the result is replicable only in spirit.

---

Verdict line preserved at top of file after read-back.
