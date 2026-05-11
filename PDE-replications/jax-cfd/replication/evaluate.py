#!/usr/bin/env python
"""Evaluate trained LI model and DNS baselines vs the 1024^2 reference.

Computes:
  - Vorticity correlation vs reference, as a function of time.
  - Time-averaged energy spectrum.
  - Wall-clock per simulation step, per resolution / model.

Outputs everything to results.npz + per-resolution PNGs.
"""
import argparse, functools, os, pickle, time
import gin, haiku as hk, jax, jax.numpy as jnp, numpy as np, xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import jax_cfd.base as cfd
import jax_cfd.ml as ml
from jax_cfd.ml import model_builder, physics_specifications


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--ckpt', default=os.path.expanduser(
        '~/jax-cfd-replication/checkpoints/li_re1000.pkl'))
    p.add_argument('--config', default='li_config.gin')
    p.add_argument('--data-dir', default=os.path.expanduser(
        '~/jax-cfd-replication/data'))
    p.add_argument('--out', default=os.path.expanduser(
        '~/jax-cfd-replication/results'))
    p.add_argument('--samples', type=int, default=8)
    p.add_argument('--rollout-frames', type=int, default=200)
    p.add_argument('--inner', type=int, default=4)
    return p.parse_args()


def vorticity_2d(u, v, dx, dy):
    """Vorticity = dv/dx - du/dy on a periodic grid (centered finite diff)."""
    dv_dx = (jnp.roll(v, -1, 0) - jnp.roll(v, 1, 0)) / (2 * dx)
    du_dy = (jnp.roll(u, -1, 1) - jnp.roll(u, 1, 1)) / (2 * dy)
    return dv_dx - du_dy


