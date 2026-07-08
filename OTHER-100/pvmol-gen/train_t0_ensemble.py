"""Ensemble SMILES-X classifier with enriched RDKit descriptors.

Computes additional molecular descriptors beyond ha_num/o_num,
then runs multi-seed 5-fold CV and averages predictions across seeds
for more robust evaluation.

Usage:
    python train_t0_ensemble.py                  # 5 seeds (default)
    python train_t0_ensemble.py --n-seeds 10     # more seeds
"""

import argparse
import json
import logging
import os
import sys
from typing import List

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

from smilesx import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/train_t0_ensemble.log"),
    ],
)
logger = logging.getLogger(__name__)

DATA_PATH = "data/T0.csv"
OUTDIR = "models/t0_ensemble"

# Descriptors to compute
DESCRIPTOR_FUNCS = {
    "molwt": Descriptors.MolWt,
    "logp": Descriptors.MolLogP,
    "tpsa": Descriptors.TPSA,
    "hbd": rdMolDescriptors.CalcNumHBD,
    "hba": rdMolDescriptors.CalcNumHBA,
    "rot_bonds": rdMolDescriptors.CalcNumRotatableBonds,
    "ring_count": rdMolDescriptors.CalcNumRings,
    "aromatic_rings": rdMolDescriptors.CalcNumAromaticRings,
    "frac_csp3": rdMolDescriptors.CalcFractionCSP3,
    "num_heteroatoms": rdMolDescriptors.CalcNumHeteroatoms,
}


def compute_descriptors(df: pd.DataFrame, smiles_col: str = "smiles") -> pd.DataFrame:
    """Add RDKit descriptor columns to dataframe."""
    df = df.copy()
    for name, func in DESCRIPTOR_FUNCS.items():
        values = []
        for smi in df[smiles_col]:
            mol = Chem.MolFromSmiles(smi)
            if mol is not None:
                values.append(func(mol))
            else:
                values.append(np.nan)
        df[name] = values
    logger.info(f"Computed {len(DESCRIPTOR_FUNCS)} RDKit descriptors for {len(df)} molecules")
    return df


def run_single_seed(
    df: pd.DataFrame,
    extra_cols: List[str],
    seed: int,
    outdir: str,
) -> dict:
    """Run 5-fold CV with a single seed, return per-fold results."""
    clf = SmilesXClassifier(
        data=df,
        smiles_col="smiles",
        label_col="bin_class",
        extra_feature_cols=extra_cols,
        embed_dim=32,
        lstm_units=128,
        tdense_units=64,
        dense_depth=2,
        dropout=0.3,
        lr=1.67e-4,
        weight_decay=5e-6,
        batch_size=32,
        n_epochs=100,
        patience=25,
        class_weight=True,
        outdir=outdir,
        seed=seed,
    )

    result = clf.cross_validate(n_folds=5, augment=True, threshold=None)
    return {
        "seed": seed,
        "mean_f1": result.mean_f1,
        "std_f1": result.std_f1,
        "mean_auc": result.mean_auc,
        "std_auc": result.std_auc,
        "folds": [
            {
                "fold": f.fold,
                "f1": f.f1,
                "auc_roc": f.auc_roc,
                "auc_pr": f.auc_pr,
                "accuracy": f.accuracy,
                "precision": f.precision,
                "recall": f.recall,
                "threshold": f.threshold,
            }
            for f in result.folds
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-seeds", type=int, default=5)
    args = parser.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Load and enrich data
    df = pd.read_csv(DATA_PATH)
    df = compute_descriptors(df)

    # All extra feature columns: original + new descriptors
    extra_cols_all = ["ha_num", "o_num"] + list(DESCRIPTOR_FUNCS.keys())
    logger.info(f"Extra features ({len(extra_cols_all)}): {extra_cols_all}")

    # Also test with original features only for comparison
    extra_cols_orig = ["ha_num", "o_num"]

    # ---- Run 1: Original features, multi-seed ----
    logger.info("\n" + "=" * 60)
    logger.info("RUN A: Original features (ha_num, o_num) — multi-seed ensemble")
    logger.info("=" * 60)

    seeds = [42 + i * 7 for i in range(args.n_seeds)]
    results_orig = []
    for i, seed in enumerate(seeds):
        logger.info(f"\n--- Seed {seed} ({i+1}/{args.n_seeds}) ---")
        seed_dir = os.path.join(OUTDIR, f"orig_seed_{seed}")
        res = run_single_seed(df, extra_cols_orig, seed, seed_dir)
        results_orig.append(res)
        logger.info(f"  Seed {seed}: F1={res['mean_f1']:.4f}±{res['std_f1']:.4f}  AUC={res['mean_auc']:.4f}")

    # ---- Run 2: Enriched features, multi-seed ----
    logger.info("\n" + "=" * 60)
    logger.info("RUN B: Enriched features (12 descriptors) — multi-seed ensemble")
    logger.info("=" * 60)

    results_enriched = []
    for i, seed in enumerate(seeds):
        logger.info(f"\n--- Seed {seed} ({i+1}/{args.n_seeds}) ---")
        seed_dir = os.path.join(OUTDIR, f"enriched_seed_{seed}")
        res = run_single_seed(df, extra_cols_all, seed, seed_dir)
        results_enriched.append(res)
        logger.info(f"  Seed {seed}: F1={res['mean_f1']:.4f}±{res['std_f1']:.4f}  AUC={res['mean_auc']:.4f}")

    # ---- Summary ----
    print_summary("A: Original (ha_num, o_num)", results_orig)
    print_summary("B: Enriched (12 descriptors)", results_enriched)

    # Save all results
    all_results = {
        "original_features": results_orig,
        "enriched_features": results_enriched,
        "extra_cols_original": extra_cols_orig,
        "extra_cols_enriched": extra_cols_all,
        "seeds": seeds,
    }
    with open(os.path.join(OUTDIR, "ensemble_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)

    logger.info(f"\nResults saved to {OUTDIR}/ensemble_results.json")


def print_summary(label: str, results: list):
    """Print ensemble summary across seeds."""
    f1s = [r["mean_f1"] for r in results]
    aucs = [r["mean_auc"] for r in results]

    # Per-seed breakdown
    print(f"\n{'=' * 70}")
    print(f"  {label}")
    print(f"{'=' * 70}")
    for r in results:
        print(
            f"  Seed {r['seed']:4d}: F1={r['mean_f1']:.4f}±{r['std_f1']:.4f}  "
            f"AUC={r['mean_auc']:.4f}±{r['std_auc']:.4f}"
        )
    print(f"{'-' * 70}")
    print(
        f"  Ensemble ({len(results)} seeds):\n"
        f"    F1  = {np.mean(f1s):.4f} ± {np.std(f1s):.4f}  "
        f"(range: {np.min(f1s):.4f} – {np.max(f1s):.4f})\n"
        f"    AUC = {np.mean(aucs):.4f} ± {np.std(aucs):.4f}  "
        f"(range: {np.min(aucs):.4f} – {np.max(aucs):.4f})"
    )
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
