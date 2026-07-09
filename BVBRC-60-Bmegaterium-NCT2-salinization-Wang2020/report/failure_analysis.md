# Failure analysis — BVBRC-60 (Priestia megaterium NCT-2, Wang et al. 2020)

Paper: doi:10.1155/2020/4109186 · PMID 32190639 · PMCID PMC7066406
Verdict: **REPLICATED** (coverage 1.00, agreement 1.00)

This document records what *could* have failed, what *did* differ, and what the reader should treat as a soft rather than hard confirmation.

---

## 1. Nothing catastrophic failed

All six testable claims (C1–C6) reproduced with either exact matches or sub-0.3% rounding-level deltas. There is no hard failure to analyse, so this file focuses on the near-misses, the substituted methods, and the residual uncertainty.

## 2. Numeric discrepancies (all classified MINOR-DIFF)

| Where | Paper | Reproduced | Delta | Interpretation |
|---|---|---|---|---|
| Whole-genome GC | 37.87% | 37.78% | −0.09% abs | Rounding-level; consistent with the paper's v.1 annotation vs the current v.3 assembly. |
| Chromosome GC | 38.2% | 38.18% | −0.02% abs | Rounding. |
| Plasmid GC range | 33.7–37.0% | 33.65–37.02% | ±0.05% | Rounding. |
| Total genes (incl. pseudo) | 6,039 | 6,038 | −1 gene | Annotation-pipeline evolution across GenBank versions. |
| CDS / proteins | 5,606 | 5,605 (proteins) | −1 protein | Same. |
| RNA / pseudogene / tRNA / rRNA subcounts | as claimed | exact | 0 | No delta. |
| 6-strain Table 1 sizes / GC | as claimed | agree to ≤0.04% | ≤0.04% | Rounding. |

None of these deltas invalidate any qualitative claim in the paper. All are attributable to annotation-pipeline drift between GCA_000334875 v.1 (used by the authors) and v.3 (current NCBI record), and to the authors' rounding conventions.

## 3. Method substitutions (acknowledged)

- **Phylogeny.** The paper used CVTree + 16S NJ + MAUVE. The replication used `fastANI` for the pairwise-ANI ordering. This is a substitution, not a re-implementation. It could have failed if the two methods disagreed on the top-2 ordering; they did not (DSM 319 first, QM B1551 second in both). If they had disagreed, the correct next step would have been to rerun CVTree rather than declare a disagreement between paper and replication.
- **Functional gene evidence.** The replication grep-searches product strings in the deposited GFF rather than running an HMM (Pfam/TIGRFAM) or ortholog assignment (OrthoFinder). Presence/absence is therefore evidence-of-name, not evidence-of-structure. A miscurated product line would score identically to a real hit. For the qualitative-inventory claim in the paper this is adequate; for a structural or activity claim it would not be.
- **LLM judge.** The final REPLICATED label is emitted by an Argo `gpt-5.2` LLM over the claim/result JSON. The judge does not add evidence. If the judge disagreed with the numeric agreement table, the numeric table wins.

## 4. Non-testable elements

- **C7 (wet-lab provenance).** Isolation from secondary-salinized greenhouse soil, CGMCC 4698 deposit, and the HiSeq 4000 + PacBio RSII hybrid workflow cannot be verified from the deposition alone. This is not a replication failure — it is a limit of what the deposition surface exposes.

## 5. Failure modes that were *avoided*

Recording these so a future replicator does not stumble into them:

- **Wrong assembly version.** GenBank still lists the earlier 204-contig draft (v.1); using it would have failed C1 (no 10 discrete plasmid replicons) and would have produced non-matching annotation counts. The replication uses v.3 (Complete Genome) — the version consistent with the paper's Data Availability.
- **RefSeq vs GenBank confusion.** GCF_000334875.3 (RefSeq) and GCA_000334875.3 (GenBank) are mirrored but annotated by different pipelines and can produce different gene counts. The replication uses the GenBank record (GCA), which matches the paper's counts more closely.
- **Reclassification.** The organism was reclassified from *Bacillus megaterium* to *Priestia megaterium* (Gupta et al. 2020). NCBI records may return the new binomial while the paper uses the old one. This is a naming change only; the same physical genome and the same accession are involved. A search that assumed the *Bacillus* binomial only would still succeed via the CGMCC / accession routes.
- **fastANI reporting cutoff.** fastANI returns no line for pairs below ~80% ANI. The three non-*megaterium* comparators (*B. subtilis* 168, *B. cereus* Q1, *B. licheniformis* DSM 13) correctly produced no lines. This absence *is* the evidence they are distant, not a tool failure; a naive interpretation would have flagged it as missing data.

## 6. Residual uncertainties (referred to `open_questions.json`)

The replication does not, and cannot, establish:

- Whether the observed gene set actually *causes* the salinization/PGPR phenotype (only that it is present in the genome).
- Whether the "incomplete Trp-dependent" IAA pathway produces measurable IAA in culture.
- Which replicon (chromosome or which of the 10 plasmids) carries each functional inventory, and how phenotype-stable NCT-2 is under plasmid loss.
- Whether phosphate solubilization is preserved under salinity stress.
- Whether NCT-2 is remarkable within the modern *Priestia megaterium* pangenome, which now contains many complete genomes beyond the 5-strain 2020 comparator set.

These are experimental / broader-informatic questions, not failures of this replication; they are exposed as O1–O5 in `open_questions.json`.

## 7. Bottom line

No hard failure. Numeric agreement to ≤0.09% on all continuous metrics and to ≤1 count on all discrete metrics. Two methodological substitutions (ANI for CVTree; grep for HMM) are documented and did not change the substantive verdict. The REPLICATED label attaches to the paper's *informatic* description of the NCT-2 genome; the paper's *causal* / phenotype-attribution story is neither confirmed nor refuted by this work and is properly the subject of the follow-up questions in `open_questions.json`.
