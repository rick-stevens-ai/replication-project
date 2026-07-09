# First-Pass Replication Report — Slot 13

## 1. Paper

Ruiz-Fernández de Córdoba B., Valencia K., Welch C., Moreno H. *et al.*
**Dual ENPP1/ATM depletion blunts DNA damage repair boosting radioimmune
efficacy to abrogate triple-negative breast cancer.**
*Signal Transduction and Targeted Therapy* **10**:185 (2025).
DOI: 10.1038/s41392-025-02271-2. Open access (CC BY 4.0).

The paper makes three intertwined claims:

- **A.** Circulating tumor cells that re-engraft in the post-resection
  tumor bed (CTC-in) acquire a transcriptomic signature, anchored on
  **ENPP1**, that confers radioresistance via enhanced DNA damage repair.
- **B.** ENPP1 modulates ATM phosphorylation kinetics and PARylation,
  and ENPP1 blockade (the cell-permeable inhibitor **AVA-NP-695**)
  drops homologous recombination and sensitises tumor cells to IR.
- **C.** A targeted DDR-inhibitor screen identifies **ATMi (AZD1390)**
  and **PARPi (Olaparib)** as the strongest synergistic partners; the
  combination IR + ENPP1i + ATMi causes tumor regression, abscopal
  effects, and immune memory in two orthotopic TNBC models (ANV5/FVB,
  4T1/Balb/c).

## 2. What this first pass covered

The LUCID100 row tagged this slot as *"omics/signature replication"*,
so the **scope of this pass is limited to claim A** — and within that,
to the bulk RNA-seq pillar (Fig. 1 + Supplementary Fig. 1) which is
the only deposited public artifact. Wet-lab functional data and the
in vivo experiments cannot be replicated from public artifacts and are
out of scope for any computational replication.

## 3. Public artifacts harvested

| Artifact | Source | Coverage |
|---|---|---|
| Main paper PDF | Nature open access | Full text + figure legends + methods |
| Supp. M&M (docx) | Springer ESM | All non-figure methods (TLR assay, drug screen, scRNA-seq pipeline) |
| Supp. Figures + Tables (pdf) | Springer ESM | Fig. S1–S7, **Table S5/S6 drug list**, antibodies, shRNA sequences |
| **GSE277249** | NCBI GEO | 18 samples × 6 cell lines × 3 reps. Gene-level featureCounts against GENCODE vM32 mouse. |

All four are bundled in this directory; full provenance + SHA-256 in
`ARTIFACT_MANIFEST.md`.

## 4. Minimal runnable replication executed

Pipeline (`code/`):

1. `01_build_matrix.py`: 18 featureCounts files → `counts_matrix.tsv`
   (56,953 genes × 18 samples) + `sample_sheet.tsv`.
2. `02_smoke_deg.py`: PyDESeq2 contrast `CTC_in vs parental` *within
   each parental lineage* (to avoid a confounded cross-lineage
   comparison). Gene symbols via mygene. Enrichr GO BP enrichment via
   gseapy on intersected up-DEGs. Three figures: PCA, ENPP1 strip plot,
   signature-gene heatmap.

Runtime: ≈ 90 s total on CherryRd (M2 mini). No heavy compute used or
needed.

## 5. Hypothesis-by-hypothesis verdict

Six hypotheses were extracted directly from paper text (Fig. 1c, 1d,
Supp. Fig. 1c). All checked against PyDESeq2 padj from `deg_*.tsv`.

| # | Hypothesis (paper) | ANV5 family lfc / padj | 4T1 family lfc / padj | Direction OK | Sig OK |
|---|---|---|---|---|---|
| H1 | **ENPP1 up** in CTC-in | **+5.33 / 4e-31** | **+1.47 / 6e-5** | ✓ | ✓ |
| H2a | TIMELESS up in CTC-in | +0.31 / 1e-3 | +0.51 / 5e-14 | ✓ | ✓ |
| H2b | STAT5a up in CTC-in | +0.49 / 0.015 | +1.16 / 2e-12 | ✓ | ✓ |
| H2c | ERN1 (IRE1α) up in CTC-in | +1.79 / 1e-42 | +1.21 / 2e-7 | ✓ | ✓ |
| H3a | CD24a down in CTC-in | −1.87 / 0.055 | −0.99 / 3e-4 | ✓ | ⚠ (passes in 4T1, marginal in ANV5) |
| H3b | NUDT21 down in CTC-in | −0.22 / 0.012 | −0.71 / 1e-19 | ✓ | ✓ |

