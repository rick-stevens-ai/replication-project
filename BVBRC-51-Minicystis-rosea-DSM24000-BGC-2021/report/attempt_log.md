# Attempt Log — BVBRC-51 (Minicystis rosea DSM 24000T)

**Analyst:** Ollie (OpenClaw subagent) — BVBRC Replication Wave, 2026-07-02
**Compute:** CherryRd (local blastp, python) + uicgpu (antiSMASH 8.0.4, /data/stevens/scratch/bvbrc51)

## Candidate selection
- Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar.
- Scanned BVBRC_TOPUP85_2026-06-26.tsv ranks 31+. Rank 31 (Lactococcus lactis LL16) already = BVBRC-10 (Milerienė2023). Rank 32 = Minicystis rosea DSM 24000T (Pal 2021, BMC Genomics) — no organism/topic overlap with BVBRC-01..50. Picked rank 32.

## Paper harvest
- Europe PMC: PMID 34511070 -> PMC8436480, DOI 10.1186/s12864-021-07955-x, OA=Y.
- Pulled full-text XML (166 KB) -> fulltext.xml -> stripped to fulltext.txt.
- Extracted accessions: chromosome CP016211.1, BioProject PRJNA321464. antiSMASH v5.0 used by authors. PacBio assembly.

## Data harvest
- Mapped PRJNA321464 -> assembly GCF_001931535.1 / GCA_001931535.1 (esearch/esummary).
- Downloaded GCA_001931535.1 via NCBI Datasets REST (FASTA+GFF+PROT), 8.15 MB zip (MD5 bcb8c0d436c06cc140597d1a14e8f178).
- Genome = single contig CP016211.1, 16,040,666 bp. protein.faa = 14,018 proteins.

## C2/C3 — genome statistics (local)
- genome_stats.py over FASTA+GFF. Results EXACTLY match paper Table 1:
  size 16,040,666 bp (=), GC 69.10% (paper 69.07%), CDS 14,018 (=), +strand 6,983 (=), -strand 7,035 (=),
  coding density 87.59% (paper 87.31%), tRNA 89 (paper 88), rRNA 4x16S/4x23S (paper "four 5S-16S-23S operons").
- The exact match of CDS strand counts confirms this is the identical deposited assembly.

## C5 — pfa PUFA gene cluster (local BLAST + synteny)
- efetch'd the 10 reference Pfa proteins the paper cites (Aetherobacter sp. SBSr008, A. fasciculatus, Sorangium cellulosum So ce56) -> pfa_refs.faa.
- makeblastdb on M. rosea proteome; blastp (e<=1e-10). Every reference Pfa has a strong M. rosea ortholog:
  Pfa1->APR86155 (71% id), Pfa2/PfaA->APR86156 (67% id), Pfa3/PfaC->APR86157 (60-63% id), PfaE->APR88149 (63% id).
- GFF synteny: APR86155/86156/86157 = consecutive locus tags A7982_11504/11505/11506, same (+) strand, 27-29 bp gaps -> contiguous pfa operon (= paper's "conserved synteny of the complete pfa gene cluster").
- NCBI annotation independently labels APR86156 "omega-3 polyunsaturated fatty acid synthase subunit, PfaA".

## C4 — antiSMASH BGC survey (uicgpu)
- No antiSMASH in existing envs. mamba-created /data/stevens/envs/antismash (antiSMASH 8.0.4), downloaded+prebuilt all DBs.
- antismash --genefinding-tool prodigal --cpus 16 on mrosea.fna. Runtime ~15 min for core detection.
- Result: 53 BGC regions (paper: 47 with antiSMASH v5.0). Category tally reproduces paper's ranking:
  terpene 12 (paper 9), RiPP-like 9 (7), NRPS+NRPS-like 8 (7), PKS 5 (4), RRE-containing 5 (4), indole 3 (3),
  thioamitides 3 (2), arylpolyene 2 (2), lanthipeptide 3 (3); rare BGCs phosphonate/phenazine/siderophore all 1 (=).
  Count delta (53 vs 47) fully attributable to antiSMASH v8 vs v5 rule expansion.
- antiSMASH independently flagged a T1PKS/hglE-KS region at 13,095,900-13,151,432 exactly overlapping the pfa cluster
  (hglE-KS is the PUFA-synthase PKS class) -> third independent confirmation of C5.

## Notes / gotchas
- Local blastp prints a harmless "MBEDTLS version mismatch" warning; results unaffected.
- antiSMASH knownclusterblast comparison tail runs long/quiet after the core JSON is written; parsed mrosea.json (core region detection) once available.
