# LUCID-100 #27 — Liew et al. 2021 IJROBP — "Deciphering" FLASH dynamic UNIVERSE

Paper: **Liew H, Mein S, Dokic I, Haberer T, Debus J, Abdollahi A, Mairani A.**
"Deciphering Time-Dependent DNA Damage Complexity, Repair, and Oxygen Tension:
A Mechanistic Model for FLASH-Dose-Rate Radiation Therapy."
*Int. J. Radiation Oncology Biol. Phys.* **110**(2): 574-586, 2021.
DOI: `10.1016/j.ijrobp.2020.12.048`. Lead group: DKFZ Heidelberg.

## Scope of this replication

**This is a first-pass artifact harvest + scoping + qualitative smoke replication.**
It is **not** a numerical reproduction of the paper's figures/tables, and it
cannot be one, because:

1. The paper itself is paywalled (Elsevier, Red Journal). Unpaywall confirms
   `is_oa=false`, `has_repository_copy=false` and we have no OA copy.
2. No supplementary information / parameter tables / validation data were obtained.
3. The Liew/Mairani group has **never** released the UNIVERSE source code,
   parameter database, or simulation inputs for any of their 2019-2024 UNIVERSE
   papers (verified by checking the data-availability statements of the open-access
   predecessors PMC6929106 and PMC7278970, and the 2022 follow-up which we
   replicated in slot `lucid-universe-repair-doserate-rbe`).
4. The paper's key contribution is the **dynamic** extension that adds
   (i) time-dependent first-order DNA-damage repair on multiple complexity
   classes, (ii) radiolytic oxygen depletion (ROD) during irradiation, and
   (iii) reoxygenation. The numerical values for g_ROD, tau_reox, the fast/slow
   repair half-lives per endpoint, and the lethality coefficients per
   biological endpoint (mouse tail necrosis, brain memory, lung, intestine,
   in-vitro clonogenic) are in the paywalled tables/supplement.

What we **can** do, and have done:

* Recover the **static** UNIVERSE giant-loop equations from the OA
  predecessors (Eqs. 1-7 of Liew 2019 + Eqs. 1-10 of Liew 2020).
* Implement those equations in pure Python/NumPy.
* Add a **literature-bounded** ROD + reoxygenation ODE on top
  (g_ROD ≈ 0.42 mmHg/Gy, tau_reox ≈ 5 s — central values from
  Pratx 2019, Petersson 2020, Labarbe 2020).
* Add first-order exponential repair using representative half-lives
  from Liew 2022 IJMS Table 1 (DU145: 4 min / 100 min for iDSB / cDSB).
* Run a 20-condition sweep (2 doses × 5 [O2] levels × 2 dose-rates)
  and check that the *qualitative* FLASH-sparing direction matches the
  central claim of the paper at low O2.

## What the smoke shows

`results/smoke_sweep.csv` and `figures/smoke_flash_vs_conv_oxygen.png`
summarise a 20-condition Monte Carlo sweep.

**Headline qualitative result (D = 20 Gy, 0.5 % initial O2):**

| Regime | Dose rate | Mean SF | Direction |
|---|---|---|---|
| CONV  | 0.07 Gy/s   | **0.0056** | baseline |
| FLASH | 100 Gy/s    | **0.0275** | **higher SF -- FLASH-sparing reproduced qualitatively** |

The same direction holds at D = 10 Gy / 0.5 % O2 (CONV 0.118 → FLASH 0.168).
At ≥ 2 % initial O2 the smoke shows CONV > FLASH in this minimal parametrization
because the small ROD-driven O2 dip is masked by in-irradiation repair during
the long CONV exposure; that is a known limitation of toy ROD-only smokes and
matches the discussion in Pratx 2019 / Petersson 2020. The paper itself
predicts a non-trivial O2 window where the FLASH effect is largest; reproducing
that window quantitatively requires the paper's parameter values, which are
paywalled.

## Reuse

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-flash-oxygen-repair-mechanistic-model
python3 code/flash_oxygen_smoke.py
```

Runtime: ~65 s on CherryRd CPU. Dependencies: `numpy`, `matplotlib`.

## Files

* `code/flash_oxygen_smoke.py` — minimal dynamic-UNIVERSE smoke
* `results/smoke_sweep.csv` — 20-condition SF + DSB + O2 trajectory summary
* `figures/smoke_flash_vs_conv_oxygen.png` — SF vs initial [O2] at D = 10 and 20 Gy
* `logs/smoke_run.log` — run summary + parameters used
* `artifacts/` — paper metadata + Europe PMC full-text of the OA predecessors
* `ARTIFACT_MANIFEST.md` — detailed inventory + sources
* `PROGRESS.md` — chronology
* `FIRST_PASS_REPORT.md` — verdict

## Verdict

**Smoke-only / GO-but-degraded.** The mechanism is reproducible from open
predecessors. The numerical replication is blocked by paywalled
parameter tables. See `FIRST_PASS_REPORT.md` for a recommended QA retag.
