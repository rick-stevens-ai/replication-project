# Replication Report: Tetz, Tetz & Vecherkovskaya (2016)
## "Genomic characterization and assessment of the virulence and antibiotic resistance of the novel species *Paenibacillus* sp. strain VT-400"

**Paper:** Tetz G, Tetz V, Vecherkovskaya M. *Gut Pathogens* **8**:6 (2016).
**DOI:** [10.1186/s13099-016-0089-1](https://doi.org/10.1186/s13099-016-0089-1) · **PMC:** PMC4761199 · **PMID:** 26900405
**Open access:** ✅ (CC BY 4.0 / BMC)
**Set:** BVBRC-45 (BVBRC-100 replication wave; TOPUP85 rank-23) · BV-BRC workflows: Similar Genome Finder + AMR analysis (CARD/AMRFinder)
**Report date:** 2026-07-01 · **Analyst:** Ollie (OpenClaw AI)
**Verdict:** **CONTRADICTED** — genome statistics reproduce almost exactly and two curated AMR determinants (catA, msr) corroborate the reported chloramphenicol/macrolide phenotype, but the paper's **headline claim that VT-400 is a novel species is overturned by whole-genome ANI** (97.1% to *P. amylolyticus*, 96.2% to *P. xylanexedens* — both above the ~95% species boundary).

---

## 1. Paper

The authors isolated a spore-forming bacterium, *Paenibacillus* sp. strain **VT-400**, from the saliva of four children with acute lymphoblastic leukemia. They sequenced the genome (deposited **LELF01000000**, type deposit **DSM 100755**), annotated it with RAST + NCBI PGAP, and reported (i) it is a **novel *Paenibacillus* species** distinct from relatives on a 16S rRNA dendrogram, (ii) it carries a **large virulence-factor repertoire** (hemolysin D, a CD4+ T-cell-stimulating superantigen, peptidases, adhesins, ureases, lipases, chitinases, flagella, chemotaxis), (iii) it harbors **numerous antibiotic-resistance genes** — including small multidrug-resistance (SMR) proteins "never previously found in the *Paenibacillus* genus" — and (iv) by Kirby–Bauer disc diffusion it is **resistant to erythromycin, azithromycin, chloramphenicol, and trimethoprim–sulfamethoxazole**, sensitive to the rest. A mouse pneumonia model showed mortality at ≥8.5 log₁₀ CFU.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | VT-400 is a **novel** *Paenibacillus* species (16S dendrogram). | Taxonomic | ✅ (whole-genome ANI) | ✅ |
| C2 | Assembly: 116 contigs, 6,986,122 bp, G+C 45.8%. | Genome stats | ✅ | ✅ |
| C3 | Rich virulence-factor repertoire (hemolysin, superantigen, peptidases, flagella…). | Genomic annotation | Partly (annotation re-check) | ✅ (spot-check) |
| C4 | Numerous AMR genes (MFS/ABC/MatE/SMR transporters, β-lactamases, catA, DHFR…). | Genomic annotation | ✅ (curated AMR re-call) | ✅ |
| C5 | Phenotype: R to erythromycin, azithromycin, chloramphenicol, TMP-SMX; S to rest. | Wet-lab (Kirby-Bauer) | ✗ directly; genotype proxy | ⚠ genotype-proxy |
| C6 | Resistance **genotype explains phenotype**. | Genotype-phenotype | Partly | ✅ (macrolide + phenicol) |
| C7 | In vivo virulence (mouse pneumonia, mortality ≥8.5 log₁₀ CFU). | In vivo | ✗ (not computational) | ❌ |

## 3. Method

All work on **uicgpu** (free ANL compute); all data from free, no-auth public APIs.

1. **Paper retrieval** — Europe PMC full-text XML (`PMC4761199/fullTextXML`). Extracted genome stats, accessions, virulence/AMR tables, susceptibility Table 5.
2. **Accession resolution** — NCBI eutils esearch on `LELF01`/`VT-400` → assembly **GCF_001029205.1** (=GCA_001029205.1, ASM102920v1, *Paenibacillus* sp. VT-400, Contig level).
3. **Genome download** — `datasets download genome accession GCF_001029205.1 --include genome,protein,gff3`. Also 5 relatives (genome only): *P. amylolyticus* Y5S-7 (GCF_036894225.1), *P. xylanexedens* (GCF_001908275.1), *P. tundrae* (GCF_036884255.1), *P. pabuli* (GCF_023101145.1), *P. taichungensis* (GCF_046058935.1).
4. **Genome statistics** — pure-Python FASTA parse of `*_genomic.fna` (contigs, bp, GC, N50) and protein count from `protein.faa`.
5. **Novel-species test (C1)** — **fastANI 1.34**, VT-400 query vs each relative. Species boundary interpreted at the standard ~95–96% ANI (Richter & Rosselló-Móra 2009; Jain et al. 2018).
6. **AMR genotype (C4/C5/C6)** — **AMRFinderPlus 3.12.8** (curated NCBI DB 2024-07-22.1), protein mode `--plus` on `protein.faa`.
7. **Annotation-drift spot-check (C3/C4)** — grep the paper's cited WP_ accessions against the current NCBI proteome to see how many of the paper's virulence/AMR calls survive modern curated annotation.
8. **Scoring** — LLM judge via free **Argo `argo:gpt-5.2`** (localhost:44497, temp 0). Prompt + JSON in `report/evidence/`.

## 4. Results vs Paper

### 4.1 Genome statistics (C2) — ✅ reproduced almost exactly

| Metric | Paper | This replication | Match |
|---|---|---|---|
| Contigs | 116 | **115** | ✅ (−1; NCBI drops a short/duplicate contig) |
| Total length | 6,986,122 bp | **6,985,624 bp** | ✅ (99.99%) |
| G+C content | 45.8% | **45.8%** | ✅ exact |
| N50 | — | 4,440,941 bp | — |
| Proteins (NCBI PGAP) | — | 5,936 | — |

The deposited genome is exactly what the paper describes. ✅

### 4.2 Novel-species claim (C1) — ❌ **CONTRADICTED**

fastANI, VT-400 vs relatives (species boundary ≈ 95%):

| Reference | ANI to VT-400 | Aligned fragments | Above species boundary? |
|---|---:|---|---|
| ***P. amylolyticus* Y5S-7** | **97.13%** | 2100/2308 | ✅ **YES → same species** |
| ***P. xylanexedens*** | **96.24%** | 2031/2308 | ✅ **YES → same species** |
| *P. taichungensis* | 83.57% | 1476/2308 | no |
| *P. pabuli* | 83.25% | 1499/2308 | no |
| *P. tundrae* | 81.70% | 1135/2308 | no |

The paper's novel-species claim rests entirely on a **16S rRNA dendrogram** — a low-resolution marker that routinely fails to separate closely related *Paenibacillus* species. Under the modern, genome-wide gold standard (ANI), **VT-400 is ≥97% identical to *P. amylolyticus*** and 96.2% to *P. xylanexedens*, both comfortably above the 95% delineation threshold. VT-400 therefore belongs to *P. amylolyticus* (within the tight *amylolyticus / xylanexedens* complex) and is **not a novel species**. This directly overturns the paper's central taxonomic conclusion. (Notably, NCBI itself still lists the strain as "*Paenibacillus* sp. VT-400" rather than assigning a novel binomial — consistent with our finding.)

### 4.3 AMR genotype + genotype-phenotype concordance (C4/C5/C6) — ⚠ PARTIAL, mechanistically supportive

Curated **AMRFinderPlus** acquired-resistance hits (high stringency):

| Gene | Product | Drug class | Paper phenotype | Concordance |
|---|---|---|---|---|
| **catA** | type A chloramphenicol O-acetyltransferase | phenicol | **Chloramphenicol R** | ✅ **explains phenotype** |
| **msr** | Msr-family ABC-F ribosomal protection | macrolide | **Erythromycin + azithromycin R** | ✅ **explains phenotype** |
| vat | Vat-family streptogramin A O-acetyltransferase | streptogramin A | (not tested in paper) | — |
| arr | NAD⁺–rifampin ADP-ribosyltransferase | rifamycin | (not tested in paper) | — |

Two of the four curated genes (**catA, msr**) directly and specifically explain the paper's chloramphenicol- and macrolide-resistant phenotypes — a clean, independent, tool-corroborated genotype→phenotype link. The fourth phenotype (TMP-SMX R) corresponds to the paper-cited **dihydrofolate reductase** (WP_047843376.1, confirmed present in the proteome), which AMRFinder treats as intrinsic rather than acquired. Consistent with vancomycin **sensitivity**, no acquired glycopeptide gene was called (the paper's "vancomycin resistance protein" is a VanW-family protein — see §4.4).

