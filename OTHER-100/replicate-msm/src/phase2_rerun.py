"""
Phase 2 rerun with fast count computation.
Only runs Q=10,000 (Q=2000 already done).
"""

import sys
import numpy as np
from scipy import linalg
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

from fast_counts import count_stats_fast, direct_msm, oom_msm


def build_2d_system(nx=40, ny=40, beta=3.0):
    """Build 2D potential + sparse transition matrix."""
    x = np.linspace(0, 4, nx)
    y = np.linspace(0, 4, ny)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    V = np.zeros_like(X)
    V += 0.3 * ((X - 2)**2 + (Y - 2)**2)
    V -= 4.0 * np.exp(-1.5 * ((X - 0.8)**2 + (Y - 0.8)**2))
    V -= 3.5 * np.exp(-1.5 * ((X - 3.2)**2 + (Y - 0.8)**2))
    V -= 3.0 * np.exp(-1.2 * ((X - 2.0)**2 + (Y - 3.0)**2))
    V += 1.5 * np.exp(-3.0 * (X - 2.0)**2)
    
    n = nx * ny
    T = lil_matrix((n, n))
    
    for ix in range(nx):
        for iy in range(ny):
            i = ix * ny + iy
            neighbors = []
            if ix > 0: neighbors.append(((ix-1)*ny + iy, V[ix-1, iy]))
            if ix < nx-1: neighbors.append(((ix+1)*ny + iy, V[ix+1, iy]))
            if iy > 0: neighbors.append((ix*ny + iy-1, V[ix, iy-1]))
            if iy < ny-1: neighbors.append((ix*ny + iy+1, V[ix, iy+1]))
            
            pp = 1.0 / len(neighbors)
            total = 0.0
            for j, vj in neighbors:
                a = min(1.0, np.exp(-beta * (vj - V[ix, iy])))
                T[i, j] = pp * a
                total += pp * a
            T[i, i] = 1.0 - total
    
    T_csr = T.tocsr()
    
    # Exact properties
    eigenvalues, _ = eigs(T_csr.T, k=5, which='LR')
    eigenvalues = np.sort(np.real(eigenvalues))[::-1]
    ts_exact = [-1.0/np.log(eigenvalues[k]) for k in range(1, len(eigenvalues)) if 0 < eigenvalues[k] < 1]
    
    return x, y, X, Y, V, T_csr, np.array(ts_exact), eigenvalues


