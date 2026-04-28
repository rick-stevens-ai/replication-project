"""
Neural-network VMC for light nuclei (A=2, A=4) with the Minnesota NN potential.

Replication of OSTI 1864334 ("VMC of A<=12 nuclei with a NN correlator ansatz").
We use the Minnesota central potential (Thompson, LeMere, Tang 1977) as a
tractable surrogate for AV6'/AV8'. For the deuteron (A=2) we work in the
relative-coordinate one-body picture (triplet-even channel). For helium-4
(A=4) we use a spatially-symmetric (S=0,T=0) ansatz in which the spin-isospin
wave function is fully antisymmetric and the spatial part is symmetric, so
a (signless) Jastrow x NN-backflow spatial wave function suffices.

Author: Ollie (OpenClaw subagent replicating 1864334)
"""

import argparse, math, os, time, json
import numpy as np
import torch
import torch.nn as nn

# --- physical constants (MeV, fm) --------------------------------------
HBARC = 197.3269804       # MeV fm
MN    = 938.91875         # average nucleon mass, MeV/c^2
HBAR2_2M = HBARC * HBARC / (2.0 * MN)   # ~20.7355 MeV fm^2

# --- Minnesota potential parameters (Thompson, LeMere, Tang 1977) -------
# V(r) = V_R exp(-k_R r^2)
#      + (V_s/2)(1 + P^sigma) exp(-k_s r^2)    # singlet projector
#      + (V_t/2)(1 - P^sigma) exp(-k_t r^2)    # triplet projector
V_R, K_R = 200.0,  1.487
V_s, K_s = -91.85, 0.465
V_t, K_t = -178.0, 0.639

def minnesota_triplet(r):
    """Radial potential in a pure spin-triplet (S=1) pair channel (P^sigma=+1).
    Used for the deuteron."""
    return V_R*torch.exp(-K_R*r*r) + V_t*torch.exp(-K_t*r*r)

def minnesota_avg_even(r):
    """Spin-isospin-averaged (even state) Minnesota used for the
    spatially-symmetric A=4 alpha-particle ansatz.
    For a totally space-symmetric (L=S=T=0) pair, half the pair is singlet
    (deuteron-like spin-antisymmetric) and half triplet; averaging:
        V_eff(r) = V_R e^{-k_R r^2} + 0.5 V_s e^{-k_s r^2} + 0.5 V_t e^{-k_t r^2}
    This is the standard 'central' Minnesota used in 4-body benchmarks.
    """
    return (V_R*torch.exp(-K_R*r*r)
            + 0.5*V_s*torch.exp(-K_s*r*r)
            + 0.5*V_t*torch.exp(-K_t*r*r))

# =======================================================================
# 1.  DEUTERON  (A=2, one relative coordinate r in R^3)
# =======================================================================

class DeuteronPsi(nn.Module):
    """Log-wavefunction: log|psi(r)| = -alpha*r + NN(r).
    Nodeless, isotropic S-wave ansatz.  NN sees features [r, exp(-r)]."""
    def __init__(self, hidden=32):
        super().__init__()
        self.log_alpha = nn.Parameter(torch.tensor(math.log(0.3)))  # alpha~0.3 fm^-1
        self.net = nn.Sequential(
            nn.Linear(2, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )
        # Start the NN correction near zero.
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0.0, 0.05)
                nn.init.zeros_(m.bias)

    def log_psi(self, r):               # r: (B,) tensor of distances >0
        alpha = self.log_alpha.exp()
        feats = torch.stack([r, torch.exp(-r)], dim=-1)
        correction = self.net(feats).squeeze(-1)
        return -alpha*r + correction

