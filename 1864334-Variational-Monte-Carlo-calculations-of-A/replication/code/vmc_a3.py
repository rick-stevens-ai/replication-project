"""
Tier-lift OSTI 1864334 — A=3 (³H, ³He) NN-VMC extension with the
Minnesota central potential (even-state average, same convention as the
He-4 run in vmc_nuclei.py).

The ground-state of ³H/³He is dominantly L=0, S=1/2, T=1/2 with a
spatially symmetric (totally-symmetric) component of weight ~89-90 %
(plus ~9 % S' and small D, T').  In this central-potential reduction we
keep ONLY the S spatial-symmetric piece — same approximation as our A=4
run — and treat the spin-isospin antisymmetrising factor analytically.

Coulomb is added for ³He (Z=2 → 1 pp pair) but not ³H.

Reference values (Minnesota, central only, Faddeev):
   ³H : E = -8.38 MeV
   ³He: E = -7.74 MeV (with Coulomb)
Experiment:
   ³H : -8.482 MeV
   ³He: -7.718 MeV
"""
import argparse, math, os, time, json
import numpy as np
import torch
import torch.nn as nn

# Re-use constants and potential from vmc_nuclei
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vmc_nuclei import (HBARC, MN, HBAR2_2M, minnesota_avg_even)

# Coulomb in MeV·fm
ALPHA_FS = 1.0/137.035999
E2_MeVfm = ALPHA_FS * HBARC   # ≈ 1.4400

class A3Psi(nn.Module):
    """Spatially-symmetric log-wavefunction for A=3.
    log|Psi| = -alpha * sum_i |r_i - R_cm|^2  +  sum_{i<j} u_NN(r_ij)
    with u_NN containing a soft 1/(r+ε) attraction for binding stability.
    """
    def __init__(self, hidden=24):
        super().__init__()
        self.A = 3
        self.log_alpha = nn.Parameter(torch.tensor(math.log(0.10)))   # fm^-2
        self.log_core  = nn.Parameter(torch.tensor(math.log(0.2)))    # bind strength
        self.jas = nn.Sequential(
            nn.Linear(3, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )
        for m in self.jas.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0.0, 0.03)
                nn.init.zeros_(m.bias)

    def _pair_u(self, r):
        c = self.log_core.exp()
        feats = torch.stack([r, torch.exp(-r), torch.exp(-2.0*r)], dim=-1)
        nn_out = self.jas(feats).squeeze(-1)
        return -c/(r + 0.2) + nn_out

    def log_psi(self, X):                       # X: (B,3,3)
        B = X.shape[0]
        Rcm = X.mean(dim=1, keepdim=True)
        d2 = ((X - Rcm)**2).sum(dim=-1)         # (B,3)
        gauss = -self.log_alpha.exp() * d2.sum(dim=-1)
        diff = X.unsqueeze(2) - X.unsqueeze(1)  # (B,3,3,3)
        r = torch.linalg.norm(diff + 1e-12, dim=-1)
        iu, ju = torch.triu_indices(3, 3, offset=1)
        rij = r[:, iu, ju]                      # (B,3) pairs
        u = self._pair_u(rij).sum(dim=-1)
        return gauss + u

def a3_local_energy(model, X, with_coulomb=False, n_pp_pairs=0):
    X = X.detach().requires_grad_(True)
    B = X.shape[0]
    logpsi = model.log_psi(X)
    grad = torch.autograd.grad(logpsi.sum(), X, create_graph=True)[0]
    lap = 0.0
    for a in range(3):
        for k in range(3):
            g2 = torch.autograd.grad(grad[:,a,k].sum(), X,
                                     create_graph=True, retain_graph=True)[0][:,a,k]
            lap = lap + g2
    g2tot = (grad*grad).sum(dim=(-1,-2))
    kinetic = -HBAR2_2M*(lap + g2tot)
    diff = X.unsqueeze(2) - X.unsqueeze(1)
    r = torch.linalg.norm(diff + 1e-12, dim=-1)
    iu, ju = torch.triu_indices(3, 3, offset=1)
    rij = r[:, iu, ju]
    V = minnesota_avg_even(rij).sum(dim=-1)
    if with_coulomb and n_pp_pairs > 0:
        # symmetric ansatz; treat pp Coulomb as an *expectation-value* over
        # randomly-chosen pp pair (equivalent for fully-symmetric spatial part)
        # i.e. take fraction (n_pp_pairs / total_pairs) * sum_{i<j} e^2 / r_{ij}
        coul_total = (E2_MeVfm / rij).sum(dim=-1)
        V = V + (n_pp_pairs / 3.0) * coul_total   # 3 pairs total in A=3
    return kinetic + V

