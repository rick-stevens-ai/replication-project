#!/usr/bin/env python3
"""
Extended MC — reproduces the paper's methodology class of computing a
temperature-dependent thermodynamic quantity by lattice-swap Metropolis on
the interstitial (H, N, Va) sublattice, then using thermodynamic integration
to get free energy F(T) - F(T_ref).

Method
------
1. Fix Lu skeleton, occupy 24 interstitial sites with (H, N, Va) at a chosen
   composition, use the paper's stated pair-energy Hamiltonian on the 4.5A
   cutoff graph. (Same surrogate as make_dataset.py — this is engineering
   validation of the MC pipeline; the paper's real MC calls its trained CGCNN
   as the energy oracle inside the same loop.)
2. Metropolis H<->N swaps at fixed composition. 20000 steps, first 5000 as
   equilibration.
3. Sweep T in log grid 200..2500 K, 8 temperatures.
4. Record <E>(T), C_v(T) = Var(E)/(k_B T^2).
5. Compute F(T) - F(T_ref) via thermodynamic integration:
       F(T)/T - F(T_ref)/T_ref = -integral(U/T^2 dT)   (from T_ref to T).
   This is the correct free-energy-from-energy method used by the paper.
6. Result: F(T) curve should be monotonically decreasing (thermodynamically
   stable direction) and C_v should be positive definite.

Output: mc_free_energy_results.json  +  mc_free_energy_plot.txt
"""
import json, math, random, os
from pathlib import Path
import numpy as np

# Build the FCC Lu skeleton + 24 interstitial sites (same as make_dataset.py)
random.seed(20260704)
np.random.seed(20260704)

A_LATT = 5.03  # Å
CELL = 2 * A_LATT  # 2x2x2 supercell edge
N_INT = 24
KB = 8.617333262e-5  # eV/K

# Coordinates of 24 interstitial sites (8 octa + 16 tetra) inside 2x2x2 fcc
def interstitial_sites():
    sites = []
    # 8 octahedral sites at (0.5, 0.5, 0.5) of each of 8 primitive fcc cells
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sites.append(((i+0.5)*A_LATT, (j+0.5)*A_LATT, (k+0.5)*A_LATT))
    # 16 tetrahedral sites at (0.25,0.25,0.25) + fcc translates in each subcell
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for (dx, dy, dz) in [(0.25,0.25,0.25),(0.25,0.75,0.75)]:
                    sites.append(((i+dx)*A_LATT, (j+dy)*A_LATT, (k+dz)*A_LATT))
    return np.array(sites)  # (24, 3)

SITES = interstitial_sites()
assert SITES.shape == (24, 3)

# Pair energies (eV, same as make_dataset.py)
PAIR = {
    ("H","H"): 0.15, ("N","N"): -0.60, ("H","N"): -0.05, ("N","H"): -0.05,
    ("Va","H"): 0.0, ("H","Va"): 0.0, ("Va","N"): 0.0, ("N","Va"): 0.0,
    ("Va","Va"): 0.0,
}

R_CUT = 4.5  # Å, same as paper CGCNN edge cutoff
def cosine_cutoff(r):
    return 0.5*(np.cos(np.pi*r/R_CUT)+1) if r < R_CUT else 0.0

# Precompute site distances with PBC (min-image)
def pair_distances():
    D = np.zeros((N_INT, N_INT))
    for i in range(N_INT):
        for j in range(N_INT):
            if i==j: continue
            d = SITES[i]-SITES[j]
            d -= CELL*np.round(d/CELL)
            D[i,j] = np.linalg.norm(d)
    return D
D = pair_distances()
CUT_WEIGHTS = np.zeros_like(D)
for i in range(N_INT):
    for j in range(N_INT):
        if i != j and D[i,j] < R_CUT:
            CUT_WEIGHTS[i,j] = cosine_cutoff(D[i,j])

def energy(occ):
    """Sum of cosine-cutoff-weighted pair energies, eV, per interstitial atom."""
    e = 0.0
    for i in range(N_INT):
        for j in range(i+1, N_INT):
            w = CUT_WEIGHTS[i,j]
            if w > 0:
                e += w * PAIR[(occ[i], occ[j])]
    return e / N_INT

def delta_energy(occ, i, new_i, j, new_j):
    """Energy change if we swap types at sites i and j simultaneously."""
    dE = 0.0
    for k in range(N_INT):
        if k==i or k==j: continue
        w_ik = CUT_WEIGHTS[i,k]
        w_jk = CUT_WEIGHTS[j,k]
        if w_ik > 0:
            dE += w_ik * (PAIR[(new_i, occ[k])] - PAIR[(occ[i], occ[k])])
        if w_jk > 0:
            dE += w_jk * (PAIR[(new_j, occ[k])] - PAIR[(occ[j], occ[k])])
    # And the direct i-j pair
    w_ij = CUT_WEIGHTS[i,j]
    if w_ij > 0:
        dE += w_ij * (PAIR[(new_i, new_j)] - PAIR[(occ[i], occ[j])])
    return dE / N_INT

def init_config(n_H, n_N):
    n_Va = N_INT - n_H - n_N
    occ = ["H"]*n_H + ["N"]*n_N + ["Va"]*n_Va
    random.shuffle(occ)
    return occ

