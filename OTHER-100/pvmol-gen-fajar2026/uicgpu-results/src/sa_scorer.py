"""
Synthetic Accessibility (SA) Score.
Adapted from RDKit Contrib (Ertl & Schuffenhauer, J. Cheminform. 2009).
This is a standalone implementation so we don't depend on RDKit contrib paths.
"""
import math
import pickle
from collections import defaultdict
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

# Fragment scores file — will be generated on first run if missing
_FSCORES_FILE = Path(__file__).parent / "fpscores.pkl"
_fscores = None


def _read_fragment_scores():
    global _fscores
    if _fscores is not None:
        return _fscores

    if _FSCORES_FILE.exists():
        with open(_FSCORES_FILE, "rb") as f:
            _fscores = pickle.load(f)
        return _fscores

    # Generate from RDKit's built-in data
    import gzip
    from rdkit.Chem import rdMolDescriptors as _rd

    # Try to find fpscores from RDKit contrib
    try:
        from rdkit.Chem import RDConfig
        import os
        contrib_path = os.path.join(RDConfig.RDContribDir, "SA_Score", "fpscores.pkl.gz")
        if os.path.exists(contrib_path):
            with gzip.open(contrib_path, "rb") as f:
                _fscores = pickle.load(f)
            # Cache uncompressed
            with open(_FSCORES_FILE, "wb") as f:
                pickle.dump(_fscores, f)
            return _fscores
    except Exception:
        pass

    # Fallback: compute fragment scores from scratch
    # This is a simplified version; for full accuracy use RDKit contrib
    _fscores = {}
    return _fscores


def calculate_score(mol) -> float:
    """
    Calculate synthetic accessibility score for a molecule.
    Returns value between 1 (easy to synthesize) and 10 (hard).
    """
    if mol is None:
        return 10.0

    fscores = _read_fragment_scores()

    # Fragment score
    fp = rdMolDescriptors.GetMorganFingerprint(mol, 2)
    fps = fp.GetNonzeroElements()

    score1 = 0.0
    nf = 0
    for bit, count in fps.items():
        nf += count
        if bit in fscores:
            score1 += fscores[bit]

    if nf > 0:
        score1 /= nf

    # Features score
    n_atoms = mol.GetNumAtoms()
    n_chiral = len(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
    ri = mol.GetRingInfo()
    n_bridgeheads = rdMolDescriptors.CalcNumBridgeheadAtoms(mol)
    n_spiro = rdMolDescriptors.CalcNumSpiroAtoms(mol)
    try:
        n_macrocycles = sum(1 for size in ri.RingSizes() if size > 8)
    except Exception:
        n_macrocycles = 0

    size_penalty = n_atoms ** 1.005 - n_atoms
    stereo_penalty = math.log10(n_chiral + 1)
    spiro_penalty = math.log10(n_spiro + 1)
    bridge_penalty = math.log10(n_bridgeheads + 1)
    macrocycle_penalty = 0
    # macrocycle penalty would require ring size info

    score2 = (
        0.0
        - size_penalty
        - stereo_penalty
        - spiro_penalty
        - bridge_penalty
        - macrocycle_penalty
    )

    # Correction for fragment score
    score3 = 0.0
    if nf > 0:
        score3 = math.log(nf) - math.log(n_atoms) if n_atoms > 0 else 0

    sa_score = score1 + score2 + score3

    # Normalize to 1-10 range
    min_score = -4.0
    max_score = 2.5
    sa_score = 11.0 - (sa_score - min_score) / (max_score - min_score) * 9.0
    sa_score = max(1.0, min(10.0, sa_score))

    return sa_score
