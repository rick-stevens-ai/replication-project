"""
Shared utilities: SMILES validation, fingerprinting, augmentation.
"""
import logging
from typing import Optional, List, Set

import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, rdMolDescriptors
from rdkit.DataStructs import TanimotoSimilarity

RDLogger.DisableLog("rdApp.*")

logger = logging.getLogger(__name__)


def validate_smiles(smiles: str) -> Optional[str]:
    """Return canonical SMILES if valid, else None."""
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if mol is None:
            return None
        Chem.SanitizeMol(mol)
        return Chem.MolToSmiles(mol, canonical=True)
    except Exception:
        return None


def augment_smiles(smiles: str, n: int = 5) -> List[str]:
    """Generate n random SMILES representations of a molecule."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return [smiles]
    augmented = {Chem.MolToSmiles(mol, canonical=True)}
    for _ in range(n * 3):  # oversample to hit target
        augmented.add(Chem.MolToSmiles(mol, canonical=False))
        if len(augmented) >= n + 1:
            break
    return list(augmented)


def morgan_fingerprint(smiles: str, radius: int = 2, n_bits: int = 1024):
    """Compute Morgan fingerprint as bit vector."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)


def tanimoto(fp1, fp2) -> float:
    """Tanimoto similarity between two fingerprints."""
    return TanimotoSimilarity(fp1, fp2)


def fp_to_array(fp) -> np.ndarray:
    """Convert RDKit fingerprint to numpy array."""
    return np.array(list(fp), dtype=np.float32)


def compute_basic_descriptors(smiles: str) -> Optional[dict]:
    """Compute RDKit descriptors for a molecule."""
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Chem.MolSanitizeException:
        return None
    return {
        "SMILES": smiles,
        "HBD": rdMolDescriptors.CalcNumHBD(mol),
        "HBA": rdMolDescriptors.CalcNumHBA(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "MolWt": rdMolDescriptors.CalcExactMolWt(mol),
        "NumRotBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "NumRings": rdMolDescriptors.CalcNumRings(mol),
    }


def is_novel(smiles: str, known_set: Set[str]) -> bool:
    """Check if a canonical SMILES is not in the known set."""
    canon = validate_smiles(smiles)
    if canon is None:
        return False
    return canon not in known_set
