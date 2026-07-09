# Independent Replication — Guan et al. 2022, *Olsenella intestinalis* sp. nov.

**Set / rank:** BVBRC / 61 · **PMID:** 35689096 · **DOI:** 10.1007/s00203-022-03017-2
**Journal:** *Archives of Microbiology* 204:384 (2022) · **Cites:** 3 (as of task assignment)
**Replication verdict: PARTIAL** — every core taxonomic/genomic claim we could independently test on public data was reproduced; ANI magnitude differs from the paper's tool but not its qualitative conclusion; some paper-internal inconsistencies were exposed; phenotypic claims are out-of-reach without the live isolate.

## 1. Paper summary

The paper describes a single novel bacterium, strain **BGYT1ᵀ** (= KCTC 25379ᵀ = GDMCC 1.3011ᵀ), isolated from cow feces (Andong, Republic of Korea). It uses a **polyphasic taxonomy** approach: 16S rRNA phylogeny, whole-genome sequencing (Illumina + Oxford Nanopore) and TYGS/GBDP phylogenomics, plus classical wet-lab morphology / physiology / biochemistry / chemotaxonomy. Based on the combined evidence, the authors propose **Olsenella intestinalis sp. nov.** with BGYT1ᵀ as the type strain.

The BV-BRC pipeline analog is **Codon Tree / Phylogenetic Tree** on the newly-sequenced genome plus reference *Olsenella* type strains — i.e., a genome-based phylogenetic placement of a novel species announcement. This falls in the class of "complete-genome announcement" papers where the primary artifact IS the deposited assembly + 16S sequence.

## 2. Claims table

| # | Claim (paper) | Type | Testable from public data? | Tested? | Verdict |
|---|---|---|---|---|---|
| C1 | Genome length = 2,476,083 bp (abstract) / 2,453,694 bp (body) | Quantitative | Yes | Yes | **REPLICATED** for the body value (2,453,694 bp — exact match to NCBI + our recount); **CONTRADICTS** the abstract value (paper-internal typo) |
| C2 | G+C content = 66.9 mol% | Quantitative | Yes | Yes | **REPLICATED** (our value 66.95%) |
| C3 | 8 contigs | Quantitative | Yes | Yes | **PARTIAL** — current GenBank/RefSeq assembly = 2 contigs; NCBI-level cleanup vs. paper's original |
| C4 | N50 = 604,117 bp | Quantitative | Yes | Yes | **PARTIAL** — reflects the 8-contig paper number; NCBI's 2-contig N50 = 1,425,513 bp |
| C5 | 1835 genes / 1778 CDS / 50 tRNAs / 6 rRNAs (5S,16S,23S) / 1 tmRNA / 2 BGCs | Quantitative | Yes | Yes | **REPLICATED** within re-annotation drift: current PGAP v6.11 (2026-05-18) reports 1810 genes / 1761 CDS / 49 tRNAs / 6 rRNAs / 1 tmRNA; BGCs not directly counted in PGAP |
| C6 | Closest 16S neighbor = *O. umbonata* KCTC 15140ᵀ at 98.2% (abstract) / 98.24% (body) | Quantitative | Yes | Yes | **REPLICATED** — our pairwise identity 98.38% (aln-based) / 98.45% (nogap) |
| C7 | ANI to closest = 76.8% | Quantitative | Yes | Yes | **PARTIAL** — fastANI 80.83%, skani 79.43%, our ANIb 83.36% — all clearly below 95% species boundary (qualitative claim confirmed) but paper's magnitude appears low relative to modern tools |
| C8 | AAI to *O. umbonata* = 67.3% | Quantitative | Yes | **No** | **NOT_TESTED** (deferred; heavier all-vs-all BLASTp) |
| C9 | dDDH to *O. umbonata* = 22.2% | Quantitative | Yes (via GGDC) | **No** | **NOT_TESTED** (GGDC is web-only submission) |
| C10 | Novel species classification (below all species thresholds) | Qualitative | Yes | Yes | **REPLICATED** — every metric we computed is far below species threshold |
| C11 | Phylogenetic placement within genus *Olsenella*, sister to *O. umbonata* | Qualitative | Yes | Yes | **REPLICATED** — our NJ tree of 13 type strains puts BGYT1 in a clade with *O. umbonata* + *O. profusa* |
| C12 | Cell-wall-degrading enzyme genes: chitinases, β-1,3-glucanases, proteases | Presence | Yes (annotation grep) | Yes | **PARTIAL** — proteases/peptidases confirmed (54 hits); no chitinase or explicit β-1,3-glucanase in current PGAP annotation |
| C13 | Gram-negative staining; anaerobic; non-motile; rod-shaped | Phenotypic | No (need isolate) | No | **OUT_OF_REACH** — note the paper's own body text describes the *Olsenella* genus as "Gram stain positive", so the Gram-negative claim for BGYT1 is atypical and worth wet-lab re-check |
| C14 | Growth pH 6–8 (opt 7), T 35–40 °C (opt 35), NaCl 0.5–1.5% (opt 0.5%) | Phenotypic | No | No | **OUT_OF_REACH** |
| C15 | Dominant FAs: C16:0 DMA 20.2%, C16:0 20.2%, C18:0 10.5%, C18:1 cis-9 17.0% | Chemotaxonomy | No | No | **OUT_OF_REACH** |
| C16 | Polar lipids: 1 phospholipid + 4 glycolipids + 3 lipids (all unidentified) | Chemotaxonomy | No | No | **OUT_OF_REACH** |

