# Workflow — BVBRC-22 replication of Chauhan et al. (2018)

**Paper:** Chauhan A, Pathak A, Jaswal R, et al. (2018) *Physiological and Comparative Genomic Analysis of Arthrobacter sp. SRS-W-1-2016 Provides Insights on Niche Adaptation for Survival in Uraniferous Soils.* Genes 9(1):31. doi:10.3390/genes9010031.

**Verdict:** PARTIAL (Coverage 8/10, Agreement 8/10; independent LLM judge gpt-5.2).

---

## 0. Objective
Reproduce the four core evidentiary claims of the paper against the *deposited* genome and using *open-source* tooling as substitutes for the paper's proprietary/pipeline choices:

1. Genome size / GC / CDS counts of SRS-W-1-2016.
2. ANI to the paper's named closest relative (*Paenarthrobacter aurescens* TC1).
3. Lineage-specific gene content vs. close *Arthrobacter* relatives.
4. Metal / metalloid resistance gene complement underpinning the uraniferous-soil niche-adaptation argument.

## 1. Data acquisition
- **Focal genome:** GCA_002009585.1 (WGS accession MTPV00000000; BioProject PRJNA352261) → `data/genomes/`.
- **Comparators (nearest available public assemblies):**
  - *Paenarthrobacter aurescens* TC1 — GCA_000014925.1 (paper's named closest relative; exact match).
  - *Arthrobacter cupressi* DSM 24664 — GCA_013409905.1 (substitute; paper's CGMCC1 not deposited).
  - *A. globiformis* CNM05 — GCA_046536215.2 (substitute; paper's NBRC 1237 not deposited).
- Substitutions logged; nearest-available conspecific used in every case.

## 2. Genome characterisation
- **Tool used:** `prodigal` for CDS calling; direct arithmetic on the assembly FASTA for genome size and GC.
- **Paper's tool:** RAST / IMG / PGAAP.
- **Outputs:** `data/SRS_proteins.faa`, plus summary line in the results table.

## 3. Average Nucleotide Identity (ANI)
- **Tool used:** `fastANI` (SRS-W-1-2016 vs. each of the 3 comparators).
- **Paper's tool:** JSpecies (BLAST-ANI).
- **Output:** `data/ani_srs_vs_all.tsv`.

## 4. Lineage-specific genes
- **Approach used:** `diamond blastp` of SRS-W-1-2016 proteins against a pooled database of the 3 comparator proteomes; a query with no hit at ≥30% identity and ≥50% query coverage is called "lineage-specific."
- **Paper's approach:** EDGAR (orthology-based pan/core-genome partitioning, vs. 4 comparators).
- **Output:** `data/srs_vs_comp.tsv`; head-count = 858 CDS in this rerun.

## 5. Metal / biocide resistance
- **Tool used:** `abricate --db bacmet2` (BacMet2 experimentally-confirmed metal/biocide resistance DB).
- **Paper's tool:** RAST subsystems.
- **Output:** `data/abricate/bacmet2_SRS.tsv` — 132 hits across arsC/arsT (As), copR/cutC (Cu), cadD (Cd), chrR (Cr), czcP/czcR/czrA (Zn/Co/Cd), fbpABC/fecDE (Fe).
- **Negative controls (environmental-isolate check):** `abricate --db ncbi` → `data/ncbi_SRS.tsv`; `abricate --db card` → `data/card_SRS.tsv`. Both returned 0 antibiotic-AMR hits, consistent with a non-clinical soil isolate.

## 6. Not attempted (and why)
- **antiSMASH biosynthetic-gene-cluster mining:** antiSMASH not installed on the compute host at the time of the rerun. The paper's actual niche-adaptation argument rests on the metal-resistance complement (reproduced via BacMet2), so this omission was tolerated at the cost of a PARTIAL rather than FULL verdict.
- **Phenotypic uranyl-tolerance assay:** out of scope for a genomic replication; also not performed by the original paper.
- **Full EDGAR-style pan-genome reconstruction:** intentionally substituted with diamond best-hit to test whether the qualitative claim (~10³ lineage-specific CDS) survives a much simpler orthology definition. It does, at 858 vs. 1159.

## 7. Reproduction pipeline (single entry point)
- `scripts/run_all.sh` — orchestrates steps 2–5 given the assemblies in `data/genomes/`.
- All intermediate outputs live under `data/`; final tabular claims are consolidated in `report/REPORT.md`.

## 8. Interpretation gates
Only two of four claims required tool substitution to reproduce quantitatively:
- Claims 1 (genome stats) and 2 (ANI): reproduced within the paper's stated precision.
- Claim 3 (lineage-specific): same order of magnitude, off by ~26% due to orthology-tool + comparator differences.
- Claim 4 (metal resistance): reproduced qualitatively across the same 6 metal categories with a modern DB.

## 9. Provenance
- Every substitution (comparator strain, tool) is documented inline in `report/REPORT.md` and preserved here for auditability.
- No numbers appear in `REPORT.md` or `REPORT.tex` that are not backed by an artifact in `data/`.
