# RE-TIER (2026-06-25): VERDICT = NO-GO (hard ceiling, was SPOT-CHECK)

**Reclassified SPOT-CHECK -> NO-GO** per Rick's rule.

**Precise blocker (6/22 rule):** Elsevier paywall + the UNIVERSE mechanistic engine was never released across 4+ Liew/Mairani papers; structural code block. Missing artifact: the UNIVERSE oxygen-depletion/repair source code + parameter set.

---

# LUCID-100 Replication Report

**Slot:** `lucid100-flash-oxygen-repair-mechanistic-model` (LUCID-100 #27)
**Paper:** Liew H, Mein S, Dokic I, Haberer T, Debus J, Abdollahi A, Mairani A.
"Deciphering Time-Dependent DNA Damage Complexity, Repair, and Oxygen Tension:
A Mechanistic Model for FLASH-Dose-Rate Radiation Therapy."
*Int. J. Radiation Oncology Biol. Phys.* **110**(2):574-586 (2021).
DOI: [10.1016/j.ijrobp.2020.12.048](https://doi.org/10.1016/j.ijrobp.2020.12.048).
**Group:** Liew/Mairani, DKFZ Heidelberg (UNIVERSE model lineage).
**Auditor:** Ollie subagent, 2026-06-22.
**Audit-of-prior-work:** the 2026-06-09 first-pass deliverable in this slot
(`FIRST_PASS_REPORT.md`, `code/flash_oxygen_smoke.py`, 20-condition smoke).

---

## TL;DR

This audit confirms that the existing first-pass artifact is an honest
**mechanism-level, parameter-free smoke**, not a numerical reproduction of the
Liew 2021 IJROBP figures. The replication is **data-blocked at L3** by an
Elsevier paywall (paper + supplement), by the never-released UNIVERSE engine
source, and by the absence of any consolidated open dataset for the in-vivo
endpoints the paper fits. The qualitative direction of the FLASH effect at low
[O2] is reproduced; the paper's central quantitative claim that the FLASH
sparing effect peaks at intermediate (physoxic) [O2] is **not** reproduced
with literature-default `g_ROD` and `τ_reox`. An added dose-rate sweep
(this audit, `code/dose_rate_sweep.py`) further shows the smoke gives a
non-monotone SF-vs-dose-rate curve at 0.5% O2 with a maximum sparing of
~1.55× near 10-32 Gy/s, then *reverses* at the extreme FLASH end
(SF declines from 0.177 at 32 Gy/s back to 0.094 at 1000 Gy/s). The paper's
own numeric FLASH curves cannot be tested without the closed parameters and
closed code.

Net assessment: **SPOT-CHECK**. The mechanism is reproducible from open
predecessors (Liew 2019, Liew 2020) and the qualitative FLASH-at-low-O2
direction is reproduced; nothing in this folder is a substitute for the
paper's numerical predictions, and any user wanting parity with Liew 2021
Figs. 1-5 / Tables 1-2 needs the paywalled artifacts.

---

## 1. Data sources

| Resource | Status | Local copy |
|---|---|---|
| Liew 2021 IJROBP full text | **PAYWALLED (Elsevier 403)** — `is_oa=false`, `has_repository_copy=false` per Unpaywall | none |
| Liew 2021 supplement (parameter tables) | **PAYWALLED** | none |
| Author code (UNIVERSE engine) | **NEVER RELEASED** by the Liew/Mairani group (confirmed across 2019, 2020, 2021, 2022 papers) | none |
| Liew 2021 abstract | OPEN via Crossref / Semantic Scholar / OSTI BIBLIO 23198562 | `artifacts/osti_page.html`, `artifacts/crossref_liew2021.json`, `artifacts/semanticscholar_liew2021.json` |
| Liew 2019 IJMS predecessor (static UNIVERSE eqs.) | **OPEN (MDPI)** | `artifacts/PMC6929106.xml` (Europe PMC full text) |
| Liew 2020 IJMS predecessor (DMSO + indirect action) | **OPEN (MDPI)** | `artifacts/PMC7278970.xml` |
| Liew 2022 IJMS sibling (repair-kinetic UNIVERSE) | **OPEN** + already replicated locally in sibling slot `lucid-universe-repair-doserate-rbe/` | (reference only, not re-imported) |
| FLASH ROD literature parameters (`g_ROD`, `τ_reox`) | OPEN (Pratx 2019, Petersson 2020, Labarbe 2020) | used as priors in the smoke (`G_ROD = 0.42 mmHg/Gy`, `τ_reox = 5 s`) |
| In-vivo FLASH endpoint data (mouse tail necrosis, brain memory, lung, intestine) | aggregated from 52 cited primary papers; **no consolidated open dataset** | none |
| OSTI / DKFZ inrepo / ResearchGate preprint search | no preprint found; DKFZ page is a JS shell | `artifacts/dkfz_record.html`, `artifacts/osti_page.html` |

The data block is **structural**: every UNIVERSE paper from this lab since
2019 has shipped without code and (in the Elsevier outlets) without an open
supplement. Author contact and paid endpoints are excluded by task policy.

---

## 2. Methods comparison

| Element | Paper (per abstract + predecessors) | Replication / smoke | Match? |
|---|---|---|---|
| Static UNIVERSE giant-loop DSB model | Eq. 1-7 of Liew 2019 (α_DSB Poisson-deposited into N_giant_loop = 3000 domains of 2 Mbp; 1 break = iDSB, ≥ 2 = cDSB; `S = (1-K_iDSB)^N_iDSB · (1-K_cDSB)^N_cDSB`) | Implemented in `code/flash_oxygen_smoke.py::sample_iDSB_cDSB` and `survival_dynamic` with identical parametrization (α=30 DSB/Gy, N=3000) | ✅ structural match |
| Hypoxia handling | HRF([O2]) = (m·K + [O2])/(K + [O2]) with m = 2.94, K = 0.129 % O2 (Liew 2019 eq. 6) | Implemented identically in `HRF()`; used to modulate α_DSB → α_eff per time-step | ✅ structural match |
| Time-dependent DNA-damage repair | First-order exponential on iDSB and cDSB pools with distinct half-lives **(values closed)** | First-order exponential with DU145 representative values T_iDSB = 4 min, T_cDSB = 100 min (from open Liew 2022 IJMS Table 1) | ⚠️ structure matches; **numerical half-lives per endpoint are paper-specific and closed** |
| Radiolytic O2 depletion (ROD) | Linear in dose with coefficient `g_ROD` **(value closed)** | `d[O2]/dt = -g_ROD · dD/dt + ([O2]_amb - [O2])/τ_reox` integrated on 400-point grid; `g_ROD = 0.42 mmHg/Gy` from Pratx 2019 central estimate | ⚠️ structure matches; **g_ROD is closed** |
| Reoxygenation | First-order relaxation with `τ_reox` **(value closed)** | Same ODE; `τ_reox = 5 s` from Petersson 2020 central estimate | ⚠️ structure matches; **τ_reox is closed** |
| Endpoint-specific lethality | Distinct (K_iDSB, K_cDSB, fast/slow half-lives) per endpoint (in-vitro clonogenic, mouse tail necrosis, brain memory, lung fibrosis, intestinal crypt) | Single DU145-like (K_iDSB = 5.9e-3, K_cDSB = 0.17); **no endpoint fitting** | ❌ paper has 5+ endpoints, smoke has 1 |
| Validation data | digitized in-vitro and in-vivo dose-responses from Montay-Gruel 2017/18/19, Vozenin 2019, Favaudon 2014, Beyreuther 2019 etc. | **none re-digitized** | ❌ not attempted |
| Statistical / fit machinery | unspecified in abstract; presumably χ² or maximum-likelihood per endpoint | none — smoke is parameter-free | n/a |

**Audit verdict on methods:** the mechanism scaffolding is faithful to the
open UNIVERSE lineage, but the smoke deliberately does not implement the
paper's parameter-fitting or endpoint-fitting layers, because the inputs
(paywalled tables and digitized endpoint data) are unavailable.

---

## 3. Quantitative claim audit

Because the paper itself is paywalled, the testable numeric claims accessible
to this audit are only those derivable from the open abstract (general
directional claims) and from the open predecessor / sibling papers (specific
parameter values for the static engine). All paper-specific numeric headline
results (e.g. fitted `g_ROD` per endpoint, specific FLASH sparing factor at
specific [O2]) are **not testable** without the closed PDF/supplement.

| # | Claim (source) | Direction the paper asserts | Smoke result | Status |
|---|---|---|---|---|
| C1 | Static UNIVERSE α_DSB = 30 DSB/Gy/cell at 21% O2 (Liew 2019 eq. 2 + ref. Stewart 2011) | exact equality | smoke uses α=30 DSB/Gy (literal); mean DSB at 10 Gy, 21% O2 = 297/cell ≈ 30/Gy | ✅ verified (by construction) |
| C2 | HRF([O2]) parametrization with m = 2.94, K = 0.129% O2 (Liew 2019 eq. 6) | exact equality | identical implementation; HRF(0.1%) = 2.94·0.129/(0.129+0.1) + 0.1/(0.129+0.1) ≈ 2.09 in both | ✅ verified (by construction) |
| C3 | Liew 2022 IJMS (open sibling) DU145 repair half-lives ~ 4 min iDSB / 100 min cDSB | order-of-magnitude | smoke uses 4/100 min from IJMS Table 1; reproduces decay envelope | ✅ verified (input) |
| C4 | FLASH sparing direction at low [O2]: SF(FLASH) > SF(CONV) (paper abstract claim) | qualitative direction | At 20 Gy / 0.5% O2: SF_CONV=0.0056, SF_FLASH=0.0275 (smoke); at 10 Gy / 0.5% O2: 0.118 vs 0.168 — both consistent | ✅ verified qualitatively (same sign) |
| C5 | FLASH sparing peaks at *intermediate* (physoxic) [O2] window, ~ 4-7 % (per Liew 2021 results & FLASH-effect consensus) | window with internal maximum | smoke shows OPPOSITE: at ≥ 2% O2 in the main 20-cond sweep SF_CONV ≥ SF_FLASH; dose-rate sweep confirms negligible/inverted FLASH effect at 4% and 7.5% O2 | ❌ contradicted by smoke; rescuing this requires the paper's larger g_ROD and/or endpoint-tuned parameters |
| C6 | FLASH sparing exists across a clinically relevant dose-rate threshold (~ 40 Gy/s) | monotonically increasing SF above ~40 Gy/s | dose-rate sweep at 0.5% O2 shows **non-monotone** SF(R): max at R ≈ 10-32 Gy/s (SF ≈ 0.17), declining to 0.094 at 1000 Gy/s | ❌ contradicted; suggests our ROD ODE with literature `g_ROD/τ_reox` over-depletes O2 at very high dose rate so that DSB induction recovers via post-irradiation reoxygenation before pre-repair completes |
| C7 | Reoxygenation timescale of order seconds (paper text + Petersson 2020, Cao 2021) | τ_reox ~ 1-10 s | smoke uses τ_reox = 5 s | ✅ verified (input prior) |
| C8 | ROD coefficient g_ROD of order 0.3-0.7 mmHg/Gy (review lit.) | order-of-magnitude | smoke uses 0.42 mmHg/Gy | ✅ verified (input prior) |
| C9 | Paper headline numbers from Tables 1-2 (per-endpoint fitted lethality + repair parameters) | exact numeric | **not testable — paywalled** | ⛔ not tested |
| C10 | Per-endpoint in-vivo dose response (mouse tail necrosis, brain memory, lung, intestine) | quantitative fits | **not testable — paywalled paper + no consolidated open data** | ⛔ not tested |
| C11 | Validation against in-vitro clonogenic FLASH data (Beyreuther 2019, Vozenin 2019, Adrian 2019, etc.) | dose-response curve agreement | **not tested — primary sources not digitized in this slot** | ⛔ not tested |

**Tally:** Verified or verified-by-construction: 6/11 (C1-C4, C7, C8).
Contradicted: 2/11 (C5, C6) — these contradictions are interpretable as
"smoke is parameter-free; the paper's fitted parameters likely fix this."
Not testable due to paywall/data block: 3/11 (C9-C11). Counting only
*testable* claims (8), agreement is 6/8 = 75 % directional, 0/3 quantitative.

---

## 4. Scope audit

**Primary analyzable units of the paper** (inferred from abstract +
typical UNIVERSE paper structure + sibling papers):

| Unit | Approx. count | This slot covers? |
|---|---|---|
| Core mechanistic model (giant-loop + HRF + ROD + repair + reoxygenation) | 1 | ✅ implemented |
| Dose-rate sweep (CONV vs FLASH at fixed [O2]) | 1+ figures | ✅ added in this audit (`code/dose_rate_sweep.py`) |
| [O2] sweep at fixed dose rate | 1+ figures | ✅ implemented (first-pass smoke) |
| Endpoint-specific lethality fits (in-vitro clonogenic) | ~1 fit | ❌ not done |
| Endpoint-specific lethality fits (in-vivo): mouse tail, brain, lung, intestine | ~4 fits | ❌ not done |
| Tables 1-2 of numeric parameters | 2 tables | ❌ not testable (paywalled) |
| Figures 1-5 (dose-rate × O2 × endpoint surfaces) | 5 figures | ❌ not reproducible bit-exactly (paywalled inputs) |
| Validation comparison against literature FLASH datasets | unknown N (≥ 4 datasets cited) | ❌ not done |

**Coverage estimate:** of ~12-14 primary analyzable units, this slot
genuinely covers 3 (model implementation, [O2] sweep, dose-rate sweep) and
verifies inputs/structure for 3 more. Roughly **3-4 of ~12** = **~25-33%
scope coverage**. The remaining ~67-75% is gated by the paywall.

Per protocol § 1, this is below the 80% threshold and therefore explicitly a
"spot check / partial validation" — flagged as such.

---

## 5. What I actually ran

All on CherryRd (Apple Silicon, single-thread CPython 3.13, numpy 2.4.3,
matplotlib 3.10.8). No HPC, no paid endpoints, no external POSTs.

```bash
# already executed by the first-pass agent on 2026-06-09 (kept verbatim):
python3 code/flash_oxygen_smoke.py
# wall: 64.5 s; outputs: results/smoke_sweep.csv (20 rows),
#                       figures/smoke_flash_vs_conv_oxygen.png,
#                       logs/smoke_run.log

# added by this audit on 2026-06-22:
python3 code/dose_rate_sweep.py
# wall: 120.4 s; outputs: results/dose_rate_sweep.csv (27 rows),
#                        figures/dose_rate_sweep.png,
#                        logs/dose_rate_sweep.log
```

Smoke params (`logs/smoke_run.log` and source defaults): α_DSB = 30 DSB/Gy,
N_DOMAINS = 3000, HRF m = 2.94, K = 0.129 %, K_iDSB = 5.9e-3, K_cDSB = 0.17,
T_iDSB_half = 4 min, T_cDSB_half = 100 min, g_ROD = 0.42 mmHg/Gy,
τ_reox = 5 s; 4000 stochastic iterations/condition (smoke) / 1500
iterations/condition (sweep).

The dose-rate sweep specifically tested:
* 9 dose rates spanning 0.1 → 1000 Gy/s (log-spaced) × 3 initial [O2]
  (0.5 %, 4 %, 7.5 %) at fixed total dose D = 10 Gy = 27 conditions.
* Headline finding at 0.5 % O2: SF(R) is **non-monotone**, peaking at
  R ≈ 31.6 Gy/s with SF ≈ 0.177 (vs. 0.114 at R = 0.1 Gy/s and 0.094 at
  R = 1000 Gy/s). Sparing maximum = SF_max / SF_min ≈ 1.55×.
* At 4 % and 7.5 % O2 the smoke gives essentially **no FLASH sparing**;
  SF is flat-to-declining with dose rate.

This is consistent with the first-pass authors' note that
"with literature-default parameters the FLASH window is not where the
paper places it"; the audit extension nails that down with an explicit
SF-vs-dose-rate curve.

---

## 6. Key output files

```
lucid100-flash-oxygen-repair-mechanistic-model/
├── REPORT.md                          ← THIS audit report
├── README.md                          first-pass narrative (2026-06-09)
├── FIRST_PASS_REPORT.md               first-pass verdict (2026-06-09)
├── ARTIFACT_MANIFEST.md               paper / predecessor inventory
├── PROGRESS.md                        chronology
├── code/
│   ├── flash_oxygen_smoke.py          dynamic UNIVERSE smoke (290 LOC)
│   └── dose_rate_sweep.py             ← NEW (audit extension, 140 LOC)
├── results/
│   ├── smoke_sweep.csv                20 cond: D × [O2] × {CONV, FLASH}
│   └── dose_rate_sweep.csv            ← NEW: 27 cond, 9 dose rates × 3 [O2]
├── figures/
│   ├── smoke_flash_vs_conv_oxygen.png SF vs [O2]_0 at D=10,20 Gy
│   └── dose_rate_sweep.png            ← NEW: SF vs log10(dose rate)
├── logs/
│   ├── smoke_run.log
│   └── dose_rate_sweep.log            ← NEW
└── artifacts/
    ├── PMC6929106.xml                 Liew 2019 (open, equations source)
    ├── PMC7278970.xml                 Liew 2020 (open, equations source)
    ├── crossref_liew2021.json         paper metadata + 52-ref bibliography
    ├── semanticscholar_liew2021.json  paper metadata
    ├── osti_page.html                 abstract source
    └── dkfz_record.html               DKFZ SPA shell (no useful content)
```

---

## 7. Honest gaps

What blocks a full numeric replication of Liew 2021 IJROBP, named precisely:

1. **Paper PDF (Elsevier, Red Journal).** Specific missing artifact:
   `Liew_et_al_2021_IJROBP_110_574-586.pdf` (or the open-access deposit
   equivalent). Without it, every paragraph of the Results, every legend
   on Figs. 1-5, and every entry in Tables 1-2 is inaccessible.
2. **Supplementary material (Elsevier appendix).** Specific missing artifact:
   the Elsevier supplemental ZIP / appendix that accompanies DOI
   `10.1016/j.ijrobp.2020.12.048`. This is where the fitted endpoint
   parameter tables live (per the typical UNIVERSE paper format) and is the
   single most replication-critical artifact.
3. **UNIVERSE source code.** Specific missing artifact: any tagged release
   of the UNIVERSE engine from the Liew/Mairani group. They have never
   published one; data-availability statements of their open papers
   (e.g. Liew 2022 IJMS) say "Not applicable", and the 2021 paper makes no
   code-availability statement at all (typical for older IJROBP).
4. **Consolidated open dataset for the in-vivo endpoints used in
   validation.** Specific missing artifact: digitized survival /
   fibrosis / cognition-score curves from Montay-Gruel 2017/2018/2019,
   Vozenin 2019, Favaudon 2014, Beyreuther 2019 etc., normalized into a
   single table. None exist publicly; would have to be re-digitized
   figure-by-figure (~1-2 days of work, would constitute a separate
   replication slot).
5. **No author-contact channel** per task policy. (Would normally request
   the parameter table directly from the corresponding author.)
6. **No paid endpoint** per task policy. (Would normally use a library
   institutional access to pull the Elsevier PDF.)

What the smoke itself does *not* do, even given its inputs:

* Does not implement the paper's per-endpoint K_iDSB/K_cDSB and
  per-endpoint half-life fits (paper has ≥ 5 endpoints; smoke has 1
  DU145-like parametrization).
* Does not implement multi-pulse irradiation schedules with inter-pulse
  reoxygenation (paper considers single-pulse FLASH, but a complete
  reproduction would test pulsed delivery too).
* Does not implement the indirect-action / DMSO scavenger handling that
  Liew 2020 added (open-access, would be straightforward to port if needed).
* Does not propagate parameter uncertainty (no Bayesian/MCMC layer); the
  paper itself is point-estimate per endpoint, but for replication
  robustness this would be an upgrade.
* No model-to-model cross-validation against the independent open
  implementations (`sjmcmahon/FLASH-OER`, `igoncres/flash-radiotherapy`,
  `openFLASH/radioBioModel`) — listed as a candidate L4 follow-up in
  `FIRST_PASS_REPORT.md` § 6.

---

## 8. Verdict

**SPOT-CHECK.** Mechanism is implemented faithfully from open
predecessors (Liew 2019, Liew 2020) and from the open sibling
(Liew 2022 IJMS). Qualitative FLASH-at-low-O2 direction reproduces.
Two of the paper's quantitative central claims (C5 = FLASH peaks at
physoxia; C6 = monotone SF-vs-dose-rate above a threshold) are
**not** reproduced with literature-default parameters; this is
expected because the paper's actual fitted parameters (specific
`g_ROD`, `τ_reox`, per-endpoint repair and lethality coefficients) are
behind a paywall and have never been released publicly. The replication
covers ~25-33 % of the paper's primary analyzable units and 6 / 8
*testable* claims; both numbers are below the 80 % thresholds, so this
is explicitly **not** a REPLICATED slot.