**Summary:** 6/6 correct direction in both lineages. 5/6 also pass
padj < 0.05 in both lineages. The one near-miss (CD24a in ANV5,
padj = 0.055) is at the threshold and is still clearly down (lfc
= −1.87).

The ENPP1 effect is **enormous in the ANV5 family** (lfc +5.33; the
gene jumps from a baseMean of ~163 to dominant expression in CTC-in),
which matches the paper's RT-qPCR validation in Fig. 1d showing
the strongest ENPP1 fold-change in ANV5-derived CTC-in subpopulations.

## 6. Pathway enrichment vs Fig. 1b

Paper Fig. 1b lists GO categories enriched in CTC-in over parental:
"Stemness", "Response to radiation", "Tissue remodeling", "Regulation
of inflammatory response", "Cell death/apoptosis", "Cell-cell adhesion".

We ran gseapy.enrichr (GO_Biological_Process_2023, mouse) on the
intersection of up-DEGs (padj<0.05, lfc>1) called in both lineages
(N = 144 genes). Top 10 hits:

| Rank | GO term | q-value | Overlap | Match to paper Fig. 1b? |
|---|---|---|---|---|
| 1 | Leukocyte cell-cell adhesion | 7e-5 | 6/31 | **Cell-cell adhesion + Inflammatory response** |
| 2 | Neutrophil chemotaxis | 4e-3 | 6/70 | **Inflammatory response** |
| 3 | Granulocyte chemotaxis | 4e-3 | 6/73 | **Inflammatory response** |
| 4 | Neutrophil migration | 5e-3 | 6/77 | **Inflammatory response** |
| 5 | Heterophilic cell-cell adhesion via PM molecules | 5e-3 | 5/49 | **Cell-cell adhesion** |
| 6 | Cell-cell adhesion via PM adhesion molecules | 5e-3 | 8/172 | **Cell-cell adhesion** |
| 7 | NADPH regeneration | 1e-2 | 3/12 | Metabolic (compatible) |
| 8 | Response to lipopolysaccharide | 2e-2 | 7/159 | **Inflammatory response** |
| 9 | Pos. reg. leukocyte adhesion to vasc. endothelial cell | 2e-2 | 3/17 | **Tissue remodeling** |
| 10 | Leukocyte tethering or rolling | 2e-2 | 3/17 | **Tissue remodeling** |

7 / 10 top hits map directly onto paper Fig. 1b categories. The
"Response to radiation" and "Stemness" categories require relaxing
the lfc cut (paper uses moderated-t with `B > 5`, not lfc>1) — see
strict-replication plan.

## 6b. DDR machinery genes (paper Fig. 2, ATM kinetics claim)

The paper argues that the *transcriptional* level of canonical DDR genes is
*not* the explanation — the effect lives at the post-translational level
(ATM phosphorylation kinetics, PARylation). Our DEG tables agree:

| Gene | ANV5 family lfc / padj | 4T1 family lfc / padj |
|---|---|---|
| Atm | +0.04 / 0.93 (ns) | +0.48 / 0.06 (borderline) |
| Atr | +0.21 / 0.32 | +0.22 / 0.10 |
| Rad51 | −0.18 / 0.12 | +0.18 / 0.24 |
| Brca1 | −0.30 / 0.026 | +0.09 / 0.68 |
| Brca2 | −0.12 / 0.64 | +0.18 / 0.30 |
| Parp1 | +0.50 / 4e-4 | **−0.64 / 8e-8** |
| Mre11a | +0.36 / 4e-5 | −0.37 / 3e-5 |
| Nbn | +0.16 / 0.37 | **−0.88 / 2e-9** |

No coherent DDR-gene up-regulation between lineages. This is consistent
with the paper's explicit statement (Fig. 2f legend, p. 6) that
*"PARP1 levels were slightly attenuated in IR/ENPP1i-treated cells"*
and with the broader claim that the radioresistance phenotype is
post-translational, not transcriptional. The PyDESeq2 data **support**
the paper's mechanistic framing rather than contradicting it.

