# LUCID Slot 53 (Wave 6) — High-LET Carbon/Iron vs X-rays in PBMCs

**DOI:** 10.3389/fonc.2021.768493
**Journal:** Frontiers in Oncology, 2021, vol. 11
**Title:** *High-LET Carbon and Iron Ions Elicit a Prolonged and Amplified p53 Signaling and Inflammatory Response Compared to low-LET X-Rays in Human Peripheral Blood Mononuclear Cells*
**LUCID master row:** id 84, Wave 6, Block B, candidate_curated
**Replication class:** omics / signature replication

## Verdict at a glance

| Item | Status |
|---|---|
| Main PDF harvested | ✅ `artifacts/fonc-11-768493.pdf` (7.9 MB, 30 pp) |
| Raw microarray accessions | ✅ E-MTAB-3463 (X-ray, 60 CELs) + E-MTAB-5761 (heavy ions, 16 CELs) |
| Both accessions live & open | ✅ verified HTTP 200 from EBI FTP |
| Sample sheets (SDRF + IDF) | ✅ `data/E-MTAB-{3463,5761}.{sdrf,idf}.txt` |
| All 76 CEL URLs enumerated | ✅ `data/cel_urls.txt` |
| Sample CELs downloaded + parsed | ✅ 6 of 76 in `data/cel_subset/`, all confirmed HuGene-1_0-st-v1 |
| Smoke script | ✅ `scripts/cel_header_sniff.py` (Python-only, no Bioconductor) |
| Smoke result | ✅ PASS — `artifacts/cel_sniff_output.txt` |
| Full RMA + limma run plan | ✅ `scripts/RUN_PLAN.md` (target: uicgpu, ~10 min wall) |
| Replication feasibility | ✅ **GO** |
| QA recommendation | 🔁 **RETAG B → A** (replication-ready) |

## What the paper does

Compares the transcriptional response of isolated human PBMCs (healthy donors)
8 h after exposure to 1 Gy of:

- **X-rays** (Pantak HF420 RX, 250 kV @ SCK-CEN; also 0.1 Gy)
- **Carbon ions** (~60–80 keV/µm in middle of SOBP @ GSI SIS)
- **Iron ions** (155 keV/µm, 1 GeV/n monoenergetic @ GSI SIS)

Platform: Affymetrix GeneChip Human Gene 1.0 ST (28,536 transcript clusters).
Validation: qRT-PCR at 24 h on PCNA, GADD45A, RPS27L, ASTN2, NDUFAF6, FDXR, MAMDC4;
γH2AX foci for residual damage; RRHO + Enrichr for signature/TF/GO comparison.

Main finding: all DE genes (any radiation type) are *up-regulated* and dominated
by **p53 targets**; heavy ions show **prolonged amplitude** (qPCR at 24 h) plus
*radiation-type-specific* enrichment of **immune/inflammatory** processes; carbon
in particular drives **transcript variant** changes (alt splicing); one donor
in the iron arm shows a distinct DNA-repair profile.

## What this folder contains

```
lucid100-highlet-pbmc-p53-inflammation/
├── README.md                ← this file
├── PROGRESS.md              ← turn-by-turn status log
├── MANIFEST.json            ← machine-readable artifact + accession manifest
├── FIRST_PASS_REPORT.md     ← scoping report + verdict
├── artifacts/
│   ├── fonc-11-768493.pdf   ← main paper, full text
│   └── cel_sniff_output.txt ← smoke-test stdout (6 CELs sniffed, all HuGene 1.0 ST)
├── data/
│   ├── E-MTAB-3463.{sdrf,idf}.txt   ← X-ray experiment sample sheet + investigation
│   ├── E-MTAB-5761.{sdrf,idf}.txt   ← heavy-ion experiment sample sheet + investigation
│   ├── cel_urls.txt                 ← 76 ready-to-download CEL URLs
│   └── cel_subset/                  ← 6 representative CELs (1 per condition)
└── scripts/
    ├── cel_header_sniff.py          ← minimal Python smoke (CEL header validator)
    └── RUN_PLAN.md                  ← full-replication recipe (R + Bioconductor on uicgpu)
```

## Reproduce the smoke test

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-highlet-pbmc-p53-inflammation
python3 scripts/cel_header_sniff.py data/cel_subset/*.CEL
# Expect: 'OK: all 6 CELs share array_type=HuGene-1_0-st-v1'
```

## Reproduce the full replication

See `scripts/RUN_PLAN.md`. Short version:

```bash
ssh uicgpu
mkdir -p /data/stevens/scratch/lucid53/cels
xargs -n1 -P4 -I{} bash -c 'curl -sSL -o cels/$(basename {}) {}' < cel_urls.txt
Rscript -e 'source("rma_limma_pipeline.R")'  # see RUN_PLAN.md for the recipe body
```

## Compute policy

- **Heavy compute (RMA on 76 CELs + limma + RRHO) belongs on uicgpu**, not CherryRd.
- This folder contains only the artifact harvest + a Python-only smoke test
  (CEL header sniff). No heavy lifting was done on CherryRd, per task rules.
- Full job plan is in `scripts/RUN_PLAN.md`; estimated wall time on uicgpu is
  under 15 minutes.