Recommended downstream tag (consistent with first-pass recommendation):
`smoke-only: closed paper + closed code; qualitative FLASH-sparing at low O2
reproduced; quantitative FLASH-at-physoxia and monotone-dose-rate claims
NOT reproduced with literature-default parameters; paywall block is structural`.

---

### Audit scorecard

* **Coverage:** 3-4 of ~12 primary analyzable units explicitly covered
  (~25-33 %) → **3/10**.
* **Agreement:** 6/8 *testable* claims verified (mostly structural /
  input-prior), 2 directional / quantitative claims contradicted, 3
  paywall-blocked claims not tested. On testable subset only: 75 %
  agreement; on full claim set: 6/11 = 55 % → **5/10**.
* **Verdict:** SPOT-CHECK (per protocol § 5: < 50 % scope coverage,
  numeric agreement only on inputs and qualitative direction, paper's
  headline numbers untested).

### Repro blockers (3-line summary)

1. **Elsevier paywall** on Liew et al. 2021 IJROBP DOI `10.1016/j.ijrobp.2020.12.048` (paper + supplement) — Unpaywall confirms no open copy anywhere; specific missing artifact = the supplemental ZIP containing per-endpoint fitted parameters (`g_ROD`, `τ_reox`, K_iDSB, K_cDSB, repair half-lives per endpoint).
2. **Closed UNIVERSE engine** — Liew/Mairani lab has never released source code for any UNIVERSE paper (2019, 2020, 2021, 2022 all silent or "Not applicable"); no GitHub repo, no Zenodo archive.
3. **No consolidated open validation dataset** for the in-vivo endpoints (mouse tail necrosis, brain memory, lung, intestine) the paper fits — only the original primary-source figures (Montay-Gruel, Vozenin, Favaudon, Beyreuther) exist, undigitized.

---

VERDICT=SPOT-CHECK COVERAGE=3/10 AGREEMENT=5/10
Blocker 1: Elsevier paywall on Liew 2021 IJROBP paper + supplement (missing: Elsevier supplemental ZIP with per-endpoint g_ROD, τ_reox, K_iDSB, K_cDSB, repair half-lives).
Blocker 2: UNIVERSE engine source code never released by Liew/Mairani lab across 4+ papers.
Blocker 3: no consolidated open dataset for the in-vivo FLASH endpoints (mouse tail/brain/lung/intestine) the paper fits.
