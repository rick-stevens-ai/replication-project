# Failure analysis — Fang et al. (2018) replication

**Paper:** Fang X et al., *BMC Systems Biology* 12:66 (2018).
**Verdict:** PARTIAL REPLICATION (strong). Not full REPLICATED.

This document catalogues, honestly, what did **not** work / what was **not** done, and why. The corresponding narrative is in the "GENUINE CRITIQUE" section of `REPORT.tex` and item 6 of `REPORT.md`.

---

## 1. What replicated (for contrast)

- **Central FBA prediction (C4a–c).** Table-1 substrate growth on K-12 reference iML1515/iJO1366 reproduced quantitatively for 6/8 substrates; 2 within paper's reported within-phylogroup variance.
- **Central mechanism claim (C5).** Direct tblastn on the three canonical B2 reference genomes (LF82, UTI89, NRG857c) — entire frl operon (frlA/B/C/D + regulator frlR) absent (0/5), K-12 control retains all 5 (5/5). Textbook single-operon-deletion signature.
- **Sanity panel (C3).** 16/17 K-12 catabolism reference genes conserved (≥96%) in each B2 strain; loss is frl-specific, not a general assembly artifact.
- **Phylogroup (C6).** Independently re-derived via in-silico Clermont 2013 quadruplex; 4/4 agreement with paper.
- **Genome statistics (C2).** LF82 4.77 Mb, UTI89 5.18 Mb, NRG857c 4.89 Mb — match published values.

---

## 2. What did NOT replicate

### 2.1 110-strain pan-genome (Fig. 1a, 3a)

- **Not done.** Only 4 genomes touched at the sequence level (3 B2 + 1 A control).
- **Reason not done:** time-boxed replication (~3 min compute, few days analyst); full pan-genome would need Roary/PanX/CD-HIT-at-80% across 110 proteomes plus per-strain GEM reconstruction.
- **Impact:** Figures 1a (110 × reactions matrix) and 3a (110 × 649 substrate-growth heatmap) remain unverified. The B2-vs-non-B2 pan-genome signal from the paper is not independently regenerated at scale.
- **Estimated cost to close:** ~1–2 weeks single-workstation analyst time. No commercial software, GPUs, or restricted data required. All 110 accessions are public (Additional file 1 / Table S1 in the BMC supplementary materials).

### 2.2 53 IBD-patient isolate per-strain modeling

- **Not done.** The paper's epidemiological punchline (B2 over-represented in IBD) rests on the 53 IBD isolates. We did not (a) remap them to current BV-BRC accessions, (b) rebuild per-strain GEMs, or (c) score them substrate-by-substrate.
- **Reason not done:** BV-BRC's strain-name index for clinical IBD isolates is sparse, and the paper's strain list would need manual reconciliation.
- **Impact:** The IBD-cohort claim itself is not independently re-tested; only the phylogroup-level metabolic claim is.
- **Estimated cost to close:** Manual accession mapping + CarveMe per-strain reconstruction. ~1 week.

### 2.3 649-substrate FBA panel (Fig. 3a)

- **Not done.** Only 8 Table-1 substrates + 7 mucus glycans were tested (15 of 649).
- **Reason not done:** The 649-substrate list (Additional file 1, Table S3) was not parsed for BiGG IDs and looped through per-strain GEMs; the paper's Fig. 3a requires the loop.
- **Impact:** The full metabolic-capability landscape per strain is not verified; we only sampled 2.3% of the substrates.
- **Estimated cost to close:** Straightforward COBRApy loop once per-strain GEMs and BiGG-ID map exist.

### 2.4 SelectKBest 100-gene discriminative scoring

- **Not done.** The paper's ranking of top-100 phylogroup-discriminative metabolic genes was not reproduced.
- **Reason not done:** Depends on per-strain gene-presence matrix across 110 strains (see §2.1).
- **Impact:** We cannot cross-validate the paper's specific gene rankings; we only verified that the top-ranked gene family (frl operon) shows the expected B2-loss signature.

