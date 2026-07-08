"""
Flow field reconstruction via occupation kernels.

Implements Algorithm 1 from the paper (iterative motion tomography).
"""

import numpy as np
from scipy import integrate

from .kernels import (gram_matrix_fast, gaussian_rbf, occupation_kernel_eval,
                      gram_matrix_entry, occupation_kernel_eval_batch)
from .trajectories import (generate_trajectory_with_estimate,
                           generate_dead_reckoned_trajectory)


class FlowReconstructor:
    """Iterative motion tomography via occupation kernels.
    
    Parameters
    ----------
    kernel_func : callable(x, y, mu) -> scalar
    mu : float - kernel width
    lam : float - regularization parameter (Tikhonov)
    n_steps : int - trajectory integration steps
    """
    
    def __init__(self, kernel_func=gaussian_rbf, mu=1.0, lam=0.0, n_steps=100):
        self.kernel_func = kernel_func
        self.mu = mu
        self.lam = lam
        self.n_steps = n_steps
        
        # After fitting
        self.weights = None  # (N, 2) - weights for each component
        self.trajectories = None  # list of trajectory arrays
        self.times_list = None
    
    def _build_flow_estimator(self, weights, trajectories, times_list):
        """Build callable flow field estimate from weights and trajectories.
        
        Handles both single point (d,) and batch (M, d) inputs.
        """
        mu = self.mu
        
        def F_hat(x):
            x = np.asarray(x, dtype=float)
            scalar = (x.ndim == 1)
            if scalar:
                x = x.reshape(1, 2)
            
            M = len(x)
            result = np.zeros((M, 2))
            for i in range(len(trajectories)):
                ok_vals = occupation_kernel_eval_batch(
                    x, trajectories[i], times_list[i], mu)
                result[:, 0] += weights[i, 0] * ok_vals
                result[:, 1] += weights[i, 1] * ok_vals
            
            if scalar:
                return result[0]
            return result
        return F_hat
    
    def fit_iterative(self, r0s, speeds, thetas, true_endpoints, T=1.0, 
                      n_iterations=10, verbose=False):
        """Run Algorithm 1: iterative motion tomography.
        
        Parameters
        ----------
        r0s : array (N, 2) - initial positions
        speeds : array (N,) or float - vehicle speeds
        thetas : array (N,) - heading angles
        true_endpoints : array (N, 2) - observed final positions r_i(T)
        T : float - time horizon
        n_iterations : int - number of iterations
        verbose : bool
        
        Returns
        -------
        F_hat : callable - estimated flow field
        errors : list - mean errors per iteration
        """
        N = len(r0s)
        if np.isscalar(speeds):
            speeds = np.full(N, speeds)
        
        # Initialize: F_hat_0 = 0
        F_hat = lambda x: np.zeros(2)
        errors_history = []
        
        for n in range(n_iterations):
            # Step 1: Generate trajectories under current estimate
            trajectories = []
            times_list = []
            for i in range(N):
                if n == 0:
                    traj, times = generate_dead_reckoned_trajectory(
                        r0s[i], speeds[i], thetas[i], T, self.n_steps)
                else:
                    traj, times = generate_trajectory_with_estimate(
                        r0s[i], speeds[i], thetas[i], F_hat, T, self.n_steps)
                trajectories.append(traj)
                times_list.append(times)
            
            # Step 2: Compute displacements
            displacements = np.zeros((N, 2))
            for i in range(N):
                displacements[i] = true_endpoints[i] - trajectories[i][-1]
            
            # Step 3: Build Gram matrix
            G = gram_matrix_fast(trajectories, times_list, self.kernel_func, self.mu)
            
            # Add regularization
            G_reg = G + self.lam * np.eye(N)
            
            # Step 4: Build RHS and solve for each component
            weights = np.zeros((N, 2))
            for comp in range(2):
                b = displacements[:, comp].copy()
                if n > 0:
                    # Add <F_hat_n, Gamma_i> term - vectorized eval
                    for i in range(N):
                        F_vals = F_hat(trajectories[i])  # (n_steps+1, 2)
                        b[i] += integrate.simpson(F_vals[:, comp], x=times_list[i])
                
                weights[:, comp] = np.linalg.solve(G_reg, b)
            
            # Build new F_hat
            F_hat = self._build_flow_estimator(weights, trajectories, times_list)
            
            # Track convergence
            mean_disp = np.mean(np.linalg.norm(displacements, axis=1))
            if verbose:
                print(f"  Iteration {n+1}/{n_iterations}: mean displacement = {mean_disp:.6f}")
            errors_history.append(mean_disp)
        
        self.weights = weights
        self.trajectories = trajectories
        self.times_list = times_list
        
        return F_hat, errors_history
    
    def fit_single_step(self, trajectories, times_list, displacements):
        """Single-step reconstruction (no iteration, for simple tests).
        
        Solves (G + λI) w = D for each component.
        """
        N = len(trajectories)
        G = gram_matrix_fast(trajectories, times_list, self.kernel_func, self.mu)
        G_reg = G + self.lam * np.eye(N)
        
        weights = np.zeros((N, 2))
        for comp in range(2):
            weights[:, comp] = np.linalg.solve(G_reg, displacements[:, comp])
        
        self.weights = weights
        self.trajectories = trajectories
        self.times_list = times_list
        
        F_hat = self._build_flow_estimator(weights, trajectories, times_list)
        
        return F_hat, None
    
    def evaluate_on_grid(self, xlim=(0, 1), ylim=(0, 1), nx=20, ny=20):
        """Evaluate current estimate on a grid (vectorized)."""
        xg = np.linspace(xlim[0], xlim[1], nx)
        yg = np.linspace(ylim[0], ylim[1], ny)
        X, Y = np.meshgrid(xg, yg)
        
        F_hat = self._build_flow_estimator(
            self.weights, self.trajectories, self.times_list)
        
        points = np.stack([X.ravel(), Y.ravel()], axis=-1)
        F_vals = F_hat(points)  # (nx*ny, 2)
        U = F_vals[:, 0].reshape(ny, nx)
        V = F_vals[:, 1].reshape(ny, nx)
        
        return X, Y, U, V


