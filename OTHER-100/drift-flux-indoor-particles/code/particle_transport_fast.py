#!/usr/bin/env python3
"""
Drift-Flux Particle Transport Model — Vectorized NumPy Implementation
Replication of Chen, Yu & Lai (2006), Atmospheric Environment 40, 357-367

Fast vectorized version using numpy array operations instead of triple loops.
"""

import numpy as np
import json
import os
import sys
import time as clock

# Physical constants
K_BOLTZMANN = 1.38e-23
G = 9.81
T_AIR = 293.0
RHO_AIR = 1.205
MU_AIR = 1.81e-5
NU_AIR = MU_AIR / RHO_AIR
LAMBDA_AIR = 6.6e-8
RHO_PARTICLE = 1400.0

# Room geometry
LX, LY, LZ = 0.8, 0.4, 0.4
NX, NY, NZ = 40, 20, 20


def particle_properties(dp_um):
    """Compute all properties for a particle diameter in micrometers."""
    dp = dp_um * 1e-6
    Kn = 2 * LAMBDA_AIR / dp
    Cc = 1 + Kn * (2.514 + 0.800 * np.exp(-0.55 / Kn))
    tau_p = RHO_PARTICLE * dp**2 * Cc / (18 * MU_AIR)
    vs = tau_p * G
    D_brown = K_BOLTZMANN * T_AIR * Cc / (3 * np.pi * MU_AIR * dp)
    return {'dp': dp, 'dp_um': dp_um, 'Cc': Cc, 'vs': vs,
            'D_brown': D_brown, 'tau_p': tau_p}


def lai_nazaroff_vd(dp_um, u_star, orientation='vertical'):
    """Lai & Nazaroff (2000) deposition velocity."""
    pp = particle_properties(dp_um)
    Sc = NU_AIR / pp['D_brown']
    vs_plus = pp['vs'] / u_star if u_star > 0 else 0

    # Numerical integration of resistance through boundary layer
    n = 5000
    y_plus = np.linspace(0.01, 100, n)
    dy = y_plus[1] - y_plus[0]

    # Turbulent diffusivity profile (DNS-fitted)
    ep_plus = np.zeros(n)
    mask1 = y_plus < 0.5
    mask2 = (y_plus >= 0.5) & (y_plus < 5.0)
    mask3 = y_plus >= 5.0
    ep_plus[mask2] = (y_plus[mask2] / 14.5)**3
    ep_plus[mask3] = 0.4 * y_plus[mask3] - 1.0
    ep_plus = np.maximum(ep_plus, 0)

    D_total = 1.0 / Sc + ep_plus
    R = np.sum(dy / D_total)

    if orientation == 'floor':
        vd_plus = vs_plus + 1.0 / R
    elif orientation == 'ceiling':
        arg = vs_plus * R
        if arg > 50:
            vd_plus = 1.0 / R
        elif arg < 1e-10:
            vd_plus = 1.0 / R
        else:
            vd_plus = vs_plus / (np.exp(arg) - 1.0)
    else:
        vd_plus = 1.0 / R

    return vd_plus * u_star


def simple_flow_field(nx, ny, nz, u_inlet):
    """
    Create a simplified recirculating flow field.
    For proper replication, replace with OpenFOAM solution.

    This models the key features:
    - Inlet jet near ceiling
    - Primary recirculation cell
    - Return flow along floor
    """
    dx, dy, dz = LX/nx, LY/ny, LZ/nz
    xc = np.linspace(dx/2, LX-dx/2, nx)
    yc = np.linspace(dy/2, LY-dy/2, ny)
    zc = np.linspace(dz/2, LZ-dz/2, nz)

    X, Y, Z = np.meshgrid(xc, yc, zc, indexing='ij')

    # Jet from inlet (x=0, y~0.2, z~0.36)
    dy_jet = Y - 0.2
    dz_jet = Z - 0.36
    r_jet = np.sqrt(dy_jet**2 + dz_jet**2)

    # Jet spreading
    sigma = 0.02 + 0.2 * X
    u_jet = u_inlet * (0.02/sigma)**0.5 * np.exp(-(r_jet/sigma)**2)

    # Recirculation: return flow at bottom
    x_n = X / LX
    z_n = Z / LZ
    u_recirc = -0.15 * u_inlet * np.sin(np.pi * x_n) * (1 - z_n)**2

    U = u_jet + u_recirc
    V = np.zeros_like(U)

    # Vertical velocity from continuity (approximate)
    W = -0.08 * u_inlet * np.sin(np.pi * x_n) * np.sin(np.pi * z_n)

    # Turbulent viscosity (order of magnitude estimate)
    nut = 10 * NU_AIR * np.ones_like(U)

    # Friction velocity (approximate from wall shear)
    u_star_val = 0.04 * u_inlet

    return U, V, W, nut, u_star_val, xc, yc, zc


