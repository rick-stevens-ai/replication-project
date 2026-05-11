#!/usr/bin/env python
"""Generic evaluation: roll out trained LI model, compare to DNS baselines.

Computes vorticity correlation vs reference, time-averaged 1D energy spectrum,
and (for the decaying case) total kinetic energy over time.

Saves results to <out>/results.json + <out>/<tag>.npz and PNG figures.
"""
import argparse, os, pickle, time, json
import gin, haiku as hk, jax, jax.numpy as jnp, numpy as np, xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import jax_cfd.base as cfd
import jax_cfd.ml as ml  # noqa
from jax_cfd.ml import model_builder, physics_specifications


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--ckpt', required=True)
    p.add_argument('--config', required=True)
    p.add_argument('--ref-data', required=True,
                   help='Reference dataset (highest-res available, coarsened to LI grid)')
    p.add_argument('--baselines', nargs='*', default=[],
                   help='Pairs name=path for baseline coarsened DNS datasets')
    p.add_argument('--out', required=True)
    p.add_argument('--samples', type=int, default=4)
    p.add_argument('--frames', type=int, default=200)
    p.add_argument('--inner', type=int, default=4)
    p.add_argument('--tag', default='run')
    p.add_argument('--energy-curve', action='store_true',
                   help='Also compute total KE(t) (for decaying turbulence)')
    return p.parse_args()


def vorticity_2d(u, v, dx, dy):
    dv_dx = (jnp.roll(v, -1, 0) - jnp.roll(v, 1, 0)) / (2 * dx)
    du_dy = (jnp.roll(u, -1, 1) - jnp.roll(u, 1, 1)) / (2 * dy)
    return dv_dx - du_dy


