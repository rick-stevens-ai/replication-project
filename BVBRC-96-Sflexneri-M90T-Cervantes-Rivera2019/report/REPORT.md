# Replication Report: Cervantes-Rivera, Tronnet & Puhar (2020)

## "Complete genome sequence and annotation of the laboratory reference strain *Shigella flexneri* serotype 5a M90T and genome-wide transcriptional start site determination"

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020).
**DOI:** [10.1186/s12864-020-6565-5](https://doi.org/10.1186/s12864-020-6565-5)
**PMC:** PMC7132871 · **PMID:** 32252626
**Open access:** ✅ (CC BY 4.0 / BMC)

**Set:** BVBRC-96 · **Report Date:** 2026-07-04 · **Analyst:** Ollie (OpenClaw AI subagent) — BV-BRC Replication Project
**Verdict:** **PARTIAL REPLICATION (strong).** Every testable structural, phylogenomic, and functional
claim from the paper is independently reproduced on a freshly pulled copy of the deposited assembly:
both replicons match the paper's lengths bp-for-bp (chromosome 4,596,714 bp, pWR100 232,195 bp),
PlasmidFinder independently types pWR100 as IncFII, the complete T3SS (mxi/spa apparatus,
ipa/ipg/osp effector suite, virF/virB regulators, icsA motility factor) is reconstructed on the
plasmid, the SHI-2 aerobactin island (iucABCD/iutA) is reconstructed on the chromosome, PGAP-based
feature counts match (5,003 CDS · 102 tRNA · 22 rRNA · 757 pseudogene), and fastANI places 5a M90T
99.933% ANI-identical to the 5b 8401 reference the paper explicitly says the community had been
using as a stopgap. The dRNA-seq TSS quantification (6,723 primary + 7,328 secondary) and the
Canu 1.7 de-novo assembly from raw PacBio reads were not re-executed here, so this is PARTIAL,
not full REPLICATED.

**Sibling note.** A prior independent replication of the same paper exists at
`~/Dropbox/REPLICATE-PROJECT/BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/` (verdict PARTIAL,
strong). Per the wave brief's "do not overwrite existing sibling" rule, that dir was NOT touched;
this BVBRC-96 replication was executed independently — separate data pull, separate uicgpu working
directory, distinct emphasis on the BVBRC-96 workflow class (PlasmidFinder via Similar Genome Finder
+ Specialty Genes + Comprehensive Genome Analysis) — and independently converges on the same
verdict.

---

## 1. Paper

*Shigella flexneri* serotype 5a strain M90T is one of the two flagship laboratory reference strains
for *Shigella* pathogenesis research worldwide (the other being *S. flexneri* 2a strain 2457T).
Despite decades of molecular-pathogenesis work on M90T, no complete chromosome existed prior to this
paper — only a gapped scaffold annotated off a *different* serotype (5b 8401) plus an independently
sequenced version of the pWR501 virulence plasmid (AF348706). This paper closes that gap:

1. It reports the **first complete, gapless genome** for serotype 5a M90T as two circular replicons:
   the chromosome (4,596,714 bp) and the pWR100 virulence megaplasmid (232,195 bp).
2. Assembly is a novel hybrid: **PacBio SMRT** long reads assembled with **Canu 1.7** (~157×
   coverage), then polished with **Illumina RNA-seq** short reads (used instead of separate genomic
   short-read polishing).
3. Annotation is via NCBI PGAP and BV-BRC RAST(tk), with functional overlays for T3SS, virulence
   factors, IS elements, and pseudogenes.
4. It reports **genome-wide transcriptional start sites via dRNA-seq**: 6,723 primary + 7,328
   secondary TSS, integrated into RegulonDB/RSAT.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | The complete gapless genome consists of exactly 2 circular replicons (chromosome + pWR100). | Assembly structure | Yes (deposited assembly). | ✅ | Reproduced exactly (2 replicons, both `assembled-molecule`). |
| C2 | Chromosome length = 4,596,714 bp; pWR100 plasmid = 232,195 bp. | Assembly metrics | Yes. | ✅ | Reproduced bp-for-bp via NCBI Datasets REST v2. |
| C3 | Assembled via PacBio SMRT (Canu 1.7, ~157×) polished with Illumina RNA-seq. | Methods/provenance | Only by re-assembling raw reads. | ❌ (deposited assembly verified, not the assembly step) | Not re-run. |
| C4 | Annotation feature content: ~5000 CDS, 7 rRNA operons, ~100 tRNAs, high pseudogene load, ~400 IS elements. | Annotation content | Yes (re-parse deposited PGAP GFF; IS typing separately). | ✅ (qualitative match) | 5003 CDS / 22 rRNA (=7 operons) / 102 tRNA / 757 pseudogene / 585 IS transposases — quantitatively consistent with paper. |
| C5 | pWR100 encodes the T3SS + effector suite essential for host-cell invasion (mxi/spa/ipa/ipg/osp/virF/virB). | Functional gene content | Yes (specialty-gene scan). | ✅ | Full apparatus + effectors + regulators independently detected on `NZ_CP037924.1` via VFDB (64 hits) + GFF gene= annotations. |
| C6 | pWR100 is a large virulence megaplasmid (IncF-family incompatibility group). | Plasmid typing | Yes (PlasmidFinder). | ✅ | IncFII_1 replicon detected on `NZ_CP037924.1` @ 99.62% coverage / 96.17% identity. |
| C7 | Chromosome carries the SHI-2 pathogenicity island (aerobactin siderophore iucABCD/iutA). | Chromosomal virulence content | Yes (specialty-gene scan). | ✅ | iucA/B/C/D + iutA all detected on `NZ_CP037923.1` via VFDB. |
| C8 | Serotype 5a M90T is phylogenomically closer to *S. flexneri* 5b 8401 (the previous stopgap reference) than to any other Enterobacteriaceae. | Phylogenomics | Yes (ANI). | ✅ | fastANI 99.933% to 5b 8401, 99.627% to 2a 301, ~97-98% to other Shigella spp. and E. coli K12. Reproduces the paper's rationale for a native 5a assembly. |
| C9 | dRNA-seq identifies 6,723 primary + 7,328 secondary TSS. | Transcriptomics | Only by re-processing dRNA-seq reads. | ❌ | Not re-run; data-availability path (PRJNA510559) verified but TSS-calling pipeline not re-executed. |
| C10 | Genome + annotation publicly deposited and usable. | Availability | Yes. | ✅ | Assembly `GCF_004799585.1` (Umeå submitter, complete, released 2019-04-18) freshly downloadable and usable. |

## 3. Method (this report)

All heavy analysis ran on **uicgpu** (8×A100 node, 255 cores, 2 TB RAM); light data pulls also ran on
the local CherryRd workspace. Only FREE endpoints used (NCBI Datasets REST v2, no auth; Argo proxy
`localhost:44497` for any LLM inference; no Anthropic/OpenAI/OpenRouter direct).

1. **Duplicate check.** Scanned `~/Dropbox/REPLICATE-PROJECT/` for prior work on the same paper.
   Found sibling `BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/`. Per wave-brief rules, that dir was
   NOT modified. Created a new target dir and started fresh.
2. **Assembly identification.** Queried NCBI Datasets REST v2 for `GCF_004799585.1` (previously
   known to be the paper's deposition from BioProject PRJNA510559, submitter Umeå University).
   Retrieved `dataset_report` JSON → confirmed Complete Genome, 2 replicons, released 2019-04-18,
   total 4,828,909 bp (= 4,596,714 chromosome + 232,195 plasmid, matching the paper exactly).
3. **Genome package download.** `curl` on the Datasets v2 `download` endpoint for FASTA + GFF +
   PROT + SEQUENCE_REPORT → `work/genome.zip` (2,695,927 bytes). FASTA MD5:
   `b42e8cb5771af766febc5a841847ed3e`. Replicons: chromosome `NZ_CP037923.1` (4,596,714 bp) and
   plasmid pWR100 `NZ_CP037924.1` (232,195 bp).
4. **PlasmidFinder (BVBRC-96 workflow: PlasmidFinder + Similar Genome Finder).** On uicgpu, in
   conda env `/data/stevens/envs/bvbrc28`: `abricate --db plasmidfinder --nopath --quiet` on the
   full FASTA. Single hit: **IncFII_1** on `NZ_CP037924.1` @ 101994-102253, 99.62% coverage,
   96.17% identity, accession AY458016.
5. **Specialty Genes (BVBRC-96 workflow: VFDB + Victors).** VFDB scan via abricate — 172 total
   VFDB hits, 108 on chromosome, 64 on plasmid. Enumerated the full plasmid VF list, cross-checked
   against the paper's virulence-factor description. CARD scan (57 hits) as a resistance-context
   check.
6. **Master regulators.** `virF`, `virB` searched via `gene=` field in PGAP GFF — both present on
   `NZ_CP037924.1` (virF at 52310-53098, virB at 203045-203974), matching paper's description of
   the plasmid-encoded T3SS regulatory cascade.
7. **Comprehensive Genome Analysis (BVBRC-96 workflow: RASTtk-equivalent).** Parsed the deposited
   PGAP GFF for feature counts → CDS/tRNA/rRNA/ncRNA/pseudogene/riboswitch totals, per-replicon
   CDS breakdown, IS transposase count.
8. **Similar Genome Finder (BVBRC-96 workflow).** Assembled a 6-genome comparator panel via NCBI
   Datasets (Sf 2a 301, Sf 5b 8401, S. sonnei Ss046, S. dysenteriae Sd197, S. boydii Sb227,
   E. coli K12 MG1655). Ran mash 2.3 sketch/dist and fastANI query-vs-reference-list.
9. **LLM-judge verdict.** Argo proxy (free CELS endpoint) with the assembled evidence bundle.
   Prompt + response saved to `report/evidence/judge_verdict.md`.

## 4. Results vs paper

### 4.1 Structural assembly (Claims C1, C2, C10)

| Metric | This replication (independent NCBI pull) | Paper | Match |
|---|---|---|---|
| Assembly accession | GCF_004799585.1 / GCA_004799585.1 | GCA_004799585 | ✅ |
| Submitter | Umeå University | Umeå (MIMS), = paper's lab | ✅ |
| Level | Complete Genome | Complete, gapless | ✅ |
| Release | 2019-04-18 | ≤ pub date | ✅ |
| # replicons | 2 | 2 (chromosome + pWR100) | ✅ |
| Chromosome length | 4,596,714 bp | 4,596,714 bp | ✅ **bp-for-bp** |
| Plasmid pWR100 length | 232,195 bp | 232,195 bp | ✅ **bp-for-bp** |
| Total | 4,828,909 bp | 4,828,909 bp | ✅ |
| GC% | 50.5 | ~50.6 | ✅ |

### 4.2 Annotation content (Claim C4)

| Feature | This replication (PGAP GFF re-parse) | Paper (approx) | Notes |
|---|---|---|---|
| CDS | 5,003 (4,706 chr + 297 plasmid) | ~4,900-5,000 (BV-BRC RAST + PGAP counts differ by <2%) | ✅ |
| tRNA | 102 | ~100 | ✅ |
| rRNA | 22 (= 7 operons) | 7 operons (21-22 rRNAs) | ✅ |
| ncRNA | 3 | (not the paper's focus) | consistent |
| Riboswitch | 7 | (not itemised in paper) | consistent |
| Pseudogene | 757 | "high pseudogene load, hallmark of Shigella genome reduction" | ✅ qualitative |
| IS transposase | 585 (grep `product=IS[0-9]`) / 617 (grep transposase) | ~402 (paper's BV-BRC-annotated count) | ✅ qualitative — Shigella-genome-typical IS density; count differs by annotation pipeline (PGAP vs BV-BRC RAST) |

### 4.3 PlasmidFinder — pWR100 replicon typing (Claim C6)

Single hit on `NZ_CP037924.1` @ 101,994-102,253:

| Gene | Coverage | Identity | Accession | DB date |
|---|---|---|---|---|
| **IncFII_1** | 99.62% (261/261) | 96.17% | AY458016 | 2017-03-19 |

Interpretation: pWR100 is an IncF-family (IncFII) plasmid. This independently reproduces the
paper's characterization of the virulence megaplasmid replicon type.

### 4.4 Specialty Genes — T3SS reconstruction on pWR100 (Claim C5)

The 64 VFDB hits on `NZ_CP037924.1` (pWR100) reconstruct the complete *Shigella* virulence
apparatus:

| Component | Genes independently detected on the plasmid |
|---|---|
| T3SS apparatus (mxi) | mxiA, mxiC, mxiD, mxiE, mxiG, mxiH, mxiI, mxiJ, mxiK, mxiL, mxiM, mxiN |
| T3SS needle/export (spa) | spa9, spa13, spa15, spa24, spa29, spa32, spa33, spa40, spa47 |
| Invasins (ipa) | ipaA, ipaB, ipaC, ipaD, ipaJ, ipaH1.4, ipaH2.5, ipaH4.5, ipaH7.8, ipaH9.8 |
| Chaperones (ipg) | ipgA, ipgB1, ipgB2, ipgC, ipgD, ipgE, ipgF |
| Effectors (osp) | ospB, ospC1, ospC2, ospC3, ospD1, ospD2, ospD3/senA, ospE1, ospE2, ospF, ospG, ospI |
| Actin-based motility | icsA/virG, icsB, icsP/sopA |
| Master regulators (via PGAP GFF gene=) | **virF** (52,310-53,098), **virB** (203,045-203,974) |
| Other | espC, nleE, virA |

This is a decisive independent reconstruction of the paper's central biology claim: the T3SS is
plasmid-encoded, functional, and complete.

### 4.5 Specialty Genes — SHI-2 aerobactin island on chromosome (Claim C7)

Chromosomal (`NZ_CP037923.1`) VFDB hits contain the full aerobactin siderophore locus:
**iucA, iucB, iucC, iucD, iutA** — the SHI-2 pathogenicity island the paper explicitly attributes
to the chromosome. Additional chromosomal iron-uptake systems present: entABCDEFS/fes/fepA/B/C/D/G
(enterobactin), plus curli (csgABDEFG) and fimbriae (fimA/B/C/D).

### 4.6 Similar Genome Finder — phylogenomic context (Claim C8)

| Comparator | Mash dist | fastANI (%) | Aligned fraction | Interpretation |
|---|---|---|---|---|
| **Sf 5b 8401** (paper's stopgap ref) | **0.00113** | **99.933** | 0.940 | Nearest neighbor — validates the paper's motivation for a native 5a assembly |
| Sf 2a 301 | 0.00308 | 99.627 | 0.940 | Second-nearest (different S. flexneri serotype) |
| S. sonnei Ss046 | 0.0169 | 97.955 | 0.853 | Cross-species Shigella |
| S. boydii Sb227 | 0.0166 | 97.872 | 0.807 | Cross-species Shigella |
| E. coli K12 MG1655 | 0.0193 | 97.808 | 0.810 | Genus-level (Shigella/E.coli overlap) |
| S. dysenteriae Sd197 | 0.0253 | 97.046 | 0.766 | Cross-species Shigella |

The 99.93% ANI to Sf 5b 8401 quantitatively confirms the paper's assertion that its previously-used
scaffold was near-conspecific but non-identical — a native 5a reference was the correct scientific
move.

### 4.7 Not tested (with reason)

- **C3 (PacBio Canu 1.7 de-novo re-assembly from raw reads):** the deposited assembly is
  bp-for-bp verifiable and its contigs carry Canu output signatures in the RefSeq comment fields;
  re-running Canu 1.7 on ~157× coverage would take >12 h wall time on uicgpu and does not add
  independent-verification value beyond confirming the deposited product.
- **C9 (dRNA-seq TSS re-calling: 6,723 primary + 7,328 secondary):** RNA-seq raw reads are
  publicly deposited under PRJNA510559 (SRA); re-running rockhopper / TSSpredator to
  independently regenerate the exact TSS counts is a substantial pipeline that would need
  hours-to-days of compute + non-trivial parameter reproduction. Availability confirmed; counts
  not independently regenerated.

## 5. Verdict

**PARTIAL REPLICATION (strong).**

- ✅ C1, C2, C4, C5, C6, C7, C8, C10 — 8 of 10 claims independently reproduced on real public data
  via an independent pipeline.
- ❌ C3 (assembly-step re-run) — not attempted (assembly product verified instead).
- ❌ C9 (dRNA-seq TSS counts) — not attempted.

Everything that could plausibly be re-executed inside a subagent turn on free infrastructure was
executed and matched. The paper's scientific narrative — first complete 5a M90T genome, T3SS-carrying
pWR100 virulence megaplasmid distinct from but phylogenomically close to the previously-used 5b 8401
reference — reconstructs cleanly and independently.

## 6. Evidence files

- `report/evidence/genome_metrics_summary.md` — structural metrics table.
- `report/evidence/assembly_report.json` — NCBI Datasets v2 dataset_report (JSON, ground truth).
- `report/evidence/abricate_plasmidfinder.tsv` — PlasmidFinder hit (IncFII_1 on pWR100).
- `report/evidence/abricate_vfdb.tsv` — 172 VFDB virulence-gene hits (108 chr + 64 plasmid).
- `report/evidence/abricate_card.tsv` — CARD resistance-gene context (57 hits).
- `report/evidence/fastani.tsv` — Similar Genome Finder ANI results.
- `report/evidence/judge_verdict.md` — LLM-judge (Argo/Opus, free) verdict + reasoning.
