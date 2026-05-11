#!/usr/bin/env python
"""Generate Re=7000 Kolmogorov reference DNS at 1024^2, coarsen to 128^2,
save in same .nc layout as the public datasets.

Mirrors the Re=4000 jax-cfd public-dataset config, but with viscosity
scaled to ~5/7 * 5e-4 = 2.86e-4 (kinematic viscosity scales like 1/Re).
"""
import os, time, sys, json
import numpy as np
import jax, jax.numpy as jnp
import jax_cfd.base as cfd
import jax_cfd.base.forcings as bforcings
import jax_cfd.spectral as spectral
import xarray as xr


def main(out_path, n_samples=8, n_save=300, sim_grid=1024, save_grid=128,
         viscosity=2.86e-4, seed=0):
    domain = 4 * np.pi  # match Re=4000 setup
    sim_grid_obj = cfd.grids.Grid((sim_grid, sim_grid),
                                  domain=((0, domain), (0, domain)))
    save_grid_obj = cfd.grids.Grid((save_grid, save_grid),
                                   domain=((0, domain), (0, domain)))
    max_velocity = 7.0
    cfl = 0.5
    save_dt = 0.07012484
    dt = cfd.equations.stable_time_step(max_velocity, cfl, viscosity, sim_grid_obj)
    inner = max(1, int(np.ceil(save_dt / dt)))
    dt = save_dt / inner
    print(f'sim_grid={sim_grid} save_grid={save_grid} domain={domain:.4f} '
          f'nu={viscosity:.4e} dt={dt:.4e} inner={inner}', flush=True)

    forcing_fn = lambda g: bforcings.kolmogorov_forcing(g, scale=0.5, k=2)
    # Linear damping (drag) — stronger than the Re=4000 dataset's 0.05 to
    # keep the under-resolved 512² flow numerically bounded.
    drag = 0.1
    eq = spectral.equations.NavierStokes2D(
        viscosity, sim_grid_obj, drag=drag,
        smooth=True, forcing_fn=forcing_fn)
    step_fn = jax.jit(spectral.time_stepping.crank_nicolson_rk4(eq, dt))

    def make_run_steps(n):
        @jax.jit
        def f(vh):
            def body(carry, _):
                return step_fn(carry), None
            return jax.lax.scan(body, vh, None, length=int(n))[0]
        return f
    run_inner = make_run_steps(inner)

    # Coarsen by spectral truncation then ifft
    fact = sim_grid // save_grid
    @jax.jit
    def velocity_from_vort_coarse(vh):
        # vh is rfft of vorticity at sim grid (sim_grid, sim_grid//2+1)
        # convert vorticity → velocity in spectral, then ifft on coarse grid
        kx, ky = sim_grid_obj.rfft_mesh()
        k2 = kx**2 + ky**2
        k2 = jnp.where(k2 == 0, 1.0, k2)
        psi_h = vh / k2
        psi_h = psi_h.at[0, 0].set(0)
        # u =  d psi/dy, v = -d psi/dx
        uh = 1j * ky * psi_h
        vhh = -1j * kx * psi_h
        # Spectral truncation to coarse
        # rfft layout: keep first save_grid//2+1 in y axis, and split kx
        # Simplest: take real-space ifft on full grid then average
        u_full = jnp.fft.irfftn(uh, s=(sim_grid, sim_grid))
        v_full = jnp.fft.irfftn(vhh, s=(sim_grid, sim_grid))
        # Block-average to coarse grid (pointwise downsampling could alias;
        # spectral truncation is better but messier with rfft layout)
        u_c = u_full.reshape(save_grid, fact, save_grid, fact).mean(axis=(1, 3))
        v_c = v_full.reshape(save_grid, fact, save_grid, fact).mean(axis=(1, 3))
        return u_c, v_c

    # Run warmup as a chunk of inner-sized scans for jit reuse + memory limits.
    n_warmup_chunks_total = 0
    rng = jax.random.PRNGKey(seed)
    samples_u = np.zeros((n_samples, n_save, save_grid, save_grid), np.float32)
    samples_v = np.zeros((n_samples, n_save, save_grid, save_grid), np.float32)
    warmup_time = 30.0  # let drag equilibrate flow
    n_warmup_save = int(warmup_time / save_dt)
    print(f'warmup save_steps per sample: {n_warmup_save} (each {inner} solver steps)', flush=True)
    t_start = time.time()
    for s_idx in range(n_samples):
        rng, sub = jax.random.split(rng)
        v0 = cfd.initial_conditions.filtered_velocity_field(
            sub, sim_grid_obj, max_velocity, peak_wavenumber=4)
        # initial vorticity in rfft space
        uh0 = jnp.fft.rfftn(v0[0].data)
        vh0 = jnp.fft.rfftn(v0[1].data)
        kx, ky = sim_grid_obj.rfft_mesh()
        vort_h = 1j * (kx * vh0 - ky * uh0)
        # Warmup (chunked)
        for _ in range(n_warmup_save):
            vort_h = run_inner(vort_h)
        vort_h.block_until_ready()
        for t in range(n_save):
            u_c, v_c = velocity_from_vort_coarse(vort_h)
            samples_u[s_idx, t] = np.asarray(u_c)
            samples_v[s_idx, t] = np.asarray(v_c)
            if t < n_save - 1:
                vort_h = run_inner(vort_h)
        elapsed = time.time() - t_start
        eta = elapsed / (s_idx + 1) * (n_samples - s_idx - 1) / 60
        print(f'sample {s_idx+1}/{n_samples} done '
              f'(max|u|={np.max(np.abs(samples_u[s_idx])):.2f}) '
              f'elapsed={elapsed/60:.1f}m ETA={eta:.1f}m', flush=True)

    # Save xarray
    times = np.arange(n_save) * save_dt
    coord_x = (np.arange(save_grid) + 0.5) * (domain / save_grid)
    ds = xr.Dataset(
        data_vars=dict(
            u=(('sample', 'time', 'x', 'y'), samples_u),
            v=(('sample', 'time', 'x', 'y'), samples_v),
        ),
        coords=dict(sample=np.arange(n_samples), time=times,
                    x=coord_x, y=coord_x),
        attrs=dict(
            domain_size=float(domain),
            domain_size_multiple=2,
            simulation_grid_size=int(sim_grid),
            save_grid_size=int(save_grid),
            viscosity=float(viscosity),
            forcing='kolmogorov_k2_scale0.5_lin-0.05',
            note='Generated in-house for Re=7000 (no public dataset available)',
        ))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ds.to_netcdf(out_path)
    print(f'Wrote {out_path}', flush=True)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--samples', type=int, default=8)
    p.add_argument('--n-save', type=int, default=300)
    p.add_argument('--sim-grid', type=int, default=1024)
    p.add_argument('--save-grid', type=int, default=128)
    p.add_argument('--viscosity', type=float, default=2.857e-4)
    p.add_argument('--seed', type=int, default=0)
    a = p.parse_args()
    main(a.out, a.samples, a.n_save, a.sim_grid, a.save_grid, a.viscosity, a.seed)
