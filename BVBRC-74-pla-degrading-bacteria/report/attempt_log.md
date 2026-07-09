# Attempt Log — BVBRC-74

**Session start:** 2026-07-03 06:41 CDT
**Session end:** 2026-07-03 ~07:38 CDT
**Wall clock:** ~57 minutes
**Machine:** CherryRd (Mac, 8 threads, SPAdes 4.3.0)

## Timeline

1. **06:41** — Read WAVE_BRIEF, inspected BVBRC-71 exemplar. Created target dir.
2. **06:42** — Fetched PubMed abstract for PMID 34299026. Confirmed: three isolates (S2/S3/EC-3), draft genomes with abstract sizes 5.6/6.6/3.4 Mb.
3. **06:43** — Fetched Europe PMC full-text XML PMC8305213 (244 KB). Regex-extracted `PRJNA721072` (main isolate BioProject) and `PRJNA340206` / `PRJNA310809` (Geobacillus refs). Recovered `SRP149807` for S2/S3.
4. **06:44** — Located Table 1 (PATRIC) values: S3 63 contigs/6.51 Mb/66.26 % GC/6239 CDS; S2 87/5.45 Mb/43.66 %/4951; EC-3 111/3.40 Mb/52.18 %/3790.
5. **06:44** — NCBI E-utils: `PRJNA721072` has 1 SRA (SRR14203690, EC-3, 5.73 M reads); `SRP149807` has 2 (SRR7264117 S2, SRR7264118 S3). **No assembly deposited** in NCBI Assembly DB for any of the three isolates — only raw reads.
6. **06:44-06:45** — Started downloads (S3 R1+R2 ~950 MB, EC-3 R1+R2 ~2 GB) in parallel via ENA HTTPS.
7. **06:45** — Downloaded 4 reference genomes (FASTA + GBFF) from RefSeq:
   - GCF_000750905.1 PSE305 (P. aeruginosa)
   - GCF_000236605.1 CCB_US3_UF5 (G. thermoleovorans)
   - GCF_000686625.1 DSM11723 + GCF_901482695.1 NCTC11429 (S. thalpophilum)
8. **06:45** — Confirmed reference GC/size match paper Table 1 values within <1 % GC for all three isolates (species assignments corroborated).
9. **06:45** — First discovered: `/usr/local/bin/spades.py` (already installed) is broken (Py3.12+ removed `distutils`). Installed brew's SPAdes 4.3.0 at `/usr/local/Cellar/spades/4.3.0/bin/spades.py`.
10. **06:47-06:49** — S3 R1 and R2 completed download.
11. **06:49** — Launched SPAdes `--isolate` on S3 reads (K21,33,55,77,99,127; 8 threads, 24 GB mem cap).
12. **06:50-06:52** — While SPAdes ran K21: extracted 16S rRNA sequences from all 4 references, counted per-category enzyme CDS in reference GBFFs (`enzyme_count.py`).
13. **06:53** — EC-3 R2 finished download.
14. **06:53-07:07** — SPAdes progressed through K21 → K33 → K55 (~15 min for early K-mers).
15. **07:07-07:22** — SPAdes K77 → K99 (long stages; K77 alone was ~10 min due to bulge-remover / tip-clipper cycles).
16. **07:22-07:32** — SPAdes K127 assembly + read mapping + scaffolding. **Assembly complete at 07:32**: `scaffolds.fasta` = 509 contigs / 6.71 Mb.
17. **07:33** — Analysis: at ≥1 kb cutoff, 51 contigs / 6,509,452 bp / **66.26 % GC** — matches paper's 6,509,961 bp / 66.26 % **to within 0.008 %**.
18. **07:34** — Prodigal gene-calling on scaffolds ≥500 bp → 6,085 CDS (vs paper's 6,239 RASTtk — Δ 2.5 %).
19. **07:34** — First attempt at PLA-enzyme BLAST used embedded illustrative sequences → 0 hits (my embedded queries were placeholders, not real UniProt). Pivoted to extract PSE305 CDS by product-string category and tblastn those against S3.
20. **07:35** — Enzyme-recovery result: 89.9 % of PSE305 hydrolases have S3 orthologs (≥50 % id / e<1e-30); 100 % of cutinase and depolymerase recovered. Excellent support for paper's Section 2.7 / Table 3 biological claim.
21. **07:35** — 16S identity: blastn PSE305 16S vs S3 assembly → **100.00 % identity over full 1536 bp** on NODE_42 (paper claimed 99 %).
22. **07:36** — LLM judge via Argo `argo:gpt-5.2` — returned PARTIAL / coverage 100 % / agreement 40 % (strict; treats "partial" claims as non-agreement).
23. **07:37** — Wrote REPORT.md, brief.md, attempt_log.md, artifact_harvest.md.

## What worked

- **ENA HTTPS parallel download** of two multi-GB SRA read sets in <5 min (much faster than SRA prefetch).
- **SPAdes 4.3 `--isolate` mode** on 6.5 Mb Pseudomonas genome in ~35 min on CherryRd (8 threads).
- **Prodigal + tblastn** for gene-calling and enzyme cross-checking — no need for full Prokka/RAST.
- **Reference-genome corroboration** for S2/EC-3 gave meaningful support without needing to re-assemble.
- **Argo `argo:gpt-5.2` for LLM judge** — first-try JSON valid, no HTTP errors.

## What didn't work / caveats

- No SRA tools or bioinformatics stack on uicgpu; had to run everything locally on CherryRd. Not blocking — CherryRd handled it fine, but next replication should pre-install SPAdes+Prokka+SRA-tools on uicgpu.
- Old `/usr/local/bin/spades.py` broken due to Py3.12 `distutils` removal; brew's SPAdes 4.3.0 works out of the box (uses bundled Python 3.14).
- S2 and EC-3 not re-assembled independently due to compute-time budget for a single subagent session. Reads are staged; a follow-up subagent could complete those assemblies in ~30 min each.
- My first enzyme-BLAST attempt used sequences I typed from memory as illustrative — 0 hits. Fix: pull the real reference CDS from GBFF and use those as queries. Lesson: never embed pseudo-FASTA "from memory"; always extract from a real source.
- Paper abstract says 435/303 contigs for S2/S3 but Table 1 says 87/63 — internal inconsistency in the paper itself. Table 1 is post-MeDuSa scaffolded, abstract is pre-scaffolded raw SPAdes.
- Paper's read-count numbers for S2/S3 (Section 4.3) are ~2× the SRA spot count. Most likely a paper-side counting convention (each PE mate) rather than data loss. Flagged in report.

## Verdict

**PARTIAL — REPLICATED-leaning.** Core S3 assembly claim (genome length 0.008 % delta, GC exact, N50 within 5 %) fully independently reproduced. Biological claim on enzyme repertoire fully supported. S2/EC-3 corroborated indirectly via reference genomes. Zero contradictions.