def solve_transport_vectorized(U, V, W, nut, u_star, xc, yc, zc,
                                particle, dt, t_end, save_times=None):
    """
    Vectorized FVM solver for particle transport.

    dC/dt + div[(u+vs_z)C] = div[(D+nut)gradC] - deposition_sinks
    """
    nx, ny, nz = U.shape
    dx, dy, dz = xc[1]-xc[0], yc[1]-yc[0], zc[1]-zc[0]

    if save_times is None:
        save_times = [60, 180, 300, 600, 1200, 1800]

    pp = particle
    vs = pp['vs']
    D_eff = pp['D_brown'] + nut  # 3D array

    # Deposition velocities
    vd_floor = lai_nazaroff_vd(pp['dp_um'], u_star, 'floor')
    vd_ceil = lai_nazaroff_vd(pp['dp_um'], u_star, 'ceiling')
    vd_vert = lai_nazaroff_vd(pp['dp_um'], u_star, 'vertical')

    # Inlet/outlet masks
    inlet_mask_yz = np.zeros((ny, nz), dtype=bool)
    outlet_mask_yz = np.zeros((ny, nz), dtype=bool)
    for iy in range(ny):
        for iz in range(nz):
            if abs(yc[iy] - 0.2) <= 0.02 and abs(zc[iz] - 0.36) <= 0.02:
                inlet_mask_yz[iy, iz] = True
            if abs(yc[iy] - 0.2) <= 0.02 and abs(zc[iz] - 0.04) <= 0.02:
                outlet_mask_yz[iy, iz] = True

    C = np.zeros((nx, ny, nz))
    n_steps = int(t_end / dt)

    results = {'times': [], 'cv': [], 'mean_c': [], 'fields': {}}
    save_every = max(1, int(60 / dt))  # stats every 60s

    t_start = clock.time()

    for step in range(1, n_steps + 1):
        t = step * dt

        # ---- Convective fluxes (1st order upwind, fully vectorized) ----
        # Ghost-cell padded concentration
        Cp = np.pad(C, 1, mode='edge')  # pad with edge values
        # Override ghost cells: inlet = 1.0, walls = 0 flux (handled below)
        Cp[0, 1:-1, 1:-1] = np.where(inlet_mask_yz, 1.0, C[0])  # inlet ghost

        # x-direction: faces at i+1/2 for i=0..nx
        uf = np.zeros((nx+1, ny, nz))
        uf[1:-1] = 0.5 * (U[:-1] + U[1:])
        uf[0] = U[0]
        uf[-1] = U[-1]

        # Left/right cell concentrations at each face
        C_left_x = Cp[:-1, 1:-1, 1:-1]   # (nx+1, ny, nz)
        C_right_x = Cp[1:, 1:-1, 1:-1]   # (nx+1, ny, nz)
        # But Cp is (nx+2, ny+2, nz+2), so slicing gives (nx+1, ny, nz) -- correct

        Fx = np.where(uf >= 0, uf * C_left_x, uf * C_right_x)
        # Zero wall flux at x=0 (non-inlet) and x=Lx (non-outlet)
        Fx[0] = np.where(inlet_mask_yz, Fx[0], 0)
        Fx[-1] = np.where(outlet_mask_yz, Fx[-1], 0)

        conv_x = (Fx[1:] - Fx[:-1]) / dx

        # y-direction: faces at j+1/2 for j=0..ny
        vf = np.zeros((nx, ny+1, nz))
        vf[:, 1:-1, :] = 0.5 * (V[:, :-1, :] + V[:, 1:, :])

        C_left_y = Cp[1:-1, :-1, 1:-1][:, :ny+1, :]  # ghost included
        C_right_y = Cp[1:-1, 1:, 1:-1][:, :ny+1, :]
        # Simpler: use shifted C
        Cpy = np.pad(C, ((0,0),(1,1),(0,0)), mode='edge')
        C_left_y = Cpy[:, :-1, :]   # (nx, ny+1, nz)
        C_right_y = Cpy[:, 1:, :]   # (nx, ny+1, nz)

        Fy = np.where(vf >= 0, vf * C_left_y, vf * C_right_y)
        Fy[:, 0, :] = 0   # y=0 wall
        Fy[:, -1, :] = 0  # y=Ly wall

        conv_y = (Fy[:, 1:, :] - Fy[:, :-1, :]) / dy

        # z-direction (with settling)
        W_eff = W - vs
        wf = np.zeros((nx, ny, nz+1))
        wf[:, :, 1:-1] = 0.5 * (W_eff[:, :, :-1] + W_eff[:, :, 1:])
        wf[:, :, 0] = -vs   # floor face: settling downward
        wf[:, :, -1] = 0    # ceiling: zero flux

        Cpz = np.pad(C, ((0,0),(0,0),(1,1)), mode='edge')
        C_left_z = Cpz[:, :, :-1]  # (nx, ny, nz+1)
        C_right_z = Cpz[:, :, 1:]  # (nx, ny, nz+1)

        Fz = np.where(wf >= 0, wf * C_left_z, wf * C_right_z)
        Fz[:, :, 0] = wf[:, :, 0] * C[:, :, 0]  # floor: settling out
        Fz[:, :, -1] = 0  # ceiling: no flux

        conv_z = (Fz[:, :, 1:] - Fz[:, :, :-1]) / dz

        conv_total = conv_x + conv_y + conv_z

        # ---- Diffusive fluxes (central differencing) ----
        diff = np.zeros((nx, ny, nz))

        # x-direction
        diff[1:-1] += D_eff[1:-1] * (C[:-2] - 2*C[1:-1] + C[2:]) / dx**2
        diff[0] += D_eff[0] * (C[1] - C[0]) / dx**2  # one-sided
        diff[-1] += D_eff[-1] * (C[-2] - C[-1]) / dx**2

        # y-direction
        diff[:, 1:-1, :] += D_eff[:, 1:-1, :] * \
            (C[:, :-2, :] - 2*C[:, 1:-1, :] + C[:, 2:, :]) / dy**2
        diff[:, 0, :] += D_eff[:, 0, :] * (C[:, 1, :] - C[:, 0, :]) / dy**2
        diff[:, -1, :] += D_eff[:, -1, :] * (C[:, -2, :] - C[:, -1, :]) / dy**2

        # z-direction
        diff[:, :, 1:-1] += D_eff[:, :, 1:-1] * \
            (C[:, :, :-2] - 2*C[:, :, 1:-1] + C[:, :, 2:]) / dz**2
        diff[:, :, 0] += D_eff[:, :, 0] * (C[:, :, 1] - C[:, :, 0]) / dz**2
        diff[:, :, -1] += D_eff[:, :, -1] * (C[:, :, -2] - C[:, :, -1]) / dz**2

        # ---- Deposition sinks ----
        dep = np.zeros((nx, ny, nz))
        dep[:, :, 0] += vd_floor / dz * C[:, :, 0]          # floor
        dep[:, :, -1] += vd_ceil / dz * C[:, :, -1]         # ceiling
        dep[:, 0, :] += vd_vert / dy * C[:, 0, :]           # y=0 wall
        dep[:, -1, :] += vd_vert / dy * C[:, -1, :]         # y=Ly wall
        # x=0 wall (non-inlet cells)
        dep[0, :, :] += vd_vert / dx * C[0, :, :] * \
            (~inlet_mask_yz[np.newaxis, :, :]).squeeze().astype(float)
        # x=Lx wall (non-outlet cells)
        dep[-1, :, :] += vd_vert / dx * C[-1, :, :] * \
            (~outlet_mask_yz[np.newaxis, :, :]).squeeze().astype(float)

        # ---- Time integration (explicit Euler) ----
        C = C + dt * (-conv_total + diff - dep)
        C = np.maximum(C, 0)  # non-negative

        # ---- Statistics and saving ----
        if step % save_every == 0 or step == n_steps:
            C_mean = np.mean(C)
            cv = np.std(C) / C_mean if C_mean > 1e-15 else 1.0
            results['times'].append(t)
            results['cv'].append(cv)
            results['mean_c'].append(C_mean)

        if t in save_times or step == n_steps:
            results['fields'][t] = C.copy()
            elapsed = clock.time() - t_start
            C_mean = np.mean(C)
            cv = np.std(C) / C_mean if C_mean > 1e-15 else 1.0
            print(f"    t={t:7.1f}s: mean(C+)={C_mean:.4f}, CV={cv:.3f}  "
                  f"[elapsed {elapsed:.1f}s, step {step}/{n_steps}]",
                  flush=True)

    return results


