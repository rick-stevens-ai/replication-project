# Impact of Low-Dose CT Radiation on Gene Expression and DNA Integrity

LUCID100 Wave 2 slot 15 (Wave 2 backfill).

## Paper

- **Title:** Impact of Low-Dose CT Radiation on Gene Expression and DNA Integrity
- **Authors:** Schmid N, Gorte V, Akers M, Verloh N, Haimerl M, Stroszczynski C, Scherthan H, Orben T, Stewart S, Kubitscheck L, Kaatsch HL, Port M, Abend M, Ostheim P.
- **Affiliation (corresponding):** Bundeswehr Institute of Radiobiology affiliated to Ulm University, Munich, Germany.
- **DOI:** 10.3390/ijms262411869
- **PMID / PMCID:** 41465293 / PMC12732518
- **Venue / year:** Int J Mol Sci, vol. 26, issue 24, art. 11869, 2025 (electronic publication 9 Dec 2025)
- **License:** CC BY 4.0 (open access via Europe PMC / PMC)
- **Master TSV row:** rank 46, Wave 2, tier A, score 19, themes "DNA repair / DDR; dose-rate / low-dose response; omics / biomarkers / signatures; computational model / simulation", worktype "omics/signature replication"
- **PMC URL:** <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12732518/>
- **Europe PMC full-text XML:** `artifacts/europepmc_fullText.xml` (canonical JATS; MDPI HTML/PDF endpoints are gated by Akamai 403)

## TL;DR — what the paper actually is

A **prospective clinical biomarker study** in 60 adult patients undergoing diagnostic CT scans (mean DLP ≈ 562 mGy·cm, effective dose ≈ 8.3 mSv). Peripheral whole blood drawn before and after CT, with two post-scan protocols:

- **In vivo incubation** (post-CT sample drawn 4–6 h after scan, n = 28 in abstract / n = 27 in Table 2)
- **Ex vivo incubation** (post-CT sample drawn immediately after scan, then incubated 4 h ex vivo at 37 °C, n = 32 / n = 33)

Two assays:

1. **qRT-PCR** of 9 radiation-responsive genes (DDB2, FDXR, POU2AF1, WNT3, BAX, AEN, EDA2R, MIR34AHG, PHLDA3), normalized to PUM1, calibrated by ΔΔCt to each patient's own pre-CT sample.
2. **γ-H2AX + 53BP1 DSB focus assay** by immunofluorescence microscopy in a 12-patient subset (PBMCs from Ficoll, 100 nuclei/sample).

Headline findings:

- In vivo, six genes (EDA2R, MIR34AHG, PHLDA3, DDB2, FDXR, AEN) are significantly upregulated (p ≤ 0.041); ex vivo incubation masks the effect — i.e. the choice of incubation protocol matters more than has been appreciated in prior CT-biodosimetry literature.
- AEN and FDXR show a linear dose–response (DLP vs DGE) with r² = 0.66 and 0.56 respectively in vivo.
- γ-H2AX foci increase by 0.1 ± 0.15 RIF/cell post-CT in 12 patients — slight, NOT statistically significant (p = 0.37) at this dose.

## What is in the open-access JATS XML (good news for replication)

Despite the formal data-availability statement that "data … are available on request from the corresponding author … not publicly available due to privacy and ethical restrictions", **the appendix tables in the published JATS XML contain the entire per-patient numeric dataset**:

- **Table A1** — 60 patients × 9 genes of DGE values + DLP + effective dose. This is the qRT-PCR dataset, every cell.
- **Table A2** — 12 patients × pre-CT, post-CT, RIF γ-H2AX+53BP1 foci/cell + DLP + effective dose.
- **Table A3** — 60 patients × indication, anatomic region, conversion factor k, prior conditions.
- **Table 1** — patient demographics (n, mean ± SD, range).
- **Table 2** — group medians + p-values per gene for in-vivo vs ex-vivo and male vs female (no per-patient labels but provides group-level comparison values).

Extracted to TSV: `artifacts/ijms-26-11869-t0A1.tsv` (per-patient gene expression), `artifacts/ijms-26-11869-t0A2.tsv` (per-patient γ-H2AX foci), `artifacts/ijms-26-11869-t0A3.tsv` (scan metadata), `artifacts/ijms-26-11869-t001.tsv`, `artifacts/ijms-26-11869-t002.tsv`.

**Missing for full replication:** per-patient in-vivo vs ex-vivo *label*. Table A1 lists all 60 patients but does not annotate which incubation arm each belongs to. Group sizes are known (n=28/32 from §2.1 and abstract; n=27/33 from Table 2). The label can almost certainly be inferred by reconciling per-gene medians + signs in Table 2 against Table A1 subsets if one is willing to brute-force or solve as an assignment problem — see "Open questions" below. For first pass, we replicate the **all-patients combined** analyses, which the per-patient table fully supports.

