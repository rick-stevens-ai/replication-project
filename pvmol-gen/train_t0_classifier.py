"""Train SMILES-X binary classifier on T0 dataset.

Uses the local smilesx package (PyTorch BiLSTM+Attention) with 5-fold
stratified cross-validation, SMILES augmentation, and extra features
(ha_num, o_num) matching the Fajar et al. protocol.
"""

import logging
import sys

from smilesx import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/train_t0.log"),
    ],
)

if __name__ == "__main__":
    clf = SmilesXClassifier(
        # Data
        data_path="data/T0.csv",
        smiles_col="smiles",
        label_col="bin_class",
        extra_feature_cols=["ha_num", "o_num"],
        # Architecture (matches paper defaults)
        embed_dim=512,
        lstm_units=128,
        tdense_units=128,
        dense_depth=0,
        dropout=0.3,
        # Training
        lr=1e-4,
        weight_decay=1e-4,
        batch_size=16,
        n_epochs=100,
        patience=25,
        class_weight=True,
        # Output
        outdir="models/t0_classifier",
        seed=42,
    )

    result = clf.cross_validate(
        n_folds=5,
        augment=True,
        threshold=None,  # auto-optimize per fold
    )

    print("\n" + result.summary())
