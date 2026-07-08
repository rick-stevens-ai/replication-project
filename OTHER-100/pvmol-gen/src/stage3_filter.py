"""
Stage 3: Physicochemical filtering and candidate selection.

Steps:
  1. Compute RDKit properties (SA, PAINS, HBD, HBA, TPSA)
  2. Compute xTB properties (HOMO-LUMO gap, dipole moment)
  3. Apply seven filters
  4. Cluster into 10 groups, pick one per cluster
"""
import logging
import os
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from sklearn.cluster import AgglomerativeClustering
from tqdm import tqdm

from config import (
    GEN_CYCLE_DIR, RESULTS_DIR, PROPERTIES_FILE, FILTERED_FILE, SELECTED_FILE,
    SA_MAX, HBD_RANGE, HBA_RANGE, TPSA_RANGE, GAP_RANGE, DIPOLE_RANGE,
    NUM_CLUSTERS, XTB_WORKERS
)
from sa_scorer import calculate_score as sa_score
from utils import morgan_fingerprint, fp_to_array

RDLogger.DisableLog("rdApp.*")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── PAINS filter ────────────────────────────────────────
_pains_params = FilterCatalogParams()
_pains_params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
_pains_catalog = FilterCatalog(_pains_params)


def compute_rdkit_properties(smiles: str) -> dict | None:
    """Compute all RDKit-based molecular properties."""
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Chem.MolSanitizeException:
        return None

    return {
        "SMILES": smiles,
        "SA": sa_score(mol),
        "PAINS": _pains_catalog.HasMatch(mol),
        "HBD": rdMolDescriptors.CalcNumHBD(mol),
        "HBA": rdMolDescriptors.CalcNumHBA(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "MolWt": rdMolDescriptors.CalcExactMolWt(mol),
    }


def compute_xtb_properties(smiles: str) -> tuple:
    """
    Compute HOMO-LUMO gap and dipole moment using GFN2-xTB.
    Returns (smiles, gap_eV, dipole_debye).
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return smiles, np.nan, np.nan

    mol = Chem.AddHs(mol)
    result_embed = AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    if result_embed != 0 or mol.GetNumConformers() == 0:
        return smiles, np.nan, np.nan

    # Write XYZ
    conf = mol.GetConformer(0)
    coords = conf.GetPositions()
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]

    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False, mode="w") as f:
        f.write(f"{mol.GetNumAtoms()}\n\n")
        for atom, pos in zip(atoms, coords):
            f.write(f"{atom} {pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}\n")
        xyz_path = f.name

    try:
        proc = subprocess.run(
            ["xtb", xyz_path, "--opt", "none"],  # Match original: single-point, no optimization
            capture_output=True, text=True, timeout=120
        )

        gap = dip = np.nan
        for line in proc.stdout.splitlines():
            clean = line.replace("|", "").strip()
            # HOMO-LUMO gap: "HOMO-LUMO GAP   2.842 eV" or "HOMO-LUMO/GAP   2.842 eV"
            if "HOMO-LUMO" in clean and "GAP" in clean:
                try:
                    gap = float(clean.split()[-2])
                except (ValueError, IndexError):
                    pass
            # Total dipole: "Total Dipole     2.05 Debye" (match original parse)
            if "Total Dipole" in clean and "Debye" in clean:
                try:
                    dip = float(clean.split()[-2])
                except (ValueError, IndexError):
                    pass

        return smiles, gap, dip

    except subprocess.TimeoutExpired:
        logger.warning(f"xTB timeout for {smiles}")
        return smiles, np.nan, np.nan
    except FileNotFoundError:
        logger.error("xTB not found. Install with: conda install -c conda-forge xtb")
        return smiles, np.nan, np.nan
    finally:
        os.remove(xyz_path)
        # Clean up xTB output files
        for f in ["charges", "wbo", "xtbrestart", "xtbtopo.mol", ".xtboptok"]:
            try:
                os.remove(f)
            except FileNotFoundError:
                pass


def compute_gasteiger_dipole(smiles: str) -> float:
    """
    Fallback dipole moment estimation using Gasteiger charges.
    Less accurate than xTB but always available.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.nan

    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, AllChem.ETKDG()) != 0:
        return np.nan

    AllChem.ComputeGasteigerCharges(mol)
    conf = mol.GetConformer(0)

    dipole = np.zeros(3)
    for i, atom in enumerate(mol.GetAtoms()):
        charge = float(atom.GetProp("_GasteigerCharge"))
        pos = conf.GetAtomPosition(i)
        dipole += charge * np.array([pos.x, pos.y, pos.z])

    # Convert to Debye (1 e·Å = 4.8032 D)
    return np.linalg.norm(dipole) * 4.8032


