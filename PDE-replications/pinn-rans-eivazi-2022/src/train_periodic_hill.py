"""
Train PINN for periodic hill case.
Re_b = 2800, full RANS with all Reynolds stress components.
"""

import numpy as np
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

from generate_periodic_hill import generate_periodic_hill_field
from pinn_rans import RANSSolver, relative_l2_error


def main():
    config = {
        'mode': 'rans_full',
        'Re': 2800,
        'n_hidden': 8,
        'n_neurons': 20,
        'adam_lr': 1e-3,
        'adam_epochs': 20000,
        'lbfgs_epochs': 15000,
        'device': 'cuda' if __import__('torch').cuda.is_available() else 'cpu',
    }
    
    print("=" * 60)
    print("Periodic Hill — Turbulent Flow over Periodic Hill")
    print(f"Re_b = 2800, Device: {config['device']}")
    print("=" * 60)
    
    # Generate reference data
    print("\nGenerating reference data...")
    X, Y, U_ref, V_ref, P_ref, uu_ref, uv_ref, vv_ref, params = \
        generate_periodic_hill_field(nx=120, ny=60)
    
    nu = params['nu']
    config['Re'] = 1.0 / nu
    
    # Extract boundaries
    # Bottom (y=0)
    x_bot, y_bot = X[0, :].ravel(), Y[0, :].ravel()
    u_bot = np.column_stack([U_ref[0, :].ravel(), V_ref[0, :].ravel(), P_ref[0, :].ravel(),
                             uu_ref[0, :].ravel(), uv_ref[0, :].ravel(), vv_ref[0, :].ravel()])
    
    # Top
    x_top, y_top = X[-1, :].ravel(), Y[-1, :].ravel()
    u_top = np.column_stack([U_ref[-1, :].ravel(), V_ref[-1, :].ravel(), P_ref[-1, :].ravel(),
                             uu_ref[-1, :].ravel(), uv_ref[-1, :].ravel(), vv_ref[-1, :].ravel()])
    
    # Left (inlet)
    x_left, y_left = X[:, 0].ravel(), Y[:, 0].ravel()
    u_left = np.column_stack([U_ref[:, 0].ravel(), V_ref[:, 0].ravel(), P_ref[:, 0].ravel(),
                              uu_ref[:, 0].ravel(), uv_ref[:, 0].ravel(), vv_ref[:, 0].ravel()])
    
    # Right (outlet)
    x_right, y_right = X[:, -1].ravel(), Y[:, -1].ravel()
    u_right = np.column_stack([U_ref[:, -1].ravel(), V_ref[:, -1].ravel(), P_ref[:, -1].ravel(),
                               uu_ref[:, -1].ravel(), uv_ref[:, -1].ravel(), vv_ref[:, -1].ravel()])
    
    x_bc = np.concatenate([x_bot, x_top, x_left, x_right])
    y_bc = np.concatenate([y_bot, y_top, y_left, y_right])
    u_bc = np.vstack([u_bot, u_top, u_left, u_right])
    
    # Collocation points
    n_colloc = 15000
    np.random.seed(42)
    x_pde = np.random.uniform(X.min(), X.max(), n_colloc)
    y_pde = np.random.uniform(Y.min(), Y.max(), n_colloc)
    
    # Setup solver
    solver = RANSSolver(config)
    lb = np.array([X.min(), Y.min()])
    ub = np.array([X.max(), Y.max()])
    solver.setup_model(lb, ub)
    solver.set_data(x_bc, y_bc, u_bc, x_pde, y_pde)
    
    t_start = time.time()
    solver.train_adam(print_every=2000)
    solver.train_lbfgs(print_every=1000)
    t_total = time.time() - t_start
    
    # Evaluate
    print("\n--- Evaluation ---")
    x_eval = X.ravel()
    y_eval = Y.ravel()
    u_ref_flat = np.column_stack([U_ref.ravel(), V_ref.ravel(), P_ref.ravel(),
                                  uu_ref.ravel(), uv_ref.ravel(), vv_ref.ravel()])
    
    errors = solver.compute_errors(x_eval, y_eval, u_ref_flat)
    
    print(f"\nRelative L2 errors (%):")
    for k, v in errors.items():
        print(f"  E_{k}: {v:.4f}%")
    
    paper_errors = {'U': 2.77, 'V': 19.70, 'P': 8.61, 'uu': 28.18, 'uv': 16.70, 'vv': 20.24}
    print(f"\nPaper values:")
    for k, v in paper_errors.items():
        our = errors.get(k, float('nan'))
        print(f"  E_{k}: paper={v}%, ours={our:.4f}%")
    
    print(f"\nTraining time: {t_total:.1f}s")
    
    # Save
    outdir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(outdir, exist_ok=True)
    
    pred = solver.predict(x_eval, y_eval)
    np.savez(os.path.join(outdir, 'periodic_hill_results.npz'),
             X=X, Y=Y,
             U_ref=U_ref, V_ref=V_ref, P_ref=P_ref,
             uu_ref=uu_ref, uv_ref=uv_ref, vv_ref=vv_ref,
             U_pred=pred[:, 0].reshape(X.shape),
             V_pred=pred[:, 1].reshape(X.shape),
             P_pred=pred[:, 2].reshape(X.shape),
             uu_pred=pred[:, 3].reshape(X.shape),
             uv_pred=pred[:, 4].reshape(X.shape),
             vv_pred=pred[:, 5].reshape(X.shape),
             errors=errors, training_time=t_total)
    
    solver.save(os.path.join(outdir, 'periodic_hill_model.pt'))
    
    results = {
        'case': 'Periodic Hill',
        'errors': {k: float(v) for k, v in errors.items()},
        'paper_errors': paper_errors,
        'training_time_s': t_total,
        'n_bc': len(x_bc),
        'n_colloc': n_colloc,
    }
    with open(os.path.join(outdir, 'periodic_hill_summary.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    return results


if __name__ == '__main__':
    main()
