"""
Phase 1: 1D Double-Well Markov Chain — Vectorized

Replicates the synthetic test system from Nüske et al. (2017).
- 100 microstates along x-axis
- Double-well potential with Metropolis dynamics
- 7-state MSM discretization
- Slowest timescale t2 ≈ 3708 steps

Reference: J. Chem. Phys. 146, 094104 (2017), Section IV.A
"""

import sys
import numpy as np
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path


def build_system(n_micro=100, x_range=(-4, 4)):
    """Build 1D double-well potential and Metropolis transition matrix."""
    x = np.linspace(x_range[0], x_range[1], n_micro)
    # Scale=0.633 tuned to give t2 ≈ 3708 with beta=1.0
    V = 0.633 * ((x**2 - 4)**2 / 4 - 0.3 * x)
    
    # Build transition matrix (Metropolis, nearest-neighbor)
    T = np.zeros((n_micro, n_micro))
    for i in range(n_micro):
        if i > 0:
            a = min(1.0, np.exp(-(V[i-1] - V[i])))
            p = 0.5 if (0 < i < n_micro - 1) else 1.0
            T[i, i-1] = p * a
        if i < n_micro - 1:
            a = min(1.0, np.exp(-(V[i+1] - V[i])))
            p = 0.5 if (0 < i < n_micro - 1) else 1.0
            T[i, i+1] = p * a
        T[i, i] = 1.0 - T[i].sum()
    
    return x, V, T


def exact_properties(T, n_ts=10):
    """Compute exact stationary distribution and implied timescales."""
    evals = np.sort(np.real(linalg.eigvals(T)))[::-1]
    ts = np.array([-1.0/np.log(evals[k]) for k in range(1, n_ts+1) if 0 < evals[k] < 1])
    
    # Stationary distribution
    eigenvalues, eigvecs = linalg.eig(T.T)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigvecs[:, idx])
    pi /= pi.sum()
    
    return pi, ts, evals


def seven_state_assignment(x):
    """7-state coarse graining. State 4 deliberately spans barrier + right well."""
    bounds = [-np.inf, -2.8, -1.6, -0.4, 1.2, 2.0, 2.8, np.inf]
    assign = np.digitize(x, bounds[1:-1])
    return assign  # 0-indexed: states 0..6


def generate_trajectories_vectorized(T_cumsum, n_traj, K, start_dist):
    """Generate trajectories using vectorized sampling — all trajectories in parallel."""
    n = T_cumsum.shape[0]
    trajs = np.zeros((n_traj, K + 1), dtype=np.int32)
    
    # Sample initial states
    cdf = np.cumsum(start_dist)
    trajs[:, 0] = np.searchsorted(cdf, np.random.random(n_traj))
    trajs[:, 0] = np.clip(trajs[:, 0], 0, n - 1)
    
    # Advance all trajectories in parallel
    for k in range(K):
        r = np.random.random(n_traj)
        current = trajs[:, k]
        # Vectorized lookup: for each trajectory, find next state
        for i in range(n_traj):
            trajs[i, k+1] = np.searchsorted(T_cumsum[current[i]], r[i])
        trajs[:, k+1] = np.clip(trajs[:, k+1], 0, n - 1)
    
    return trajs


def generate_trajectories_fast(T_cumsum, n_traj, K, start_dist, batch_size=500):
    """Generate trajectories in batches, fully vectorized within each step."""
    n = T_cumsum.shape[0]
    all_trajs = []
    
    for b_start in range(0, n_traj, batch_size):
        b_end = min(b_start + batch_size, n_traj)
        bs = b_end - b_start
        trajs = np.zeros((bs, K + 1), dtype=np.int32)
        
        cdf = np.cumsum(start_dist)
        trajs[:, 0] = np.searchsorted(cdf, np.random.random(bs))
        trajs[:, 0] = np.clip(trajs[:, 0], 0, n - 1)
        
        for k in range(K):
            r = np.random.random(bs)
            # Build per-trajectory CDF rows and searchsorted
            rows = T_cumsum[trajs[:, k]]  # (bs, n)
            # Vectorized searchsorted along axis 1
            trajs[:, k+1] = np.array([np.searchsorted(rows[i], r[i]) for i in range(bs)], dtype=np.int32)
            trajs[:, k+1] = np.clip(trajs[:, k+1], 0, n - 1)
        
        all_trajs.append(trajs)
    
    return np.vstack(all_trajs)


