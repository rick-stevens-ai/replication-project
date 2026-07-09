# Workflow — BVBRC-63 (Yasuike et al. 2017, *Nocardia seriolae* UTF1)

## Replication workflow (as executed)

1. **Claim extraction** — 10 claims (C1–C10) from the paper: genome length, GC, CDS count, rRNA operons, core orthologs, unique genes, mobile-element/unknown-fn/ABC enrichment, virulence orthologs.
2. **Assembly retrieval** — RefSeq GCF_002356035.1 (ASM235603v1; GenBank AP017900.1) from NCBI FTP. PacBio RS, 133x, SMRT Analysis 2.2.0 (paper's own deposit, BioProject PRJDB5277).
3. **Basic sequence stats** — Biopython `Bio.SeqIO` parse → chromosome count, length, GC.
4. **Independent re-annotation** — Prokka 1.12 (Prodigal 2.6.3, HMMER 3.4, aragorn, barrnap, minced) on uicgpu (8xA100, 32 threads), `--kingdom Bacteria --gcode 11`.
5. **Comparator retrieval** — RefSeq complete genomes for the 4 paper-named strains: N. farcinica IFM 10152 (GCF_000009805.1), N. brasiliensis HUJEG-1 (GCF_000250675.2), N. cyriacigeorgica GUH-2 (GCF_000284035.1), N. nova SH22a (GCF_000523235.1).
6. **Orthology / core-genome** — reciprocal-best-hit BLASTP (BLAST 2.5, e-value 1e-5, max_target_seqs 5), RBH filter pid>=25% / cov>=40%. Core = RBH in all 4 comparators; unique = RBH in none.
7. **Functional categories** — regex keyword counting (ABC transporter / mobile element / hypothetical / Mce / siderophore / beta-lactamase / efflux / catalase-SOD) across 5 RefSeq `.faa` description lines. Coarse direction-of-enrichment proxy.
8. **Verdict** — LLM judge (Argo `argo:claude-opus-4.7`, localhost:44497) given all 10 claims + results. No regex scoring of verdict.

## Tools / codes used

| Tool | Role | Cost |
|---|---|---|
| NCBI RefSeq FTP | Genome + comparator retrieval | Free |
| Biopython 1.87 | Sequence stats | Free |
| Prokka 1.12 (Prodigal/HMMER/barrnap) | Independent re-annotation | Free |
| BLAST+ 2.5 (blastp) | RBH orthology | Free |
| regex keyword counter | Functional-category proxy | Free |
| Argo `argo:claude-opus-4.7` | LLM-as-judge | Free |

## Compute footprint

- Host: uicgpu (8xA100, 32 CPU threads used for Prokka + BLAST)
- Prokka on 8.12 Mb genome: ~10-15 min
- RBH BLASTP UTF1 vs 4 comparators (both directions): ~20-40 min
- **Total effective effort: ~1.5-2 h** analyst + compute for the 10-claim replication.
- Extensions (COG enrichment Q1, threshold sweep Q2, mobile-element characterization Q3, expanded pan-genome Q5) each add materially more.
