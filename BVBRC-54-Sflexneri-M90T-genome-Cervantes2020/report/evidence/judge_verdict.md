## Claims table

| ID | Claim | Type | Tested? | Agreement verdict |
|---|---|---|---|---|
| C1 | Complete, gapless genome with exactly 2 circular replicons (chromosome + pWR100) | Assembly structure | Yes (downloaded assembly + replicon check) | **Reproduced-exactly** |
| C2 | Chromosome 4,596,714 bp; plasmid 232,195 bp | Assembly metrics | Yes (independent FASTA parse) | **Reproduced-exactly** |
| C3 | Built from PacBio SMRT (Canu 1.7, ~157×) and polished with Illumina RNA-seq | Methods/provenance | No (no re-assembly from raw reads) | **Not-tested** |
| C4 | Annotation feature counts (CDS/tRNA/rRNA/IS/pseudogenes; high IS load) | Annotation content | Partly (Prokka + PGAP compared; IS not re-typed) | **Reproduced** (partial/approximate; IS count not directly verified) |
| C5 | pWR100 encodes T3SS essential for invasion | Functional gene content | Yes (VF/AMR scans locating full T3SS on plasmid) | **Reproduced** |
| C6 | dRNA-seq TSS counts: 6723 primary, 7328 secondary | Transcriptomics result | No (dRNA-seq not re-run) | **Not-tested** |
| C7 | Genome+annotation publicly deposited and usable | Availability/usability | Yes (NCBI download + RefSeq annotation) | **Verified-availability-only** |

## Overall coverage
Tested (fully or partially): **5/7 claims = 71%**.

## Overall agreement assessment
All tested claims agree with the paper, with exact matches for the core assembly structure and replicon lengths (C1–C2). Annotation-level agreement is broadly consistent across independent pipelines, but the specific IS-element count was not directly reproduced (C4). Key transcriptomics (TSS counts) and the end-to-end assembly/polishing workflow from raw reads were not independently replicated (C3, C6).

## FINAL VERDICT: **PARTIAL**
The replication independently confirms the deposited “complete genome” structure (two circular replicons) and exact chromosome/plasmid lengths, and it corroborates that the virulence plasmid carries a complete T3SS gene set. Annotation statistics are broadly consistent but not fully revalidated for IS elements. However, the study’s raw-read assembly strategy and the dRNA-seq TSS quantifications were not re-executed, leaving major methodological and transcriptomic claims untested.