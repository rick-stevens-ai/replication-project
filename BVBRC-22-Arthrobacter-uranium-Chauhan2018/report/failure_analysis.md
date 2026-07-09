# Failure Analysis — BVBRC-22-Arthrobacter-uranium-Chauhan2018

**Verdict: PARTIAL** (Coverage 8/10, Agreement 8/10; independent LLM judge gpt-5.2).

This document dissects *why* the verdict is PARTIAL rather than FULL, and separates true replication failures from documented substitutions and out-of-scope items.

---

## 1. What replicated cleanly

| Claim | Paper | Rerun | Outcome |
|---|---|---|---|
| Genome size | 4,564,701 bp | 4,564,701 bp | Exact match — the deposited assembly IS the one the paper analysed, and prodigal's summary agrees with the paper's pipeline (RAST/IMG/PGAAP) at the assembly-arithmetic level. |
| GC content | 64.1% | 64.1% | Exact match. |
| CDS count | 4327 | 4327 | Exact match; strongly suggests gene-caller choice (prodigal vs RAST) does not meaningfully perturb this genome. |
| Contigs | 93 | 93 | Property of the deposited assembly; trivially reproduced. |
| ANI to *P. aurescens* TC1 | 80.28% (JSpecies BLAST-ANI) | 80.58% (fastANI) | Within 0.3% — well inside the expected inter-tool noise band for ANI, and both values place the pair below the ~95% genomic species boundary. |
| Metal/metalloid resistance (As, Cu, Cd, Cr, Zn/Co, Fe) | qualitative complement asserted from RAST subsystems | 132 BacMet2 hits across the same six categories | Qualitatively reproduced with a modern, curated DB. |
| No clinical AMR profile (environmental isolate) | implied | 0 NCBI/CARD antibiotic-AMR hits | Clean negative control. |

## 2. What did NOT fully replicate, and why

### 2a. Lineage-specific gene count (858 vs 1159)
- **Nominal delta:** ~26% fewer lineage-specific CDS than the paper reports.
- **Contributing factor A (tool substitution):** EDGAR (paper) uses orthology + pan/core-genome partitioning; the rerun uses `diamond blastp` best-hit with id ≥ 30% / qcov ≥ 50%. Best-hit is *more permissive at declaring shared* (i.e., fewer "unique" calls) than EDGAR's stricter orthology-group definition.
- **Contributing factor B (comparator substitution):** The paper's exact comparator strains *A. globiformis* NBRC 1237 and *A. cupressi* CGMCC1 have no public assemblies under those tags; substitutes (DSM 24664, CNM05) were used. Different comparator content re-partitions the "unique to focal" set.
- **Classification:** Documented method + comparator substitution, not a true replication failure. Same order of magnitude, qualitative claim (hundreds to ~10³ niche-specific CDS) intact.

### 2b. antiSMASH biosynthetic-gene-cluster (BGC) mining — NOT RERUN
- **Reason:** antiSMASH was not installed on the compute host at the time of the rerun.
- **Consequence:** The paper's secondary-metabolite / niche-specialty BGC claim is entirely unaudited by this replication. This is the single largest gap and the dominant reason the verdict is PARTIAL, not FULL.
- **Classification:** Infrastructure gap, not a scientific disagreement.

## 3. What neither the paper nor the rerun demonstrated

These are shared limitations, not asymmetries between paper and rerun. They are what keep the "uranium tolerance" claim genomically-supported but not mechanistically proven:

1. **No direct uranyl-ion tolerance assay** — no MIC, no growth-under-U(VI), no biosorption / bioaccumulation quantification.
2. **No transcriptomic response** to U(VI) exposure — cannot show that the annotated metal-resistance loci are actually induced under uranium challenge.
3. **No uranium-specific determinant identified at the sequence level** — the BacMet2 catalog covers other heavy metals; uranium tolerance is inferred by proxy from generic metal-resistance complement plus isolation-site provenance.
4. **No mobile-element / horizontal-transfer analysis** — biosafety and evolutionary-dynamics implications of any candidate tolerance loci are unaddressed.
5. **No pan-genus pan-genome** to test whether the "niche-specific" gene set is actually restricted to uraniferous-soil isolates vs. broadly distributed across Arthrobacter.

## 4. Root-cause summary

| Failure mode | Category | Recoverable how? |
|---|---|---|
| Lineage-specific count differs from paper | Tool + comparator substitution (documented) | Rerun with EDGAR (or roary/panaroo) on the paper's exact strains once available. |
| antiSMASH not rerun | Infrastructure gap | Install antiSMASH on the compute host and rerun; no scientific obstacle. |
| No uranium phenotype | Out-of-scope for genomic replication; also absent from paper | Would require wet-lab MIC and ICP-MS uptake work, or transcriptomic uranium-challenge RNA-seq. |
| No mobile-element / HGT audit | Not attempted here or in paper | MOB-suite / ICEberg / geNomad pass on the assembly is cheap and could be added. |
| No pan-genus context | Not attempted here or in paper | Assemble a ≥50-genome Arthrobacter panel and rerun the pan-genome analysis. |

## 5. Bottom line
The **genome-level bookkeeping** of Chauhan et al. (2018) reproduces cleanly. The **biological thesis** — that this organism is uranium-tolerant *because* of its metal-resistance gene complement — is not directly demonstrated by the paper and could not be directly reproduced by a genomic replication either. That structural gap is what keeps the verdict at PARTIAL, and it motivates the five open questions filed alongside this report.
