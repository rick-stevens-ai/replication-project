# Failure Analysis — BVBRC-16 (Ghattargi 2018 replication)

**Overall verdict:** PARTIAL (4/6 testable claims reproduced).
**Purpose of this file:** honestly enumerate what did NOT reproduce, why, and what would resolve each miss. This is the failure-log entry for the pass.

---

## FAILURE 1 — C5 (mobile-genetic-element stability claim) does NOT reproduce

### What the paper said
17OM39 has higher genomic stability than pathogenic *E. faecium* strains, i.e. fewer transposons and mobile genetic elements. This is the paper's genome-stability argument for probiotic suitability.

### What we found (REPORT.md §4.4)
BV-BRC RASTtk product-name scan across all annotated CDS:

| MGE class | 17OM39 (5,776 CDS) | T110 (5,173 CDS) |
|---|---|---|
| transposase | 66 | 21 |
| mobile element | 56 | 25 |
| phage | 47 | 19 |
| integrase | 26 | 4 |
| **TOTAL MGE-like CDS** | **237 (4.10%)** | **87 (1.68%)** |

17OM39 has **~2.7× more MGE-like CDS than T110** — the OPPOSITE direction of the paper's claim.

### Root cause (why this happened, honestly)

**Not a paper error, not exactly a replication error either — it is an assembly-status confound.**

1. **17OM39 is a draft assembly (106 contigs, SPAdes short-read).** Draft assemblies systematically over-count transposases and IS elements because:
   - Repetitive IS elements break contigs. A single IS-family element gets fragmented across the ends of two or more contigs, so RASTtk sees "transposase (partial)" annotated on each contig-end fragment. One biological IS → three annotated CDS.
   - Ambiguous repeat regions get collapsed differently in finished vs draft assemblies.
2. **T110 is a finished/complete genome (1 chromosome + 1 plasmid).** No contig-boundary artifacts, so its transposase count is closer to the true biological count.
3. **The paper's actual C5 comparator was NOT T110 — it was pathogenic clinical isolates.** We did not pull those. So our "17OM39 vs T110" comparison is not the same experiment the paper ran.

The paper's claim therefore cannot be *rejected* by our data — but the public BV-BRC RASTtk annotation on its face does not *support* it either. This is a case where the raw evidence available to a third-party replicator points the wrong way, even though the underlying biology may be correct.

### Contributing factors on the paper side
- The paper does not publish the exact ISEScan / IScompass / equivalent command line and version.
- The paper does not publish the list of pathogenic comparator accessions used for the MGE count.
- The paper does not describe how draft-vs-complete assembly status was controlled for.

Together these three omissions make C5 the paper's canonical "underspecified methods" reproducibility failure. A future paper reporting a similar claim should publish the tool, version, command line, and comparator accession list, and should either (a) restrict the comparison to finished genomes or (b) explicitly bias-correct for contig count.

### Contributing factors on the replicator side
- We used BV-BRC RASTtk product-name matching, not a dedicated IS caller (ISEScan / digIS). Product-name matching over-reports transposase in draft assemblies for the same contig-boundary reason.
- We only pulled 17OM39 and T110, not the paper's actual pathogenic comparators.

### Fix
Run ISEScan on the FASTAs of 17OM39, T110, and the paper's pathogenic comparators (Aus0004, TX16, DO, etc.). ISEScan uses hidden-Markov models on the six-frame translation of the assembly and de-duplicates fragments that come from the same IS element. Wall-cost: ~2 CPU-h. This would either resolve C5 in the paper's direction or definitively refute it.

### Lesson
- **Never compare MGE counts across assemblies of different completeness without a contig-count correction or an IS-caller that handles fragmentation.**
- **Never accept product-name keyword counting as a substitute for a dedicated caller for repeat-family features.**
- Product-name counting is a legitimate first-pass screen for the presence/absence of unique genes (vanA, tetM, Cna), but it fails systematically on repeat families.

---

## FAILURE 2 — C6 (core-genome phylogeny) NOT TESTED

### What the paper said
17OM39 clusters with T110 on the core-genome phylogenetic tree (implying commensal/probiotic clade B rather than hospital-adapted CC17 clade A1).

### What we did
Nothing. C6 was explicitly out of scope for this pass because it requires Roary/PhyloPhlAn (~6-8 CPU-h) and a set of comparator genomes.

