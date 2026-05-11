#!/usr/bin/env python
"""Train a Learned-Interpolation (LI) Navier–Stokes model on 64x64 Kolmogorov flow.

Replication of Kochkov et al., PNAS 2021, jax-cfd LI model.

Training data: coarsened (64x64) trajectories from 1024^2 DNS reference
(downloaded from gs://gresearch/jax-cfd/public_eval_datasets/kolmogorov_re_1000).

Loss: MSE between predicted and target velocities over an unrolled rollout.
"""
import argparse, functools, os, pickle, time
import gin, haiku as hk, jax, jax.numpy as jnp, numpy as np, optax, xarray as xr

import jax_cfd.base as cfd  # noqa: F401
import jax_cfd.ml as ml  # noqa: F401
from jax_cfd.ml import model_builder, physics_specifications


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--config', default='li_config.gin')
    p.add_argument('--data', default=os.path.expanduser(
        '~/jax-cfd-replication/data/eval_1024x1024_64x64.nc'))
    p.add_argument('--out', default=os.path.expanduser(
        '~/jax-cfd-replication/checkpoints/li_re1000.pkl'))
    p.add_argument('--steps', type=int, default=4000)
    p.add_argument('--batch', type=int, default=8)
    p.add_argument('--unroll', type=int, default=32,
                   help='final rollout length (in coarse model steps) per training example')
    p.add_argument('--curriculum', type=str, default='1:0,2:200,4:600,8:1500,16:2500',
                   help='colon-separated unroll:start-step pairs')
    p.add_argument('--inner', type=int, default=1,
                   help='inner steps per saved frame; coarse model uses dt=save_dt/inner')
    p.add_argument('--lr', type=float, default=1e-3)
    p.add_argument('--warmup', type=int, default=200)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--log-every', type=int, default=20)
    return p.parse_args()


