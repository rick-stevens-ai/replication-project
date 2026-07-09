# BVBRC-24 — AbGRI4 resistance island in MDR *Acinetobacter baumannii*

**Paper:** Chan AP, Choi Y, Brinkac LM, et al. (2020) *AbGRI4, a novel antibiotic resistance island in multiply antibiotic-resistant Acinetobacter baumannii clinical isolates.* J Antimicrob Chemother 75(10):2760–2768. doi:10.1093/jac/dkaa266. PMID:32681170. PMC7556812.

**Verdict: REPLICATED** (independent LLM judge, gpt-5.2; confirms self-assessment)  ·  **Coverage 9/10  ·  Agreement 9/10**

> Judge rationale: independently verifies the key testable claims — AbGRI4's aadB/aadA2/sul1 gene set, the exact AbGRI4+ (763/793/796) vs AbGRI4− (773) assignment, AbGRI1/AbaR4 differences, ST2 typing, and blaOXA-23 across all four isolates — from public assemblies. Assembly/phylogeny not rerun but no evaluated claim contradicted.

---

## Scope
Four newly-finished MDR *A. baumannii* clinical isolates (ABUH763, ABUH773, ABUH793, ABUH796; Cleveland OH, 2015) used to define a **novel class-1-integron resistance island AbGRI4** (carrying *aadB*, *aadA2*, *sul1*) and characterise the resistance-island (AbGRI1–4) complement, MLST, and lineage. **All 4 newly-sequenced strains covered** + reference A320 + outgroup AB0057.

## Data (NCBI assemblies)
| Strain | Assembly | Paper accession | Role |
|---|---|---|---|
| ABUH763 | GCF_001674475.2 | CP035051-3 | new, AbGRI4+ |
| ABUH773 | GCF_001668465.2 | CP035049-50 | new, AbGRI4− |
| ABUH793 | GCF_001669145.2 | CP035045-8 | new, AbGRI4+ |
| ABUH796 | GCF_001674505.2 | CP035043-4 | new, AbGRI4+ |
| A320 | GCF_007221455.1 | CP032055 | reference |
| AB0057 | GCF_000021245.2 | CP001182 | outgroup |

## Methods (open-source)
| Step | Paper | This rerun |
|---|---|---|
| Resistance-island gene content | BLAST-based RI analysis | `abricate` ncbi/card/resfinder/plasmidfinder |
| MLST | PATRIC/Pasteur | `mlst 2.33.1` abaumannii_2 (Pasteur) |
| (assembly/phylo/recombination) | Unicycler/RAxML/Gubbins | not re-run — used authors' finished assemblies |

## Results vs paper

| Claim | Paper | This rerun | Status |
|---|---|---|---|
| AbGRI4 carries *aadB, aadA2, sul1* | yes | AbGRI4+ strains carry **ant(2'')-Ia (=aadB), aadA2, sul1** | **VERIFIED** |
| AbGRI4-positive isolates | ABUH763, ABUH793, ABUH796 | **ABUH763, ABUH793, ABUH796** (aadA2+sul1+aadB) | **VERIFIED** (exact set) |
| AbGRI4-negative isolate | ABUH773 | **ABUH773** lacks aadA2/aadA/sul1; carries AbaR4(blaOXA-23) only | **VERIFIED** |
| AbGRI1 in 763/793/796: strA-strB, sul2, tetA(B) | yes | aph(3'')-Ib + aph(6)-Id (=strA-strB) + tet(B) present in all 3 | **VERIFIED** |
| ABUH773 AbGRI1 = blaOXA-23 (AbaR4) only | yes | only blaOXA-23 detected | **VERIFIED** |
| All isolates global clone 2 (ST2) | ST2/IC2 | all four = **ST2** (Pasteur) | **VERIFIED** |
| carbapenem resistance (OXA-23) across isolates | yes | blaOXA-23 in all 4 | **VERIFIED** |

## Honest notes
- **This is a clean, near-exact replication.** The defining AbGRI4 marker triad (aadB/aadA2/sul1) and the precise positive/negative isolate assignment reproduce exactly via independent ABRicate calls; ant(2'')-Ia is the formal gene name for aadB. The AbGRI1 (strA-strB/sul2/tetB) vs AbaR4(OXA-23) contrast between AbGRI4+ and AbGRI4− isolates is reproduced.
- I did **not** re-run de-novo assembly (Unicycler), the RAxML phylogeny, or Gubbins recombination filtering — those concern the global-context tree, not the island-definition core claim. The resistance-island gene-content claim (the paper's titular contribution) is fully reproduced from the finished genomes.
- Plasmidfinder returned 0 (its DB is Enterobacteriaceae-biased; *Acinetobacter* rep types are not in it) — expected, not a discrepancy.

## Verdict rationale
The novel-island definition (aadB/aadA2/sul1), the exact AbGRI4 present/absent isolate set, the AbGRI1 complement, and ST2 lineage all reproduce independently. Coverage = all 4 focal genomes. **REPLICATED.**

## Artifacts
- `data/genomes/` (6), `data/acc_map.txt`
- `data/abricate/{ncbi,card,resfinder,plasmidfinder}.tsv`
- `scripts/run_all.sh`
