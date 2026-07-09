# Workflow — Ghattargi et al. 2018 replication (BVBRC-16)

**Target paper:** Ghattargi VC et al. *BMC Genomics* 19:652 (2018), doi:10.1186/s12864-018-5043-9
**Strains:** 17OM39 candidate probiotic (BV-BRC `1352.1047`, GCF_001652715.1); T110 marketed probiotic (BV-BRC `1344042.3`, GCA_000737555.1)
**Verdict this pass:** PARTIAL (promoted from SPOT-CHECK 2026-06-17 → PARTIAL 2026-06-25)

## Pipeline (executed this pass)

```
[1] Bibliographic anchor
    └─ Europe PMC REST (paper metadata)
        → evidence/europepmc_ghattargi2018.json

[2] Genome metadata
    └─ BV-BRC /genome/?eq(genome_id,<GID>) for 1352.1047 + 1344042.3
        → evidence/bvbrc_17OM39_strain.json
        → evidence/bvbrc_T110_probiotic_strain.json
    └─ Confirm assembly status, length, contig count (C1, C2)

[3] Specialty-gene rescreen (AMR + VF)
    └─ BV-BRC /sp_gene/?eq(genome_id,<GID>)
              &select(genome_id,property,source,gene,product,evidence,classification)
              &limit(2000)
        → evidence/sp_gene_1352.1047.json      (158 rows, 56 AMR, 18 VF)
        → evidence/sp_gene_1344042.3.json      (148 rows, 52 AMR, 19 VF)
        → evidence/sp_gene_1344042.14.json     (T110 44 kb plasmid)
        → evidence/sp_gene_summary.json        (derived roll-up)
    └─ Filter property=="Antibiotic Resistance" → count van*/tet* → C3
    └─ Filter property=="Virulence Factor"    → note Cna presence in T110 → C4

[4] Full CDS feature dump
    └─ BV-BRC /genome_feature/?eq(genome_id,<GID>)&eq(feature_type,CDS)&limit(20000)
        → evidence/features_1352.1047.json     (5,776 CDS)
        → evidence/features_1344042.3.json     (5,173 CDS)
    └─ python3 regex scan of product names:
        transposase | mobile element | phage | integrase | recombinase |
        resolvase  | invertase       | prophage | insertion sequence |
        conjugal   | vancomycin/van* | tetracycline/tet* |
        bile salt hydrolase | bacteriocin/enterocin | sortase | LPxTG |
        adhesin | pilus | collagen-binding
        → evidence/feature_scan_summary.json

[5] Compare to paper claims
    └─ C1 metadata     ✅
    └─ C2 genome size  ✅
    └─ C3 no van/tet   ✅ (1 minor MFS-efflux caveat in 17OM39)
    └─ C4 no VF        ✅ (17OM39 cleaner than T110 — Cna in T110 only)
    └─ C5 fewer MGEs   ❌ opposite direction; confounded by draft vs finished
    └─ C6 phylogeny    ⬜ NOT RUN (needs Roary/PhyloPhlAn)

[6] Write REPORT.md → promoted verdict → PARTIAL
```

## Wall-clock + cost

| Step | Wall | CPU | Cost |
|---|---|---|---|
| Europe PMC pull | 2 s | negligible | free |
| BV-BRC sp_gene (2 genomes + 1 plasmid) | 4 s | negligible | free |
| BV-BRC feature dump (2 genomes) | 8 s | negligible | free |
| Local regex scans | 30 s | negligible | free |
| Report drafting | manual | — | — |
| **TOTAL COMPUTE** | **~5 min end-to-end** | **<0.01 CPU-h** | **$0** |

## What was NOT run (deliberately) and would cost to add

| Missing analysis | Tool | ~Cost | Which claim it closes |
|---|---|---|---|
| Core-genome phylogeny | prokka + roary + FastTree | ~6-8 CPU-h | C6 |
| Fair MGE count (contig-break-safe) | ISEScan on FASTA | ~2 CPU-h | C5 |
| DB-version-exact AMR + VF rescreen | abricate (resfinder, vfdb DBs) | ~10 CPU-min | confirms C3, C4 with paper's DB |
| Pathogenic comparator arm | pull Aus0004 / TX16 / DO from BV-BRC + repeat §3 pipeline | ~5 min | fair C5 baseline |
| Clade A vs B assignment | mlst + fastANI + Lebreton SNP panel | ~30 CPU-min | strengthens C6 |

**Total to promote to full REPLICATED:** ~10 CPU-h, all free, gated only by tool installation.

## Data-flow diagram (text form)

```
Europe PMC ──> paper metadata
                                  \
BV-BRC /genome ──> assembly stats  } ── analyzed ──> REPORT.md ──> PARTIAL verdict
BV-BRC /sp_gene ──> AMR+VF tables /           |
BV-BRC /genome_feature ──> CDS dumps ─────────┘
                        │
                        └── python3 regex ──> feature_scan_summary.json
```

## Reproducibility

Every raw curl blob is in `evidence/*.json`; every derived count in the report is one `jq` command away from the raw data. `evidence/feature_scan_summary.json` is the summary the numbers in §4.2, §4.4, §4.5 of REPORT.md were computed from. Re-running this pipeline requires only `curl`, `jq`, `python3` (+ `re` from stdlib). No paid APIs, no licensed DBs, no logged-in accounts.

## Standing rules honored

- **Free endpoints only.** Europe PMC and BV-BRC public API — no paid tokens used.
- **Single writer, resume-safe.** All fetches are idempotent GETs; re-running overwrites the same JSON blobs.
- **Do not fabricate numbers.** Every count in REPORT.md traces back to `evidence/*.json`.
- **Honest verdict.** PARTIAL, not REPLICATED — C5 disagrees and C6 wasn't run.
