# Replication Workflow — BVBRC-46 (K. pneumoniae ST1588 NDM-1 megaplasmid)

**Paper.** Quezada-Aguiluz et al., *Antibiotics* 11(9):1207 (2022).
DOI 10.3390/antibiotics11091207 · PMC9494972 · CC BY 4.0.
**Verdict.** REPLICATED (Coverage 8/10, Agreement 9/10).
**Compute host.** uicgpu (conda envs `kleborate` v3.2.4 and `bvbrc14`).
**Total wall-clock.** ~few minutes of active compute + one-time Kleborate DB pull.
**Cost.** $0 (all free/public endpoints — Europe PMC REST, NCBI eutils,
NCBI Datasets v2alpha REST, Argo proxy for the LLM judge).

---

## Stage 1 — Paper acquisition & accession extraction

| Step | Tool / endpoint | Output |
|---|---|---|
| Resolve DOI → PMC ID | Europe PMC REST `search?query=DOI:10.3390/antibiotics11091207` | PMC9494972 |
| Pull full-text XML | Europe PMC REST `article/PMC9494972/fullTextXML` | XML → parsed text |
| Extract accessions | Python regex on XML (`JAMJQY\w+`, `SAMN\w+`) | JAMJQY000000000, SAMN28534325 |

**Note.** No `pdf`/`image` (paid) tools used. Europe PMC full-text XML is
free and complete for CC-BY open-access articles.

## Stage 2 — Assembly resolution & download

| Step | Tool / endpoint | Output |
|---|---|---|
| WGS → assembly | eutils `esearch db=assembly term=JAMJQY01` | GCF_023554495.1 |
| Genome bundle | NCBI Datasets v2alpha REST `genome/accession/GCF_023554495.1/download` (types: GENOME_FASTA, PROT_FASTA, CDS_FASTA, GENOME_GFF) | `GCF_023554495.1.zip` |
| Unzip + inspect | `unzip` + Biopython `SeqIO.parse` | 15 contigs, total ~5.8 Mb |

## Stage 3 — Contig inventory & split

| Step | Tool | Output |
|---|---|---|
| Enumerate contigs (length, GC, description) | Biopython `SeqIO` + `SeqUtils.gc_fraction` | `contig_inventory.tsv` |
| Identify + split megaplasmid | `SeqIO.write` on `NZ_JAMJQY010000002.1` | `pNDM-1_UCO-361.fna` (314,976 bp, GC 47.08%) |
| Identify + split IncFIB(K) contig | `SeqIO.write` on `NZ_JAMJQY010000003.1` | `IncFIBK_contig3.fna` (197,209 bp, GC 52.15%) |

## Stage 4 — Typing on uicgpu

Two conda environments; both free/open tools.

### 4a. Kleborate (conda env `kleborate` v3.2.4)
```bash
kleborate -a UCO-361.fna -o kleborate_out -p kpsc
```
Returns: species, KpSC 7-locus MLST/ST, Kaptive K locus, Kaptive O locus,
acquired resistome, virulence loci.

### 4b. abricate per-contig (conda env `bvbrc14`, DBs 2026-Apr-3)
```bash
for db in plasmidfinder resfinder ncbi card; do
  for contig in chr.fna pNDM-1_UCO-361.fna IncFIBK_contig3.fna; do
    abricate --db $db $contig > abricate_${db}_${contig%.fna}.tsv
  done
done
```
Per-contig runs localize replicons and ARGs to specific molecules.

### 4c. AMRFinderPlus whole-assembly
```bash
amrfinder -n UCO-361.fna --plus --organism Klebsiella_pneumoniae \
  -o amrfinder_out.tsv
```
Provides contig coordinates + AMR + stress genes; used as third
independent AMR call.

## Stage 5 — Tn3000 structure reconstruction

| Step | Tool | Output |
|---|---|---|
| Parse PGAP `genomic.gff` | Python | CDS list on megaplasmid |
| Window ±12 kb around blaNDM-1 (308,200–309,012) | Python filter on start/end | 9-feature transposon table |
| Cross-map to paper Fig. 1B labels | Manual annotation | `tn3000_order.tsv` |

## Stage 6 — Comparative genomics