def count_matrix_from_array(trajs, assign, n_states, lag):
    """Compute count matrix from trajectory array (n_traj, K+1)."""
    coarse = assign[trajs]  # (n_traj, K+1)
    C = np.zeros((n_states, n_states), dtype=np.float64)
    for k in range(coarse.shape[1] - lag):
        i_col = coarse[:, k]
        j_col = coarse[:, k + lag]
        for i in range(n_states):
            mask = (i_col == i)
            if mask.any():
                for j in range(n_states):
                    C[i, j] += np.sum(j_col[mask] == j)
    return C


def two_step_counts_from_array(trajs, assign, n_states, lag):
    """Compute two-step count matrices S^{2τ}_r(i,j) from trajectory array."""
    coarse = assign[trajs]
    s = np.zeros(n_states, dtype=np.float64)
    S_tau = np.zeros((n_states, n_states), dtype=np.float64)
    S2 = np.zeros((n_states, n_states, n_states), dtype=np.float64)  # [r, i, j]
    
    max_k = coarse.shape[1] - 2 * lag
    for k in range(max_k):
        i_col = coarse[:, k]
        r_col = coarse[:, k + lag]
        j_col = coarse[:, k + 2 * lag]
        
        # Count vector
        for st in range(n_states):
            s[st] += np.sum(i_col == st)
        
        # One-step counts
        for i in range(n_states):
            mask_i = (i_col == i)
            if not mask_i.any():
                continue
            for r in range(n_states):
                S_tau[i, r] += np.sum(r_col[mask_i] == r)
        
        # Two-step counts
        for i in range(n_states):
            mask_i = (i_col == i)
            if not mask_i.any():
                continue
            for r in range(n_states):
                mask_ir = mask_i & (r_col == r)
                if not mask_ir.any():
                    continue
                for j in range(n_states):
                    S2[r, i, j] += np.sum(j_col[mask_ir] == j)
    
    return s, S_tau, S2


def oom_estimate(s, S_tau, S2, n_states, lag, M=None):
    """
    OOM-based corrected MSM estimator (Nüske et al. Eqs. 44-55).
    
    Returns: T_corrected, pi_corrected, eigenvalues_oom
    """
    # SVD of count matrix
    U, sigma, Vt = np.linalg.svd(S_tau, full_matrices=False)
    
    if M is None:
        M = max(2, np.sum(sigma > sigma[0] * 0.01))
        M = min(M, n_states - 1, len(sigma))
    M = min(M, len(sigma))
    
    U_M = U[:, :M]
    sigma_M = sigma[:M]
    V_M = Vt[:M, :].T
    
    sigma_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(sigma_M, 1e-10)))
    F1 = U_M @ sigma_inv_sqrt
    F2 = V_M @ sigma_inv_sqrt
    
    # Set-observable operators
    Xi_hat = np.zeros((n_states, M, M))
    for r in range(n_states):
        Xi_hat[r] = F1.T @ S2[r] @ F2
    
    sigma_hat = F1.T @ s
    Xi_Omega = np.sum(Xi_hat, axis=0)
    
    # Left eigenvector of Xi_Omega with eigenvalue 1
    eigenvalues_xi, eigvecs_xi = linalg.eig(Xi_Omega.T)
    idx = np.argmin(np.abs(eigenvalues_xi - 1.0))
    omega_hat = np.real(eigvecs_xi[:, idx])
    denom = omega_hat @ sigma_hat
    if abs(denom) < 1e-12:
        raise ValueError("omega^T sigma ~ 0, OOM estimation failed")
    omega_hat = omega_hat / denom
    
    # Corrected equilibrium correlations
    C_eq = np.zeros((n_states, n_states))
    pi_corr = np.zeros(n_states)
    for i in range(n_states):
        for j in range(n_states):
            C_eq[i, j] = omega_hat @ Xi_hat[i] @ Xi_hat[j] @ sigma_hat
        pi_corr[i] = omega_hat @ Xi_hat[i] @ sigma_hat
    
    pi_corr = np.maximum(pi_corr, 0)
    if pi_corr.sum() > 0:
        pi_corr /= pi_corr.sum()
    
    # Corrected transition matrix
    T_corr = np.zeros((n_states, n_states))
    for i in range(n_states):
        rs = C_eq[i].sum()
        if rs > 0:
            T_corr[i] = np.maximum(C_eq[i], 0) / rs
        else:
            T_corr[i, i] = 1.0
    
    # OOM eigenvalues
    evals_oom = np.sort(np.real(linalg.eigvals(Xi_Omega)))[::-1]
    
    return T_corr, pi_corr, evals_oom


