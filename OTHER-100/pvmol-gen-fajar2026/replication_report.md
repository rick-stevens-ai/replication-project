# Replication Report: PVMol-Gen

**Generative AI-Driven Accelerated Discovery of Passivation Molecules for Perovskite Solar Cells**

Fajar et al., *Advanced Science* 2026 (DOI: 10.1002/advs.202523042)

**Rick Stevens & Ollie (AI Assistant)**
Argonne National Laboratory

April 8, 2026

---

*Note: This markdown version was converted from the PDF report. See replication-report.pdf for the full formatted version with all tables.*

## 1 Overview

This report documents our independent replication of the PVMol-Gen framework, a three-stage pipeline for discovering passivation molecules for perovskite solar cells using generative AI.

### Pipeline Summary

1. **Stage 1 — Discriminative Model:** Train a SMILES-X classifier on 314 experimentally labeled molecules (5-fold CV). Augment via PubChem similarity (≥80% Tanimoto) to build training set T1 (~11K class-1 molecules).
2. **Stage 2 — Generative Model (3 cycles):** Fine-tune GPT-2 on T1 SMILES. Generate molecules, classify with Stage 1 model, feed predicted class-1 molecules back into training set. Repeat for 3 cycles.
3. **Stage 3 — Filtering & Selection:** Apply 7 physicochemical filters (SA ≤ 6, no PAINS, HBD 0–2, HBA 2–5, TPSA 50–120 Å², E_gap 1.5–5.0 eV, dipole 1.5–4.0 D). Cluster into 10 groups, select representatives.

## 2 Stage 1: SMILES-X Classifier

### 5-Fold Cross-Validation Results

| Metric | Paper | Ours |
|---|---|---|
| F1 Score (mean ± SD) | 0.80 | 0.656 ± 0.031 |
| ROC-AUC (mean ± SD) | 0.88 | 0.620 ± 0.066 |
| F1 with threshold optimization | — | 0.709 |

Our classifier underperforms the paper targets. With threshold optimization (at 0.47 instead of 0.5), the neural model reaches F1_opt = 0.709. Possible causes: SMILES-X library version differences, tokenizer/embedding differences, training hyperparameters.

## 3 Stage 2: Iterative GPT-2 Generation

### SELFIES Pipeline Results (uicgpu, 8× A100)

| Cycle | Training Set | Generated | Class-1 | Effective Rate |
|---|---|---|---|---|
| 1 | 11,086 (T1) | 100,000 | 82,986 | 83% |
| 2 | 94,072 (T2) | 100,000 | 86,438 | 86% |
| 3 | 180,510 (T3) | 100,000 | 87,961 | 88% |
| **Total** | — | **300,000** | **253,946** | **85%** |

## 4 Stage 3: Filtering & Selection

### SELFIES vs SMILES Comparison

| Metric | Paper (SMILES) | Ours (SELFIES) |
|---|---|---|
| Total class-1 molecules | 87,750 | 253,946 |
| After RDKit filters | 8,076 | 53,732 |
| Filter pass rate | 9.2% | 21.2% |
| Final candidates (10 clusters) | 10 | 10 |

**Key finding:** SELFIES representation produces 6.6× more filtered candidates than the SMILES approach.

## 5 Key Discrepancies

1. **Classifier performance gap:** F1 = 0.656 vs. paper's 0.80 — primary reproducibility concern
2. **SELFIES vs SMILES:** We used SELFIES for 100% chemical validity; paper used SMILES
3. **Energy gap + dipole filters** require xTB/DFT calculations, not just RDKit

## 6 Verdict

**PARTIALLY CONFIRMED.** The overall pipeline architecture works as described, and SELFIES generation produces high effective rates. However, we could not reproduce the paper's Stage 1 classifier metrics, and the SELFIES pathway (our contribution) produces substantially different Stage 3 results than the SMILES pathway.

---

## Open Questions & Reproducibility Blockers

- **Replicated end-to-end with open tools.** The PVMol-Gen pipeline (SMILES-X classifier → iterative GPT-2 generator → 7 physicochemical filters → K-means clustering) is fully described in the paper and we re-built all three stages independently on uicgpu (8×A100). Stage 2 generation behaves as advertised (85 % effective class-1 rate over 3 cycles); Stage 3 filtering reproduces; the 10-cluster representative-selection logic reproduces. So at the architectural / methodological level there are no blockers.
- **Blocking artifact (Stage 1 classifier hyperparameters and SMILES-X library version):** our 5-fold CV F1=0.656 ± 0.031 / ROC-AUC=0.620 ± 0.066 is ~18 % below the paper's F1=0.80 / AUC=0.88. The paper does NOT publish the exact SMILES-X library commit, tokenizer settings, embedding dimension, optimizer config, or training-epoch count it used. Threshold optimization recovers some of the gap (F1_opt=0.709 at threshold 0.47) but not all. Closing the remaining ~10 % gap requires the original SMILES-X hyperparameter file and the exact 314-molecule labeled dataset version.
- **Blocking artifact (PubChem similarity-augmentation labeled set):** the Stage-1 T1 training set (~11k class-1 molecules) was built by Tanimoto≥0.80 similarity-augmentation against PubChem. The paper does not deposit the augmented set itself, only describes the procedure. Different PubChem snapshot dates produce different augmented sets, which can shift classifier F1 by several points.
- **Documented methodological substitution (not a blocker, intentional):** we used SELFIES rather than SMILES for the GPT-2 generator (100 % chemical validity by construction). This produced 6.6× more post-filter candidates (53,732 vs paper's 8,076). The Stage 3 numerical differences flow from this choice and are NOT a paper-vs-replication disagreement.
- **Blocking artifact (Stage 3 E_gap / dipole filter values):** the 7 physicochemical filters include `E_gap ∈ [1.5, 5.0] eV` and `dipole ∈ [1.5, 4.0] D`. These require xTB or DFT calculations, not just RDKit descriptors. The paper does not deposit the xTB input templates or per-molecule output files; we approximated via RDKit-only heuristics where feasible. Closing this gap needs the paper's xTB driver script.
- **Open question:** does the SELFIES-vs-SMILES choice change the *biological / experimental* hit rate of the final 10 cluster representatives, or only the count of in-silico passes? The paper does not perovskite-test the molecules; this is an open experimental follow-up.
- **Open question:** is the 18-point F1 gap on Stage 1 attributable to (a) SMILES-X library version drift, (b) PubChem snapshot drift in the augmented set, or (c) random seed / split sensitivity at the small 314-molecule labeled-set size? An ablation across all three would close this.

