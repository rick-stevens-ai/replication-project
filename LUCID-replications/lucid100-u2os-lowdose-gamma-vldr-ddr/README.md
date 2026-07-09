# LUCID100 Slot 43 — U2OS Low-Dose Very-Low-Dose-Rate Gamma DDR

**Paper:** Płódowska M, Krakowiak W, Węgierek-Ciuk A, Gałczyńska K, Pasińska K, Sobota D, Wołowiec P, Braziewicz J, Lankoff A, Arabski M, Wojcik A, Lisowska H. *DNA damage response of U2OS cells to low doses of gamma radiation delivered at very low dose rate.* **DNA Repair** 152:103875 (Aug 2025).

- **DOI:** [10.1016/j.dnarep.2025.103875](https://doi.org/10.1016/j.dnarep.2025.103875)
- **PMID:** 40737910 · **PII:** S1568-7864(25)00071-0
- **License:** CC-BY 4.0 (open access, hybrid; Polish RAP 2025 waiver)
- **Corresponding author:** Halina Lisowska — `halina.lisowska@ujk.edu.pl` (Jan Kochanowski University, Kielce, Poland)
- **LUCID100 master:** rank **74**, Wave 5, Tier A, priority 14 — *omics/signature replication* worktype (in catalog).
- **QA decision in master:** KEEP: relevant and replication-plausible.

## Scope (this folder)

First-pass artifact harvest + replication scoping. **Status: NO-GO for full replication this pass** because the article body and supplementary files could not be retrieved (publisher Cloudflare gating + no PMC mirror + no public data deposition flagged by Europe PMC). Computational replication scaffolding (53BP1 foci kinetics model + skeleton fitter) is in place so the next pass can drop in digitized figure data and run end-to-end.

## What the paper studies

- **Cell line:** U2OS (osteosarcoma, *wild-type p53*).
- **Adapting dose (AD):** very-low-dose-rate gamma — two arms:
  - 5.9 mGy @ 31 µGy/h
  - 10.5 mGy @ 55 µGy/h
- **Challenging dose (CD):** 1 Gy photon @ 1 Gy/min.
- **ATM perturbation:** KU-55933 (small-molecule ATM kinase inhibitor).
- **Endpoints:**
  1. **53BP1 foci** formation and decay kinetics (immunofluorescence).
  2. **Cell-cycle progression** (G2 block).
  3. **Gene expression** (panel; method/format not yet captured — likely qPCR panel given Europe PMC `hasData=N`).
- **Headline findings (per abstract):**
  - AD alone → significant 53BP1 foci induction; *not blocked by KU-55933* (i.e., not strictly ATM-dependent at VLDR).
  - AD modulates response to subsequent CD.
  - KU-55933 *inhibits* foci induction by CD-alone but *fails* to inhibit AD-alone or AD+CD.
  - KU-55933 *potentiates* G2 block in AD+CD cells.
  - Gene expression modulated by AD.

## What is actually fetchable (this pass)

| Artifact                          | Status      | Path                                      |
| --------------------------------- | ----------- | ----------------------------------------- |
| Crossref record                   | ✓ saved     | `source/crossref.json`                    |
| Europe PMC core record            | ✓ saved     | `source/europepmc_metadata.json`          |
| Unpaywall (OA status)             | ✓ saved     | `source/unpaywall.json`                   |
| Elsevier coredata XML (metadata)  | ✓ saved     | `source/elsevier_coredata.xml`            |
| PubMed abstract                   | ✓ saved     | `source/pubmed_abstract.txt`              |
| **Full text PDF**                 | ✗ blocked   | Cloudflare bot-check on ScienceDirect & ResearchGate; PMC has no mirror |
| **Supplementary files (mmc*)**    | ✗ unknown   | Cannot enumerate without rendering the article landing page |
| **Public omics deposition**       | ✗ none flagged | Europe PMC `hasData=N`, `hasDbCrossReferences=N`, `hasSuppl=N` |
| **Author code/repo**              | ✗ not located | No GitHub/Zenodo/figshare links via search |

See `notes/artifact_manifest.json` for the machine-readable manifest and `notes/data_availability_check.md` for the search trail.

## Layout

```
source/                — publisher/index metadata snapshots
supplementary/         — (empty) target for mmc1.docx, mmc2.xlsx, ... once PDF landing page is rendered
data/                  — (empty) target for digitized Fig 1/2/… points and any table data
code/                  — skeleton kinetics model + fit driver
results/               — (empty) target for fitted parameters & validation tables
figures/               — (empty) target for replication overlays
notes/                 — search trail, manifest, replication design
PROGRESS.md            — turn-by-turn log
README.md              — this file
FIRST_PASS_REPORT.md   — verdict + next-pass plan (NO-GO for compute now)
```

## Smoke test (runnable today)

```
python3 code/foci_kinetics.py --demo
```

Produces a synthetic AD/CD/AD+CD 53BP1 foci curve set with a Lengert-style two-component model (peak generation + first-order resolution) and writes `results/smoke_synthetic.csv` + `figures/smoke_synthetic.png`. This is a placeholder until digitized figure data lands in `data/`.

## Next-pass plan

See `FIRST_PASS_REPORT.md` § Next pass.
