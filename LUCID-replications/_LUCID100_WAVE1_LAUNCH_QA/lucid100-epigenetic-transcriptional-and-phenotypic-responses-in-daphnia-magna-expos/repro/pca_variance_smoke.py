#!/usr/bin/env python3
"""LUCID100 slot 5 — PCA variance smoke test.

Acceptance metric (from Thaulow et al. 2020 §3.8):
    PC1 + PC2 explained variance ratio == 0.8541 +/- 0.01

Reproduction path (deferred — see FIRST_PASS_REPORT.md):
    1. Hand-digitise mean dose-response values for the endpoints listed in
       repro/digitized_dose_response_template.csv from Figs. 1, 2, 3, 6 of
       the paper using WebPlotDigitizer or equivalent.
    2. Pivot to a (dose_rate x endpoint) matrix of MEANS.
    3. Standardise columns (z-score) and run PCA.
    4. PASS if PC1+PC2 explained variance is within +/-0.01 of 0.8541.

Until step 1 is done, this script runs on a SYNTHETIC dose-response matrix
that mimics the paper's qualitative structure (monotone dose effects in two
opposing endpoint clusters). The synthetic run is purely a wiring smoke test
and is NOT a replication claim.

Run:
    python3 pca_variance_smoke.py
or with a populated template:
    python3 pca_variance_smoke.py --csv digitized_dose_response_template.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

try:
    import pandas as pd
    from sklearn.decomposition import PCA
except Exception as exc:  # pragma: no cover - friendly error
    sys.stderr.write(
        "Missing dependency: install with `pip install numpy pandas scikit-learn` "
        f"(import error: {exc})\n"
    )
    sys.exit(2)


TARGET_VARIANCE = 0.8541
TOLERANCE = 0.01


def synthetic_matrix(seed: int = 0) -> pd.DataFrame:
    """Return a small (dose_rate x endpoint) mean matrix for smoke testing.

    Two opposing trends, plus moderate noise, designed so that PCA on the
    standardised matrix puts most variance on PC1 and the rest on PC2,
    roughly mimicking the paper's reported 85% PC1+PC2 share.
    """

    rng = np.random.default_rng(seed)
    dose_rates = np.array([0.0, 0.4, 1.0, 4.0, 10.0, 40.0])
    log_dose = np.log10(dose_rates + 0.1)
    n_dose = len(dose_rates)

    # Cluster A: monotone up with dose (e.g. global methylation, Vtg1, Vtg2, Met)
    cluster_a = log_dose[:, None] * np.array([[1.0, 0.9, 0.95, 1.05]]) \
        + rng.normal(scale=0.05, size=(n_dose, 4))
    # Cluster B: monotone down with dose (e.g. Sahh, Dnmt3a2, Calm, Rad50, Triap, Gst)
    cluster_b = -log_dose[:, None] * np.array([[1.0, 0.95, 1.0, 1.1, 0.85, 0.9]]) \
        + rng.normal(scale=0.05, size=(n_dose, 6))

    df = pd.DataFrame(
        np.hstack([cluster_a, cluster_b]),
        index=pd.Index(dose_rates, name="dose_rate_mGy_h"),
        columns=[
            "global_5mC", "Vtg1", "Vtg2", "Met",
            "Sahh", "Dnmt3a2", "Calm", "Rad50", "Triap", "Gst",
        ],
    )
    return df


def load_template(csv_path: Path) -> pd.DataFrame:
    """Pivot the digitised template to a (dose_rate x endpoint_label) means matrix.

    Drops rows that have a blank `mean`. Requires at least 3 dose-rate rows per
    endpoint to be useful for PCA.
    """

    long = pd.read_csv(csv_path)
    if "mean" not in long.columns or "dose_rate_mGy_h" not in long.columns:
        raise SystemExit("CSV must have columns 'mean', 'dose_rate_mGy_h', 'endpoint'.")
    long = long.dropna(subset=["mean"])
    if long.empty:
        raise SystemExit(
            "No populated `mean` rows in the digitised template — fill it in first."
        )
    long["endpoint_label"] = long["figure"].astype(str) + ":" + long["endpoint"].astype(str)
    wide = long.pivot_table(
        index="dose_rate_mGy_h", columns="endpoint_label", values="mean", aggfunc="mean"
    )
    return wide.dropna(axis=1)  # only keep endpoints with full dose coverage


def run_pca(matrix: pd.DataFrame) -> tuple[float, float]:
    if matrix.shape[1] < 2:
        raise SystemExit(
            f"Need at least 2 endpoint columns for PCA; got matrix shape {matrix.shape}."
        )
    x = matrix.to_numpy(dtype=float)
    # Column-wise z-score (the scale=TRUE convention used in XLSTAT defaults).
    x = (x - x.mean(axis=0)) / x.std(axis=0, ddof=0)
    pca = PCA(n_components=min(2, x.shape[1]))
    pca.fit(x)
    pc1 = float(pca.explained_variance_ratio_[0])
    pc2 = float(pca.explained_variance_ratio_[1]) if pca.n_components_ > 1 else 0.0
    return pc1, pc2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Path to a populated digitized_dose_response_template.csv",
    )
    args = parser.parse_args()

    if args.csv is None:
        matrix = synthetic_matrix()
        mode = "SYNTHETIC (wiring smoke test — NOT a replication)"
    else:
        matrix = load_template(args.csv)
        mode = f"DIGITISED ({args.csv})"

    pc1, pc2 = run_pca(matrix)
    pc12 = pc1 + pc2
    ok = abs(pc12 - TARGET_VARIANCE) <= TOLERANCE

    print(f"mode               : {mode}")
    print(f"matrix shape       : {matrix.shape}  (dose_rates x endpoints)")
    print(f"PC1 explained var  : {pc1:.4f}")
    print(f"PC2 explained var  : {pc2:.4f}")
    print(f"PC1+PC2 explained  : {pc12:.4f}")
    print(f"target (Thaulow 2020 §3.8): {TARGET_VARIANCE:.4f} +/- {TOLERANCE:.2f}")
    verdict = "PASS" if ok else "MISS"
    print(f"acceptance         : {verdict}")
    if args.csv is None:
        print("note               : synthetic mode — verdict is informational only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
