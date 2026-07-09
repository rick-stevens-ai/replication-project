# LUCID100 Slot 31 — IFITM3 / Alzheimer's / Low-Dose-Rate Radiation

**Paper:** Son Y, Lee CG, Kim JS, Lee H-J. *Low-dose-rate ionizing radiation affects innate immunity protein IFITM3 in a mouse model of Alzheimer's disease.* International Journal of Radiation Biology, 99(11):1649-1659, 2023.
**DOI:** [10.1080/09553002.2023.2211142](https://doi.org/10.1080/09553002.2023.2211142)
**PMID:** 37162420   **S2 paperId:** 1a97870e10d00a628c34dbe73e5a9e38c7951351
**LUCID100 slot:** 31 (Wave 4, A-tier, score 15)

## Master-row category recommendation

Master TSV (`LUCID100_SOLID_MASTER_QA.tsv` line 75) tags this as
**"simulation/model replication"** under topics including "computational
model / simulation."

**This is incorrect.** The paper is a fully in vivo wet-lab study:

- Live 5xFAD vs WT mice
- 112-day chronic LDR exposure at cumulative 0, 0.1, 0.3 Gy
- Behavioral assays (Y-maze, open field)
- IHC/qPCR/western for gliosis (Iba1/GFAP), cytokines (IL-1β/IL-6/TNF-α), IFN-γ, and IFITM3

There is **no computational model, no simulation, no code, no public
dataset deposit, and no supplementary file** indicated in any
metadata source (Crossref/PubMed/EuropePMC/Unpaywall).

**Recommended retag:** `wet-lab in vivo / no public data` →
**NO-GO for in-silico replication.** This row should probably be
demoted from Wave 4 A-tier or moved to a "non-replicable wet-lab"
bucket. See `NO_GO_REPORT.md` for the full verdict.

## Authors / affiliations

- Yeonghoon Son — KIRAMS, Seoul, Korea
- Chang Geun Lee — DIRAMS, Busan, Korea
- Joong Sun Kim — Chonnam National University, Gwangju, Korea
- Hae-June Lee (corresponding) — KIRAMS, Seoul, Korea

## Repo layout

```
lucid100-ifitm3-alzheimers-low-dose-rate/
├── README.md                ← this file
├── PROGRESS.md              ← step-by-step run log
├── FIRST_PASS_REPORT.md     ← scoping verdict + narrative
├── NO_GO_REPORT.md          ← no-go decision with rationale
├── artifacts/
│   ├── MANIFEST.md          ← artifact inventory
│   ├── unpaywall.json
│   ├── semantic_scholar.json
│   └── europepmc.json
├── data/                    ← (empty: no public data found)
├── figures/                 ← (empty: no PDF to digitize without paywall access)
├── notes/                   ← scratch notes
└── scripts/
    └── smoke_scope.py       ← smoke-test that re-checks OA status + metadata
```

## Quick reproduction of this scoping pass

```bash
python3 scripts/smoke_scope.py
```

Re-pulls Unpaywall + Semantic Scholar + EuropePMC and confirms paper
remains closed-access with no PMC mirror and no listed supplementary
material. If status ever changes (publisher releases OA, KIRAMS
deposits data), this script will flag it.