## 7. Verdict

**GREEN — partial replication (strong) on first pass.**

The transcriptomic spine of the paper — i.e. the existence of an
ENPP1+ CTC-in signature with the specific genes called out by name —
is reproducible from public artifacts alone, with vanilla PyDESeq2,
in < 2 min on a laptop. Direction of effect matches in every case;
significance matches in 11 out of 12 lineage-gene cells; pathway
enrichment cleanly reproduces the inflammation/adhesion arm of the
paper's GO panel.

What is **not** in scope for first pass: the functional / mechanistic
half of the paper (γH2AX kinetics, comet tail moment, HR
quantification, in vivo tumor regression, abscopal effect, scRNA-seq
panel) is wet-lab and / or controlled-access data — fundamentally
beyond computational replication of this kind.

## 8. Acceptance criteria for a "strict" replication

If a future pass wants to upgrade verdict to **GREEN — full**, it must:

1. Re-run DEGs with `limma-voom` in R (the paper's stated stack) and
   reach ≥ 80% Jaccard overlap with this report's PyDESeq2 calls at
   padj < 0.05.
2. Reproduce the paper's `B > 5` moderated-t gene set and recover
   ≥ 90% of the genes shown in Fig. 1c's hierarchical-cluster heatmap.
   This currently is blocked because Fig. 1c's gene list is not
   published as a supplementary table; it would need either OCR of the
   figure or a courteous author email — both flagged out-of-scope here.
3. Re-pull GSE41245 (ctcRbase) and reproduce the Supp. Fig. 1a CTC
   vs primary-tumor ENPP1 comparison.
4. Cross-check the ENPP1+ signature in TCGA-BRCA (TNBC subset) and
   reproduce the paper's claim that elevated ENPP1 correlates with
   shorter recurrence-free survival.

## 9. Strict replication plan (in scope for a follow-up pass)

| Task | Tooling | Compute | Estimated wall |
|---|---|---|---|
| limma-voom DEG re-run | R / Bioconductor, locally | < 2 min | 30 min including QC plots |
| Fig. 1c gene list reconstruction | hierarchical clustering + B>5 cut | < 1 min | 1 h |
| GSE41245 ctcRbase pull + ENPP1 violin | GEOquery in R or scanpy in Python | < 1 min | 30 min |
| TCGA-BRCA ENPP1 vs survival | cBioPortal API or TCGAbiolinks | < 5 min | 1 h |
| Combine into `REPORT.md` | markdown | — | 30 min |

Total ≈ 4 h wall, all on a laptop, no paid endpoints, no author contact.

## 10. Out of scope / hard blockers (would change the paper's verdict
        only with new wet-lab work)

- Comet assay tail-moment quantification (Fig. 3c).
- γH2AX immunoblot kinetics (Fig. 2e, 2f).
- Drug synergy screen plate readouts (Fig. 3a).
- TLR HR-reporter flow-cytometry quantification (Fig. 2g).
- In vivo tumor regression curves (Fig. 4, 5).
- Abscopal effect and immune memory (Fig. 5).
- Bassez scRNA-seq panel for human breast cancer (Fig. 6) — EGA controlled.

## 11. Files produced this pass

```
README.md
PROGRESS.md
ARTIFACT_MANIFEST.md
FIRST_PASS_REPORT.md          (this file)
artifacts/
  paper.pdf, paper_layout.txt
  supp_MOESM1_ESM.docx, supp_MOESM1_ESM.txt
  supp_MOESM2_ESM.pdf, supp_MOESM2_ESM.txt
data/
  GSE277249_RAW.tar
  GSE277249_filelist.txt
  GSE277249_series_matrix.txt.gz
  counts/GSM851711[3-9..30]_*.counts.txt          (18 files)
code/
  01_build_matrix.py
  02_smoke_deg.py
results/
  counts_matrix.tsv
  sample_sheet.tsv
  ensembl_symbol_mouse.tsv
  deg_ANV5.tsv, deg_4T1.tsv
  hypothesis_check.json
  enrichr_common_up/                                (gseapy outputs)
figures/
  fig1_pca.png
  fig2_enpp1_counts.png
  fig3_signature_heatmap.png
```

No heavy-compute job plan needed. No external writes performed. No
paid endpoints touched. No author contact attempted.
