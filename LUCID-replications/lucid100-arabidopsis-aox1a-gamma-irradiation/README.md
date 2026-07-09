# LUCID100 slot 40 — Arabidopsis AOX1a × γ-irradiation (Belykh 2022)

**Paper.** Belykh ES, Velegzhaninov IO, Garmash EV (2022). *Responses of genes
of DNA repair, alternative oxidase, and pro-/antioxidant state in Arabidopsis
thaliana with altered expression of AOX1a to gamma irradiation.*
**Int J Radiat Biol** 98(1):60–68.
DOI [`10.1080/09553002.2022.1998712`](https://doi.org/10.1080/09553002.2022.1998712),
PMID `34714725`.
Institute of Biology, Komi Scientific Centre, Ural Branch RAS, Syktyvkar.

**LUCID100 row.** rank 71 / Wave 4 backfill slot 40, tier A, priority 14,
worktype = *omics/signature replication*.

## Bottom-line verdict

**FIRST-PASS NO-GO for quantitative replication; partial-GO for lateral
directional cross-validation.**

| Axis | Status |
|---|---|
| Open-access paper PDF | ❌ closed (Taylor & Francis) |
| Author qPCR Cq table / supplementary | ❌ not deposited; supplement paywalled |
| Raw RNA-seq / microarray | ❌ none — paper is qPCR + biochemistry only |
| GEO/SRA/ArrayExpress/BioStudies accession | ❌ none; abstract gives no accession |
| Three Arabidopsis genotypes (Col-0 / AS-12 / XX-2) | ⚠️ AS-12 + XX-2 are lab-specific Komi/Syktyvkar lines, not commercially distributed |
| 200 Gy γ-source | ⚠️ requires institutional high-dose-rate ⁶⁰Co/¹³⁷Cs facility |
| Author contact | ⛔ disallowed by task scope |
| Lateral cross-validation from public data | ✅ feasible — see `code/smoke_check.py` |

The paper is a wet-lab qPCR + enzymatic-activity study; there is no
computational artifact to replicate quantitatively, and the experimental
artifact requires custom AOX1a-altered Arabidopsis lines plus a 200 Gy
γ-source. **Recommend QA retag from "omics/signature replication" →
"wet-lab qPCR + biochemistry / no public deposit"; keep in corpus as a
mechanistic anchor for the AOX-mitochondrial-retrograde / DDR axis.**

## What we did instead — lateral cross-validation

The paper makes one strong directional claim that *is* publicly testable:
**γ-irradiation upregulates DNA-repair genes in wild-type Arabidopsis**
(and that response is partially decoupled in AOX1a-overexpressing XX-2
plants). We tested this claim against an independent public scaffold.

**Scaffold dataset.** GSE112773 = the SuperSeries of Bourbousse et al.
*Genome Res* 2018 (PMID 30060114) — the SOG1 + MYB3R DREM time-course
of γ-IR in WT vs *sog1* Arabidopsis seedlings. We pulled
`GSE112773_Source_Data_2.tar.gz` and used the
`Princeton_GO_inputs_GeneListsByPath/W*.txt` and `S*.txt` AGI gene
lists (one per DREM dynamic-response path).

**Panel.** 27 AGI loci reconstructed from the Belykh abstract: 5 AOX
family members, 14 DDR genes (ATM/ATR/SOG1 + HR + NHEJ + BER + cell-cycle
checkpoint), 8 antioxidant enzymes. AGI assignments are TAIR-authoritative
and listed inline in `code/smoke_check.py`.

**Result** (one-liner):
- **5/5 (100%)** of the canonical HR/BER DSB-response panel genes
  *detected* in the GSE112773 DREM scaffold land in WT-γ-IR-induced
  paths (RAD51→W2, RAD54→W3, BRCA1→W1, PARP1→W1, PARP2→W3).
- **7/14 (50%)** of the full DDR panel are detected at all (others
  fall below the Bourbousse DREM-significance threshold).
- **2/7 detected DDR genes are discordant** (WT-repressed instead of
  induced): APE1L (W4) and WEE1 (W4). WEE1 in particular is a
  *checkpoint* gene whose repression dynamics post-γ-IR are model-dependent.
- **AOX1a (AT3G22370) lands in WT-repressed W4 and sog1 S2** in the
  Bourbousse scaffold — a *partial contradiction* of the Belykh
  qualitative claim that WT γ-IR upregulates AOX1a. Worth flagging
  for a downstream meta-analysis; time-courses differ (12 h post-200 Gy
  in Belykh vs Bourbousse 0–24 h post-100 Gy on seedlings, not 5 wk
  plants), and the *sog1* hit means the response is SOG1-dependent.
- **AOX1c (AT3G27620) lands in WT-induced W7** — consistent with the
  AOX-family stress-induction model.

Verdict: **the directional claim "γ-IR induces DDR genes in WT
Arabidopsis" is robustly reproduced from independent public data**;
**the specific claim about AOX1a being a primary γ-IR target is not
supported by the Bourbousse scaffold**, which actually shows AOX1a in
the WT-repressed (early-late) dynamics path and is SOG1-dependent.
That second finding is the interesting lateral artifact this slot
produced.

## Folder layout

```
lucid100-arabidopsis-aox1a-gamma-irradiation/
├── README.md                ← this file
├── PROGRESS.md              ← timestamped activity log
├── FIRST_PASS_REPORT.md     ← detailed verdict + evidence + qa retag
├── MANIFEST.json            ← artifact manifest (paths, sizes, sha256)
├── code/
│   └── smoke_check.py       ← pure-stdlib panel-vs-DREM-paths cross-validation
├── results/
│   └── smoke_output.json    ← machine-readable per-gene + summary
├── source/
│   ├── crossref.json
│   ├── unpaywall.json
│   ├── epmc.json
│   ├── pubmed.txt
│   ├── abstract.txt
│   ├── semanticscholar.json
│   ├── GSE112773_Source_Data_2.tar.gz   ← scaffold (8.6 MB)
│   ├── GSE112773_Source_Data_file_descriptions.txt
│   ├── GSE112773_SD2/                   ← extracted per-DREM-path AGI lists
│   ├── GSE112529_summary.json
│   ├── GSE_SOG1_search.json
│   ├── GSE_AOX1a_top.json
│   ├── geo_arabidopsis_ddr_summary.json
│   ├── biostudies_search.json
│   └── biostudies_search_aox1a.json
└── notes/                   ← (empty; reserved)
```

## How to re-run

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-arabidopsis-aox1a-gamma-irradiation
python3 code/smoke_check.py
```

Runtime: ~50 ms; pure stdlib; no GPU; no install; no network; CPU-only on
CherryRd. **No heavy-compute job plan needed.**

## Key references for any follow-up

- Bourbousse C et al. 2018 *Genome Res* 28:1264–1275 — GSE112773 scaffold.
- Yoshiyama K et al. 2009 *PNAS* 106:12843 — SOG1 master DDR TF.
- Culligan KM et al. 2006 *Plant J* 48:947 — ATM substrate transcriptome.
- Missirian V et al. 2014 *BMC Plant Biol* 14:135 — IR-induced transposon
  silencing.
- Vanlerberghe GC 2013 *Int J Mol Sci* 14:6805 — AOX in plant stress.
- Umbach AL et al. 2005 *Plant Physiol* 139:1806 — the original AOX1a
  AS / XX construct ancestry that Belykh's AS-12 / XX-2 lines descend from.
