#!/usr/bin/env python3
"""
2D simulation of post-discharge kernel ignition in a turbulent stratified crossflow.
Replicates key physics from Jaravel et al. (2019), OSTI 1559043.

Fully vectorized numpy implementation for performance.
Solves advection-diffusion-reaction for velocity, temperature, and species.
"""

import numpy as np
from scipy import ndimage
import os
import time as timer
import json

# ============================================================
# Physical Constants & Species Data
# ============================================================
R_u = 8.314  # J/(mol*K)

SPECIES = ['CH4', 'O2', 'N2', 'CO2', 'H2O', 'NO', 'O']
N_SP = len(SPECIES)
SP_IDX = {sp: i for i, sp in enumerate(SPECIES)}

MW = np.array([16.04e-3, 32.0e-3, 28.0e-3, 44.01e-3, 18.015e-3, 30.01e-3, 16.0e-3])
CP_BASE = np.array([2226.0, 918.0, 1040.0, 846.0, 1864.0, 995.0, 1300.0])

# Chemistry constants
Q_comb = 50.0e6    # J/kg CH4
Ea_comb = 125.52e3  # J/mol
A_comb = 1.3e8      # 1/s (Westbrook-Dryer adjusted)
Ea_NO = 319.0e3     # J/mol
A_NO = 1.8e14

# Stoich: CH4 + 2O2 -> CO2 + 2H2O
# Mass ratios per kg CH4 consumed
NU_O2 = 2 * 32.0 / 16.04    # 3.99 kg O2 / kg CH4
NU_CO2 = 44.01 / 16.04      # 2.744
NU_H2O = 2 * 18.015 / 16.04 # 2.246

# ============================================================
# Domain & Grid
# ============================================================
Lx, Lz = 0.073, 0.050  # m
dx = dz = 0.0005       # m (0.5mm)
Nx, Nz = int(Lx/dx), int(Lz/dz)

# Operating conditions
u_in = 20.0        # m/s
T_in = 456.0       # K
P_amb = 1.0e5      # Pa
h_s = 6.4e-3       # m splitter plate height
u_prime = 2.0      # m/s RMS
l_turb = 3.2e-3    # m

# Kernel
U_ker = 2000.0     # m/s
tau_pulse = 3e-6   # s
D_ker = 5.0e-3     # m
T_ker = 3300.0     # K
x_ker_pos = 13.0e-3  # m from inlet

# Time
dt = 5e-7
t_end = 0.002  # 2ms
Nt = int(t_end / dt)

# Transport
mu_ref = 1.8e-5   # Pa*s
D_diff = 2.0e-5   # m^2/s
alpha_th = 2.5e-5  # m^2/s

# Kernel composition (mass fractions)
Y_ker = np.zeros(N_SP)
# Convert mole fractions from paper Table 1 to mass fractions
X_ker = {'N2': 0.74, 'O2': 0.14, 'NO': 0.054, 'O': 0.062}
Mmix_ker = sum(X_ker.get(sp, 0) * MW[i] for i, sp in enumerate(SPECIES))
for sp, xf in X_ker.items():
    Y_ker[SP_IDX[sp]] = xf * MW[SP_IDX[sp]] / Mmix_ker

print(f"Grid: {Nx}x{Nz}={Nx*Nz} cells, dt={dt*1e6:.2f}μs, Nt={Nt}")

# ============================================================
# Vectorized helper functions
# ============================================================
def laplacian_2d(f, dx, dz):
    """2D Laplacian using central differences."""
    d2fdx2 = np.zeros_like(f)
    d2fdz2 = np.zeros_like(f)
    d2fdx2[1:-1, :] = (f[2:, :] - 2*f[1:-1, :] + f[:-2, :]) / dx**2
    d2fdz2[:, 1:-1] = (f[:, 2:] - 2*f[:, 1:-1] + f[:, :-2]) / dz**2
    return d2fdx2 + d2fdz2