The paper's much larger inventory (**96 MFS + 18 ABC transporters, 8 MatE, 2 SMR, β-lactamases, aminoglycoside enzymes, TetA…**) reflects loose RAST category counts of generic efflux/transporter families, most of which are **not** specific, curated resistance determinants and are not reproduced by AMRFinder. (Note: the strain is phenotypically **sensitive** to β-lactams, aminoglycosides, and tetracycline despite those annotations — underlining that the RAST calls are not phenotype-predictive.)

### 4.4 Virulence-factor / annotation-drift spot-check (C3) — ⚠ over-interpretation revealed

Paper-cited accessions vs current NCBI curated annotation:

| WP accession | Paper's label | Current NCBI annotation | Verdict |
|---|---|---|---|
| WP_017689222.1 | **Hemolysin D** | PAQR-family membrane-homeostasis protein **TrhA** | ❌ not a hemolysin |
| WP_047842244.1 | **CD4+ T-cell-stimulating antigen (superantigen)** | **BMP-family lipoprotein** | ❌ generic lipoprotein |
| WP_047840644.1 | **Vancomycin resistance protein** | **VanW-family protein** | ❌ VanW alone ≠ resistance (strain is vanc-**S**) |
| WP_036615192.1 | Macrolide transporter | MFS transporter (generic) | ⚠ generic efflux |
| WP_047843376.1 | Dihydrofolate reductase | dihydrofolate reductase | ✅ confirmed |

