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
