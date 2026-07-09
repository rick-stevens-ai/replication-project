# Failure Analysis — BVBRC-41 (*S. algae* 2NE11 replication)

Honest accounting of what did NOT work, what was skipped, and where the
verdict is weaker than the top-line "REPLICATED" suggests.

## 1. PDF availability

- **No paid PDF fetch used.** The paper (Lizárraga et al. 2022, *Biotech Reports*
  33:e00704) is CC-BY 4.0 open access via PMC8816663; we pulled the full-text
  XML from Europe PMC's free REST endpoint. No `pdf` tool was invoked, no paid
  Elsevier/Springer subscription touched.
- **Figures were not independently re-extracted from a PDF.** We worked from
  the Europe PMC XML which contains full body text and Table 2/Table 3
  contents but not the rendered Fig. 2 (the genomic-islands schematic).
  For Fig. 2, we relied on the caption text + the paper's numerical
  descriptions (GI-I 25,322 bp / 21 genes; GI-II 70,550 bp / 64 genes) rather
  than re-analyzing the figure image.
- **Impact:** Low. All quantitative claims are captured in the XML text.
  A future rerun could pull the PDF via unpaywall or PMC's PDF endpoint if
  figure-image re-analysis were needed.

## 2. Analyses that were NOT run

### 2.1 SRA re-assembly (skipped)
- **What was skipped:** downloading the raw PacBio reads from BioProject
  PRJNA547647 / BioSample SAMN15232066 and re-running Unicycler + Quiver from
  scratch.
- **Why:** ~5–20 GB SRA download + hours of assembly compute; the deposited
  assembly is the community-of-record artifact.
- **Consequence:** C1–C4 (length, GC, contigs, coverage) are "matched" against
  the same bytes the authors uploaded, not against an independent assembly.
  This is the biggest asymmetry in our REPLICATED verdict — see Genuine
  Critique in REPORT.tex.
- **Fix (future work):** `prefetch SRRxxxxxxx && fasterq-dump && unicycler
  --long ...` on uicgpu, then diff the resulting FASTA vs CP055159. Est. 4–8 h
  wall-clock.

### 2.2 IslandViewer 4 (skipped; substituted with in-house DIMOB)
- **What was skipped:** running the actual IslandViewer 4 service
  (SIGI-HMM + IslandPath-DIMOB + IslandPick consensus) that the paper used.
- **Why:** IslandViewer 4 requires a web submission (rate-limited) or an
  offline install of the full multi-method pipeline; we implemented a
  self-contained DIMOB-style detector instead.
- **Consequence:** Our 7 islands vs the paper's 2 is a real discrepancy that
  gets recorded as "method-dependent PARTIAL". A rerun with actual
  IslandViewer 4 might show exact agreement or expose a substantive
  disagreement — we do not currently know which.
- **Fix (future work):** submit GCF_014263185.1 to
  https://www.pathogenomics.sfu.ca/islandviewer/ and diff.

### 2.3 BLAST / HMM orthology (skipped)
- **What was skipped:** BLAST-vs-reference or HMM-based orthology confirmation
  of the key enzymes (azoreductase, Dyp peroxidase, Mtr operon, OmcA).
- **Why:** grep on RefSeq product strings + locus-tag + byte-for-byte length
  match was deemed sufficient for the top-line replication verdict.
- **Consequence:** A silent RefSeq re-annotation that flipped a product
  string (e.g. relabeling MtrC as OmcA) would pass our test. The "OmcA
  duplication" claim (Open Question #2) is particularly exposed to this.
- **Fix (future work):** reciprocal BLAST vs *S. oneidensis* MR-1 reference
  proteins (SO_1779 OmcA, SO_1778 MtrC, SO_4180 for Dyp-family peroxidase),
  plus InterProScan for domain confirmation.

### 2.4 Three specific NADPH oxidoreductases (skipped)
- **What was skipped:** individual verification of the paper's three named
  NADPH-dep oxidoreductases at HU689_04585 / 04700 / 21345.
- **Why:** first-pass grep found "multiple oxidoreductases present" and we
  marked it PARTIAL rather than drill into each.
- **Consequence:** C8 is marked NOT-TESTED by the LLM judge, dragging
  agreement from 12/12 down to 10/12.
