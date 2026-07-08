"""
Step 2: Build ground-truth timescales from the long reference trajectories.

Loads 10 × 100 ns trajectories (saved at 1 ps intervals = 100,001 frames each),
clusters into 40 k-means states in φ/ψ space (same clustering as short data),
and builds standard MSMs at multiple lag times to extract converged t₂ and t₃.

Paper reference values: t₂ ≈ 1400 ps, t₃ ≈ 70 ps
"""

import numpy as np
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fast_counts import count_stats_fast, direct_msm


def main():
    data_dir = Path(__file__).parent.parent / "data" / "alanine_long"
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Long Reference Analysis — Ground Truth Timescales")
    print("=" * 60)

    # Load merged long-reference data
    f = np.load(data_dir / "long_reference_merged.npz")
    dihedrals = f['dihedrals']  # (n_traj, n_frames, 2)
    n_traj, n_frames, _ = dihedrals.shape
    print(f"Loaded: {n_traj} trajectories × {n_frames} frames")
    print(f"  Total simulation time: {n_traj * n_frames * 1e-3:.0f} ns")

    # Cluster into 40 states using cos/sin transform
    n_clusters = 40
    flat = dihedrals.reshape(-1, 2)
    features = np.column_stack([
        np.cos(flat[:, 0]), np.sin(flat[:, 0]),
        np.cos(flat[:, 1]), np.sin(flat[:, 1])
    ])

    print(f"\nClustering {len(features)} frames into {n_clusters} states...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    labels = kmeans.fit_predict(features)
    assignments = labels.reshape(n_traj, n_frames)

    # Cluster centers in φ/ψ
    c4 = kmeans.cluster_centers_
    centers_phi = np.arctan2(c4[:, 1], c4[:, 0])
    centers_psi = np.arctan2(c4[:, 3], c4[:, 2])
    centers = np.column_stack([centers_phi, centers_psi])

    # Right-half states (φ > 0)
    right_states = np.where(centers[:, 0] > 0)[0]
    print(f"  States with φ > 0: {len(right_states)} of {n_clusters}")

    # Build MSMs at multiple lag times
    # Data saved at 1 ps intervals, so lag in frames = lag in ps
    lag_frames = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

    print(f"\nBuilding MSMs at {len(lag_frames)} lag times...")
    print(f"{'Lag (ps)':>10s}  {'t₂ (ps)':>10s}  {'t₃ (ps)':>10s}  {'π(φ≥0)':>10s}")
    print("-" * 50)

    results = {
        'lag_ps': [],
        't2': [],
        't3': [],
        'pi_right': [],
    }

    for tau in lag_frames:
        if tau * 2 >= n_frames:
            print(f"  {tau:>8d}  (skipped — too large for trajectory length)")
            continue

        # Count statistics
        s, S_tau, S2 = count_stats_fast(assignments, np.arange(n_clusters), n_clusters, tau)

        # Direct MSM
        T, ev, ts = direct_msm(S_tau, n_clusters, tau)
        ts_ps = ts * 1.0  # 1 frame = 1 ps

        # Stationary distribution
        try:
            ev_pi, vecs = linalg.eig(T.T)
            idx_pi = np.argmin(np.abs(ev_pi - 1.0))
            pi = np.real(vecs[:, idx_pi])
            pi = np.abs(pi)
            pi /= pi.sum()
            pi_right = pi[right_states].sum()
        except Exception:
            pi_right = np.nan

        results['lag_ps'].append(tau)
        results['t2'].append(ts_ps[0])
        results['t3'].append(ts_ps[1])
        results['pi_right'].append(pi_right)

        print(f"  {tau:>8d}  {ts_ps[0]:>10.1f}  {ts_ps[1]:>10.1f}  {pi_right:>10.4f}")

    # Convert to arrays
    for k in results:
        results[k] = np.array(results[k])

    # Extract converged values (at largest reasonable lag time)
    # Use lag=500 ps as reference (well-converged but not too large)
    ref_idx = np.argmin(np.abs(results['lag_ps'] - 500))
    t2_ref = results['t2'][ref_idx]
    t3_ref = results['t3'][ref_idx]
    pi_right_ref = results['pi_right'][ref_idx]

    print(f"\n{'='*60}")
    print(f"GROUND TRUTH (converged at lag={results['lag_ps'][ref_idx]:.0f} ps):")
    print(f"  t₂ = {t2_ref:.1f} ps  (paper: ~1400 ps)")
    print(f"  t₃ = {t3_ref:.1f} ps  (paper: ~70 ps)")
    print(f"  π(φ≥0) = {pi_right_ref:.4f}  (paper: ~0.35-0.40)")
    print(f"{'='*60}")

    # Plot implied timescales
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    ax = axes[0]
    ax.semilogx(results['lag_ps'], results['t2'], 'b-o', ms=4, label='t₂')
    ax.axhline(1400, color='k', ls='--', alpha=0.5, label='Paper ref (1400 ps)')
    ax.set_xlabel('Lag time (ps)')
    ax.set_ylabel('t₂ (ps)')
    ax.set_title('Slowest timescale t₂')
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.semilogx(results['lag_ps'], results['t3'], 'r-o', ms=4, label='t₃')
    ax.axhline(70, color='k', ls='--', alpha=0.5, label='Paper ref (70 ps)')
    ax.set_xlabel('Lag time (ps)')
    ax.set_ylabel('t₃ (ps)')
    ax.set_title('Second timescale t₃')
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.semilogx(results['lag_ps'], results['pi_right'], 'g-o', ms=4)
    ax.axhline(0.375, color='k', ls='--', alpha=0.5, label='Paper ref (~0.375)')
    ax.set_xlabel('Lag time (ps)')
    ax.set_ylabel('π(φ≥0)')
    ax.set_title('Stationary prob. right-half')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out = results_dir / "long_reference_timescales.png"
    fig.savefig(out, dpi=150)
    print(f"\nSaved plot: {out}")
    plt.close()

    # Save results
    np.savez(results_dir / "long_reference_results.npz", **results)
    print(f"Saved data: {results_dir / 'long_reference_results.npz'}")

    return results, t2_ref, t3_ref, pi_right_ref


if __name__ == "__main__":
    main()