def energy_spectrum_1d(u, v):
    n = u.shape[-1]
    uh = np.fft.fft2(u) / (n * n)
    vh = np.fft.fft2(v) / (n * n)
    E2 = 0.5 * (np.abs(uh)**2 + np.abs(vh)**2)
    kx = np.fft.fftfreq(n, d=1.0/n)
    ky = np.fft.fftfreq(n, d=1.0/n)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    K = np.sqrt(KX**2 + KY**2)
    kbins = np.arange(0.5, n//2 + 0.5)
    spec = np.zeros(len(kbins))
    for i, kk in enumerate(kbins):
        m = (K >= kk - 0.5) & (K < kk + 0.5)
        spec[i] = E2[m].sum()
    return np.arange(1, n//2 + 1), spec


def correlation(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float((a*b).sum() / (np.sqrt((a*a).sum() * (b*b).sum()) + 1e-12))


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)

    ref = xr.open_dataset(args.ref_data)
    n_eval = min(args.samples, ref.sizes['sample'])
    n_T = min(args.frames + 1, ref.sizes['time'])
    u_ref = ref['u'].values[:n_eval, :n_T].astype(np.float32)
    v_ref = ref['v'].values[:n_eval, :n_T].astype(np.float32)
    save_dt = float(ref['time'].values[1] - ref['time'].values[0])
    nx = u_ref.shape[-1]
    domain = float(ref.attrs.get('domain_size', 2*np.pi))
    grid = cfd.grids.Grid((nx, nx), domain=((0, domain), (0, domain)))
    dx = grid.step[0]
    print(f'Ref: {n_eval}x{n_T}x{nx}^2  domain={domain:.3f}  dt={save_dt:.4f}', flush=True)

    baselines = {}
    for spec in args.baselines:
        if '=' not in spec: continue
        name, path = spec.split('=', 1)
        if not os.path.exists(path):
            print(f'  baseline {name}: missing'); continue
        ds = xr.open_dataset(path)
        baselines[name] = (
            ds['u'].values[:n_eval, :n_T].astype(np.float32),
            ds['v'].values[:n_eval, :n_T].astype(np.float32),
        )
        print(f'  baseline {name}: {ds.sizes}', flush=True)

    # Load checkpoint
    with open(args.ckpt, 'rb') as f:
        ckpt = pickle.load(f)
    params = ckpt['params']
    inner = ckpt.get('inner', args.inner)
    dt = save_dt / inner
    print(f'  ckpt step={ckpt.get("step")} inner={inner} dt={dt:.4f}', flush=True)

    gin.clear_config()
    gin.parse_config_file(args.config)
    physics_specs = physics_specifications.get_physics_specs()
    model_cls = model_builder.get_model_cls(grid, dt, physics_specs)

    def fwd_li(initial, n_outer):
        s = model_cls()
        x = s.encode(initial)
        _, traj = s.trajectory(x, n_outer, inner,
                               start_with_input=True,
                               post_process_fn=s.decode)
        return traj
    def li_predict(init):
        return fwd_li(init, n_T)
    li_t = hk.without_apply_rng(hk.transform(li_predict))
    apply_li = jax.jit(lambda p, x: li_t.apply(p, x))

    print('Rolling out LI...', flush=True)
    t0 = time.time()
    li_u, li_v = [], []
    for i in range(n_eval):
        init = (jnp.asarray(u_ref[i, 0:1]), jnp.asarray(v_ref[i, 0:1]))
        out = apply_li(params, init)
        li_u.append(np.asarray(out[0])[:n_T])
        li_v.append(np.asarray(out[1])[:n_T])
        print(f'  LI sample {i+1}/{n_eval} max|u|={np.max(np.abs(li_u[-1])):.2f}', flush=True)
    li_u = np.stack(li_u); li_v = np.stack(li_v)

    # Bench LI
    init0 = (jnp.asarray(u_ref[0, 0:1]), jnp.asarray(v_ref[0, 0:1]))
    def bench(fn, x, warm=2, runs=3):
        for _ in range(warm):
            jax.block_until_ready(fn(x))
        t = time.time()
        for _ in range(runs):
            jax.block_until_ready(fn(x))
        return (time.time() - t) / runs
    li_total = bench(lambda x: apply_li(params, x), init0)
    li_per_step = li_total / (n_T * inner)
    print(f'LI: {li_per_step*1e3:.3f} ms/step', flush=True)

    # Run a coarse-grid DNS at the LI resolution as solver baseline
    gin.clear_config()
    # Reuse the LI gin config but disable the learned interpolation —
    # we instead build a DNS config from scratch.
    import jax_cfd.ml.advections as adv_mod
    import jax_cfd.ml.interpolations as interp_mod
    import jax_cfd.ml.encoders as enc_mod
    import jax_cfd.ml.decoders as dec_mod
    import jax_cfd.ml.equations as eq_mod
    import jax_cfd.ml.diffusions as diff_mod
    import jax_cfd.ml.pressures as pr_mod
    # We hardwire: lax-wendroff TVD + linear, fast-diag pressure & diffusion
    gin.parse_config_file(args.config)  # for physics specs
    # Just override the LI to be the lax-wendroff scheme via gin overrides
    gin.parse_config([
        'C_INTERPOLATION_MODULE = @interpolations.transformed',
        'transformed.base_interpolation_module = @interpolations.lax_wendroff',
        'transformed.transformation = @interpolations.tvd_limiter_transformation',
    ])
    ps = physics_specifications.get_physics_specs()
    mc = model_builder.get_model_cls(grid, dt, ps)
    def fwd_dns(init):
        s = mc()
        x = s.encode(init)
        _, traj = s.trajectory(x, n_T, inner,
                               start_with_input=True,
                               post_process_fn=s.decode)
        return traj
    dns_t = hk.without_apply_rng(hk.transform(fwd_dns))
    params_dns = dns_t.init(jax.random.PRNGKey(0), init0)
    apply_dns = jax.jit(lambda p, x: dns_t.apply(p, x))
    dns_total = bench(lambda x: apply_dns(params_dns, x), init0)
    dns_per_step = dns_total / (n_T * inner)
    print(f'DNS{nx} (solver): {dns_per_step*1e3:.3f} ms/step', flush=True)

    dns_u, dns_v = [], []
    for i in range(n_eval):
        init = (jnp.asarray(u_ref[i, 0:1]), jnp.asarray(v_ref[i, 0:1]))
        out = apply_dns(params_dns, init)
        dns_u.append(np.asarray(out[0])[:n_T])
        dns_v.append(np.asarray(out[1])[:n_T])
    dns_u = np.stack(dns_u); dns_v = np.stack(dns_v)

    # Compute metrics
    print('Computing metrics...', flush=True)
    def compute(u_p, v_p, name):
        corrs, ke = [], []
        for t in range(u_p.shape[1]):
            cors = []
            for s in range(u_p.shape[0]):
                w_p = np.asarray(vorticity_2d(jnp.asarray(u_p[s, t]),
                                              jnp.asarray(v_p[s, t]), dx, dx))
                w_r = np.asarray(vorticity_2d(jnp.asarray(u_ref[s, t]),
                                              jnp.asarray(v_ref[s, t]), dx, dx))
                cors.append(correlation(w_p, w_r))
            corrs.append(np.mean(cors))
            ke.append(0.5 * float(np.mean(u_p[:, t]**2 + v_p[:, t]**2)))
        # Time-averaged spectrum from late times
        s_start = min(50, u_p.shape[1] // 4)
        E_acc = None; cnt = 0
        for s in range(u_p.shape[0]):
            for t in range(s_start, u_p.shape[1]):
                _, E = energy_spectrum_1d(u_p[s, t], v_p[s, t])
                E_acc = E if E_acc is None else E_acc + E; cnt += 1
        E_avg = E_acc / cnt
        # Early-time spectrum (decaying turb wants this)
        E_early = None; cnt2 = 0
        for s in range(u_p.shape[0]):
            for t in range(min(5, u_p.shape[1])):
                _, E = energy_spectrum_1d(u_p[s, t], v_p[s, t])
                E_early = E if E_early is None else E_early + E; cnt2 += 1
        E_early = E_early / cnt2
        k_axis = np.arange(1, u_p.shape[-1]//2 + 1)
        return dict(corr=np.array(corrs), ke=np.array(ke),
                    spec_k=k_axis, spec=E_avg, spec_early=E_early)

    results = {'reference': compute(u_ref, v_ref, 'ref'),
               'LI': compute(li_u, li_v, 'LI'),
               f'DNS{nx}_solver': compute(dns_u, dns_v, f'DNS{nx}')}
    for name, (uu, vv) in baselines.items():
        results[name] = compute(uu, vv, name)

    # Summary
    times = np.arange(n_T) * save_dt
    def at_t(c, T):
        idx = int(min(len(c)-1, round(T/save_dt))); return float(c[idx])
    def thr_t(c, thr=0.95):
        below = np.where(c < thr)[0]
        return float(times[below[0]]) if len(below) else float(times[-1])

    summary = {'tag': args.tag, 'n_eval': n_eval, 'n_T': n_T, 'save_dt': save_dt,
               'grid': nx, 'domain': domain,
               'li_per_step_ms': li_per_step * 1e3,
               'dns_solver_per_step_ms': dns_per_step * 1e3,
               'metrics': {}}
    print(f'\n{args.tag} summary:')
    print(f'{"Model":<22} {"corr@t=2":<10} {"corr@t=5":<10} {"t<0.95":<10}')
    print('-'*60)
    for name, r in results.items():
        if name == 'reference': continue
        c = r['corr']
        row = dict(corr_t2=at_t(c, 2.0), corr_t5=at_t(c, 5.0), t_dec=thr_t(c))
        summary['metrics'][name] = row
        print(f'{name:<22} {row["corr_t2"]:<10.4f} {row["corr_t5"]:<10.4f} {row["t_dec"]:<10.3f}')

    with open(os.path.join(args.out, f'results_{args.tag}.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Save raw
    save = {}
    for name, r in results.items():
        for k, v in r.items():
            clean = name.replace('(', '').replace(')', '')
            save[f'{clean}_{k}'] = v
    save['times'] = times
    save['li_per_step_ms'] = li_per_step * 1e3
    np.savez(os.path.join(args.out, f'arrays_{args.tag}.npz'), **save)

    # Plots
    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = {'LI': 'red', f'DNS{nx}_solver': 'cyan',
            'DNS128': 'blue', 'DNS256': 'green', 'DNS512': 'orange',
            'DNS1024': 'purple', 'DNS2048': 'black',
            'DNS64': 'blue', 'reference': 'k'}
    for name, r in results.items():
        if name == 'reference': continue
        ax.plot(times, r['corr'], label=name, lw=2, color=cmap.get(name, 'gray'))
    ax.axhline(0.95, ls='--', color='gray', alpha=0.5)
    ax.set(xlabel='Simulation time', ylabel='Vorticity correlation vs reference',
           ylim=[-0.1, 1.05], title=f'{args.tag}: vorticity correlation')
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, f'corr_{args.tag}.png'), dpi=150)
    plt.close()

    fig, ax = plt.subplots(figsize=(7, 5))
    for name, r in results.items():
        if name == 'reference':
            ax.loglog(r['spec_k'], r['spec'], 'k-', lw=2.5, label='reference')
        else:
            ax.loglog(r['spec_k'], r['spec'], lw=1.5,
                      label=name, color=cmap.get(name, 'gray'))
    ax.set(xlabel='k', ylabel='E(k)', title=f'{args.tag}: time-avg energy spectrum')
    ax.legend(fontsize=9); ax.grid(alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, f'spec_{args.tag}.png'), dpi=150)
    plt.close()

    if args.energy_curve:
        fig, ax = plt.subplots(figsize=(7, 5))
        for name, r in results.items():
            if name == 'reference':
                ax.semilogy(times, r['ke'], 'k-', lw=2.5, label='reference')
            else:
                ax.semilogy(times, r['ke'], lw=1.5, label=name,
                            color=cmap.get(name, 'gray'))
        ax.set(xlabel='Time', ylabel='Total KE',
               title=f'{args.tag}: kinetic energy decay')
        ax.legend(fontsize=9); ax.grid(alpha=0.3, which='both')
        fig.tight_layout()
        fig.savefig(os.path.join(args.out, f'ke_{args.tag}.png'), dpi=150)
        plt.close()

    print(f'Wrote outputs to {args.out}')


if __name__ == '__main__':
    main()