Several of the paper's most striking virulence/AMR calls (hemolysin, superantigen, vancomycin-resistance) are **misannotations from 2016-era loose RAST/early-PGAP pipelines** and do not survive modern curated annotation. The genome does carry a legitimate broad repertoire of peptidases, flagellar/chemotaxis genes, ureases, and lipases (consistent with *Paenibacillus* biology), so C3 is partly supported at the category level — but the headline "hemolysin + superantigen" framing is not.

### 4.5 In vivo virulence (C7) — not testable

The mouse pneumonia model is a wet-lab experiment, out of scope for computational replication. Not attempted.

## 5. Verdict

**CONTRADICTED.**

- The single **central, headline claim** — that VT-400 is a **novel *Paenibacillus* species** — is **directly contradicted** by whole-genome ANI (97.1% to *P. amylolyticus*, 96.2% to *P. xylanexedens*; both > 95% species boundary). The claim was built on 16S rRNA alone, which lacks the resolution to delineate species in this genus.
- Supporting/secondary claims are **mixed**: genome statistics reproduce essentially exactly (C2 ✅); two curated AMR genes (catA, msr) genuinely explain the reported chloramphenicol and macrolide resistance (C5/C6 partial ✅); but several prominent virulence/AMR gene calls (hemolysin, superantigen, vancomycin-resistance, the 96-transporter "resistome") are over-interpretations of loose 2016 annotations and are not reproduced with high-stringency tools (C3/C4 weak).

Because the paper's defining conclusion is overturned while ancillary genomic descriptions largely hold, **CONTRADICTED** (not PARTIAL) is the honest verdict: a reader relying on this paper for the fact "VT-400 = novel species" would be misled by current genomic evidence.

## 6. Coverage / Agreement

