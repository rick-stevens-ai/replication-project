#!/usr/bin/env python3
"""
Final V2 experiments: upgraded PINN domain-decomposition replication.
Kopaničáková et al. (2023), arXiv:2306.17648v2

Strategy:
  - L-BFGS baseline: FullBatchLBFGS (Wolfe) for KG, PyTorch L-BFGS for others
    FullBatchLBFGS hangs on Burgers/Allen-Cahn due to Wolfe line search issues
  - MSPQN/ASPQN: PyTorch L-BFGS (strong_wolfe) for local + global
  - Adam: standard Adam with ReduceLROnPlateau
  
All use penalty-free BC formulation.
"""

import sys, os, json, time, copy, signal, torch, numpy as np, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/data/stevens/projects/PyTorch-LBFGS/functions')

from pinn_model import ResNetPINN
from problems import (KleinGordonProblem, BurgersProblem, AllenCahnProblem,
                       AdvectionDiffusionProblem)

try:
    from LBFGS import FullBatchLBFGS
    HAS_FBLBFGS = True
except ImportError:
    HAS_FBLBFGS = False

try:
    from reference_solutions import burgers_reference, allen_cahn_reference, advection_diffusion_reference
    HAS_REF = True
except:
    HAS_REF = False

RESULTS_DIR = '/data/stevens/projects/pinn-domain-decomp/results'
os.makedirs(RESULTS_DIR, exist_ok=True)

# Problems where FullBatchLBFGS works (tested empirically)
FB_SAFE_PROBLEMS = {'klein_gordon'}


def save_json(data, filename):
    def convert(obj):
        if isinstance(obj, (np.floating, np.integer)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, torch.Tensor): return obj.item() if obj.numel() == 1 else obj.tolist()
        return obj
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=convert)
    print(f"  Saved: {path}")


def compute_loss(model, X_int, problem, bc_transform):
    residual = problem.pde_residual(model, X_int, bc_transform=bc_transform)
    return torch.mean(residual ** 2)


def compute_error(model, problem, bc_transform, n_test=10000, device='cpu', ref_interp=None):
    if problem.exact_solution_available():
        with torch.no_grad():
            X = problem.generate_collocation_points(n_int=n_test, device=device)
            u_raw = model(X)
            u_pred = bc_transform(u_raw, X)
            u_exact = problem.exact_solution(X)
            return (torch.norm(u_pred - u_exact) / (torch.norm(u_pred) + 1e-30)).item()
    elif ref_interp is not None:
        with torch.no_grad():
            X = problem.generate_collocation_points(n_int=n_test, device=device)
            u_raw = model(X)
            u_pred = bc_transform(u_raw, X)
            u_ref = torch.tensor(ref_interp(X.cpu().numpy()), dtype=torch.float32,
                                 device=device).reshape(-1, 1)
            return (torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)).item()
    return None


CONFIGS = {
    'klein_gordon': {'cls': KleinGordonProblem, 'depth': 6, 'width': 50},
    'burgers': {'cls': BurgersProblem, 'depth': 8, 'width': 20},
    'allen_cahn': {'cls': AllenCahnProblem, 'depth': 6, 'width': 64},
    'advection_diffusion': {'cls': AdvectionDiffusionProblem, 'depth': 10, 'width': 50},
}


def get_ref(name):
    """Get reference solution interpolator. Returns None if unavailable or unreliable."""
    if not HAS_REF: return None
    try:
        if name == 'burgers':
            # Note: Cole-Hopf spectral reference is numerically unstable for nu=0.01/pi
            # at high resolution. Skip until we implement a stable solver.
            return None
        elif name == 'allen_cahn':
            interp, _, _, u = allen_cahn_reference()
            # Sanity check
            if np.isnan(u).any() or np.abs(u).max() > 100:
                print(f"  WARNING: Allen-Cahn reference unstable, skipping")
                return None
            return interp
        elif name == 'advection_diffusion':
            interp, _, _, u = advection_diffusion_reference()
            if np.isnan(u).any() or np.abs(u).max() > 1000:
                print(f"  WARNING: Advection-diffusion reference unstable, skipping")
                return None
            return interp
    except Exception as e:
        print(f"  WARNING: Reference solution failed for {name}: {e}")
    return None