def energy_spectrum_1d(u, v):
    """Isotropic 1D energy spectrum from a 2D velocity field."""
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
        mask = (K >= kk - 0.5) & (K < kk + 0.5)
        spec[i] = E2[mask].sum()
    return np.arange(1, n//2 + 1), spec


def correlation(a, b):
    a = a - a.mean(); b = b - b.mean()
    num = (a * b).sum()
    den = np.sqrt((a*a).sum() * (b*b).sum())
    return float(num / (den + 1e-12))


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)

    # --- Load reference (1024×1024 DNS coarsened to 64×64) and baselines ---
    ref_path = os.path.join(args.data_dir, 'eval_1024x1024_64x64.nc')
    ref_ds = xr.open_dataset(ref_path)
    print('Reference:', ref_ds.sizes)
    n_eval = min(args.samples, ref_ds.sizes['sample'])
    n_T = min(args.rollout_frames + 1, ref_ds.sizes['time'])
    u_ref = ref_ds['u'].values[:n_eval, :n_T].astype(np.float32)
    v_ref = ref_ds['v'].values[:n_eval, :n_T].astype(np.float32)

    save_dt = float(ref_ds['time'].values[1] - ref_ds['time'].values[0])
    nx = u_ref.shape[-1]  # 64
    grid = cfd.grids.Grid((nx, nx), domain=((0, 2*np.pi),)*2)
    dx = grid.step[0]
    print(f'save_dt={save_dt:.4f}, grid {nx}x{nx}, nT={n_T}, nsamp={n_eval}')

    # Load DNS baselines (already coarsened to 64×64)
    baselines = {}
    for r in [64, 128, 256]:
        path = os.path.join(args.data_dir, f'eval_{r}x{r}_64x64.nc')
        if os.path.exists(path):
            ds = xr.open_dataset(path)
            baselines[f'DNS{r}'] = (
                ds['u'].values[:n_eval, :n_T].astype(np.float32),
                ds['v'].values[:n_eval, :n_T].astype(np.float32),
            )
            print(f'Loaded DNS{r} (coarsened to 64x64)')

    # --- Load trained LI model ---
    print(f'Loading checkpoint {args.ckpt}')
    with open(args.ckpt, 'rb') as f:
        ckpt = pickle.load(f)
    params = ckpt['params']
    inner = ckpt.get('inner', args.inner)
    dt = save_dt / inner
    print(f'  inner={inner}, dt={dt:.4f}, train step={ckpt.get("step")}')

    gin.clear_config()
    gin.parse_config_file(args.config)
    physics_specs = physics_specifications.get_physics_specs()
    model_cls = model_builder.get_model_cls(grid, dt, physics_specs)

    def model_fwd(initial, n_outer):
        s = model_cls()
        x = s.encode(initial)
        _, traj = s.trajectory(x, n_outer, inner,
                                start_with_input=True,
                                post_process_fn=s.decode)
        return traj

    def predict(init):
        return model_fwd(init, n_T)
    transformed = hk.without_apply_rng(hk.transform(predict))
    apply_fn = jax.jit(lambda p, init: transformed.apply(p, init))

    # Roll out LI model
    print('Rolling out LI model on eval set...')
    t0 = time.time()
    li_u, li_v = [], []
    for i in range(n_eval):
        init = (jnp.asarray(u_ref[i, 0:1]), jnp.asarray(v_ref[i, 0:1]))
        out = apply_fn(params, init)
        u_p = np.asarray(out[0]); v_p = np.asarray(out[1])
        u_p = u_p[:n_T]; v_p = v_p[:n_T]
        li_u.append(u_p); li_v.append(v_p)
        print(f'  sample {i+1}/{n_eval}: max|u|={np.max(np.abs(u_p)):.2f}', flush=True)
    li_u = np.stack(li_u); li_v = np.stack(li_v)
    li_time = (time.time() - t0) / n_eval
    print(f'LI rollout: {li_time:.2f}s per sample of {n_T} frames')

    # --- Benchmark wall-clock times ---
    def bench(fn, init, warmup=2, runs=3):
        for _ in range(warmup):
            out = fn(init); jax.block_until_ready(out)
        t = time.time()
        for _ in range(runs):
            out = fn(init); jax.block_until_ready(out)
        return (time.time() - t) / runs

    init0 = (jnp.asarray(u_ref[0, 0:1]), jnp.asarray(v_ref[0, 0:1]))
    li_total = bench(lambda x: apply_fn(params, x), init0)
    li_per_step = li_total / (n_T * inner)
    print(f'LI(64): {li_total:.3f}s for {n_T} frames, {n_T*inner} inner steps -> {li_per_step*1e3:.3f}ms/step')

    # Benchmark DNS at 64×64 (the only resolution we can actually run from data)
    print('Benchmarking DNS64 solver...')
    gin.clear_config()
    gin.parse_config_file(os.path.expanduser(
        '~/jax-cfd-replication/jax-cfd/jax_cfd/ml/models_configs/implicit_diffusion_dns_config.gin'))
    gin.parse_config_file(os.path.expanduser(
        '~/jax-cfd-replication/jax-cfd/jax_cfd/ml/physics_configs/kolmogorov_forcing.gin'))

    ps = physics_specifications.get_physics_specs()
    mc = model_builder.get_model_cls(grid, dt, ps)
    def fwd_dns(init):
        s = mc()
        x = s.encode(init)
        _, traj = s.trajectory(x, n_T, inner,
                                start_with_input=True,
                                post_process_fn=s.decode)
        return traj
    tDNS = hk.without_apply_rng(hk.transform(fwd_dns))
    params_dns = tDNS.init(jax.random.PRNGKey(0), init0)
    apply_dns = jax.jit(lambda p, x: tDNS.apply(p, x))
    dns64_total = bench(lambda x: apply_dns(params_dns, x), init0)
    dns64_per = dns64_total / (n_T * inner)
    print(f'DNS64: {dns64_total:.3f}s for {n_T} frames -> {dns64_per*1e3:.3f}ms/step')

    # Also get the DNS64 predictions for vorticity comparison
    out_dns = apply_dns(params_dns, init0)
    # We only have 1 sample from our DNS64 run, so augment with remaining from dataset
    # Actually run DNS64 on all eval samples for fair comparison
    dns64_u, dns64_v = [], []
    for i in range(n_eval):
        init_i = (jnp.asarray(u_ref[i, 0:1]), jnp.asarray(v_ref[i, 0:1]))
        out_i = apply_dns(params_dns, init_i)
        dns64_u.append(np.asarray(out_i[0])[:n_T])
        dns64_v.append(np.asarray(out_i[1])[:n_T])
    dns64_u = np.stack(dns64_u); dns64_v = np.stack(dns64_v)

    # Estimate wall-clock for DNS at higher res using scaling:
    # paper says compute ~ R^3 (2D: R^2 grid × R factor for dt ~ 1/R)
    dns_runtimes = {64: (dns64_total, dns64_per, inner)}
    for R in [128, 256, 1024]:
        scale = (R / 64) ** 3  # cubic scaling estimate
        dns_runtimes[R] = (dns64_total * scale, dns64_per * scale, inner * R // 64)

    # --- Compute vorticity correlations + spectra ---
    print('Computing vorticity correlations + spectra...')
    def compute_metrics(u_pred, v_pred):
        corrs = []
        for t in range(u_pred.shape[1]):
            cors_t = []
            for s in range(u_pred.shape[0]):
                w_pred = np.asarray(vorticity_2d(jnp.asarray(u_pred[s, t]),
                                                  jnp.asarray(v_pred[s, t]), dx, dx))
                w_ref = np.asarray(vorticity_2d(jnp.asarray(u_ref[s, t]),
                                                 jnp.asarray(v_ref[s, t]), dx, dx))
                cors_t.append(correlation(w_pred, w_ref))
            corrs.append(np.mean(cors_t))
        s_start = min(50, u_pred.shape[1] // 4)
        E_acc = None
        for s in range(u_pred.shape[0]):
            for t in range(s_start, u_pred.shape[1]):
                k, E = energy_spectrum_1d(u_pred[s, t], v_pred[s, t])
                E_acc = E if E_acc is None else E_acc + E
        E_avg = E_acc / (u_pred.shape[0] * (u_pred.shape[1] - s_start))
        return np.array(corrs), (k, E_avg)

    results = {}
    # Reference (should be 1.0)
    print('  reference (sanity)...')
    results['Reference'] = compute_metrics(u_ref, v_ref)
    # LI model
    print('  LI(64)...')
    results['LI(64)'] = compute_metrics(li_u, li_v)
    # DNS64 from our solver
    print('  DNS64 (solver)...')
    results['DNS64-solver'] = compute_metrics(dns64_u, dns64_v)
    # Coarsened baselines from datasets
    for k_ in ['DNS64', 'DNS128', 'DNS256']:
        if k_ in baselines:
            print(f'  {k_} (dataset)...')
            results[k_] = compute_metrics(baselines[k_][0], baselines[k_][1])

    # Save raw arrays
    save_dict = {}
    for k, (corr, (kk, E)) in results.items():
        clean = k.replace('(', '').replace(')', '')
        save_dict[f'corr_{clean}'] = corr
        save_dict[f'spec_k_{clean}'] = kk
        save_dict[f'spec_{clean}'] = E
    save_dict['li_per_step_ms'] = li_per_step * 1e3
    save_dict['li_total_s'] = li_total
    save_dict['dns64_per_step_ms'] = dns64_per * 1e3
    save_dict['dns64_total_s'] = dns64_total
    save_dict['n_T'] = n_T
    save_dict['n_eval'] = n_eval
    save_dict['save_dt'] = save_dt
    np.savez(os.path.join(args.out, 'results.npz'), **save_dict)
    print(f'Wrote results.npz to {args.out}')

    # --- Plots ---
    times = np.arange(n_T) * save_dt

    # 1) Vorticity correlation
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'LI(64)': 'red', 'DNS64': 'blue', 'DNS128': 'green',
              'DNS256': 'orange', 'DNS64-solver': 'cyan'}
    for name, (corr, _) in results.items():
        if name == 'Reference': continue
        c = colors.get(name, 'gray')
        ax.plot(times, corr, label=name, lw=2, color=c)
    ax.axhline(0.95, color='gray', ls='--', alpha=0.5, label='0.95 threshold')
    ax.set_xlabel('Simulation time', fontsize=12)
    ax.set_ylabel('Vorticity correlation vs DNS-1024 reference', fontsize=12)
    ax.set_title('Kochkov et al. replication: Re=1000 Kolmogorov flow', fontsize=13)
    ax.legend(fontsize=10); ax.grid(alpha=0.3)
    ax.set_ylim([-0.1, 1.05])
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, 'vorticity_correlation.png'), dpi=150)
    plt.close()

    # 2) Energy spectrum
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, (_, (kk, E)) in results.items():
        if name == 'Reference':
            ax.loglog(kk, E, 'k-', lw=2.5, label='DNS-1024 (ref)')
        elif name in ('DNS64-solver',):
            continue
        else:
            ax.loglog(kk, E, lw=1.8, label=name, color=colors.get(name, 'gray'))
    ax.set_xlabel('Wavenumber $k$', fontsize=12)
    ax.set_ylabel('$E(k)$', fontsize=12)
    ax.set_title('Time-averaged energy spectrum', fontsize=13)
    ax.legend(fontsize=10); ax.grid(alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, 'energy_spectrum.png'), dpi=150)
    plt.close()

    # 3) Pareto: cost vs accuracy
    def thr_time(corr, threshold=0.95):
        below = np.where(corr < threshold)[0]
        return times[below[0]] if len(below) else times[-1]

    fig, ax = plt.subplots(figsize=(7, 5))
    pts = []
    # LI model
    if 'LI(64)' in results:
        pts.append(('LI(64)', li_per_step * 1e3, thr_time(results['LI(64)'][0])))
    # DNS at various resolutions (estimated timing)
    for R in [64, 128, 256, 1024]:
        k_ = f'DNS{R}'
        if k_ in results:
            _, per, _ = dns_runtimes[R]
            pts.append((k_, per * 1e3, thr_time(results[k_][0])))

    for name, x_, y_ in pts:
        c = colors.get(name, 'gray')
        ax.scatter([x_], [y_], s=100, color=c, zorder=5)
        ax.annotate(name, (x_, y_), xytext=(8, 5), textcoords='offset points', fontsize=10)
    ax.set_xscale('log')
    ax.set_xlabel('Wall-clock per solver step (ms, A100)', fontsize=12)
    ax.set_ylabel('Time before vorticity corr < 0.95 (sim-time)', fontsize=12)
    ax.set_title('Pareto: accuracy duration vs compute cost', fontsize=13)
    ax.grid(alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, 'pareto.png'), dpi=150)
    plt.close()

    # 4) Vorticity snapshot at t ≈ 5
    t_snap = min(int(5.0 / save_dt), n_T - 1)
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    snap_data = [
        ('DNS-1024 (ref)', u_ref[0, t_snap], v_ref[0, t_snap]),
        ('LI(64)', li_u[0, t_snap], li_v[0, t_snap]),
    ]
    if 'DNS64' in baselines:
        snap_data.append(('DNS64', baselines['DNS64'][0][0, t_snap], baselines['DNS64'][1][0, t_snap]))
    if 'DNS256' in baselines:
        snap_data.append(('DNS256', baselines['DNS256'][0][0, t_snap], baselines['DNS256'][1][0, t_snap]))

    vmin, vmax = -15, 15
    for i, (name, u_s, v_s) in enumerate(snap_data):
        if i >= 4: break
        w = np.asarray(vorticity_2d(jnp.asarray(u_s), jnp.asarray(v_s), dx, dx))
        axes[i].imshow(w.T, origin='lower', cmap='RdBu_r', vmin=vmin, vmax=vmax,
                       extent=[0, 2*np.pi, 0, 2*np.pi])
        axes[i].set_title(name, fontsize=11)
        axes[i].set_xlabel('x'); axes[i].set_ylabel('y')
    fig.suptitle(f'Vorticity at t={t_snap * save_dt:.1f}', fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, 'vorticity_snapshots.png'), dpi=150)
    plt.close()

    # 5) Training loss curve
    if 'losses' in ckpt:
        losses = ckpt['losses']
        steps_ = [l[0] for l in losses]
        loss_vals = [l[1] for l in losses]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.semilogy(steps_, loss_vals, lw=1, alpha=0.7)
        ax.set_xlabel('Training step'); ax.set_ylabel('MSE loss')
        ax.set_title('Training loss curve'); ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(args.out, 'training_loss.png'), dpi=150)
        plt.close()

    # --- Summary ---
    print('\n' + '='*70)
    print(f'{"Model":<12} {"per-step ms":<14} {"corr@t=2":<10} {"corr@t=5":<10} {"t_corr<0.95":<12}')
    print('-'*70)
    def at_t(corr, T):
        idx = int(min(len(corr) - 1, round(T / save_dt)))
        return corr[idx]

    if 'LI(64)' in results:
        c = results['LI(64)'][0]
        print(f'{"LI(64)":<12} {li_per_step*1e3:<14.3f} {at_t(c,2):<10.4f} {at_t(c,5):<10.4f} {thr_time(c):<12.2f}')

    for R in [64, 128, 256]:
        k_ = f'DNS{R}'
        if k_ in results:
            c = results[k_][0]
            _, per, _ = dns_runtimes.get(R, (0, 0, 0))
            print(f'{k_:<12} {per*1e3:<14.3f} {at_t(c,2):<10.4f} {at_t(c,5):<10.4f} {thr_time(c):<12.2f}')
    print('='*70)

    # Paper headline: LI(64) achieves accuracy comparable to DNS256 at a fraction of the cost
    if 'DNS256' in results and 'LI(64)' in results:
        li_t95 = thr_time(results['LI(64)'][0])
        dns256_t95 = thr_time(results['DNS256'][0])
        dns256_cost = dns_runtimes[256][1] * 1e3
        li_cost = li_per_step * 1e3
        print(f'\nHeadline comparison:')
        print(f'  LI(64) time-to-decorrelation: {li_t95:.2f}')
        print(f'  DNS256 time-to-decorrelation: {dns256_t95:.2f}')
        print(f'  LI cost per step: {li_cost:.3f}ms  vs  DNS256 est: {dns256_cost:.3f}ms')
        if dns256_cost > 0:
            print(f'  Speedup: ~{dns256_cost / li_cost:.1f}x')


if __name__ == '__main__':
    main()