def upwind_advect(f, u, w, dx, dz):
    """Upwind advection: -u*df/dx - w*df/dz"""
    dfdx = np.zeros_like(f)
    dfdz = np.zeros_like(f)
    
    # x-direction: upwind based on u sign
    up = u > 0
    # Forward: (f[i] - f[i-1])/dx where u>0
    dfdx[1:, :] = np.where(up[1:, :],
                            (f[1:, :] - f[:-1, :]) / dx,
                            0)
    dfdx[:-1, :] += np.where(~up[:-1, :],
                              (f[1:, :] - f[:-1, :]) / dx,
                              0)
    
    # z-direction: upwind based on w sign
    wp = w > 0
    dfdz[:, 1:] = np.where(wp[:, 1:],
                            (f[:, 1:] - f[:, :-1]) / dz,
                            0)
    dfdz[:, :-1] += np.where(~wp[:, :-1],
                              (f[:, 1:] - f[:, :-1]) / dz,
                              0)
    
    return -u * dfdx - w * dfdz

def compute_chemistry_vectorized(Y_arr, T, rho, dt_chem):
    """Vectorized chemistry source terms. Y_arr shape: (N_SP, Nx, Nz)."""
    omega = np.zeros_like(Y_arr)
    q_dot = np.zeros((Nx, Nz))
    
    Y_CH4 = np.maximum(Y_arr[SP_IDX['CH4']], 0)
    Y_O2 = np.maximum(Y_arr[SP_IDX['O2']], 0)
    Y_N2 = np.maximum(Y_arr[SP_IDX['N2']], 0)
    Y_O = np.maximum(Y_arr[SP_IDX['O']], 0)
    
    # Combustion: CH4 + 2O2 -> CO2 + 2H2O
    conc_CH4 = rho * Y_CH4 / MW[SP_IDX['CH4']]
    conc_O2 = rho * Y_O2 / MW[SP_IDX['O2']]
    
    react_mask = (T > 800) & (Y_CH4 > 1e-6) & (Y_O2 > 1e-6)
    rate = np.where(react_mask,
                    A_comb * np.power(np.maximum(conc_CH4, 1e-10), 0.2) *
                    np.power(np.maximum(conc_O2, 1e-10), 1.3) *
                    np.exp(-Ea_comb / (R_u * np.maximum(T, 300))),
                    0.0)
    
    # Limit rate for stability
    max_rate = rho * Y_CH4 / (MW[SP_IDX['CH4']] * dt_chem * 0.5 + 1e-30)
    rate = np.minimum(rate, max_rate)
    
    omega[SP_IDX['CH4']] = -rate * MW[SP_IDX['CH4']]
    omega[SP_IDX['O2']] = -rate * 2.0 * MW[SP_IDX['O2']]
    omega[SP_IDX['CO2']] = rate * MW[SP_IDX['CO2']]
    omega[SP_IDX['H2O']] = rate * 2.0 * MW[SP_IDX['H2O']]
    
    q_dot = rate * MW[SP_IDX['CH4']] * Q_comb  # W/m^3
    
    # O radical recombination (exothermic, fast)
    O_mask = Y_O > 1e-6
    tau_recomb = np.where(O_mask, 1e-4 * np.exp(10000.0 / np.maximum(T, 300)), 1e10)
    rate_O_recomb = rho * Y_O / np.maximum(tau_recomb, dt_chem)
    omega[SP_IDX['O']] -= rate_O_recomb
    omega[SP_IDX['O2']] += rate_O_recomb * 0.5
    q_dot += rate_O_recomb * 2.5e6  # recombination heat
    
    # Thermal NO (simplified Zeldovich)
    conc_N2 = rho * Y_N2 / MW[SP_IDX['N2']]
    NO_mask = (T > 1500) & (Y_N2 > 0.01)
    conc_O_eq = conc_O2 * 3.97e5 * np.exp(-31090.0 / np.maximum(T, 300))
    conc_O_total = rho * Y_O / MW[SP_IDX['O']] + conc_O_eq
    rate_NO = np.where(NO_mask,
                       A_NO * conc_N2 * conc_O_total * np.exp(-Ea_NO / (R_u * np.maximum(T, 300))),
                       0.0)
    max_rate_NO = rho * Y_N2 / (MW[SP_IDX['N2']] * dt_chem * 0.5 + 1e-30)
    rate_NO = np.minimum(rate_NO, max_rate_NO)
    omega[SP_IDX['NO']] += rate_NO * MW[SP_IDX['NO']]
    omega[SP_IDX['N2']] -= rate_NO * 0.5 * MW[SP_IDX['N2']]
    
    return omega, q_dot