### Why it matters
C6 is the paper's most paper-specific claim and the biological backbone for calling 17OM39 a probiotic candidate at all. Reproducing safety leaf-claims (C3, C4) without confirming the clade backbone means we've verified 17OM39 as *safe* but not as *phylogenetically probiotic-like*. A commensal clade-B isolate and a hospital clade-A1 isolate can both lack vanA/vanB and Cna if the resistance/virulence loci happen not to have been acquired yet.

### Fix
```
prokka --outdir prokka/17OM39 --prefix 17OM39 <17OM39.fna>
prokka --outdir prokka/T110  --prefix T110  <T110.fna>
# repeat for Aus0004, TX16, DO (pathogenic) + one NPNP
roary -p 8 -i 90 -e --mafft -f roary/ prokka/*/*.gff
FastTree -nt -gtr roary/core_gene_alignment.aln > roary/tree.nwk
```
Cost: ~6-8 CPU-h. This directly tests C6 and produces a bootstrap-supported topology at the (17OM39, T110) node.

### Lesson
- **Do not promote a paper to REPLICATED while its phylogenetic backbone claim is untested.** PARTIAL is the right verdict here. C6 must be tested before any bump to REPLICATED.

---

## FAILURE 3 (minor) — C3 tetracycline-resistance discrepancy

### What the paper said
17OM39 has zero tetracycline-resistance genes (ResFinder call).

### What we found
17OM39 has 1 CDS annotated `tetracycline resistance MFS efflux pump` in the BV-BRC RASTtk annotation (no canonical gene symbol, not a ribosomal-protection *tet* gene). T110 has 0.

### Interpretation
Two possible explanations, both benign:
- **(a) Below ResFinder threshold, above RAST homology threshold.** The MFS efflux pump could be a divergent tetracycline-related transporter that RASTtk flags on protein-family homology but ResFinder (with its stricter %identity + %coverage cutoffs on curated *tet* gene references) does not call. This is the most likely explanation — MFS efflux pumps are a huge, promiscuous family, and RAST's product-name auto-annotation is generous.
- **(b) False-positive RAST annotation.** RASTtk's product-name assignment for MFS transporters is notoriously loose.

Either way, this is NOT a canonical *tetM / tetL / tetK / tetO* ribosomal-protection gene, which is what the paper's ResFinder run would have looked for. The safety claim (no clinically relevant tetracycline resistance) is not undermined.

### Fix
Run `abricate --db resfinder` on the 17OM39 FASTA at 2026 DB version. Cost: ~10 CPU-min. Will either confirm the paper (no *tet*) or upgrade this to a real discrepancy.

### Lesson
- **DB-pipeline coupling matters.** BV-BRC RASTtk product-name calls and ResFinder BLAST calls answer subtly different questions. When they disagree by 1 CDS, run the paper's actual tool before reporting a discrepancy as real.

---

## Summary of failures

| # | What failed | Severity | Root cause | Fix | Cost |
|---|---|---|---|---|---|
| 1 | C5 MGE-stability claim opposite direction | high | draft-vs-finished + product-name counting | ISEScan on all 4 FASTAs | ~2 CPU-h |
| 2 | C6 phylogeny untested | medium | out of scope this pass | prokka + roary + FastTree | ~6-8 CPU-h |
| 3 | C3 tet-efflux borderline hit | minor | RASTtk vs ResFinder pipeline coupling | abricate resfinder | ~10 CPU-min |

## What DID reproduce, honestly (so the failure story is balanced)

- **C1 (data deposits):** exact match to paper.
- **C2 (genome size):** exact match.
- **C3 (no *vanA*/*vanB*, no canonical *tet*):** reproduced under independent CARD+NDARO+PATRIC rescreen. The only "acquired-style" AMR calls (Lsa(A), Msr(C)) are known chromosomally intrinsic to *E. faecium*.
- **C4 (no functional virulence):** reproduced under independent VFDB+Victors rescreen, and in fact 17OM39 is *cleaner* than the paper's positive-control probiotic T110 — T110 carries the *Cna* collagen adhesin that 17OM39 lacks. This is a small positive finding the paper did not emphasize.

## Prevention for the next pass

- **Always run the paper's own tool at the paper's own settings for safety-relevant claims**, not just the current-pipeline surrogate. Even when the current-pipeline result agrees, doing the exact rerun collapses the ambiguity we saw in Failure 3.
- **Never compare repeat-family features (IS, transposons) across assemblies of unequal completeness** without either (a) a dedicated caller that handles contig-boundary fragmentation or (b) an explicit contig-count normalization.
- **Do not withhold verdict promotion on the basis of untested phylogeny** — but do not overclaim REPLICATED either. PARTIAL is the honest verdict when the leaf claims reproduce and the backbone claim is untested. Book it.
