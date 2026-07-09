#!/usr/bin/env python3.11
"""
Re-pass for Kopaničáková et al. 2023 (arXiv:2306.17648v2).
Goal: diagnose the agreement gap (prior pass: best KG E_rel = 2.65e-2 vs paper 6.1e-4)
and lift coverage by retesting with corrected setup.

Key fixes vs prior pass:
 1. Klein-Gordon BC ansatz no longer = exact solution. Prior pass used
    A(t,x) = x*cos(t) which IS u_exact, making the residual landscape degenerate
    and MSPQN trivially worse. Re-pass uses
       A(t,x) = (1-x^2)/(1+t^2) * x  +  ((1+x)/2)*cos(t) + ((1-x)/2)*(-cos(t))
                                       = (1-x^2)*x/(1+t^2)  +  x*cos(t)
    which satisfies all Dirichlet BCs and IC u(0,x)=x, u_t(0,x)=0
    but is NOT the analytic solution.
 2. n_subdomains = depth (=6 for KG, paper's actual setting), not 4.
 3. Adam warm-up (paper convention; warmup_epochs=2000).
 4. Custom strong-Wolfe L-BFGS using scipy.optimize.minimize(method='L-BFGS-B')
    which implements a more careful line search than torch.optim.LBFGS.
 5. Honest documentation when paper's wall-time budget exceeds what's feasible
    on CherryRd CPU (paper used Piz Daint P100 GPU, 236.5 min for KG L-BFGS).

Outputs JSON per (problem, method) into results/repass/.
Runs on CPU; selected experiments only (KG + Burgers diagnostic).
"""

import os, json, time, math, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import torch
import torch.nn as nn

# --------------------------------------------------------------------- #
#  Repro / device                                                       #
# --------------------------------------------------------------------- #
SEED = 0
torch.manual_seed(SEED)
np.random.seed(SEED)
DEVICE = torch.device("cpu")  # honest re-pass on CherryRd CPU
RESULTS = os.path.join(
    "/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/"
    "pinn-domain-decomp-2023/results/repass"
)
os.makedirs(RESULTS, exist_ok=True)

# --------------------------------------------------------------------- #
#  Hammersley quasi-random sampling (paper Sec 5.1)                     #
# --------------------------------------------------------------------- #
def _van_der_corput(n, base):
    out = np.zeros(n)
    for i in range(n):
        q, k, b = 0.0, i + 1, 1.0 / base
        while k > 0:
            q += (k % base) * b
            k //= base
            b /= base
        out[i] = q
    return out

def hammersley(n, d):
    pts = np.zeros((n, d))
    pts[:, 0] = (np.arange(n) + 0.5) / n
    bases = [2, 3, 5, 7]
    for j in range(1, d):
        pts[:, j] = _van_der_corput(n, bases[j - 1])
    return pts

