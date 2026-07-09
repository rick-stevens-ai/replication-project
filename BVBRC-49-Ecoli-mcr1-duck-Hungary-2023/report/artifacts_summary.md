# Artifacts Summary — BVBRC-49

**Paper:** Szmolka et al. 2023, *Antibiotics* 12(10):1519 (PMC10604428).
**Isolate:** Ec45-2020 (Hungarian duck E. coli, mcr-1+).
**Assembly analyzed:** GCF_038709795.1 (RefSeq) / GCA_038709795.1 (GenBank).

---

## Report deliverables (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical markdown replication report (paper summary, claims table, methods, results, verdict, coverage/agreement scores, resources, limitations). Verdict: **PARTIAL**. |
| `REPORT.tex` | LaTeX rendering of the same report with an additional **Genuine Critique** section detailing what did and did not replicate. |
| `open_questions.json` | 5 truly-open follow-on questions specific to 2023 Hungary duck E. coli mcr-1 (IncX4/IncHI2 backbone diversity, Hungarian colistin-use timeline, duck-worker zoonotic transfer, mcr-1 × ESBL co-carriage in Anseriformes, wild-waterfowl reservoir role). Each with `basis` + `next_steps`. |
| `workflow.md` | End-to-end procedure: paper acquisition → assembly resolution → download → typing on uicgpu → claim-by-claim scoring → LLM-judge → report authoring. Includes one-command reproducibility block. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest accounting of what did not work, was not done, or fell outside sequence-only replication. |

## Raw evidence (`report/evidence/`)

| File | Tool | What it contains |
|---|---|---|
| `mlst.tsv` | mlst 2.33.1 | Sequence type call (ST162) + 7-gene Achtman allele profile: adk(9) fumC(65) gyrB(5) icd(1) mdh(9) purA(13) recA(6). |
| `amrfinder.tsv` | AMRFinderPlus 4.2.7 (DB 2026-03-24.1) | AMR gene calls (mcr-1.1 on CP134089; blaEC AmpC; QRDR point mutations gyrA S83L + D87N and parC S80I on chromosome; qnrS1, dfrA12, aadA1/2, sul3, cmlA1, floR, blaTEM-135, sul2, tet(A), tet(M), qacL on CP134088; virulence: astA, lpfA, ybtP/ybtQ, hlyE). |
| `abricate_resfinder.tsv` | abricate 1.4.0 + resfinder DB (2026-Apr-3) | Acquired ARG hits per contig with % coverage/identity and reference accession. |
| `abricate_plasmidfinder.tsv` | abricate 1.4.0 + plasmidfinder DB (2026-Apr-3) | Plasmid replicon calls: IncX4 on CP134089 (100/100 to CP002895); IncHI1A + IncHI1B(R27) + IncFIA(HI1) on CP134088. |
| `abricate_vfdb.tsv` | abricate 1.4.0 + vfdb DB (2026-Apr-3) | 124 virulence-factor gene hits on chromosome incl. astA (EAST1), lpfA, lpfA-O113, hlyE, ybtP/ybtQ (yersiniabactin/HPI). |
| `genome_stats.json` | Custom Python (Biopython SeqIO) | Per-replicon length + GC%. Chromosome 4,967,063 bp / 50.73% GC + 5 plasmids (254,224; 190,488; 101,848; 33,541; 5,714 bp). |
| `llm_judge_gpt52.md` | Argo proxy `argo:gpt-5.2` | LLM-judge natural-language reasoning for coverage/agreement scores. Coverage 8/10, Agreement 9/10. |

## Working files (`work/`)

| File | Purpose |
|---|---|
| `genome_stats.py` | Python script that iterates the RefSeq assembly FASTA (Biopython SeqIO) and emits per-replicon length + GC% JSON. |
| `GCF_038709795.1/` | Unpacked NCBI Datasets download bundle (genomic FASTA, protein FASTA, GFF3). |
| `GCF_038709795.1.zip` | Original ~3.2 MB download bundle from NCBI Datasets v2alpha REST. |

## External inputs

| Source | Access | Purpose |
|---|---|---|
| Europe PMC (PMC10604428 fullTextXML) | REST, free | Paper text, claim extraction, accession recovery. |
| NCBI Datasets v2alpha REST | REST, free, no auth | BioProject PRJNA1012593 → GCF_038709795.1 → FASTA/GFF/protein download. |
| NCBI RefSeq assembly GCF_038709795.1 | Public | The genome analyzed. Replicons NZ_CP134085 (chr) + NZ_CP134086–NZ_CP134090 (5 plasmids). |

## Compute footprint

- **Host:** uicgpu (8×A100 A100 node), conda env `bvbrc14`.
- **Wall clock:** ~2 min (mlst + abricate ×3 DBs) + 63 s (AMRFinderPlus) = ~3 min end-to-end typing.
- **Storage:** ~3.2 MB download + ~15 MB unpacked + ~200 KB evidence tables.
- **Network cost:** 0 (free Europe PMC + NCBI Datasets endpoints).

## Verdict inputs

| Input | Value |
|---|---|
| Claims tested (C1, C2, C3, C4, C5-genotype, C6) | 6 of 7 |
| Claims exactly matched | C1, C2, C3, C4, C6 (5 of 7) |
| Claim partially matched | C5 (genotype ✅, MIC ❌ not re-measured) |
| Claim not tested | C7 (no offline serotyper) |
| Coverage score (LLM-judge, argo:gpt-5.2) | 8/10 |
| Agreement score (LLM-judge, argo:gpt-5.2) | 9/10 |
| Fabricated numbers | 0 (all numbers derive from mlst/AMRFinderPlus/abricate on unmodified assembly) |
| Contradictions with paper | 0 |
| **Final verdict** | **PARTIAL REPLICATION (strong)** |
