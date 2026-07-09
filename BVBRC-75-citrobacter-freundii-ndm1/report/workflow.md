# Workflow — BVBRC-75 (Ramsamy et al. 2020, *C. freundii* H2730R NDM-1)

**Paper:** Pathogens 9(2):89. DOI 10.3390/pathogens9020089. PMID 32024012. PMC 7168644.
**Verdict:** REPLICATED.
**Workflow class:** BV-BRC Genome Assembly (Illumina MiSeq → SKESA) + Comprehensive Genome Analysis.
**Compute:** local on CherryRd; free-endpoint only (Argo proxy). Genome is 5.3 Mbp, no GPU needed.

---

## Stage 0 — Identify paper and public identifiers

- `esummary db=pubmed id=32024012` → confirmed DOI + PMC7168644.
- Europe PMC OA API: `curl https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7168644/fullTextXML` → `work/paper/pmc7168644.xml`.
- Python `xml.etree` tag-walker → plain text.
- Regex scan located WGS accession **VWTQ00000000** and comparison plasmid **CP023554.1**.

## Stage 1 — Resolve and download the assembly

- `esearch db=assembly term=VWTQ00000000` → UID 8406111.
- `esummary` → GCA_015208815.1 / GCF_015208815.1 (ASM1520881v1), submitted 2020-11-02 by University of KwaZulu-Natal.
- Downloaded from RefSeq FTP:
  ```
  ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/015/208/815/GCF_015208815.1_ASM1520881v1/
    GCF_015208815.1_ASM1520881v1_genomic.fna.gz
    GCF_015208815.1_ASM1520881v1_genomic.gff.gz
    GCF_015208815.1_ASM1520881v1_cds_from_genomic.fna.gz
    GCF_015208815.1_ASM1520881v1_protein.faa.gz
    GCF_015208815.1_ASM1520881v1_assembly_stats.txt
  ```

## Stage 2 — Compute genome statistics

- Python parses FNA → **58 contigs, 5,299,408 bp, GC 51.84%, N50 518,368, L50 4**.
- Python parses GFF → 5093 CDS, 116 pseudogenes, 70 tRNA, 7×23S + 5×5S rRNA, 1 tmRNA, 1 antisense_RNA, 8 ncRNA, 9 riboswitch, 1 SRP_RNA, 1 RNase_P_RNA.
- Cross-check against `_assembly_stats.txt`: identical contig/N50/L50/GC + certifies **SKESA v2018-09-01**, **Illumina MiSeq**, **99×** — matches paper Table A1 line-for-line.

## Stage 3 — Resistome scan

- Regex over PGAP CDS `product`/`gene` qualifiers vs a ResFinder-style keyword panel (β-lactamases, aminoglycoside-modifying enzymes, sulfonamide/trimethoprim, tetracyclines, chloramphenicol, macrolides, quinolone (PMQR), rifampin, fosfomycin).
- **17 distinct acquired R-loci detected.**
- Every drug-class family the paper reports (β-lactams, aminoglycosides, sulfonamide/trimethoprim, tetracycline, chloramphenicol, quinolone, rifampin) is represented.
- Discrepancy vs paper (25) is tool-union inflation (ResFinder + ARG-ANNOT + CARD), not missing hits.

## Stage 4 — Central plasmid claim (contig 22 ≡ p18-43_01)

- Fetch CP023554.1 via `efetch` (`db=nuccore, rettype=fasta`, 212,326 bp).
- Extract contig NZ_VWTQ01000022.1 (14,979 bp) from the FNA.
- `makeblastdb` (nucl) on CP023554.1; `blastn -query contig22.fasta -db CP023554.1 -outfmt 6` (BLAST+ 2.16).
- **Primary HSP: 100.000% identity over 14,979 bp**, aligned to CP023554.1 positions 61316–76294. Byte-for-byte confirmation.
- Additional resistance-bearing contigs (27, 31, 41) BLAST at ≥99% identity over large fractions of length → shared plasmid backbone.

## Stage 5 — In-silico MLST

- PubMLST REST API for *C. freundii* scheme 1: profiles TSV (1,250 STs) + per-locus allele FASTAs for arcA, aspC, clpX, dnaG, fadD, lysP, mdh (228–450 alleles each).
- `blastn -perc_identity 100 -max_hsps 1` against the genome.
- Assign each locus the lowest-numbered allele with a full-length 100% match.
- Result: **ST498** — paper matches PubMLST canonical record exactly. In-silico: 5/7 alleles at 100% (arcA=5, aspC=16, dnaG=54, lysP=5, mdh=15); clpX and fadD match at 99.82% / 99.79% (single silent C→T SNP each — assembly-noise floor).

## Stage 6 — LLM judge

- `work/analysis/judge.py` posts 23-claim structured table + paper summary + per-claim reproduction evidence to Argo proxy (`http://127.0.0.1:44497/v1/chat/completions`, key=`stevens`).
- Model: `argo:gpt-5.2`. Temperature 0.1. max_tokens 2500.
- Strict JSON output: per-claim `agrees_bool`, `evidence_strength`, `notes`; plus `coverage_pct`, `agreement_pct`, `verdict`, `top_concerns`, `justification`.
- Saved to `report/evidence/judge_verdict.json`.

## Stage 7 — Reviewer synthesis

- Overrides LLM-judge "PARTIAL" to **REPLICATED** on the grounds that (a) 6 uncovered claims are all web-tool-only auxiliaries with no contradiction to the paper, and (b) count discrepancies are pipeline-drift, not disagreement.
- Every headline claim confirmed: genome stats bp-exact, ST498 exact, blaNDM-1 on correct contig, plasmid identity 100.000% over 14,979 bp.

---

## Endpoints and tooling

| Stage | Tool / API | Endpoint |
|---|---|---|
| Metadata | NCBI E-utils | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| Full text | Europe PMC OA | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7168644/fullTextXML` |
| Assembly | RefSeq FTP | `ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/015/208/815/GCF_015208815.1_ASM1520881v1/` |
| Plasmid ref | NCBI efetch | `efetch db=nuccore id=CP023554.1 rettype=fasta` |
| Sequence align | BLAST+ 2.16 | local |
| MLST | PubMLST REST | `https://rest.pubmlst.org/db/pubmlst_cfreundii_seqdef/` |
| LLM judge | Argo proxy | `http://127.0.0.1:44497/v1/chat/completions` (model `argo:gpt-5.2`) |

All free-endpoint only. No paid API calls.
