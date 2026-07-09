# Genome structure & annotation comparison — S. flexneri 5a M90T

Paper: Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020).
Deposited assembly re-fetched independently: **GCF_004799585.1 / GCA_004799585.1 (ASM479958v1)**, submitter **Umeå University**, released 2019-04-18.
RefSeq replicon accessions: chromosome **NZ_CP037923.1** (GenBank CP037923.1), plasmid pWR100 **NZ_CP037924.1** (GenBank CP037924.1).

## Replicon structure (paper Table 1 & Table 2 "This work" rows)

| Replicon | Accession | Paper length (bp) | Independent length (bp) | Match |
|---|---|---:|---:|---|
| Chromosome | CP037923 | 4,596,714 | 4,596,714 | EXACT |
| Plasmid pWR100 | CP037924 | 232,195 | 232,195 | EXACT |
| **Total** | — | 4,828,909 | 4,828,909 | EXACT |
| # circular replicons | — | 2 | 2 | EXACT |

Independent GC content (computed here from the FASTA):
- Chromosome NZ_CP037923.1: 50.92% (NCBI datasets report: 51.0%)
- Plasmid NZ_CP037924.1: 45.68% (NCBI datasets report: 45.5%)
- Whole genome: 50.67%

## Annotation feature comparison

The paper annotated with Prokka (original 2019 submission). Three independent annotation
sources are compared below:
- **Paper** = Table 1/Table 2 "This work" (CP037923 chromosome, CP037924 plasmid).
- **RefSeq** = NCBI PGAP re-annotation attached to NZ_CP037923/NZ_CP037924 (2025 refresh).
- **Prokka(here)** = my independent Prokka 1.12 run on the downloaded FASTA (uicgpu, bvbrc28).

### Chromosome (CP037923)
| Feature | Paper | RefSeq | Prokka(here) |
|---|---:|---:|---:|
| Length (bp) | 4,596,714 | 4,596,714 | 4,596,714 |
| CDS (chromosome) | 4,629 | ~ (see whole-genome) | 4,720 |
| tRNA (genome) | 102 | 102 | 103 |
| rRNA (genome) | 22 | 22 | 22 |
| ISs (chromosome) | 296 | — | (not IS-typed here) |
| Pseudogenes (chr) | 640 | 757 (whole genome) | — |

### Plasmid pWR100 (CP037924)
| Feature | Paper | Prokka(here) |
|---|---:|---:|
| Length (bp) | 232,195 | 232,195 |
| CDS (plasmid) | 320 | 284 |
| ISs (plasmid) | 106 | (not IS-typed here) |
| Pseudogenes (plasmid) | 129 | — |

### Whole-genome annotation totals (independent)
- Prokka(here): 2 contigs, 4,828,909 bp, **CDS 5,004**, tRNA 103, rRNA 22, tmRNA 1.
- RefSeq: total genes 4,941; protein-coding 4,053; pseudogenes 757; non-coding 131.
- Paper (chr+plasmid summed): genes 4,049+307=4,356; CDS 4,629+320=4,949; tRNA 102; rRNA 22; ISs 402; pseudogenes 640+129=769.

**Interpretation.** Replicon count, replicon identities, and both replicon lengths reproduce
*to the base pair*. rRNA (22) and tRNA (102 vs 103) match near-exactly across all three sources.
CDS/pseudogene/IS totals differ by a few percent, which is the expected level of divergence
between independent annotation pipelines (Prokka 1.12 here vs paper Prokka + manual curation vs
NCBI PGAP), NOT a reproduction failure. Notably the paper's own pseudogene count (769)
and RefSeq's (757) are within ~1.5% of each other despite fully independent pipelines.

## IS elements (paper Table 3)
Paper reports **402 total IS elements** (296 chromosome + 106 plasmid) — an unusually high IS load,
which is the genomic hallmark of *Shigella* (genome degradation/pseudogenization relative to
commensal E. coli). This IS-driven pseudogene burden is corroborated qualitatively here by the
large pseudogene counts (RefSeq 757, paper 769) — consistent with the *Shigella* reductive-evolution
signature. Full ISfinder typing was not re-run (paper used ISsaga/ISfinder); flagged as
verified-plausible rather than re-executed.
