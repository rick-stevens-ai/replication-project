#!/usr/bin/env python
"""
PDEBench Wave 4 — 1D viscous Burgers complementary replication.

Complement to the existing pdebench/ REPORT.md (which covered 1D Advection):
this run targets the 1D Burgers equation, also in the PDEBench benchmark,
to provide a *different PDE* under the same protocol family (data-gen →
sanity check vs reference → small FNO baseline).

Equation: u_t + u u_x = nu u_xx, periodic on [0,1].

Approach (faithful to PDEBench's generator design but simpler/reproducible
without JAX pmap):
  - Upwind flux for the convective term, central diff for diffusion
    (same scheme PDEBench's burgers_multi_solution_Hydra.py implements)
  - Small batch of random multi-mode sinusoid initial conditions
  - Self-convergence check: fine-grid reference (nx=1024) compared
    against several coarser grids; expect 1st-order in dx for upwind.

Output: HDF5 file matching PDEBench's layout: dataset 'tensor' of shape
(B, T, X), plus 'x-coordinate' and 't-coordinate'.
"""
import os, json, time
from pathlib import Path
import numpy as np
import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/pdebench-wave4")
EVID = ROOT / "evidence"
FIGS = ROOT / "figures"
EVID.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)


def initial_condition(x, num_modes=4, rng=None):
    """Random sum of sin/cos modes, same family as PDEBench init_multi."""
    if rng is None:
        rng = np.random.default_rng(2022)
    u = np.zeros_like(x)
    for k in range(1, num_modes + 1):
        a = rng.uniform(-1.0, 1.0)
        b = rng.uniform(-1.0, 1.0)
        u += a * np.sin(2 * np.pi * k * x) + b * np.cos(2 * np.pi * k * x)
    # normalize amplitude
    u = u / max(np.max(np.abs(u)), 1e-9)
    return u


def burgers_step(u, dx, dt, nu):
    """One step of upwind + central diffusion, periodic BCs."""
    # extend with periodic ghost cells
    uL = np.roll(u, 1)   # u_{i-1}
    uR = np.roll(u, -1)  # u_{i+1}
    # upwind flux for u u_x
    # f(u) = 0.5*u^2; use Roe/upwind:
    a = 0.5 * (u + uR)  # face speed on right
    flux_R = np.where(a >= 0, 0.5 * u * u, 0.5 * uR * uR)
    a = 0.5 * (uL + u)  # face speed on left
    flux_L = np.where(a >= 0, 0.5 * uL * uL, 0.5 * u * u)
    conv = (flux_R - flux_L) / dx
    # central diffusion
    diff = nu * (uR - 2 * u + uL) / (dx * dx)
    return u + dt * (-conv + diff)


def simulate(nx, t_final=2.0, nu=1e-2, n_traj=8, save_dt=0.05, seed=2022):
    """Run n_traj independent Burgers simulations, save snapshots every save_dt."""
    x = np.linspace(0.0, 1.0, nx, endpoint=False)
    dx = x[1] - x[0]
    # CFL: dt <= dx/max|u| (advective) AND dt <= 0.5*dx^2/nu (diffusive)
    u_max = 1.0
    dt_adv = 0.5 * dx / u_max
    dt_diff = 0.4 * dx * dx / max(nu, 1e-12)
    dt = min(dt_adv, dt_diff)
    n_steps = int(np.ceil(t_final / dt))
    dt = t_final / n_steps
    save_every = max(1, int(round(save_dt / dt)))
    n_saved = n_steps // save_every + 1

    t_save = np.array([k * save_every * dt for k in range(n_saved)])
    # cap to t_final
    t_save = t_save[t_save <= t_final + 1e-12]
    n_saved = len(t_save)
    sols = np.zeros((n_traj, n_saved, nx), dtype=np.float32)

    rng = np.random.default_rng(seed)
    t0 = time.time()
    for b in range(n_traj):
        u = initial_condition(x, num_modes=4, rng=np.random.default_rng(seed + b))
        sols[b, 0, :] = u
        save_idx = 1
        for step in range(1, n_steps + 1):
            u = burgers_step(u, dx, dt, nu)
            if step % save_every == 0 and save_idx < n_saved:
                sols[b, save_idx, :] = u
                save_idx += 1
    elapsed = time.time() - t0
    return x, t_save, sols, dict(dx=dx, dt=dt, n_steps=n_steps, elapsed_s=elapsed,
                                   nu=nu, n_traj=n_traj)


def write_pdebench_hdf5(path, x, t, sols):
    """PDEBench HDF5 layout: 'tensor' (B,T,X), 'x-coordinate' (X,), 't-coordinate' (T,)."""
    with h5py.File(path, "w") as f:
        f.create_dataset("tensor", data=sols)
        f.create_dataset("x-coordinate", data=x.astype(np.float32))
        f.create_dataset("t-coordinate", data=t.astype(np.float32))


