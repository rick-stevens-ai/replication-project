# Papers Where Replication Found Problems With the Paper
*Compiled by Ollie, 2026-06-25. Disk-verified from the actual REPORT.md verdicts (not parser auto-tags).*

"Problem with the paper" = our replication surfaced a **substantive defect in the source
paper itself** — an inverted/contradicted claim, an internal inconsistency, an impossible
number, an undisclosed method, or a non-reproducible-by-design analysis. This is distinct from
"we couldn't replicate because the data is paywalled," which is a *deposition* blocker, not a
paper defect.

Ranked roughly by severity.

---

## A. CONTRADICTED — replication inverts or refutes the paper's headline claim

| Paper | Collection | The problem |
|---|---|---|
| **lucid100-ldir-stroke-motor-recovery-brain-rewiring** | LUCID-100 | Re-analysis of the paper's only public deposit (GEO GSE244016) shows the **opposite** of its headline: at the D3 timepoint pro-inflammatory cytokines go **UP** under low-dose IR (not down) and homeostatic-microglia markers go **DOWN** (Wilcoxon p≈0.006 / 0.027) — directly contradicting "LDIR resolves inflammation / restores homeostatic microglia." (6 wet-lab pillars have no deposit → out of scope.) |
| **28589945-ARG-dissemination** | OSTI/general | Independent re-derivation contradicts the paper's reported homology/identity figure (the 93% claim does not hold on re-BLAST). Scored PARTIAL/CONTRADICTED on the key quantitative claim. |
| **BVBRC-08-Lplantarum-DJF10-Kandasamy2022** | BV-BRC | (verdict PARTIAL+ overall) but flagged: several genomic-island / specialty claims could not be reproduced; auto-tagged CONTRADICTED on a sub-claim. *Lower severity — most claims verified.* |
| **lucid-matsuya-nte-integrated** | LUCID-100 | **Table 2 has a wrong exponent** (β_b off by orders of magnitude) — a typographical/units error in the published table. |

## B. INTERNAL INCONSISTENCY / IMPOSSIBLE VALUES

| Paper | Collection | The problem |
|---|---|---|
| **lucid100-snp-occupational-radiosensitivity** | LUCID-100 | Re-derived genotype counts + exact HWE expose **5 real defects**: (1) 7/16 odds ratios are mathematically inconsistent with the stated allelic model (they secretly match a dominant/recessive model, unlabelled); (2) headline 4-allele "enrichment" **fails directionally in 5/16 strata**; (3) an **impossible p = 4.736** (column-shift typo); (4) 9/16 control panels **violate HWE** despite the paper claiming HWE was tested; (5) no multiple-testing correction. Verdict PARTIAL — headline more fragile than the abstract claims. |
| **lucid100-low-dose-ct-gene-expression-dna-integrity** | LUCID-100 | (verdict REPLICATED) but our re-analysis found the paper applied an **unpaired test (Mann-Whitney) to intrinsically paired γ-H2AX data**; the correct paired test flips their "non-significant" p=0.37 → **p=0.043** (significant). A statistical-methods defect, candidate for a technical note. |
| **lucid100-celegans-americium-ingestion-model** | LUCID-100 | Headline dosimetry number (0.748 µSv) is **physically suspect** — implies Am-241 well activity ~6 orders of magnitude below the NRC exempt quantity and below alpha-counting detection limits, yet the paper claims p<0.001 reproductive toxicity. **Predatory-adjacent venue** (Sciencedomain/ARRB; not DOAJ, not Scopus, 0 citations). Verdict NO-GO + recommended **DEMOTE** from LUCID-100 and replace. |

## C. NON-REPRODUCIBLE-BY-DESIGN (undisclosed methods / data only in figures)

| Paper | Collection | The problem |
|---|---|---|
| **lucid100-rt-dna-repair-tp53-apoptosis-model** | LUCID-100 | ~80% of the quantitative content (Figs 7–14, 17, 18) is **physically impossible to reproduce from the paper text** — the governing formulae and fitted parameters live only in the author's prior closed / figure-embedded publications. Only ~20% is in-principle reproducible. Verdict SPOT-CHECK. |
| **lucid-dsb-repair-history-review-triage** | LUCID-100 | Paper **does not provide the underlying (x,y) data pairs** — they exist only as scatter points in a figure; key relationships not reproducible without de-plotting. |
| **BVBRC-06-Smaltophilia-iron-Kalidasan2018** | BV-BRC | "DyP exclusivity" claim is a **RAST-version annotation artifact**, not a biological finding — the gene is present in all 4 strains, partially contradicting the K279a-exclusivity claim (may reflect subsystem reassignment between RAST versions). |

---

## Notes / caveats
- **Parser false-positives excluded:** earlier auto-tagging marked several REPLICATED/PARTIAL
  papers as "CONTRADICTED" because the word appeared in a *finding within* the report
  (e.g. "does not contradict the paper"). Those were read and excluded here.
- **The ldir-stroke CONTRADICTED is the campaign's cleanest inverted-claim result** and the
  highest-value negative finding — it refutes a published headline using the authors' own data.
- **Highest-confidence, most actionable for follow-up:** ldir-stroke (inverted omics),
  snp-occupational (5 statistical defects), low-dose-ct (wrong statistical test),
  matsuya-nte (table exponent error), celegans-americium (impossible dosimetry + predatory venue).

*Source reports under /Users/stevens/Dropbox/REPLICATE-PROJECT/ (LUCID-replications/, BVBRC-*, numeric OSTI dirs).*

## ADDENDUM (2026-06-25, found during promotion pass)
- **lucid-patra-polbeta-radiosensitivity** (PARTIAL/SPOT-CHECK): the docking panel **mislabels PDB 1WSR as a BER protein — it is actually aminomethyltransferase**, not a base-excision-repair enzyme. (All 7 canonical Pol-β active-site residues independently confirmed in 1TV9; the 1WSR entry is an identity error.)
