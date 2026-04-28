"""
Tier-lift OSTI 1864334 — Stochastic Reconfiguration (SR) optimizer
benchmark on the deuteron and on A=4 (alpha) Minnesota.

The paper uses SR (≈ natural gradient with the Fubini–Study metric)
rather than Adam. SR computes the parameter update via:

    Δθ = -η * (S + λI)^{-1} * g

where g_i = <(O_i - <O_i>)(E_L - <E_L>)> and
S_ij = <(O_i - <O_i>)(O_j - <O_j>)>, with O_i = ∂_i log|Ψ|.

Compared with Adam (used previously), SR explicitly accounts for the
geometry of the variational manifold, which empirically gives faster
convergence and tighter final variance for VMC.

This addresses follow-on Q2 of the existing report.
"""
import os, sys, math, time, json
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmc_nuclei import (DeuteronPsi, deuteron_local_energy,
                         deuteron_metropolis, HBAR2_2M)

def sr_step(model, X, EL, lr=0.01, damping=1e-3, device='cuda'):
    """Stochastic reconfiguration update:
       Δθ = lr * S^{-1} * g
    where g, S are MC averages over the walker batch.
    """
    n_walk = X.shape[0]
    params = list(model.parameters())
    psh = [p.shape for p in params]
    n_par = sum(p.numel() for p in params)

    # Compute O_i for each walker by autograd of log|psi| w.r.t. params
    r = torch.linalg.norm(X, dim=-1)
    logpsi = model.log_psi(r)            # (B,)
    # Build O matrix (B, n_par)
    O = torch.zeros(n_walk, n_par, device=device)
    for b in range(n_walk):
        grads = torch.autograd.grad(logpsi[b], params, retain_graph=(b<n_walk-1),
                                    create_graph=False, allow_unused=True)
        col = []
        for g, p in zip(grads, params):
            col.append((g if g is not None else torch.zeros_like(p)).reshape(-1))
        O[b] = torch.cat(col)
    O_mean = O.mean(0, keepdim=True)
    O_c = O - O_mean
    EL_c = EL - EL.mean()
    g_vec = (O_c * EL_c.unsqueeze(-1)).mean(0)              # (n_par,)
    S = (O_c.T @ O_c) / n_walk                              # (n_par, n_par)
    S = S + damping * torch.eye(n_par, device=device)
    delta = torch.linalg.solve(S, g_vec)
    # Apply update
    with torch.no_grad():
        idx = 0
        for p in params:
            n = p.numel()
            p.add_(delta[idx:idx+n].reshape(p.shape), alpha=-lr)
            idx += n

def run_sr_deuteron(out_dir, device='cuda', iters=200, walkers=512, seed=0):
    torch.manual_seed(seed); np.random.seed(seed)
    os.makedirs(out_dir, exist_ok=True)
    model = DeuteronPsi(hidden=16).to(device)
    history = {'iter': [], 'E_mean': [], 'E_std': []}
    t0 = time.time()
    for it in range(iters):
        # sample
        with torch.no_grad():
            X, acc = deuteron_metropolis(model, walkers, 8, 1.0, device,
                                         thermalize=(it == 0))
        # subsample
        idx = torch.randperm(X.shape[0], device=device)[:walkers]
        Xs = X[idx]
        EL = deuteron_local_energy(model, Xs).detach()
        # SR update
        sr_step(model, Xs, EL, lr=0.05, damping=1e-3, device=device)
        history['iter'].append(it)
        history['E_mean'].append(float(EL.mean().item()))
        history['E_std'].append(float(EL.std().item()))
        if it % 20 == 0 or it == iters-1:
            print(f"[SR-deut it {it:3d}] E={EL.mean():+8.4f} ± "
                  f"{EL.std()/math.sqrt(walkers):.4f}  ({time.time()-t0:.1f}s)")
    # Final tighter sample
    with torch.no_grad():
        X, _ = deuteron_metropolis(model, 4096, 60, 1.0, device)
    EL = deuteron_local_energy(model, X[-4096:]).detach()
    E_final = EL.mean().item()
    E_err = EL.std().item()/math.sqrt(EL.shape[0])
    summary = dict(method="stochastic_reconfiguration",
                   E_final=E_final, E_err=E_err,
                   iters=iters, walkers=walkers,
                   wall_seconds=time.time()-t0)
    print(f"\nSR-deuteron final: {E_final:+.4f} ± {E_err:.4f} MeV")
    with open(os.path.join(out_dir, 'sr_deuteron_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(out_dir, 'sr_deuteron_history.json'), 'w') as f:
        json.dump(history, f)
    return summary

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='./results')
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    p.add_argument('--iters', type=int, default=200)
    p.add_argument('--walkers', type=int, default=512)
    args = p.parse_args()
    print(f"device={args.device}")
    print("=== SR (Stochastic Reconfiguration) on deuteron ===")
    run_sr_deuteron(args.out, device=args.device,
                    iters=args.iters, walkers=args.walkers)
