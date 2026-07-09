# Predictive DNA Damage Signaling for Low-Dose Ionizing Radiation

LUCID100 Wave 2 slot 12 (Wave 2 backfill).

## Paper

- **Title:** Predictive DNA damage signaling for low-dose ionizing radiation
- **Authors:** Park JI, Jung SY, Song KH, Lee DH, Ahn J, Hwang SG, Jung IS, Lim DS, Song JY
- **Affiliation (corresponding):** Korea Institute of Radiological and Medical Sciences (KIRAMS); CHA University
- **DOI:** 10.3892/ijmm.2024.5380
- **PMID / PMCID:** 38695243 / PMC11093554
- **Venue / year:** Int J Mol Med, vol. 53, issue 6, art. 56, 2024 (published 30 Apr 2024; PMC release 14 May 2024)
- **License:** CC BY-NC-ND 4.0 (open access via PMC / Europe PMC)
- **Master TSV row:** rank 43, Wave 2, tier A, score 19, themes "DNA repair / DDR; dose-rate / low-dose response; radiation quality / RBE; computational model / simulation", worktype "simulation/model replication"
- **PMC URL:** <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11093554/>
- **Europe PMC full-text XML:** `artifacts/europepmc_fullText.xml` (canonical text; PMC HTML fetch is gated by reCAPTCHA, EuropePMC PDF endpoints currently flaky)

## TL;DR — what the paper actually is

Despite the LUCID master TSV worktype label of *"simulation/model replication"*, this is a **wet-lab biomarker discovery paper**, not a computational/simulation study:

1. **Candidate selection from literature (loosely "public database"):** 16 proteins were curated from two prior reviews (refs [8] Zhang 2012 Cytokine; [10] Marchetti 2006 Int J Radiat Biol) — DDR + cell-cycle + cytokine candidates.
2. **In vitro screen:** IM-9 (B-lymphoblastoid, p53 WT), HuT 78 (T-lymphocyte, p53 mutant p.Arg196Ter), and human PBMCs irradiated 0–2 Gy at 12 doses with two ¹³⁷Cs γ-sources (3.5 Gy/min Biobeam-8000; 0.1 cGy/min LDI-KCCH 137). Western blot + ELISA at 0.5–72 h.
3. **Down-selection rules:** (i) detectable in low-dose IR range, (ii) concentration-dependent response, (iii) applicable to blood samples. → 4 surviving markers: **p-ATM, p-CHK2, p-p53, γH2AX**.
4. **Pharmacological perturbation:** cinobufagin (ATM/CHK2 activator), KU60019 (ATM inh.), BML-277 (CHK2 inh.), pifithrin-α (p53 inh.), nutlin-3a (p53 act.). BML-277 emerges as the most effective radioprotector (reduces p-CHK2, γH2AX, apoptosis in PBMCs).
5. **In vivo:** C57BL/6 ⁶⁰Co γ irradiation at 3 Gy (sublethal) and 8 Gy (lethal). Cinobufagin gives mild, statistically non-significant survival benefit at 5 mpk; increases BM cellularity.

## Replication classification

| Claim class | Reproducibility tier |
|---|---|
| Down-selection logic (16 → 4 markers from literature criteria) | **Tier 1/3** — directly reproducible as a *literature-curation logic notebook*, not as a discovery pipeline (no public omics dataset is queried; "public database" is editorial shorthand for the two cited reviews) |
| Concentration-dependent dose–response curves (Fig 1B 5PL fits) | **Tier 3** — digitizable from figure; underlying band/ELISA values not deposited |
| Cinobufagin survival Kaplan–Meier (Fig 2C) | **Tier 3** — digitizable; raw mouse-level data on request from corresponding author |
| BML-277 apoptosis reduction in PBMCs (Fig 4A) | **Tier 3** — digitizable bar graphs; no raw FCS files |
| Whole wet-lab phenotypic screen | **Tier 4** — requires cell lines, antibodies, irradiator, PBMC donors, mice; not feasible without lab |

Data availability statement (verbatim): *"The datasets used and/or analyzed during the current study are available from the corresponding author on reasonable request."* → **No deposited supplementary data, no code, no GEO/ArrayExpress/PRIDE accession.** Per task rules, no author contact.

## Replication scope (no-lab feasible)

We can produce three legitimate computational artifacts without a wet lab:

1. **Candidate-selection logic replay (`scripts/replay_selection.py`)** — encode the 16-protein panel + the three down-selection criteria as a structured table; mark which proteins satisfy which criteria per the paper's own data; verify the 4-survivor set is the unique solution.
2. **Dose–response 5PL refit (`scripts/fit_5pl_demo.py`)** — paper says Fig 1B was fit with "asymmetrical sigmoidal, five-parameter curves". Implement the 5PL with `scipy.optimize.curve_fit` against either (a) digitized Fig 1B points (TODO; requires image grab + WebPlotDigitizer), or (b) a synthetic ATM-like example so the fitter is unit-tested. Smoke is (b).
3. **Public-DB cross-check (manual / scripted)** — for the four winners, look up annotations in MSigDB / Reactome ("DNA Double-Strand Break Repair", "G2/M DNA Damage Checkpoint") to confirm pathway membership claims. Optional; not run in first pass.

Heavy compute: **not required**. All work fits in a Python venv on CherryRd. No job plan needed.

## Folder layout

```
lucid100-predictive-dna-damage-signaling-low-dose/
├── README.md                  ← this file
├── PROGRESS.md                ← run log
├── FIRST_PASS_REPORT.md       ← verdict + next steps
├── ARTIFACT_MANIFEST.tsv      ← provenance of every artifact
├── artifacts/
│   ├── europepmc.json              ← Europe PMC core metadata (1 record)
│   ├── europepmc_fullText.xml      ← full JATS-XML body+references
│   └── europepmc_PMC11093554.pdf   ← 5.9 MB rendered PDF (all figures inline)
├── scripts/
│   ├── replay_selection.py    ← 16→4 panel down-selection replay (smoke)
│   └── fit_5pl_demo.py        ← 5PL dose-response fit unit test (smoke)
└── notes/
    └── claims.md              ← bulletised claims with anchor refs
```

## How to run smoke

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-predictive-dna-damage-signaling-low-dose
python3 scripts/replay_selection.py
python3 scripts/fit_5pl_demo.py
```

Both scripts use only the stdlib + numpy + scipy and exit non-zero on assertion failure.
