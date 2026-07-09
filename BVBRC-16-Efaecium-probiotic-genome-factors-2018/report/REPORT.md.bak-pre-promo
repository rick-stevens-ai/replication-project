# Replication Report: Ghattargi et al. (2018)
## "Comparative genome analysis reveals key genetic factors associated with probiotic property in *Enterococcus faecium* strains"

**Paper:** Ghattargi VC, Gaikwad MA, Meti BS, Nimonkar YS, Dixit K, Prakash O, Shouche YS, Pawar SP, Dhotre DP. *BMC Genomics* 19:652 (2018).
**DOI:** [10.1186/s12864-018-5043-9](https://doi.org/10.1186/s12864-018-5043-9)
**PMC:** PMC6122445 — **PMID:** 30180794
**Open access:** ✅ (CC BY 4.0 / BMC)

**Report Date:** 2026-06-25 (promotion pass; original spot-check 2026-06-17)
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Wave 4, target #16)
**Verdict:** **PARTIAL — promoted from SPOT-CHECK.** Core AMR claim (C3) reproduced directly against BV-BRC specialty-gene tables. Virulence (C4) substantially reproduced with one noteworthy nuance. **MGE claim (C5) NOT reproduced and appears to point the opposite direction in the public BV-BRC RASTtk annotation** — but this is confounded by assembly status.

---

## 1. Paper

Compares the *E. faecium* isolate **17OM39** against a marketed probiotic (**T110**), a non-pathogenic non-probiotic (NPNP) strain, and pathogenic comparators. Reports that 17OM39 (i) clusters with T110 on the core-genome tree, (ii) lacks known *vanA*/*vanB* and tetracycline resistance genes, (iii) lacks functional virulence genes, and (iv) has higher genomic stability (fewer transposons/MGEs) — concluding 17OM39 is a credible probiotic candidate.

## 2. Claims tested

| # | Claim | Tested this pass? |
|---|---|---|
| C1 | 17OM39 + T110 deposited and adequately sequenced. | ✅ (metadata pass) |
| C2 | 17OM39 genome size / topology consistent with *E. faecium*. | ✅ (metadata pass) |
| C3 | 17OM39 lacks vancomycin / tetracycline resistance genes. | ✅ via BV-BRC sp_gene (CARD/NDARO/PATRIC) + product scan |
| C4 | 17OM39 lacks functional virulence genes. | ✅ via BV-BRC sp_gene (VFDB/Victors) |
| C5 | 17OM39 has fewer MGEs than pathogenic strains. | ✅ partial — 17OM39 vs T110 only, **opposite direction** |
| C6 | 17OM39 clusters with T110 on core-genome phylogeny. | ❌ requires Roary/PhyloPhlAn — not run |

## 3. Method (this pass)

### 3.1 BV-BRC specialty-gene rescreen (real computation)
For both genomes (17OM39 = `1352.1047`; T110 = `1344042.3`) we pulled the full BV-BRC `sp_gene` table:

```
curl 'https://www.bv-brc.org/api/sp_gene/?eq(genome_id,<GID>)
      &select(genome_id,property,source,gene,product,evidence,classification)
      &limit(2000)'
```

These records are the public, pre-computed AMR + virulence calls BV-BRC maintains by aligning each genome's annotated proteins against CARD, NDARO (NCBI AMRFinder), VFDB, Victors, and PATRIC's own AMR/VF curations — the same evidence sources the paper used (CARD/ResFinder for AMR; VFDB for virulence).

### 3.2 Full CDS feature dump (real computation)
For both genomes we pulled every CDS feature (`/genome_feature/?...feature_type=CDS`) and scanned product names locally with regex for MGE-, AMR-, and probiotic/virulence-keywords. Counts below are over 5,776 CDS (17OM39) and 5,173 CDS (T110).

### 3.3 What we did NOT run
- Roary / PGAP pan-genome → no C6 phylogeny check.
- A *de novo* ResFinder / CARD-RGI / VFDB BLAST against the FASTA. We are instead relying on BV-BRC's pre-computed alignments, which use the same reference DBs but a possibly newer DB version than the paper.
- ISEScan / ICEberg de novo MGE annotation. We are using BV-BRC RASTtk product-name tags.

## 4. Results vs Paper

### 4.1 Genome metadata (C1, C2) — unchanged from spot-check

| Strain | BV-BRC `genome_id` | Assembly | Status | Length | Source |
|---|---|---|---|---|---|
| 17OM39 (candidate) | `1352.1047` | GCF_001652715.1 | WGS, 106 contigs | 2,840,201 bp | BioProject PRJNA318315 |
| T110 (comparator) | `1344042.3` | GCA_000737555.1 | **Complete** | 2,737,963 bp | + 44 kb plasmid `1344042.14` |

→ Both deposited, both sized correctly for *E. faecium*. ✅

### 4.2 AMR rescreen (C3) — REPRODUCED

BV-BRC sp_gene table, property = "Antibiotic Resistance":

| Genome | Total sp_gene | AMR rows | CARD | NDARO | PATRIC | `van*` hits | `tet*` hits |
|---|---|---|---|---|---|---|---|
| 17OM39 | 158 | **56** | 18 | 3 | 35 | **0** | **0** |
| T110 | 148 | **52** | 14 | 3 | 35 | **0** | **0** |

Cross-check via local product-name scan on all 5,776 (17OM39) and 5,173 (T110) annotated CDS:

- **vancomycin / vanA / vanB / vanC**: **0** matches in either genome. ✅
- **tetracycline / tetM / tetO / tetL**:
  - 17OM39: **1** CDS annotated as `tetracycline resistance MFS efflux pump` (no canonical gene symbol). **Minor discrepancy** — the paper's ResFinder run reported zero. This is plausibly (a) a divergent MFS pump below ResFinder's identity threshold but flagged by RASTtk on homology, or (b) a false-positive RAST annotation. It is NOT a canonical `tetM/L/K/O` ribosomal protection gene.
  - T110: 0.

→ **Paper's central safety claim (no vanA/vanB and no tetracycline-resistance genes in 17OM39) is reproduced** for the canonical loci. One additional borderline efflux annotation worth caveating.

The AMR rows that ARE present in both genomes are nearly all **intrinsic / housekeeping** alignments — translation elongation factors (EF-Tu, EF-G), gyrase B, isoleucyl-tRNA synthetase, DHFR, D-Ala-D-Ala ligase, LiaFSR cell-envelope-stress system — i.e. the conserved targets of antibiotics that CARD lists for completeness. The only acquired-style AMR call shared by both is `Lsa(A)` and `Msr(C)` ABC-F ribosomal-protection proteins, which are known to be **chromosomally encoded and intrinsic to *E. faecium*** (not acquired). This is fully consistent with the paper's "no acquired AMR" conclusion.

### 4.3 Virulence rescreen (C4) — MOSTLY REPRODUCED, with a real difference

BV-BRC sp_gene, property = "Virulence Factor" (VFDB + Victors + PATRIC_VF):

| Genome | VF rows | Notable hits |
|---|---|---|
| 17OM39 | 18 | All housekeeping or *probiotic-associated*: MalR, ClpP, EF-LepA, methionine aminopeptidase, thymidylate synthase, **choloylglycine hydrolase (= bile salt hydrolase, a *probiotic* trait)**, PerR. **No collagen-binding protein, no Esp, no cytolysin, no gelatinase, no aggregation substance.** |
| T110 | 19 | Same housekeeping set **PLUS Collagen binding protein Cna (VFDB)** — a *bona fide* virulence/adhesion factor. |

→ The paper's claim that **17OM39 lacks functional virulence genes is reproduced**. Notably, 17OM39 is *cleaner* on this axis than the comparator probiotic T110 — T110 carries the `Cna` collagen adhesin (a known *E. faecium* virulence factor), which 17OM39 does not. This is actually a small **positive finding for 17OM39's safety profile** that the paper did not emphasize.

Most "VF" hits on both genomes are essential housekeeping enzymes that VFDB/Victors list as conditional virulence factors only because they appear in PATRIC's curated VFDB-derived set. The biologically interesting result is the **presence/absence of `Cna`**.

### 4.4 MGE comparison (C5) — NOT REPRODUCED (opposite direction, with caveat)

Product-name scan of full CDS sets for MGE keywords:

| MGE term | 17OM39 (5776 CDS) | T110 (5173 CDS) |
|---|---|---|
| transposase | **66** | 21 |
| mobile element | **56** | 25 |
| phage | **47** | 19 |
| integrase | **26** | 4 |
| recombinase | 18 | 12 |
| resolvase | 10 | 3 |
| site-specific recombinase | 8 | 0 |
| invertase | 3 | 1 |
| prophage | 2 | 0 |
| insertion sequence | 0 | 1 |
| conjugal (TraE) | 1 | 1 |
| **TOTAL MGE-like CDS** | **237 (4.10%)** | **87 (1.68%)** |

→ **17OM39 has ~2.7× as many MGE-like CDS as T110, by raw count and by fraction of CDS.** This is the OPPOSITE of the paper's C5 claim that 17OM39 is "more genomically stable" than comparator strains.

**Important caveat — assembly-status confound.**
- 17OM39 is a **draft (106 contigs)** assembled by SPAdes from short reads.
- T110 is a **finished/complete** genome.

Draft assemblies massively inflate transposase counts because (a) repetitive IS elements break contigs, so a single IS gets reported as multiple partial CDS at contig boundaries, and (b) ambiguous repeats often get collapsed in finished assemblies. The 17OM39 vs T110 inequality is therefore **not a fair like-for-like MGE test**. The paper's actual C5 comparison was 17OM39 vs *pathogenic clinical* isolates (also finished/draft variability), which we did not pull this pass.

**Honest interpretation:** the paper's C5 conclusion cannot be rejected from this evidence, but the public BV-BRC RASTtk annotation does NOT, on its face, support "17OM39 has fewer MGEs than T110" — if anything the raw counts go the other way. Resolving this would require (a) running ISEScan/digIS on both genomes' FASTAs to do proper IS counting that ignores contig-break duplicates, and (b) including the paper's actual pathogenic comparators (e.g. DO, Aus0004, TX16) in the comparison.

### 4.5 Probiotic-associated genes (C4-positive / paper's other angle)

| Feature | 17OM39 | T110 |
|---|---|---|
| Bile salt hydrolase (choloylglycine hydrolase) | 3 | 3 |
| Bacteriocin / enterocin | 9 | 13 |
| Sortase A (LPxTG) | 13 | 9 |
| LPxTG cell-wall anchored proteins | 6 | 6 |
| Adhesin (generic) | 1 | 0 |
| Pilus assembly | 0 | 1 |
| Collagen-binding Cna | 0 | **1** |

→ Both strains have a comparable probiotic toolkit (bile tolerance, bacteriocin production, surface anchoring). Consistent with the paper's C4-positive subclaim that probiotic-associated genes are shared between T110 and 17OM39.

## 5. Verdict

**PARTIAL — promoted from SPOT-CHECK to PARTIAL.**

| Claim | Reproduced? |
|---|---|
| C1 (data deposits) | ✅ Exact |
| C2 (genome size) | ✅ Exact |
| C3 (no vanA/vanB, no tet) | ✅ Reproduced (one minor MFS-efflux caveat in 17OM39) |
| C4 (no functional virulence) | ✅ Reproduced — 17OM39 cleaner than even T110 (no Cna) |
| C5 (fewer MGEs) | ❌ Public BV-BRC RASTtk shows OPPOSITE; confounded by 17OM39 draft vs T110 complete; needs ISEScan rerun |
| C6 (core-genome cluster with T110) | ⬜ Not tested (needs Roary/PhyloPhlAn) |

**Honest scorecard: 4 of 6 testable claims reproduced; 1 explicit miss with a known confound; 1 untested.**

Not bumped to REPLICATED because (a) C6 — the central phylogenetic claim — was not re-run, and (b) C5 has a real disagreement with public data that needs a finished-vs-finished or ISEScan rerun to adjudicate.

To promote to REPLICATED, run:
1. `prokka` + `roary -p 8 -i 90 -e --mafft` on the 4 paper strains (17OM39 GCF_001652715.1, T110 GCA_000737555.1, Aus0004 GCA_000250945.1 as a representative pathogenic comparator, and one NPNP). Build the core-gene tree with FastTree and confirm 17OM39 sister to T110 — directly tests C6. (~6-8 CPU-h.)
2. `ISEScan` on the FASTAs of all four genomes (not RAST product names) for a fair MGE count — directly re-tests C5. (~2 CPU-h.)
3. `abricate --db resfinder` and `abricate --db vfdb` on the FASTAs at 2026 DB versions to confirm AMR + VF rescreen — already largely covered by §4.2–4.3 above but uses the exact DB the paper used. (~10 CPU-min.)

Total to full REPLICATED: ~10 CPU-h. Not gated by data availability — gated only by having `prokka`/`roary`/`ISEScan`/`abricate` installed.

## 6. Coverage / Agreement

- **Coverage: 6 / 10** — up from 3/10. We now have AMR rescreens against CARD+NDARO+PATRIC, virulence rescreens against VFDB+Victors, full CDS-table MGE scans, and head-to-head probiotic-gene comparison for both 17OM39 and T110. Missing: phylogeny (C6) and the paper's pathogenic comparators.
- **Agreement: 8 / 10** — C1, C2, C3, C4 reproduce cleanly; one minor (1-CDS MFS-efflux) discrepancy in C3; C5 does not reproduce on raw counts but is confounded by assembly status; C6 untested.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST API | Bibliographic. | Free. |
| BV-BRC public API | sp_gene + genome_feature dumps. | Free. |
| Compute | curl + python3 regex; ~5 min wall. | Negligible. |

## 8. Tools / Datasets / Hardware

**Used:** Europe PMC, BV-BRC `/sp_gene/` and `/genome_feature/` endpoints, curl, python3.
**Required for full REPLICATED:** prokka, roary, FastTree, ISEScan, abricate (+ ResFinder/VFDB DBs). All free; ~10 CPU-hours.

## 9. Limitations

- **Annotation pipeline coupling:** BV-BRC's AMR + VF calls use CARD/NDARO/VFDB but via RASTtk's alignment + threshold choices, not the paper's original ResFinder/CARD runs. Agreement therefore tests "do the same conclusions hold under a *current* pipeline?" rather than "do the *exact* numbers reproduce?". This is a feature, not a bug, for safety-relevant claims like C3 — if anything it's a stiffer test.
- **C5 confound:** raw transposase/IS counts inflate in draft assemblies. ISEScan on the FASTAs would resolve this.
- **C6 untested:** the paper's "17OM39 clusters with T110" is the most paper-specific result and needs Roary.
- **No pathogenic comparator pulled this pass:** paper's full picture is 17OM39 vs T110 vs NPNP vs *pathogenic* strains. We only loaded 17OM39 + T110.
- **Sample size is two genomes.** A real probiotic safety case would compare 17OM39 against >10 *E. faecium* clinical isolates and >10 commercial probiotic isolates; the paper does not, and neither does this pass.

## 10. Reproducibility-blocker critique (mandatory 6/22 rule)

The single biggest reproducibility hazard in the original paper is **C5 (the MGE-stability claim).** The paper does not publish:
1. The exact ISEScan / IScompass / equivalent command line and version used to count "transposons" — without this, "fewer MGEs" is a soft claim.
2. The list of pathogenic comparator accessions used as the MGE baseline.
3. How draft-vs-complete assembly status was controlled for in the MGE comparison.

Our re-analysis of the public BV-BRC RASTtk product calls actually finds 17OM39 carrying ~2.7× more MGE-like CDS than T110 — pointing the opposite direction from the paper. Without the paper's exact MGE-counting command, neither result can be cleanly adjudicated. **This is the canonical "underspecified methods" reproducibility failure** and is the reason a full REPLICATED verdict is being withheld even though the AMR + VF safety claims (C3, C4) — which actually matter for the probiotic-safety conclusion — do reproduce.

C3 and C4, the central safety claims, are robust under independent BV-BRC reannotation. That is the part of the paper that matters most clinically, and it survives.

## Evidence index

- `evidence/europepmc_ghattargi2018.json` — bibliographic.
- `evidence/bvbrc_17OM39_strain.json`, `evidence/bvbrc_T110_probiotic_strain.json` — genome metadata.
- `evidence/sp_gene_1352.1047.json`, `evidence/sp_gene_1344042.3.json`, `evidence/sp_gene_1344042.14.json` — full BV-BRC specialty-gene tables (AMR + VF + transporters + drug targets + metal resistance).
- `evidence/sp_gene_summary.json` — derived AMR/VF summary across both genomes.
- `evidence/features_1352.1047.json`, `evidence/features_1344042.3.json` — full CDS feature dumps (5,776 and 5,173 rows).
- `evidence/feature_scan_summary.json` — MGE + AMR + probiotic-VF keyword counts.
