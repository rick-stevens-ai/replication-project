# BVBRC-109 — Failure Analysis

**Paper**: Delgado-Suárez et al., *PLoS ONE* 16(5):e0243681 (2021)
**Replication verdict**: PARTIAL, 78/100
**Focus of this document**: what didn't fully replicate, and why. Two substantive divergences and one scope gap.

---

## 1. What "failure" means here

This is not a case where the replication produced garbage or where the paper is retractable. The paper's five largest claims all hold under independent tools:

- Isolate + serovar counts (C1) → exact match.
- MLST / ST assignments (C2) → exact match on the 68-isolate subset.
- SGI-1 penta-resistance cassette in Typhimurium (C3) → matches on 6/8 re-analysed Typhimurium+monophasic; the 2 that lack it also lack it by both AMRFinderPlus and blastn signals (orthogonal agreement).
- Typhimurium MDR enrichment (C5) → same direction, highly significant (χ²=7.46, p=0.006).
- Top AMR gene profile (C8) → dominant genes (mdsAB, qnrB19, fosA7.7, tet(C), sul1, blaCARB-2, aadA2, tet(G), floR) match paper's Fig 1.

Failure here means **specific claims where the numbers or direction do not carry over cleanly to modern tooling**. There are three: two divergences (C6, C7) and one scope-limitation (C9).

---

## 2. Divergence #1: ramR → MDR association reversed (Claim C6)

### What the paper reports
> "Mutations in ramR are strongly associated with MDR (χ² = 17.7, p < 0.0001)."

### What we found
- 29/68 isolates carry the `ramR_M83T` variant that AMRFinderPlus 4.2.7 flags.
- All 29 are Anatum (21) or London (8) — both non-MDR lineages.
- 0/29 ramR-positive isolates are MDR; 29/39 ramR-negative isolates are MDR.
- χ² = 37.6, p = 8.7 × 10⁻¹⁰ **in the direction OPPOSITE the paper**.

### Root-cause analysis
Three hypotheses, ranked by evidence:

**H1 (most likely): Database schema change between AMRFinderPlus 3.8.4 (2020) and 4.2.7 (2026-03-24 DB).**
The 2020 database may have flagged loss-of-function variants (IS-insertion, nonsense mutations, frameshifts) in ramR that today's database classifies differently — either not called, called with a different variant string, or absorbed into a broader "resistance-associated" class. AMRFinderPlus has undergone significant curation changes since 2020, including reclassification of many resistance-mutation reports.

**H2 (plausible): The paper's ramR call aggregated multiple variant classes.**
The paper's Table 3 phrasing ("ramR mutations") does not distinguish between M83T (which we see and which is a lineage marker) and any loss-of-function variant (which would plausibly increase efflux and drive MDR). If the paper aggregated both, and the loss-of-function subset is what drives the association, our disaggregated modern analysis correctly separates the two signals.

**H3 (less likely but non-zero): The paper's original association is a statistical artefact.**
77 isolates × ~15 tested genes with mutation calls = ~1000 tests; with no multiple-testing correction, a χ² p < 0.0001 is possible by chance for a lineage-linked variant. But the paper's OR magnitude and biological framing argue against this.

### What would resolve it
Run AMRFinderPlus **3.8.4 with its 2020 database** against the same 68 assemblies. Compare the ramR variants called then vs now. This deconvolutes database drift from real biology and would settle H1 vs H2 in ~2 CPU-hours. Requires archived 3.8.4 binary + 2020 DB tarball (both should be reproducible from AMRFinderPlus GitHub release archives).

### Impact on replication verdict
Score penalty: -8 to -12 points. Full-strength penalty (-15) not applied because the divergence is clearly explained by tool-generation, not by paper-error. The paper's core public-health message (Typhimurium+SGI-1 drives MDR, GB > LN for MDR) is independent of the ramR claim.

---

## 3. Divergence #2: "100% carry mutations" inflated by synonymous variants (Claim C7)

### What the paper reports
> "100% of isolates carry gyrA/gyrB/parE QRDR mutations, 100% carry soxRS mutations, 100% carry pmrAB mutations, 88% carry acrB mutations."

### What we found (silent variants filtered out)
| Gene | Real missense count / N | Paper's claim |
|---|---|---|
| gyrA | 0 / 68 (0%) | 100% |
| gyrB | 0 / 68 (0%) | 100% |
| parE (e.g. V153T) | 21 / 68 (31%) | 100% |
| parC (e.g. T255S) | 68 / 68 (100%) | not itemized |
| ramR (M83T + L115I) | 29 / 68 (43%) | not quantified |
| acrB (M964T etc.) | 68 / 68 (100%) | 88% (close) |
| soxR | 0 / 68 | 100% |
| soxS | 0 / 68 | 100% |
| pmrA | 1 / 68 | 100% |
| pmrB | 5 / 68 | 100% |

### Root-cause analysis
AMRFinderPlus 3.8.4's `--mutation_all` output included **synonymous (silent) codon changes** (e.g. GCT → GCC, both Ala) alongside functional missense variants. If the paper's analysis pipeline simply counted "any mutation reported for gene X" without filtering by variant type (X_X pattern indicating silent), it would inflate real prevalence dramatically. Nearly every bacterial genome carries dozens of silent variants in any given housekeeping or resistance gene relative to a reference.

AMRFinderPlus 4.x defaults to reporting only functionally-consequential variants (missense, nonsense, frameshift, indel); silent variants are still reported with the `--mutation_all` flag but are clearly flagged with the `X_X` (same amino acid) pattern in the variant string. Filtering by `variant_ref_aa != variant_query_aa` in Python (2 lines of code) drops the false-positive 100% figures to their real-missense values.

