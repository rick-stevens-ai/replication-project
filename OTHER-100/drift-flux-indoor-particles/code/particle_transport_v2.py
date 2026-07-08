#!/usr/bin/env python3
"""
Drift-Flux Particle Transport Model — v2 with mass conservation fix.

Key improvement over v1: The transport equation for concentration C is:
    dC/dt + div(u*C) = div(D*grad(C)) - deposition

The convection term div(u*C) = u·grad(C) + C·div(u).
If div(u) ≠ 0 (due to cell-center interpolation), the C·div(u) term
creates a spurious source/sink of particles.

Fix: Use the "conservative" form but subtract the divergence error:
    dC/dt + u·grad(C) = div(D*grad(C)) - deposition
    
i.e., use the advective (non-conservative) form for convection.
This is equivalent to the conservative form when div(u)=0, but doesn't
create spurious sources when div(u) has numerical errors.

For the settling velocity (which IS conservative — particles fall out),
we keep the conservative form: div(vs*C).

Replication of Chen, Yu & Lai (2006), Atmospheric Environment 40, 357-367.
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

    n = 5000
    y_plus = np.linspace(0.01, 100, n)
    dy = y_plus[1] - y_plus[0]

    ep_plus = np.zeros(n)
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
    u_star_mean = float(np.mean(u_star))
    print(f"Loaded OpenFOAM fields from {fields_dir}")
    print(f"  Ux: [{np.min(Ux):.4f}, {np.max(Ux):.4f}]")
    print(f"  nut: [{np.min(nut):.2e}, {np.max(nut):.2e}]")
    print(f"  u_star mean: {u_star_mean:.4f}")
    return Ux, Uy, Uz, nut, u_star_mean, xc, yc, zc


def solve_transport_v2(U, V, W, nut, u_star, xc, yc, zc,
                       particle, dt, t_end, save_times=None):
    """
    v2 solver: uses advective form for air velocity (non-conservative)
    and conservative form for settling velocity only.
    
    dC/dt + u·∇C + div(vs·C) = div(D·∇C) - deposition
    
    The u·∇C term is computed with upwind differences applied to gradC,
    not to div(uC). This avoids the spurious source from div(u)≠0.
    """
    nx, ny, nz = U.shape
    dx = xc[1] - xc[0]
    dy = yc[1] - yc[0]
    dz = zc[1] - zc[0]

    if save_times is None:
        save_times = [60, 180, 300, 600, 1200, 1800]

    pp = particle
    vs = pp['vs']
    D_eff = pp['D_brown'] + nut  # 3D array

    # Deposition velocities (using mean u_star from all wall cells)
    if isinstance(u_star, np.ndarray):
        u_star_val = float(np.mean(u_star))
    else:
        u_star_val = u_star
    vd_floor = lai_nazaroff_vd(pp['dp_um'], u_star_val, 'floor')
    vd_ceil = lai_nazaroff_vd(pp['dp_um'], u_star_val, 'ceiling')
    vd_vert = lai_nazaroff_vd(pp['dp_um'], u_star_val, 'vertical')

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
    save_every = max(1, int(60 / dt))

    # Pre-compute save steps from save_times (avoid float equality issues)
    save_steps = set()
    for st in save_times:
        s = int(round(st / dt))
        if 1 <= s <= n_steps:
            save_steps.add(s)
    save_steps.add(n_steps)  # always save final

    t_start = clock.time()

    for step in range(1, n_steps + 1):
        t = step * dt
        dCdt = np.zeros_like(C)

        # ============================================================
        # ADVECTION: u·∇C  (non-conservative / advective form)
        # Uses upwind-biased gradient
        # ============================================================

        # x-direction: u * dC/dx (upwind)
        # Pad C with boundary values
        # x=0: inlet cells get C=1.0, wall cells get C[0] (zero-gradient)
        C_xm = np.zeros_like(C)  # C at i-1
        C_xm[1:] = C[:-1]
        C_xm[0] = np.where(inlet_mask_yz, 1.0, C[0])

        C_xp = np.zeros_like(C)  # C at i+1
        C_xp[:-1] = C[1:]
        C_xp[-1] = C[-1]  # zero-gradient at outlet

        # Upwind: use C_xm when U>0, C_xp when U<0
        dCdx_upwind = np.where(U >= 0,
                               (C - C_xm) / dx,
                               (C_xp - C) / dx)
        dCdt -= U * dCdx_upwind

        # y-direction: v * dC/dy (upwind)
        C_ym = np.zeros_like(C)
        C_ym[:, 1:, :] = C[:, :-1, :]
        C_ym[:, 0, :] = C[:, 0, :]  # zero-gradient at wall

        C_yp = np.zeros_like(C)
        C_yp[:, :-1, :] = C[:, 1:, :]
        C_yp[:, -1, :] = C[:, -1, :]  # zero-gradient at wall

        dCdy_upwind = np.where(V >= 0,
                               (C - C_ym) / dy,
                               (C_yp - C) / dy)
        dCdt -= V * dCdy_upwind

        # z-direction: w * dC/dz (upwind, WITHOUT settling)
        C_zm = np.zeros_like(C)
        C_zm[:, :, 1:] = C[:, :, :-1]
        C_zm[:, :, 0] = C[:, :, 0]  # zero-gradient at floor

        C_zp = np.zeros_like(C)
        C_zp[:, :, :-1] = C[:, :, 1:]
        C_zp[:, :, -1] = C[:, :, -1]  # zero-gradient at ceiling

        dCdz_upwind = np.where(W >= 0,
                               (C - C_zm) / dz,
                               (C_zp - C) / dz)
        dCdt -= W * dCdz_upwind

        # ============================================================
        # SETTLING: div(vs·C) in z-direction (conservative form)
        # vs points downward (negative z), so settling flux = -vs * C
        # ============================================================
        # Conservative: d(vs*C)/dz using upwind (vs is always downward)
        # Flux at z-faces: F = -vs * C (settling is always downward)
        # At floor (k=0): flux leaves domain (deposition)
        # At ceiling (k=-1): no flux in from above

        settle_flux_top = np.zeros((nx, ny, nz + 1))
        # Interior faces: upwind for downward velocity → use cell above
        settle_flux_top[:, :, 1:-1] = -vs * C[:, :, 1:]  # flux from cell above
        settle_flux_top[:, :, -1] = 0  # nothing coming in from above ceiling
        settle_flux_top[:, :, 0] = -vs * C[:, :, 0]  # settling out at floor

        dCdt -= (settle_flux_top[:, :, 1:] - settle_flux_top[:, :, :-1]) / dz

        # ============================================================
        # DIFFUSION: div(D·∇C) (central differencing)
        # ============================================================
        diff = np.zeros_like(C)

        # x-direction
        # Interior
        D_xp_half = 0.5 * (D_eff[:-1] + D_eff[1:])
        diff[:-1] += D_xp_half * (C[1:] - C[:-1]) / dx**2
        diff[1:] -= D_xp_half * (C[1:] - C[:-1]) / dx**2
        # x=0 boundary: inlet gets diffusion from C=1, walls get zero-flux
        diff[0] += D_eff[0] * np.where(inlet_mask_yz, (1.0 - C[0]), 0) / dx**2
        # x=Lx boundary: zero-gradient → no diffusion correction needed

        # y-direction
        D_yp_half = 0.5 * (D_eff[:, :-1, :] + D_eff[:, 1:, :])
        diff[:, :-1, :] += D_yp_half * (C[:, 1:, :] - C[:, :-1, :]) / dy**2
        diff[:, 1:, :] -= D_yp_half * (C[:, 1:, :] - C[:, :-1, :]) / dy**2
        # walls: zero-gradient → no boundary diffusion

        # z-direction
        D_zp_half = 0.5 * (D_eff[:, :, :-1] + D_eff[:, :, 1:])
        diff[:, :, :-1] += D_zp_half * (C[:, :, 1:] - C[:, :, :-1]) / dz**2
        diff[:, :, 1:] -= D_zp_half * (C[:, :, 1:] - C[:, :, :-1]) / dz**2

        dCdt += diff

        # ============================================================
        # DEPOSITION: surface sinks
        # ============================================================
        dCdt[:, :, 0] -= vd_floor / dz * C[:, :, 0]       # floor
        dCdt[:, :, -1] -= vd_ceil / dz * C[:, :, -1]      # ceiling
        dCdt[:, 0, :] -= vd_vert / dy * C[:, 0, :]        # y=0 wall
        dCdt[:, -1, :] -= vd_vert / dy * C[:, -1, :]      # y=Ly wall
        # x=0 wall (non-inlet)
        dCdt[0] -= vd_vert / dx * C[0] * (~inlet_mask_yz).astype(float)
        # x=Lx wall (non-outlet)
        dCdt[-1] -= vd_vert / dx * C[-1] * (~outlet_mask_yz).astype(float)

        # ============================================================
        # INLET SOURCE
        # ============================================================
        # The inlet brings in concentration C=1.0 through convection.
        # In the advective form, this is handled by the boundary ghost cell
        # having C=1.0 (already done above in C_xm).
        # 
        # Additionally, the outlet carries concentration out — this is
        # also handled by the zero-gradient BC (C_xp[-1] = C[-1]).

        # ============================================================
        # TIME INTEGRATION
        # ============================================================
        C = C + dt * dCdt
        C = np.maximum(C, 0)

        # ============================================================
        # STATISTICS
        # ============================================================
        if step % save_every == 0 or step == n_steps:
            C_mean = np.mean(C)
            cv = np.std(C) / C_mean if C_mean > 1e-15 else 1.0
            results['times'].append(t)
            results['cv'].append(cv)
            results['mean_c'].append(C_mean)

        if step in save_steps:
            t_save = round(t)  # round to nearest integer second
            results['fields'][t_save] = C.copy()
            elapsed = clock.time() - t_start
            C_mean = np.mean(C)
            cv = np.std(C) / C_mean if C_mean > 1e-15 else 1.0
            print(f"    t={t:7.1f}s: mean(C+)={C_mean:.4f}, CV={cv:.3f}  "
                  f"[elapsed {elapsed:.1f}s, step {step}/{n_steps}]",
                  flush=True)

    return results


def extract_profiles(C, xc, yc, zc, x_locs=[0.2, 0.4, 0.6]):
    """Extract vertical concentration profiles."""
    profiles = {}
    iy_center = len(yc) // 2
    for x_loc in x_locs:
        ix = np.argmin(np.abs(xc - x_loc))
        profiles[str(x_loc)] = {
            'z': zc.tolist(),
            'C': C[ix, iy_center, :].tolist()
        }
    return profiles


def run_case(u_inlet, fields_dir, output_dir):
    """Run one case with full field output."""
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"DRIFT-FLUX v2 — U_inlet = {u_inlet} m/s")
    print(f"Grid: {NX}x{NY}x{NZ}, Room: {LX}x{LY}x{LZ} m")
    print(f"Output: {output_dir}")
    print(f"{'='*70}")

    U, V, W, nut, u_star, xc, yc, zc = load_openfoam_fields(fields_dir)
    dx = xc[1] - xc[0]

    # CFL time step
    u_max = max(np.max(np.abs(U)), np.max(np.abs(V)), np.max(np.abs(W)), 0.01)
    D_max = np.max(nut) + NU_AIR
    dt_conv = 0.3 * min(dx, LY/NY, LZ/NZ) / u_max
    dt_diff = 0.15 * min(dx, LY/NY, LZ/NZ)**2 / D_max
    dt = min(dt_conv, dt_diff, 0.05)
    print(f"dt = {dt:.4f}s (CFL: conv={dt_conv:.4f}, diff={dt_diff:.4f})", flush=True)

    sizes_um = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    save_times = [60, 180, 300, 600, 900, 1200, 1500, 1800]

    all_results = {}
    summary_data = {}

    for dp_um in sizes_um:
        pp = particle_properties(dp_um)
        print(f"\n--- dp = {dp_um} μm (vs={pp['vs']:.2e} m/s, D={pp['D_brown']:.2e} m²/s) ---",
              flush=True)

        results = solve_transport_v2(
            U, V, W, nut, u_star, xc, yc, zc,
            pp, dt=dt, t_end=1800, save_times=save_times
        )

        all_results[dp_um] = results

        # Save concentration fields
        size_dir = os.path.join(output_dir, f'dp_{dp_um}')
        os.makedirs(size_dir, exist_ok=True)
        for t_save, C_field in results['fields'].items():
            np.save(os.path.join(size_dir, f'C_t{int(t_save)}.npy'), C_field)

        if 1800 in results['fields']:
            profiles = extract_profiles(results['fields'][1800], xc, yc, zc)
            with open(os.path.join(size_dir, 'profiles_t1800.json'), 'w') as f:
                json.dump(profiles, f, indent=2)

        # Mixing time
        mix_time = None
        for t_val, cv_val in zip(results['times'], results['cv']):
            if cv_val < 0.1:
                mix_time = t_val
                break

        summary_data[str(dp_um)] = {
            'mixing_time': mix_time,
            'final_cv': float(results['cv'][-1]) if results['cv'] else None,
            'final_mean_c': float(results['mean_c'][-1]) if results['mean_c'] else None,
            'vs': float(pp['vs']),
            'D_brown': float(pp['D_brown'])
        }

    # Save aggregated results
    cv_data = {}
    for dp_um in sizes_um:
        r = all_results[dp_um]
        cv_data[str(dp_um)] = {
            'times': [float(t) for t in r['times']],
            'cv': [float(c) for c in r['cv']],
            'mean_c': [float(m) for m in r['mean_c']]
        }

    with open(os.path.join(output_dir, 'cv_timeseries.json'), 'w') as f:
        json.dump(cv_data, f, indent=2)
    with open(os.path.join(output_dir, 'summary.json'), 'w') as f:
        json.dump(summary_data, f, indent=2)

    # Print summary
    print(f"\n{'='*70}")
    print(f"RESULTS — U = {u_inlet} m/s")
    print(f"{'='*70}")
    print(f"{'dp (μm)':>10} {'vs (m/s)':>12} {'mix_time':>10} {'final CV':>10} {'⟨C⁺⟩':>10}")
    print("-" * 55)
    for dp_um in sizes_um:
        s = summary_data[str(dp_um)]
        mt = f"{s['mixing_time']:.0f}" if s['mixing_time'] else "N/A"
        print(f"{dp_um:10.2f} {s['vs']:12.2e} {mt:>10} {s['final_cv']:10.3f} {s['final_mean_c']:10.4f}")

    return summary_data


if __name__ == '__main__':
    BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')
    t0 = clock.time()

    # Case 1
    run_case(0.225,
             fields_dir=os.path.join(BASE, 'data/openfoam_fields'),
             output_dir=os.path.join(BASE, 'results/case_U0.225'))

    # Case 2
    fields2 = os.path.join(BASE, 'data/openfoam_fields_case2')
    if os.path.exists(os.path.join(fields2, 'Ux.npy')):
        run_case(0.45,
                 fields_dir=fields2,
                 output_dir=os.path.join(BASE, 'results/case_U0.45'))

    print(f"\nTotal wall time: {clock.time()-t0:.1f}s")
