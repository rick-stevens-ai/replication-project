#!/usr/bin/env python
"""Generate Re=4000 vorticity snapshot figure (LI vs DNS128 vs DNS256 vs reference).

Loads cached LI rollouts isn't easy from arrays_re4000.npz alone, so this
re-rolls a single LI trajectory plus reads vorticity from baseline datasets.
"""
import os, pickle, sys
import numpy as np
import xarray as xr
import jax, jax.numpy as jnp
import gin, haiku as hk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import jax_cfd.base as cfd
import jax_cfd.ml as ml  # noqa
from jax_cfd.ml import model_builder, physics_specifications


def vort(u, v, dx):
    dv_dx = (np.roll(v, -1, 0) - np.roll(v, 1, 0)) / (2 * dx)
    du_dy = (np.roll(u, -1, 1) - np.roll(u, 1, 1)) / (2 * dx)
    return dv_dx - du_dy


def main():
    base = os.path.expanduser('~/jax-cfd-replication')
    out  = os.path.join(base, 'results_high_re', 'snapshots_re4000.png')
    ref = xr.open_dataset(os.path.join(base, 'data_re4000', 'eval_2048x2048_128x128.nc'))
    dns128 = xr.open_dataset(os.path.join(base, 'data_re4000', 'eval_128x128_128x128.nc'))
    dns256 = xr.open_dataset(os.path.join(base, 'data_re4000', 'eval_256x256_128x128.nc'))
    domain = float(ref.attrs.get('domain_size', 4*np.pi))
    nx = ref.sizes['x']
    save_dt = float(ref['time'].values[1] - ref['time'].values[0])
    grid = cfd.grids.Grid((nx, nx), domain=((0, domain), (0, domain)))
    dx = grid.step[0]

    u_ref = ref['u'].values[0].astype(np.float32)
    v_ref = ref['v'].values[0].astype(np.float32)

    with open(os.path.join(base, 'checkpoints', 'li_re4000.pkl'), 'rb') as f:
        ckpt = pickle.load(f)
    inner = ckpt['inner']
    dt = save_dt / inner
    gin.clear_config()
    gin.parse_config_file(os.path.join(base, 'code', 'li_re4000.gin'))
    ps = physics_specifications.get_physics_specs()
    mc = model_builder.get_model_cls(grid, dt, ps)
    n_T = 80  # ~5.6 sim time units
    def fwd(init):
        s = mc()
        x = s.encode(init)
        _, traj = s.trajectory(x, n_T, inner, start_with_input=True,
                               post_process_fn=s.decode)
        return traj
    tr = hk.without_apply_rng(hk.transform(fwd))
    apply = jax.jit(lambda p, x: tr.apply(p, x))
    init = (jnp.asarray(u_ref[0:1]), jnp.asarray(v_ref[0:1]))
    li_u, li_v = apply(ckpt['params'], init)
    li_u = np.asarray(li_u); li_v = np.asarray(li_v)

    times = [0, 30, 60]  # frame indices ~ t = 0, 2.1, 4.2
    fig, axes = plt.subplots(len(times), 4, figsize=(13, 3.4*len(times)))
    vmin, vmax = -8, 8
    for ti, t in enumerate(times):
        snaps = [
            ('Reference DNS-2048', vort(u_ref[t], v_ref[t], dx)),
            ('LI(128)', vort(li_u[t], li_v[t], dx)),
            ('DNS128 (dataset)',
             vort(dns128['u'].values[0, t], dns128['v'].values[0, t], dx)),
            ('DNS256 (dataset)',
             vort(dns256['u'].values[0, t], dns256['v'].values[0, t], dx)),
        ]
        for axi, (name, w) in enumerate(snaps):
            ax = axes[ti, axi]
            im = ax.imshow(w.T, origin='lower', cmap='RdBu_r',
                           vmin=vmin, vmax=vmax,
                           extent=[0, domain, 0, domain])
            ax.set_title(f'{name} @ t={t*save_dt:.1f}', fontsize=10)
            ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle('Re=4000 Kolmogorov: LI(128) vs DNS at matched and 2× resolution',
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out, dpi=150)
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
