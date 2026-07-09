# Artifacts Summary — BVBRC-46 (K. pneumoniae ST1588 NDM-1 megaplasmid)

**Directory root.**
`~/Dropbox/REPLICATE-PROJECT/BVBRC-46-Kpneumoniae-ST1588-NDM1-megaplasmid-2022/`

**Verdict.** REPLICATED · Coverage 8/10 · Agreement 9/10 (free-Argo
`argo:gpt-5.2` judge).

**Paper.** Quezada-Aguiluz et al. 2022, *Antibiotics* 11(9):1207,
DOI 10.3390/antibiotics11091207, PMC9494972, CC BY 4.0.

---

## Reports (this directory)

| Artifact | Purpose |
|---|---|
| `REPORT.md` | Human-readable narrative report (paper summary, claims tested, method, results vs paper, verdict, limitations, reproducibility one-shot). Authoritative source-of-truth for this replication. |
| `REPORT.tex` | Full LaTeX report; section-by-section; includes dedicated **GENUINE CRITIQUE** section auditing evidence strength. |
| `open_questions.json` | 5 structured open questions (`q`, `basis`, `next_steps`) grounded in K. pneumoniae ST1588 NDM-1 megaplasmid biology. |
| `workflow.md` | End-to-end reproducible workflow: paper acquisition → assembly download → typing → Tn3000 reconstruction → comparative BLAST → LLM judge; with tool/version/endpoint manifest and work estimate. |
| `artifacts_summary.md` | This file. Index of every artifact + trace of external inputs. |
| `failure_analysis.md` | Honest failure/gap analysis: PDF availability, unrun analyses, single-judge caveat. |

## External inputs (all free/public — traces)

| Input | Accession / URL | Source | Fetched via |
|---|---|---|---|
| Paper full text | PMC9494972 (JATS XML) | Europe PMC | REST `article/PMC9494972/fullTextXML` |
| WGS project | JAMJQY000000000 (v JAMJQY010000000) | DDBJ/ENA/GenBank | eutils `esearch db=assembly term=JAMJQY01` |
| Assembly | GCF_023554495.1 / GCA_023554495.1 | NCBI RefSeq / GenBank | NCBI Datasets v2alpha REST |
| BioSample | SAMN28534325 | NCBI BioSample | (via assembly metadata) |
| Comparison plasmid | NZ_MN598004.1 (pNDM-1-EC12, E. cloacae) | NCBI nuccore | eutils `efetch` |
| Kleborate DB | KpSC scheme + Kaptive references | Kleborate v3.2.4 bundled | `kleborate --setupdb` (one-time) |
| abricate DBs | plasmidfinder, resfinder, ncbi, card | 2026-Apr-03 snapshots | `abricate --setupdb` |
| AMRFinderPlus DB | NCBI AMRFinderPlus | current | `amrfinder -u` |

## Genome-derived artifacts (in `work/` on uicgpu; sizes exact)

| File | Contents |
|---|---|
| `GCF_023554495.1/` | Full NCBI Datasets bundle (genome FASTA, protein FASTA, CDS FASTA, genomic GFF, README, data catalog). |
| `chromosome.fna` | NZ_JAMJQY010000001.1, 5,288,551 bp, GC 57.36%. |
| `pNDM-1_UCO-361.fna` | NZ_JAMJQY010000002.1, **314,976 bp**, GC 47.08% (megaplasmid — matches paper to the bp). |
| `IncFIBK_contig3.fna` | NZ_JAMJQY010000003.1, **197,209 bp**, GC 52.15% (IncFIB(K) plasmid — matches paper to the bp). |
| `contig_inventory.tsv` | Per-contig length + GC + description for all 15 contigs. |
| `kleborate_out/` | Kleborate `-p kpsc` outputs (ST, K, O, resistome, virulence tables). |
| `abricate_*_*.tsv` | Per-DB × per-contig abricate outputs (12 tables). |
| `amrfinder_out.tsv` | AMRFinderPlus whole-genome table with contig coordinates. |
| `tn3000_order.tsv` | Reconstructed Tn3000 gene order table (9 features across 304,754–316,359). |
| `blast_meg_vs_ec12.tsv` | blastn HSPs (73) between megaplasmid and pNDM-1-EC12. |
| `blast_ndm_region.tsv` | Isolated HSP overlapping blaNDM-1 → **2,488 bp @ 99.96% id** (exact match). |

## Traces / provenance

- **Analyst:** Ollie (OpenClaw AI), replication subagent.
- **Dates:** 2026-07-01 / 2026-07-02 (CDT).
- **Compute host:** uicgpu (conda envs `kleborate` v3.2.4 and `bvbrc14`).
- **LLM judge:** `argo:gpt-5.2` via free Argo proxy at
  `http://<tailnet-aggregator>:4000/v1` (Bearer `stevens`).
- **Cost:** $0. No paid tools (`pdf`/`image`) invoked. All external calls
  hit free/public endpoints (Europe PMC, NCBI eutils, NCBI Datasets REST)
  or free internal endpoints (Argo).
- **Wave:** BVBRC-46 (part of BVBRC-100 replication wave), TOPUP85 rank-28.

## Key claims → artifact mapping

| Paper claim | Artifact that supports it |
|---|---|
| Megaplasmid 314,976 bp | `contig_inventory.tsv`, `pNDM-1_UCO-361.fna` |
| Tn3000 gene order | `tn3000_order.tsv` (parsed from `genomic.gff`) |
| ST1588 / KL108 / O1 | `kleborate_out/` |
| Full resistome | `kleborate_out/`, `abricate_resfinder_*.tsv`, `amrfinder_out.tsv` |
| 197,209 bp IncFIB(K); complete tra; no ARG | `IncFIBK_contig3.fna`, `abricate_plasmidfinder_IncFIBK_contig3.tsv`, `abricate_resfinder_IncFIBK_contig3.tsv` (empty for ARGs; TraA…TraY + Trb from `genomic.gff`) |
| Un-typeable megaplasmid | `abricate_plasmidfinder_pNDM-1_UCO-361.tsv` (partial hybrid repHI5B/repFIB only) |
| 2,488 bp shared NDM region vs pNDM-1-EC12 | `blast_ndm_region.tsv` (2,488 bp @ 99.96% id — exact) |
| oqxB "on megaplasmid" (paper) → actually chromosomal | `abricate_resfinder_chr.tsv`, `abricate_ncbi_chr.tsv`, `amrfinder_out.tsv` (all locate oqxA/B on contig 1) |

## Not produced (see `failure_analysis.md`)

- No paper PDF locally cached (Europe PMC full-text XML used instead —
  the article is CC BY 4.0 so the PDF is free but was not needed).
- No re-assembly from raw Illumina + Nanopore reads.
- No wet-lab reproduction of the conjugation frequency
  (4.3×10⁻⁶ at 27 °C) or the AST/MIC panel — these are wet-lab
  phenotypes.
- No multi-judge or blinded verdict scoring (single Argo `argo:gpt-5.2`).
- No cross-database SNP calling on the raw reads.