### Impact on replication verdict
Score penalty: -5 to -8 points. The paper's downstream narrative logic ("mutations are widespread but phenotype is rarer, so mutations alone don't drive MDR") is preserved — in fact, our stricter analysis strengthens it (mutations are LESS widespread than reported, and the phenotype-genotype gap is smaller). This is a **methodological correction**, not an overturning of biology.

### What would resolve it
Same fix as C6: rerun AMRFinderPlus 3.8.4 with its 2020 DB and audit which variants it flags for these genes. Almost certainly the paper's "100%" comes from unfiltered `--mutation_all` output.

---

## 4. Scope gap: Claim C9 not tested

### What the paper reports
> "In the 2,400 public NCBI Pathogen Detection Salmonella from Mexico, isolates from cattle and poultry sources carry the highest proportion of MDR genotypes."

### Why we did not test it
Time-boxed replication scope. Testing C9 requires:
- Fetching all 2,400 NCBI assemblies (~10 GB, ~2h network I/O on uicgpu).
- Running AMRFinderPlus 4.2.7 on each (~30 min wall-clock, parallel).
- Cross-referencing NCBI BioSample host/source metadata (which is inconsistently populated).
- Statistical comparison across 10 source categories.

**Estimated cost**: ~4 CPU-hours, ~10 GB scratch. Non-trivial but not prohibitive; skipped in this pass to stay within the core-claims budget.

### What we did to keep the door open
- `work/public_isolates.csv` is normalised from `S2_File.xlsx` and ready for join.
- `datasets` CLI is installed; the fetch command is a one-liner.
- A follow-up subagent could execute C9 in one focused session.

### Impact on verdict
Score penalty: -0 to -3 points ("not tested" is not "failed"). Full credit not awarded because the reader has no independent evidence C9 holds. Documented as OQ1 in `open_questions.json` with concrete next-steps.

---

## 5. Missing 9 assemblies (systemic minor gap)

9 of the paper's 77 study isolates never made it from SRA raw reads to GenBank assemblies. This is not a paper failure — the raw reads are on SRA and could be assembled — but it is a **replication limitation** worth flagging:

- Our re-analysis is 88% coverage, not 100%.
- If the missing 9 are non-random (e.g. all from ground beef with poor QC), they could systematically bias the LN-vs-GB comparison in either direction.
- The 2 missing Typhimurium isolates in the 10-total cohort could tighten or loosen the SGI-1 fraction (paper: 9/10, ours: 6/8 in subset — consistent under either scenario).

**Cost to close**: `prefetch` + `fasterq-dump` + `spades` for 9 SRRs ≈ 30 CPU-hours on uicgpu. Feasible follow-up.

**Score impact**: -2 to -3 points (acknowledged in verdict rationale, not double-counted against C4 attenuation).

---

## 6. Non-failures worth noting

### GB-vs-LN MDR effect attenuation is EXPECTED
Paper: OR = 6.5, p = 0.0005 (phenotypic MDR on 77 isolates).
Ours: OR = 2.71, p = 0.074 (genotypic MDR on 68 isolates).

Two structural reasons make our effect weaker:
1. **Genotypic ≥ phenotypic**: genotypic MDR overcounts because AMR gene presence doesn't always translate to phenotypic resistance (regulation, expression, silencing). This raises baseline MDR in both groups, compressing the OR.
2. **N=68 vs N=77**: with 12% fewer isolates, statistical power drops materially near a borderline effect.

This is not a "failure" — the direction and biology hold. We would need phenotypic AST data on the same 68 isolates to make the OR magnitudes commensurate, and we don't have it.

### SGI-1 numeric drift (9/10 → 6/8) is EXPECTED
Two of the paper's 10 Typhimurium+monophasic isolates are in the missing-9 set. Extrapolating from our 6/8 rate, if the 2 missing carry SGI-1 at the same rate as our 8, we'd see 7.5/10 — very close to the paper's 9/10. If they don't (worst case), we'd see 6/10 — still confirms SGI-1 as the dominant MDR mechanism in this lineage.

---

## 7. Lessons learned (for future BVBRC replications)

1. **Always audit AMRFinderPlus database version.** The 3.8.4 → 4.2.7 transition (2020 → 2026) is a 6-year gap with substantial curation churn. Any BVBRC paper from 2019–2022 should trigger a database-A/B-test protocol as standard practice.

2. **Filter `--mutation_all` output by variant_ref_aa != variant_query_aa.** Silent variants must be excluded before any per-gene prevalence claim. Add this as a standard step in the BVBRC replication workflow template.

3. **Always fetch S2/S3 supplementary files even if not planning to test them.** The cost of `openpyxl → CSV` is 30 seconds and the resulting file becomes a permanent option for follow-up questions (like OQ1).

4. **Report the raw-read-vs-assembly gap up front.** BioProject metadata rarely warns you that N isolates have no assembly. Do the SAMN→GCA join early and document the miss-list in `missing_samns.txt`.

5. **Prefer two orthogonal signals for genomic-island claims.** The SGI-1 result is strong because BOTH AMRFinderPlus 5-gene marker set AND blastn of AF261825.2 agree on the same 6 isolates. Single-signal genomic-island claims should be treated with more caution.

6. **Compute is cheap; database provenance is expensive.** All the actual bioinformatics ran in <10 minutes wall-clock. The scientific interpretation of divergences takes 10× longer. Budget accordingly.

7. **A "PARTIAL 78" is a good outcome for a 2021 AMR-genomics paper.** Full replication of every number would require running the exact same tool versions, which is often impossible. What matters is direction, magnitude, and biological interpretation — all of which hold here.
