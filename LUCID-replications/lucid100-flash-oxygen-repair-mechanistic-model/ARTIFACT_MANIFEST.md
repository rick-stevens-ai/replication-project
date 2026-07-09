# Artifact Manifest — LUCID-100 slot 27

Paper: **Liew H, Mein S, Dokic I, Haberer T, Debus J, Abdollahi A, Mairani A.**
"Deciphering Time-Dependent DNA Damage Complexity, Repair, and Oxygen Tension:
A Mechanistic Model for FLASH-Dose-Rate Radiation Therapy."
*Int. J. Radiation Oncology Biol. Phys.* **110**(2): 574-586, 2021.
DOI: [10.1016/j.ijrobp.2020.12.048](https://doi.org/10.1016/j.ijrobp.2020.12.048)

Harvest performed: 2026-06-09 (UTC-5).

## 1. The paper itself

| Resource | Where to get it | Status this harvest | Notes |
|---|---|---|---|
| Full text PDF | Elsevier (red journal) | **PAYWALLED (HTTP 403)** | unpaywall.org confirms `is_oa=false`, `has_repository_copy=false` |
| Abstract | OSTI BIBLIO 23198562 / Crossref / Semantic Scholar | captured to `artifacts/osti_page.html`, `artifacts/crossref_liew2021.json`, `artifacts/semanticscholar_liew2021.json` | full abstract recovered + reference list + author affiliations |
| Author preprint | none found (DKFZ inrepo02, ResearchGate, OSTI BIBLIO) | none | DKFZ record returns SPA shell; ResearchGate would need an account; no arXiv/bioRxiv preprint exists |
| Supplementary information | Elsevier supplement (red journal) | **PAYWALLED (HTTP 403)** | numeric parameter tables and validation datasets are in the supplement and were not obtained |

## 2. Author code / data

| Resource | URL | Status | Notes |
|---|---|---|---|
| UNIVERSE source code | none published | **NOT AVAILABLE** | The data-availability statement of the immediate follow-up paper (Liew 2022 IJMS) is "Not applicable"; the 2021 Deciphering paper makes no code-availability statement at all and has no public repository |
| Underlying experimental data | references [12,14-19, and dozens of in-vivo / in-vitro studies cited in the 52-ref bibliography] | mostly published papers, not raw data | The paper aggregates literature endpoint data; no consolidated digitized dataset was released |
| FLASH-effect parameter table | Tables 1-2 of the paper | **PAYWALLED** | Reported parameter values (g_ROD, tau_reox, fast/slow repair half-lives, endpoint-specific lethalities) are not recoverable without paywall access |

## 3. Predecessor / sibling UNIVERSE papers (used as substitute documentation)

Both are **open-access (MDPI)** and contain the static UNIVERSE giant-loop equations the 2021 paper extends:

| Citation | DOI / PMCID | Local copy |
|---|---|---|
| Liew et al. 2019 — Modeling the Effect of Hypoxia and DNA Repair Inhibition on Cell Survival after Photon Irradiation. *Int. J. Mol. Sci.* 20:6054 | 10.3390/ijms20236054 / **PMC6929106** | `artifacts/PMC6929106.xml` (Europe PMC full-text XML; recovered Eqs. 1-7 incl. HRF parametrization) |
| Liew et al. 2020 — Modeling Direct and Indirect Action on Cell Survival After Photon Irradiation under Normoxia and Hypoxia. *Int. J. Mol. Sci.* 21:3471 | 10.3390/ijms21103471 / **PMC7278970** | `artifacts/PMC7278970.xml` (Europe PMC; Eqs. 1-10 incl. DMSO indirect-action handling) |
| Liew et al. 2022 — Impact of DNA Repair Kinetics and Dose Rate on RBE Predictions in the UNIVERSE. *Int. J. Mol. Sci.* 23:6268 | 10.3390/ijms23116268 | already captured under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-universe-repair-doserate-rbe/mcmahon_prise_2021.pdf` (subagent slot covered the 2022 paper) — the python scaffolding in that folder is the closest existing UNIVERSE re-implementation in this workspace |

## 4. Local prior-art reuse

The neighbouring LUCID-100 replication slot **lucid-universe-repair-doserate-rbe** already
implements the static + repair-kinetic UNIVERSE giant-loop Monte Carlo in
`code/universe_core.py` (271 LOC) and a fuller stochastic driver in
`code/simulate_universe.py` (586 LOC). For this slot we re-state the relevant
equations directly so the new code module is self-contained and stays small
(`code/flash_oxygen_smoke.py`, ~290 LOC, no cross-folder imports). The
formulations agree.

## 5. Sibling FLASH oxygen-depletion models (NOT Liew's UNIVERSE; useful for context only)

| Resource | Repo | Notes |
|---|---|---|
| McMahon FLASH-OER | https://github.com/sjmcmahon/FLASH-OER | Simple oxygen-depletion + OER model; ref-[14]-adjacent style; would be a separate replication target |
| González-Crespo flash-radiotherapy | https://github.com/igoncres/flash-radiotherapy | TCP/iso-effectiveness with ROD; companion to Pratx 2019 lineage |
| openFLASH/radioBioModel | https://github.com/openFLASH/radioBioModel | Physicochemical radiolysis model |

None of these are the Liew/Mairani UNIVERSE codebase. They are independent
implementations of overlapping mechanisms and were NOT used in this smoke;
they are listed for triage / future cross-validation.

## 6. Files in this folder

```
lucid100-flash-oxygen-repair-mechanistic-model/
├── ARTIFACT_MANIFEST.md     # this file
├── README.md
├── PROGRESS.md
├── FIRST_PASS_REPORT.md
├── artifacts/
│   ├── PMC6929106.xml                 # Liew 2019, Europe PMC full text
│   ├── PMC7278970.xml                 # Liew 2020, Europe PMC full text
│   ├── crossref_liew2021.json         # crossref metadata + full reference list of the target paper
│   ├── semanticscholar_liew2021.json  # Semantic Scholar metadata
│   ├── osti_page.html                 # OSTI biblio page (abstract scraped from <meta>)
│   └── dkfz_record.html               # DKFZ inrepo SPA shell (no useful content)
├── code/
│   └── flash_oxygen_smoke.py          # minimal mechanistic smoke implementation
├── results/
│   └── smoke_sweep.csv                # 20-condition SF sweep (3 doses x 5 [O2] x 2 dose rates)
├── figures/
│   └── smoke_flash_vs_conv_oxygen.png # SF vs initial [O2], CONV vs FLASH, two doses
└── logs/
    └── smoke_run.log                  # run wall-clock + parameter snapshot
```
