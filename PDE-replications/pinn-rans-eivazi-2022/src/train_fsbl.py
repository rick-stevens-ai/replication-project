"""
Train PINN for Falkner-Skan boundary layer (FSBL) case.
Laminar flow, Re=100, m=-0.08 (APG).

Key paper details:
- FNN: 8 hidden layers, 20 neurons each, tanh
- Training: Adam then BFGS
- Only velocity on boundaries (no pressure)
- Paper errors: EU=0.07%, EV=0.12%, EP=0.001%
"""

import numpy as np
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

from falkner_skan import generate_2d_field
from pinn_rans import RANSSolver, relative_l2_error


def main():
    m = -0.08
    Re = 100
    x_range = (1.0, 25.0)
    y_max = 5.0
    nx, ny = 200, 100
    
    config = {
        'mode': 'laminar',
        'Re': Re,
        'n_hidden': 8,
        'n_neurons': 20,
        'adam_lr': 1e-3,
        'adam_epochs': 20000,
        'lbfgs_epochs': 3000,
        'device': 'cuda' if __import__('torch').cuda.is_available() else 'cpu',
    }
    
    print("=" * 60)
    print("FSBL — Falkner-Skan Boundary Layer")
    print(f"Re={Re}, m={m}, beta_FS={2*m/(m+1):.4f}")
    print(f"Device: {config['device']}")
    print("=" * 60)
    
    # ---- Generate reference data ----
    print("\nGenerating reference data...")
    X, Y, U_ref, V_ref, P_ref, eta = generate_2d_field(m, Re, x_range, y_max, nx, ny)
    
    print(f"Grid: {X.shape}")
    print(f"U: [{U_ref.min():.6f}, {U_ref.max():.6f}]")
    print(f"V: [{V_ref.min():.6f}, {V_ref.max():.6f}]")
    print(f"P: [{P_ref.min():.6f}, {P_ref.max():.6f}]")
    
    # ---- Extract boundary data ----
    # Paper: "only the data on the domain boundaries for the velocity components"
    # Bottom (y=0)
    x_bot, y_bot = X[0, :], Y[0, :]
    # Top (y=y_max) 
    x_top, y_top = X[-1, :], Y[-1, :]
    # Left (x=x_min)
    x_left, y_left = X[:, 0], Y[:, 0]
    # Right (x=x_max)
    x_right, y_right = X[:, -1], Y[:, -1]
    
    x_bc = np.concatenate([x_bot, x_top, x_left, x_right]).ravel()
    y_bc = np.concatenate([y_bot, y_top, y_left, y_right]).ravel()
    
    u_U = np.concatenate([U_ref[0,:], U_ref[-1,:], U_ref[:,0], U_ref[:,-1]]).ravel()
    u_V = np.concatenate([V_ref[0,:], V_ref[-1,:], V_ref[:,0], V_ref[:,-1]]).ravel()
    # P is NOT provided as BC data (paper explicitly says "only velocity components")
    u_P = np.full_like(u_U, np.nan)
    u_bc = np.column_stack([u_U, u_V, u_P])
    
    print(f"Boundary points: {len(x_bc)}")
    
    # ---- Collocation points ----
    n_colloc = 20000
    np.random.seed(42)
    x_pde = np.random.uniform(x_range[0], x_range[1], n_colloc)
    y_pde = np.random.uniform(0, y_max, n_colloc)
    
    # ---- Setup and train ----
    solver = RANSSolver(config)
    lb = np.array([x_range[0], 0.0])
    ub = np.array([x_range[1], y_max])
    solver.setup_model(lb, ub)
    solver.set_data(x_bc, y_bc, u_bc, x_pde, y_pde)
    
    t_start = time.time()
    solver.train_adam(print_every=2000)
    solver.train_lbfgs(print_every=500)
    t_total = time.time() - t_start
    
    # ---- Evaluate ----
    print("\n--- Evaluation ---")
    x_eval = X.ravel()
    y_eval = Y.ravel()
    u_ref_flat = np.column_stack([U_ref.ravel(), V_ref.ravel(), P_ref.ravel()])
    
    errors = solver.compute_errors(x_eval, y_eval, u_ref_flat)
    
    print(f"\nRelative L2 errors (%):")
    for k, v in errors.items():
        print(f"  E_{k}: {v:.4f}%")
    
    paper_errors = {'U': 0.07, 'V': 0.12, 'P': 0.001}
    print(f"\nPaper values:")
    for k, v in paper_errors.items():
        our = errors.get(k, float('nan'))
        print(f"  E_{k}: paper={v}%, ours={our:.4f}%")
    
    print(f"\nTotal training time: {t_total:.1f}s")
    
    # ---- Save ----
    outdir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(outdir, exist_ok=True)
    
    pred = solver.predict(x_eval, y_eval)
    np.savez(os.path.join(outdir, 'fsbl_results.npz'),
             X=X, Y=Y,
             U_ref=U_ref, V_ref=V_ref, P_ref=P_ref,
             U_pred=pred[:, 0].reshape(X.shape),
             V_pred=pred[:, 1].reshape(X.shape),
             P_pred=pred[:, 2].reshape(X.shape),
             errors=errors, training_time=t_total)
    
    solver.save(os.path.join(outdir, 'fsbl_model.pt'))
    
    results = {
        'case': 'FSBL',
        'errors': {k: float(v) for k, v in errors.items()},
        'paper_errors': paper_errors,
        'training_time_s': t_total,
        'config': {k: str(v) if not isinstance(v, (int, float, str, bool)) else v 
                   for k, v in config.items()},
        'n_bc': len(x_bc),
        'n_colloc': n_colloc,
    }
    with open(os.path.join(outdir, 'fsbl_summary.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {outdir}")
    return results


if __name__ == '__main__':
    main()
