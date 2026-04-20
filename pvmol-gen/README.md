# Replicate

Replication of "Generative AI-Driven Accelerated Discovery of Passivation Molecules
for Perovskite Solar Cells" (Fajar et al., Advanced Science, 2026).

## Pipeline

```
Stage 1:  Train SMILES-X binary classifier on 314 labeled molecules (5-fold CV)
Stage 1b: PubChem Tanimoto augmentation → ~15K molecules → classify → build T1
Stage 2:  Fine-tune GPT-2 on T1, generate molecules, classify, repeat ×3
Stage 3:  RDKit + xTB property filters → cluster → select 10 candidates
```

## Structure

```
replicate/
├── src/
│   ├── config.py                 # All paths, hyperparameters, thresholds
│   ├── utils.py                  # SMILES validation, fingerprints, augmentation
│   ├── sa_scorer.py              # Synthetic accessibility scorer
│   ├── stage1_classifier.py      # SMILES-X BiLSTM+Attention classifier
│   ├── stage1b_pubchem_augment.py # PubChem similarity search + T1 assembly
│   ├── stage2_generator.py       # GPT-2 fine-tuning + iterative generation
│   ├── stage3_filter.py          # Property computation + filtering + clustering
│   └── run_pipeline.py           # Full pipeline orchestrator
├── data/
│   └── t0_molecules.csv          # [REQUIRED] 314 labeled molecules
├── models/                       # Trained models (auto-created)
├── results/                      # Output files (auto-created)
├── logs/                         # Pipeline logs
├── pvmol-gen/                    # Original paper's code (reference)
└── requirements.txt
```

## Setup

```bash
# Create environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: install xTB for energy gap / dipole calculations
conda install -c conda-forge xtb
```

## Data

Place the 314-molecule dataset at `data/t0_molecules.csv` with columns:
- `smiles` — SMILES string
- `delta_pce_norm` — Normalized PCE improvement

## Run

```bash
cd src

# Full pipeline
python run_pipeline.py

# Individual stages
python run_pipeline.py --stage 1      # Train classifier
python run_pipeline.py --stage 1b     # PubChem augmentation
python run_pipeline.py --stage 2      # Generative cycles
python run_pipeline.py --stage 3      # Filtering (with xTB)
python run_pipeline.py --stage 3 --no-xtb  # Filtering (Gasteiger fallback)
```

## Key Parameters (config.py)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Classification threshold | 0.47 | Optimized (not default 0.5) |
| ΔPCEnorm class boundary | 0.10 | ≥ 0.10 = effective |
| PubChem Tanimoto | 0.80 | Similarity threshold |
| Generative cycles | 3 | Stopped to avoid model collapse |
| Target molecules/cycle | 100,000 | CUN molecules |
| SA score max | 6.0 | Synthetic accessibility |
| Clusters | 10 | Agglomerative on Morgan FPs |

## Reference

- Paper: Fajar et al., Adv. Sci. 2026, DOI: 10.1002/advs.202523042
- Original code: https://github.com/adroitfajar/pvmol-gen
- SMILES-X: https://github.com/Lambard-ML-Team/SMILES-X
