# BVBRC-16 — Artifact Harvest

## Bibliographic / OA
- Europe PMC core JSON: `evidence/europepmc_ghattargi2018.json` (isOpenAccess=Y, PMC6122445).
- License: BMC open access (CC BY 4.0).

## Strain / genome metadata (BV-BRC)
- **17OM39 — exact strain match in BV-BRC**:
  - `genome_id` 1352.1047, **GCF_001652715.1**, 106 contigs, **2,840,201 bp**, BioProject **PRJNA318315**, BioSample **SAMN04784847** (WGS).
  - File: `evidence/bvbrc_17OM39_strain.json`.
- **T110 (marketed probiotic comparator)**:
  - `genome_id` 1344042.3, **GCA_000737555.1**, **Complete**, **2,737,963 bp**.
  - Associated plasmid: `genome_id` 1344042.14, 44,086 bp.
  - File: `evidence/bvbrc_T110_probiotic_strain.json`.
- Existing probe files from prior subagent runs: `bvbrc_keyword_probe.txt`, `bvbrc_strain_probe.txt`, `bvbrc_strain_probe2.txt` (kept for traceability).

## Sequencing source
- Raw + assembled data accessible via NCBI BioProject **PRJNA318315** (17OM39).

## Tool stack from the paper (for context, not run here)
- Assembly: SPAdes; Annotation: RAST/PATRIC.
- Pan-genome / core-genome: Roary or PGAP-style approach.
- AMR screen: CARD, ResFinder.
- Virulence: VFDB.
- Phylogeny: PhyloPhlAn / FastTree / RAxML.