def extract_profiles(C, xc, yc, zc, x_locs=[0.2, 0.4, 0.6]):
    """Extract vertical concentration profiles at specified x locations."""
    profiles = {}
    iy_center = len(yc) // 2  # center plane

    for x_loc in x_locs:
        ix = np.argmin(np.abs(xc - x_loc))
        profiles[x_loc] = {
            'z': zc.tolist(),
            'C': C[ix, iy_center, :].tolist()
        }
    return profiles


def load_openfoam_fields(fields_dir):
    """Load OpenFOAM-exported numpy fields."""
    Ux = np.load(os.path.join(fields_dir, 'Ux.npy'))
    Uy = np.load(os.path.join(fields_dir, 'Uy.npy'))
    Uz = np.load(os.path.join(fields_dir, 'Uz.npy'))
    nut = np.load(os.path.join(fields_dir, 'nut.npy'))
    u_star = np.load(os.path.join(fields_dir, 'u_star.npy'))
    xc = np.load(os.path.join(fields_dir, 'xc.npy'))
    yc = np.load(os.path.join(fields_dir, 'yc.npy'))
    zc = np.load(os.path.join(fields_dir, 'zc.npy'))
    # Use mean u_star for deposition model
    u_star_mean = float(np.mean(u_star))
    print(f"Loaded OpenFOAM fields from {fields_dir}")
    print(f"  Ux: [{np.min(Ux):.4f}, {np.max(Ux):.4f}]")
    print(f"  nut: [{np.min(nut):.2e}, {np.max(nut):.2e}]")
    print(f"  u_star mean: {u_star_mean:.4f}")
    return Ux, Uy, Uz, nut, u_star_mean, xc, yc, zc


