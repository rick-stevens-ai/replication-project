#!/usr/bin/env python3
"""
Complete replication of Chen, Yu & Lai (2006).
Runs both cases with full field saving for all validation figures.
"""
import numpy as np
import json
import os
import sys
import time as clock

# Import from the solver module
sys.path.insert(0, os.path.dirname(__file__))
from particle_transport_fast import (
    particle_properties, lai_nazaroff_vd, solve_transport_vectorized,
    load_openfoam_fields, simple_flow_field, extract_profiles,
    NX, NY, NZ, LX, LY, LZ, NU_AIR
)

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')


def run_case(u_inlet, fields_dir=None):
    """Run a complete case with full field saving."""
    case_name = f'case_U{u_inlet}'
    output_dir = os.path.join(BASE, 'results', case_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"CASE: U_inlet = {u_inlet} m/s")
    print(f"{'='*70}")

    # Load flow field
    if fields_dir and os.path.exists(os.path.join(fields_dir, 'Ux.npy')):
        print("Using OpenFOAM flow field")
        U, V, W, nut, u_star, xc, yc, zc = load_openfoam_fields(fields_dir)
    else:
        print("WARNING: Using analytical flow field")
        U, V, W, nut, u_star, xc, yc, zc = simple_flow_field(NX, NY, NZ, u_inlet)

    dx = xc[1] - xc[0]

    # CFL time step
    u_max = max(np.max(np.abs(U)), np.max(np.abs(V)), np.max(np.abs(W)), 0.01)
    D_max = np.max(nut) + NU_AIR
    dt_conv = 0.3 * min(dx, LY/NY, LZ/NZ) / u_max
    dt_diff = 0.15 * min(dx, LY/NY, LZ/NZ)**2 / D_max
    dt = min(dt_conv, dt_diff, 0.05)
    print(f"dt = {dt:.4f}s", flush=True)

    sizes_um = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    # Save times matching paper figures
    save_times = [60, 180, 300, 600, 900, 1200, 1500, 1800]

    all_results = {}
    summary_data = {}

    for dp_um in sizes_um:
        pp = particle_properties(dp_um)
        print(f"\n--- dp = {dp_um} μm ---", flush=True)

        results = solve_transport_vectorized(
            U, V, W, nut, u_star, xc, yc, zc,
            pp, dt=dt, t_end=1800, save_times=save_times
        )

        all_results[dp_um] = results

        # Save concentration fields at key times
        size_dir = os.path.join(output_dir, f'dp_{dp_um}')
        os.makedirs(size_dir, exist_ok=True)

        for t_save, C_field in results['fields'].items():
            np.save(os.path.join(size_dir, f'C_t{int(t_save)}.npy'), C_field)

        # Save final profiles
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

    # Save CV time series
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

    return all_results, summary_data


if __name__ == '__main__':
    t0 = clock.time()

    # Case 1: U = 0.225 m/s
    fields_dir_1 = os.path.join(BASE, 'data/openfoam_fields')
    run_case(0.225, fields_dir=fields_dir_1)

    # Case 2: U = 0.45 m/s
    fields_dir_2 = os.path.join(BASE, 'data/openfoam_fields_case2')
    if os.path.exists(os.path.join(fields_dir_2, 'Ux.npy')):
        run_case(0.45, fields_dir=fields_dir_2)
    else:
        print("\n\nCase 2 (U=0.45): No OpenFOAM fields found. Skipping.")

    print(f"\nTotal wall time: {clock.time()-t0:.1f}s")