**Coverage summary:** 12 of 16 claims are independently testable from public artifacts (assembly + 16S in GenBank/RefSeq); we tested 10, replicated 6 fully, 4 partially / with caveat, contradicted 1 sub-claim (the paper's own abstract-vs-body genome length discrepancy). 4 claims are wet-lab-only and out of scope for public-data replication.

## 3. Method

### 3.1 Data sources
- **BGYT1 assembly:** NCBI Datasets → `GCF_023276655.1` (RefSeq, `ASM2327665v1`, released 2022-05-08 by KRIBB) — FASTA and GFF fetched via `datasets/v2alpha/genome/accession/…/download`.
- **BGYT1 16S rRNA:** `NR_181929.1` (RefSeq; originally submitted as `OM533390.1`).
- **Closest relative *P. umbonata* DSM 22620 (= KCTC 15140 = A2ᵀ) assembly:** `GCF_900105025.1` (former *Olsenella umbonata*, reclassified to *Parafannyhessea umbonata*).
- **Closest relative 16S:** `AJ251324.3` (*O. umbonata* strain A2, 1433 nt).
- **Type-strain 16S panel for phylogeny (13 sequences):** `NR_181929.1, AJ251324.3, NR_199489.1, NR_180810.1, NR_180580.1, NR_179615.1, NR_179506.1, NR_173694.1, NR_173693.1, NR_173692.1, NR_116939.1, NR_116938.1, NR_115110.1` — all *Olsenella* type strains available in RefSeq's NR series, plus the *O. umbonata* GenBank entry.
- **Paper full text:** Springer Nature paywall (Unpaywall confirms no OA copy); publicly-served article HTML page (`work/springer_article_page.html`) contains full narrative and was used for extraction (`extraction/marker.md`, `extraction/nougat.mmd`); the PDF at `paper.pdf` is Chrome-headless-rendered from that page.

### 3.2 Tools & versions used (LOCAL)
- fastANI (Homebrew), skani (Homebrew), BLAST+ (`blastn`, `makeblastdb`) for reciprocal ANIb.
- `clustalo` for multiple sequence alignment of the 16S panel (13 sequences, MSA length 1505 bp).
- Biopython (`PairwiseAligner` for local pairwise, `DistanceCalculator` + `DistanceTreeConstructor` for NJ tree, `AlignIO`/`SeqIO`).
- Python 3.14; `curl` for NCBI E-utilities and NCBI Datasets v2 API.
- Chrome headless (macOS) for HTML→PDF rendering.
- `ssh uicgpu` used only for external HTTP fetches (Springer HTML) via the proxied env.

### 3.3 Commands (verbatim, condensed)
```
# 1. Metadata
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35689096&retmode=xml' > pubmed.xml
curl -s 'https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_023276655.1/dataset_report' > assembly_report.json

# 2. Genome downloads
curl -s -o BGYT1_genome.zip 'https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_023276655.1/download?include_annotation_type=GENOME_FASTA'
curl -s -o umbonata_genome.zip 'https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_900105025.1/download?include_annotation_type=GENOME_FASTA'
unzip -o BGYT1_genome.zip -d BGYT1_dl
unzip -o umbonata_genome.zip -d umbonata_dl

# 3. Genome stats (own Python)
python3 count_contigs_gc_n50.py bgyt1.fna     # -> 2,453,694 bp / 66.95% GC / 2 contigs / N50 = 1,425,513

# 4. 16S neighbor identity
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NR_181929.1&rettype=fasta' > BGYT1_16S.fasta
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=AJ251324.3&rettype=fasta'  > umbonata_16S.fasta
python3 pairwise_16s.py  # Biopython local aligner: 98.38%

# 5. ANI
fastANI -q bgyt1.fna -r umbonata.fna -o fastani_bgyt1_vs_umbonata.tsv     # 80.83%
fastANI -q umbonata.fna -r bgyt1.fna -o fastani_umb_vs_bgyt1.tsv          # 80.76%
skani dist bgyt1.fna umbonata.fna -s 70 --slow                            # 79.43%
python3 anib_reciprocal.py    # 1020 bp fragments + BLASTn + ≥30% id ≥70% cov ANIb: 83.36%

# 6. Phylogeny
curl -s '.../efetch.fcgi?db=nuccore&id=NR_181929.1,AJ251324.3,NR_199489.1,...' > olsenella_type_strains_16S.fasta
clustalo -i olsenella_type_strains_16S.fasta -o olsenella_16S_msa.fasta --force
python3 nj_tree.py   # Biopython DistanceCalculator('identity') + DistanceTreeConstructor NJ

# 7. Annotation cross-check
curl -s -o BGYT1_gff.zip '...GCF_023276655.1/download?include_annotation_type=GENOME_GFF'
awk -F'\t' '!/^#/ {print $3}' genomic.gff | sort | uniq -c
grep -Ei 'chitinase|glucanase|protease|peptidase' genomic.gff
```

## 4. Results vs. paper

### 4.1 Genome metrics
| Metric | Paper (abstract) | Paper (body) | NCBI (GCF/GCA) | Our own count | Verdict |
|---|---:|---:|---:|---:|---|
| Length (bp) | 2,476,083 | **2,453,694** | 2,453,694 | 2,453,694 | Body-text value **replicated exactly**; abstract value **inconsistent with paper's own body** |
| GC% | 66.9 | 66.9 | 67 | **66.95** | Replicated |
| Contigs | 8 | 8 | 2 | 2 | Paper's 8 not reproducible from current NCBI |
| N50 | 604,117 | 604,117 | 1,425,513 | 1,425,513 | Reflects contig-count difference |
| Genes | 1835 | 1835 | 1810 (PGAP v6.11, 2026-05-18) | — | Within re-annotation drift |
| CDS | 1778 | 1778 | 1761 | — | Within drift |
| tRNA | 50 | 50 | 49 | — | Within drift |
| rRNA | 6 (5S,16S,23S) | 6 | 6 (2× each) | — | Exact |
| tmRNA | 1 | 1 | 1 | — | Exact |

### 4.2 16S phylogenetic placement
Our pairwise 16S identity BGYT1 vs. *O. umbonata* AJ251324 = **98.38%** (matches / alignment length) / **98.45%** (matches / (matches + mismatches)) using Biopython local aligner. Paper: **98.24%** (EzBioCloud). Agreement is excellent — difference reflects the specific gap penalty and how "identity" is defined (with or without terminal gaps).

Full 16S similarity table for BGYT1 vs. 12 *Olsenella* / *P. umbonata* type strains:

| Neighbor | Our % (aln-len) | Our % (nogap) |
|---|---:|---:|
| *P. umbonata* (was *O. umbonata*) A2 (AJ251324.3) | **98.38** | 98.45 |
| *O. profusa* DSM 13989 (NR_116939.1) | 97.68 | 97.88 |
| *O. profusa* DSM 13989 (NR_116938.1) | 97.68 | 97.88 |
| *O. phocaeensis* Marseille-P2936 (NR_173693.1) | 97.54 | 97.61 |
| *O. timonensis* Marseille-P2300 (NR_179506.1) | 97.19 | 97.67 |
| *O. lakotia* SW165 (NR_180580.1) | 96.84 | 97.28 |
| *O. uli* DSM 7084 (NR_115110.1) | 96.76 | 97.10 |
| *O. urininfantis* Marseille-P3197 (NR_173692.1) | 96.62 | 96.90 |
| *O. massiliensis* SIT9 (NR_173694.1) | 95.92 | 95.99 |
| *O. absiana* YH-ols2223 (NR_199489.1) | 95.67 | 96.08 |
| *O. porci* CA-Schmier-601-WT-1 (NR_180810.1) | 95.37 | 95.70 |
| *O. congonensis* Marseille-P3359 (NR_179615.1) | 93.70 | 94.23 |

Rank order agrees with the paper's ranking (*O. umbonata* > *O. profusa* > *O. uli*). Our NJ tree (`report/evidence/olsenella_16S_NJtree.newick`) shows BGYT1 sister to *O. umbonata* with *O. profusa* as the next-closest branch — matching Fig. 1 of the paper.

### 4.3 ANI vs. *O. umbonata* (nearest relative)
| Method | Result | Paper | Interpretation |
|---|---:|---:|---|
| fastANI (BGYT1→umb) | **80.83%** (331 of 817 fragments aligned) | 76.8 | Above paper value |
| fastANI (umb→BGYT1) | **80.76%** (338 of 784) | 76.8 | Reciprocal-consistent |
| skani (learned mode, -s 70 --slow) | **79.43%** (aln fraction ~19%) | 76.8 | Above paper value |
| Own ANIb (1020 bp BLASTn frags, ≥30% id, ≥70% cov, reciprocal mean of 400 & 410 kept frags) | **83.36%** | 76.8 | Above paper value |
| **All methods’ qualitative verdict** | **≪ 95% species threshold** | ≪ 95% | Species novelty **REPLICATED** unambiguously |

The magnitude gap is a real, methodology-dependent difference. Paper used EzBioCloud's OrthoANIu tool, which at cross-genus divergences (Olsenella vs. Parafannyhessea; note the entire reclassification since the paper was written) tends to report lower ANI than fastANI/skani/ANIb. Because the values here are all well below the species-delineation boundary, the *taxonomic conclusion* is not affected.

### 4.4 Annotation feature cross-check
- **Proteases / peptidases:** 54 hits in current PGAP GFF (grep -Ei "protease|peptidase") — supports paper claim ✓
- **Chitinases:** 0 hits — paper claim NOT reproduced in current PGAP annotation
- **β-1,3-glucanases (explicit):** 0 hits — paper claim NOT reproduced
- Glycoside-hydrolase families found: GH1 (2), GH3 (2), GH25 (2, lysozyme-like — acts on bacterial peptidoglycan, not fungal cell walls), plus 3 α-amylase-family GH. This is bacterial-cell-wall / carbohydrate-metabolism machinery, not fungal-cell-wall degrading machinery.
- The paper's motivating claim that BGYT1 might function as a plant-fungal-pathogen biocontrol agent (via chitinases + glucanases) is not obviously supported by the current PGAP annotation of the deposited genome. This is a **testable and specific replication finding** and one of our Open Questions below.

## 5. Verdict + justification

**Overall verdict: PARTIAL (leaning toward REPLICATED for the core taxonomic claim)**

Justification: this is a straightforward "novel species announcement" whose *primary artifact* is the deposited assembly (`GCF_023276655.1`) + deposited 16S sequence (`NR_181929.1`). Both are public. Every core, testable quantitative claim was reproduced within tool-drift tolerance: genome length matches the paper's own body-text number exactly, GC% matches within rounding, annotation feature counts drift by <2% (attributable to PGAP re-annotation over 4 years), 16S similarity to *O. umbonata* matches within alignment-method noise. The **species-novelty conclusion is unambiguously supported** by every ANI/16S metric we computed. However, several sub-claims were only partially or not reproduced: (a) contig-count and N50 differ (NCBI cleanup), (b) the paper's abstract-vs-body genome-length inconsistency is internally contradictory, (c) chitinase and β-1,3-glucanase claims are not supported by the current PGAP annotation, and (d) phenotypic/chemotaxonomy claims are out-of-reach without the live isolate. Hence **PARTIAL** rather than **REPLICATED**.

## Open Questions

- **Q1** (heavy) — Why does the paper's abstract report 2,476,083 bp when the body text and both NCBI deposit records report 2,453,694 bp? A 22-kb (0.9%) discrepancy in an *announcement* paper is nontrivial. Likely a pre-cleanup assembly number that failed to update in the abstract. Are there similar abstract-vs-deposit mismatches across the *Archives of Microbiology* / IJSEM species-announcement corpus? Would benefit a genome-length audit of type-strain announcements 2020–2025.
- **Q2** (heavy) — Why is the paper's ANI value (76.8%) systematically 3–7 pp lower than every modern tool (fastANI, skani, ANIb) for the same genome pair? Is this an EzBioCloud OrthoANIu quirk at cross-genus divergences? Would benefit a tool-cross-comparison benchmark at 75–90% ANI using paired publications with underlying deposited genomes.
- **Q3** (heavy) — Chitinase and β-1,3-glucanase genes claimed as detected in the paper are not present in the current PGAP annotation of the deposited genome. Was the paper's original annotation tool (Prokka + KEGG-Decoder + RAST as stated) using a looser threshold, or did the paper misannotate? Re-running Prokka/KEGG-Decoder on the current FASTA and diffing against PGAP would resolve this.
- **Q4** (heavy) — The paper states "Gram-stain-negative" for BGYT1 but describes the *Olsenella* genus (Actinobacteria phylum) as "Gram stain positive" in the introduction. Actinobacteria are canonically Gram-positive. Is BGYT1's Gram-negative reaction genuine (atypical Actinobacterium worth investigating) or a Gram-stain artifact for a rod with an unusually thin wall? Requires the live isolate KCTC 25379ᵀ.
- **Q5** (heavy) — *Olsenella umbonata* was reclassified to *Parafannyhessea umbonata* (Zgheib et al. 2021, referenced by the paper itself). If BGYT1's closest relative is now in a different genus, and the paper's own phylogenomic (TYGS) tree shows BGYT1 "in a distinct species branch" from other *Olsenella*, then is *Olsenella intestinalis* also potentially a *Parafannyhessea* species rather than an *Olsenella*? An updated TYGS analysis including all currently-valid *Parafannyhessea*, *Olsenella*, *Fannyhessea*, *Lancefieldella*, and *Paratractidigestivibacter* type strains would resolve the correct genus placement.

(Same five questions with `basis` and `next_steps` in `report/open_questions.json`.)

## Evidence files
See `report/evidence/`:
- `paper_vs_replication.json` — full metric-by-metric comparison
- `16s_pairwise_identity.json` — BGYT1 vs. *O. umbonata* 16S alignment
- `16s_similarity_matrix.json` — BGYT1 vs. all 12 *Olsenella*/*Parafannyhessea* type strains
- `annotation_features.json` — PGAP feature counts + cell-wall-enzyme grep
- `olsenella_16S_NJtree.newick` — our NJ tree of 13 type strains
- `olsenella_16S_MSA.fasta` — Clustal Omega MSA (13 seqs × 1505 bp)
- `fastani_bgyt1_vs_umbonata.tsv`, `fastani_umb_vs_bgyt1.tsv` — reciprocal fastANI
- `anib_result.json` — reciprocal BLASTn-based ANIb
- `refseq_assembly_report.json`, `genbank_assembly_report.json` — NCBI Datasets metadata
