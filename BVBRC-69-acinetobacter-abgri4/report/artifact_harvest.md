# Artifact Harvest — BVBRC-69

All pulled from **NCBI Nucleotide** via `efetch` (E-utilities, free, no auth) on 2026-07-03 UTC.

## Paper-deposited genomes (Chan et al. 2020, PMID 32681170)

| Strain    | Replicon       | Accession   | Length (bp) | GC%   | Description |
|-----------|----------------|-------------|------------:|-------|-------------|
| ABUH763   | chromosome     | CP035051.1  |   3,929,411 | 39.13 | chromosome, complete genome |
| ABUH763   | plasmid p74.1  | CP035052.1  |      74,091 | 33.67 | (repAci6, TnaphA6, blaOXA-23) |
| ABUH763   | plasmid p11.0  | CP035053.1  |      10,967 | 36.92 |             |
| ABUH773   | chromosome     | CP035049.1  |   3,873,900 | 39.06 | chromosome, complete genome |
| ABUH773   | plasmid p11.8  | CP035050.1  |      11,810 | 40.27 |             |
| ABUH793   | chromosome     | CP035045.1  |   3,915,869 | 39.13 | chromosome, complete genome |
| ABUH793   | plasmid p107   | CP035046.1  |     106,963 | 42.64 |             |
| ABUH793   | plasmid p74.1  | CP035047.1  |      74,091 | 33.67 | (identical to CP035052 in ABUH763) |
| ABUH793   | plasmid p10.9  | CP035048.1  |      10,945 | 36.91 |             |
| ABUH796   | chromosome     | CP035043.1  |   3,930,797 | 39.12 | chromosome, complete genome |
| ABUH796   | plasmid p13.0  | CP035044.1  |      12,952 | 36.67 |             |

Total pulled: **11 sequences, 12.0 Mb**. All are RefSeq/GenBank complete records
including full feature annotation (CDS + product + locus_tag).

## Comparator genomes (used for novel-target-site check)

| Strain     | Accession    | Length (bp) | Source note |
|------------|--------------|------------:|-------------|
| AB0057     | CP001182.2   |   4,050,513 | Paper cites AB0057 as ST2 comparator |
| ATCC 17978 | CP000521.1   |   3,976,747 | Canonical A. baumannii reference    |

## Databases used

- **abricate 1.4.0** (Torsten Seemann) with 2026-Apr-3 DBs: `resfinder` (3206 seqs), `card` (6052), `ncbi` AMRFinder (8232), `plasmidfinder` (488).
- **mlst 2.33.1** (Torsten Seemann) — Pasteur (`abaumannii_2`) and Oxford (`abaumannii`) MLST schemes.
- **blastn / makeblastdb / tblastn** (NCBI BLAST+, from bvbrc14 conda env).
- **Biopython 1.87** (installed 2026-07-03 into bvbrc14).

## Compute environment

- **uicgpu** (8×A100, 255 cores, 2 TB RAM); conda env `/data/stevens/envs/bvbrc14`.
- Working dir on uicgpu: `/data/stevens/bvbrc69-abgri4/`.
- Deliverables mirrored to Dropbox at `~/Dropbox/REPLICATE-PROJECT/BVBRC-69-acinetobacter-abgri4/`.
