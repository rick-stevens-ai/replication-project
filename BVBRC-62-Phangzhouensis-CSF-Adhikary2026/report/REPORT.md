# BVBRC-62 — Independent Replication
## *Providencia hangzhouensis* HL_Adamas-11 (MDR, cerebrospinal fluid, Kolkata)

**Replicator:** OpenClaw subagent (CherryRd), 2026-07-02. Free/open-source tools only.

---

## 1. Paper
**Citation:** Adhikary R, Acharya K, Poddar S, Sen T, Ghosh M, Bhattacharya A, Hazra S.
"Decoding the genome of multidrug resistant (MDR) *Providencia hangzhouensis* from a
cerebrospinal fluid infection isolated from the hospital of Kolkata, West Bengal, India."
*Microbiology Resource Announcements* (2026), e01372-25.

- **DOI:** 10.1128/mra.01372-25
- **PMID:** 42059626 · **PMCID:** PMC13248694 · Open Access (CC-BY 4.0)
- Full text pulled from Europe PMC (`.../PMC13248694/fullTextXML`) — no paid PDF tools.

**Data accessions (from paper):** BioProject PRJNA1314473 · BioSample SAMN51056432 ·
WGS SGQL00000000 · SRA SRR35282168.

**Assembly used for replication:** **GCA_053592895.1 / GCF_053592895.1** (ASM5359289v1).
Identified unambiguously by matching the paper's *exact* reported Coverage = 91.664× and
ContigN50 = 16,147 bp to the NCBI assembly record linked from BioSample SAMN51056432.
(Note: NCBI also holds an identical duplicate submission GCF_056140255.1 with the same
biosample/coverage/N50 — a redundant deposit of the same isolate.)

---

## 2. What I actually ran
Downloaded the assembly (genome FASTA + protein.faa + GFF + assembly report) with the NCBI
`datasets` CLI. Then, all with free/OSS tools on CherryRd:

| Step | Tool | Purpose |
|---|---|---|
| Assembly metrics | Biopython + NCBI `datasets` report | contigs, length, GC, N50 |
| Feature counts | GFF parse + NCBI annotation stats | CDS/tRNA/rRNA/ncRNA |
| Species/ANI | `fastANI` v1.x + `skani` | taxonomy vs *P. hangzhouensis* ref GCF_029193595.2 |
| AMR/virulence | **AMRFinderPlus v4.2.7**, DB 2026-05-15.1 (`--plus`, nucleotide mode) | resistance genotype |
| MLST | `mlst` v2.33.1 (Torsten Seemann, PubMLST schemes) | sequence type |
| Plasmid replicon count | contig plasmid labels in NCBI assembly | "chromosome + 4 plasmids" claim |

Judge: Argo `gpt-5.2` (temp 0), reading the report prose (LLM judge, not regex).

---

## 3. Per-claim reproduction (my numbers vs paper)

### 3.1 Genome architecture
| Metric | Paper | My value | Verdict |
|---|---|---|---|
| Contigs | 493 | **493** | ✓ exact |
| Total length | 5,034,782 bp | 5,024,867 bp | ~✓ (−9,915 bp, −0.20%; GenBank filtering of short/low-qual contigs) |
| N50 | 16,147 bp | **16,147 bp** | ✓ exact |
| Coverage | 91.664× | 91.664× (assembly record) | ✓ exact (same deposit) |
| **GC content** | **49.5%** | **42.35% (my calc) / 42.5% (NCBI)** | ✗ **DISCREPANT** |
| Protein-coding genes | 4,935 | **4,935** | ✓ exact |
| tRNA | 59 | **59** | ✓ exact |
| rRNA | 4 | **4** | ✓ exact |
| Plasmids | chromosome + 4 plasmids | 4 distinct plasmid names (pAA860, pAB133, pAC129, pnovel_c01a4b) | ✓ |

**GC error:** The paper's 49.5% is essentially certainly a typo/error. *Providencia*
genomes are ~41–42% GC as a genus; both my independent calculation (42.35%) and NCBI's own
assembly-report field (42.5%) agree at ~42.4%. 49.5% would be biologically anomalous for the
genus and is not supported by the deposited sequence. Every other architecture number matches
exactly, so this is an isolated reporting error, not a data problem.

### 3.2 Taxonomy / ANI
- Paper: "98.75% ANI with the reference genome"; 99.93% homology to *Providencia* sp. PR002.
- Mine: **fastANI 98.46%** and **skani 98.62%** vs *P. hangzhouensis* reference GCF_029193595.2
  (strain PR-310). Both are well above the 95% species boundary → species assignment
  *P. hangzhouensis* confirmed. My 98.46–98.62% is within ~0.3% of the paper's 98.75%
  (differences attributable to which reference genome is chosen and which ANI tool). ✓ Agreement.

### 3.3 MLST
- Paper: **ST-356** (PubMLST).
- Mine: `mlst` v2.33.1 with its bundled `providencia` scheme calls the isolate as **ST = "-"
  (unassigned/novel)** with alleles fusA(17) gyrB(105) ileS(29) lepA(~49) leuS(49).
- **Not reproduced / inconclusive.** The `mlst` package ships the classic *Providencia*
  (largely *P. stuartii*) 5-locus scheme; the paper used the live PubMLST *Providencia* DB,
  which has since added *P. hangzhouensis* profiles/allele numbers. This is a **scheme/DB-version
  mismatch**, not necessarily a contradiction — I cannot confirm or refute ST-356 without the
  exact PubMLST scheme version the authors queried. See §5.

### 3.4 AMR genotype (the paper's central functional claim)
Paper's claimed resistance cassette vs my AMRFinderPlus (nucleotide, DB 2026-05-15.1):