def self_convergence_test(nus=(1e-2,), grids=(64, 128, 256, 512), n_traj=4, t_final=1.0):
    """Reference: nx=1024. Compare coarse grids against down-sampled reference."""
    nx_ref = 1024
    x_ref, t_ref, sol_ref, info_ref = simulate(nx_ref, t_final=t_final, nu=nus[0],
                                                n_traj=n_traj, save_dt=0.1)
    print(f"  reference nx={nx_ref}: dt={info_ref['dt']:.2e}, {info_ref['n_steps']} steps, "
          f"{info_ref['elapsed_s']:.1f}s")
    results = {"reference_nx": nx_ref, "nu": float(nus[0]), "n_traj": n_traj,
               "t_final": t_final, "grids": []}
    for nx in grids:
        x, t, sol, info = simulate(nx, t_final=t_final, nu=nus[0],
                                    n_traj=n_traj, save_dt=0.1)
        # down-sample reference to this nx
        factor = nx_ref // nx
        ref_ds = sol_ref[:, : sol.shape[1], ::factor]
        # truncate to matching time length
        nt = min(sol.shape[1], ref_ds.shape[1])
        diff = sol[:, :nt, :] - ref_ds[:, :nt, :]
        l2 = float(np.sqrt(np.mean(diff ** 2)))
        linf = float(np.max(np.abs(diff)))
        l2_norm = float(np.sqrt(np.mean(ref_ds[:, :nt, :] ** 2)))
        rel = l2 / max(l2_norm, 1e-12)
        results["grids"].append(dict(nx=nx, dx=float(info['dx']),
                                     L2=l2, Linf=linf, relL2=rel,
                                     dt=float(info['dt']),
                                     elapsed_s=round(info['elapsed_s'], 2)))
        print(f"  nx={nx:4d}  L2={l2:.3e}  relL2={rel:.3e}  Linf={linf:.3e}  "
              f"({info['elapsed_s']:.1f}s)")
    # observed orders
    Ns = [g['nx'] for g in results['grids']]
    rels = [g['relL2'] for g in results['grids']]
    orders = []
    for i in range(1, len(Ns)):
        if rels[i] > 0 and rels[i - 1] > 0:
            o = np.log(rels[i - 1] / rels[i]) / np.log(Ns[i] / Ns[i - 1])
            orders.append(round(float(o), 3))
    results["observed_orders"] = orders
    return results, x_ref, t_ref, sol_ref


def plot_trajectory(x, t, sol, outpath):
    fig, ax = plt.subplots(figsize=(7, 4))
    times_plot = [0, len(t) // 4, len(t) // 2, 3 * len(t) // 4, len(t) - 1]
    for ti in times_plot:
        ax.plot(x, sol[0, ti, :], label=f"t={t[ti]:.2f}", lw=1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.set_title(f"1D viscous Burgers (PDEBench layout), nu={1e-2}, traj 0")
    ax.legend(fontsize=8)
    ax.grid(True, ls=":")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_convergence(conv, outpath):
    Ns = [g['nx'] for g in conv['grids']]
    rels = [g['relL2'] for g in conv['grids']]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(Ns, rels, 'bo-', lw=2, label='upwind+central, n_traj=4')
    ax.loglog(Ns, [rels[0] * (Ns[0] / N) for N in Ns], 'r--', label='O(Δx)')
    ax.loglog(Ns, [rels[0] * (Ns[0] / N) ** 2 for N in Ns], 'g--', label='O(Δx²)')
    ax.set_xlabel("nx")
    ax.set_ylabel("relative L2 vs nx=1024 reference")
    ax.set_title(f"PDEBench Burgers self-convergence (nu={conv['nu']}, t_final={conv['t_final']})")
    ax.legend()
    ax.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


if __name__ == "__main__":
    print("PDEBench Wave 4 — 1D viscous Burgers")
    print("=" * 50)

    # 1. Small generation matching PDEBench layout
    print("\n[1] Generate small Burgers dataset (n_traj=8, nx=256, nu=1e-2)")
    x, t, sol, info = simulate(nx=256, t_final=2.0, nu=1e-2, n_traj=8, save_dt=0.05)
    print(f"   dx={info['dx']:.4e}  dt={info['dt']:.2e}  steps={info['n_steps']}  "
          f"({info['elapsed_s']:.1f}s)")
    h5_path = EVID / "1D_Burgers_Sols_Nu1e-2_small.hdf5"
    write_pdebench_hdf5(h5_path, x, t, sol)
    print(f"   wrote {h5_path}  ({h5_path.stat().st_size//1024} KB)")
    plot_trajectory(x, t, sol, FIGS / "burgers_trajectory.png")
    print(f"   plotted {FIGS / 'burgers_trajectory.png'}")

    # 2. Self-convergence study
    print("\n[2] Self-convergence vs nx=1024 reference (nu=1e-2, t_final=1.0)")
    conv, x_ref, t_ref, sol_ref = self_convergence_test(
        nus=(1e-2,), grids=(64, 128, 256, 512), n_traj=4, t_final=1.0
    )
    print(f"   observed orders: {conv['observed_orders']}")
    plot_convergence(conv, FIGS / "burgers_convergence.png")
    print(f"   plotted {FIGS / 'burgers_convergence.png'}")

    # 3. Sanity: conservation of mean (no source, periodic) → mean(u) should be constant
    means = sol_ref.mean(axis=2)  # (n_traj, n_saved)
    cons_err = np.max(np.abs(means - means[:, :1]), axis=1)
    print(f"\n[3] Conservation check (max |mean(u,t) - mean(u,0)| over saved times)")
    for b in range(min(4, len(cons_err))):
        print(f"   traj {b}: {cons_err[b]:.3e}")

    summary = dict(
        equation="1D viscous Burgers, u_t + u u_x = nu u_xx, periodic [0,1]",
        scheme="upwind convective flux + central diffusion (matches PDEBench burgers_multi_solution_Hydra)",
        small_dataset=dict(path=str(h5_path), shape=list(sol.shape),
                           nu=1e-2, dx=float(info['dx']),
                           dt=float(info['dt']),
                           elapsed_s=round(info['elapsed_s'], 2)),
        self_convergence=conv,
        conservation_max_abs_drift=[float(c) for c in cons_err.tolist()],
    )
    out = EVID / "burgers_results.json"
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n  summary -> {out}")
    print("Done.")
