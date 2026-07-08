"""Run Stage 3 filtering + clustering on the paper's pre-computed G_class1 data.

The paper's G_class1.csv already has all 87,750 class 1 molecules with
RDKit and xTB properties computed. We just need to apply the 7 filters,
cluster, and select representatives.
"""

import logging
import sys
import os

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem
from sklearn.cluster import AgglomerativeClustering

RDLogger.DisableLog("rdApp.*")

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from config import (
    SA_MAX, HBD_RANGE, HBA_RANGE, TPSA_RANGE, GAP_RANGE, DIPOLE_RANGE,
    NUM_CLUSTERS, RESULTS_DIR,
)
from utils import morgan_fingerprint, fp_to_array

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/stage3_paper_data.log"),
    ],
)
logger = logging.getLogger(__name__)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load paper's pre-computed data
    df = pd.read_csv("data/G_class1.csv")
    logger.info(f"Loaded {len(df)} class 1 molecules from paper's G_class1.csv")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Properties available: SA={df['SA'].notna().sum()}, "
                f"PAINS={df['PAINS'].notna().sum()}, "
                f"Gap={df['Gap'].notna().sum()}, "
                f"Dipole={df['Dipole'].notna().sum()}")

    # ── Apply 7 filters (matching paper Section 4 of SI) ──
    n_start = len(df)

    # Per-filter breakdown
    f1 = df["SA"] <= SA_MAX
    f2 = df["PAINS"] == False
    f3 = df["HBA"].between(*HBA_RANGE)
    f4 = df["HBD"].between(*HBD_RANGE)
    f5 = df["TPSA"].between(*TPSA_RANGE)
    f6 = df["Gap"].between(*GAP_RANGE)
    f7 = df["Dipole"].between(*DIPOLE_RANGE)

    logger.info(f"\nFilter breakdown ({n_start} starting):")
    logger.info(f"  1. SA <= {SA_MAX}: {f1.sum()} pass ({f1.sum()/n_start*100:.1f}%)")
    logger.info(f"  2. No PAINS: {f2.sum()} pass ({f2.sum()/n_start*100:.1f}%)")
    logger.info(f"  3. HBA {HBA_RANGE}: {f3.sum()} pass ({f3.sum()/n_start*100:.1f}%)")
    logger.info(f"  4. HBD {HBD_RANGE}: {f4.sum()} pass ({f4.sum()/n_start*100:.1f}%)")
    logger.info(f"  5. TPSA {TPSA_RANGE}: {f5.sum()} pass ({f5.sum()/n_start*100:.1f}%)")
    logger.info(f"  6. Gap {GAP_RANGE} eV: {f6.sum()} pass ({f6.sum()/n_start*100:.1f}%)")
    logger.info(f"  7. Dipole {DIPOLE_RANGE} D: {f7.sum()} pass ({f7.sum()/n_start*100:.1f}%)")

    # Sequential filtering (cumulative)
    logger.info(f"\nCumulative filtering:")
    filtered = df.copy()
    for i, (name, mask) in enumerate([
        (f"SA <= {SA_MAX}", f1),
        ("No PAINS", f2),
        (f"HBA {HBA_RANGE}", f3),
        (f"HBD {HBD_RANGE}", f4),
        (f"TPSA {TPSA_RANGE}", f5),
        (f"Gap {GAP_RANGE} eV", f6),
        (f"Dipole {DIPOLE_RANGE} D", f7),
    ], 1):
        filtered = filtered[mask[filtered.index]]
        logger.info(f"  After filter {i} ({name}): {len(filtered)} remain")

    logger.info(f"\nFinal: {n_start} -> {len(filtered)} molecules ({len(filtered)/n_start*100:.1f}%)")
    filtered.to_csv(RESULTS_DIR / "filtered_paper_data.csv", index=False)

    # ── Cluster with agglomerative clustering on Morgan FPs ──
    logger.info(f"\nClustering {len(filtered)} molecules into {NUM_CLUSTERS} groups...")

    fps = []
    valid_idx = []
    for i, smi in enumerate(filtered["SMILES"]):
        fp = morgan_fingerprint(smi)
        if fp is not None:
            fps.append(fp_to_array(fp))
            valid_idx.append(i)

    logger.info(f"Valid fingerprints: {len(fps)} of {len(filtered)}")

    X = np.array(fps)
    clustering = AgglomerativeClustering(n_clusters=NUM_CLUSTERS)
    labels = clustering.fit_predict(X)

    cluster_df = filtered.iloc[valid_idx].copy()
    cluster_df["Cluster"] = labels

    # Cluster size distribution
    logger.info(f"\nCluster sizes:")
    for c in range(NUM_CLUSTERS):
        n = (labels == c).sum()
        logger.info(f"  Cluster {c}: {n} molecules")

    # Select one representative per cluster (first occurrence, matching paper)
    selected = cluster_df.groupby("Cluster").first().reset_index()
    selected = selected.sort_values("Cluster")

    logger.info(f"\n{'='*80}")
    logger.info(f"SELECTED {len(selected)} CANDIDATE MOLECULES")
    logger.info(f"{'='*80}")
    for _, row in selected.iterrows():
        logger.info(
            f"  Cluster {row['Cluster']}: SA={row['SA']:.2f} HBA={row['HBA']} "
            f"HBD={row['HBD']} TPSA={row['TPSA']:.1f} "
            f"Gap={row['Gap']:.2f}eV Dipole={row['Dipole']:.2f}D"
        )
        logger.info(f"    SMILES: {row['SMILES']}")

    selected.to_csv(RESULTS_DIR / "selected_paper_data.csv", index=False)
    logger.info(f"\nResults saved to {RESULTS_DIR}/")

    # ── Compare with paper's Rep10 ──
    logger.info(f"\n{'='*80}")
    logger.info("COMPARISON WITH PAPER'S REP10")
    logger.info(f"{'='*80}")
    try:
        rep10 = pd.read_excel("data/dataset.xlsx", sheet_name="Rep10")
        logger.info(f"Paper's Rep10 has {len(rep10)} molecules")
        logger.info(f"Columns: {list(rep10.columns)}")
        logger.info(f"\n{rep10.to_string()}")
    except Exception as e:
        logger.warning(f"Could not load Rep10: {e}")


if __name__ == "__main__":
    main()