## Replication classification

| Claim class | Reproducibility tier | First-pass status |
|---|---|---|
| Patient demographics (Table 1: n, age, DLP, dose) | **Tier 1** — fully reproducible from Tables A1+A3 | ✅ verified by smoke script |
| Combined (in-vivo + ex-vivo) median DGE and one-sample Wilcoxon p per gene (corresponds to §2.2 "When all samples were initially analyzed, combined…") | **Tier 1** — reproducible from Table A1 | ✅ smoke script reproduces direction + significance pattern for all 9 genes |
| In-vivo only median DGE & one-sample test per gene (§2.2, Figure 2) | **Tier 2** — needs in-vivo patient labels which are not in tables; inferable with subset-search | ⚠️ scoped, not yet executed |
| Ex-vivo only median DGE & one-sample test per gene | **Tier 2** — same caveat | ⚠️ scoped, not yet executed |
| In-vivo vs ex-vivo comparison (Table 2 left p-values) | **Tier 2** — requires labels (could be recovered by combinatorial fit) | ⚠️ scoped |
| Linear regression DLP vs DGE (Figure 3) — combined r² | **Tier 1** | ✅ smoke script computes per-gene OLS on full N=60 |
| Linear regression DLP vs DGE — *in vivo only* r² (e.g. AEN r²=0.66, FDXR r²=0.56) | **Tier 2** — requires labels | ⚠️ scoped |
| γ-H2AX RIF mean and post-vs-pre p-value (paired t / Wilcoxon, n=12, p=0.37 reported) | **Tier 1** — reproducible from Table A2 | ✅ smoke script reproduces means and paired test |
| Figure 1B-5 visual reproduction (jitter, regression, boxplot) | **Tier 1** — directly producible from Tables A1+A2 | scoped, not in first-pass |

Heavy compute: **not required**. Everything fits in numpy/scipy/pandas on CherryRd in seconds. No job plan needed.

## Folder layout

```
lucid100-low-dose-ct-gene-expression-dna-integrity/
├── README.md                       ← this file
├── PROGRESS.md                     ← run log
├── FIRST_PASS_REPORT.md            ← verdict + next steps
├── ARTIFACT_MANIFEST.tsv           ← provenance of every artifact
├── artifacts/
│   ├── europepmc.json              ← Europe PMC core metadata (1 record)
│   ├── europepmc_fullText.xml      ← canonical JATS body+references (CC BY)
│   ├── europepmc_PMC12732518.pdf   ← EuropePMC PDF render (3-page wrapper; MDPI gated)
│   ├── ijms-26-11869-t0A1.tsv      ← per-patient DGE (60 pat × 9 genes) + DLP + effDose
│   ├── ijms-26-11869-t0A2.tsv      ← per-patient γ-H2AX RIF (12 pat)
│   ├── ijms-26-11869-t0A3.tsv      ← per-patient scan metadata
│   ├── ijms-26-11869-t001.tsv      ← Table 1 demographics summary
│   └── ijms-26-11869-t002.tsv      ← Table 2 group medians + p-values
├── scripts/
│   └── replicate_smoke.py          ← Tier-1 reproduction of combined analyses + γ-H2AX
└── notes/
    └── claims.md                   ← bulletised claims with anchor refs
```

## How to run smoke

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-low-dose-ct-gene-expression-dna-integrity
python3 scripts/replicate_smoke.py
```

Uses only stdlib + numpy + scipy. Exits non-zero on failed assertion. Prints a per-gene comparison vs paper-reported values.

## Open questions / next-pass scope

1. **Recover per-patient incubation labels.** Table A1 + the published Table 2 medians (in vivo / ex vivo, per gene) form a constrained partition problem: pick a 27-or-28 subset of the 60 patients such that the in-vivo subset medians match all 9 gene values in Table 2 within rounding. Brute force is C(60,28) ≈ 4e16 — infeasible — but a constraint/LP relaxation or greedy fit per gene should converge quickly. Solving this would lift every Tier-2 claim to Tier-1.
2. **Per-figure digitization** of Figures 1–4 to cross-check the jitter and regression line parameters against our recomputed values.
3. **Pre-registration of biomarker panel** in a public CT-biodosimetry dataset (e.g., GSE43151 — Manning 2013 ex vivo whole-blood IR; GSE65292; CTBiodose project deposits) for external validation of the AEN/FDXR/PHLDA3/DDB2/EDA2R signature reported here.
4. **Power analysis** of the n=12 γ-H2AX subset to confirm the p=0.37 (i.e., is the study underpowered to detect a 0.1 RIF/cell shift, or genuinely null?). Trivial to compute.

## Compliance notes

- No author contact (per task rules).
- No paid endpoints used.
- All sources public, CC BY where applicable.
- All compute is light (msec on CherryRd); no GPU/job-plan required.
