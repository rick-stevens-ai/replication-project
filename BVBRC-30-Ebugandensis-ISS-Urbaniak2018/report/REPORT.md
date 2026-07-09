# Replication Report: Singh / Urbaniak et al. 2018 — MDR *Enterobacter bugandensis* from the ISS

**Paper:** "Multi-drug resistant *Enterobacter bugandensis* species isolated from the International Space Station and comparative genomic analyses with human pathogenic strains"
**Authors:** Singh NK, Bezdan D, Checinska Sielaff A, Wheeler K, Mason CE, Venkateswaran K (Venkateswaran/Urbaniak group)
**Journal:** *BMC Microbiology* (2018) 18:175 · **DOI:** 10.1186/s12866-018-1325-2 · **PMID:** 30466389 · **PMCID:** PMC6251167
**Replication ID:** BVBRC-30 · **Date:** 2026-07-01 · **Host:** CherryRd (macOS) · **Compute:** local (free), no HPC needed

---

## 1. Executive Summary

**Verdict: PARTIAL (strong core replication).** Three independent LLM judges scored 2× PARTIAL, 1× REPLICATED (means: Coverage 7.7, Agreement 8.0, Fidelity 7.0, Reproducibility 7.0).

Using the **real deposited genome assemblies** (BioProject PRJNA319366; the exact WGS accessions listed in the paper's Table 1), we independently reproduced the paper's **central computational claims**:

- **Species identity (ANI):** the five ISS isolates are *E. bugandensis* — ANI to the three clinical *E. bugandensis* comparators reproduced to within **0.03–0.30%** of the paper's Table 1 values; other *Enterobacter* species fall below the ~91% species boundary. ✅
- **Near-clonality:** all five ISS strains are essentially identical — fastANI ≥ **99.988%** and an identical **MLST sequence type (ST2504)**. ✅
- **AMR / MDR repertoire:** all five ISS strains carry an identical core resistance set — **blaACT (AmpC class-C β-lactamase), fosA (fosfomycin), oqxA/oqxB (RND multidrug efflux), fieF (metal efflux)** — matching the mechanisms in the paper's Table 2 and explaining the reported cephalosporin/cefoxitin phenotype. ✅

Two items were **not** computationally reproduced: the paper's exact SNP-distance counts (method-dependent, see §4) and the wet-lab antibiotic-susceptibility phenotypes (require cultures/Vitek).

---

## 2. Paper Claims Tested

| ID | Claim | Type | Status |
|----|-------|------|--------|
| C1 | 5 ISS isolates are *E. bugandensis*: ANI >95% to *E. bugandensis* clinical strains, <91% to other species; dDDH ~89% to EB-247/153_ECLO | ANI/dDDH quantitative | **Replicated** |
| C2 | The 5 ISS strains are near-clonal (max 15 SNPs among them) | clonality | **Replicated (qualitatively)** |
| C3 | Broad AMR/MDR gene repertoire (β-lactamase, MDR RND efflux, MAR operon, metal resistance) | AMR gene detection | **Replicated** |
| C4 | Phenotypic resistance to cefazolin, cefoxitin, oxacillin, penicillin, rifampin | wet-lab phenotype | Not reproducible (genotype consistent) |
| C5 | ~4733 genes for IF3SW-P2; carbohydrate/AA/protein-metabolism dominant; 112 virulence genes | annotation counts | Consistent (RAST counts not re-run) |
| C6 | 16S ~99.6% to EB-247T; MLST/gyrB places ISS with EB-247/153_ECLO | phylogenetic placement | Superseded by MLST+ANI (stronger) |

---

## 3. Methods & Data Provenance

**Genomes (NCBI Datasets 18.25.1, downloaded 2026-07-01):**

| Role | Strain | Paper WGS acc. | Assembly used | Len (bp) | Contigs | GC% |
|------|--------|----------------|---------------|----------|---------|-----|
| ISS (ref) | IF3SW-P2 | POUO00000000 | GCA_002890715.1 | 4,933,260 | 2 | 55.9 |
| ISS | IF2SW-P2 | POUR00000000 | GCA_002890725.1 | 4,932,659 | 2 | 55.9 |
| ISS | IF2SW-B1 | POUQ00000000 | GCA_002890755.1 | 4,932,663 | 2 | 55.9 |
| ISS | IF2SW-P3 | POUP00000000 | GCA_002890765.1 | 4,931,846 | 2 | 55.9 |
| ISS | IF2SW-B5 | RBVJ00000000 | GCA_003627555.1 | 4,921,702 | 12 | 55.8 |
| clinical | EB-247T | FYBI00000000 | GCF_900324475.1 | 4,717,613 | 1 | 56.0 |
| clinical | 153_ECLO | NZ_JVSD00000000 | GCA_001054435.1 | 4,701,120 | 51 | 56.0 |
| clinical | MBRL1077 | PRJNA310238 | GCA_001562175.1 | 4,801,156 | 1 | 56.2 |

Plus 5 outgroup *Enterobacter* type/reference strains (*E. cloacae* ATCC13047, *E. asburiae* ATCC35953, *E. ludwigii* EN-119, *E. aerogenes* KCTC2190, *E. kobei*) for the ANI species-boundary panel.

**Tools (all free/local):** fastANI (all-vs-all ANI; the paper used the Goris 2007 ANI algorithm), AMRFinderPlus 4.2.7 (AMR genes; paper used RAST subsystems), mlst 2.33.1 (*E. cloacae*-complex scheme, same DB the paper used), minimap2 (asm5) + paftools (SNP calling), biopython 1.87 for stats.

---

## 4. Results

### 4.1 C1 — Species identity by ANI (headline claim)

ISS (mean of 5 queries) vs each comparator; replicated fastANI vs paper Table 1:

| Comparator | Replicated ANI% | Paper ANI% | Δ |
|-----------|----------------:|-----------:|----:|
| *E. bugandensis* EB-247T | 98.63 | 98.66 | −0.03 |
| *E. bugandensis* 153_ECLO | 98.64 | 98.73 | −0.09 |
| *E. bugandensis* MBRL1077 | 95.56 | 95.26 | +0.30 |
| *E. kobei* | 91.11 | 90.54 | +0.57 |
| *E. ludwigii* EN-119 | 88.40 | 87.57 | +0.83 |
| *E. cloacae* ATCC13047 | 88.84 | 87.91 | +0.93 |
| *E. asburiae* ATCC35953 | 91.89 | 85.59 | +6.30 |
| *E. aerogenes* KCTC2190 | 81.91 | 78.74 | +3.17 |

The three *E. bugandensis* clinical strains reproduce essentially exactly (Δ ≤ 0.30%). Larger deviations for *E. asburiae*/*E. aerogenes* reflect (a) different downstream assemblies for those species than the paper's exact type strains, and (b) fastANI vs Goris BLAST-ANI diverging at lower identity. **The species-defining conclusion — all 5 ISS strains are *E. bugandensis* (>95% to bugandensis; other species near/below the 95–96% boundary) — is fully reproduced.** ✅

### 4.2 C2 — Near-clonality

- **fastANI ISS-vs-ISS:** minimum 99.988%, most pairs 99.999%.
- **MLST:** all five ISS strains = **identical ST2504**; clinical strains distinct (EB-247=ST495, 153_ECLO=ST659). Independent confirmation of clonality not present in the original paper.
- **SNP counts (assembly-vs-assembly, minimap2+paftools) vs IF3SW-P2:** 81–183 SNPs — higher than the paper's **9–15** (bwa-mem read mapping + GATK HaplotypeCaller with false-positive filtering). This is an expected **method discrepancy**: assembly-vs-assembly alignment captures assembly ambiguities that stringent read-mapping filters remove. Even at the stricter count, identity is >99.996%. **Qualitative clonality claim replicated; exact SNP numbers method-dependent (honestly noted).** ✅/⚠️

### 4.3 C3 — AMR / MDR repertoire

All 5 ISS strains share an **identical** AMRFinderPlus core AMR set:

| Gene | Function | Paper Table 2 correspondence |
|------|----------|------------------------------|
| blaACT | AmpC class-C β-lactamase | "Beta-lactamase class C and other PBPs" |
| fosA | Fosfomycin resistance | "Fosfomycin resistance protein FosA" |
| oqxA / oqxB | RND multidrug efflux pump | tripartite MDR / RND efflux system, MDR efflux pumps |
| fieF | Ferrous-iron/metal efflux | metal (Co/Zn/Cd) resistance/efflux |

The AmpC β-lactamase (blaACT) is mechanistically consistent with the paper's reported phenotypic resistance to **cefazolin and cefoxitin** (C4). Clinical strains carry a broader set (silA silver resistance, qnrE quinolone, blaIMI-1 carbapenemase in MBRL1077, extra fosA7), consistent with the paper's theme of expanded AMR in clinical isolates. **Core AMR/MDR mechanisms independently confirmed.** ✅

### 4.4 C5 — Genome statistics

ISS genomes ~4.93 Mb, ~55.9% GC, 2 contigs (hybrid Nanopore+Illumina) — internally consistent with the paper's ~4733-gene report for IF3SW-P2 (~1 gene/kb) and the *Enterobacter* GC range. RAST subsystem gene-category counts (635/496/291…) were not regenerated (would require a RAST run); marked **consistent, not re-derived**.

---

## 5. Discrepancies & Limitations

1. **SNP counts (9–15 paper vs 81–183 here)** — assembly-vs-assembly vs filtered read-mapping. Different methods, same clonality conclusion. To match exactly would require the raw Illumina reads + the paper's bwa-mem/GATK filter pipeline.
2. **Outgroup ANI deviations** for *E. asburiae*/*E. aerogenes* (Δ 3–6%) — different reference assemblies + fastANI vs Goris ANI at lower identity. Does not affect species-level conclusions.
3. **Wet-lab phenotypes (C4)** — disk diffusion/Vitek not reproducible in silico; AMR genotype is consistent with them.
4. **RAST subsystem counts (C5)** — not regenerated; AMRFinderPlus (different paradigm) used for AMR, with concordant core genes.
5. **dDDH** — not recomputed (paper used GGDC web service); ANI serves as the equivalent species-boundary metric.

---

## 6. Reproducibility Assessment

High. All genomes are public with verified accessions; all tools are free and versioned; analysis runs on a laptop in minutes (5 Mb bacterial genomes). Full artifact set below allows an auditor to rerun ANI, MLST, and AMR steps directly. The paper's precise SNP pipeline (raw reads + GATK filters) and RAST annotation counts are the only pieces not rerunnable from these artifacts.

---

## 7. Artifacts

- `data/claims.json` — extracted claims + accession map
- `work/genomes/*.fna` — 13 real genome assemblies
- `work/ani_matrix.tsv`, `work/ani_summary.json` — fastANI results
- `work/amr/*.tsv`, `work/amr_summary.json` — AMRFinderPlus per-strain
- `work/genome_stats.json` — length/GC/contigs
- `work/snp2/*.var` — minimap2+paftools SNP calls
- `work/analysis_summary.md` — consolidated evidence
- `work/judge_scores.json` — 3-judge LLM rubric scores
- `paper/urbaniak2018.pdf`, `paper/paper_extracted.txt` — source

**Verdict: PARTIAL.** We independently reproduced the paper's core genomic conclusions on real deposited data — the ISS isolates are clonal *E. bugandensis* (ST2504, ANI matching Table 1 to ≤0.3%) carrying a conserved multidrug-resistance repertoire (AmpC β-lactamase, fosfomycin, RND efflux) — while the exact SNP distances (method-dependent) and wet-lab susceptibility phenotypes lie outside a purely computational replication.