def deuteron_local_energy(model, R):
    """R: (B,3) relative-coordinate samples.  Returns local energies (MeV).
    H = -(hbar^2/m_N) nabla_r^2 + V_t(r).  Note reduced mass mu = m_N/2,
    so hbar^2/(2 mu) = hbar^2/m_N  -> prefactor = 2 * HBAR2_2M.
    """
    R = R.detach().requires_grad_(True)
    r = torch.linalg.norm(R, dim=-1)
    logpsi = model.log_psi(r)
    grad = torch.autograd.grad(logpsi.sum(), R, create_graph=True)[0]  # (B,3)
    lap = 0.0
    for k in range(3):
        g2 = torch.autograd.grad(grad[:,k].sum(), R, create_graph=True)[0][:,k]
        lap = lap + g2
    # psi^{-1} nabla^2 psi = nabla^2 log|psi| + |grad log|psi||^2
    kinetic = -2.0*HBAR2_2M*(lap + (grad*grad).sum(-1))
    V = minnesota_triplet(r)
    return kinetic + V

def deuteron_metropolis(model, n_walkers, n_steps, step, device, thermalize=True):
    """Simple Gaussian-proposal Metropolis sampler in 3D."""
    R = torch.randn(n_walkers, 3, device=device) * 2.0
    with torch.no_grad():
        logpsi_old = model.log_psi(torch.linalg.norm(R, dim=-1))
    accepts = 0
    total = 0
    burn = n_steps // 4 if thermalize else 0
    samples = []
    for s in range(n_steps + burn):
        Rnew = R + step*torch.randn_like(R)
        with torch.no_grad():
            lp_new = model.log_psi(torch.linalg.norm(Rnew, dim=-1))
        ratio = 2.0*(lp_new - logpsi_old)
        u = torch.rand(n_walkers, device=device).log()
        accept = (u < ratio)
        R = torch.where(accept.unsqueeze(-1), Rnew, R)
        logpsi_old = torch.where(accept, lp_new, logpsi_old)
        if s >= burn:
            samples.append(R.clone())
            accepts += accept.sum().item()
            total += n_walkers
    return torch.cat(samples, dim=0), accepts/max(total,1)


def run_deuteron(out_dir, device='cuda', iters=800, walkers=4096, steps=8,
                 mc_step=1.2, lr=3e-3, seed=0, log_every=20):
    torch.manual_seed(seed); np.random.seed(seed)
    model = DeuteronPsi().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    step = mc_step
    t0 = time.time()
    for it in range(iters):
        R, acc = deuteron_metropolis(model, walkers, steps, step, device)
        # Tune step to keep ~50% acceptance
        if acc > 0.6: step *= 1.05
        elif acc < 0.4: step *= 0.95
        EL = deuteron_local_energy(model, R)                       # (N,)
        # Clip to tame occasional outliers
        EL_c = torch.clamp(EL, EL.quantile(0.005).item(), EL.quantile(0.995).item())
        E_mean = EL_c.mean()
        # Variational-energy gradient via log-derivative trick:
        # dE/dtheta = 2 * < (E_L - <E_L>) * d log|psi| / dtheta >
        r = torch.linalg.norm(R, dim=-1).detach()
        logpsi = model.log_psi(r)
        surrogate = 2.0*((EL_c.detach() - E_mean.detach()) * logpsi).mean()
        opt.zero_grad(); surrogate.backward(); opt.step()
        history.append(dict(it=it, E=EL.mean().item(), E_clip=E_mean.item(),
                            std=EL.std().item()/math.sqrt(R.shape[0]),
                            acc=acc, step=step))
        if it % log_every == 0 or it == iters-1:
            print(f"[deut it={it:4d}] E={EL.mean().item():+.4f} "
                  f"std={EL.std().item()/math.sqrt(R.shape[0]):.4f} "
                  f"acc={acc:.2f} step={step:.3f}")
    # Final evaluation with bigger sample
    R, acc = deuteron_metropolis(model, 16384, 40, step, device)
    EL = deuteron_local_energy(model, R).detach().cpu().numpy()
    E = float(EL.mean()); SE = float(EL.std()/math.sqrt(EL.size))
    print(f"[deut FINAL] N={EL.size}  E = {E:+.5f} +/- {SE:.5f} MeV  "
          f"(exp = -2.2246 MeV)  time={time.time()-t0:.1f}s")
    # Save
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'deuteron_history.json'), 'w') as f:
        json.dump(history, f)
    np.save(os.path.join(out_dir, 'deuteron_final_EL.npy'), EL)
    with open(os.path.join(out_dir, 'deuteron_summary.json'), 'w') as f:
        json.dump(dict(E_final=E, SE=SE, N_final=EL.size, iters=iters,
                       walkers=walkers, steps=steps, device=str(device),
                       wall_time_s=time.time()-t0,
                       experiment_B=-2.2246,
                       minnesota_triplet_B_reference=-2.202), f, indent=2)
    return E, SE