def generate_inlet_turbulence(Nz, u_rms, l_int, dz):
    """Generate 1D turbulent velocity profile for inlet."""
    sigma = l_int / dz
    u_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), sigma=sigma) * u_rms * 3.0
    w_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), sigma=sigma) * u_rms * 3.0
    return u_turb, w_turb


# ============================================================
# Main simulation
# ============================================================
def run_simulation(phi, realization=0):
    """Run one ignition simulation."""
    print(f"\n{'='*60}")
    print(f"phi={phi}, realization={realization}")
    print(f"{'='*60}")
    
    np.random.seed(42 + realization * 1000 + int(phi * 100))
    
    # ---- Initialize fields ----
    u = np.full((Nx, Nz), u_in)
    w = np.zeros((Nx, Nz))
    T = np.full((Nx, Nz), T_in)
    Y_arr = np.zeros((N_SP, Nx, Nz))
    
    # Fuel stream composition
    f_stoich = 16.04 / (64.0 / 0.232)  # stoichiometric fuel-air ratio
    Y_CH4_fuel = phi * f_stoich / (1 + phi * f_stoich)
    Y_O2_fuel = 0.232 * (1 - Y_CH4_fuel / 0.232)  # approximate
    Y_O2_fuel = max(0.232 - Y_CH4_fuel * NU_O2 * 0.232 / (NU_O2 * Y_CH4_fuel + 0.232), 0)
    # Simpler: in premixed stream
    Y_O2_fuel = 0.232 * (1 - Y_CH4_fuel)
    Y_N2_fuel = 1.0 - Y_CH4_fuel - Y_O2_fuel
    
    # Smooth mixing layer at splitter plate
    z_arr = np.arange(Nz) * dz
    blend = 0.5 * (1 + np.tanh((z_arr - h_s) / 1e-3))  # shape (Nz,)
    
    Y_arr[SP_IDX['CH4'], :, :] = blend[np.newaxis, :]  * Y_CH4_fuel
    Y_arr[SP_IDX['O2'], :, :] = 0.232 * (1 - blend[np.newaxis, :]) + Y_O2_fuel * blend[np.newaxis, :]
    Y_arr[SP_IDX['N2'], :, :] = 0.768 * (1 - blend[np.newaxis, :]) + Y_N2_fuel * blend[np.newaxis, :]
    
    # Density from ideal gas
    Mmix = 1.0 / np.sum(Y_arr / MW[:, np.newaxis, np.newaxis], axis=0)
    rho = P_amb * Mmix / (R_u * T)
    
    # Kernel ejection cells
    i_ker = int(x_ker_pos / dx)
    n_ker = int(D_ker / dx)
    i_start = max(0, i_ker - n_ker // 2)
    i_end = min(Nx, i_ker + n_ker // 2)
    r_ker = np.abs(np.arange(i_start, i_end) - i_ker) * dx / (D_ker / 2)
    ker_profile = np.sqrt(np.maximum(1 - r_ker**2, 0))  # radial velocity profile
    
    # Time history storage
    t_hist, Qdot_hist, Tmax_hist = [], [], []
    snapshots = {}
    
    wall_t0 = timer.time()
    save_every = max(1, int(0.0002 / dt))
    hist_every = max(1, int(1e-5 / dt))  # record every 10μs
    
    for n in range(Nt):
        t = n * dt
        
        # ---- Advection ----
        adv_u = upwind_advect(u, u, w, dx, dz)
        adv_w = upwind_advect(w, u, w, dx, dz)
        adv_T = upwind_advect(T, u, w, dx, dz)
        
        # ---- Diffusion ----
        nu = mu_ref / np.maximum(rho, 0.1)
        diff_u = nu * laplacian_2d(u, dx, dz)
        diff_w = nu * laplacian_2d(w, dx, dz)
        diff_T = alpha_th * laplacian_2d(T, dx, dz)
        
        # ---- Species advection + diffusion ----
        adv_Y = np.zeros_like(Y_arr)
        diff_Y = np.zeros_like(Y_arr)
        for s in range(N_SP):
            adv_Y[s] = upwind_advect(Y_arr[s], u, w, dx, dz)
            diff_Y[s] = D_diff * laplacian_2d(Y_arr[s], dx, dz)
        
        # ---- Chemistry ----
        omega, q_dot = compute_chemistry_vectorized(Y_arr, T, rho, dt)
        
        # Mixture Cp
        cp_mix = np.sum(Y_arr * CP_BASE[:, np.newaxis, np.newaxis] *
                        (1 + 2.5e-4 * (T[np.newaxis, :, :] - 300)), axis=0)
        cp_mix = np.maximum(cp_mix, 500.0)
        
        # ---- Update ----
        u += dt * (adv_u + diff_u)
        w += dt * (adv_w + diff_w)
        T += dt * (adv_T + diff_T + q_dot / (rho * cp_mix))
        Y_arr += dt * (adv_Y + diff_Y + omega / np.maximum(rho[np.newaxis, :, :], 0.1))
        
        # ---- Kernel injection ----
        if t < 2 * tau_pulse:
            M_t = 1.0 if t < tau_pulse else max(0, 1.0 - (t - tau_pulse) / tau_pulse)
            if M_t > 0:
                for idx, ii in enumerate(range(i_start, i_end)):
                    u_n = M_t * U_ker * ker_profile[idx]
                    u_n *= (1.0 + 0.2 * np.random.randn())
                    u_n = max(u_n, 0)
                    
                    rho_ker = P_amb * 0.028 / (R_u * T_ker)
                    frac = min(dt * rho_ker * u_n / (dz * np.maximum(rho[ii, :3], 0.1)), 0.3)
                    
                    w[ii, :3] += frac * u_n
                    T[ii, :3] = (1 - frac) * T[ii, :3] + frac * T_ker
                    for s in range(N_SP):
                        Y_arr[s, ii, :3] = (1-frac) * Y_arr[s, ii, :3] + frac * Y_ker[s]
        
        # ---- Boundary Conditions ----
        # Inlet
        if n % 50 == 0:
            u_turb, w_turb = generate_inlet_turbulence(Nz, u_prime, l_turb, dz)
        u[0, :] = u_in + u_turb
        w[0, :] = w_turb
        T[0, :] = T_in
        Y_arr[SP_IDX['CH4'], 0, :] = blend * Y_CH4_fuel
        Y_arr[SP_IDX['O2'], 0, :] = 0.232 * (1 - blend) + Y_O2_fuel * blend
        Y_arr[SP_IDX['N2'], 0, :] = 0.768 * (1 - blend) + Y_N2_fuel * blend
        Y_arr[SP_IDX['CO2'], 0, :] = 0
        Y_arr[SP_IDX['H2O'], 0, :] = 0
        Y_arr[SP_IDX['NO'], 0, :] = 0
        Y_arr[SP_IDX['O'], 0, :] = 0
        
        # Outlet: zero gradient
        u[-1, :] = u[-2, :]
        w[-1, :] = w[-2, :]
        T[-1, :] = T[-2, :]
        Y_arr[:, -1, :] = Y_arr[:, -2, :]
        
        # Bottom wall: no-slip adiabatic
        u[:, 0] = 0; w[:, 0] = 0
        T[:, 0] = T[:, 1]
        Y_arr[:, :, 0] = Y_arr[:, :, 1]
        
        # Top wall
        u[:, -1] = 0; w[:, -1] = 0
        T[:, -1] = T[:, -2]
        Y_arr[:, :, -1] = Y_arr[:, :, -2]
        
        # Clip
        T = np.clip(T, 200, 4000)
        Y_arr = np.clip(Y_arr, 0, 1)
        
        # Update density
        Mmix = 1.0 / np.maximum(np.sum(Y_arr / MW[:, np.newaxis, np.newaxis], axis=0), 1e-10)
        rho = P_amb * Mmix / (R_u * np.maximum(T, 200))
        
        # ---- Recording ----
        if n % hist_every == 0:
            Qdot_total = np.sum(q_dot) * dx * dz
            t_hist.append(float(t * 1000))
            Qdot_hist.append(float(Qdot_total))
            Tmax_hist.append(float(np.max(T)))
        
        if n > 0 and n % save_every == 0:
            t_ms = t * 1000
            snapshots[f't_{t_ms:.1f}ms'] = {
                'T': T.copy(), 'u': u.copy(), 'w': w.copy(),
                'Y_CH4': Y_arr[SP_IDX['CH4']].copy(),
                'Y_O2': Y_arr[SP_IDX['O2']].copy(),
                'Y_NO': Y_arr[SP_IDX['NO']].copy(),
                'q_dot': q_dot.copy(),
            }
            print(f"  t={t_ms:.1f}ms Tmax={np.max(T):.0f}K Qdot={Qdot_total:.2e} "
                  f"[{timer.time()-wall_t0:.0f}s]")
        
        if n > 0 and n % (Nt // 10) == 0:
            pct = 100 * n / Nt
            el = timer.time() - wall_t0
            print(f"  {pct:.0f}% t={t*1000:.3f}ms Tmax={np.max(T):.0f}K elapsed={el:.0f}s")
    
    result = {
        'phi': phi, 'realization': realization,
        't_history': t_hist, 'Qdot_history': Qdot_hist, 'T_max_history': Tmax_hist,
        'final_Qdot': Qdot_hist[-1] if Qdot_hist else 0,
        'final_T_max': float(np.max(T)),
    }
    
    return result, snapshots


def main():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
    os.makedirs(out_dir, exist_ok=True)
    
    phis = [0.6, 0.8, 1.0, 1.2]
    n_real = 3
    
    all_results = {}
    
    for phi in phis:
        all_results[f'phi_{phi}'] = []
        for r in range(n_real):
            result, snaps = run_simulation(phi, realization=r)
            all_results[f'phi_{phi}'].append(result)
            
            # Save snapshots
            snap_dir = os.path.join(out_dir, f'snapshots_phi{phi}_r{r}')
            os.makedirs(snap_dir, exist_ok=True)
            for key, snap in snaps.items():
                np.savez_compressed(os.path.join(snap_dir, f'{key}.npz'), **snap)
    
    # Compute ignition propensity
    max_Qdot = max(r['final_Qdot'] for phi_res in all_results.values() for r in phi_res)
    max_Qdot = max(max_Qdot, 1e-10)
    
    print("\n" + "="*60)
    print("IGNITION PROPENSITY RESULTS")
    print("="*60)
    
    summary = {}
    for phi in phis:
        key = f'phi_{phi}'
        IPs = [r['final_Qdot'] / max_Qdot for r in all_results[key]]
        T_maxs = [r['final_T_max'] for r in all_results[key]]
        summary[key] = {
            'IP_mean': float(np.mean(IPs)),
            'IP_std': float(np.std(IPs)),
            'T_max_mean': float(np.mean(T_maxs)),
            'IPs': [float(x) for x in IPs],
        }
        print(f"  phi={phi:.1f}: IP={np.mean(IPs):.3f}±{np.std(IPs):.3f}, Tmax={np.mean(T_maxs):.0f}K")
    
    with open(os.path.join(out_dir, 'simulation_results.json'), 'w') as f:
        json.dump({'results': all_results, 'summary': summary}, f, indent=2, default=str)
    
    print(f"\nSaved to {out_dir}/simulation_results.json")
    return all_results, summary

if __name__ == '__main__':
    main()
