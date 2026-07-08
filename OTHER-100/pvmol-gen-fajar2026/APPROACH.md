# Replication Approach — Fajar et al. 2026
# "Generative AI-Driven Accelerated Discovery of Passivation Molecules for Perovskite Solar Cells"

## Pipeline Overview

The framework has three stages: (1) build a classifier, (2) generate molecules, (3) filter and test.

### Stage 1 — Database & Discriminative Model

1. Collect 314 experimentally reported passivation molecules from PSC literature, each labeled with normalized PCE improvement (ΔPCEnorm). Molecules with ΔPCEnorm ≥ 0.10 are class 1 (effective), below that class 0.
2. Train a SMILES-X binary classifier on these 314 molecules using 5-fold cross-validation. Target: F1 ≈ 0.80, ROC-AUC ≈ 0.88.
3. Augment the dataset by pulling molecules from PubChem with ≥ 80% Tanimoto similarity to the top class 1 molecules (ΔPCEnorm > 0.16) — this yields ~15,540 additional molecules (Data T-aug).
4. Run the SMILES-X classifier on Data T-aug (~70% predicted class 1). Combine class 1 molecules from the original 314 and from T-aug into Data T1 (~11,000 molecules).

### Stage 2 — Generative Model (Iterative)

5. Fine-tune GPT-2 on Data T1 (SMILES strings of class 1 molecules only).
6. Generate molecules, then classify them with SMILES-X. Feed predicted class 1 molecules back into the training set.
7. Repeat for 3 cycles total. By cycle 3 you should have >100,000 chemically valid, unique, novel (CUN) molecules, with >80% predicted effective.

### Stage 3 — Filtering & Selection

8. Apply seven physicochemical filters: synthetic accessibility ≤ 6, no PAINS substructures, HBD 0–2, HBA 2–5, TPSA 50–120 Å², energy gap 1.5–5.0 eV, dipole moment 1.5–4.0 D. This cuts to ~8,000 candidates.
9. Cluster the ~8,000 molecules into 10 groups using agglomerative clustering on Morgan fingerprints. Randomly sample one representative per cluster.
10. Expert evaluation → pick 3 for experimental testing in inverted PSC devices.

## Data & Code Pointers

- **Code repository:** github.com/adroitfajar/pvmol-gen
- **Data T0 (314 molecules):** included in the paper's supplementary material and likely in the GitHub repo
- **PubChem augmentation:** query PubChem for molecules with ≥ 80% Tanimoto similarity to top performers
- **SMILES-X:** the classifier framework from Lambard & Gracheva (2020), available as an open-source package
- **GPT-2:** Hugging Face's pretrained GPT-2, fine-tuned on SMILES strings
- **RDKit:** used for validity checking, fingerprinting, SA scores, PAINS filtering, and physicochemical property calculations

## Key Details for Reproducibility

- The classification threshold was optimized at 0.47 (not the default 0.5) to maximize F1.
- They stopped at 3 generative cycles specifically to avoid model collapse.
- LLaMA-2 was also tested but dropped due to being ~100× slower at inference with comparable results.
- Energy gap and dipole moment filters require semi-empirical or DFT-level calculations (not just RDKit).
- For experimental validation, MBA was applied at 1 mg/mL in isopropanol, spin-coated on perovskite, annealed at 100°C for 5 min.