# ─── Main Pipeline ───────────────────────────────────────
def compute_all_properties(smiles_list: list, use_xtb: bool = True) -> pd.DataFrame:
    """Compute all properties for a list of SMILES."""
    logger.info(f"Computing RDKit properties for {len(smiles_list)} molecules...")

    # RDKit properties (fast, single-threaded is fine)
    rdkit_records = []
    for smi in tqdm(smiles_list, desc="RDKit"):
        props = compute_rdkit_properties(smi)
        if props is not None:
            rdkit_records.append(props)

    logger.info(f"RDKit: {len(rdkit_records)} valid molecules")

    if use_xtb:
        logger.info(f"Computing xTB properties (HOMO-LUMO gap, dipole)...")
        xtb_results = {}
        with ProcessPoolExecutor(max_workers=XTB_WORKERS) as executor:
            futures = {
                executor.submit(compute_xtb_properties, rec["SMILES"]): rec["SMILES"]
                for rec in rdkit_records
            }
            for future in tqdm(as_completed(futures), total=len(futures), desc="xTB"):
                smi, gap, dip = future.result()
                xtb_results[smi] = (gap, dip)

        # Combine
        records = []
        for rec in rdkit_records:
            gap, dip = xtb_results.get(rec["SMILES"], (np.nan, np.nan))
            rec["Gap"] = gap
            rec["Dipole"] = dip
            records.append(rec)
    else:
        # Use Gasteiger dipole as fallback
        logger.info("Using Gasteiger dipole (xTB not available)...")
        records = []
        for rec in tqdm(rdkit_records, desc="Gasteiger dipole"):
            rec["Gap"] = np.nan  # Can't compute without QM
            rec["Dipole"] = compute_gasteiger_dipole(rec["SMILES"])
            records.append(rec)

    df = pd.DataFrame(records)
    df.to_csv(PROPERTIES_FILE, index=False)
    logger.info(f"Properties saved to {PROPERTIES_FILE}")
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the seven physicochemical filters."""
    n_start = len(df)

    filtered = df[
        (df["SA"] <= SA_MAX) &
        (df["PAINS"] == False) &
        (df["HBA"].between(*HBA_RANGE)) &
        (df["HBD"].between(*HBD_RANGE)) &
        (df["TPSA"].between(*TPSA_RANGE))
    ].copy()

    # Only apply gap/dipole filters if we have the data
    if "Gap" in df.columns and df["Gap"].notna().sum() > 0:
        filtered = filtered[filtered["Gap"].between(*GAP_RANGE)]
    if "Dipole" in df.columns and df["Dipole"].notna().sum() > 0:
        filtered = filtered[filtered["Dipole"].between(*DIPOLE_RANGE)]

    logger.info(f"Filtering: {n_start} → {len(filtered)} molecules")

    # Log per-filter counts
    logger.info(f"  SA ≤ {SA_MAX}: {(df['SA'] <= SA_MAX).sum()}")
    logger.info(f"  No PAINS: {(~df['PAINS']).sum()}")
    logger.info(f"  HBA {HBA_RANGE}: {df['HBA'].between(*HBA_RANGE).sum()}")
    logger.info(f"  HBD {HBD_RANGE}: {df['HBD'].between(*HBD_RANGE).sum()}")
    logger.info(f"  TPSA {TPSA_RANGE}: {df['TPSA'].between(*TPSA_RANGE).sum()}")

    filtered.to_csv(FILTERED_FILE, index=False)
    return filtered


def cluster_and_select(df: pd.DataFrame, n_clusters: int = NUM_CLUSTERS) -> pd.DataFrame:
    """Cluster molecules and select one per cluster."""
    if len(df) < n_clusters:
        logger.warning(f"Only {len(df)} molecules, fewer than {n_clusters} clusters")
        df.to_csv(SELECTED_FILE, index=False)
        return df

    logger.info(f"Clustering {len(df)} molecules into {n_clusters} groups...")

    fps = []
    valid_idx = []
    for i, smi in enumerate(df["SMILES"]):
        fp = morgan_fingerprint(smi)
        if fp is not None:
            fps.append(fp_to_array(fp))
            valid_idx.append(i)

    X = np.array(fps)
    clustering = AgglomerativeClustering(n_clusters=n_clusters)
    labels = clustering.fit_predict(X)

    cluster_df = df.iloc[valid_idx].copy()
    cluster_df["Cluster"] = labels

    # Select one per cluster
    # Original code uses groupby('Cluster').first() — take the first molecule per cluster
    # This is simpler than centroid-based selection and matches the paper's code exactly
    selected = cluster_df.groupby("Cluster").first().reset_index()
    selected.to_csv(SELECTED_FILE, index=False)
    logger.info(f"Selected {len(selected)} candidate molecules")
    logger.info(f"\n{selected[['SMILES', 'SA', 'HBA', 'HBD', 'TPSA', 'Cluster']].to_string()}")

    return selected


# ─── Main ───────────────────────────────────────────────
def run_stage3(use_xtb: bool = True):
    """Run the full filtering pipeline."""
    # Load all generated class 1 molecules
    gen_file = GEN_CYCLE_DIR / "all_generated_class1.csv"
    if not gen_file.exists():
        logger.error(f"Generated molecules file not found: {gen_file}")
        return

    df = pd.read_csv(gen_file)
    smiles_list = df["smiles"].tolist()
    logger.info(f"Loaded {len(smiles_list)} generated class 1 molecules")

    # Compute properties
    props_df = compute_all_properties(smiles_list, use_xtb=use_xtb)

    # Filter
    filtered_df = apply_filters(props_df)

    # Cluster and select
    selected_df = cluster_and_select(filtered_df)

    return selected_df


if __name__ == "__main__":
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-xtb", action="store_true",
                        help="Skip xTB, use Gasteiger dipole instead")
    args = parser.parse_args()

    run_stage3(use_xtb=not args.no_xtb)
