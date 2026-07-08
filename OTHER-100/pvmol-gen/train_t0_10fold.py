"""10-fold CV using best Optuna config + enriched RDKit descriptors."""

import logging
import sys

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
        logging.FileHandler("logs/train_t0_10fold.log"),
    ],
)
logger = logging.getLogger(__name__)

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


def compute_descriptors(df):
    df = df.copy()
    for name, func in DESCRIPTOR_FUNCS.items():
        values = []
        for smi in df["smiles"]:
            mol = Chem.MolFromSmiles(smi)
            values.append(func(mol) if mol else np.nan)
        df[name] = values
    return df


if __name__ == "__main__":
    df = pd.read_csv("data/T0.csv")
    df = compute_descriptors(df)

    extra_cols = ["ha_num", "o_num"] + list(DESCRIPTOR_FUNCS.keys())
    logger.info(f"Extra features ({len(extra_cols)}): {extra_cols}")

    clf = SmilesXClassifier(
        data=df,
        smiles_col="smiles",
        label_col="bin_class",
        extra_feature_cols=extra_cols,
        # Best Optuna config
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
        outdir="models/t0_10fold",
        seed=42,
    )

    result = clf.cross_validate(n_folds=10, augment=True, threshold=None)
    print("\n" + result.summary())