- **Fix (future work):** trivial — 3× grep on RefSeq GFF for each specific
  locus tag + measure bp/aa. Est. 5 min analyst time.

### 2.5 Wet-lab phenotype (impossible in silico)
- **What is not testable:** the paper's headline biological claim of
  89–97% azo/anthraquinone dye decolorization in 12 h, biochemical Table 1
  assays, growth-condition tolerances.
- **Why:** requires bench work, not compute.
- **Consequence:** we can only test whether the *genomic basis* for
  decolorization exists (it does), not whether the strain actually decolorizes
  at the reported rate.
- **Fix (future work):** collaborator wet-lab assay, or heterologous
  expression of HU689_RS20690 in *E. coli* BL21 with a dye panel.

### 2.6 Comparative genomics across *S. algae* strains (skipped)
- **What was skipped:** comparison of 2NE11 gene content vs closely related
  *S. algae* strains (MARS 14, OK-1, others) to test whether decolorization
  capacity is 2NE11-specific or clade-wide.
- **Why:** out of scope for a single-genome replication.
- **Consequence:** we cannot say whether the ecologically-interesting genes
  are strain-specific adaptations or core-genome features.
- **Fix (future work):** pangenome analysis with Roary or PPanGGOLiN on all
  sequenced *S. algae* isolates.

## 3. Single-judge caveat

- **What was done:** ONE LLM judge (Argo `gpt-5.2` with fallback to
  `argo:claude-opus-4.8`) scored the per-claim evidence, producing the
  Coverage 12/13, Agreement 10/12, REPLICATED verdict recorded in
  `report/evidence/llm_judge.txt`.
- **What was NOT done:**
  - No cross-model panel (e.g. gpt-5.2 + claude-opus + gemini-3-pro voting).
  - No blind human re-scoring by an independent analyst.
  - No sensitivity test — the same evidence blob fed to a different judge or
    same judge with different prompt could produce a slightly different
    per-claim scorecard.
- **Consequence:** the "REPLICATED" verdict is the assessment of one LLM
  reading one carefully-assembled evidence packet. The underlying evidence
  (byte-for-byte assembly + cross-pipeline gene content) is strong, but the
  aggregation is single-judge.
- **Fix (future work):** add a two-model or three-model judge panel and
  require consensus for the top-line verdict. Ideally add one human
  ground-truth spot-check per BVBRC batch.

## 4. Confirmation-bias risk

We searched for *evidence supporting* each claim rather than *evidence
against*. Specifically:
- We did not try to falsify the "OmcA duplication" claim (could be
  MtrC + OmcA canonical architecture mislabeled).
- We did not check whether the "2 genomic islands" number is preferred by
  IslandViewer 4 defaults vs alternative cutoffs.
- We did not check whether *any* claim in the paper is contradicted by the
  RefSeq re-annotation (e.g. if a claimed gene became a pseudogene in 2026).

For a genome-announcement paper this is probably acceptable — the paper's
claims are mostly existential ("gene X is present"), which is easier to
confirm than to falsify. But the confirmation-bias structure of the workflow
should be acknowledged.

## 5. What the "REPLICATED" verdict actually means

**Strong evidence for:**
- Deposited assembly bytes reproduce paper Table 2 exactly.
- Two independent annotation pipelines (RefSeq/PGAP + Prokka 1.12) converge
  on the same gene content.
- Byte-for-byte length matches for the two headline decolorization enzymes.
- All qualitative gene-content claims (Mtr, metal resistance, CRISPR,
  carbohydrate metabolism) confirmed on the actual public genome.

**Weaker / not-tested:**
- Independent re-assembly from SRA reads (not run).
- IslandViewer 4 enumeration (substituted with DIMOB-only method).
- BLAST/HMM orthology (substituted with product-string grep).
- Three specific NADPH oxidoreductases (marked partial).
- Wet-lab phenotype (impossible in silico).
- Multi-judge aggregation (single-judge only).

The verdict is well-supported for a genome-announcement paper of this kind
(where the load-bearing claims are assembly stats + gene presence), but it
does not certify the paper's *biological* conclusions (bioremediation
capacity, decolorization mechanism) — only the *genomic evidence base* for
them.
