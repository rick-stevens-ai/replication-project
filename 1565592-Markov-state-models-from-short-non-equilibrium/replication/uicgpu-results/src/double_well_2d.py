"""
Phase 2: 2D Potential Energy Landscape — Stress Test

Replicates Section IV.C of Nüske et al. (2017).
- 40×40 = 1600 microstates on 2D grid
- Metropolis dynamics (x and y moves)
- 16 MSM states (4×4 regular grid, deliberately poor)
- t2 ≈ 144,000 steps, t3 ≈ 17,000 steps
- K=5000, Q=2000 and Q=10,000
- Starting from uniform distribution over all microstates

Reference: J. Chem. Phys. 146, 094104 (2017), Section IV.C, Fig 7
"""

import sys
import numpy as np
from scipy import linalg
from scipy.sparse import lil_matrix, csr_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Import OOM estimator from phase 1
sys.path.insert(0, str(Path(__file__).parent))
from double_well_1d import oom_estimate


def build_2d_potential(nx=40, ny=40):
    """
    Build 2D energy landscape with multiple metastable states.
    
    The paper shows (Fig 7a) a landscape with:
    - Multiple minima creating at least 3 metastable regions
    - t2 ≈ 144,000 and t3 ≈ 17,000 steps
    - Coordinates x,y ∈ [0, 4+]
    
    We use a three-well potential in 2D, tuned to match timescales.
    """
    x = np.linspace(0, 4, nx)
    y = np.linspace(0, 4, ny)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    # Three-well potential:
    # Well 1: (1, 1), Well 2: (3, 1), Well 3: (2, 3)
    # With barriers between them of different heights
    V = np.zeros_like(X)
    
    # Base: quadratic confinement
    V += 0.3 * ((X - 2)**2 + (Y - 2)**2)
    
    # Three Gaussian wells
    V -= 4.0 * np.exp(-1.5 * ((X - 0.8)**2 + (Y - 0.8)**2))  # deep well bottom-left
    V -= 3.5 * np.exp(-1.5 * ((X - 3.2)**2 + (Y - 0.8)**2))  # medium well bottom-right  
    V -= 3.0 * np.exp(-1.2 * ((X - 2.0)**2 + (Y - 3.0)**2))  # shallow well top-center
    
    # Additional barrier ridge
    V += 1.5 * np.exp(-3.0 * (X - 2.0)**2)  # vertical barrier at x=2
    
    return x, y, X, Y, V


def build_2d_transition_matrix(V, nx, ny, beta=1.0):
    """
    Build transition matrix for 2D Metropolis dynamics on grid.
    Moves to 4 nearest neighbors (up/down/left/right).
    """
    n = nx * ny
    T = lil_matrix((n, n))
    
    def idx(ix, iy):
        return ix * ny + iy
    
    for ix in range(nx):
        for iy in range(ny):
            i = idx(ix, iy)
            neighbors = []
            if ix > 0: neighbors.append(idx(ix-1, iy))
            if ix < nx-1: neighbors.append(idx(ix+1, iy))
            if iy > 0: neighbors.append(idx(ix, iy-1))
            if iy < ny-1: neighbors.append(idx(ix, iy+1))
            
            n_neigh = len(neighbors)
            proposal_prob = 1.0 / n_neigh if n_neigh > 0 else 0
            
            total_out = 0.0
            for j in neighbors:
                jx, jy = j // ny, j % ny
                dV = V[jx, jy] - V[ix, iy]
                accept = min(1.0, np.exp(-beta * dV))
                rate = proposal_prob * accept
                T[i, j] = rate
                total_out += rate
            
            T[i, i] = 1.0 - total_out
    
    return T.tocsr()


