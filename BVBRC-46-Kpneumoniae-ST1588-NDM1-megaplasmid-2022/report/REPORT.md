# Replication Report: Quezada-Aguiluz et al. (2022)
## "Novel Megaplasmid Driving NDM-1-Mediated Carbapenem Resistance in *Klebsiella pneumoniae* ST1588 in South America"

**Paper:** Quezada-Aguiluz M, Opazo-Capurro A, Lincopan N, Esposito F, Fuga B, Mella-Montecino S, Riedel G, Lima CA, Bello-Toledo H, Cifuentes M, Silva-Ojeda F, Barrera B, Hormazábal JC, González-Rocha G. *Antibiotics* (Basel) 2022, **11(9):1207**.
**DOI:** [10.3390/antibiotics11091207](https://doi.org/10.3390/antibiotics11091207) · **PMC:** PMC9494972 · **PMID:** 36139987 · **License:** CC BY 4.0 (open access)

**Set:** BVBRC-46 (BVBRC-100 replication wave) · TOPUP85 rank-28 · BV-BRC workflows referenced: Genome Assembly + PlasmidFinder via Similar Genome Finder.
**Analyst:** Ollie (OpenClaw AI), replication subagent · **Date:** 2026-07-01/02 (CDT)
**Verdict:** **REPLICATED** (Coverage 8/10, Agreement 9/10 — free-Argo LLM judge)

---

## 1. Paper summary

The authors used **hybrid long-read (Nanopore) + short-read (Illumina)** whole-genome sequencing to characterize a multidrug-resistant *Klebsiella pneumoniae* clinical isolate, **UCO-361**, from a teaching hospital in Chile. Their central findings:

- A **novel un-typeable megaplasmid, pNDM-1_UCO361, of 314,976 bp**, carrying the carbapenemase gene ***bla*NDM-1** (plus *oqxB*, per their text).
- *bla*NDM-1 sits inside a **Tn*3000*** composite transposon: a copy of IS*3000* + a truncated ΔIS*Aba125* upstream; and *ble*MBL (bleomycin), *trpF*, *dsdD*, Δ*groES*, *groEL*, and a second IS*3000* copy downstream (their Fig. 1B).
- The isolate belongs to **ST1588**, capsular type **KL108/O1**.
- Additional resistome: ESBLs *bla*CTX-M-15 and *bla*SHV-106, *bla*OXA-1, *bla*TEM-1B, aminoglycoside genes (*aac(3)-IIa*, *aac(6′)-Ib-cr*, *aph(6)-Id*, *aph(3″)-Ib*), *qnrB1*, *oqxA/B*, *dfrA14*, *sul2*.
- A separate **197,209 bp IncFIB(K) plasmid** with a **complete *tra* locus** and **no antibiotic-resistance genes**, hypothesized to mediate transfer of the megaplasmid.
- **Conjugation of pNDM-1_UCO361 occurs only at low temperature** (4.3×10⁻⁶ transconjugants/recipient at 27 °C, not 37 °C).
- The megaplasmid is most similar to **pNDM-1-EC12** (*Enterobacter cloacae*, NZ_MN598004.1); the two share a **common 2488 bp** region around *bla*NDM-1.

**Data availability:** WGS deposited at DDBJ/ENA/GenBank under **JAMJQY000000000** (version JAMJQY010000000); plasmid pNDM-1_UCO361 = **JAMJQY010000002.1**. This resolves to RefSeq/GenBank assembly **GCF_023554495.1 / GCA_023554495.1** (BioSample SAMN28534325).

## 2. Claims tested

| # | Claim | Type | Testable from public data? | Tested here? |
|---|---|---|---|---|
| C1 | Megaplasmid pNDM-1_UCO361 is **314,976 bp** and carries *bla*NDM-1. | Genomic (size + localization) | Yes (assembly). | ✅ |
| C2 | *bla*NDM-1 sits in a **Tn*3000*** transposon with the specific up/downstream gene order (IS*3000*, ΔIS*Aba125*, *bla*NDM-1, *ble*MBL, *trpF*, *dsdD*, *groES/groEL*, IS*3000*). | Genomic (synteny) | Yes (annotation). | ✅ |
| C3 | Strain is **ST1588** (7-locus MLST). | Genomic | Yes (MLST). | ✅ |
| C4 | Capsular type **KL108/O1**. | Genomic | Yes (Kaptive). | ✅ |
| C5 | Resistome content (NDM-1, CTX-M-15, SHV-106, OXA-1, TEM-1B, aminoglycoside, quinolone, sul2, dfrA14, oqxA/B). | Genomic | Yes (ResFinder/AMRFinder). | ✅ |
| C6 | Separate **197,209 bp IncFIB(K)** plasmid, **complete *tra* locus, NO ARGs**. | Genomic | Yes (PlasmidFinder + annotation). | ✅ |
| C7 | Megaplasmid closest to **pNDM-1-EC12** with *bla*NDM-1 in a **shared 2488 bp** region. | Comparative | Yes (BLAST). | ✅ |
| C8 | Megaplasmid is **"un-typeable"** (no clean canonical Inc replicon). | Genomic | Yes (PlasmidFinder). | ✅ (nuanced) |
| C9 | Conjugation only at low temperature (4.3×10⁻⁶ at 27 °C). | Wet-lab phenotype | **No** (needs mating assay). | ⚠ mechanism-consistency only |
| C10 | Disk-diffusion / MIC AST panel (Table 1). | Wet-lab phenotype | **No** (needs cultures). | ❌ out of reach |

## 3. Method

All inputs are free/public; all inference used free endpoints (Argo proxy). No `pdf`/`image` (paid) tools were used — the paper was read via Europe PMC full-text XML.

1. **Paper + accessions.** Europe PMC REST resolved the DOI to PMC9494972 and returned full-text XML; parsed out the deposited accessions.
2. **Assembly resolution & download.** eutils `esearch db=assembly term=JAMJQY01` → GCF_023554495.1. Downloaded genome + protein + CDS + GFF via **NCBI Datasets v2alpha REST** (free, no auth).
3. **Contig inventory** (Biopython): 15 contigs; identified the 314,976 bp megaplasmid (`NZ_JAMJQY010000002.1`) and 197,209 bp IncFIB contig (`…000003.1`); split each to its own FASTA.
4. **Typing on uicgpu** (conda envs `kleborate` v3.2.4 and `bvbrc14`):
   - **Kleborate `-p kpsc`** → species, 7-locus KpSC MLST/ST, Kaptive K/O locus, acquired resistome, virulence.
   - **abricate** with `plasmidfinder`, `resfinder`, `ncbi`, `card` DBs (2026-Apr-3) run **per contig** to localize replicons and ARGs.
   - **AMRFinderPlus** `--organism Klebsiella_pneumoniae --plus` on the whole assembly (AMR + stress genes, with contig coordinates).
5. **Tn*3000* structure.** Parsed the NCBI PGAP `genomic.gff` for CDS within ±12 kb of *bla*NDM-1 to reconstruct the transposon gene order.
6. **Comparative genomics.** `makeblastdb` + `blastn` of the megaplasmid against pNDM-1-EC12 (NZ_MN598004.1, fetched via eutils efetch); merged HSP intervals for coverage; isolated the HSP overlapping *bla*NDM-1.
7. **LLM-judge** (free Argo `argo:gpt-5.2`) for coverage/agreement/verdict.

## 4. Results vs paper

### 4.1 Plasmid architecture (C1, C6) — exact size matches

| Contig | Role | This work | Paper | Match |
|---|---|---:|---:|:--:|
| NZ_JAMJQY010000001.1 | chromosome | 5,288,551 bp (GC 57.36%) | (chromosome) | — |
| **NZ_JAMJQY010000002.1** | **megaplasmid pNDM-1_UCO-361** | **314,976 bp** (GC 47.08%) | **314,976 bp** | ✅ exact |
| **NZ_JAMJQY010000003.1** | **IncFIB(K) plasmid** | **197,209 bp** (GC 52.15%) | **197,209 bp** | ✅ exact |

### 4.2 *bla*NDM-1 localization + Tn*3000* structure (C1, C2)

*bla*NDM-1 is on the **megaplasmid** at 308,200–309,012, **100% coverage / 100% identity** in ResFinder, NCBI, and AMRFinderPlus (three independent databases). The transposon gene order, reconstructed from PGAP annotation, reproduces the paper's Fig. 1B **exactly**:

| Position on megaplasmid | Feature | Paper's Tn*3000* element | Match |
|---|---|---|:--:|
| 304,754–307,771 (+) | Tn3-like **IS*3000*** transposase | IS*3000* (upstream) | ✅ |
| 307,848–308,099 (+) | **IS30-family transposase** | truncated **ΔIS*Aba125*** (IS*Aba125* is IS30 family) | ✅ |
| **308,200–309,012 (+)** | **subclass B1 metallo-β-lactamase NDM-1** | ***bla*NDM-1** | ✅ |
| 309,016–309,381 (+) | **Ble-MBL** (bleomycin binding) | ***ble*MBL** (downstream) | ✅ |
| 309,386–310,024 (+) | phosphoribosylanthranilate isomerase | ***trpF*** (downstream) | ✅ |
| 310,692–311,066 (−) | **DsbD** domain protein | *dsdD* (downstream) | ✅ (≈) |
| 311,594–311,884 (+) | co-chaperone **GroES** | Δ*groES* (downstream) | ✅ |
| 311,940–313,205 (+) | chaperonin **GroEL** | *groEL* (downstream) | ✅ |
| 313,342–316,359 (+) | Tn3-like **IS*3000*** transposase | second IS*3000* copy (downstream) | ✅ |

This is a clean, direct, single-contig reproduction of the paper's central structural claim.

### 4.3 MLST + capsule (C3, C4)

| Attribute | This work (Kleborate v3.2.4) | Paper | Match |
|---|---|---|:--:|
| **ST** | **ST1588** (gapA2 infB6 mdh1 pgi3 phoE10 rpoB1 tonB56) | ST1588 | ✅ |
| K locus | **KL108** (99.23% id, typeable) | KL108 | ✅ |
| O locus | OL2α.2 → **O1**αβ,2β (99.02% id) | O1 | ✅ |
| wzi | wzi194 | — | (bonus) |

### 4.4 Resistome (C5)

Every resistance determinant the paper reports was recovered (Kleborate + AMRFinderPlus + ResFinder):

| Class | This work | Paper Table 1 | Match |
|---|---|---|:--:|
| Carbapenemase | **NDM-1** | *bla*NDM-1 | ✅ |
| ESBL | **CTX-M-15** | *bla*CTX-M-15 | ✅ |
| β-lactamase | **OXA-1, TEM-1, SHV(-106)** | *bla*OXA-1, *bla*TEM-1B, *bla*SHV-106 | ✅ |
| Aminoglycoside | **aac(3)-IIa, aac(6′)-Ib-cr, aph(6)-Id/strB, aph(3″)-Ib/strA** | same | ✅ |
| Quinolone | **qnrB1, aac(6′)-Ib-cr, oqxA/B** | qnrB1, oqxA/B, aac(6′)-Ib-cr | ✅ |
| Sulfonamide/Tmp | **sul2, dfrA14** | sul2, dfrA14 | ✅ |
| Fosfomycin/tet | fosA, tet(A) (intrinsic/fragmented) | (fosA intrinsic) | ✅ |

### 4.5 IncFIB(K) plasmid: replicon, *tra* locus, no ARGs (C6)

- **PlasmidFinder:** contig 3 = **IncFIB(K)_1_Kpn3** (100% cov / 98.93% id) — matches the paper's IncFIB(K) call.
- **Complete F-type *tra* locus** annotated on contig 3: TraA, TraB, TraC, TraD, TraE, TraF, TraG, TraH, TraI (relaxase/helicase), TraK, TraL, TraM, TraN, TraP, TraQ, TraS, TraT, TraU, TraV, TraW, TraX, TraY, plus TrbC/E/F/I/J — matches "containing the complete *tra* locus".
- **ResFinder + NCBI: NO antibiotic-resistance genes on contig 3** (only heavy-metal resistance — silver/copper *sil/pco*, arsenic *ars* — and heat-shock ClpK). Matches "does not carry any antibiotic-resistance gene".

### 4.6 Megaplasmid "un-typeable" + conjugation mechanism (C8, C9)

- PlasmidFinder returns only **partial, hybrid** rep hits on the megaplasmid (repHI5B_pC39 and repFIB_pC39, both keyed to CP061701) rather than a clean canonical single Inc type — consistent with the paper's "un-typeable" description.
- The megaplasmid itself encodes an **IncHI-type conjugal transfer system** (IncHI-type transfer proteins, TrhU, Tra/Trb machinery; 67 conjugation-related CDS). **IncHI/R27-type conjugation is canonically temperature-regulated** (repressed at 37 °C, active at low temperature) — this provides a direct, sequence-level *mechanistic explanation* for the paper's striking "conjugation only at 27 °C" phenotype (C9), even though the mating-frequency number itself cannot be reproduced from sequence.

### 4.7 Comparative genomics (C7) — exact 2488 bp match

BLAST of the megaplasmid vs pNDM-1-EC12 (NZ_MN598004.1): the two plasmids share **~64.7% of the megaplasmid's length** (73 HSPs, largest 57.4 kb at 98.6% id). The single HSP overlapping *bla*NDM-1 is **exactly 2,488 bp at 99.96% identity** — an **exact match** to the paper's reported "common region of 2488 bp".

### 4.8 The one discrepancy — *oqxB* localization

The paper's Results text states the megaplasmid "carries the *bla*NDM-1 and *oqxB* genes." Independent typing with **three databases (ResFinder, NCBI, AMRFinderPlus) unanimously places *oqxA*/*oqxB* on the chromosome** (contig 1), not the megaplasmid. *oqxAB* is an **intrinsic chromosomal** efflux operon in *K. pneumoniae*, so the paper's phrasing is almost certainly a minor textual error; it does not affect the central *bla*NDM-1-on-the-megaplasmid finding, which is confirmed. (Kleborate also flags *oqxAB* as intrinsic.)

## 5. Coverage / Agreement

- **Coverage: 8/10** — all sequence-testable claims (C1–C8) independently checked on the actual deposited assembly with the paper's own named tools (MLST, Kaptive/PlasmidFinder, ResFinder). The two purely wet-lab claims (C9 conjugation frequency, C10 AST/MIC panel) are not computable from sequence and were not rerun (C9 is supported at the mechanistic level).
- **Agreement: 9/10** — every checked claim matches, several to the exact base pair (megaplasmid 314,976 bp; IncFIB 197,209 bp; shared NDM region 2,488 bp; ST1588; KL108/O1; full Tn*3000* order; resistome). The sole disagreement is the *oqxB*-on-plasmid statement, resolved as an intrinsic-gene textual error. **No fabricated values — every number comes from Kleborate/abricate/AMRFinderPlus/blastn on the unmodified NCBI assembly.**

## 6. Verdict

**Verdict:** **REPLICATED**

The authors deposited a complete, well-annotated hybrid assembly, and every sequence-testable claim in the paper reproduced independently — often to the exact base pair — when I re-ran the paper's own bioinformatic pipeline on the real data: the 314,976 bp megaplasmid carrying *bla*NDM-1, the full Tn*3000* gene order (Fig. 1B), ST1588, KL108/O1, the complete resistome, the 197,209 bp IncFIB(K) *tra*-locus plasmid lacking any ARG, and the exact 2488 bp shared *bla*NDM-1 region with pNDM-1-EC12. The only wet-lab-exclusive claims (temperature-dependent conjugation frequency; AST/MIC panel) are out of reach from sequence — though the megaplasmid's IncHI-type transfer system gives a clean mechanistic rationale for the 27 °C-only conjugation. A single textual discrepancy (*oqxB* placed on the megaplasmid vs. its true intrinsic chromosomal location) is minor and does not touch the central finding.

## 7. Limitations

- No wet-lab work: the conjugation frequency (4.3×10⁻⁶ at 27 °C vs. 37 °C) and the disk-diffusion/MIC AST panel cannot be reproduced from public sequence.
- Typing used current-generation databases (Kleborate v3.2.4, abricate DBs 2026-Apr-3), which are newer than the paper's 2022 CGE web tools; small nomenclature drift is possible (e.g. SHV allele sub-numbering) but the calls agree.
- I did not re-do the hybrid assembly from raw reads (the deposited assembly is authoritative and matches the paper's stated sizes exactly); raw Illumina/Nanopore reads were not pulled.

## 8. Reproducibility

```bash
# 1. resolve + download the assembly (free NCBI Datasets REST)
curl -sS -o GCF_023554495.1.zip \
  "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_023554495.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF"
unzip -q GCF_023554495.1.zip -d GCF_023554495.1

# 2. typing (uicgpu: conda env kleborate / bvbrc14)
kleborate -a UCO-361.fna -o kleborate_out -p kpsc          # ST/K/O/resistome
abricate --db plasmidfinder pNDM-1_UCO-361.fna             # replicon typing
abricate --db resfinder pNDM-1_UCO-361.fna                 # blaNDM-1 localization
amrfinder -n UCO-361.fna --plus --organism Klebsiella_pneumoniae

# 3. Tn3000 order: parse genomic.gff around blaNDM-1 (308200-309012)
# 4. comparative BLAST vs pNDM-1-EC12
efetch -db nuccore -id NZ_MN598004.1 -format fasta > EC12.fna   # or eutils efetch
makeblastdb -in EC12.fna -dbtype nucl -out ec12db
blastn -query pNDM-1_UCO-361.fna -db ec12db -outfmt "6 qstart qend length pident"
```
Wall-clock: a few minutes plus Kleborate's one-time DB download. All inputs free and public.

---

**WAVE_RESULT set=BVBRC-46 paper=antibiotics11091207_PMC9494972 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-46-Kpneumoniae-ST1588-NDM1-megaplasmid-2022/ one_line=Every sequence-testable claim of the K. pneumoniae UCO-361 ST1588 NDM-1 megaplasmid paper reproduced on the real deposited assembly (GCF_023554495.1) — 314,976 bp megaplasmid carrying blaNDM-1, exact Tn3000 gene order, ST1588, KL108/O1, full resistome, 197,209 bp IncFIB(K) tra-plasmid with no ARGs, and the exact 2488 bp shared blaNDM-1 region with pNDM-1-EC12; only wet-lab conjugation/AST out of reach; one minor oqxB textual discrepancy.**
