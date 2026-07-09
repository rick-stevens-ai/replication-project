# lucid100-rprm-egfr-hsc-irradiation

LUCID100 replication scoping, Wave 2 max-rate backfill (master row 49, slot 17 — see slot-mismatch note).

## Paper

- **Title:** RPRM deletion preserves hematopoietic regeneration by promoting EGFR-dependent DNA repair and hematopoietic stem cell proliferation post ionizing radiation
- **Authors:** Z. Li, Z. Zhou, S. Tian, K. Zhang, G. An, Y. Zhang, R. Ma, B. Sheng, T. Wang, H. Yang, L. Yang
  - Corresponding: Hongying Yang (yanghongying@suda.edu.cn), Lin Yang (yanglin@suda.edu.cn)
  - Affiliation: State Key Laboratory of Radiation Medicine and Protection, Soochow University, Suzhou, China
- **Journal:** *Cell Biology International* 46(12):2158–2172 (2022)
- **DOI:** [10.1002/cbin.11900](https://doi.org/10.1002/cbin.11900)
- **PubMed / PMC:** PMID 36041213 / PMC9804513
- **License:** CC BY-NC-ND 4.0 (open access)

## Master labeling and slot mismatch

| Field | Master TSV says | Reality from paper |
| ----- | --------------- | ------------------ |
| Wave  | Wave 2 | OK |
| Slot  | **17** (task asked for slot **18**) | n/a — see note |
| Approach | "simulation/model replication" | **wet-lab in vivo mouse study + RNA-seq + qPCR / flow / Western** — *no model or simulation in this paper* |
| Topic | DNA repair / DDR; radiation quality / RBE; computational model / simulation | DNA repair / DDR ✅, hematopoietic radiation injury ✅; *no RBE, no model* |

**Slot note:** the source-of-truth TSV (`LUCID100_SOLID_MASTER_QA.tsv`) lists this DOI at **row 49 / slot 17**, not slot 18 as the task descriptor said. I treated slot 17 as canonical (the DOI in the task matches that row uniquely). No other Wave-2 row in master matched.

**QA retag recommendation:** see `FIRST_PASS_REPORT.md` and the JSON progress record. Reclassify `approach` from `simulation/model replication` to `experimental / in-vivo + bulk RNA-seq` (or whatever the project's preferred wet-lab tag is). The "computational model / simulation" tag should be removed from topic.

## Directory layout

```
.
├── README.md                    # this file
├── PROGRESS.md                  # turn-by-turn progress log
├── FIRST_PASS_REPORT.md         # scoping verdict + claim matrix + replication plan
├── MANIFEST.json                # artifact inventory
├── code/
│   └── smoke_check.py           # tiny sanity script: reproduces paper-stated qPCR primer set + checks data deposit URLs
├── figures/                     # (empty — populated by smoke if applicable)
├── results/
│   └── smoke_output.json        # written by smoke_check.py
├── logs/
└── source/
    ├── cbin.11900.pdf           # full paper (via Europe PMC OA render)
    ├── cbin.11900.txt           # pdftotext extraction
    ├── cbin.11900.xml           # JATS XML from Europe PMC fullTextXML
    ├── crossref.json            # Crossref metadata
    ├── epmc.json                # Europe PMC search record
    ├── geo_search.json          # NCBI GEO esearch (returned 0 hits — see report)
    ├── figures/                 # 6 JPEGs extracted from PDF (figures 1–5 + abstract image)
    └── supplementary/           # EMPTY — see Blockers below
```

## Quick start

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-rprm-egfr-hsc-irradiation
python3 code/smoke_check.py
cat results/smoke_output.json
```

The smoke script is a **scoping smoke**, not a computational replication: this paper has no model or code to re-run. The smoke (a) inventories what we successfully harvested, (b) parses the qPCR primer table from the JATS XML and re-asserts the primer set the paper used, and (c) probes the three deposit endpoints (Wiley supp, PMC supp, NCBI GEO for the BGI-commissioned RNA-seq) and records the access verdict.

## Replication verdict (one-liner)

> **Not a model paper.** Pure wet-lab in vivo mouse study (RPRM⁻/⁻ vs WT C57BL/6 ± 4–6 Gy X-rays, ± erlotinib, ± NU7441) with bulk RNA-seq of sorted LSK cells (n=3/group, BGI). **No deposited transcriptomic data**, no code, no model. Data-availability statement is "available from the corresponding author upon reasonable request." Author contact is disallowed by task scope. **Independent quantitative replication is not feasible from public artifacts.** Qualitative claims about EGFR / STAT3 / DNA-PKcs / Lin28a pathway are well-anchored in prior literature (Fang 2020, Javvadi 2012, Yuan 2012/2013) and could in principle be cross-checked against public HSC RNA-seq datasets, but that would be a *new* meta-analysis, not a replication.

See `FIRST_PASS_REPORT.md` for the full claim matrix and what *would* be needed for a true replication.

## Blockers

1. **No accession for the BGI-commissioned RNA-seq** (LSK cells, n=3/group, 1 h post 4 Gy). NCBI GEO `esearch` for "RPRM hematopoietic" returns 0 hits. Without raw counts or the DEG table, Figure 4a (KEGG inflammatory-cytokine enrichment) cannot be reproduced.
2. **Supplementary files (S1–S6) are unfetchable via free routes** at the time of this run:
   - Wiley `downloadSupplement` → 403 (anti-bot challenge)
   - Europe PMC `/articles/PMC9804513/bin/CBIN-46-2158-s00N.*` → 301 to `ptpmcrender.fcgi`, which then returns empty HTTP/2 streams (also empty over HTTP/1.1)
   - `pmc.ncbi.nlm.nih.gov/articles/PMC9804513/bin/...` → 404 (file paths exist in JATS but PMC has not re-rendered them)
   - PMC OA tarball listed by `oa.fcgi` at `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/b5/97/PMC9804513.tar.gz` → 550 (FTP) / 404 (HTTPS mirror)
   These files would contain S1–S5 (sex-matched control panels, female-mouse parallel figures, replicate counts) and one DOCX (likely the methods extension or RNA-seq differential table — name not visible without fetch). Task forbids paid endpoints, so an institutional Wiley click-through is the next step but is out-of-scope here.
3. **No code, no protocols beyond the M&M section.** All quantification (γ-H2AX, p-DNA-PKcs, p-EGFR, p-STAT3) is image-based confocal + flow cytometry analyzed in GraphPad Prism 6.01 — no raw images, no FCS files.

## Next actions

1. **(Triage)** Update `LUCID100_SOLID_MASTER_QA.tsv` row 49 to retag approach as wet-lab/experimental; remove "computational model / simulation" from topic. Add `friction_tags: [no-deposit, no-code, supp-blocked, paywall-supplement, in-vivo-only]`.
2. **(If escalated)** Try Wiley supp download via a logged-in OpenAthens/Shibboleth route at Argonne; or contact authors (out-of-scope per task).
3. **(Lateral artifact opportunity)** Look at Zhang et al. 2021 (the same group's predecessor paper this work cites for the RPRM-KO model) — if *that* paper deposited transcriptomic data, those data plus this paper's qPCR primer set could anchor a partial cross-check of RPRM induction kinetics. Out of scope for this slot.
4. **(Cross-paper synergy)** The EGFR-DNA-PKcs feedback loop and EGFR→DNA repair in HSCs are also claimed in Fang et al. 2020 (Theranostics, 10.7150/thno.60143) — that paper is more likely to have deposited data and could serve as the *modelable* anchor for an EGFR-HSC-repair replication. Flag for a separate LUCID slot if not already covered.