def a3_metropolis(model, n_walkers, n_steps, step, device, thermalize=True):
    X = torch.randn(n_walkers, 3, 3, device=device) * 1.5
    with torch.no_grad():
        lp_old = model.log_psi(X)
    burn = n_steps // 4 if thermalize else 0
    samples = []; accepts = 0; total = 0
    for s in range(n_steps + burn):
        Xnew = X + step*torch.randn_like(X)
        with torch.no_grad():
            lp_new = model.log_psi(Xnew)
        ratio = 2.0*(lp_new - lp_old)
        u = torch.rand(n_walkers, device=device).log()
        accept = (u < ratio)
        X = torch.where(accept.view(-1,1,1), Xnew, X)
        lp_old = torch.where(accept, lp_new, lp_old)
        if s >= burn:
            samples.append(X.clone())
            accepts += accept.sum().item(); total += n_walkers
    return torch.cat(samples, dim=0), accepts/max(total,1)

def run_a3(label, with_coulomb, n_pp_pairs, out_dir, device='cuda',
           iters=1500, walkers=2048, steps=12, mc_step=0.7, lr=4e-4, seed=2):
    torch.manual_seed(seed); np.random.seed(seed)
    os.makedirs(out_dir, exist_ok=True)
    model = A3Psi().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = {'iter': [], 'E_mean': [], 'E_std': [], 'acc': []}
    t0 = time.time()
    for it in range(iters):
        with torch.no_grad():
            X, acc = a3_metropolis(model, walkers, steps, mc_step, device,
                                   thermalize=(it == 0))
        # subsample for gradient stability
        idx = torch.randperm(X.shape[0], device=device)[:walkers]
        Xs = X[idx]
        EL = a3_local_energy(model, Xs, with_coulomb, n_pp_pairs)
        # quantile clip outliers
        q_lo, q_hi = torch.quantile(EL.detach(), torch.tensor([0.02, 0.98], device=device))
        clip = EL.clamp(q_lo, q_hi)
        E_mean = clip.mean()
        loss = ((EL.detach() - E_mean.detach()) * 2.0 *
                (model.log_psi(Xs) - model.log_psi(Xs).detach().mean())).mean()
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        history['iter'].append(it)
        history['E_mean'].append(float(E_mean.item()))
        history['E_std'].append(float(EL.std().item()))
        history['acc'].append(acc)
        if it % 50 == 0 or it == iters-1:
            print(f"[{label} it {it:4d}] E={E_mean.item():+8.3f} ± "
                  f"{EL.std().item()/math.sqrt(walkers):.3f}  acc={acc:.2f}  "
                  f"({time.time()-t0:.1f}s)")
    # final big sample
    with torch.no_grad():
        X, acc = a3_metropolis(model, 4096, 60, mc_step, device)
    EL = a3_local_energy(model, X[-4096:], with_coulomb, n_pp_pairs)
    E_final = EL.mean().item(); E_err = EL.std().item()/math.sqrt(EL.shape[0])
    summary = dict(label=label, with_coulomb=with_coulomb,
                   E_final=E_final, E_err=E_err,
                   n_iters=iters, walkers=walkers,
                   wall_seconds=time.time()-t0)
    with open(os.path.join(out_dir, f'a3_{label}_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(out_dir, f'a3_{label}_history.json'), 'w') as f:
        json.dump(history, f)
    np.save(os.path.join(out_dir, f'a3_{label}_final_EL.npy'),
            EL.detach().cpu().numpy())
    print(f"\n{label}: E_final = {E_final:+.4f} ± {E_err:.4f} MeV")
    return summary

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='./results')
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    p.add_argument('--iters', type=int, default=1500)
    p.add_argument('--walkers', type=int, default=2048)
    p.add_argument('--system', choices=['3H','3He','both'], default='both')
    args = p.parse_args()
    print(f"device={args.device}")
    out = []
    if args.system in ('3H','both'):
        print("\n=== TRITON ³H (A=3, no Coulomb) ===")
        out.append(run_a3('3H', with_coulomb=False, n_pp_pairs=0,
                          out_dir=args.out, device=args.device,
                          iters=args.iters, walkers=args.walkers))
    if args.system in ('3He','both'):
        print("\n=== HELION ³He (A=3, 1 pp Coulomb pair) ===")
        out.append(run_a3('3He', with_coulomb=True, n_pp_pairs=1,
                          out_dir=args.out, device=args.device,
                          iters=args.iters, walkers=args.walkers))
    print("\nSummary:")
    for s in out:
        print(f"  {s['label']:>4s}  E = {s['E_final']:+.3f} ± {s['E_err']:.3f} MeV")
