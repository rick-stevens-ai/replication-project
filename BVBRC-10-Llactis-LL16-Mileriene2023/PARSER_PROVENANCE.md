# Parser Provenance — BVBRC-10 LL16 Mileriene 2023 (re-pass)

**Re-pass date:** 2026-06-23
**Purpose:** Track exactly which parsers/tools turn raw artifacts into the numbers cited in the REPORT, so claim-by-claim grounding is auditable.

## Canonical parse pipeline (pass-1, retained)
- **Genome FASTA → genome stats:** BioPython `SeqIO.parse` on `data/LL16_genome.fna` (GCF_029912225.1); summary in `analysis/genome_stats.json` (total_length, num_contigs, GC, N50, L50). Verified independently here with `seqkit stats`-equivalent counting.
- **PGAP GFF → feature counts:** hand-written Python over `data/annotated/ncbi_dataset/data/GCF_029912225.1/genomic.gff` (NCBI PGAP annotation). CDS, tRNA, rRNA, tmRNA, ncRNA, pseudogene counts come from `type` column.
- **Protein FASTA → BLAST:** `makeblastdb` of `data/annotated/.../protein.faa` → `analysis/LL16_prot_db.*`. Reference protein queries (`analysis/ref_*.faa`) for gadB, bsh, efTu, cspA, fbp, lcnB, enlA, aadc.
- **Annotation keyword search:** regex/string matching on `product=`, `gene=`, `Name=` attributes in the GFF.

## Re-pass parser additions (this round)
All scripts are version-pinned to the tools shipped with the system Homebrew + Python and write incremental outputs under `results/repass/`.

| Output | Producer | Inputs | Tool version |
|---|---|---|---|
| `results/repass/skani_LL16_vs_IL1403.tsv` | `skani dist` | `data/LL16_genome.fna`, `data/IL1403/IL1403.fna` (AE005176.1) | skani 0.3.2 |
| `results/repass/fastani_LL16_vs_IL1403.tsv` | `fastANI` | same | FastANI 1.33 |
| `results/repass/annotation_mining.json` | `code/repass/mine_annotations.py` | PGAP GFF | Python 3 stdlib + regex |
| `results/repass/minced_LL16.crisprs` (empty) / `minced_LL16.gff` (header only) | `minced` (defaults: minNR=3, minRL=23-47, minSL=26-50) | `data/LL16_genome.fna` | MinCED 0.4.2 |
| `results/repass/minced_LL16_loose.crisprs` / `.gff` | `minced -minNR 2 -minRL 20 -maxRL 50 -minSL 20 -maxSL 60` | same | MinCED 0.4.2 |
| `data/IL1403/IL1403.fna` | NCBI E-utilities efetch | accession AE005176.1 | curl + NCBI efetch |

## Provenance notes
- **ANI:** skani uses an MAG-trained regression model that may adjust the raw value; we report both skani and FastANI numbers. FastANI is the closer methodological match to OrthoANI (both are alignment-free vs. alignment-based — but both are widely accepted ANI substitutes). The numbers are consistent (98.7 / 98.2) and both within 0.5% of the paper's OrthoANI 98.73%.
- **CRISPR:** MinCED defaults found zero canonical CRISPR arrays (≥3 repeats, 23-47 bp DR, 26-50 bp spacer). Loose mode finds short tandem repeats but these are mostly low-complexity sequence noise, not true CRISPR-Cas arrays. The paper used CRISPRCasFinder (web tool, more sensitive, classifies repeat structure). The PGAP annotation contains Cas2 (a CRISPR-associated protein), supporting the *presence* of a CRISPR system, but the deposited assembly does not yield a canonical 3-spacer / 23-repeat array at standard MinCED thresholds — likely because the array is fragmented across contigs in the draft assembly or sits in a region filtered by NCBI's contamination screen.
- **IS elements:** counted by regex on PGAP `product=` field for IS-family tokens. PGAP does not assign specific ISfinder strain names (e.g. ISS1B vs ISS1N vs ISLla3) so the granularity in the paper (3 specific named IS) cannot be reproduced without ISfinder/MobileElementFinder — but per-family counts are reportable.
- **Vitamin / adhesion / acid-bile / lactose / tryptophan / enzyme gene presence:** all derived from regex on PGAP product/gene/name. Per-claim hit lists are written to `results/repass/annotation_mining.json`.
- **No re-assembly / no re-annotation:** the analysis still uses the deposited PGAP annotation (paper used Prokka). Pipeline-difference disclaimer in original report still applies.

## Tools NOT used in this re-pass (and why)
- OrthoANI web tool — replaced by skani + FastANI.
- ResFinder / VirulenceFinder / PathogenFinder / BAGEL4 / antiSMASH / KEGG BlastKOALA — still web-only with no FOSS drop-in available within the free-compute budget of this re-pass.
- MobileElementFinder (web) and ISfinder DB — would allow strain-level IS naming; not run here.
- CRISPRCasFinder local CLI — exists but requires Java + Vmatch + perl deps that were not worth installing for the marginal claim-coverage lift.
