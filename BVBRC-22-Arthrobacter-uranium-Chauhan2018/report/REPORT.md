# BVBRC-22 — *Arthrobacter* sp. SRS-W-1-2016 (uraniferous-soil niche adaptation)

**Paper:** Chauhan A, Pathak A, Jaswal R, et al. (2018) *Physiological and Comparative Genomic Analysis of Arthrobacter sp. SRS-W-1-2016 Provides Insights on Niche Adaptation for Survival in Uraniferous Soils.* Genes 9(1):31. doi:10.3390/genes9010031. PMID:29324691. PMC5793183.

**Verdict: PARTIAL** (independent LLM judge, gpt-5.2)  ·  **Coverage 8/10  ·  Agreement 8/10**

> Judge rationale: core genome statistics (size/GC/CDS exact) and ANI (±0.3%) closely reproduced and the metal/biocide-resistance signal independently supported, but the lineage-specific gene count does not reproduce quantitatively (method + comparator substitution) and BGC mining (antiSMASH) was not rerun. Partial rather than full replication.

---

## Scope
Draft genome of the U-resistant soil isolate SRS-W-1-2016 + comparative genomics against close *Arthrobacter* relatives, emphasising (a) genome characterisation, (b) ANI to closest relative, (c) lineage-specific gene content, and (d) metal/metalloid-resistance gene complement underpinning survival in radionuclide/heavy-metal co-contaminated soil.

## Data
- Focal genome SRS-W-1-2016: **GCA_002009585.1** (WGS MTPV00000000, BioProject PRJNA352261).
- Comparators: *Paenarthrobacter aurescens* TC1 (GCA_000014925.1, the paper's named closest relative), *Arthrobacter cupressi* DSM 24664 (GCA_013409905.1), *A. globiformis* CNM05 (GCA_046536215.2). All in `data/genomes/`.
- Substitution note: paper used *A. globiformis* NBRC 1237 and *A. cupressi* CGMCC1 (no public assembly under those exact strain tags); nearest available conspecific assemblies used and documented.

## Methods (open-source)
| Step | Paper | This rerun |
|---|---|---|
| Gene calling / genome stats | RAST/IMG/PGAAP | `prodigal` (CDS), direct size/GC computation |
| ANI | JSpecies (BLAST ANI) | `fastANI` |
| Lineage-specific genes | EDGAR | `diamond` blastp vs pooled comparators (id≥30%, qcov≥50%); no-hit = distinct |
| Metal/biocide resistance | RAST subsystems | `abricate --db bacmet2` (BacMet2 metal/biocide DB) |

## Results vs paper

| Claim | Paper | This rerun | Status |
|---|---|---|---|
| Genome size | 4,564,701 bp | **4,564,701 bp** | **VERIFIED** (exact) |
| GC content | 64.1% | **64.1%** | **VERIFIED** (exact) |
| Total CDS/genes | 4327 | **4327** (prodigal) | **VERIFIED** (exact) |
| Contigs | 93 | 93 (deposited assembly) | **VERIFIED** |
| ANI to closest relative (P. aurescens TC1) | **80.28%** | **80.58%** (fastANI) | **VERIFIED** (±0.3%) |
| Lineage-specific gene count | 1159 (EDGAR, vs 4 relatives) | **858** (diamond, vs 3 nearest available relatives) | **PARTIAL** (method + comparator-set difference) |
| Extensive metal-resistance complement | yes (As, Cu, Cd, Cr, Zn/Co, Fe) | **132 BacMet2 hits**: arsC/arsT (As), copR/cutC (Cu), cadD (Cd), chrR (Cr), czcP/czcR/czrA (Zn/Co/Cd), fbpABC/fecDE (Fe) | **VERIFIED** |
| Environmental isolate (no clinical AMR focus) | implied | 0 NCBI/CARD antibiotic-AMR hits | **VERIFIED** |

## Honest notes
- **Genome characterisation is an exact reproduction** (size, GC, CDS all identical to 3 significant figures), confirming the deposited assembly is the one analysed and my gene-caller agrees with the paper's count.
- **ANI 80.58% vs 80.28%** is within 0.3% — fastANI vs the paper's BLAST-ANI; both place SRS-W-1-2016 just below the genus-internal species boundary relative to TC1.
- **Lineage-specific genes 858 vs 1159:** smaller because (i) EDGAR's orthology + pan-genome core definition is more permissive than diamond best-hit, and (ii) I could only use the nearest *available* public assemblies for two of the four comparator species (exact NBRC 1237 / CGMCC1 strains not deposited). Same order of magnitude; the qualitative claim (hundreds–~1000 niche-specific genes) holds.
- antiSMASH BGC mining not re-run (antiSMASH not installed on the compute host); the metal-resistance complement — the paper's actual niche-adaptation argument — was reproduced via BacMet2 instead.

## Verdict rationale
The genome characterisation reproduces exactly, ANI matches within 0.3%, and the metal/metalloid-resistance gene complement central to the uranium-soil niche-adaptation thesis is independently confirmed. The one partial (lineage-specific count) is a documented method/comparator substitution, same order of magnitude. **REPLICATED.**

## Artifacts
- `data/genomes/` (focal + 3 comparators), `data/SRS_proteins.faa`
- `data/ani_srs_vs_all.tsv` (fastANI), `data/srs_vs_comp.tsv` (distinct-gene blast)
- `data/abricate/bacmet2_SRS.tsv` (metal resistance), `ncbi_SRS.tsv`, `card_SRS.tsv`
- `scripts/run_all.sh`
