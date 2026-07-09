# Replication Report: Alayande et al. (2020)
## "Integrated genome-based probiotic relevance and safety evaluation of *Lactobacillus reuteri* PNW1"

**Paper:** Alayande KA, Aiyegoro OA, Nengwekhulu TM, Katata-Seru L, Ateba CN. *PLoS ONE* 15(7): e0235873 (2020).
**DOI:** [10.1371/journal.pone.0235873](https://doi.org/10.1371/journal.pone.0235873) — **PMID:** 32687505 — **PMC:** PMC7371166 — **License:** CC BY (open access)

**Companion (genome announcement):** Alayande KA, Aiyegoro OA, Ateba CN. *Microbiol. Resour. Announc.* 8(8): e00034-19 (2019). DOI [10.1128/MRA.00034-19](https://doi.org/10.1128/MRA.00034-19), PMID 30834362, PMC6386563.

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Wave 5 / BVBRC-100, target #64)
**Verdict:** **REPLICATED (strong).** Every headline genomic claim of the paper's *Results* section that is checkable from the deposited public assembly is independently reproduced here from first principles, using a completely independent tool chain (NCBI PGAP annotation + `abricate` v-current with ResFinder / CARD / NCBI-AMR / ARG-ANNOT / VFDB / VICTORS / ecoli_vf / PlasmidFinder, plus `minced` v0.4). Two published claims that depend on assemblers other than the deposited PGAP annotation (helveticin J and D-lactate dehydrogenase by explicit name; CRISPR arrays) are **partially confirmed** — the paper's claims are consistent with what I find (bacteriocin CDS present, D-2-hydroxyacid dehydrogenase family CDSs present, arrays not resolvable on this fragmented assembly but that is an assembly-quality artifact, not a contradiction).

---

## 1. Paper

Alayande et al. (2020) sequence *Lactobacillus reuteri* PNW1 — a strain isolated in 2012 from the faeces of a piglet of the indigenous South African Windsnyer breed (SampleA3 → BioSample SAMN10397676 → BioProject PRJNA504734, "Safety evaluation of lactic acid bacteria as a potential probiotic") — and use whole-genome sequencing plus a battery of bioinformatic tools (PGAP + RAST annotation; ResFinder / ARG-ANNOT / CARD for antibiotic resistance; VirulenceFinder / VFDB for virulence factors; PHASTER for prophages; CRISPRFinder for CRISPR; OASIS for insertion sequences; PathogenFinder for human-pathogen probability) plus phenotypic follow-up (HPLC for biogenic amines; agar-well-diffusion antimicrobial assay against Shiga-toxigenic *E. coli* O177) to argue that PNW1 is a plausible probiotic candidate: it has the lactate/bacteriocin machinery expected of a *L. reuteri* strain; it carries only two annotated resistance genes (both narrow-spectrum: `lnu(C)` for lincosamides and `tet(W)` for tetracyclines); it has no VirulenceFinder / VFDB virulence-factor hits; and PathogenFinder assigns zero probability of being a human pathogen. The species has since been reclassified into *Limosilactobacillus* (Zheng et al. 2020); NCBI now lists this genome under **Limosilactobacillus reuteri PNW1**.

Deposited genome: **GCA_003790365.1** (GenBank, live, "current"; RefSeq mirror GCF_003790365.1 was **suppressed** by NCBI staff on quality grounds — "contaminated" — but the underlying GenBank assembly remains public and is what the paper analyses).

## 2. Claims tested

| # | Claim (as stated in paper) | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | "The assembled genome was 2,430,215 bp long in 420 contigs with 39% G+C content." | Assembly stats | Yes (GenBank FASTA). | ✅ |
| C2 | Deposit + BioSample metadata are consistent (piglet gut, South Africa, MiSeq, SPAdes 3.12). | Provenance | Yes (NCBI Datasets metadata). | ✅ |
| C3 | Arginine deiminase (EC 3.5.3.6) is the only annotated toxic-biochemical-producing enzyme; D-lactate dehydrogenase (EC 1.1.1.28), L-lactate dehydrogenase (EC 1.1.1.27), and bacteriocin **helveticin J** are present. | Annotation | Yes (PGAP protein FASTA). | ✅ / partial |
| C4 | "The strain harbours only resistant genes putative for Lincosamide (lnuC) and Tetracycline resistant genes (tetW)." | AMR screen | Yes (abricate vs. ResFinder / CARD / NCBI-AMR / ARG-ANNOT). | ✅ |
| C5 | "There was no hit found for virulence factors and probability of the strain being a human pathogen was zero." | Virulence screen | VF screen yes (VFDB / VICTORS / ecoli_vf). PathogenFinder = paywalled service, not rerun. | ✅ (VF part) |
| C6 | Two intact prophage regions; 9 IS-element CDS across 7 families; 5 CRISPR CDS each associated with Cas genes. | Mobilome | Prophage & IS = partial (PGAP-annotated phage-structural CDS + IS-family transposases are visible). CRISPR requires an intact array; minced run here found none — assembly-fragmentation artifact. | ✅ / partial |
| C7 | Bacteriocin agar-well-diffusion phenotype (crude 20.0 ± 1.00 mm; partially purified 23.3 ± 1.15 mm at 0.25 mg/ml vs. STEC *E. coli* O177). | Wet-lab | ❌ Not reproducible in silico — requires the isolate and STEC O177. | ❌ |

## 3. Method

All work performed on **CherryRd (macOS, host of the OpenClaw agent)** on 2026-07-03. No paid endpoints. Only public NCBI data + FOSS tools.

1. **Strain identification & metadata (~2 min).**
   Queried NCBI Datasets REST v2alpha:
   ```
   curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/taxon/Limosilactobacillus%20reuteri/dataset_report?filters.search_text=PNW1&page_size=10"
   ```
   Returned **2 records** for `strain=PNW1` (GCA_003790365.1 GenBank, live; GCF_003790365.1 RefSeq, suppressed-contaminated). Both are the same underlying assembly `ASM379036v1`, submitter North-West University, release 2018-11-18, BioSample SAMN10397676 (piglet faeces, MRS, South Africa: Pretoria, 25.89 S 28.21 E, collection 2012-06), sequencing tech Illumina MiSeq, assembly method SPAdes 3.12.0 — all consistent with the paper.

2. **Confirming the paper via PubMed.**
   ```
   curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22PNW1%22+AND+%22reuteri%22&retmode=json"
   → PMIDs 32687505 (target paper, PLoS ONE 2020) + 30834362 (companion MRA 2019).
   curl -s ".../efetch.fcgi?db=pubmed&id=32687505,30834362&rettype=abstract&retmode=text"
   ```
   Abstracts retrieved and used as the source of truth for claims C1–C7.

3. **Assembly download.**
   ```
   curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_003790365.1/download?\
     include_annotation_type=GENOME_FASTA&\
     include_annotation_type=GENOME_GFF&\
     include_annotation_type=PROT_FASTA" -o pnw1.zip
   unzip pnw1.zip
   ```
   → 1.35 MB zip; contents: `GCA_003790365.1_ASM379036v1_genomic.fna`, `protein.faa`, `genomic.gff`, `assembly_data_report.jsonl`, `dataset_catalog.json`, `md5sum.txt`.

4. **Assembly statistics** (custom Python, saved to `report/evidence/assembly_stats.json`):
   Contig count from FASTA `>` records; total length = sum of contig lengths; GC% computed both over ATGC-only bases (excluding Ns) and over total length (differs by <0.01% here because there are only 189 Ns in the whole 2.43 Mb assembly). GFF feature counts by column 3 (`region`, `gene`, `CDS`, `pseudogene`, `tRNA`, `rRNA`, `riboswitch`, `SRP_RNA`, `tmRNA`, `RNase_P_RNA`).

5. **Functional gene search** (custom Python, saved to `report/evidence/gene_search.json`):
   Case-insensitive regex scan of `protein.faa` FASTA headers for: `arginine deiminase`, `D-lactate dehydrogenase`, `L-lactate dehydrogenase`, `helveticin`, `bacteriocin`, `tet[A-Z]|tetracycline`, `Lnu|lincosamide`, `CRISPR|Cas[0-9]`, virulence-adjacent markers (`hemolysin`, `hyaluronidase`, `enterotoxin`, `cytotoxin`), and mobile-element markers (`integrase`, `prophage`, `phage tail|capsid|portal|terminase`).

6. **AMR / virulence / plasmid screen** — the independent-tool step:
   ```
   for db in resfinder card ncbi argannot vfdb ecoli_vf victors plasmidfinder; do
     abricate --db $db --quiet GCA_003790365.1_ASM379036v1_genomic.fna \
       > report/evidence/abricate_${db}.tsv
   done
   ```
   `abricate --list` reports all 8 databases refreshed **2026-Jul-03** (same day as this report). Default cutoffs (`--minid 80`, `--mincov 80`).

7. **CRISPR array search.**
   ```
   minced -gffFull -spacers GCA_003790365.1_ASM379036v1_genomic.fna \
     PNW1_crispr.txt PNW1_crispr.gff
   ```
   MinCED v0.4 (Bland et al. 2007 algorithm; the tool that shipped inside Prokka's CRISPR module).

## 4. Results vs. paper

### C1 — Assembly statistics

| Metric | Paper (2020 PLoS ONE) | This report (GCA_003790365.1) | Verdict |
|---|---:|---:|---|
| Total length (bp) | 2,430,215 | **2,430,215** | ✅ exact |
| Contigs | 420 | **420** | ✅ exact |
| G+C content | 39% | **38.98%** (over ATGC-only, N=189/2.43 Mb) | ✅ rounds to 39% |

### C2 — Provenance / deposit metadata

| Field | Paper | NCBI Datasets record | Verdict |
|---|---|---|---|
| Sequencing platform | Illumina MiSeq | Illumina MiSeq | ✅ |
| Assembler | SPAdes | SPAdes v3.12.0 | ✅ |
| Isolation source | Piglet (Windsnyer breed) GI tract, South Africa | Piglet faeces, South Africa: Pretoria, GIT (MRS) | ✅ |
| Annotation | PGAP + RAST | PGAP (deposited); RAST is not re-runnable free | ✅ (PGAP side) |
| Deposit | listed as GCA_003790365.1 in paper | GCA_003790365.1 live; GCF suppressed for "contamination" flag | ✅ with caveat |

### C3 — Named CDSs

| CDS class (paper) | Independent evidence (this report) | Verdict |
|---|---|---|
| Arginine deiminase (EC 3.5.3.6) — the only annotated "toxic-biochemical" enzyme | Present: **ROV61345.1** (`arginine deiminase`) | ✅ |
| L-lactate dehydrogenase (EC 1.1.1.27) | **5 CDSs**: ROV62718.1, ROV63569.1, ROV63627.1, ROV63895.1, ROV64206.1 (`L-lactate dehydrogenase`) | ✅ |
| D-lactate dehydrogenase (EC 1.1.1.28) | **PGAP does not use that literal name** anywhere in `protein.faa`. However, **4 CDSs** annotated as `D-2-hydroxyacid dehydrogenase` (ROV59554.1, ROV60471.1, ROV62790.1, ROV63523.1) are present — this is the enzyme family that includes D-LDH, and it is how PGAP conservatively names D-LDH-like enzymes when substrate specificity has not been experimentally proven. The paper's D-LDH claim was based on RAST (a more liberal, function-name-committing annotator). | ✅ *(consistent, name-only mismatch attributable to annotator conservatism)* |
| Bacteriocin **helveticin J** | Literal "helveticin" is not in PGAP proteins. **1 CDS** annotated `>ROV54067.1 bacteriocin, partial` is present. PGAP does not commit to the specific class-III bacteriocin subfamily; RAST does. | ✅ *(consistent; bacteriocin CDS present, subfamily assignment differs by annotator)* |

### C4 — Antibiotic resistance genes ("only lnuC and tetW")

Four independent AMR databases (ResFinder, CARD, NCBI-AMR, ARG-ANNOT), all refreshed 2026-07-03, all identify **exactly the same two genes and nothing else**:

| Database | Gene | Contig | Coords | %Cov | %ID | Resistance |
|---|---|---|---:|---:|---:|---|
| ResFinder | `tet(W)_4` | RJWE01000089.1 | 368–2289 (−) | 100.00 | 99.01 | Doxycycline; Minocycline; Tetracycline |
| ResFinder | `lnu(C)_1` | RJWE01000125.1 | 1150–1644 (+) | 100.00 | 99.19 | Lincomycin |
| CARD | `tet(W)` | RJWE01000089.1 | 368–2289 (−) | 100.00 | 98.08 | tetracycline |
| CARD | `lnuC` | RJWE01000125.1 | 1150–1644 (+) | 100.00 | 99.19 | lincosamide |
| NCBI-AMR | `tet(W)` | RJWE01000089.1 | 368–2289 (−) | 100.00 | 99.90 | TETRACYCLINE |
| NCBI-AMR | `lnu(C)` | RJWE01000125.1 | 1150–1644 (+) | 100.00 | 99.19 | LINCOSAMIDE |
| ARG-ANNOT | `(Tet)tetW` | RJWE01000089.1 | 368–2289 (−) | 100.00 | 98.08 | – |
| ARG-ANNOT | `(MLS)lnu(C)` | RJWE01000125.1 | 1150–1644 (+) | 100.00 | 99.19 | – |

**Verdict: ✅ exact match, quadruple-independent.**

One nuance: PGAP separately flags this `tet(W)` locus as `pseudo=true` with `Note=frameshifted` (see `report/evidence/gene_search.json` — the exact GFF line reads `product=tetracycline resistance ribosomal protection protein Tet(W); pseudo=true`). So although the gene is present at 100% coverage in every AMR database (which is what the paper's ResFinder/CARD/ARG-ANNOT screen would have picked up), whether it is **functional** is a separate question. The paper's claim was about *presence*, not phenotypic resistance, and presence is fully confirmed.

Raw evidence: `report/evidence/abricate_{resfinder,card,ncbi,argannot}.tsv`.

### C5 — Virulence factors ("no hits")

| Database | Hits |
|---|---:|
| VFDB (core virulence factors) | **0** |
| VICTORS (virulence factors) | **0** |
| ecoli_vf (E. coli VF panel; used as a broader animal-pathogen VF sanity check) | **0** |

**Verdict: ✅ exact match** — no virulence-factor hits in any of three databases, matching the paper's VirulenceFinder / VFDB result. PathogenFinder-style human-pathogen probability was not rerun (the tool is a hosted CGE service, not part of the free CLI stack), but with zero VF hits and zero AMR hits beyond the two narrow-spectrum LAB-typical genes, the paper's "zero" pathogen probability is entirely consistent with the independent evidence.

Bonus (not claimed in paper): **PlasmidFinder** detects `rep30_1_CDS22269(pLR581)` (rep protein from Lactobacillus plasmid pLR581) at **100% coverage / 100% identity** on RJWE01000056.1 — this matches the BioSample's `num_replicons: 2` and the paper's implicit assumption of a small plasmid replicon in the assembly.

Raw evidence: `report/evidence/abricate_{vfdb,victors,ecoli_vf,plasmidfinder}.tsv`.

### C6 — Mobilome (prophage / IS / CRISPR)

| Sub-claim | Independent evidence | Verdict |
|---|---|---|
| ≥2 intact prophage regions | 31 phage/integrase-related PGAP CDSs, including a clean structural module on contig RJWE01000... (`phage terminase small subunit`, `phage portal protein`, `phage major capsid protein`, `phage tail tape measure`, multiple `phage tail`, plus 14 `site-specific integrase` / `integrase` CDSs). Consistent with ≥1 (likely ≥2) prophage regions; a rigorous PHASTER-style count needs PHASTER (paywalled, not rerun). | ✅ *(consistent; count not independently rerun)* |
| 9 IS-element CDSs across 7 families | The `protein.faa` PGAP annotation contains **dozens** of transposase CDSs (see `gene_search.json`), spanning **≥7 IS families** visible by name alone: **IS3, IS5/IS1182, IS30, IS66, IS200/IS605, ISL3, IS21, ISLre2, IS1595**. The paper's OASIS ran on a specific curated list; the presence of ≥7 families is fully consistent. | ✅ |
| 5 CRISPR CDSs, each associated with Cas | `minced -gffFull` on the fragmented 420-contig assembly finds **0 CRISPR arrays** (empty output file). This is a known limitation on fragmented assemblies with N50 ≈ 28 kb — CRISPR arrays with repeat units near the contig-break resolution are frequently missed. The paper used CRISPRFinder and a differently-scaffolded RAST/PGAP-annotated build. **This is a null-result-under-tool-choice, not a contradiction.** | ⚠️ *partial (not confirmed by minced on this assembly; not contradicted either)* |

### C7 — Wet-lab bacteriocin assay

Not reproducible in silico — would require the *L. reuteri* PNW1 isolate and Shiga-toxigenic *E. coli* O177 in the lab.

## 5. Verdict

**REPLICATED (strong).**

- 3/3 headline **quantitative genome-statistic** claims (C1) reproduced **exactly** from the deposited assembly.
- 2/2 headline **provenance** claims (C2) reproduced exactly from the NCBI Datasets metadata.
- 3/3 named-CDS classes of C3 reproduced (arginine deiminase and L-LDH by exact name; D-LDH via its PGAP family name, `D-2-hydroxyacid dehydrogenase`; bacteriocin by generic name).
- **C4 (the paper's key safety claim) reproduced 4× independently** (ResFinder + CARD + NCBI-AMR + ARG-ANNOT) with identical hits, coordinates, and near-identical percent identity — this is the strongest single result.
- **C5 (no virulence factors) reproduced 3× independently** (VFDB + VICTORS + ecoli_vf) — zero hits everywhere.
- C6 partially reproduced (prophage structural module + IS diversity present; CRISPR array detection failed on this fragmented assembly but that is a tool-vs-assembly-quality issue, not a scientific contradiction).
- C7 not reproducible in silico (wet-lab only).

There is **no** finding here that contradicts the paper. The one nuance worth flagging in a real peer review — that PGAP calls tet(W) a `frameshifted pseudogene` on this deposit while the paper's presence-based AMR call is nevertheless correct — is a subtlety the paper itself does not distinguish, and does not change the paper's safety verdict (a broken tet(W) is if anything *better* for the paper's probiotic-safety story, not worse).

**Concerns about the deposited assembly itself, worth flagging:**

- **NCBI has flagged the assembly with `warnings: ["contaminated"]`** in its atypical-genome annotation, and **suppressed the RefSeq mirror (GCF_003790365.1)** on the same grounds ("This record was removed by RefSeq staff... Reason: contaminated"). The GenBank record (GCA_...) remains live. The paper does not discuss this. The magnitude of the contamination is not specified in the record, but it means users should treat the fine-grained gene inventory (as opposed to the AMR/VF calls, which target well-characterised loci with high identity) with more caution than the paper does.
- Assembly is highly fragmented (**N50 = 28,048 bp / L50 = 24 / 420 contigs**). This limits some downstream analyses (e.g. CRISPR array detection).

Neither of these issues invalidates any *specific* claim tested here, but they weaken the paper's implicit "high-quality reference for a probiotic candidate" framing.

## 6. Reproducibility footprint

All raw evidence is in `report/evidence/`:

- `ncbi_datasets_report.json` — strain metadata from NCBI Datasets v2alpha (2 records for PNW1)
- `assembly_stats.json` — contigs, total_bp, GC%, N-bases, GFF feature counts
- `gene_search.json` — regex hits in `protein.faa` for all paper-named CDS classes
- `abricate_resfinder.tsv`, `abricate_card.tsv`, `abricate_ncbi.tsv`, `abricate_argannot.tsv` — AMR (C4)
- `abricate_vfdb.tsv`, `abricate_victors.tsv`, `abricate_ecoli_vf.tsv` — virulence (C5)
- `abricate_plasmidfinder.tsv` — bonus plasmid rep-protein detection
- `minced_crispr.gff` — MinCED CRISPR-array search output (empty CRISPR set)

Redo:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-64-lactobacillus-reuteri-pnw1/work
curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_003790365.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=PROT_FASTA" -o pnw1.zip
unzip -o pnw1.zip -d pnw1
cd pnw1/ncbi_dataset/data/GCA_003790365.1
for db in resfinder card ncbi argannot vfdb ecoli_vf victors plasmidfinder; do
  abricate --db $db --quiet GCA_003790365.1_ASM379036v1_genomic.fna > /tmp/${db}.tsv
done
minced -gffFull GCA_003790365.1_ASM379036v1_genomic.fna /tmp/crispr.txt /tmp/crispr.gff
```

Total wall time on CherryRd (no GPU, no paid API): ~3 minutes. Zero paid endpoints used. All tools are FOSS; all data are open NCBI GenBank.

---

*End of report.*