```bash
# reference plasmid
efetch -db nuccore -id NZ_MN598004.1 -format fasta > EC12.fna
makeblastdb -in EC12.fna -dbtype nucl -out ec12db

# BLAST megaplasmid vs pNDM-1-EC12
blastn -query pNDM-1_UCO-361.fna -db ec12db -evalue 1e-50 \
  -outfmt "6 qstart qend sstart send length pident evalue" \
  > blast_meg_vs_ec12.tsv

# merge HSP intervals for coverage %
python merge_hsps.py blast_meg_vs_ec12.tsv    # → ~64.7% coverage
# isolate HSP overlapping blaNDM-1 → 2,488 bp @ 99.96% id
```

## Stage 7 — LLM judge (Coverage / Agreement / Verdict)

```bash
# free Argo endpoint, model argo:gpt-5.2
curl -sS http://<tailnet-aggregator>:4000/v1/chat/completions \
  -H "Authorization: Bearer stevens" \
  -H "Content-Type: application/json" \
  -d '{"model":"argo:gpt-5.2","messages":[
    {"role":"system","content":"You are a replication judge..."},
    {"role":"user","content":"<paper summary + results table>"}]}'
```
Judge returned: **Coverage 8/10, Agreement 9/10, Verdict REPLICATED**
(single-model, single-prompt — see failure_analysis.md).

---

## Tool & code manifest (all free, all reproducible)

| Category | Tool | Version | Endpoint |
|---|---|---|---|
| Paper text | Europe PMC REST | live | `https://www.ebi.ac.uk/europepmc/webservices/rest/` |
| Assembly lookup | NCBI Entrez eutils | live | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| Assembly download | NCBI Datasets v2alpha REST | live | `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/` |
| Sequence I/O | Biopython | 1.83 | conda |
| Species / ST / K/O / resistome | Kleborate | 3.2.4 | conda env `kleborate` |
| Replicon / AMR (per-contig) | abricate | ≥1.0.1 | conda env `bvbrc14` |
| AMR DBs for abricate | plasmidfinder, resfinder, ncbi, card | 2026-Apr-03 | `abricate --setupdb` |
| AMR + stress (whole genome) | AMRFinderPlus | recent | conda env `bvbrc14` |
| BLAST | blastn / makeblastdb | 2.15+ | conda env `bvbrc14` |
| LLM judge | Argo proxy `argo:gpt-5.2` | live | `http://<tailnet-aggregator>:4000/v1` (Bearer stevens) |
| Orchestration | Python + shell subagent scripts | — | Ollie subagent runtime |

## Work estimate

| Phase | Human/agent effort | Compute wall-clock |
|---|---|---|
| Read paper (Europe PMC XML) + extract accessions | 5 min | <1 min |
| Download assembly (NCBI Datasets) | <1 min | <1 min |
| Contig inventory + split | <5 min | <10 s |
| Kleborate (`-p kpsc`, first-run DB download) | — | ~5–10 min (one-time), ~1 min steady-state |
| abricate per-contig × 4 DBs | — | ~1 min |
| AMRFinderPlus (whole genome) | — | ~1 min |
| Tn3000 GFF parsing | 5 min | <5 s |
| blastn vs pNDM-1-EC12 + HSP merge | 5 min | ~30 s |
| LLM judge call + result parse | 2 min | ~10 s |
| Report assembly (Markdown + LaTeX) | ~15 min | — |
| **Total** | **~40 min agent time** | **~5–15 min compute (dominated by Kleborate first-run)** |

## Reproducibility one-shot

```bash
# Everything above, chained
curl -sS -o GCF_023554495.1.zip \
  "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_023554495.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF"
unzip -q GCF_023554495.1.zip -d GCF_023554495.1
kleborate -a UCO-361.fna -o kleborate_out -p kpsc
abricate --db plasmidfinder pNDM-1_UCO-361.fna
abricate --db resfinder    pNDM-1_UCO-361.fna
amrfinder -n UCO-361.fna --plus --organism Klebsiella_pneumoniae
efetch -db nuccore -id NZ_MN598004.1 -format fasta > EC12.fna
makeblastdb -in EC12.fna -dbtype nucl -out ec12db
blastn -query pNDM-1_UCO-361.fna -db ec12db \
  -outfmt "6 qstart qend length pident" > blast.tsv
```