def compute_errors(true_func, est_func, xlim=(0, 1), ylim=(0, 1), nx=20, ny=20):
    """Compute error metrics between true and estimated flow fields.
    
    Returns
    -------
    dict with: max_error, mean_error, rmse, rel_l2_error
    """
    xg = np.linspace(xlim[0], xlim[1], nx)
    yg = np.linspace(ylim[0], ylim[1], ny)
    X, Y = np.meshgrid(xg, yg)
    
    points = np.stack([X.ravel(), Y.ravel()], axis=-1)
    M = len(points)
    
    # Try batch evaluation, fall back to point-by-point
    try:
        v_true = np.asarray(true_func(points))
        if v_true.shape != (M, 2):
            raise ValueError
    except (ValueError, TypeError):
        v_true = np.array([true_func(p) for p in points])
    
    try:
        v_est = np.asarray(est_func(points))
        if v_est.shape != (M, 2):
            raise ValueError
    except (ValueError, TypeError):
        v_est = np.array([est_func(p) for p in points])
    
    error_norms = np.linalg.norm(v_true - v_est, axis=1)
    true_norms = np.linalg.norm(v_true, axis=1)
    
    # Relative errors (avoiding division by zero)
    mask = true_norms > 1e-12
    rel_errors = np.zeros_like(error_norms)
    rel_errors[mask] = error_norms[mask] / true_norms[mask]
    
    total_true = np.sqrt(np.sum(true_norms**2))
    total_err = np.sqrt(np.sum(error_norms**2))
    
    return {
        'max_error': np.max(rel_errors[mask]) if np.any(mask) else 0.0,
        'mean_error': np.mean(rel_errors[mask]) if np.any(mask) else 0.0,
        'rmse': np.sqrt(np.mean(error_norms**2)),
        'rel_l2_error': total_err / total_true if total_true > 0 else 0.0,
        'max_abs_error': np.max(error_norms),
        'mean_abs_error': np.mean(error_norms),
    }