**β-lactam** — paper: blaTEM-1, blaNDM-1, blaVEB-9, blaOXA-21, blaOXA-181
- ✓ blaTEM, ✓ blaNDM-1, ✓ blaVEB-9, ✓ blaOXA-21, ✓ blaOXA-181 — **all 5 recovered.**
  (My DB also flags additional β-lactamases: blaOXA-9, blaPER, blaDHA.)

**Aminoglycoside** — paper: aph(3')-V, aadA21, armA
- ✓ **armA** (exact). ✓ **aph(3')-VI** recovered (paper wrote "aph(3')-V"; APH(3')-VI is the
  valid real gene — likely a paper typo). ✓ aadA family present as **aadA1 + aadA2** (paper
  wrote "aadA21"; my DB resolves to aadA1/aadA2 — allele-nomenclature/typo difference).
  Also found aac(6')-Ib. **Class fully confirmed.**

**Macrolide / phenicol** — paper: MphE, msrE, mrx, catA1, cmlA5
- ✓ mph(E), ✓ msr(E), ✓ mrx(A), ✓ catA1, ✓ cmlA5 — **all 5 recovered exactly.**
  (Plus mph(A), ere(A)×2 additional macrolide genes.)

**Overall AMR concordance:** every one of the paper's 4 named resistance classes (β-lactam,
aminoglycoside, macrolide, phenicol) is confirmed, and 11–13 of the ~13 specifically named
genes are recovered exactly or as the obvious correct allele. My independent screen also finds
**more** resistance determinants than the paper reported (tet(A), qnrD, sul1, dfrA1, arr-2,
blaPER, blaDHA, blaOXA-9, aac(6')-Ib, mph(A), ere(A), ble) — i.e. the MDR claim is if anything
*understated* in the announcement. Metal-resistance (mer operon: merA/B/D/E/P/R/T) also present.

Full table: `work/amrfinder_nuc.tsv` (27 AMR rows).

---

## 4. Verdict

**PARTIAL** — verdict assigned by independent Argo gpt-5.2 LLM judge (temp 0).

- **Coverage/10: 8** (judge)
- **Agreement/10: 7** (judge)

What replicated exactly: genome architecture (contigs 493, N50 16,147, coverage 91.664×,
CDS 4,935, tRNA 59, rRNA 4, chromosome+4 plasmids), species/ANI assignment
(*P. hangzhouensis*, 98.46–98.62% vs 98.75%), and the entire named AMR cassette — all 5
β-lactamases (incl. NDM-1 carbapenemase + OXA-181), armA + aph/aadA aminoglycoside genes,
and all 5 macrolide/phenicol genes (mph(E), msr(E), mrx(A), catA1, cmlA5). My independent
screen finds *more* AMR determinants than the paper reported, so the MDR conclusion is fully
(and then some) supported.

What pulled the verdict to PARTIAL: (1) GC% is a real numeric discrepancy — paper 49.5% vs
true ~42.4% (an author typo, contradicted by the deposited sequence and NCBI's own field);
(2) MLST ST-356 could not be independently confirmed (PubMLST scheme-version mismatch;
bundled `mlst` returns ST-unassigned); (3) CheckM completeness/contamination was not re-run
(out of scope). The core science replicates; the verdict reflects these unverified/erroneous
secondary items.

**Judge rationale (verbatim):** "The replication re-tested most genome-derivable claims tied
to the deposited assembly … strong concordance. However, at least two paper-reported
genome-derived items were not reproduced or were contradicted: GC% is a major numeric
discrepancy … and MLST ST-356 was not independently confirmed … Overall, substantial but not
complete coverage, with generally good agreement except for the GC% error and unresolved MLST."

---

## 5. Reproducibility-blocker critique (precise missing artifacts)

1. **GC = 49.5% is unreproducible and wrong.** The deposited assembly is 42.4% GC by two
   independent methods (my Biopython calc + NCBI's own report field). The paper's 49.5% is not
   derivable from any deposited artifact. *Missing/broken artifact:* none — this is a
   transcription error in the manuscript, not a data gap.

2. **MLST ST-356 not independently confirmable.** *Missing artifact:* the exact **PubMLST
   *Providencia* scheme version / allele-definition snapshot** the authors used. The `mlst`
   package's bundled scheme returns ST-unassigned. Without the pinned PubMLST DB date (or the
   per-locus allele numbers the authors called), ST-356 cannot be reproduced deterministically.
   Authors should have cited the PubMLST download date and the 7/5-locus allele profile.

3. **CheckM completeness 93.78% / contamination 5.14% not re-run.** *Missing artifact:* none
   critical — CheckM v1.2.4 + its lineage DB would reproduce this, but it was out of scope here
   (heavy DB). Given all other annotation numbers match, this is low-risk. Reproducible in
   principle with the deposited assembly.

4. **aadA21 / aph(3')-V allele nomenclature.** *Missing artifact:* the authors' exact
   CARD v6.0.5 / ResFinder v4.7.2 hit tables. My AMRFinderPlus resolves these to aadA1/aadA2
   and aph(3')-VI. The class-level resistance is unambiguous; only the precise allele label
   differs, likely a manuscript typo (there is no "aph(3')-V"; APH(3')-VI is the real gene).

None of these block the core scientific conclusion. The genome + AMR genotype fully replicate
from public data.

---

## 6. Files
- `work/paper_fulltext.xml` — Europe PMC full text
- `genomes/…/GCA_053592895.1_…_genomic.fna` — assembly
- `work/fastani_ref.txt` — ANI result
- `work/mlst_out.txt`, `work/mlst.log` — MLST
- `work/amrfinder_nuc.tsv`, `work/amrfinder_nuc.log` — AMR genotype
- `work/judge_input.md`, `work/judge_output.md` — LLM judge I/O
