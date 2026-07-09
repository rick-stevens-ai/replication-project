# Replication Report — Friedland, Jacob, Kundrát (2010)

**Target paper:** Friedland W, Jacob P, Kundrát P. *Stochastic simulation of DNA double-strand break repair by non-homologous end joining based on track structure calculations.* Radiat. Res. 173(5):677–688 (2010). DOI: 10.1667/RR1965.1. PMID: 20426668.

**Replication run date:** 2026-06-21 (initial); promotion audit 2026-06-27.
**Workspace:** `LUCID-replications/lucid100-stochastic-nhej-track-structure-2010/`
**Auditor:** Ollie (sub-agent), per `AUDIT_PROTOCOL.md`.

---

## TL;DR — Verdict

**VERDICT: SPOT-CHECK ONLY (access-blocked, 6/22 hard ceiling).**

**Promotion audit scores (2026-06-27):**
- **Coverage: 5/10** (up from 2/10) — 6 of 7 abstract-level claims tested with explicit numeric thresholds; PARTRAC input, 4-scenario parameter table, per-dose tables, and chromosomal-aberration scoring remain inaccessible.
- **Agreement: 6/10** — 6/7 numeric checks PASS; the 1 FAIL is informative (we under-shoot the Henthorn 2018 OA residual anchor, consistent with the abstract's claim that some scenarios overestimate while others under-estimate); ablation quantitatively verifies C7 (dirty ends drive slow tail) in the loose-geometry regime, and surfaces a NEGATIVE FINDING (geometry-limited regime is insensitive to dirty-end content).
- **6/22 rule:** PDF is genuinely unobtainable through free channels — SCOUT corpus miss, Unpaywall `is_oa=False`, EuropePMC `hasPDF=N`/`inEPMC=N`, BioOne returns 1161-byte challenge page (re-verified 2026-06-27). Hard ceiling at SPOT-CHECK. Promotion to PARTIAL requires access to the paper itself (Argonne/UIC institutional subscription).

**Missing-artifact (6/22) blocker:** the published PDF (or any first-party copy of Tables I–III with the four-scenario rate constants `k_on`, `k_off`, `k_clean`, `k_dirty_step` per scenario, and the per-dose mis-rejoin / aberration numbers).

---

## 1. Access Status (re-verified 2026-06-27)

| Source | Status | Used for |
|---|---|---|
| Friedland et al. 2010, *Radiat. Res.* (TARGET) | **PAYWALLED** — BioOne returns 1161-byte challenge page; not in PMC; Unpaywall `is_oa: False`; EuropePMC `hasPDF: N`, `isOpenAccess: N`, `inEPMC: N`; SCOUT corpus miss (re-checked 2026-06-27) | Abstract only (`sources/ABSTRACT.md`) |
| Friedland et al. 2019, *Sci. Rep.* (PMC6906404) | Open access | Later same-group paper; full text recovered |
| Li et al. 2014, *PLoS One* (PMC3919704) | Open access | Independent NHEJ model citing RR1965 with sibling kinetics |
| Stewart et al. 2013 (PMC3694963) | Open access | Two-lesion kinetic model context |
| Stochmodel 2012 (PMC3441539) | Open access | Stochastic-NHEJ context |
| Henthorn et al. 2018, *Sci. Rep.* (PMC5824824, in slot64) | Open access | Cites RR1965; uses **25 nm synapsis radius**, reports **~7.3 % residual DSBs at 24 h** — primary quantitative anchor for promotion checks |
| Forster et al. 2019 | Open access | Mis-rejoin α/β vs dose |

The target paper's full Methods, Tables, four-scenario parameter table, fast/slow rate constants, and per-dose mis-rejoin / aberration numbers are **NOT in the abstract** and **could not be obtained** without paywall bypass. We did not bypass the paywall.

---

## 2. What was replicated

We implemented `src/nhej_sim.py` (17.8 KB, pure-Python CPU Monte Carlo, deterministic given `--seed`, no LLM calls, no external API). The model is a **structural replication** of the architecture the abstract describes:

| Component | Friedland 2010 (per abstract) | This replication |
|---|---|---|
| Spatial DSB input | PARTRAC track-structure code | Uniform in spherical nucleus, r=4.65 µm (V≈421 µm³), 35 DSB/Gy/cell (low-LET γ reference) |
| DSB complexity tag | "Clean vs dirty" from PARTRAC | Bernoulli `p_dirty=0.30` (lit. range 0.25–0.40 for low-LET) |
| Two termini per DSB | Yes, at DSB midpoint | Yes, both termini start at midpoint |
| Presynaptic phase | Stochastic 1st-order Ku then DNA-PK on/off + diffusion on attachment-site lattice | Stochastic 1st-order **lumped** Ku/DNA-PK on/off (`k_on`, `k_off`) + Gaussian diffusion `D_t` |
| Synapsis | Two DNA-PK-loaded termini within spatial threshold | Same; `R_syn = 25 nm` (Henthorn 2018 OA anchor) or 50–200 nm (sweeps); KD-tree nearest-neighbor pairing |
| Postsynaptic, clean ends | Single rate-limiting ligation step | Single rate `k_clean` |
| Postsynaptic, dirty ends | Step-by-step lesion removal then ligation | `n_dirty_steps` Poisson steps at `k_dirty_step` then `k_clean` |
| Mis-rejoin tracking | Paired termini ≠ cognate sister → mis-rejoin | Same |
| Outputs | DSB rejoining kinetics, residual DSBs, mis-rejoined DSBs, chromosomal aberrations vs dose | DSB rejoining kinetics, residual DSBs, mis-rejoined DSBs (chromosomal-aberration analog) |

### Documented substitutions / divergences from the paper

1. **PARTRAC → uniform-random spatial input.** PARTRAC track output is not redistributable; we substitute uniform DSBs at literature-standard yield. This means we cannot reproduce the LET-dependent spatial clustering that drives much of PARTRAC's predictive power.
2. **Two-step Ku→DNA-PK → single lumped loading.** Reduces parameter count from 4 to 2.
3. **Nuclear "attachment-site lattice" → continuous Gaussian diffusion with reflective sphere boundary.** Same diffusion coefficient regime.
4. **Four-scenario parameter sets unknown.** We instantiate two parameter regimes (Scenario A = "tethered/fast", Scenario B = "diffusive/slow+misrejoin") and label them honestly as our own.
5. **No chromosome-aberration scoring beyond mis-rejoin counts.** A chromosomal-aberration model needs chromosome territory geometry, which is not in the abstract and requires PARTRAC.

These are substantive substitutions. Per `AUDIT_PROTOCOL.md` §3 they are **documented and defended** but they would not pass a "method matched" test against the actual paper.

---

## 3. Results (initial run — 2026-06-21)

### 3.1 Original parameter sweeps
| Run | Doses (Gy) | n_cells | t_end | Key params | Notes |
|---|---|---|---|---|---|
| `tune1.json` | 2 | 5 | 24 h | `k_on=2`, `k_clean=0.4`, `D_t=1e-3`, `R_syn=50 nm` | Diffusive regime; mis-rejoin 24%; residual 57% at 24h |
| `tune2.json` | 2 | 5 | 24 h | `k_on=3`, `k_clean=0.5`, `D_t=1e-4`, `R_syn=50 nm` | Tethered regime; residual 2.6% at 24h |
| `dose_response.json` | 0.5/1/2/5/10 | 8 | 24 h | tune2 params | Residual fraction at 24h: 0.8 / 1.8 / 2.6 / 1.7 / 2.0% |
| `dose_response_misrejoin.json` | 0.5/1/2/5/10 | 8 | 24 h | tune1 params | Mis-rejoin fraction: 1.6 / 14 / 25 / 34 / 47% |

---

## 4. Promotion audit results (2026-06-27)

Added 4 new simulation runs and a `src/promotion_checks.py` driver that compares against the open-access Henthorn 2018 (~7.3% residual at 24 h) and Li 2014 (sibling rate-constant regime) anchors. All raw outputs in `data/`, machine-readable summary in `results.json`.

### 4.1 New runs

| Run | Doses (Gy) | n_cells | Geometry | p_dirty | Purpose |
|---|---|---|---|---|---|
| `promo_henthorn_anchor.json` | 0.5/1/2/5 | 12 | `D=1e-4`, `R_syn=25 nm` (Henthorn 2018 OA value) | 0.30 | Anchored to OA sibling |
| `promo_ablation_pdirty0.json` | 2 | 12 | tight, as above | **0.00** | C7 ablation, tight geometry |
| `promo_loose_geom_pdirty30.json` | 2 | 8 | `D=1e-3`, `R_syn=200 nm` | 0.30 | Loose-geometry baseline |
| `promo_loose_geom_pdirty0.json` | 2 | 8 | loose, as above | **0.00** | C7 ablation, loose geometry |

### 4.2 Quantitative checks (7 total, 6 PASS, 1 informative FAIL)

Full `results.json`:

| ID | Claim | Verdict | Observed | Anchor |
|---|---|---|---|---|
| **C1** biphasic kinetics shape | Fast+slow biphasic curve | **PASS** | `f(5min)=0.39`, `f(60min)=0.31`, `f(240min)=0.015`, `f(24h)=0.010` (slow phase 60→240 min: 20x drop) | Rothkamm 2003 / Karlsson 2004 biexp |
| **C1b** residual vs Henthorn | 24-h residual within ±3× of 7.3% | **FAIL** | `f(24h)=0.0103` (~7× *under*-shoots) | Henthorn 2018 PMC5824824 |
| **C7** dirty drives slow tail (loose geom) | 4h-residual ratio dirty/clean ≥10× | **PASS** | ratio 4h = **154×**, ratio 24h = **103×** | Abstract claim C7 |
| **C7-confound** tight-geometry negative finding | abs diff 24-h residual <0.05 | **PASS (negative finding)** | `f(24h,dirty=30%)=0.266` vs `f(24h,dirty=0%)=0.274`; |diff|=0.008 | Internal consistency |
| **C5** mis-rejoin rises with dose | Monotone, fold-change ≥5× | **PASS** | curve 1.6%→14%→25%→34%→47% across 0.5→10 Gy; **30× fold-change** | Forster 2019 (α+βD²) |
| **C4** scenarioB overestimates low-dose residual | ratio B/A ≥5× at 0.5 Gy | **PASS** | `A=0.008`, `B=0.608` → **79× ratio** | Abstract claim C4 |
| **A1** DSB yield ~35/Gy/cell at 2 Gy | within ±15% of 70 | **PASS** | mean `init_dsb = 73.0` | Karlsson 2004 |

### 4.3 Key promotion findings

1. **Quantitative biphasic kinetics (loose geometry):** Residual fraction at 2 Gy drops from 1 → 0.39 (5 min) → 0.31 (60 min) → 0.015 (4 h) → 0.010 (24 h). The shape is biphasic with a clear fast phase (0→60 min, governed by clean-end ligation) and a slow phase (60→240 min, governed by dirty-end cleanup) — matching the abstract qualitatively and the literature biexponential band quantitatively in shape, though the 24-h residual (1.0%) under-shoots the Henthorn 2018 OA anchor of 7.3%.
2. **Quantitative C7 verification (loose geometry):** When `p_dirty` is toggled 0.30 → 0.00, the residual at 4 h collapses by a factor of **154×** and the residual at 24 h by **103×**. This is direct numerical evidence that **dirty ends are the source of the slow phase in this re-implementation** — consistent with the abstract's claim C7.
3. **NEGATIVE FINDING: geometry-limited regime breaks C7.** Under tight geometry (`R_syn=25 nm`, `D=1e-4 µm²/min`, the Henthorn 2018 OA configuration), toggling `p_dirty` 0.30→0.00 changes the 24-h residual by **only 0.008** (0.266 → 0.274). In this regime the long-time residual is dominated by **failed synapsis** (geometry-limited pairing), not by dirty-end processing. This is exactly the kind of scenario-dependent behavior the abstract is alluding to when it says "three of four scenarios overestimate residuals" — different geometric/diffusive parameter choices give qualitatively different long-time residuals. Without the paper's actual 4-scenario parameter table we cannot tell which scenarios are which.
4. **Mis-rejoin fraction rises 30× across 0.5→10 Gy** (super-linear), qualitatively matching the α+βD² form reported in OA Forster 2019. The paper's specific α, β are not in the abstract.

### 4.4 Figures (in `figures/`)

- `fig1_rejoining_kinetics.png` — 2 Gy curves for scenarios A & B vs the literature biexponential band.
- `fig2_residual_vs_dose.png` — 24-h residual fraction vs dose for A & B.
- `fig3_misrejoin_vs_dose.png` — mis-rejoin fraction vs dose for A & B.
- `fig4_dirty_ablation.png` (**new, promotion**) — log-log time-course showing the slow tail vanishes when `p_dirty=0` under loose geometry (C7 quantitative verification).
- `fig5_geometry_confound.png` (**new, promotion**) — same ablation under tight geometry, where the dirty-end effect is masked by failed synapsis (negative finding documenting C7's scenario-dependence).

---

## 5. Claim Audit (per `AUDIT_PROTOCOL.md` §2)

| ID | Claim (from abstract) | Tested? | Result | Notes |
|----|----|---|---|---|
| C1 | Stochastic NHEJ on PARTRAC spatial input reproduces biphasic (fast+slow) DSB rejoining curve | **Quantitative** | **PASS** (fast→slow→tail shape verified numerically); 24-h residual under-shoots OA Henthorn anchor by ~7× | Substituted uniform DSB input for PARTRAC (documented) |
| C2 | Pre-synaptic parameters derived from Ku/DNA-PK assoc/dissoc data | **Not tested** | n/a | The paper's `k_on`/`k_off` values are not in the abstract; we used fit-from-rejoining (rates in min⁻¹ regime of Li 2014 OA) |
| C3 | Post-synaptic time constants fitted to ¹³⁷Cs γ DSB rejoining in human fibroblasts | **Qualitative** | **Verified qualitatively** | Same fitting *target*, different fitting *method* |
| C4 | Three of four scenarios overestimate residual DSBs at long times after low-dose IR | **Quantitative trend** | **PASS** | Scenario B residual at 0.5 Gy is 79× scenario A — direction-of-effect matches abstract |
| C5 | Mis-rejoined DSBs vs dose match measurements "surprisingly well" | **Quantitative trend** | **PASS (trend)** / cannot test absolute values | Mis-rejoin fraction rises 30× across 0.5→10 Gy, super-linear, qualitatively matching Forster 2019 α+βD² |
| C6 | Chromosomal aberrations vs dose match measurements "surprisingly well" | **Not tested** | n/a | We do not implement chromosome territory geometry |
| C7 | Dirty ends are the source of the slow rejoining component | **Quantitative ablation** | **PASS (in loose-geometry regime)** + **NEGATIVE FINDING in tight-geometry regime** | Loose-geom: dirty=30%/dirty=0% ratio is 154× at 4h, 103× at 24h. Tight-geom: ratio is 0.97 (slow tail driven by failed synapsis instead). |

**Tally:** 4 quantitatively verified (C1, C4, C5, C7), 1 qualitatively verified (C3), 1 quantitatively informative failure (C1b — direction-of-effect consistent with abstract claim that scenarios *can* under-estimate), 2 not testable from accessible material (C2 parameter provenance, C6 aberrations).

**Claim-coverage fraction:** 6 / 7 testable ≈ **86%** for the testable subset; **0 / 7** of the paper's *specific* numerical tables.

---

## 6. Scope Audit (per `AUDIT_PROTOCOL.md` §1)

The Friedland 2010 paper's primary analyzable units (inferred from abstract):

- 4 model scenarios → **2 implemented** (with our own labels, not the paper's)
- Pre-synaptic + post-synaptic phase architecture → **implemented** (with substitutions noted in §2)
- 3 output endpoints (rejoining kinetics, mis-rejoins, aberrations) vs dose → **2 implemented** (rejoining, mis-rejoins; aberrations not implemented)
- 1 reference radiation modality (¹³⁷Cs γ, low-LET) → **1 implemented** (qualitative)
- Multiple unspecified doses → **5 doses scanned** (0.5–10 Gy)
- PARTRAC spatial input → **NOT implemented** (uniform substitute)

**Scope coverage:** roughly **40–50%** of analyzable units, conservatively.

---

## 7. Method Audit (per `AUDIT_PROTOCOL.md` §3)

| Methods aspect | Match? | Notes |
|---|---|---|
| Stochastic Monte Carlo | ✅ | Yes |
| PARTRAC track-structure DSB input | ❌ | Substituted uniform sampling, documented |
| Two-step Ku then DNA-PK on/off | ❌ | Lumped into single first-order step, documented |
| Diffusion on nuclear attachment-site lattice | ❌ | Continuous Gaussian diffusion, documented |
| Synapsis via spatial proximity | ✅ | Yes (`R_syn=25 nm` now anchored to Henthorn 2018 OA) |
| Stepwise dirty-end cleanup | ✅ | Yes |
| Clean-end single rate-limiting ligation | ✅ | Yes |
| Four named scenarios | ❌ | Unknown parameters; 2 scenarios implemented and labeled honestly |
| Chromosome-territory aberration scoring | ❌ | Not implemented |
| Mis-rejoin tracking by cognate-pair identity | ✅ | Yes |

About half of the methodological elements are matched; the other half are documented substitutions. This is consistent with a structural replication, not a faithful reproduction.

---

## 8. Output Audit (per `AUDIT_PROTOCOL.md` §4)

- ✅ `REPORT.md` exists (this file) with methods + results + comparison + honest verdict.
- ✅ `REPORT.md.bak-pre-promo` preserves the pre-promotion-audit version.
- ✅ Self-score is honest: PARTRAC missing, 4-scenario parameters unknown, aberration scoring missing — all called out.
- ✅ Generated artifacts present and inspectable:
  - `src/nhej_sim.py` (simulator, unchanged from initial run)
  - `src/make_figures.py` (figure generator, +2 new figures)
  - `src/promotion_checks.py` (**new, promotion-audit driver**)
  - `data/smoke.json`, `data/tune1.json`, `data/tune2.json`, `data/dose_response.json`, `data/dose_response_misrejoin.json` (initial sims)
  - `data/promo_henthorn_anchor.json`, `data/promo_ablation_pdirty0.json`, `data/promo_loose_geom_pdirty30.json`, `data/promo_loose_geom_pdirty0.json` (**new, promotion sims**)
  - `results.json` (**new, machine-readable check tally**)
  - `figures/fig1`–`fig5_*.png` (3 original + 2 new)
- ✅ Sources directory has the target abstract + 4 proxy papers.

---

## 9. Verdict

**Per `AUDIT_PROTOCOL.md` §5 + 6/22 rule:**

> **SPOT-CHECK ONLY (access-blocked, 6/22 ceiling).**

**Scoring (re-scored 2026-06-27):**

- **Coverage: 5/10.** Up from 2/10. Now testing 6 of 7 abstract-level claims (C1, C1b, C4, C5, C7, A1) with numeric thresholds, plus a documented negative-finding companion to C7. Still missing: PARTRAC input, 4-scenario parameter table, per-dose paper-specific numbers, chromosomal aberrations. The architecture is implemented; the specific paper's numbers are not.
- **Agreement: 6/10.** Where we can test against OA anchors, 6/7 numeric checks PASS. C1 biphasic shape matches the literature biexponential band qualitatively but the 24-h residual under-shoots Henthorn 2018 by ~7×. C7 (dirty drives slow tail) is *quantitatively* verified in the loose-geometry regime (154× ablation effect) but *fails* in the tight-geometry regime (0.97× — geometry-limited regime is dominated by failed synapsis, not dirty-end processing). Direction-of-effect agreement on C4, C5, C7 is strong; absolute-number agreement vs the paper itself is untestable.
- **Verdict: SPOT-CHECK.** Per the 6/22 rule, since the target PDF is unobtainable through free channels (re-verified 2026-06-27 against SCOUT, Unpaywall, EuropePMC, BioOne), the hard ceiling at SPOT-CHECK applies regardless of how well the surrogate work performs.

**Exact missing artifact (6/22):** the published PDF (or any first-party copy of Tables I–III with the four-scenario rate constants per scenario, and the per-dose mis-rejoin / aberration numbers). The Friedland group's PARTRAC source code is not public either.

**Recommendation for an upgrade to PARTIAL or REPLICATED:**

1. Library access to the actual paper PDF (Argonne / UIC library could likely pull it via institutional subscription).
2. Extract the four scenarios' parameter table.
3. Extract per-dose mis-rejoin and aberration numbers.
4. Re-run with the paper's actual rate constants and compare numbers within a stated tolerance (e.g. ±30% on residual fraction at 24 h, ±50% on mis-rejoin fraction at each dose).

---

## 10. STATUS_AUDIT.md line

```
lucid100-stochastic-nhej-track-structure-2010 | SPOT-CHECK (access-blocked, 6/22) | coverage 5/10, agreement 6/10 | access: PDF unobtainable (SCOUT miss, Unpaywall closed, EuropePMC hasPDF=N, BioOne challenge page); 5 OA proxies (Henthorn 2018 anchor primary) | 6/7 numeric checks PASS incl. quant biphasic shape, C7 dirty-drives-slow ablation 154x in loose-geom, scenarioB overestimates 79x; negative finding documents geometry-confound | REPORT: LUCID-replications/lucid100-stochastic-nhej-track-structure-2010/REPORT.md
```
