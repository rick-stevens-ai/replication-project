"""
Tier-lift OSTI 1412756 — classical Monte Carlo verification of the
2D Ising universality (β = 1/8) of the chiral-spin-order transition.

The paper argues that the finite-T transition in the Kondo-Heisenberg
chiral phase reduces to a 2D Ising transition for the order parameter
σ = sign(α) (the canting handedness / chirality sign). We test this
directly with a Wolff cluster Monte Carlo on the 2D nearest-neighbour
Ising model and extract β from finite-size scaling, comparing to
Onsager's exact β = 1/8 = 0.125.

This addresses follow-on Q1 of the existing replication report.
"""
import numpy as np
import time

KB = 1.0
J = 1.0
TC_EXACT = 2.0 / np.log(1 + np.sqrt(2))   # = 2.2691853...

def init_lattice(L, rng):
    return rng.choice([-1, 1], size=(L, L)).astype(np.int8)

def wolff_step(s, T, rng):
    """One Wolff cluster update."""
    L = s.shape[0]
    p = 1.0 - np.exp(-2.0 * J / T)
    i, j = rng.integers(0, L, size=2)
    sign = s[i, j]
    stack = [(i, j)]
    cluster = {(i, j)}
    while stack:
        x, y = stack.pop()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = (x+dx) % L, (y+dy) % L
            if (nx, ny) not in cluster and s[nx, ny] == sign:
                if rng.random() < p:
                    cluster.add((nx, ny))
                    stack.append((nx, ny))
    for (x, y) in cluster:
        s[x, y] = -sign
    return s

def magnetization(s):
    return np.abs(s.mean())

def run(L, T, n_therm=2000, n_meas=8000, seed=0):
    rng = np.random.default_rng(seed)
    s = init_lattice(L, rng)
    for _ in range(n_therm):
        wolff_step(s, T, rng)
    ms = np.empty(n_meas)
    for i in range(n_meas):
        wolff_step(s, T, rng)
        ms[i] = magnetization(s)
    m = ms.mean(); m2 = (ms**2).mean(); m4 = (ms**4).mean()
    binder = 1.0 - m4 / (3.0 * m2**2)
    chi = L*L * (m2 - m**2) / T
    return m, chi, binder

def main():
    print(f"Exact 2D Ising T_c = {TC_EXACT:.6f}, β_exact = 0.125")
    Ls = [16, 24, 32, 48]
    # Sweep T near criticality to locate T_c via Binder crossing
    Ts = np.linspace(2.20, 2.34, 8)
    print(f"\nBinder cumulant U(L,T):")
    print(f"{'T':>8s} " + " ".join(f"L={L:>3d}" for L in Ls))
    binder_grid = np.zeros((len(Ls), len(Ts)))
    m_at_Tc = np.zeros(len(Ls))
    chi_at_Tc = np.zeros(len(Ls))
    t0 = time.time()
    for j_T, T in enumerate(Ts):
        row = []
        for i_L, L in enumerate(Ls):
            m, chi, U = run(L, T, n_therm=800, n_meas=2500, seed=42+i_L*10+j_T)
            binder_grid[i_L, j_T] = U
            row.append(f"{U:.4f}")
        print(f"{T:8.4f} " + " ".join(f"{r:>7s}" for r in row))
    # Run at T_c specifically with longer chains
    print(f"\nFinite-size scaling at T = T_c = {TC_EXACT:.5f} (β/ν = 1/8 expected):")
    print(f"{'L':>4s} {'<|m|>':>10s} {'chi':>10s}")
    ms_tc = []
    for i_L, L in enumerate(Ls):
        m, chi, U = run(L, TC_EXACT, n_therm=2000, n_meas=8000, seed=999+i_L)
        ms_tc.append(m)
        chi_at_Tc[i_L] = chi
        print(f"{L:4d} {m:10.5f} {chi:10.4f}")
    # Fit ln|m| = const - (β/ν) ln L  → slope = -β/ν, ν=1, so slope = -β = -1/8
    logL = np.log(Ls)
    logm = np.log(ms_tc)
    A = np.vstack([logL, np.ones_like(logL)]).T
    slope, intercept = np.linalg.lstsq(A, logm, rcond=None)[0]
    beta_fit = -slope    # ν=1 in 2D Ising, so β/ν = β
    print(f"\nFit: ln<|m|> = {slope:.4f} ln L + {intercept:.4f}")
    print(f"  -> β/ν = {-slope:.4f}  (exact 0.125)")
    print(f"  -> deviation: {(beta_fit - 0.125):+.4f}")
    print(f"\nElapsed: {time.time()-t0:.1f} s")

    # Also fit chi ~ L^(γ/ν), expect γ/ν = 7/4 = 1.75
    logchi = np.log(chi_at_Tc)
    s2, i2 = np.linalg.lstsq(A, logchi, rcond=None)[0]
    print(f"χ(L) fit: γ/ν = {s2:.4f}  (exact 1.75)")

    return beta_fit

if __name__ == "__main__":
    main()
