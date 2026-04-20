"""
Kernel functions and occupation kernel computations.

Implements:
- Gaussian RBF kernel: K(x,y) = exp(-||x-y||^2 / mu)
- Exponential dot product kernel: K(x,y) = exp(x·y / mu)
- Occupation kernel: Gamma_gamma(x) = int_0^T K(x, gamma(t)) dt
- Gram matrix: G_ij = <Gamma_i, Gamma_j> = int int K(gamma_i(t), gamma_j(s)) ds dt
"""

import numpy as np
from scipy import integrate


def gaussian_rbf(x, y, mu=1.0):
    """Gaussian RBF kernel K(x,y) = exp(-||x-y||^2 / mu).
    
    x, y: arrays of shape (..., d) or (d,)
    Returns scalar or array of kernel values.
    """
    diff = np.asarray(x) - np.asarray(y)
    return np.exp(-np.sum(diff**2, axis=-1) / mu)


def exponential_dot(x, y, mu=1.0):
    """Exponential dot product kernel K(x,y) = exp(x·y / mu).
    
    x, y: arrays of shape (..., d) or (d,)
    """
    return np.exp(np.sum(np.asarray(x) * np.asarray(y), axis=-1) / mu)


def occupation_kernel_eval(x, trajectory, times, kernel_func, mu=1.0):
    """Evaluate occupation kernel Gamma_gamma(x) = int_0^T K(x, gamma(t)) dt.
    
    Uses Simpson's rule for numerical integration.
    
    Parameters
    ----------
    x : array (d,) - evaluation point
    trajectory : array (F+1, d) - trajectory points gamma(t_i)
    times : array (F+1,) - time points
    kernel_func : callable(x, y, mu) -> scalar
    mu : kernel width parameter
    
    Returns
    -------
    float - value of occupation kernel at x
    """
    x = np.asarray(x)
    # Evaluate kernel at all trajectory points
    k_vals = np.array([kernel_func(x, trajectory[i], mu) for i in range(len(times))])
    # Simpson's rule
    return integrate.simpson(k_vals, x=times)


def occupation_kernel_eval_vectorized(eval_points, trajectory, times, kernel_func, mu=1.0):
    """Evaluate occupation kernel at multiple points.
    
    Parameters
    ----------
    eval_points : array (M, d) - evaluation points
    trajectory : array (F+1, d) - trajectory points
    times : array (F+1,) - time points
    kernel_func : callable
    mu : kernel width
    
    Returns
    -------
    array (M,) - occupation kernel values at each eval point
    """
    M = len(eval_points)
    result = np.zeros(M)
    for i in range(M):
        result[i] = occupation_kernel_eval(eval_points[i], trajectory, times, kernel_func, mu)
    return result


def gram_matrix_entry(traj_i, times_i, traj_j, times_j, kernel_func, mu=1.0):
    """Compute Gram matrix entry G_ij = <Gamma_i, Gamma_j>_H.
    
    G_ij = int_0^T int_0^T K(gamma_i(t), gamma_j(s)) ds dt
    
    Uses 2D Simpson's rule.
    """
    # Build 2D kernel matrix K(gamma_i(t_k), gamma_j(s_l))
    n_i = len(times_i)
    n_j = len(times_j)
    K_mat = np.zeros((n_i, n_j))
    for k in range(n_i):
        for l in range(n_j):
            K_mat[k, l] = kernel_func(traj_i[k], traj_j[l], mu)
    
    # Integrate over s (inner integral) for each t_k
    inner = np.array([integrate.simpson(K_mat[k, :], x=times_j) for k in range(n_i)])
    # Integrate over t (outer integral)
    return integrate.simpson(inner, x=times_i)


def gram_matrix(trajectories, times_list, kernel_func, mu=1.0):
    """Compute full Gram matrix G where G_ij = <Gamma_i, Gamma_j>.
    
    Parameters
    ----------
    trajectories : list of arrays, each (F+1, d)
    times_list : list of arrays, each (F+1,)
    kernel_func : kernel function
    mu : kernel width
    
    Returns
    -------
    G : array (N, N)
    """
    N = len(trajectories)
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            val = gram_matrix_entry(trajectories[i], times_list[i],
                                    trajectories[j], times_list[j],
                                    kernel_func, mu)
            G[i, j] = val
            G[j, i] = val
    return G


def gram_matrix_fast(trajectories, times_list, kernel_func, mu=1.0):
    """Faster Gram matrix using vectorized kernel evaluations for Gaussian RBF.
    
    Uses composite Simpson's rule via scipy.integrate.simpson.
    """
    N = len(trajectories)
    G = np.zeros((N, N))
    
    for i in range(N):
        for j in range(i, N):
            ti = trajectories[i]  # (ni, d)
            tj = trajectories[j]  # (nj, d)
            # Compute pairwise kernel matrix
            diff = ti[:, np.newaxis, :] - tj[np.newaxis, :, :]  # (ni, nj, d)
            sq_dist = np.sum(diff**2, axis=-1)  # (ni, nj)
            K_mat = np.exp(-sq_dist / mu)
            
            # 2D Simpson integration - vectorized inner integral
            # integrate.simpson along axis=1 for all rows at once
            inner = integrate.simpson(K_mat, x=times_list[j], axis=1)
            val = integrate.simpson(inner, x=times_list[i])
            G[i, j] = val
            G[j, i] = val
    return G


def occupation_kernel_eval_batch(eval_points, trajectory, times, mu=1.0):
    """Evaluate Gaussian RBF occupation kernel at multiple points - fully vectorized.
    
    Parameters
    ----------
    eval_points : array (M, d)
    trajectory : array (F+1, d)
    times : array (F+1,)
    mu : kernel width
    
    Returns
    -------
    array (M,) - occupation kernel values
    """
    # eval_points: (M, d), trajectory: (F, d)
    # diff: (M, F, d)
    diff = eval_points[:, np.newaxis, :] - trajectory[np.newaxis, :, :]
    sq_dist = np.sum(diff**2, axis=-1)  # (M, F)
    K_mat = np.exp(-sq_dist / mu)
    # Integrate over trajectory time for each eval point
    return integrate.simpson(K_mat, x=times, axis=1)


def rhs_vector(trajectories, times_list, displacements, F_hat, kernel_func, mu=1.0):
    """Compute RHS vector b_i = D_i + <F_hat, Gamma_i>.
    
    For each component (x, y separately).
    
    Parameters
    ----------
    trajectories : list of arrays (F+1, d)
    times_list : list of arrays (F+1,)  
    displacements : array (N, d) - D_i vectors
    F_hat : callable(x) -> (d,) - current flow estimate (or None for zero)
    kernel_func, mu : kernel parameters
    
    Returns
    -------
    b : array (N, d) - RHS vectors
    """
    N = len(trajectories)
    d = displacements.shape[1]
    b = np.zeros((N, d))
    
    for i in range(N):
        b[i] = displacements[i].copy()
        if F_hat is not None:
            # Compute <F_hat, Gamma_i> = int_0^T F_hat(gamma_i(t)) dt
            F_vals = np.array([F_hat(trajectories[i][k]) for k in range(len(times_list[i]))])
            for comp in range(d):
                b[i, comp] += integrate.simpson(F_vals[:, comp], x=times_list[i])
    return b