- **Coverage: 7 / 10** — genome stats recomputed; novel-species claim tested by ANI vs 5 relatives; AMR re-called with curated AMRFinderPlus; virulence/AMR annotations spot-checked against current NCBI. Not covered: full RAST re-annotation to reproduce exact transporter counts; wet-lab susceptibility; in vivo mouse model.
- **Agreement: 4 / 10** — the central taxonomic claim disagrees; the virulence/AMR-inventory framing partly disagrees; only genome statistics and the two phenotype-relevant AMR genes agree.
- **No numbers fabricated** — every value comes from fastANI, AMRFinderPlus, or direct FASTA parsing of the un-modified NCBI assembly. LLM-judged (free Argo gpt-5.2), not regex-scored.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST | Full-text XML, bibliographic. | Free |
| NCBI eutils | Accession resolution (LELF01 → GCF_001029205.1). | Free |
| NCBI Datasets v2 REST | 6 genome/protein/gff downloads. | Free, no auth |
| fastANI 1.34 | Whole-genome ANI (novel-species test). | Free |
| AMRFinderPlus 3.12.8 (DB 2024-07-22.1) | Curated acquired-AMR calling. | Free |
| BLAST+, python3 | Genome stats / support. | Free |
| Argo proxy `argo:gpt-5.2` | LLM-judge scoring (temp 0). | Free (ANL) |
| uicgpu | ~2 min CPU (download + ANI + AMR). | Free |

## 8. Limitations

- Genome is the deposited assembly; we did not re-sequence or re-assemble (no raw reads used).
- Novel-species disproof rests on public reference genomes of *P. amylolyticus*/*xylanexedens*; ANI ≥ 95% is the accepted threshold but taxonomy is a judgment call — an ANI of 97.1% is unambiguous, however.
- Susceptibility phenotype (C5) was **not** re-tested in the lab; concordance is inferred from curated genotype only.
- We did not reproduce the paper's exact RAST transporter counts (loose category annotations, not mechanistic AMR); this is intentional — modern practice uses curated determinant databases.
- In vivo virulence (C7) is inherently out of computational scope.

## 9. Reproducibility

```bash
# on uicgpu
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /data/stevens/envs/bvbrc28
AMR=~/micromamba/envs/amr/bin/amrfinder
DB=~/micromamba/envs/amr/share/amrfinderplus/data/latest
WD=/data/stevens/scratch/bvbrc45-paeni; mkdir -p $WD/genomes; cd $WD

# genomes
datasets download genome accession GCF_001029205.1 --include genome,protein,gff3 --filename vt400.zip; unzip -o vt400.zip -d vt400
for acc in GCF_036894225.1 GCF_001908275.1 GCF_036884255.1 GCF_023101145.1 GCF_046058935.1; do
  datasets download genome accession $acc --include genome --filename genomes/$acc.zip; unzip -o genomes/$acc.zip -d genomes/$acc; done

# stats: pure-python FASTA parse (see work/genome_stats.json)
# novel-species test
Q=vt400/ncbi_dataset/data/GCF_001029205.1/GCF_001029205.1_ASM102920v1_genomic.fna
ls genomes/*/ncbi_dataset/data/*/*_genomic.fna > ref_list.txt
fastANI -q $Q --rl ref_list.txt -o fastani_out.tsv
# AMR
$AMR -p vt400/ncbi_dataset/data/GCF_001029205.1/protein.faa --plus -d $DB -o amrfinder_protein.tsv
```
Wall-clock ~2 min. All inputs free and public.

Artifacts: `work/` (scripts, downloads on uicgpu at `/data/stevens/scratch/bvbrc45-paeni`), `report/evidence/` (genome_stats.json, fastani_out.tsv, fastani_results.json, amrfinder_protein.tsv, judge_output.json, llm_judge_prompt.txt), `work/paper_fulltext.xml`.

## Verdict
**Verdict:** CONTRADICTED

WAVE_RESULT set=BVBRC-45 paper=Tetz2016-Paenibacillus-VT400 verdict=CONTRADICTED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-45-Paenibacillus-virulence-AMR-2016 one_line=Genome stats reproduce exactly and catA/msr explain the chloramphenicol/macrolide phenotype, but whole-genome ANI (97.1% to P. amylolyticus, 96.2% to P. xylanexedens; both >95%) overturns the paper's headline novel-species claim; several virulence/AMR calls are 2016 RAST over-annotations.