# =======================================================================
# 2.  HELIUM-4 (A=4, spatially symmetric Jastrow x NN-backflow)
# =======================================================================

class He4Psi(nn.Module):
    """Spatially-symmetric log-wavefunction of A=4 nucleons.
      log|Psi| = -alpha sum_i |r_i-R_cm|^2 + sum_{i<j} u_NN(r_ij) + (c_hc / r_ij)
    The spin-isospin factor (fully antisymmetric S=0,T=0 alpha ket) is handled
    analytically; here we only evolve the spatial part which must be totally
    symmetric. A short-range 1/r repulsion ("hard-core wall") is ADDED to the
    Jastrow so that the wave function vanishes rapidly at small r, preventing
    the unphysical cluster-collapse that Minnesota's finite core allows in a
    purely spatial-symmetric ansatz.
    The NN is a per-pair radial MLP on features [r, exp(-r), exp(-2r)]; it is
    applied pairwise (symmetric under permutation by construction).
    """
    def __init__(self, A=4, hidden=24):
        super().__init__()
        self.A = A
        self.pairs = A*(A-1)//2
        self.log_alpha = nn.Parameter(torch.tensor(math.log(0.15)))  # fm^-2
        self.log_core  = nn.Parameter(torch.tensor(math.log(0.3)))   # hard-core coeff [fm]
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
        # u(r) = -core/r  +  NN([r, e^-r, e^-2r])
        core = self.log_core.exp()
        feats = torch.stack([r, torch.exp(-r), torch.exp(-2.0*r)], dim=-1)
        nn_out = self.jas(feats).squeeze(-1)
        return -core / (r + 0.2) + nn_out

    def log_psi(self, X):
        B, A, _ = X.shape
        Rcm = X.mean(dim=1, keepdim=True)
        d2 = ((X - Rcm)**2).sum(dim=-1)
        alpha = self.log_alpha.exp()
        gauss = -alpha*d2.sum(dim=-1)
        diff = X.unsqueeze(2) - X.unsqueeze(1)
        r = torch.linalg.norm(diff + 1e-12, dim=-1)
        iu, ju = torch.triu_indices(A, A, offset=1)
        rij = r[:, iu, ju]                               # (B,P)
        u = self._pair_u(rij).sum(dim=-1)
        return gauss + u

def he4_local_energy(model, X, create_graph=True):
    """X: (B,A,3).  H = -sum_i (hbar^2/2m) nabla_i^2 + sum_{i<j} V(r_ij).
    Ansatz is CM-invariant, so (sum_i nabla_i) psi = 0 and T_cm = 0 automatically;
    no explicit subtraction required.
    """
    X = X.detach().requires_grad_(True)
    B, A, _ = X.shape
    logpsi = model.log_psi(X)
    grad = torch.autograd.grad(logpsi.sum(), X, create_graph=True)[0]  # (B,A,3)
    lap = 0.0
    for a in range(A):
        for k in range(3):
            g2 = torch.autograd.grad(grad[:,a,k].sum(), X,
                                     create_graph=create_graph,
                                     retain_graph=True)[0][:,a,k]
            lap = lap + g2
    g2tot = (grad*grad).sum(dim=(-1,-2))
    kinetic = -HBAR2_2M*(lap + g2tot)
    diff = X.unsqueeze(2) - X.unsqueeze(1)
    r = torch.linalg.norm(diff + 1e-12, dim=-1)
    iu, ju = torch.triu_indices(A, A, offset=1)
    rij = r[:, iu, ju]
    V = minnesota_avg_even(rij).sum(dim=-1)
    return kinetic + V

def he4_metropolis(model, n_walkers, n_steps, step, device, A=4, thermalize=True):
    X = torch.randn(n_walkers, A, 3, device=device) * 1.5
    with torch.no_grad():
        lp_old = model.log_psi(X)
    accepts, total = 0, 0
    burn = n_steps // 4 if thermalize else 0
    samples = []
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