def run_simulation(u_inlet=0.225):
    """Run full simulation for one inlet velocity."""
    output_dir = os.path.join(
        os.path.expanduser('~'),
        f'Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles/results/case_U{u_inlet}'
    )
    os.makedirs(output_dir, exist_ok=True)

    print(f"{'='*70}")
    print(f"DRIFT-FLUX PARTICLE TRANSPORT — U_inlet = {u_inlet} m/s")
    print(f"Grid: {NX}x{NY}x{NZ}, Room: {LX}x{LY}x{LZ} m")
    print(f"Output: {output_dir}")
    print(f"{'='*70}")

    # Try to load OpenFOAM fields first
    fields_dir = os.path.join(
        os.path.expanduser('~'),
        'Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles/data/openfoam_fields'
    )
    if os.path.exists(os.path.join(fields_dir, 'Ux.npy')):
        print("Using OpenFOAM flow field")
        U, V, W, nut, u_star, xc, yc, zc = load_openfoam_fields(fields_dir)
    else:
        print("WARNING: No OpenFOAM fields found, using analytical approximation")
        U, V, W, nut, u_star, xc, yc, zc = simple_flow_field(NX, NY, NZ, u_inlet)
    dx = xc[1] - xc[0]
    dy = yc[1] - yc[0]
    dz = zc[1] - zc[0]

    # CFL time step
    u_max = max(np.max(np.abs(U)), np.max(np.abs(V)), np.max(np.abs(W)), 0.01)
    D_max = np.max(nut) + NU_AIR
    dt_conv = 0.3 * min(dx, dy, dz) / u_max
    dt_diff = 0.15 * min(dx, dy, dz)**2 / D_max
    dt = min(dt_conv, dt_diff, 0.05)
    print(f"dt = {dt:.4f}s (CFL: conv={dt_conv:.4f}, diff={dt_diff:.4f})")

    sizes_um = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    all_results = {}
    summary_data = {}

    for dp_um in sizes_um:
        pp = particle_properties(dp_um)
        print(f"\n--- dp = {dp_um} um (vs={pp['vs']:.2e} m/s, D={pp['D_brown']:.2e} m2/s) ---")

        results = solve_transport_vectorized(
            U, V, W, nut, u_star, xc, yc, zc,
            pp, dt, t_end=1800, save_times=[60, 180, 300, 600, 1200, 1800]
        )

        all_results[dp_um] = results

        # Save concentration field at final time
        if 1800 in results['fields']:
            np.save(os.path.join(output_dir, f'C_dp{dp_um}_t1800.npy'),
                    results['fields'][1800])

            # Extract profiles for validation
            profiles = extract_profiles(results['fields'][1800], xc, yc, zc)
            with open(os.path.join(output_dir, f'profiles_dp{dp_um}.json'), 'w') as f:
                json.dump(profiles, f, indent=2)

        # Mixing time
        mix_time = None
        for t_val, cv_val in zip(results['times'], results['cv']):
            if cv_val < 0.1:
                mix_time = t_val
                break

        summary_data[str(dp_um)] = {
            'mixing_time': mix_time,
            'final_cv': results['cv'][-1] if results['cv'] else None,
            'final_mean_c': results['mean_c'][-1] if results['mean_c'] else None,
            'vs': pp['vs'],
            'D_brown': pp['D_brown']
        }

    # Save CV time series for plotting
    cv_data = {}
    for dp_um in sizes_um:
        r = all_results[dp_um]
        cv_data[str(dp_um)] = {
            'times': r['times'],
            'cv': r['cv'],
            'mean_c': r['mean_c']
        }

    with open(os.path.join(output_dir, 'cv_timeseries.json'), 'w') as f:
        json.dump(cv_data, f, indent=2, default=lambda x: float(x))

    with open(os.path.join(output_dir, 'summary.json'), 'w') as f:
        json.dump(summary_data, f, indent=2, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else x)

    # Print summary table
    print(f"\n{'='*70}")
    print(f"RESULTS SUMMARY — U_inlet = {u_inlet} m/s")
    print(f"{'='*70}")
    print(f"{'dp (um)':>10} {'vs (m/s)':>12} {'mix_time (s)':>14} {'final CV':>10} {'final <C>':>10}")
    print("-" * 60)
    for dp_um in sizes_um:
        s = summary_data[str(dp_um)]
        mt = f"{s['mixing_time']:.0f}" if s['mixing_time'] else "N/A"
        print(f"{dp_um:10.2f} {s['vs']:12.2e} {mt:>14} {s['final_cv']:10.3f} {s['final_mean_c']:10.4f}")

    return all_results


if __name__ == '__main__':
    u_inlet = 0.225
    if len(sys.argv) > 1:
        u_inlet = float(sys.argv[1])

    t0 = clock.time()
    run_simulation(u_inlet)
    print(f"\nTotal wall time: {clock.time()-t0:.1f}s")