def sparse_exact_properties(T_sparse, n_evals=5):
    """Compute leading eigenvalues/timescales from sparse transition matrix."""
    from scipy.sparse.linalg import eigs
    
    # Get leading eigenvalues (closest to 1)
    eigenvalues, eigvecs = eigs(T_sparse.T, k=n_evals, which='LR')
    eigenvalues = np.real(eigenvalues)
    order = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[order]
    
    timescales = []
    for k in range(1, len(eigenvalues)):
        if 0 < eigenvalues[k] < 1:
            timescales.append(-1.0 / np.log(eigenvalues[k]))
        else:
            timescales.append(np.inf)
    
    # Stationary distribution
    idx = np.argmax(eigenvalues)
    pi = np.real(eigvecs[:, order[0]])
    pi = np.abs(pi)
    pi /= pi.sum()
    
    return pi, np.array(timescales), eigenvalues


def assign_16_states(nx=40, ny=40):
    """
    16-state discretization: regular 4×4 grid over the 2D domain.
    States 13, 14, 15 blend different metastable regions (poor discretization).
    """
    n = nx * ny
    assign = np.zeros(n, dtype=int)
    
    for ix in range(nx):
        for iy in range(ny):
            # 4×4 grid: each block is 10×10 microstates
            bx = min(ix // 10, 3)
            by = min(iy // 10, 3)
            state = bx * 4 + by
            assign[ix * ny + iy] = state
    
    return assign


def generate_trajs_sparse(T_sparse, n_traj, K, start_dist, batch=1000):
    """Generate trajectories from sparse transition matrix."""
    n = T_sparse.shape[0]
    T_dense_rows = {}  # cache CDF rows as needed
    
    all_trajs = []
    for b_start in range(0, n_traj, batch):
        b_end = min(b_start + batch, n_traj)
        bs = b_end - b_start
        trajs = np.zeros((bs, K + 1), dtype=np.int32)
        
        # Initial states
        cdf = np.cumsum(start_dist)
        trajs[:, 0] = np.searchsorted(cdf, np.random.random(bs))
        trajs[:, 0] = np.clip(trajs[:, 0], 0, n - 1)
        
        for k in range(K):
            r = np.random.random(bs)
            for t in range(bs):
                state = trajs[t, k]
                if state not in T_dense_rows:
                    row = T_sparse[state].toarray().flatten()
                    T_dense_rows[state] = np.cumsum(row)
                trajs[t, k+1] = np.searchsorted(T_dense_rows[state], r[t])
                trajs[t, k+1] = min(trajs[t, k+1], n - 1)
        
        all_trajs.append(trajs)
        if (b_start + batch) % 2000 == 0:
            print(f"    {b_start + batch}/{n_traj} trajectories...", flush=True)
    
    return np.vstack(all_trajs)


def count_stats(trajs, assign, n_states, lag):
    """Compute s, S_tau, S2_tau for OOM estimator."""
    coarse = assign[trajs]
    n_traj, L = coarse.shape
    
    s = np.zeros(n_states)
    S_tau = np.zeros((n_states, n_states))
    S2 = np.zeros((n_states, n_states, n_states))
    
    max_k = L - 2 * lag
    if max_k <= 0:
        raise ValueError(f"Trajectories too short for lag={lag} (need >{2*lag} steps)")
    
    for k in range(max_k):
        i_col = coarse[:, k]
        r_col = coarse[:, k + lag]
        j_col = coarse[:, k + 2 * lag]
        
        for st in range(n_states):
            s[st] += np.sum(i_col == st)
        
        for i in range(n_states):
            mask_i = (i_col == i)
            if not mask_i.any():
                continue
            for r in range(n_states):
                count_ir = np.sum(r_col[mask_i] == r)
                S_tau[i, r] += count_ir
                if count_ir == 0:
                    continue
                mask_ir = mask_i & (r_col == r)
                for j in range(n_states):
                    S2[r, i, j] += np.sum(j_col[mask_ir] == j)
    
    return s, S_tau, S2


def tune_beta(nx=40, ny=40, target_t2=144000, target_t3=17000):
    """Find beta that gives desired timescales."""
    print("Tuning 2D potential beta...", flush=True)
    
    x, y, X, Y, V = build_2d_potential(nx, ny)
    
    for beta in [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0]:
        T = build_2d_transition_matrix(V, nx, ny, beta)
        pi, ts, evals = sparse_exact_properties(T, n_evals=5)
        print(f"  beta={beta:.1f}: t2={ts[0]:.0f}, t3={ts[1]:.0f}", flush=True)
        if ts[0] > target_t2 * 0.8:
            break
    
    return beta


def run_experiment():
    """Run full 2D potential experiment."""
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    nx, ny = 40, 40
    n_micro = nx * ny
    
    # Build and tune system
    print("Building 2D system (40×40 = 1600 microstates)...", flush=True)
    x, y, X, Y, V = build_2d_potential(nx, ny)
    
    # Try a range of betas
    best_beta = None
    best_diff = float('inf')
    
    for beta in np.arange(2.0, 12.0, 0.5):
        T = build_2d_transition_matrix(V, nx, ny, beta)
        pi, ts, evals = sparse_exact_properties(T, n_evals=5)
        diff = abs(ts[0] - 144000) + abs(ts[1] - 17000) * 5
        if diff < best_diff:
            best_diff = diff
            best_beta = beta
            best_ts = ts.copy()
        print(f"  beta={beta:.1f}: t2={ts[0]:.0f}, t3={ts[1]:.0f}", flush=True)
    
    print(f"\nBest beta = {best_beta:.1f}: t2={best_ts[0]:.0f}, t3={best_ts[1]:.0f}", flush=True)
    
    T_sparse = build_2d_transition_matrix(V, nx, ny, best_beta)
    pi_exact, ts_exact, evals_exact = sparse_exact_properties(T_sparse, n_evals=5)
    
    assign = assign_16_states(nx, ny)
    n_states = 16
    
    # Uniform starting distribution
    start_dist = np.ones(n_micro) / n_micro
    
    np.random.seed(42)
    K = 5000
    
    configs = [
        ("Q=2000", 2000),
        ("Q=10000", 10000),
    ]
    
    all_results = {}
    lags = [10, 20, 50, 100, 200, 500, 1000]
    
    for label, Q in configs:
        print(f"\nGenerating trajectories ({label}, K={K})...", flush=True)
        trajs = generate_trajs_sparse(T_sparse, Q, K, start_dist)
        print(f"  Shape: {trajs.shape}", flush=True)
        
        its_direct = []
        its_oom = []
        
        for tau in lags:
            if 2 * tau >= K:
                its_direct.append([np.nan, np.nan])
                its_oom.append([np.nan, np.nan])
                continue
            
            print(f"  τ = {tau}...", end="", flush=True)
            
            # Direct MSM
            s, S_tau, S2 = count_stats(trajs, assign, n_states, tau)
            T_est = np.zeros((n_states, n_states))
            for i in range(n_states):
                rs = S_tau[i].sum()
                T_est[i] = S_tau[i] / rs if rs > 0 else 0
                if rs == 0: T_est[i, i] = 1.0
            
            ev = np.sort(np.real(linalg.eigvals(T_est)))[::-1]
            t2_d = -tau / np.log(ev[1]) if 0 < ev[1] < 1 else np.inf
            t3_d = -tau / np.log(ev[2]) if 0 < ev[2] < 1 else np.inf
            its_direct.append([t2_d, t3_d])
            
            # OOM
            try:
                T_c, pi_c, ev_oom = oom_estimate(s, S_tau, S2, n_states, tau, M=4)
                t2_o = -tau / np.log(ev_oom[1]) if 0 < ev_oom[1] < 1 else np.inf
                t3_o = -tau / np.log(ev_oom[2]) if 0 < ev_oom[2] < 1 else np.inf
                its_oom.append([t2_o, t3_o])
            except Exception as e:
                print(f" OOM fail: {e}", end="", flush=True)
                its_oom.append([np.nan, np.nan])
            
            print(f" d=[{t2_d:.0f},{t3_d:.0f}] o=[{its_oom[-1][0]:.0f},{its_oom[-1][1]:.0f}]", flush=True)
        
        all_results[label] = {
            'lags': np.array(lags),
            'its_direct': np.array(its_direct),
            'its_oom': np.array(its_oom),
        }
    
    # Plot
    print("\nPlotting...", flush=True)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # 2D potential
    ax = axes[0, 0]
    im = ax.pcolormesh(X, Y, V, cmap='viridis', shading='auto')
    plt.colorbar(im, ax=ax)
    # Draw 4×4 grid
    for bx in range(1, 4):
        ax.axvline(x[bx * 10], color='w', ls='--', alpha=0.7)
    for by in range(1, 4):
        ax.axhline(y[by * 10], color='w', ls='--', alpha=0.7)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('2D Potential (16-state discretization)')
    
    # Timescale spectrum
    ax = axes[0, 1]
    ax.semilogy(range(2, len(ts_exact)+2), ts_exact, 'ko-', ms=8)
    ax.set_xlabel('Mode m'); ax.set_ylabel('t_m')
    ax.set_title(f'Exact Spectrum (t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f})')
    ax.grid(True, alpha=0.3)
    
    # Stationary distribution
    ax = axes[0, 2]
    pi_states = np.zeros(n_states)
    for s in range(n_states):
        pi_states[s] = pi_exact[assign == s].sum()
    ax.bar(range(n_states), pi_states)
    ax.set_xlabel('State'); ax.set_ylabel('π')
    ax.set_title('Exact Stationary Distribution')
    
    # ITS plots for both Q values
    for idx, label in enumerate(["Q=2000", "Q=10000"]):
        r = all_results[label]
        
        ax = axes[1, idx]
        valid = ~np.isnan(r['its_direct'][:, 0])
        ax.semilogy(r['lags'][valid], r['its_direct'][valid, 0], 'g-o', ms=5, label='Direct t₂')
        valid_o = ~np.isnan(r['its_oom'][:, 0])
        ax.semilogy(r['lags'][valid_o], r['its_oom'][valid_o, 0], 'b-s', ms=5, label='OOM t₂')
        ax.axhline(ts_exact[0], color='k', ls='--', label=f'Exact t₂={ts_exact[0]:.0f}')
        
        valid3 = ~np.isnan(r['its_direct'][:, 1])
        ax.semilogy(r['lags'][valid3], r['its_direct'][valid3, 1], 'g--^', ms=4, alpha=0.5, label='Direct t₃')
        valid3_o = ~np.isnan(r['its_oom'][:, 1])
        ax.semilogy(r['lags'][valid3_o], r['its_oom'][valid3_o, 1], 'b--d', ms=4, alpha=0.5, label='OOM t₃')
        ax.axhline(ts_exact[1], color='gray', ls=':', label=f'Exact t₃={ts_exact[1]:.0f}')
        
        ax.set_xlabel('Lag time τ'); ax.set_ylabel('Implied timescale')
        ax.set_title(label); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    
    # Summary text
    ax = axes[1, 2]
    ax.axis('off')
    summary = f"PHASE 2 SUMMARY\n\nExact: t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f}\n"
    for label in all_results:
        r = all_results[label]
        last = -1
        while np.isnan(r['its_direct'][last, 0]) and abs(last) < len(r['lags']):
            last -= 1
        summary += f"\n{label} @ τ={r['lags'][last]}:\n"
        summary += f"  Direct: t₂={r['its_direct'][last,0]:.0f}\n"
        summary += f"  OOM:    t₂={r['its_oom'][last,0]:.0f}\n"
    ax.text(0.1, 0.9, summary, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    out = results_dir / "fig7_2d_potential.png"
    fig.savefig(out, dpi=150)
    print(f"Saved: {out}", flush=True)
    
    print("\n" + "="*60)
    print("PHASE 2 RESULTS")
    print("="*60)
    print(f"Exact: t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f}")
    for label in all_results:
        r = all_results[label]
        last = -1
        while np.isnan(r['its_direct'][last, 0]) and abs(last) < len(r['lags']):
            last -= 1
        print(f"\n{label} @ τ={r['lags'][last]}:")
        print(f"  Direct: t₂={r['its_direct'][last,0]:.0f}, t₃={r['its_direct'][last,1]:.0f}")
        print(f"  OOM:    t₂={r['its_oom'][last,0]:.0f}, t₃={r['its_oom'][last,1]:.0f}")


if __name__ == "__main__":
    run_experiment()