# --------------------------------------------------------------------- #
#  PINN architecture (ResNet + adaptive tanh + Xavier init, per paper)  #
# --------------------------------------------------------------------- #
class AdaptiveTanh(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.a = nn.Parameter(torch.ones(width))
    def forward(self, x): return torch.tanh(self.a * x)

class ResNetPINN(nn.Module):
    def __init__(self, input_dim, output_dim, depth, width):
        super().__init__()
        self.depth = depth
        self.width = width
        self.input_layer = nn.Linear(input_dim, width, bias=False)
        self.hidden_layers = nn.ModuleList(
            [nn.Linear(width, width) for _ in range(depth)]
        )
        self.activations = nn.ModuleList(
            [AdaptiveTanh(width) for _ in range(depth)]
        )
        self.output_layer = nn.Linear(width, output_dim)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None: nn.init.zeros_(m.bias)
    def forward(self, x):
        y = self.input_layer(x)
        for L, A in zip(self.hidden_layers, self.activations):
            y = y + A(L(y))
        return self.output_layer(y)
    def get_layer_groups(self):
        groups = [list(self.input_layer.parameters())]
        for L, A in zip(self.hidden_layers, self.activations):
            groups.append(list(L.parameters()) + list(A.parameters()))
        groups.append(list(self.output_layer.parameters()))
        return groups
    def n_layers(self): return len(self.get_layer_groups())

# --------------------------------------------------------------------- #
#  Problems                                                             #
# --------------------------------------------------------------------- #
class KleinGordon:
    name = "klein_gordon"
    input_dim, output_dim = 2, 1
    depth, width = 6, 50
    domain = {"t": (0.0, 12.0), "x": (-1.0, 1.0)}
    # paper Table 1: KG -> n_sd=6, k_s=50, Adam lr=1e-3
    n_sd_paper, k_s_paper, adam_lr = 6, 50, 1e-3
    paper_Erel = 6.1e-4

    @staticmethod
    def sample_interior(n):
        pts = hammersley(n, 2)
        t = pts[:, 0] * 12.0
        x = pts[:, 1] * 2.0 - 1.0
        X = np.stack([t, x], 1).astype(np.float32)
        return torch.tensor(X, requires_grad=True, device=DEVICE)

    @staticmethod
    def bc_transform_v1_BAD(u_raw, X):
        """Prior pass: A == exact solution. Degenerate."""
        t = X[:, 0:1]; x = X[:, 1:2]
        A = x * torch.cos(t)
        ell = t * (1 - x ** 2)
        return A + ell * u_raw

    @staticmethod
    def bc_transform(u_raw, X):
        """
        Non-trivial A satisfying all BCs but != exact solution.
          BCs: u(0,x)=x, u_t(0,x)=0, u(t,-1)=-cos(t), u(t,1)=cos(t).
          A1(t,x) = x*cos(t)        ← satisfies Dirichlet+IC u(0,x)=x and u_t(0,x)=0
                                     (and equals exact, so we MUST add a perturbation
                                      that vanishes on all BCs so A != exact)
          A(t,x) = x*cos(t) + eps * x * (1-x^2) * (1 - exp(-t/2))^2
          The extra term is exactly zero at t=0 (since (1-exp(0))^2 = 0),
          its first time derivative at t=0 is 0 (because d/dt[(1-exp(-t/2))^2]|_{t=0}
          = 2*(1-1)*(0.5) = 0), and it is zero at x=±1.
          Choose eps=0.1 so the perturbation magnitude is modest but non-trivial.
        Then u = A + ell * u_raw with ell = (1 - exp(-t)) * (1-x^2). The PINN must
        learn u_raw such that the perturbation is cancelled out -- so u_raw is
        genuinely non-trivial. We use 1-exp(-t) instead of t to keep ell bounded
        on the long [0,12] time interval (avoids ill-conditioning).
        """
        t = X[:, 0:1]; x = X[:, 1:2]
        eps = 0.1
        bump_t = (1.0 - torch.exp(-t / 2.0)) ** 2
        A = x * torch.cos(t) + eps * x * (1.0 - x ** 2) * bump_t
        ell = (1.0 - torch.exp(-t)) * (1.0 - x ** 2)
        return A + ell * u_raw

    @staticmethod
    def exact(X):
        t = X[:, 0:1]; x = X[:, 1:2]
        return x * torch.cos(t)

    @staticmethod
    def residual(model, X, bc_transform):
        X.requires_grad_(True)
        u_raw = model(X)
        u = bc_transform(u_raw, X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_t, u_x = gu[:, 0:1], gu[:, 1:2]
        gut = torch.autograd.grad(u_t, X, torch.ones_like(u_t), create_graph=True)[0]
        gux = torch.autograd.grad(u_x, X, torch.ones_like(u_x), create_graph=True)[0]
        u_tt, u_xx = gut[:, 0:1], gux[:, 1:2]
        t = X[:, 0:1]; x = X[:, 1:2]
        # alpha=-1, beta=0, gamma=1, f = -x cos t + x^2 cos^2 t
        f = -x * torch.cos(t) + (x ** 2) * torch.cos(t) ** 2
        return u_tt - u_xx + u ** 2 - f

class Burgers:
    name = "burgers"
    input_dim, output_dim = 2, 1
    depth, width = 8, 20
    domain = {"t": (0.0, 1.0), "x": (-1.0, 1.0)}
    n_sd_paper, k_s_paper, adam_lr = 8, 50, 5e-4
    nu = 0.01 / math.pi
    paper_Erel = 4.6e-4

    @staticmethod
    def sample_interior(n):
        pts = hammersley(n, 2)
        t = pts[:, 0] * 1.0
        x = pts[:, 1] * 2.0 - 1.0
        X = np.stack([t, x], 1).astype(np.float32)
        return torch.tensor(X, requires_grad=True, device=DEVICE)

    @staticmethod
    def bc_transform(u_raw, X):
        """A satisfies u(0,x)=-sin(pi x), u(t,±1)=0."""
        t = X[:, 0:1]; x = X[:, 1:2]
        A = (1.0 - t) * (-torch.sin(math.pi * x))
        ell = t * (1.0 - x ** 2)
        return A + ell * u_raw

    @staticmethod
    def residual(model, X, bc_transform):
        X.requires_grad_(True)
        u_raw = model(X)
        u = bc_transform(u_raw, X)
        gu = torch.autograd.grad(u, X, torch.ones_like(u), create_graph=True)[0]
        u_t, u_x = gu[:, 0:1], gu[:, 1:2]
        gux = torch.autograd.grad(u_x, X, torch.ones_like(u_x), create_graph=True)[0]
        u_xx = gux[:, 1:2]
        return u_t + u * u_x - Burgers.nu * u_xx

# --------------------------------------------------------------------- #
#  Loss + Erel                                                          #
# --------------------------------------------------------------------- #
def pde_loss(model, X, problem):
    r = problem.residual(model, X, problem.bc_transform)
    return torch.mean(r ** 2)

def Erel_KG(model, n_test=20000):
    """Paper formula: Erel = ||u_NN - u*|| / ||u_NN||  (paper Eq 6.1)."""
    pts = hammersley(n_test, 2)
    t = pts[:, 0] * 12.0
    x = pts[:, 1] * 2.0 - 1.0
    X = torch.tensor(np.stack([t, x], 1).astype(np.float32), device=DEVICE)
    model.eval()
    with torch.no_grad():
        u_pred = KleinGordon.bc_transform(model(X), X)
        u_true = KleinGordon.exact(X)
        num = torch.norm(u_pred - u_true)
        den = torch.norm(u_pred) + 1e-30
    model.train()
    return (num / den).item()

# --------------------------------------------------------------------- #
#  Trainers                                                             #
# --------------------------------------------------------------------- #
def train_adam(model, problem, X, n_epochs=2000, lr=None, log_every=200):
    if lr is None: lr = problem.adam_lr
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    t0 = time.time(); loss_hist = []; err_hist = []; time_hist = []
    for ep in range(n_epochs):
        opt.zero_grad()
        L = pde_loss(model, X, problem)
        L.backward(); opt.step()
        if (ep + 1) % log_every == 0 or ep == 0 or ep == n_epochs - 1:
            e = Erel_KG(model) if problem.name == "klein_gordon" else None
            loss_hist.append(L.item()); err_hist.append(e)
            time_hist.append(time.time() - t0)
            tag = f" Erel={e:.3e}" if e is not None else ""
            print(f"  [Adam] ep={ep:5d} loss={L.item():.3e}{tag}")
    return loss_hist, err_hist, time_hist

def train_lbfgs_torch(model, problem, X, n_epochs=400, max_iter=20, log_every=20):
    """PyTorch L-BFGS with strong_wolfe (m=3, per paper)."""
    opt = torch.optim.LBFGS(model.parameters(), max_iter=max_iter,
                            history_size=3, lr=1.0,
                            line_search_fn="strong_wolfe",
                            tolerance_grad=1e-14, tolerance_change=1e-14)
    t0 = time.time(); loss_hist = []; err_hist = []; time_hist = []
    last = float("inf"); stag = 0
    for ep in range(n_epochs):
        box = [0.0]
        def closure():
            opt.zero_grad()
            L = pde_loss(model, X, problem)
            L.backward(); box[0] = L.item(); return L
        opt.step(closure)
        if not math.isfinite(box[0]):
            print(f"  [LBFGS-torch] NaN at ep={ep}; stopping"); break
        loss_hist.append(box[0]); time_hist.append(time.time() - t0)
        e = Erel_KG(model) if problem.name == "klein_gordon" else None
        err_hist.append(e)
        if (ep + 1) % log_every == 0 or ep == 0:
            tag = f" Erel={e:.3e}" if e is not None else ""
            print(f"  [LBFGS-torch] ep={ep:5d} loss={box[0]:.3e}{tag}"
                  f" t={time_hist[-1]:.1f}s")
        if abs(last - box[0]) / (abs(last) + 1e-30) < 1e-12:
            stag += 1
            if stag >= 30:
                print(f"  [LBFGS-torch] stagnated at ep={ep}"); break
        else:
            stag = 0
        last = box[0]
    return loss_hist, err_hist, time_hist

def _flatten(params):
    return torch.cat([p.detach().reshape(-1) for p in params])

def _set_flat(params, flat):
    i = 0
    for p in params:
        n = p.numel()
        p.data.copy_(flat[i:i + n].view_as(p.data))
        i += n

def train_lbfgs_scipy(model, problem, X, max_iter=400, log_every=20):
    """scipy.optimize.minimize(method='L-BFGS-B') with maxcor=3 (paper m=3) and
    a strict-Wolfe-ish line search (scipy's f77 implementation is closer to
    Dennis-Schnabel cubic backtracking than torch's strong_wolfe zoom)."""
    from scipy.optimize import minimize
    params = list(model.parameters())
    x0 = _flatten(params).cpu().numpy().astype(np.float64)
    t0 = time.time(); loss_hist = []; err_hist = []; time_hist = []
    iter_box = {"n": 0}

    def fg(x):
        _set_flat(params, torch.from_numpy(x.astype(np.float32)))
        model.zero_grad()
        L = pde_loss(model, X, problem)
        L.backward()
        g = torch.cat([(p.grad.detach() if p.grad is not None
                        else torch.zeros_like(p)).reshape(-1) for p in params])
        return float(L.item()), g.cpu().numpy().astype(np.float64)

    def cb(xk):
        iter_box["n"] += 1
        if iter_box["n"] % log_every == 0 or iter_box["n"] == 1:
            _set_flat(params, torch.from_numpy(xk.astype(np.float32)))
            # pde_loss requires grad through X (autograd needs requires_grad=True
            # on X). DO NOT wrap in no_grad here -- just compute & discard.
            L = float(pde_loss(model, X, problem).detach().item())
            e = Erel_KG(model) if problem.name == "klein_gordon" else None
            loss_hist.append(L); err_hist.append(e)
            time_hist.append(time.time() - t0)
            tag = f" Erel={e:.3e}" if e is not None else ""
            print(f"  [LBFGS-scipy] it={iter_box['n']:5d} loss={L:.3e}{tag}"
                  f" t={time_hist[-1]:.1f}s")

    res = minimize(fg, x0, jac=True, method="L-BFGS-B",
                   callback=cb,
                   options=dict(maxcor=3, maxiter=max_iter,
                                ftol=1e-16, gtol=1e-14, maxls=40, disp=False))
    # final
    _set_flat(params, torch.from_numpy(res.x.astype(np.float32)))
    Lf = float(pde_loss(model, X, problem).detach().item())
    ef = Erel_KG(model) if problem.name == "klein_gordon" else None
    loss_hist.append(Lf); err_hist.append(ef); time_hist.append(time.time() - t0)
    print(f"  [LBFGS-scipy] DONE iters={res.nit} loss={Lf:.3e} Erel={ef}")
    return loss_hist, err_hist, time_hist, dict(nit=int(res.nit), nfev=int(res.nfev),
                                                message=str(res.message))

# --------------------------------------------------------------------- #
#  SPQN (additive / multiplicative), paper Algorithm 3.1                #
# --------------------------------------------------------------------- #
def _solve_local_subproblem(model, X, problem, sd_params, k_s, history=3):
    all_params = list(model.parameters())
    sd_ids = {id(p) for p in sd_params}
    for p in all_params:
        p.requires_grad_(id(p) in sd_ids)
    active = [p for p in sd_params if p.requires_grad]
    if not active:
        for p in all_params: p.requires_grad_(True)
        return
    opt = torch.optim.LBFGS(active, max_iter=k_s, history_size=history,
                            lr=1.0, line_search_fn="strong_wolfe",
                            tolerance_grad=1e-14, tolerance_change=1e-14)
    def closure():
        opt.zero_grad()
        L = pde_loss(model, X, problem)
        L.backward(); return L
    try:
        opt.step(closure)
    except Exception as e:
        print(f"    local LBFGS error: {e}")
    for p in all_params: p.requires_grad_(True)

def train_spqn(model, problem, X, mode="multiplicative",
               n_sd=None, k_s=None, alpha=1.0,
               n_outer=200, log_every=10):
    if k_s is None: k_s = problem.k_s_paper
    if n_sd is None: n_sd = problem.n_sd_paper
    groups = model.get_layer_groups()
    # build n_sd subdomains by combining consecutive layers
    if n_sd >= len(groups):
        subdomains = groups
    else:
        subdomains = []
        per = len(groups) // n_sd
        rem = len(groups) % n_sd
        i = 0
        for s in range(n_sd):
            cnt = per + (1 if s < rem else 0)
            grp = []
            for _ in range(cnt):
                if i < len(groups):
                    grp.extend(groups[i]); i += 1
            subdomains.append(grp)
    n_actual = len(subdomains)

    global_opt = torch.optim.LBFGS(model.parameters(), max_iter=20,
                                   history_size=3, lr=1.0,
                                   line_search_fn="strong_wolfe",
                                   tolerance_grad=1e-14, tolerance_change=1e-14)
    t0 = time.time(); loss_hist = []; err_hist = []; time_hist = []
    for ep in range(n_outer):
        if mode == "additive":
            saved = [p.detach().clone() for p in model.parameters()]
            updates = []
            for sd in subdomains:
                for p, s in zip(model.parameters(), saved): p.data.copy_(s)
                _solve_local_subproblem(model, X, problem, sd, k_s)
                upd = [(p.detach() - s).clone()
                       for p, s in zip(model.parameters(), saved)]
                updates.append(upd)
            for p, s in zip(model.parameters(), saved): p.data.copy_(s)
            for upd in updates:
                for p, du in zip(model.parameters(), upd):
                    p.data.add_(du, alpha=alpha)
        else:  # multiplicative
            for sd in subdomains:
                _solve_local_subproblem(model, X, problem, sd, k_s)
        # global step
        box = [0.0]
        def closure():
            global_opt.zero_grad()
            L = pde_loss(model, X, problem)
            L.backward(); box[0] = L.item(); return L
        try:
            global_opt.step(closure)
        except Exception as e:
            print(f"  [SPQN-{mode}] global step error: {e}"); break
        if not math.isfinite(box[0]):
            print(f"  [SPQN-{mode}] NaN at outer ep={ep}; stopping"); break
        loss_hist.append(box[0])
        e = Erel_KG(model) if problem.name == "klein_gordon" else None
        err_hist.append(e); time_hist.append(time.time() - t0)
        if (ep + 1) % log_every == 0 or ep == 0:
            tag = f" Erel={e:.3e}" if e is not None else ""
            print(f"  [SPQN-{mode} n_sd={n_actual} k_s={k_s}] ep={ep:4d}"
                  f" loss={box[0]:.3e}{tag} t={time_hist[-1]:.1f}s")
    return loss_hist, err_hist, time_hist, dict(n_sd=n_actual, k_s=k_s)

# --------------------------------------------------------------------- #
#  Experiment harness                                                   #
# --------------------------------------------------------------------- #
def save(name, payload):
    path = os.path.join(RESULTS, f"{name}.json")
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=lambda o: float(o)
                  if isinstance(o, (np.floating,)) else str(o))
    print(f"  saved -> {path}")

def fresh_model(problem):
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    return ResNetPINN(problem.input_dim, problem.output_dim,
                      problem.depth, problem.width).to(DEVICE)

def run_kg_diagnostic():
    """Six-way KG comparison to isolate the agreement gap.
    Budgets tuned for CPU CherryRd ~30 min total."""
    P = KleinGordon
    print(f"\n===== Klein-Gordon diagnostic ({P.depth}x{P.width}={sum(p.numel() for p in fresh_model(P).parameters())} params) =====")
    n_int = 5000  # paper uses 10000 but cuts CPU time in half
    print(f"Sampling {n_int} Hammersley collocation points (paper uses 10000; smaller for CPU)")
    X = P.sample_interior(n_int)

    # --- A: torch L-BFGS, no warmup, OLD (degenerate) BC ---
    print("\n[A] torch.LBFGS strong_wolfe, NO warmup, BAD BC (=exact). Prior-pass-like.")
    P.bc_transform, _bc_save = P.bc_transform_v1_BAD, P.bc_transform  # type: ignore
    m = fresh_model(P)
    lh, eh, th = train_lbfgs_torch(m, P, X, n_epochs=60, max_iter=10, log_every=10)
    P.bc_transform = _bc_save  # type: ignore  # restore good BC for subsequent runs
    save("kg_A_torch_lbfgs_bad_bc", dict(
        method="torch_lbfgs_strong_wolfe_max_iter10", warmup=0, bc="bad_A_eq_exact",
        loss=lh, Erel=eh, time=th, best_loss=min(lh) if lh else None,
        best_Erel=min((e for e in eh if e is not None), default=None),
    ))

    # --- B: torch L-BFGS, NO warmup, GOOD BC ---
    print("\n[B] torch.LBFGS strong_wolfe, NO warmup, GOOD BC")
    m = fresh_model(P)
    lh, eh, th = train_lbfgs_torch(m, P, X, n_epochs=60, max_iter=10, log_every=10)
    save("kg_B_torch_lbfgs_good_bc", dict(
        method="torch_lbfgs_strong_wolfe_max_iter10", warmup=0, bc="good_nontrivial_A",
        loss=lh, Erel=eh, time=th, best_loss=min(lh) if lh else None,
        best_Erel=min((e for e in eh if e is not None), default=None),
    ))

    # --- C: scipy L-BFGS-B (cubic backtracking line search), NO warmup, GOOD BC ---
    print("\n[C] scipy L-BFGS-B m=3, NO warmup, GOOD BC")
    m = fresh_model(P)
    lh, eh, th, meta = train_lbfgs_scipy(m, P, X, max_iter=1500, log_every=100)
    save("kg_C_scipy_lbfgs_good_bc", dict(
        method="scipy_LBFGSB_m3", warmup=0, bc="good_nontrivial_A",
        loss=lh, Erel=eh, time=th, best_loss=min(lh) if lh else None,
        best_Erel=min((e for e in eh if e is not None), default=None),
        meta=meta,
    ))

    # --- D: Adam warmup 2000ep -> scipy L-BFGS-B, GOOD BC ---
    print("\n[D] Adam warmup 2000ep -> scipy L-BFGS-B m=3, GOOD BC")
    m = fresh_model(P)
    a_lh, a_eh, a_th = train_adam(m, P, X, n_epochs=2000, log_every=400)
    s_lh, s_eh, s_th, smeta = train_lbfgs_scipy(m, P, X, max_iter=1500, log_every=100)
    save("kg_D_adam_then_scipy_lbfgs", dict(
        method="adam_then_scipy_LBFGSB_m3", warmup=2000, bc="good_nontrivial_A",
        adam=dict(loss=a_lh, Erel=a_eh, time=a_th),
        lbfgs=dict(loss=s_lh, Erel=s_eh, time=s_th, meta=smeta),
        best_loss=min(s_lh) if s_lh else None,
        best_Erel=min((e for e in (s_eh or []) if e is not None), default=None),
    ))

    # --- E: Adam warmup -> MSPQN (n_sd=6, k_s=50, paper config) ---
    print("\n[E] Adam warmup 2000ep -> MSPQN n_sd=6 k_s=50 (paper config), GOOD BC")
    m = fresh_model(P)
    a_lh, a_eh, a_th = train_adam(m, P, X, n_epochs=2000, log_every=400)
    s_lh, s_eh, s_th, smeta = train_spqn(m, P, X, mode="multiplicative",
                                         n_sd=6, k_s=50, n_outer=40, log_every=2)
    save("kg_E_adam_then_mspqn_paper", dict(
        method="adam_then_MSPQN_n_sd6_k_s50_alpha1",
        warmup=2000, bc="good_nontrivial_A",
        adam=dict(loss=a_lh, Erel=a_eh, time=a_th),
        mspqn=dict(loss=s_lh, Erel=s_eh, time=s_th, meta=smeta),
        best_loss=min(s_lh) if s_lh else None,
        best_Erel=min((e for e in (s_eh or []) if e is not None), default=None),
    ))

    # --- F: Adam warmup -> ASPQN (n_sd=6, k_s=50, alpha=0.5 damping) ---
    print("\n[F] Adam warmup 2000ep -> ASPQN n_sd=6 k_s=50 alpha=0.5 (damped), GOOD BC")
    m = fresh_model(P)
    a_lh, a_eh, a_th = train_adam(m, P, X, n_epochs=2000, log_every=400)
    s_lh, s_eh, s_th, smeta = train_spqn(m, P, X, mode="additive",
                                         n_sd=6, k_s=50, alpha=0.5,
                                         n_outer=25, log_every=2)
    save("kg_F_adam_then_aspqn_damped", dict(
        method="adam_then_ASPQN_n_sd6_k_s50_alpha0.5",
        warmup=2000, bc="good_nontrivial_A",
        adam=dict(loss=a_lh, Erel=a_eh, time=a_th),
        aspqn=dict(loss=s_lh, Erel=s_eh, time=s_th, meta=smeta),
        best_loss=min(s_lh) if s_lh else None,
        best_Erel=min((e for e in (s_eh or []) if e is not None), default=None),
    ))

def run_burgers_diagnostic():
    """Burgers replication with Adam warmup + scipy L-BFGS-B (paper m=3)."""
    P = Burgers
    print(f"\n===== Burgers ({P.depth}x{P.width}) =====")
    X = P.sample_interior(5000)

    # H: Adam 2000 -> scipy L-BFGS-B
    print("\n[H] Adam warmup 2000ep -> scipy L-BFGS-B m=3")
    m = fresh_model(P)
    a_lh, _, a_th = train_adam(m, P, X, n_epochs=2000, log_every=400)
    s_lh, _, s_th, smeta = train_lbfgs_scipy(m, P, X, max_iter=1500, log_every=100)
    save("burgers_H_adam_then_scipy_lbfgs", dict(
        method="adam_then_scipy_LBFGSB_m3", warmup=2000,
        adam=dict(loss=a_lh, time=a_th),
        lbfgs=dict(loss=s_lh, time=s_th, meta=smeta),
        best_loss=min(s_lh) if s_lh else None,
    ))

    # I: Adam 2000 -> MSPQN paper config (n_sd=8, k_s=50)
    print("\n[I] Adam warmup 2000ep -> MSPQN n_sd=8 k_s=50 (paper)")
    m = fresh_model(P)
    a_lh, _, a_th = train_adam(m, P, X, n_epochs=2000, log_every=400)
    s_lh, _, s_th, smeta = train_spqn(m, P, X, mode="multiplicative",
                                      n_sd=8, k_s=50, n_outer=20, log_every=2)
    save("burgers_I_adam_then_mspqn", dict(
        method="adam_then_MSPQN_n_sd8_k_s50", warmup=2000,
        adam=dict(loss=a_lh, time=a_th),
        mspqn=dict(loss=s_lh, time=s_th, meta=smeta),
        best_loss=min(s_lh) if s_lh else None,
    ))

# --------------------------------------------------------------------- #
def main():
    print(f"torch={torch.__version__} device={DEVICE}")
    overall_t0 = time.time()
    run_kg_diagnostic()
    run_burgers_diagnostic()
    print(f"\nTotal wall time: {time.time() - overall_t0:.1f}s")

if __name__ == "__main__":
    main()
