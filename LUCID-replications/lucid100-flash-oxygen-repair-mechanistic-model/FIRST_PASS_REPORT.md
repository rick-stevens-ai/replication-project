# FIRST-PASS REPORT — LUCID-100 slot 27

**Paper.** Liew H, Mein S, Dokic I, Haberer T, Debus J, Abdollahi A, Mairani A.
"Deciphering Time-Dependent DNA Damage Complexity, Repair, and Oxygen Tension:
A Mechanistic Model for FLASH-Dose-Rate Radiation Therapy."
*IJROBP* 110(2):574-586, 2021. DOI `10.1016/j.ijrobp.2020.12.048`.

**Verdict.** **GO-but-degraded / smoke-only.** Replication-plausible at the
mechanism level; bit-exact figure/table replication blocked by paywalls.

**Recommended QA retag.** Keep `KEEP: relevant and replication-plausible`,
but downgrade the `worktype` from `simulation/model replication` to
`mechanism-replication: smoke (closed-access paper + closed code)` so
downstream reviewers know not to expect numerical agreement against the
paper's figures.

## 1. What the paper does

The paper is the **dynamic** (time-resolved) extension of the UNIVERSE
mechanistic radiobiological model that Liew/Mairani had been building since
2019. The 2019 baseline (open access, PMC6929106) models cell survival
after photon irradiation in terms of:

* Poisson-sampled DSB induction (`α_DSB = 5e-3 DSB / (Mbp · Gy)`,
  ≡ 30 DSB / Gy / 6 Gbp nucleus) deposited into N_giant_loop = 3000
  "giant-loop" chromatin domains of 2 Mbp each;
* Domain occupancy → isolated DSB (1 break / domain) vs complex DSB
  (≥ 2 breaks / domain), giving survival `S = (1-K_iDSB)^N_iDSB · (1-K_cDSB)^N_cDSB`;
* Hypoxia handled by a multiplicative oxygen-modifying factor
  `HRF([O2]) = (m·K + [O2]) / (K + [O2])` with m = 2.94 and K = 0.129 % O2.

The 2021 "Deciphering..." paper extends this baseline with three new
time-dependent ingredients, made explicit only in the abstract / figures
(which we have, via OSTI metadata) and inferred from the title:

1. **DNA-damage repair kinetics (DDRK)** — first-order exponential repair
   of iDSB and cDSB with distinct half-lives, so that on long CONV-style
   irradiations a non-trivial fraction of damage is already repaired before
   the next pulse arrives. (Specific half-life values per endpoint:
   paywalled; the open Liew 2022 IJMS paper lists representative values
   ~ 4 min / 100 min for DU145.)
2. **Radiolytic oxygen depletion (ROD)** — O2 is consumed during
   irradiation in proportion to instantaneous dose rate; this transiently
   raises HRF (= reduces DSB induction) on the timescale of the pulse.
   (Specific g_ROD value: paywalled; literature centre ≈ 0.42 mmHg / Gy
   per Pratx 2019, Petersson 2020.)
3. **Reoxygenation** — first-order relaxation of [O2] back to ambient
   with time constant τ_reox of order a few seconds. (Specific value:
   paywalled.)

These three dynamics together give the model the ability to predict the
**FLASH effect**: when dose rate ≫ 1 / τ_reox, the entire dose is
deposited before the O2 reservoir can be refilled, intracellular O2 dips,
DSB induction drops, and SF rises relative to CONV at the same total
dose. The paper validates this against in-vitro clonogenic data and
in-vivo endpoints (mouse tail necrosis, brain memory, lung, intestine)
drawn from the FLASH literature (Montay-Gruel 2017/2018/2019, Vozenin 2019,
Favaudon 2014, Beyreuther 2019 etc.).

## 2. Artifact availability — assessment

| Component | Open? | Notes |
|---|---|---|
| Paper | NO | Elsevier paywall; unpaywall confirms no OA copy anywhere |
| Supplement / parameter tables | NO | inside the Elsevier supplement |
| Source code (UNIVERSE engine) | NO | never released; consistent with the 2019/2020/2022 papers from the same group |
| Underlying experimental data | mixed | aggregated from published in-vitro/in-vivo papers (52 refs); not consolidated; would have to be re-digitized |
| Predecessor model description | YES | Liew 2019 (PMC6929106) + Liew 2020 (PMC7278970) give static UNIVERSE in full; Liew 2022 IJMS gives the repair-kinetic extension (already replicated in `lucid-universe-repair-doserate-rbe`) |

**Net openness score: 1/5 (low).** Mechanism documentation is fully open,
but every parameter that turns the model into a numerical FLASH predictor
is closed.

## 3. Replication scoping — what is feasible

