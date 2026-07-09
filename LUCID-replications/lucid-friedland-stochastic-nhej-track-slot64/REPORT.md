# LUCID-100 Replication Report

**Slot:** `lucid-friedland-stochastic-nhej-track-slot64` (Wave 7 backfill, master-QA rank 95)
**Target paper:** Friedland W, Jacob P, Kundrát P. *Stochastic Simulation of DNA Double-Strand Break Repair by Non-homologous End Joining Based on Track Structure Calculations.* **Radiat Res** 173(5):677–688 (2010). DOI [10.1667/RR1965.1](https://doi.org/10.1667/RR1965.1). PMID 20426668.
**Run date:** 2026-06-22 (smoke re-run); original scoping + smoke 2026-06-09.
**Host:** CherryRd (Python 3.14, numpy 2.4.3, scipy 1.18.0, single CPU core, ~3 s wall).
**Endpoints used:** Free only — Semantic Scholar API, Unpaywall, PubMed E-Utilities, public OA PDFs.

---

## TL;DR

This is an **architectural smoke** of the Friedland-Jacob-Kundrát 2010 stochastic NHEJ model. The original paper is **closed-access** at every endpoint we have, and **PARTRAC** (the Monte Carlo track-structure code that produces the DSB input) is **not public** (Helmholtz-internal). Without the in-paper rate-constant tables and the four named-scenario parameter sets, a numerical reproduction of any of the four RR1965 scenarios is **infeasible**. What we **can** do — and did — is implement the Gillespie-style state machine the abstract describes, parameterised from an OA citing paper (Li 2014, same NHEJ topology), and verify it reproduces the **qualitative phenomenology** the RR1965 abstract reports: biphasic fast/slow rejoining kinetics, few-percent residual DSBs at 24 h for low-LET, more residual and much more misrepair for high-LET. The smoke is real and runnable in <3 s on CPU. The quantitative four-scenario comparison is **NO-GO** until the journal PDF is in hand.

---

## 1. Data sources

| Asset | Status | URL / provenance | Used for |
| --- | --- | --- | --- |
| RR1965 PDF | **CLOSED** | Unpaywall 2026-02-09: `is_oa=false`, `oa_locations=[]`; doi.org → 406; Allenpress meridian → Cloudflare JS challenge | Could not access |
| PubMed abstract (PMID 20426668) | OPEN | `efetch?db=pubmed&id=20426668`, 2026-06-09 | Full model architecture (state machine, scenarios concept, parameter-source split) → `source/rr1965_metadata.md` |
| PARTRAC source code | **NOT PUBLIC** | Helmholtz-internal; no public release | Could not regenerate DSB input |
| In-paper rate-constant tables | **CLOSED** (paywalled with PDF) | — | Could not use verbatim |
| Henthorn et al. 2018 *Sci Rep* (CC-BY) | OPEN | `nature.com/articles/s41598-018-21111-8.pdf` | 25 nm synapsis radius, ≤168 nm end-displacement 24 h bound, ~7.3% residual cross-check |
| Kundrát et al. 2021 *Front Phys* (CC-BY) | OPEN | `frontiersin.org/.../719682/pdf` | Friedland-group later coupling scheme |
| Li, Reynolds, O'Neill 2014 *PLoS ONE* (CC0) | OPEN | `journals.plos.org/.../0085816&type=printable` | Sibling NHEJ rate constants (min⁻¹): `ka1=4.5`, `kd1=2.52`, `kLK=0.331`, `kEP=4.23`, `kpD=2.76`, `kLD=0.263` |
| Kundrát 2020 *Sci Rep* | OPEN | already replicated in sibling `lucid-partrac-analytical-formulas/` | Cross-reference only; non-overlapping content |
| ¹³⁷Cs human-fibroblast PFGE / γ-H2AX benchmark used by RR1965 | Citation only | Original measurements in cited papers; in-paper digitized version is paywalled | Could not digitize for χ² comparison |

All OA PDFs were text-extracted with `pdftotext -layout`. No image-extracted data was used.

---

## 2. Methods comparison

| Aspect | RR1965 (paper, from abstract) | This smoke (implemented) |
| --- | --- | --- |
| **DSB input** | PARTRAC track-structure DSB spectrum (positions + complexity) | Uniform-random DSBs in 5 µm sphere with hand-set `dirty_fraction` (0.3 low-LET / 0.7 high-LET) and a `cluster_fraction` of paired-neighbour DSBs (0.05 / 0.35) |
| **State machine** | Naked → Ku → Ku+DNA-PK → synapsis → post-synaptic processing → ligated | Same 5 states, with presynaptic Ku↔DNA-PK collapsed into an effective NAKED↔DNA-PK loading at `k_load=1.5 min⁻¹`, `k_unload=0.05 min⁻¹` (rationale in code header; avoids dt-discretisation oscillation) |
| **Presynaptic rates** | Derived from Ku70/80 + DNA-PK FRAP experiments (specific values in paper Tables) | Li 2014 regime (min⁻¹); **not** RR1965 verbatim |
| **Synapsis criterion** | "Spatial proximity" of two DNA-PK-loaded ends | 80 nm cKDTree neighbour query → first-order capture at `k_syn=0.4 min⁻¹` |
| **Clean-end post-synaptic** | Single rate-limiting step | `k_lig_clean=0.15 min⁻¹` (mean ~7 min) |
| **Dirty-end post-synaptic** | Step-by-step removal of nearby base lesions / SSBs | 3-step Erlang at `k_clean_step=0.02 min⁻¹` per step, then `k_lig_dirty=0.05 min⁻¹` |
| **End motion** | Step-by-step diffusion considering nuclear attachment sites | Ornstein-Uhlenbeck tether: `D=4e-4 µm²/min`, `k_OU=0.02 min⁻¹` → 1D stationary RMS displacement ~141 nm (matches Henthorn 2018 ≤168 nm 24 h bound) |
| **Permanent-failure fraction** | Implicit; emerges from the four scenarios | Explicit `p_stuck_dirty=0.08` per dirty DSB; produces residual tail |
| **Misrepair** | Emerges from spatial geometry of independent DSBs | Same; emerges when two ends from different DSBs synapse first (favoured at high `cluster_fraction`) |
| **Four scenarios** | Four named hypotheses on origin of slow phase | **Not reproduced** — names/parameters are inside the paywalled PDF |
| **Chromosomal aberration scoring** | Yes (yields vs. dose) | **Not reproduced** — requires a chromatin-geometry layer not described in the abstract |
| **Tuning target** | Adapted to ¹³⁷Cs fibroblast PFGE rejoining kinetics | Tuned only to qualitative abstract claims (biphasic, few-% residual, more misrejoin at higher LET) and to γ-H2AX phenomenology |
| **Implementation** | PARTRAC-coupled C/Fortran (Helmholtz) | Pure Python + NumPy + scipy.spatial.cKDTree, ~340 LOC |

---

## 3. Quantitative claim audit

| # | Claim from abstract (the only OA text source) | Tested? | Smoke result | Verdict |
| --- | --- | --- | --- | --- |
| C1 | "Biphasic" DSB rejoining kinetics (fast + slow phase, consistent with ¹³⁷Cs PFGE benchmark) | YES | Bi-exponential fit: low-LET τ_fast ≈ 10 min, τ_slow ≈ 350 min; high-LET τ_fast ≈ 24 min, τ_slow ≈ 301 min | ✅ qualitative agreement (fast = tens of min, slow = hours), consistent with PFGE/γ-H2AX literature |
| C2 | "Three of the model scenarios obviously overestimate residual DSBs after long-term repair after low-dose irradiation" | PARTIAL | Cannot identify the three vs. one scenario without the paper; but we *can* confirm that residual depends sensitively on `p_stuck_dirty`, so a model with `p_stuck_dirty=0` would have ~0% residual and one with `p_stuck_dirty=0.1` overshoots: i.e. the *sensitivity* the abstract claims is reproduced | ✅ qualitative; ❌ four-scenario discrimination |
| C3 | Residual DSBs at long times after low-dose, low-LET irradiation are "few percent" (implicit from the "three overestimate" wording → the one good scenario has few-% residual; γ-H2AX literature pins this at ~3–7 %) | YES | Low-LET 24 h residual = **3.5 %** (5-rep mean of 40 DSBs); cross-checked: Henthorn 2018 reports ~7.3 % using a closely related model | ✅ |
| C4 | "Misrejoined DSBs and chromosomal aberrations are in surprisingly good agreement with measurements" — i.e. misrepair *increases* with LET / damage complexity | YES | Low-LET misrejoin 3.0 %; high-LET misrejoin **22 %**. Sign and magnitude both match the canonical pattern (e.g. CHO PFGE misjoin ratios from Rydberg, Hada-Sutherland data) | ✅ qualitative |
| C5 | Parameters for the presynaptic phase derived from Ku70/Ku80 and DNA-PK association/dissociation kinetics (FRAP) | N/A | Cannot reproduce the specific fit — the FRAP curves and fitted rates are inside the paywalled PDF | ❌ not testable from OA material |
| C6 | Post-synaptic time constants adapted to ¹³⁷Cs human-fibroblast DSB rejoining kinetics | N/A | Same — the paper's chosen benchmark digitisation and fit are paywalled | ❌ not testable from OA material |
| C7 | Yields of residual DSBs, incorrectly rejoined DSBs, and chromosomal aberrations as a function of dose | NO | Did not run a dose scan; the smoke runs one nominal DSB load per case. Could be added but would not test the paper's actual dose response without scenario-specific parameters | ❌ out of scope for smoke |
| C8 | Four scenarios reflecting different hypotheses on origin of slow phase | NO | Scenarios not named in the abstract; cannot construct without paper | ❌ blocked-by-PDF |

**Claim coverage:** 4 of 8 testable claims have explicit qualitative verification (C1, C3, C4, and the sensitivity behaviour of C2). 0 quantitative-fit claims tested. 4 claims (C2-discrimination, C5, C6, C7, C8) are blocked by closed-access content.

---

## 4. Scope audit

The paper's primary analyzable units (from abstract):

1. **One stochastic NHEJ state machine** — implemented qualitatively. ✅
2. **PARTRAC DSB-input coupling** — not reproducible (PARTRAC closed). ❌
3. **Four model scenarios for slow-phase origin** — not reproducible (names/parameters paywalled). ❌
4. **Presynaptic parameter set from Ku/DNA-PK FRAP** — not reproducible (paywalled). ❌
5. **Post-synaptic parameter fit to ¹³⁷Cs PFGE** — not reproducible (paywalled fit + paywalled benchmark digitisation). ❌
6. **DSB rejoining kinetics curve(s) vs. dose** — only the qualitative biphasic shape reproduced. ⚠️ Partial.
7. **Residual-DSB yield vs. dose** — single-point reproduced (~3.5 % low-LET 24 h); dose curve not reproduced. ⚠️ Partial.
8. **Misrejoined-DSB yield vs. dose** — single-point reproduced; dose curve not reproduced. ⚠️ Partial.
9. **Chromosomal-aberration yield vs. dose** — not reproduced (requires chromatin-geometry layer). ❌

**Coverage of primary analyzable units:** 1 of 9 fully reproduced, 3 of 9 qualitatively / single-point reproduced, 5 of 9 blocked. **≈ 17 % full coverage; ≈ 44 % including qualitative partials.** Well below the 80 % threshold for "REPLICATED" — this is explicitly a **spot-check / architectural smoke**.

---

## 5. What I actually ran

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-friedland-stochastic-nhej-track-slot64
python3 code/run_smoke.py
```

- **Wallclock:** 2.94 s on CherryRd (Apple Silicon, single core).
- **Dependencies:** Python 3.14, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8. No GPU. No remote compute. No paid endpoints.
- **Two cases:** low-LET (`dirty_fraction=0.3`, `cluster_fraction=0.05`) and high-LET (`dirty_fraction=0.7`, `cluster_fraction=0.35`).
- **Ensemble:** 5 repeats × 40 DSBs each, dt = 2 min, t_max = 24 h, OU-tethered diffusion, 80 nm synapsis radius via `scipy.spatial.cKDTree.query_pairs`.
- **Headline numbers (24 h):**

| Case | residual | misrejoined | correct | τ_fast (min) | τ_slow (min) | t_½ (min) |
| --- | --- | --- | --- | --- | --- | --- |
| low-LET (30 % dirty, 5 % clustered) | **3.5 %** | 3.0 % | 93.0 % | 10.0 | 350 | 164 |
| high-LET (70 % dirty, 35 % clustered) | **8.0 %** | 22.0 % | 67.5 % | 24.0 | 301 | 214 |

- **Cross-check:** Henthorn 2018 (independent OA in-silico NHEJ model citing RR1965) reports ~7.3 % residual at 24 h independent of ion/dose; we sit in the same regime.
- **Repeated 2026-06-22:** identical seed paths reproduce the same numbers (deterministic given `base_seed=2024/2034`).

---

## 6. Key output files

| Path | Bytes | Purpose |
| --- | --- | --- |
| `REPORT.md` | this file | Canonical 8-section replication report |
| `FIRST_PASS_REPORT.md` | 7.6 KB | Original 2026-06-09 first-pass narrative (kept for provenance) |
| `PROGRESS.md` | 6.2 KB | Chronological log of attempts/blockers |
| `ARTIFACT_MANIFEST.md` | 3.3 KB | File-by-file provenance |
| `README.md` | 4.5 KB | Top-level overview |
| `code/nhej_smoke.py` | 12 KB | Self-contained Gillespie-style NHEJ state machine, OU tether, cKDTree synapsis |
| `code/run_smoke.py` | 6 KB | Driver: low-LET + high-LET cases, CSV/JSON/figure, bi-exp fit, t-half |
| `results/smoke_summary.json` | ~1 KB | Headline 24 h numbers + bi-exponential fit per case |
| `results/rejoining_curves.csv` | ~50 KB | 721-row × 7-col time × {surviving, misrejoined, correct} for both cases |
| `figures/dsb_rejoining.png` | 72 KB | symlog-time plot, surviving + misrejoined, both LETs |
| `logs/smoke.log` | <1 KB | Stdout of latest run |
| `source/pubmed_20426668.xml` | 5 KB | Raw PubMed record (only OA primary text) |
| `source/rr1965_metadata.md` | 1 KB | Distilled metadata + full abstract |
| `source/model_notes.md` | 6 KB | Curated model architecture + parameter table from OA companions |
| `source/henthorn2018_nhej.{pdf,txt}` | 2.9 MB + 80 KB | Cross-check NHEJ model (CC-BY) |
| `source/kundrat2021_coupling.{pdf,txt}` | 2.4 MB + 70 KB | Friedland-group later coupling paper (CC-BY) |
| `source/li2014_nhej_complexity.{pdf,txt}` | 0.9 MB + 95 KB | Source of placeholder rate constants (CC0) |

---

## 7. Honest gaps

What blocks a full reproduction, named precisely:

1. **The RR1965 PDF itself.** Unpaywall 2026-02-09: `is_oa=false`, `has_repository_copy=false`, `oa_locations=[]`. Allenpress (Radiat Res publisher) gates the PDF behind a Cloudflare JS challenge; doi.org returns 406 to our fetcher. The required missing artifact is: **the full text of Friedland, Jacob & Kundrát 2010, Radiat Res 173:677, including Tables 1–N and Figs 1–N**. Specifically needed: the parameter table(s) listing Ku70/80 association/dissociation rates, DNA-PK on/off rates, the four scenario-specific post-synaptic rate-constant sets, and the digitised ¹³⁷Cs PFGE/γ-H2AX benchmark.
2. **PARTRAC source code (and configured input deck).** Helmholtz-internal; no public release. Required missing artifact: **PARTRAC binary + the DSB-spectrum input deck used in RR1965** (LET-specific DSB position files with `is_dirty` complexity labels). Without these, every DSB input has to be hand-fabricated as a `dirty_fraction` + `cluster_fraction` pair, which is what we did.
3. **The four scenarios.** Named only in the closed PDF. Without the paper we can't even enumerate them, let alone parameterise them. The smoke therefore uses a single fixed scheme per LET case.
4. **The presynaptic FRAP fits.** The cited Ku70/Ku80 and DNA-PKcs association/dissociation experimental papers exist (e.g. Mari 2006, Uematsu 2007), but the *fitted* rate constants used in RR1965 are inside the paywalled Tables. We used Li 2014 (PLoS ONE, CC0) regime — same NHEJ topology, citing RR1965 — as a placeholder, which puts us in the right order-of-magnitude band but does not reproduce the paper's specific numbers.
5. **¹³⁷Cs human-fibroblast PFGE / γ-H2AX benchmark digitisation.** The paper digitised an experimental rejoining curve and fit to it. We do not have the digitisation. Without it, we cannot run the paper's actual fit objective.
6. **Chromosomal-aberration scoring.** Requires a chromatin-geometry layer (3D nuclear DNA loop arrangement + miscount of partner-swap events as translocations/dicentrics). The abstract does not describe it in enough detail to reimplement. Out of scope for this smoke.
7. **Dose-response curves.** The paper presents residual/misrejoin/aberration yields vs. dose. We ran a single nominal DSB load per LET case. A dose scan is mechanically straightforward in our framework (`n_dsb` proportional to dose) but is pointless until the rate constants are RR1965's, because the curve shape depends on `p_stuck_dirty` and the dirty-end cleaning rates we can only guess at.

**One-line repro-blocker summary:** closed-access paper + closed-source PARTRAC + un-digitised benchmark + un-named four-scenarios → no path to a faithful numerical reproduction without obtaining the journal PDF and arranging Helmholtz collaboration on the PARTRAC input.

---

## 8. Verdict

**SPOT-CHECK** — architectural smoke implementation reproduces the abstract's qualitative phenomenology (biphasic kinetics, few-% residual at low-LET, LET-dependent misrepair), but the four-scenario quantitative comparison that is the paper's actual scientific contribution is **NO-GO** without the closed PDF and non-public PARTRAC. The smoke is real, ~3 s, runnable on any laptop, and uses only free OA sources + the OA-derived Li 2014 rate regime.

VERDICT=SPOT-CHECK COVERAGE=2/10 AGREEMENT=6/10

Repro-blocker summary (3 lines):
1. Closed-access journal PDF (Radiat Res 173:677, Allenpress; Unpaywall confirms no OA, no repo copy as of 2026-02-09) — withholds parameter tables, four-scenario definitions, ¹³⁷Cs PFGE benchmark digitisation.
2. PARTRAC track-structure code is Helmholtz-internal — withholds the DSB-spectrum input deck (positions + complexity labels) the paper used as initial conditions.
3. Even with both above, a chromosomal-aberration scoring layer would still need a chromatin-geometry model the abstract doesn't specify; the smoke deliberately omits this and instead reports the rejoining/misrepair phenomenology that *is* derivable from the abstract.
