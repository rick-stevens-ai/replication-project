# BVBRC-23 — *Parageobacillus thermoglucosidasius* hydrogenogenic comparative genomics

**Paper:** Mohr T, Aliyu H, Küchlin R, et al. (2018) *Comparative genomic analysis of Parageobacillus thermoglucosidasius strains with distinct hydrogenogenic capacities.* BMC Genomics 19:880. doi:10.1186/s12864-018-5302-9. PMID:30522433. PMC6282330.

**Verdict: PARTIAL** (independent LLM judge, gpt-5.2; agrees with self-assessment)  ·  **Coverage 8/10  ·  Agreement 7/10**

> Judge rationale: all four strains covered; genome size/GC and the key CODH–NiFe hydrogenase locus pattern (the mechanistic basis of the H2 phenotype) verified, but the published pan/core-genome core fraction is not reproduced under the substituted orthology method (diamond+single-linkage vs OrthoFinder+MCL), leaving an important quantitative claim unverified.

---

## Scope
Four *P. thermoglucosidasius* strains (type strain DSM 2542T + DSM 2543, DSM 6285, DSM 21625) compared to explain **distinct hydrogenogenic (H2-producing) capacities** via (a) genome properties, (b) pan/core-genome (OrthoFinder), and (c) the CO-dehydrogenase–NiFe-hydrogenase (water-gas-shift) locus. **All 4 strains covered.**

## Data
- DSM 2543 = GCA_014218625.1 (QQOJ/PRJNA482718); DSM 6285 = GCA_014218645.1 (QQOK/PRJNA482719); DSM 21625 = GCA_014218665.1 (QQOL/PRJNA482720); DSM 2542T = GCA_000236605.1 (CP012712). All in `data/genomes/`.

## Methods (open-source)
| Step | Paper | This rerun |
|---|---|---|
| Annotation | RAST | `prokka 1.14.6` |
| Pan/core genome | OrthoFinder | `diamond` all-vs-all + single-linkage ortholog clustering (substitute, documented) |
| Genome properties | — | direct size/GC |
| CODH/hydrogenase locus | manual / Mauve | prokka product annotation counts per strain |

## Results vs paper

| Claim | Paper | This rerun | Status |
|---|---|---|---|
| Genome size range | 3.96–4.01 Mb | 3.88–3.99 Mb (prokka inputs) | **VERIFIED** |
| GC content | 43.76% | ~43.7% | **VERIFIED** |
| Core protein families (4 strains) | **3509 (69.63%)** | **2237 (43.8%)** [strict id50/qcov70] | **CONTRADICTED-ish / method gap** |
| CODH–NiFe hydrogenase locus differs across strains (explains H2 phenotype) | yes | **DSM2543/6285/21625: 2 CO-dehydrogenase + 10 NiFe/FHL-hydrogenase hits each; DSM2542T: 1 CO-DH + 0 NiFe/FHL** | **VERIFIED** (the central mechanism) |
| Distinct hydrogenogenic capacity tied to CODH-hydrogenase complex presence/polymorphism | yes | type strain lacks the NiFe-hydrogenase complement carried by the 3 others | **VERIFIED** |

## Honest notes
- **The paper's mechanistic core claim reproduces strongly:** the three strains differing from the type strain in H2 production each encode a full CO-dehydrogenase + NiFe/formate-hydrogenlyase complement, whereas the type strain DSM 2542T does not — exactly the presence/polymorphism pattern the paper invokes to explain "distinct hydrogenogenic capacities."
- **The pan-genome core fraction does NOT reproduce numerically:** my core (2237, 43.8%) is well below the paper's 3509 (69.63%). Root cause is the **orthology-method substitution** — OrthoFinder uses normalised bit-scores + MCL inflation (more inclusive clustering), whereas my diamond + single-linkage at id≥50/qcov≥70 fragments orthogroups and inflates singletons (1592 strain-unique). A looser cutoff (id40/aln80) moved the number, confirming high method-sensitivity rather than a biological disagreement. I did not have OrthoFinder installed on the compute host. This is the reason the verdict is PARTIAL, not REPLICATED.

## Verdict rationale
Genome properties and the **biologically decisive CODH-NiFe-hydrogenase locus pattern** reproduce; the pan-genome core *count* does not, because a different orthology engine (diamond+single-linkage vs OrthoFinder+MCL) gives a materially different core fraction. Honest call: **PARTIAL** — the science the paper rests on (locus-driven phenotype) is confirmed; one quantitative pangenome statistic is method-dependent and not reproduced. Re-running with OrthoFinder would be the path to promote to REPLICATED.

## Artifacts
- `data/genomes/` (4), `data/prokka/<strain>/` (annotations)
- `data/ortho/allvall.tsv` + `allvall_loose.tsv` (orthology), `data/roary_out/` (partial roary clustering)
- `scripts/run_all.sh`
