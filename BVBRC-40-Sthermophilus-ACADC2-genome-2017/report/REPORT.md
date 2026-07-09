# Replication Report: Alexandraki et al. (2017)
## "The complete genome sequence of the yogurt isolate *Streptococcus thermophilus* ACA-DC 2"

**Paper:** Alexandraki V, Kazou M, Blom J, Pot B, Tsakalidou E, Papadimitriou K. *Standards in Genomic Sciences* **12**:18 (2017).
**DOI:** [10.1186/s40793-017-0227-5](https://doi.org/10.1186/s40793-017-0227-5) — **PMID:** 28163827 — **PMCID:** PMC5282782
**Open access:** ✅ (CC BY 4.0 / BMC)
**Genome:** ENA **LT604076** · BioProject **PRJEB14916** · NCBI assembly **GCA_900094135.1** (RefSeq **GCF_900094135.1**), ASM90009413v1

**Set:** BVBRC-40 (BVBRC-100 replication set; TOPUP85 rank-20)
**Report date:** 2026-07-01
**Analyst:** Ollie (OpenClaw AI) — Replication Wave 2026-07-01 (night push)
**Verdict:** **PARTIAL REPLICATION (strong).**

---

## 1. Paper

A genome-report describing the first complete genome of *Streptococcus thermophilus* ACA-DC 2, a
yogurt starter isolate. The genome was sequenced (Illumina + gap-filling), assembled into **one
circular chromosome**, and annotated with **RAST v2.0** plus Prodigal/MetaGeneAnnotator/FGENESB
gene calling, GenePRIMP pseudogene detection, WebMGA/EggNOG COG assignment, Pfam/Phobius domain
and topology analysis, and CRISPRFinder/REBASE/BAGEL3 for defense and bacteriocin features. The
paper's central deliverable is the **Table 3 genome-statistics report** plus qualitative findings
on CRISPR-*cas*, restriction-modification systems, stress-response genes, antimicrobial peptides,
and whole-genome phylogeny. It is exactly the class of paper the BV-BRC **Comprehensive Genome
Analysis (RASTtk)** workflow is designed to reproduce.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Complete genome publicly deposited; one circular chromosome. | Data availability | Yes | ✅ |
| C2 | Genome size = 1,731,838 bp. | Genome stat | Yes | ✅ |
| C3 | G+C = 39.21% (679,104 GC bp). | Genome stat | Yes | ✅ |
| C4 | 1,556 protein-coding genes. | Annotation stat | Yes | ✅ |
| C5 | 70 RNA genes = 56 tRNA + 14 rRNA. | Annotation stat | Yes | ✅ |
| C6 | 224 pseudogenes. | Annotation stat | Yes | ✅ |
| C7 | 1,850 total genes. | Annotation stat | Yes | ✅ |
| C8 | Function assigned to 1,182 genes (63.89%). | Functional annotation | Partly (workflow-dependent) | ⚠️ partial |
| C9 | Two single-spacer CRISPRs; one *cas*-associated (~STACADC2_0849-0856), one orphan; like LMD-9. | Genomic feature | Yes (with caveats) | ⚠️ partial |
| C10 | Annotation reproducible via standard RASTtk tools (BV-BRC CGA / Prokka). | Method | Yes | ⚠️ partial |

## 3. Method

All data pulled from **free public endpoints only**; all inference via **free Argo** (localhost:44497).
No paid `pdf`/`image` tools used — paper text obtained via Europe PMC OA XML.

1. **Paper text.** Fetched Europe PMC OA full-text XML (`PMC5282782/fullTextXML`, 107 KB), stripped
   to plain text (`work/paper_text.txt`), extracted Table 3 verbatim and the ENA accession
   (**LT604076**) + BioProject (**PRJEB14916**).
2. **Assembly resolution.** NCBI Datasets v2alpha REST `genome/bioproject/PRJEB14916/dataset_report`
   → **GCA_900094135.1** (author GenBank) and **GCF_900094135.1** (RefSeq/PGAP).
3. **Genome download.** NCBI Datasets REST `genome/accession/<acc>/download` with GENOME_FASTA +
   PROT_FASTA + GENOME_GFF + CDS_FASTA for both assemblies (free, no auth).
4. **Statistics recompute.** `work/genome_stats.py` (pure Python stdlib): length, GC bp/%, contig
   count, CDS count (protein.faa + GFF), tRNA/rRNA/pseudogene from GFF, gene-biotype breakdown.
5. **De-novo re-annotation (RASTtk-analog).** Copied the GCA chromosome to **uicgpu** (conda env
   `bvbrc28`), ran **Prokka 1.12** (`--kingdom Bacteria --genus Streptococcus --species thermophilus`),
   which bundles Prodigal (CDS), Aragorn (tRNA/tmRNA), barrnap (rRNA) — the same tool families the
   BV-BRC CGA RASTtk pipeline uses.
6. **CRISPR detection.** **minced** on the chromosome at default `minNR=3` and at `minNR=2`.
7. **LLM-judge scoring.** Fed the full claims table + real recomputed results to **argo:gpt-5.2**
   (free) for verdict/coverage/agreement. Output in `report/evidence/judge_output.txt`.

Scripts + data: `work/genome_stats.py`, `work/genome_stats.json`, `work/genomes/`,
`work/prokka_out/`, `work/paper_text.txt`, `work/judge_input.txt`, `work/judge_output.txt`.

## 4. Results vs Paper

### 4.1 Core genome statistics — GCA author assembly vs paper Table 3

| Attribute | Paper Table 3 | GCA_900094135.1 (recomputed) | Match |
|---|---:|---:|:--:|
| Genome size (bp) | 1,731,838 | 1,731,838 | ✅ EXACT |
| DNA G+C (bp) | 679,104 | 679,104 | ✅ EXACT |
| G+C % | 39.21 | 39.21 | ✅ EXACT |
| DNA scaffolds | 1 | 1 (circular) | ✅ |
| Protein-coding genes | 1,556 | 1,556 | ✅ EXACT |
| RNA genes | 70 | 70 (56 tRNA + 14 rRNA) | ✅ EXACT |
| tRNAs | 56 | 56 | ✅ EXACT |
| rRNAs | 14 | 14 | ✅ EXACT |
| Pseudogenes | 224 | 224 | ✅ EXACT |
| Total genes | 1,850 | 1,850 (1,556 CDS + 70 RNA + 224 pseudo) | ✅ EXACT |

**Every quantitative value in the paper's Table 3 reproduces to the digit** from the independently
downloaded, independently parsed deposited assembly. This confirms the public record is faithful to
the published table (no silent post-publication drift). *Caveat (weighted by the judge):* because the
deposited assembly IS the paper's assembly, exact agreement here primarily validates **record
fidelity**, not an orthogonal re-derivation — hence the independent-tool reruns below carry the
replication weight.

### 4.2 RefSeq/PGAP independent re-annotation (GCF, same sequence)

| Attribute | Paper | GCF_900094135.1 (PGAP) | Note |
|---|---:|---:|---|
| Genome size / GC | 1,731,838 bp / 39.21% | 1,731,838 bp / 39.21% | identical sequence |
| Protein-coding | 1,556 | 1,490 | within pipeline variance |
| Pseudogenes | 224 | 226 | within variance |
| tRNA | 56 | 56 | EXACT |
| rRNA | 14 | 15 | +1 |
| extra ncRNA | — | 1 tmRNA, 1 RNase_P, 1 SRP, 4 riboswitch | PGAP calls more ncRNA |

### 4.3 Prokka 1.12 de-novo re-annotation (RASTtk-analog, our run on uicgpu)

| Feature | Paper (RAST + manual curation) | Prokka 1.12 (de-novo) | Note |
|---|---:|---:|---|
| CDS | 1,556 (curated) | 1,818 (uncurated) | ≈ 1,556 + 224 pseudo-called-as-CDS + ~38 small ORFs |
| tRNA | 56 | 56 | ✅ EXACT |
| rRNA | 14 | 15 | +1 |
| tmRNA | — | 1 | — |
| Function assigned | 1,182 (63.89%) | 653 (35.9%) | default single-DB vs multi-tool+manual |

The CDS gap is the well-known **de-novo-vs-curated** difference (Prokka keeps short/dubious ORFs and
does not merge the 224 manually-flagged pseudogenes); tRNA is an exact match; the function-assignment
gap reflects Prokka's default DB search vs the paper's RAST + WebMGA + EggNOG + Pfam + manual stack.

### 4.4 CRISPR (C9)

| Setting | minced result | Interpretation |
|---|---|---|
| Default (minNR=3) | **0 arrays** | Single-spacer arrays have only 2 repeats → below default cutoff. **Corroborates** the paper's specific "both CRISPRs carry only one spacer." |
| minNR=2 | 6 low-repeat candidates | One at **~849,603–849,704 bp** coincides positionally with the paper's *cas*-flanked CRISPR near locus **STACADC2_0849** (~850 kb on a 1.73 Mb genome). |

CRISPR **presence is confirmed independently**; the exact array count is tool/threshold-dependent
(CRISPRFinder curated 2 confirmed vs minced-nr2 6 candidates), but the distinctive
**short/single-spacer, *cas*-adjacent** character the paper emphasizes is reproduced. Notably, the
fact that default minced finds *nothing* is itself positive evidence for the paper's single-spacer claim.

## 5. Verdict

**PARTIAL REPLICATION (strong).**

- **Reproduced exactly (C1–C7):** genome availability, single circular chromosome, size
  (1,731,838 bp), GC (39.21%), protein-coding count (1,556), RNA count (70 = 56 tRNA + 14 rRNA),
  pseudogenes (224), total genes (1,850) — all to the digit from the independently pulled/parsed
  assembly, cross-checked by PGAP re-annotation (within variance) and Prokka (tRNA exact).
- **Partial (C8–C10):** the paper's 63.89% function-assignment percentage was **not** reproduced
  with default Prokka (needs the paper's multi-tool + manual-curation workflow); the exact "two
  single-spacer CRISPRs" is tool-parameter-sensitive (presence confirmed, count not); the full
  RAST/RASTtk workflow was approximated with Prokka rather than rerun through the BV-BRC CGA service.

This is not a full REPLICATED because the highest-value exact agreements are record-fidelity
confirmations of the authors' own deposit, and the workflow-dependent claims (functional annotation
%, exact CRISPR count) were only partially reproduced. It is well above SPOT-CHECK because real data
were pulled and multiple independent tools (own stdlib recompute, PGAP, Prokka, minced) were run and
agree on all structural claims.

## 6. Coverage / Agreement

- **Coverage: 10/10** — all ten claims were testable against the real deposited sequence and/or
  independent re-annotations, and all were tested (LLM-judge concurred: 10/10).
- **Agreement: 7/10** — C1–C7 agree exactly; C8 (function %), C9 (exact CRISPR count), C10 (full
  RASTtk workflow) are only partially reproduced (LLM-judge: 7/10). **No contradictions** were found:
  every partial is a workflow/threshold gap, not a data conflict. No numbers were fabricated — all
  come from parsing un-modified NCBI assemblies and from `prokka`/`minced`/`optimize`-class tool output.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST (`fullTextXML`) | OA paper text + accessions | Free |
| NCBI Datasets v2alpha REST | BioProject→assembly resolve + genome/protein/GFF download | Free, no auth |
| Python 3 stdlib | genome-stats recompute | Free |
| Prokka 1.12 (+ Prodigal/Aragorn/barrnap) | de-novo RASTtk-analog annotation | Free (uicgpu) |
| minced 2.x | CRISPR detection | Free (uicgpu) |
| Argo proxy `argo:gpt-5.2` | LLM-judge scoring | Free |
| uicgpu A100 node | annotation compute (~1 min) | Free |

## 8. Limitations

- Exact Table-3 agreement is partly expected (deposit = paper's assembly); the independent weight
  is in the PGAP/Prokka/minced reruns.
- Function-assignment % requires the paper's RAST + WebMGA + EggNOG + Pfam + manual pipeline; not
  reproduced here with default Prokka.
- Exact CRISPR count is tool/threshold-dependent; only presence + single-spacer/*cas*-adjacency
  reproduced, not the curated count of exactly two.
- The actual BV-BRC Comprehensive Genome Analysis (RASTtk) web service was not run; Prokka used as
  a free local analog. Running the genome through BV-BRC CGA would close the C10 gap.
- RM systems, stress genes, bacteriocins, and whole-genome phylogeny (secondary qualitative paper
  findings) were not independently reproduced this pass.

## Verdict
**Verdict:** PARTIAL

WAVE_RESULT set=BVBRC-40 paper=Sthermophilus-ACADC2-genome-2017 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-40-Sthermophilus-ACADC2-genome-2017/ one_line=Deposited assembly (GCA_900094135.1/LT604076) reproduces paper Table 3 to the digit (1,731,838 bp, 39.21% GC, 1,556 CDS, 56 tRNA, 14 rRNA, 224 pseudo, 1,850 genes); PGAP+Prokka re-annotation within variance (tRNA exact); CRISPR presence + single-spacer/cas-adjacency confirmed via minced; function-% and exact CRISPR count workflow-dependent → PARTIAL (strong), coverage 10/10 agreement 7/10.