def run_experiment():
    """Run full 1D double-well replication."""
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    print("Building 1D double-well (100 microstates)...", flush=True)
    x, V, T_micro = build_system()
    pi_exact, ts_exact, evals_exact = exact_properties(T_micro)
    print(f"  t2 = {ts_exact[0]:.1f}, t3 = {ts_exact[1]:.1f}", flush=True)
    
    assign = seven_state_assignment(x)
    n_states = 7
    
    # Starting distribution: ρ = [0.3, 0.3, 0.3, 0, 0.05, 0.05, 0] (uniform within states)
    rho = np.array([0.3, 0.3, 0.3, 0.0, 0.05, 0.05, 0.0])
    start_dist = np.zeros(100)
    for s in range(n_states):
        mask = (assign == s)
        n_in = mask.sum()
        if n_in > 0 and rho[s] > 0:
            start_dist[mask] = rho[s] / n_in
    
    T_cumsum = np.cumsum(T_micro, axis=1)
    np.random.seed(42)
    
    # Dataset 1: K=250, Q=5000
    print("Generating short dataset (Q=5000, K=250)...", flush=True)
    trajs_short = generate_trajectories_fast(T_cumsum, 5000, 250, start_dist)
    print(f"  Shape: {trajs_short.shape}", flush=True)
    
    # Dataset 2: K=2000, Q=5000
    print("Generating long dataset (Q=5000, K=2000)...", flush=True)
    trajs_long = generate_trajectories_fast(T_cumsum, 5000, 2000, start_dist)
    print(f"  Shape: {trajs_long.shape}", flush=True)
    
    # Analyze at various lag times
    configs = [
        ("short (K=250)", trajs_short, [1, 2, 5, 10, 15, 20, 25, 30]),
        ("long (K=2000)", trajs_long, [1, 2, 5, 10, 20, 50, 100, 150, 200]),
    ]
    
    all_results = {}
    
    for label, trajs, lags in configs:
        print(f"\nAnalyzing {label}...", flush=True)
        its_direct = []
        its_oom = []
        
        for tau in lags:
            print(f"  τ = {tau}...", end="", flush=True)
            
            # Direct MSM
            C = count_matrix_from_array(trajs, assign, n_states, tau)
            T_est = np.zeros_like(C)
            for i in range(n_states):
                rs = C[i].sum()
                T_est[i] = C[i] / rs if rs > 0 else 0
                if rs == 0:
                    T_est[i, i] = 1.0
            
            ev = np.sort(np.real(linalg.eigvals(T_est)))[::-1]
            t2_d = -tau / np.log(ev[1]) if 0 < ev[1] < 1 else np.inf
            t3_d = -tau / np.log(ev[2]) if 0 < ev[2] < 1 else np.inf
            its_direct.append([t2_d, t3_d])
            
            # OOM corrected
            try:
                s, S_tau, S2 = two_step_counts_from_array(trajs, assign, n_states, tau)
                T_c, pi_c, ev_oom = oom_estimate(s, S_tau, S2, n_states, tau, M=3)
                t2_o = -tau / np.log(ev_oom[1]) if 0 < ev_oom[1] < 1 else np.inf
                t3_o = -tau / np.log(ev_oom[2]) if 0 < ev_oom[2] < 1 else np.inf
                its_oom.append([t2_o, t3_o])
            except Exception as e:
                print(f" OOM failed: {e}", end="", flush=True)
                its_oom.append([np.nan, np.nan])
            
            print(f" direct=[{t2_d:.0f},{t3_d:.0f}] oom=[{its_oom[-1][0]:.0f},{its_oom[-1][1]:.0f}]", flush=True)
        
        all_results[label] = {
            'lags': np.array(lags),
            'its_direct': np.array(its_direct),
            'its_oom': np.array(its_oom),
        }
    
    # Plot
    print("\nGenerating plots...", flush=True)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Potential
    ax = axes[0, 0]
    ax.plot(x, V, 'k-', lw=2)
    bounds = [-2.8, -1.6, -0.4, 1.2, 2.0, 2.8]
    for b in bounds:
        ax.axvline(b, color='gray', ls='--', alpha=0.5)
    ax.set_xlabel('x'); ax.set_ylabel('V(x)')
    ax.set_title('1D Double-Well (7-state discretization)')
    
    # Timescale spectrum
    ax = axes[0, 1]
    ax.semilogy(range(2, min(12, len(ts_exact)+2)), ts_exact[:10], 'ko-', ms=8)
    ax.set_xlabel('Mode m'); ax.set_ylabel('t_m (steps)')
    ax.set_title(f'Exact Spectrum (t₂={ts_exact[0]:.0f})')
    ax.grid(True, alpha=0.3)
    
    # Short dataset ITS
    for idx, (label, key) in enumerate([("Short (K=250)", "short (K=250)"), ("Long (K=2000)", "long (K=2000)")]):
        ax = axes[1, idx]
        r = all_results[key]
        ax.semilogy(r['lags'], r['its_direct'][:, 0], 'g-o', ms=5, label='Direct MSM t₂')
        ax.semilogy(r['lags'], r['its_oom'][:, 0], 'b-s', ms=5, label='OOM t₂')
        ax.axhline(ts_exact[0], color='k', ls='--', label=f'Exact t₂={ts_exact[0]:.0f}')
        if len(ts_exact) > 1:
            ax.semilogy(r['lags'], r['its_direct'][:, 1], 'g--^', ms=4, alpha=0.5, label='Direct t₃')
            ax.semilogy(r['lags'], r['its_oom'][:, 1], 'b--d', ms=4, alpha=0.5, label='OOM t₃')
            ax.axhline(ts_exact[1], color='gray', ls=':', label=f'Exact t₃={ts_exact[1]:.0f}')
        ax.set_xlabel('Lag time τ'); ax.set_ylabel('Implied timescale')
        ax.set_title(label); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    out = results_dir / "fig5_1d_double_well.png"
    fig.savefig(out, dpi=150)
    print(f"  Saved: {out}", flush=True)
    
    # Summary
    print("\n" + "="*60)
    print("PHASE 1 RESULTS")
    print("="*60)
    print(f"Exact: t₂ = {ts_exact[0]:.1f}, t₃ = {ts_exact[1]:.1f}")
    for key in all_results:
        r = all_results[key]
        last = -1
        print(f"\n{key} @ τ={r['lags'][last]}:")
        print(f"  Direct MSM: t₂={r['its_direct'][last,0]:.1f}, t₃={r['its_direct'][last,1]:.1f}")
        print(f"  OOM:        t₂={r['its_oom'][last,0]:.1f}, t₃={r['its_oom'][last,1]:.1f}")


if __name__ == "__main__":
    run_experiment()