def mc_run(occ, T, n_steps=20000, n_eq=5000):
    """H<->N swap MC at fixed composition. Metropolis."""
    beta = 1.0 / (KB * T)
    E = energy(occ)
    E_samples = []
    n_acc = 0
    n_prop = 0
    for step in range(n_steps):
        # Pick two different sites; require types differ AND at least one is H or N
        i = random.randrange(N_INT)
        j = random.randrange(N_INT)
        while j==i:
            j = random.randrange(N_INT)
        if occ[i] == occ[j]:
            continue
        n_prop += 1
        # Swap
        new_i, new_j = occ[j], occ[i]
        dE = delta_energy(occ, i, new_i, j, new_j)
        # Metropolis
        if dE < 0 or random.random() < math.exp(-beta * dE):
            occ[i], occ[j] = new_i, new_j
            E += dE
            n_acc += 1
        if step >= n_eq:
            E_samples.append(E)
    return np.array(E_samples), (n_acc/max(1,n_prop))

def thermodynamic_integration(T_grid, U_grid):
    """
    F(T)/T = F(T_ref)/T_ref  - integrate  U(T')/T'^2 dT' from T_ref to T.
    We normalize F(T_ref) = U(T_ref) as a reference (arbitrary constant).
    """
    U = np.asarray(U_grid); T = np.asarray(T_grid)
    F = np.zeros_like(T, dtype=float)
    F[0] = U[0]
    for k in range(1, len(T)):
        # Trapezoid rule on U/T^2 from T[k-1] to T[k]
        integrand = 0.5*(U[k-1]/T[k-1]**2 + U[k]/T[k]**2) * (T[k]-T[k-1])
        F[k] = T[k] * (F[k-1]/T[k-1] - integrand)
    return F

def main():
    T_grid = [300, 500, 800, 1100, 1500, 2000, 2500]
    # Two compositions to compare: N-rich and N-lean (paper's key finding)
    scenarios = [
        {"name":"N-lean_LuH2.5",   "n_H": 20, "n_N": 0},   # xN/xLu = 0
        {"name":"low_N_LuH2N0.25", "n_H": 16, "n_N": 2},   # xN/xLu = 0.25
        {"name":"high_N_LuH1N1",   "n_H": 8,  "n_N": 8},   # xN/xLu = 1.0
    ]

    out = {"T_grid_K": T_grid, "kB_eV_per_K": KB, "scenarios": []}
    for s in scenarios:
        print(f"\n=== {s['name']}  (n_H={s['n_H']}, n_N={s['n_N']}) ===")
        occ = init_config(s['n_H'], s['n_N'])
        U_grid = []
        Cv_grid = []
        acc_grid = []
        # Warm start: equilibrate at lowest T first, then anneal up
        for T in T_grid:
            E_samples, acc = mc_run(occ, T, n_steps=20000, n_eq=5000)
            U_mean = float(E_samples.mean())
            U_var = float(E_samples.var())
            Cv = U_var / (KB * T**2)  # per atom (E is per atom)
            U_grid.append(U_mean)
            Cv_grid.append(Cv)
            acc_grid.append(acc)
            print(f"  T={T:>5} K  <E>={U_mean*1000:+8.2f} meV/atom  σ={E_samples.std()*1000:5.2f}  Cv={Cv*1e6:8.2f} µeV/(atom·K)  acc={acc*100:.1f}%")
        F_grid = thermodynamic_integration(T_grid, U_grid).tolist()
        out["scenarios"].append({
            "name": s["name"], "n_H": s["n_H"], "n_N": s["n_N"],
            "x_N_over_x_Lu": s["n_N"]/8.0,
            "U_eV_per_atom": U_grid,
            "Cv_eV_per_atom_per_K": Cv_grid,
            "F_eV_per_atom": F_grid,
            "accept_rates": acc_grid,
        })
        print("  F(T) integration (eV/atom, w/ F(T_ref)=U(T_ref)):")
        for T, F in zip(T_grid, F_grid):
            print(f"    T={T:>5} K  F={F*1000:+8.2f} meV/atom")

    # Save
    outfile = Path(__file__).parent / "mc_free_energy_results.json"
    outfile.write_text(json.dumps(out, indent=2))
    print(f"\nWROTE {outfile}")

    # Also emit a plaintext summary
    plot_file = Path(__file__).parent / "mc_free_energy_plot.txt"
    with open(plot_file, "w") as f:
        f.write("Temperature (K) vs Gibbs free energy F(T) - F(300K) per atom (meV)\n")
        f.write("Reference: same composition, T=300 K\n\n")
        f.write(f"{'T (K)':>7}  " + "  ".join(f"{s['name']:>20s}" for s in out["scenarios"]) + "\n")
        for i, T in enumerate(T_grid):
            row = [f"{T:>7}"]
            for s in out["scenarios"]:
                dF = (s["F_eV_per_atom"][i] - s["F_eV_per_atom"][0])*1000
                row.append(f"{dF:>20.2f}")
            f.write("  ".join(row) + "\n")
    print(f"WROTE {plot_file}")

if __name__ == "__main__":
    main()
