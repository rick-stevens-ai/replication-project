"""
Stage 1b: PubChem Tanimoto Augmentation.

Steps:
  1. Take top-performing class 1 molecules (ΔPCEnorm > 0.16)
  2. Query PubChem for molecules with ≥ 80% Tanimoto similarity
  3. Classify augmented molecules with the trained SMILES-X
  4. Combine class 1 molecules into Data T1
"""
import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

from rdkit import Chem
from rdkit.Chem import AllChem

from config import (
    T0_FILE, T_AUG_FILE, T1_FILE, CLASSIFIER_DIR,
    PCE_THRESHOLD, PCE_TOP_THRESHOLD, TANIMOTO_THRESHOLD,
    PUBCHEM_MAX_RESULTS, CLASSIFICATION_THRESHOLD, RESULTS_DIR
)
from utils import validate_smiles, morgan_fingerprint, tanimoto

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def smiles_to_pubchem_query(smiles: str, threshold: float = TANIMOTO_THRESHOLD,
                            max_results: int = PUBCHEM_MAX_RESULTS) -> list:
    """
    Query PubChem for similar molecules using Tanimoto similarity.
    Uses PubChem PUG REST API.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    # Step 1: Submit similarity search
    try:
        url = (f"{base_url}/compound/similarity/smiles/"
               f"{requests.utils.quote(smiles)}/JSON"
               f"?Threshold={int(threshold * 100)}&MaxRecords={max_results}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Get the list key (async)
        if "Waiting" in data:
            list_key = data["Waiting"]["ListKey"]
        elif "IdentifierList" in data:
            cids = data["IdentifierList"]["CID"]
            return _fetch_smiles_for_cids(cids, base_url)
        else:
            logger.warning(f"Unexpected response for {smiles}: {list(data.keys())}")
            return []

        # Step 2: Poll for results
        for _ in range(30):  # max 30 polls
            time.sleep(2)
            poll_url = f"{base_url}/compound/listkey/{list_key}/cids/JSON"
            resp = requests.get(poll_url, timeout=30)
            data = resp.json()

            if "IdentifierList" in data:
                cids = data["IdentifierList"]["CID"]
                return _fetch_smiles_for_cids(cids, base_url)
            elif "Waiting" in data:
                continue
            else:
                break

    except Exception as e:
        logger.warning(f"PubChem query failed for {smiles}: {e}")

    return []


def _fetch_smiles_for_cids(cids: list, base_url: str, batch_size: int = 100) -> list:
    """Fetch canonical SMILES for a list of PubChem CIDs."""
    all_smiles = []
    for i in range(0, len(cids), batch_size):
        batch = cids[i:i+batch_size]
        cid_str = ",".join(str(c) for c in batch)
        try:
            url = f"{base_url}/compound/cid/{cid_str}/property/CanonicalSMILES/JSON"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            for prop in data.get("PropertyTable", {}).get("Properties", []):
                # PubChem may return SMILES under different keys
                smi = (prop.get("CanonicalSMILES") or 
                       prop.get("ConnectivitySMILES") or
                       prop.get("SMILES") or
                       prop.get("IsomericSMILES"))
                if smi:
                    all_smiles.append(smi)
        except Exception as e:
            logger.warning(f"Failed to fetch SMILES for CID batch: {e}")
        time.sleep(0.5)  # Rate limit
    return all_smiles


def run_pubchem_augmentation():
    """Query PubChem for similar molecules to top performers."""
    df = pd.read_csv(T0_FILE)
    # Normalize columns
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if "smiles" in cl:
            col_map[c] = "smiles"
        elif "pce" in cl or "delta" in cl:
            col_map[c] = "delta_pce_norm"
    df = df.rename(columns=col_map)

    # Select top performers
    top = df[df["delta_pce_norm"] > PCE_TOP_THRESHOLD]
    logger.info(f"Top performers (ΔPCEnorm > {PCE_TOP_THRESHOLD}): {len(top)}")

    all_augmented = set()
    known_smiles = set(df["smiles"].apply(validate_smiles).dropna())

    for _, row in tqdm(top.iterrows(), total=len(top), desc="PubChem queries"):
        smi = row["smiles"]
        similar = smiles_to_pubchem_query(smi)
        for s in similar:
            canon = validate_smiles(s)
            if canon and canon not in known_smiles:
                all_augmented.add(canon)
        time.sleep(1)  # Rate limit between queries

    logger.info(f"PubChem augmentation: {len(all_augmented)} novel molecules found")

    # Save
    aug_df = pd.DataFrame({"smiles": list(all_augmented)})
    aug_df.to_csv(T_AUG_FILE, index=False)
    logger.info(f"Saved to {T_AUG_FILE}")
    return aug_df


def _compute_extra_features(smiles: str) -> tuple:
    """Compute ha_num (H-bond acceptors) and o_num (oxygen count) for a SMILES."""
    from rdkit.Chem import rdMolDescriptors
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return (0.0, 0.0)
    ha_num = float(rdMolDescriptors.CalcNumHBA(mol))
    o_num = float(sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O'))
    return (ha_num, o_num)


def build_t1_dataset():
    """
    Classify T-aug molecules and combine class 1 from T0 + T-aug into T1.
    Computes ha_num/o_num extra features for T-aug (matching author's approach).
    """
    import pickle
    import json
    from stage1_classifier import predict_class

    # Load tokenizer
    with open(CLASSIFIER_DIR / "tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    # Check if model uses extra features
    config_path = CLASSIFIER_DIR / "model_config.json"
    uses_extra = False
    if config_path.exists():
        with open(config_path) as f:
            cfg = json.load(f)
        uses_extra = cfg.get("extra_dim", 0) > 0

    # T0 class 1
    df_t0 = pd.read_csv(T0_FILE)
    col_map = {}
    for c in df_t0.columns:
        cl = c.lower().strip()
        if "smiles" in cl:
            col_map[c] = "smiles"
        elif "pce" in cl or "delta" in cl:
            col_map[c] = "delta_pce_norm"
    df_t0 = df_t0.rename(columns=col_map)
    t0_class1 = df_t0[df_t0["delta_pce_norm"] >= PCE_THRESHOLD]["smiles"].tolist()
    logger.info(f"T0 class 1: {len(t0_class1)}")

    # T-aug classification
    df_aug = pd.read_csv(T_AUG_FILE)
    aug_smiles = df_aug["smiles"].tolist()
    logger.info(f"Classifying {len(aug_smiles)} augmented molecules...")

    # Compute extra features for T-aug molecules if model uses them
    extra_features = None
    if uses_extra:
        logger.info("Computing ha_num/o_num extra features for T-aug molecules...")
        extra_features = [_compute_extra_features(s) for s in tqdm(aug_smiles, desc="Extra features")]
        logger.info(f"Extra features computed for {len(extra_features)} molecules")

    probs = predict_class(aug_smiles, tokenizer, extra_features=extra_features)
    preds = (probs >= CLASSIFICATION_THRESHOLD).astype(int)
    aug_class1 = [s for s, p in zip(aug_smiles, preds) if p == 1]
    pct = len(aug_class1)/len(aug_smiles)*100 if len(aug_smiles) > 0 else 0
    logger.info(f"T-aug class 1: {len(aug_class1)} ({pct:.1f}%)")

    # Combine
    t1_smiles = list(set(t0_class1 + aug_class1))
    logger.info(f"T1 total (unique class 1): {len(t1_smiles)}")

    t1_df = pd.DataFrame({"smiles": t1_smiles})
    t1_df.to_csv(T1_FILE, index=False)
    logger.info(f"Saved to {T1_FILE}")
    return t1_df


if __name__ == "__main__":
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Stage 1b: PubChem augmentation...")
    run_pubchem_augmentation()

    logger.info("Building T1 dataset...")
    build_t1_dataset()
    logger.info("Done.")