def run_he4(out_dir, device='cuda', iters=1200, walkers=2048, steps=10,
            mc_step=0.8, lr=5e-4, seed=1, log_every=25):
    torch.manual_seed(seed); np.random.seed(seed)
    model = He4Psi(A=4).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    step = mc_step
    t0 = time.time()
    for it in range(iters):
        X, acc = he4_metropolis(model, walkers, steps, step, device)
        if acc > 0.6: step *= 1.05
        elif acc < 0.4: step *= 0.95
        EL = he4_local_energy(model, X)
        lo, hi = EL.quantile(0.02).item(), EL.quantile(0.98).item()
        # hard cap to prevent catastrophic updates from cluster-collapse samples
        lo = max(lo, -80.0)
        EL_c = torch.clamp(EL, lo, hi)
        E_mean = EL_c.mean()
        logpsi = model.log_psi(X.detach())
        surrogate = 2.0*((EL_c.detach() - E_mean.detach())*logpsi).mean()
        opt.zero_grad(); surrogate.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.2)
        opt.step()
        history.append(dict(it=it, E=EL.mean().item(), E_clip=E_mean.item(),
                            std=EL.std().item()/math.sqrt(EL.numel()),
                            acc=acc, step=step))
        if it % log_every == 0 or it == iters-1:
            print(f"[he4 it={it:4d}] E={EL.mean().item():+.3f} "
                  f"Ec={E_mean.item():+.3f} std={EL.std().item()/math.sqrt(EL.numel()):.3f} "
                  f"acc={acc:.2f} step={step:.3f}")
    # Big final eval in chunks (no create_graph => OOM-safe)
    X, acc = he4_metropolis(model, 4096, 40, step, device)
    EL_list = []
    for i in range(0, X.shape[0], 1024):
        chunk = X[i:i+1024]
        EL_list.append(he4_local_energy(model, chunk, create_graph=False).detach().cpu())
    EL = torch.cat(EL_list).numpy()
    E = float(EL.mean()); SE = float(EL.std()/math.sqrt(EL.size))
    print(f"[he4 FINAL] N={EL.size}  E = {E:+.4f} +/- {SE:.4f} MeV  "
          f"(Minnesota-central alpha ref ~ -29.9 MeV; exp -28.30)  "
          f"time={time.time()-t0:.1f}s")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'he4_history.json'), 'w') as f:
        json.dump(history, f)
    np.save(os.path.join(out_dir, 'he4_final_EL.npy'), EL)
    with open(os.path.join(out_dir, 'he4_summary.json'), 'w') as f:
        json.dump(dict(E_final=E, SE=SE, N_final=EL.size, iters=iters,
                       walkers=walkers, steps=steps, device=str(device),
                       wall_time_s=time.time()-t0,
                       experiment_B=-28.296,
                       minnesota_central_alpha_ref=-29.94), f, indent=2)
    return E, SE


# =======================================================================
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--system', choices=['deuteron','he4','both'], default='both')
    p.add_argument('--out', default='./results')
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    p.add_argument('--deut_iters', type=int, default=800)
    p.add_argument('--he4_iters',  type=int, default=1200)
    p.add_argument('--deut_walkers', type=int, default=4096)
    p.add_argument('--he4_walkers',  type=int, default=2048)
    args = p.parse_args()

    print(f"device={args.device}  torch={torch.__version__}  "
          f"cuda_avail={torch.cuda.is_available()}")
    if args.device.startswith('cuda'):
        print("GPU:", torch.cuda.get_device_name(0))

    if args.system in ('deuteron','both'):
        print("\n=== DEUTERON (A=2), Minnesota triplet ===")
        run_deuteron(args.out, device=args.device,
                     iters=args.deut_iters, walkers=args.deut_walkers)
    if args.system in ('he4','both'):
        print("\n=== HELIUM-4 (A=4), Minnesota central (even-state avg) ===")
        run_he4(args.out, device=args.device,
                iters=args.he4_iters, walkers=args.he4_walkers)