def make_model(cfg, device):
    return ResNetPINN(cfg['cls'].input_dim, cfg['cls'].output_dim,
                      cfg['depth'], cfg['width']).to(device)


def subsample_list(lst, max_n=200):
    if len(lst) <= max_n: return lst
    step = max(1, len(lst) // max_n)
    return [lst[i] for i in range(0, len(lst), step)]


# ============================================================
# L-BFGS with FullBatchLBFGS (for safe problems) or PyTorch L-BFGS
# ============================================================
def train_lbfgs_v2(prob_name, device, n_epochs=3000):
    cfg = CONFIGS[prob_name]
    P = cfg['cls']
    ref = get_ref(prob_name)
    use_fb = HAS_FBLBFGS and prob_name in FB_SAFE_PROBLEMS

    torch.manual_seed(42); np.random.seed(42)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)

    model = make_model(cfg, device)
    X = P.generate_collocation_points(n_int=10000, device=device)
    n_params = model.count_parameters()
    print(f"  Parameters: {n_params}")

    loss_hist, err_hist, time_hist = [], [], []
    t0 = time.time()
    le = max(1, n_epochs // 50)
    opt_name = 'FullBatchLBFGS_Wolfe' if use_fb else 'PyTorch_LBFGS_strong_wolfe'

    if use_fb:
        print("  Using FullBatchLBFGS with Wolfe line search")
        opt = FullBatchLBFGS(model.parameters(), lr=1.0, history_size=3, line_search='Wolfe')
        def fb_closure():
            opt.zero_grad()
            return compute_loss(model, X, P, P.bc_transform)
        opt.zero_grad()
        loss_init = compute_loss(model, X, P, P.bc_transform)
        loss_init.backward()
        obj = loss_init
        stag = 0; prev = float('inf')

        for ep in range(n_epochs):
            options = {
                'closure': fb_closure, 'current_loss': obj, 'damping': True,
                'max_ls': 25, 'interpolate': True, 'inplace': True,
                'c1': 1e-4, 'c2': 0.9, 'eta': 2,
            }
            try:
                result = opt.step(options)
                if isinstance(result, tuple) and len(result) >= 8:
                    obj, grad, t_step, ls_step, _, _, desc_dir, fail = result
                    lv = obj.item() if isinstance(obj, torch.Tensor) else obj
                    if fail:
                        opt.zero_grad()
                        loss = compute_loss(model, X, P, P.bc_transform)
                        loss.backward()
                        obj = loss; lv = obj.item()
                else:
                    opt.zero_grad()
                    loss = compute_loss(model, X, P, P.bc_transform)
                    loss.backward()
                    obj = loss; lv = obj.item()
            except:
                opt.zero_grad()
                loss = compute_loss(model, X, P, P.bc_transform)
                loss.backward()
                obj = loss; lv = obj.item()

            el = time.time() - t0
            loss_hist.append(lv); time_hist.append(el)
            if abs(prev - lv) / (abs(prev) + 1e-30) < 1e-12: stag += 1
            else: stag = 0
            prev = lv
            if ep % le == 0 or ep == n_epochs - 1:
                e = compute_error(model, P, P.bc_transform, device=device, ref_interp=ref)
                err_hist.append(e)
                es = f", E_rel={e:.4e}" if e is not None else ""
                print(f"  L-BFGS {ep:5d}: loss={lv:.4e}{es} | {el:.1f}s")
            if stag >= 100:
                print(f"  Stagnated at epoch {ep}, resetting with lr/2")
                lr = opt.param_groups[0]['lr']
                opt = FullBatchLBFGS(model.parameters(), lr=lr*0.5, history_size=3, line_search='Wolfe')
                opt.zero_grad()
                loss = compute_loss(model, X, P, P.bc_transform)
                loss.backward()
                obj = loss; stag = 0
            if lv < 1e-14: break
    else:
        print("  Using PyTorch L-BFGS (strong_wolfe)")
        _train_pytorch_lbfgs(model, X, P, ref, device, n_epochs,
                             loss_hist, err_hist, time_hist, t0, le)

    ve = [e for e in err_hist if e is not None]
    return {
        'method': 'lbfgs_v2', 'problem': prob_name, 'optimizer': opt_name,
        'n_params': n_params,
        'final_loss': loss_hist[-1], 'min_loss': min(loss_hist),
        'final_error': err_hist[-1], 'min_error': min(ve) if ve else None,
        'total_time_s': time_hist[-1], 'n_epochs': len(loss_hist),
        'loss_history': subsample_list(loss_hist),
        'error_history': subsample_list(err_hist),
    }


def _train_pytorch_lbfgs(model, X, P, ref, device, n_epochs,
                          loss_hist, err_hist, time_hist, t0, le):
    opt = torch.optim.LBFGS(
        model.parameters(), max_iter=20, history_size=3, lr=1.0,
        line_search_fn='strong_wolfe',
        tolerance_grad=1e-16, tolerance_change=1e-16,
    )
    stag = 0; prev = float('inf')
    ep_offset = len(loss_hist)
    for ep in range(n_epochs):
        lv_holder = [0.0]
        def closure():
            opt.zero_grad()
            loss = compute_loss(model, X, P, P.bc_transform)
            loss.backward()
            lv_holder[0] = loss.item()
            return loss
        opt.step(closure)
        lv = lv_holder[0]
        el = time.time() - t0
        loss_hist.append(lv); time_hist.append(el)
        if abs(prev - lv) / (abs(prev) + 1e-30) < 1e-12: stag += 1
        else: stag = 0
        prev = lv
        actual_ep = ep_offset + ep
        if actual_ep % le == 0 or ep == n_epochs - 1:
            e = compute_error(model, P, P.bc_transform, device=device, ref_interp=ref)
            err_hist.append(e)
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  L-BFGS {actual_ep:5d}: loss={lv:.4e}{es} | {el:.1f}s")
        if stag >= 50:
            print(f"  Stagnated at epoch {actual_ep}, resetting with lr/2")
            opt = torch.optim.LBFGS(
                model.parameters(), max_iter=20, history_size=3,
                lr=opt.defaults['lr'] * 0.5,
                line_search_fn='strong_wolfe',
                tolerance_grad=1e-16, tolerance_change=1e-16)
            stag = 0
        if lv < 1e-14: break


# ============================================================
# SPQN with PyTorch L-BFGS (strong_wolfe)
# ============================================================
def train_spqn_v2(prob_name, mode, device, n_epochs=200, k_s=50):
    cfg = CONFIGS[prob_name]
    P = cfg['cls']
    ref = get_ref(prob_name)
    mname = "ASPQN" if mode == 'additive' else "MSPQN"

    torch.manual_seed(42); np.random.seed(42)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)

    model = make_model(cfg, device)
    X = P.generate_collocation_points(n_int=10000, device=device)
    n_params = model.count_parameters()
    print(f"  Parameters: {n_params}")

    layer_groups = model.get_layer_params()
    subdomains = layer_groups
    n_sd = len(subdomains)
    print(f"  Subdomains: {n_sd}, k_s: {k_s}")

    # Persistent global optimizer
    global_opt = torch.optim.LBFGS(
        model.parameters(), max_iter=20, history_size=3, lr=1.0,
        line_search_fn='strong_wolfe',
        tolerance_grad=1e-16, tolerance_change=1e-16,
    )

    loss_hist, err_hist, time_hist = [], [], []
    t0 = time.time()
    le = max(1, n_epochs // 25)
    spqn_stag = 0
    spqn_prev = float('inf')

    for ep in range(n_epochs):
        all_params = list(model.parameters())
        if mode == 'additive':
            saved = [p.data.clone() for p in all_params]
            updates = []
            for sd in subdomains:
                for p, s in zip(all_params, saved): p.data.copy_(s)
                _solve_local(model, sd, X, P, k_s=k_s)
                updates.append([(p.data - s).clone() for p, s in zip(all_params, saved)])
            for p, s in zip(all_params, saved): p.data.copy_(s)
            for upd in updates:
                for p, du in zip(all_params, upd): p.data.add_(du)
        else:
            for sd in subdomains:
                _solve_local(model, sd, X, P, k_s=k_s)

        lv_holder = [0.0]
        def g_closure():
            global_opt.zero_grad()
            loss = compute_loss(model, X, P, P.bc_transform)
            loss.backward()
            lv_holder[0] = loss.item()
            return loss
        global_opt.step(g_closure)
        lv = lv_holder[0]

        el = time.time() - t0
        loss_hist.append(lv); time_hist.append(el)

        if ep % le == 0 or ep == n_epochs - 1:
            e = compute_error(model, P, P.bc_transform, device=device, ref_interp=ref)
            err_hist.append(e)
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  {mname} {ep:5d}: loss={lv:.4e}{es} | {el:.1f}s")

        # Early stop on NaN
        if np.isnan(lv) or np.isinf(lv):
            print(f"  NaN/Inf detected at epoch {ep}, stopping early")
            break

        # Early stop on stagnation (30 epochs no change)
        if abs(spqn_prev - lv) / (abs(spqn_prev) + 1e-30) < 1e-10:
            spqn_stag += 1
        else:
            spqn_stag = 0
        spqn_prev = lv
        if spqn_stag >= 30:
            print(f"  SPQN stagnated for 30 epochs at epoch {ep}, stopping early")
            break

    ve = [e for e in err_hist if e is not None and not np.isnan(e)]
    vl = [l for l in loss_hist if not np.isnan(l) and not np.isinf(l)]
    return {
        'method': f'{mname.lower()}_v2', 'problem': prob_name,
        'optimizer': 'PyTorch_LBFGS_strong_wolfe',
        'n_params': n_params, 'n_subdomains': n_sd, 'k_s': k_s,
        'final_loss': loss_hist[-1] if loss_hist else None,
        'min_loss': min(vl) if vl else None,
        'final_error': err_hist[-1] if err_hist else None,
        'min_error': min(ve) if ve else None,
        'total_time_s': time_hist[-1] if time_hist else 0,
        'n_epochs': len(loss_hist),
        'loss_history': subsample_list(loss_hist),
        'error_history': subsample_list(err_hist),
        'note': 'Diverged to NaN' if (loss_hist and np.isnan(loss_hist[-1])) else None,
    }


def _solve_local(model, sd_params, X, P, k_s=50):
    all_p = list(model.parameters())
    sd_ids = {id(p) for p in sd_params}
    for p in all_p: p.requires_grad_(id(p) in sd_ids)
    active = [p for p in sd_params if p.requires_grad]
    if not active:
        for p in all_p: p.requires_grad_(True)
        return
    local_opt = torch.optim.LBFGS(
        active, max_iter=k_s, history_size=3, lr=1.0,
        line_search_fn='strong_wolfe',
        tolerance_grad=1e-16, tolerance_change=1e-16)
    def closure():
        local_opt.zero_grad()
        loss = compute_loss(model, X, P, P.bc_transform)
        loss.backward()
        return loss
    local_opt.step(closure)
    for p in all_p: p.requires_grad_(True)


# ============================================================
# Adam baseline
# ============================================================
def train_adam_v2(prob_name, device, n_epochs=50000):
    cfg = CONFIGS[prob_name]
    P = cfg['cls']
    ref = get_ref(prob_name)

    torch.manual_seed(42); np.random.seed(42)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)

    model = make_model(cfg, device)
    X = P.generate_collocation_points(n_int=10000, device=device)
    n_params = model.count_parameters()
    print(f"  Parameters: {n_params}")

    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=500, factor=0.5, min_lr=1e-6)

    loss_hist, err_hist, time_hist = [], [], []
    t0 = time.time()
    le = max(1, n_epochs // 25)

    for ep in range(n_epochs):
        opt.zero_grad()
        loss = compute_loss(model, X, P, P.bc_transform)
        loss.backward()
        opt.step()
        sched.step(loss.item())

        el = time.time() - t0
        lv = loss.item()
        loss_hist.append(lv); time_hist.append(el)

        if ep % le == 0 or ep == n_epochs - 1:
            e = compute_error(model, P, P.bc_transform, device=device, ref_interp=ref)
            err_hist.append(e)
            es = f", E_rel={e:.4e}" if e is not None else ""
            print(f"  Adam {ep:5d}: loss={lv:.4e}{es} | {el:.1f}s")

    ve = [e for e in err_hist if e is not None]
    return {
        'method': 'adam_v2', 'problem': prob_name, 'optimizer': 'Adam',
        'n_params': n_params,
        'final_loss': loss_hist[-1], 'min_loss': min(loss_hist),
        'final_error': err_hist[-1], 'min_error': min(ve) if ve else None,
        'total_time_s': time_hist[-1], 'n_epochs': len(loss_hist),
        'loss_history': subsample_list(loss_hist),
        'error_history': subsample_list(err_hist),
    }


# ============================================================
# Main
# ============================================================
EPOCH_CFG = {
    'klein_gordon': {'lbfgs': 3000, 'spqn': 200, 'adam': 20000},
    'burgers': {'lbfgs': 3000, 'spqn': 200, 'adam': 20000},
    'allen_cahn': {'lbfgs': 3000, 'spqn': 200, 'adam': 20000},
    'advection_diffusion': {'lbfgs': 2000, 'spqn': 100, 'adam': 20000},
}


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if torch.cuda.is_available(): print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"PyTorch: {torch.__version__}")
    print(f"FullBatchLBFGS available: {HAS_FBLBFGS}\n")

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    force = '--force' in sys.argv

    if len(args) >= 2:
        problems = [args[0]]
        methods = [args[1]] if args[1] != 'all' else ['lbfgs', 'mspqn', 'aspqn', 'adam']
    elif len(args) >= 1 and args[0] == 'all':
        problems = list(CONFIGS.keys())
        methods = ['lbfgs', 'mspqn', 'aspqn', 'adam']
    elif len(args) >= 1:
        problems = [args[0]]
        methods = ['lbfgs', 'mspqn', 'aspqn', 'adam']
    else:
        problems = list(CONFIGS.keys())
        methods = ['lbfgs', 'mspqn', 'aspqn', 'adam']

    all_results = {}

    for prob_name in problems:
        ec = EPOCH_CFG[prob_name]
        for method in methods:
            tag = f"{prob_name}_{method}"
            outfile = f"v2_{tag}.json"
            outpath = os.path.join(RESULTS_DIR, outfile)

            if os.path.exists(outpath) and not force:
                print(f"\n  Skipping {tag} (exists)")
                with open(outpath) as f: r = json.load(f)
                all_results[tag] = {
                    'min_loss': r.get('min_loss'), 'min_error': r.get('min_error'),
                    'time': r.get('total_time_s'),
                }
                continue

            print(f"\n{'='*70}")
            print(f"  {prob_name.upper()} | {method.upper()} | V2")
            print(f"{'='*70}")

            try:
                if method == 'lbfgs':
                    result = train_lbfgs_v2(prob_name, device, n_epochs=ec['lbfgs'])
                elif method == 'mspqn':
                    result = train_spqn_v2(prob_name, 'multiplicative', device,
                                           n_epochs=ec['spqn'], k_s=50)
                elif method == 'aspqn':
                    result = train_spqn_v2(prob_name, 'additive', device,
                                           n_epochs=ec['spqn'], k_s=50)
                elif method == 'adam':
                    result = train_adam_v2(prob_name, device, n_epochs=ec['adam'])
                else:
                    continue

                save_json(result, outfile)
                ml, me = result['min_loss'], result.get('min_error')
                mes = f"{me:.4e}" if me is not None else "N/A"
                print(f"\n  ✓ {tag}: min_loss={ml:.4e}, min_error={mes}, time={result['total_time_s']:.1f}s")
                all_results[tag] = {'min_loss': ml, 'min_error': me, 'time': result['total_time_s']}
            except Exception as e:
                print(f"\n  ✗ FAILED: {e}")
                traceback.print_exc()
                all_results[tag] = {'error': str(e)}

    # Summary
    print(f"\n\n{'='*70}")
    print("  FINAL SUMMARY — V2 Results")
    print(f"{'='*70}")
    for key in sorted(all_results.keys()):
        v = all_results[key]
        if 'error' in v:
            print(f"  {key:40s} | FAILED")
        else:
            me = v.get('min_error')
            es = f"E_rel={me:.4e}" if me is not None else "E_rel=N/A"
            print(f"  {key:40s} | loss={v['min_loss']:.4e} | {es} | {v['time']:.1f}s")

    save_json(all_results, 'v2_final_summary.json')
    print("\nDone!")


if __name__ == '__main__':
    main()