def main():
    args = parse_args()
    print('JAX devices:', jax.devices())
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # --- Load coarsened DNS data --------------------------------------------
    ds = xr.open_dataset(args.data)
    print('Dataset:', ds.sizes, 'sample x time x grid')
    u = ds['u'].values.astype(np.float32)  # (sample, time, x, y)
    v = ds['v'].values.astype(np.float32)
    n_samples, n_times, nx, ny = u.shape
    save_dt = float(ds['time'].values[1] - ds['time'].values[0])
    print(f'save_dt={save_dt:.4f}, grid {nx}x{ny}, samples={n_samples}, times={n_times}')

    # --- Configure model with gin ------------------------------------------
    gin.parse_config_file(args.config)
    grid = cfd.grids.Grid((nx, ny), domain=((0, 2*np.pi), (0, 2*np.pi)))
    dt = save_dt / args.inner
    physics_specs = physics_specifications.get_physics_specs()
    model_cls = model_builder.get_model_cls(grid, dt, physics_specs)

    def model_fwd(initial, n_outer):
        solver = model_cls()
        encoded = solver.encode(initial)
        _, traj = solver.trajectory(encoded, n_outer, args.inner,
                                    start_with_input=True,
                                    post_process_fn=solver.decode)
        return traj  # tuple of (T, nx, ny) arrays

    # The model takes initial as a *trajectory* with leading time axis (length 1)
    # because aligned_array_encoder slices time index -1.
    def predict_traj(initial_uv, n_outer):
        # initial_uv: (u0, v0) each (1, nx, ny)
        return model_fwd(initial_uv, n_outer)

    # Build a transformed apply for each curriculum unroll (sharing params).
    def make_transformed(n_outer):
        def fn(init):
            return predict_traj(init, n_outer + 1)
        return hk.without_apply_rng(hk.transform(fn))

    transformed_init = make_transformed(1)  # for params init only
    transformed = transformed_init  # current rollout

    # Init params
    rng = jax.random.PRNGKey(args.seed)
    sample_init = (jnp.asarray(u[0, 0:1]), jnp.asarray(v[0, 0:1]))
    print('Initializing model params...')
    t0 = time.time()
    params = transformed_init.init(rng, sample_init)
    n_params = sum(int(np.prod(p.shape)) for p in jax.tree_util.tree_leaves(params))
    print(f'Params: {n_params:,} ({time.time()-t0:.1f}s)')

    # --- Optimizer ---------------------------------------------------------
    warmup = min(args.warmup, max(1, args.steps // 5))
    schedule = optax.warmup_cosine_decay_schedule(
        init_value=0.0, peak_value=args.lr,
        warmup_steps=warmup, decay_steps=args.steps, end_value=args.lr*0.05)
    opt = optax.chain(optax.clip_by_global_norm(1.0), optax.adam(schedule))
    opt_state = opt.init(params)

    # --- Training step -----------------------------------------------------
    def make_loss_and_step(n_unroll):
        tr = make_transformed(n_unroll)
        def loss_fn(params, batch):
            (u0_b, v0_b), (u_tgt, v_tgt) = batch
            def single(u0_i, v0_i):
                init = (u0_i[None], v0_i[None])
                return tr.apply(params, init)
            u_pred, v_pred = jax.vmap(single)(u0_b, v0_b)
            T = u_tgt.shape[1]
            u_pred = u_pred[:, :T]; v_pred = v_pred[:, :T]
            err = (u_pred - u_tgt)**2 + (v_pred - v_tgt)**2
            # exponentially-decaying weight to focus on early frames first
            return err.mean()

        @jax.jit
        def train_step(params, opt_state, batch):
            loss, grads = jax.value_and_grad(loss_fn)(params, batch)
            gn = optax.global_norm(grads)
            # NaN-safe: zero out updates if any NaN
            is_finite = jnp.isfinite(loss) & jnp.isfinite(gn)
            grads = jax.tree_util.tree_map(
                lambda g: jnp.where(is_finite, g, jnp.zeros_like(g)), grads)
            updates, opt_state = opt.update(grads, opt_state, params)
            params_new = optax.apply_updates(params, updates)
            params = jax.tree_util.tree_map(
                lambda pn, p: jnp.where(is_finite, pn, p), params_new, params)
            return params, opt_state, loss, gn
        return train_step

    # Pre-compile train_step for each curriculum unroll length
    curric_pairs = []
    for token in args.curriculum.split(','):
        u_str, s_str = token.split(':')
        curric_pairs.append((int(u_str), int(s_str)))
    curric_pairs.sort(key=lambda x: x[1])
    print('Curriculum:', curric_pairs)
    train_steps_by_unroll = {u: make_loss_and_step(u) for u, _ in curric_pairs}

    # --- Data sampler ------------------------------------------------------
    rng_np = np.random.default_rng(args.seed)

    def sample_batch(n_unroll):
        T = n_unroll + 1
        max_t = n_times - T
        idx_s = rng_np.integers(0, n_samples, size=args.batch)
        idx_t = rng_np.integers(0, max_t, size=args.batch)
        u_init = np.stack([u[s, t]   for s, t in zip(idx_s, idx_t)])
        v_init = np.stack([v[s, t]   for s, t in zip(idx_s, idx_t)])
        u_tgt  = np.stack([u[s, t:t+T] for s, t in zip(idx_s, idx_t)])
        v_tgt  = np.stack([v[s, t:t+T] for s, t in zip(idx_s, idx_t)])
        return ((jnp.asarray(u_init), jnp.asarray(v_init)),
                (jnp.asarray(u_tgt),  jnp.asarray(v_tgt)))

    # --- Train -------------------------------------------------------------
    losses = []
    print('Starting training...')
    t_start = time.time()
    best_loss = float('inf')
    cur_unroll = curric_pairs[0][0]
    train_step = train_steps_by_unroll[cur_unroll]
    nan_streak = 0
    for step in range(1, args.steps + 1):
        # advance curriculum if next pair starts here
        for u_, s_ in curric_pairs:
            if step == s_ + 1 or (step == 1 and s_ == 0):
                if cur_unroll != u_:
                    cur_unroll = u_
                    train_step = train_steps_by_unroll[cur_unroll]
                    print(f'[step {step}] curriculum -> unroll={cur_unroll}')
        batch = sample_batch(cur_unroll)
        params, opt_state, loss, gn = train_step(params, opt_state, batch)
        loss = float(loss); gn = float(gn)
        losses.append((step, loss, gn))
        if not (np.isfinite(loss) and np.isfinite(gn)):
            nan_streak += 1
        else:
            nan_streak = 0
        if step % args.log_every == 0 or step == 1:
            elapsed = time.time() - t_start
            rate = step / max(elapsed, 1e-6)
            eta = (args.steps - step) / max(rate, 1e-6) / 60
            print(f'step {step:5d}/{args.steps}  unroll={cur_unroll}  loss={loss:.4e}  |grad|={gn:.2e}  '
                  f'{rate:.2f} steps/s  ETA {eta:.1f}min', flush=True)
        if nan_streak > 50:
            print('Aborting: too many consecutive NaN steps')
            break
        if loss < best_loss:
            best_loss = loss
        # periodic checkpoint
        if step % 500 == 0 or step == args.steps:
            ckpt = dict(params=params, step=step, losses=losses,
                        config_str=gin.config_str(), dt=dt, inner=args.inner,
                        save_dt=save_dt, grid_shape=(nx, ny))
            with open(args.out, 'wb') as f:
                pickle.dump(ckpt, f)
    print(f'Training done in {(time.time()-t_start)/60:.1f}min. Best loss {best_loss:.4e}')
    print(f'Checkpoint -> {args.out}')


if __name__ == '__main__':
    main()
