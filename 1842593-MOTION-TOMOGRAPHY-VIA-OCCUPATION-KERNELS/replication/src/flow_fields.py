"""
Synthetic flow fields for testing motion tomography.

Implements:
1. Flow field from paper Eq (14) - Gaussian bump mixture
2. Linear flow field: f1=x2, f2=-0.2*x1
3. Constant flow field: f1=0.2, f2=0.1
"""

import numpy as np


def flow_field_paper(x):
    """Flow field from paper Eq (14).
    
    F(x) = (1/8) * [f1(x), f2(x)]
    
    Parameters
    ----------
    x : array (..., 2) or (2,)
    
    Returns
    -------
    F : array (..., 2) or (2,)
    """
    x = np.asarray(x, dtype=float)
    scalar = (x.ndim == 1)
    if scalar:
        x = x.reshape(1, 2)
    
    x1, x2 = x[..., 0], x[..., 1]
    
    # Centers
    c1 = np.array([0.25, 0.25])
    c2 = np.array([0.25, 0.75])
    c3 = np.array([0.75, 0.75])
    c4 = np.array([0.75, 0.25])
    
    def dist2(pts, center):
        return (pts[..., 0] - center[0])**2 + (pts[..., 1] - center[1])**2
    
    d1 = dist2(x, c1)
    d2 = dist2(x, c2)
    d3 = dist2(x, c3)
    d4 = dist2(x, c4)
    
    f1 = (5 * np.exp(-2 * d1) 
          - 0.2 * np.exp(-d2)
          + 2 * np.exp(-d3)
          - 5 * np.exp(-2 * d4))
    
    f2 = (3 * np.exp(-d1)
          + np.exp(-d2)
          - 3 * np.exp(-3 * d3)
          + np.exp(-d4))
    
    result = np.stack([f1, f2], axis=-1) / 8.0
    
    if scalar:
        return result[0]
    return result


def flow_field_linear(x):
    """Linear flow field: f1=x2, f2=-0.2*x1."""
    x = np.asarray(x, dtype=float)
    scalar = (x.ndim == 1)
    if scalar:
        x = x.reshape(1, 2)
    
    result = np.stack([x[..., 1], -0.2 * x[..., 0]], axis=-1)
    if scalar:
        return result[0]
    return result


def flow_field_constant(x):
    """Constant flow field: f1=0.2, f2=0.1."""
    x = np.asarray(x, dtype=float)
    scalar = (x.ndim == 1)
    if scalar:
        return np.array([0.2, 0.1])
    return np.broadcast_to(np.array([0.2, 0.1]), x.shape).copy()


def evaluate_on_grid(flow_func, xlim=(0, 1), ylim=(0, 1), nx=20, ny=20):
    """Evaluate flow field on a regular grid.
    
    Returns
    -------
    X, Y : meshgrid arrays (ny, nx)
    U, V : flow components (ny, nx)
    """
    xg = np.linspace(xlim[0], xlim[1], nx)
    yg = np.linspace(ylim[0], ylim[1], ny)
    X, Y = np.meshgrid(xg, yg)
    
    points = np.stack([X.ravel(), Y.ravel()], axis=-1)
    F = flow_func(points)
    U = F[:, 0].reshape(ny, nx)
    V = F[:, 1].reshape(ny, nx)
    
    return X, Y, U, V