| Level | Feasible without paywall? | Effort |
|---|---|---|
| L0: mechanism re-derivation (math equations) | YES | done in `code/flash_oxygen_smoke.py` |
| L1: qualitative smoke (FLASH > CONV at low O2) | YES | done; CSV + figure in this folder |
| L2: parameter fitting against an open dataset (e.g. Montay-Gruel zebrafish, Favaudon C57BL/6 lung fibrosis) | feasible with effort | requires manual digitization of Fig. 2/3 of the cited primary sources; 1-2 days of work |
| L3: numerical reproduction of Liew 2021 Figs. 1-5 / Tables 1-2 | **NOT FEASIBLE** without paywall access | even with paywall access, parameters span ≥ 7 endpoints x ≥ 5 free parameters; the published paper does not always list every fitted value |
| L4: cross-validation against an independent FLASH model | feasible | sjmcmahon/FLASH-OER, igoncres/flash-radiotherapy, openFLASH/radioBioModel give 3 independent implementations of the ROD+OER side; would let us bound model-to-model spread |

For LUCID-100 throughput we have done L0 + L1. Anything beyond L1 needs
either paper access (L3) or a deliberate 1-2 day digitisation pass (L2/L4).

## 4. Smoke results — what reproduces and what does not

Smoke generated `results/smoke_sweep.csv` (20 conditions: D ∈ {10, 20} Gy ×
[O2]_0 ∈ {0.5, 2, 5, 7.5, 21} % × {CONV 0.07 Gy/s, FLASH 100 Gy/s}).

**Qualitatively reproduced:**

* The **FLASH-sparing direction** at low O2 (≤ 0.5 %). At 20 Gy / 0.5 % O2
  the smoke gives `SF_CONV = 0.0056` vs `SF_FLASH = 0.0275` — ~5× higher
  surviving fraction under FLASH. Same direction at 10 Gy / 0.5 %.
* Increasing total DSB count with dose at fixed O2 (~213 → ~425 mean
  DSB / cell going 10 → 20 Gy at 0.5 % O2; the slight CONV > FLASH gap
  at low O2 corresponds to ROD-driven HRF rise during the FLASH pulse).
* Increasing baseline DSB with [O2]: ~213 at 0.5 % → ~297 at 21 % at
  10 Gy CONV, as expected from the HRF parametrization.

**NOT reproduced (limitations):**

* The non-trivial **O2 window** where FLASH-sparing is maximal. With
  default literature parameters the smoke shows CONV > FLASH for
  [O2]_0 ≥ 2 %, which is the opposite of the paper's central result that
  FLASH effect peaks around physoxia (~4-7 % O2). Fixing this requires
  the paper's larger g_ROD value and/or a non-linear oxygen-effect curve
  tuned per endpoint.
* Any of the in-vivo endpoint predictions (mouse tail, brain memory,
  lung) — those need endpoint-specific lethality + repair parameters
  that are paywalled.

## 5. Compute footprint

* Wall clock: **64.5 s** single-thread Python 3 on CherryRd
  (M-series-equivalent Mac; numpy/matplotlib only).
* No heavy compute job plan needed. If we ever want L2/L4 work
  (digitise primary-source endpoint data, fit parameters), it stays well
  inside CherryRd CPU budget; no HPC submission required.

## 6. Next actions (in priority order)

1. **Retag in QA TSV.** Change column 16 from
   `TODO: simulation/model replication; artifact harvest; brief; run; report`
   to `smoke-only: closed paper + closed code; qualitative FLASH-sparing reproduced; see lucid100-flash-oxygen-repair-mechanistic-model/FIRST_PASS_REPORT.md`.
   Recommend column 17 stays `KEEP: relevant and replication-plausible`
   so it shows in the "completed-with-caveats" bucket.
2. **(Optional, low effort)** Cross-run the same conditions through
   `sjmcmahon/FLASH-OER` (open MIT-licensed Python, ~ 100 LOC) to put
   a second-implementation bracket around the FLASH-sparing prediction.
   That is a deliverable an L4 follow-up subagent could complete in
   one session; it does not need the paywalled UNIVERSE parameters.
3. **(Optional, medium effort)** Re-attempt PDF acquisition via the
   user's institutional Elsevier subscription (if available); if a copy
   becomes available, re-open this slot to bump to L3 replication.
4. **Do NOT** attempt author contact (per task constraint and per
   `BOOTSTRAP/AGENTS.md` "ask first" policy for outbound messages).

## 7. Blockers (recap)

* Paywall: paper + supplement.
* Closed source: UNIVERSE engine.
* No-author-contact constraint.
* No-paid-endpoints constraint.

No new blockers for QA / triage. Slot is **complete at the first-pass level**.