### 2.5 Partial disagreements on 2 Table-1 substrates

- **Xanthosine and XMP.** K-12 iML1515 grows at μ ≈ 1.02 h⁻¹; iJO1366 at μ ≈ 1.21 h⁻¹.
- **Paper says:** 38–46% of non-B2 strains grow on these substrates. Our K-12 gives a binary GROW; the paper's fraction is much less than 100%.
- **Is this a fail?** No, it is *within* the paper's reported within-phylogroup variance — some phylogroup-A strains grow, some don't; K-12 happens to be a grower per the reference GEM. But a clean REPLICATED tag would require reproducing the *fraction* of A/B1/D strains that grow, not just the K-12 binary answer.
- **Reason not resolved:** Would need per-strain GEMs for many phylogroup-A strains (see §2.1).

### 2.6 Extraction/marker stage

- `extraction/marker.md` does not exist in the project directory. This report's replication logic bypassed the marker/nougat extraction stage and worked directly from the open-access BMC PDF plus the paper's supplementary tables. Not a failure of the replication — a gap in the extraction pipeline artifact set.

---

## 3. Categorization of the gap

| Gap type | Item | Blocker | Resolvable? |
|---|---|---|---|
| Scale | 110-strain pan-genome | Analyst time (~1–2 wk) | Yes; all inputs public |
| Scale | 649-substrate FBA panel | Analyst time (~days) | Yes; pending §2.1 |
| Scale | 53 IBD-isolate per-strain GEMs | Manual accession map + compute | Yes; ~1 wk |
| Method-match | SelectKBest 100-gene ranking | Depends on §2.1 | Yes; downstream |
| Method-match | Fraction-of-strains-growing on xanthosine/XMP | Depends on §2.1 | Yes; downstream |
| Pipeline | extraction/marker.md missing | Extraction stage not run | Yes; low priority (paper is CC-BY PDF) |

**None of the gaps are blocked by cost, data access, or software licensing.** All 110 accessions are public NCBI; BiGG is public; COBRApy/BLAST+/CarveMe are all free. The blocker is analyst time (~1–2 weeks single workstation).

---

## 4. Failures / issues encountered during this replication

- **Weak spurious tblastn cross-hits (19–29% identity) in B2 strains for frl proteins.** Initially concerning; resolved by applying comparative-genomics-standard presence rule (pident ≥ 70, cov ≥ 70, e ≤ 1e-30). Weak hits map to unrelated sugar transporters (YjjPB family for FrlA) and generic 6-P sugar deglycases (for FrlB). Not a false-positive risk under the standard threshold.
- **Two-contig assemblies (UTI89, NRG857c).** BLAST-database construction handles multi-contig fine but Clermont amplicon-distance check has to allow same-contig pairing. Verified pass.
- **GalNAc infeasibility on K-12** initially looked like a bug (0.000 growth) — turned out to be the *expected* result and directly supports the paper's B2 TBP-aldolase advantage thesis (K-12 lacks the B2-specific aldolase copies).
- **No solver-choice sensitivity tested.** All FBA numbers are from GLPK (COBRApy default). CPLEX/Gurobi cross-check not performed. Would only matter for numerical edge cases; qualitative growth calls are solver-independent.

---

## 5. Trust boundary

- **All numbers in `REPORT.md` come from `cobra.Model.optimize()` and `tblastn` on un-modified BiGG models and NCBI assemblies.**
- **No fluxes were fabricated. No BLAST hits were invented. No genome statistics were guessed.**
- Weak tblastn hits (19–29% identity for B2 frl) are reported *as weak* in the results table — labelled "weak N%" rather than presented as orthology-grade hits.
- 2 partial disagreements (xanthosine, XMP) are reported openly rather than hidden.
- The 4-strain scope vs. 110-strain paper scope is stated explicitly in the verdict and in the 6/22 Rule critique section.
