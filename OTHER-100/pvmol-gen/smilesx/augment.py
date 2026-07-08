"""SMILES augmentation via atom-order enumeration.

Reproduces the augmentation from SMILES-X (augm.py): for each molecule,
generate non-canonical SMILES by rotating the atom numbering.
"""

from typing import List, Optional
import logging

from rdkit import Chem

logger = logging.getLogger(__name__)


def enumerate_smiles(smiles: str, canonical: bool = True) -> List[str]:
    """Generate SMILES variants by rotating atom indices.

    Parameters
    ----------
    smiles : str
        Input canonical SMILES string.
    canonical : bool
        If True, return only the canonical form (no augmentation).
        If False, enumerate all atom-rotation variants.

    Returns
    -------
    list of str
        Unique SMILES variants. Returns empty list if molecule is invalid.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return []
    except Exception:
        return []

    n_atoms = mol.GetNumAtoms()
    if n_atoms == 0:
        return []

    results = set()

    if canonical:
        canon = Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)
        if canon:
            results.add(canon)
    else:
        # Generate variants by rotating atom ordering
        atom_order = list(range(n_atoms))
        for start in range(n_atoms):
            rotated = atom_order[start:] + atom_order[:start]
            try:
                renumbered = Chem.RenumberAtoms(mol, rotated)
                smi = Chem.MolToSmiles(renumbered, isomericSmiles=True, canonical=False)
                if smi:
                    results.add(smi)
            except Exception:
                continue
        # Also include the canonical form
        canon = Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)
        if canon:
            results.add(canon)

    return list(results)


def augment_smiles(
    smiles_list: List[str],
    labels: Optional[List] = None,
    augment: bool = True,
) -> tuple:
    """Augment a dataset of SMILES strings.

    Parameters
    ----------
    smiles_list : list of str
        Input SMILES.
    labels : list, optional
        Corresponding labels (repeated for each augmented variant).
    augment : bool
        If True, enumerate atom-rotation variants. If False, just canonicalize.

    Returns
    -------
    aug_smiles : list of str
        Augmented SMILES.
    aug_labels : list or None
        Corresponding labels (if provided).
    group_ids : list of int
        Maps each augmented SMILES back to its original index.
    """
    aug_smiles = []
    aug_labels = []
    group_ids = []
    rejected = []

    for i, smi in enumerate(smiles_list):
        variants = enumerate_smiles(smi, canonical=not augment)
        if not variants:
            rejected.append(smi)
            continue
        for v in variants:
            aug_smiles.append(v)
            if labels is not None:
                aug_labels.append(labels[i])
            group_ids.append(i)

    if rejected:
        logger.warning(f"Rejected {len(rejected)} invalid SMILES: {rejected[:5]}...")

    return (
        aug_smiles,
        aug_labels if labels is not None else None,
        group_ids,
    )