def assign_16(nx=40, ny=40):
    n = nx * ny
    assign = np.zeros(n, dtype=int)
    for ix in range(nx):
        for iy in range(ny):
            bx = min(ix // 10, 3)
            by = min(iy // 10, 3)
            assign[ix * ny + iy] = bx * 4 + by
    return assign


def gen_trajs(T_csr, n_traj, K, start_dist, batch=2000):
    """Generate trajectories from sparse T, in batches."""
    n = T_csr.shape[0]
    # Cache CDF rows
    cdf_cache = {}
    
    all_trajs = []
    for b in range(0, n_traj, batch):
        bs = min(batch, n_traj - b)
        trajs = np.zeros((bs, K + 1), dtype=np.int32)
        
        cdf_start = np.cumsum(start_dist)
        trajs[:, 0] = np.searchsorted(cdf_start, np.random.random(bs))
        trajs[:, 0] = np.clip(trajs[:, 0], 0, n - 1)
        
        for k in range(K):
            r = np.random.random(bs)
            for t in range(bs):
                st = trajs[t, k]
                if st not in cdf_cache:
                    row = T_csr[st].toarray().flatten()
                    cdf_cache[st] = np.cumsum(row)
                trajs[t, k+1] = np.searchsorted(cdf_cache[st], r[t])
                trajs[t, k+1] = min(trajs[t, k+1], n - 1)
        
        all_trajs.append(trajs)
        print(f"    {min(b + batch, n_traj)}/{n_traj}", flush=True)
    
    return np.vstack(all_trajs)


def main():
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    print("Phase 2 rerun: 2D potential", flush=True)
    print("Building system...", flush=True)
    x, y, X, Y, V, T_csr, ts_exact, evals_exact = build_2d_system()
    print(f"  Exact: t2={ts_exact[0]:.0f}, t3={ts_exact[1]:.0f}", flush=True)
    
    assign = assign_16()
    n_states = 16
    start_dist = np.ones(1600) / 1600
    K = 5000
    lags = [10, 20, 50, 100, 200, 500, 1000]
    
    np.random.seed(42)
    
    all_results = {}
    
    for Q_label, Q in [("Q=2000", 2000), ("Q=10000", 10000)]:
        print(f"\n{Q_label}: Generating {Q} trajectories (K={K})...", flush=True)
        trajs = gen_trajs(T_csr, Q, K, start_dist)
        print(f"  Shape: {trajs.shape}", flush=True)
        
        its_direct = []
        its_oom = []
        
        for tau in lags:
            if 2 * tau >= K:
                its_direct.append([np.nan, np.nan])
                its_oom.append([np.nan, np.nan])
                continue
            
            print(f"  τ={tau}...", end="", flush=True)
            
            s, S_tau, S2 = count_stats_fast(trajs, assign, n_states, tau)
            
            _, _, ts_d = direct_msm(S_tau, n_states, tau)
            its_direct.append([ts_d[0], ts_d[1] if len(ts_d) > 1 else np.nan])
            
            try:
                _, _, _, ts_o, _ = oom_msm(s, S_tau, S2, n_states, tau, M=4)
                its_oom.append([ts_o[0], ts_o[1] if len(ts_o) > 1 else np.nan])
            except Exception as e:
                print(f" OOM fail: {e}", end="", flush=True)
                its_oom.append([np.nan, np.nan])
            
            d = its_direct[-1]
            o = its_oom[-1]
            print(f" d=[{d[0]:.0f},{d[1]:.0f}] o=[{o[0]:.0f},{o[1]:.0f}]", flush=True)
        
        all_results[Q_label] = {
            'lags': np.array(lags),
            'its_direct': np.array(its_direct),
            'its_oom': np.array(its_oom),
        }
    
    # Plot
    print("\nPlotting...", flush=True)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    ax = axes[0, 0]
    im = ax.pcolormesh(X, Y, V, cmap='viridis', shading='auto')
    plt.colorbar(im, ax=ax)
    for bx in range(1, 4):
        ax.axvline(x[bx * 10], color='w', ls='--', alpha=0.7)
    for by in range(1, 4):
        ax.axhline(y[by * 10], color='w', ls='--', alpha=0.7)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('2D Potential (16-state)')
    
    ax = axes[0, 1]
    ax.semilogy(range(2, len(ts_exact)+2), ts_exact, 'ko-', ms=8)
    ax.set_xlabel('Mode m'); ax.set_ylabel('t_m')
    ax.set_title(f'Spectrum (t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f})')
    ax.grid(True, alpha=0.3)
    
    axes[0, 2].axis('off')
    
    for idx, qlabel in enumerate(["Q=2000", "Q=10000"]):
        r = all_results[qlabel]
        ax = axes[1, idx]
        v = ~np.isnan(r['its_direct'][:, 0])
        ax.semilogy(r['lags'][v], r['its_direct'][v, 0], 'g-o', ms=5, label='Direct t₂')
        vo = ~np.isnan(r['its_oom'][:, 0])
        ax.semilogy(r['lags'][vo], r['its_oom'][vo, 0], 'b-s', ms=5, label='OOM t₂')
        ax.axhline(ts_exact[0], color='k', ls='--', label=f'Exact t₂={ts_exact[0]:.0f}')
        ax.axhline(ts_exact[1], color='gray', ls=':', alpha=0.5, label=f'Exact t₃={ts_exact[1]:.0f}')
        ax.set_xlabel('Lag τ'); ax.set_ylabel('Implied timescale')
        ax.set_title(qlabel); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    
    # Summary panel
    ax = axes[1, 2]
    ax.axis('off')
    txt = f"PHASE 2 SUMMARY\n\nExact: t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f}\n"
    for qlabel in all_results:
        r = all_results[qlabel]
        last = -1
        while abs(last) < len(r['lags']) and np.isnan(r['its_direct'][last, 0]):
            last -= 1
        txt += f"\n{qlabel} @ τ={r['lags'][last]}:\n"
        txt += f"  Direct: t₂={r['its_direct'][last,0]:.0f}\n"
        txt += f"  OOM:    t₂={r['its_oom'][last,0]:.0f}\n"
    ax.text(0.1, 0.9, txt, transform=ax.transAxes, fontsize=11, va='top', family='monospace')
    
    plt.tight_layout()
    out = results_dir / "fig7_2d_potential.png"
    fig.savefig(out, dpi=150)
    print(f"Saved: {out}", flush=True)
    
    print("\n" + "="*60)
    print("PHASE 2 COMPLETE")
    print("="*60)
    for qlabel in all_results:
        r = all_results[qlabel]
        last = -1
        while abs(last) < len(r['lags']) and np.isnan(r['its_direct'][last, 0]):
            last -= 1
        print(f"\n{qlabel} @ τ={r['lags'][last]}:")
        print(f"  Direct: t₂={r['its_direct'][last,0]:.0f}, t₃={r['its_direct'][last,1]:.0f}")
        print(f"  OOM:    t₂={r['its_oom'][last,0]:.0f}, t₃={r['its_oom'][last,1]:.0f}")
        print(f"  Exact:  t₂={ts_exact[0]:.0f}, t₃={ts_exact[1]:.0f}")


if __name__ == "__main__":
    main()
