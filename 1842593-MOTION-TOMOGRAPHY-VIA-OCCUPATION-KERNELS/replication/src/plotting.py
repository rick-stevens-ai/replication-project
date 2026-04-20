"""
Plotting utilities for motion tomography replication.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def plot_flow_field(X, Y, U, V, ax=None, title='', trajectories=None, 
                    color='black', scale=None, alpha=1.0):
    """Plot a flow field as quiver plot.
    
    Parameters
    ----------
    X, Y : meshgrid arrays
    U, V : flow components
    ax : matplotlib axis (creates new if None)
    title : str
    trajectories : list of (n, 2) arrays to overlay
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    
    ax.quiver(X, Y, U, V, color=color, scale=scale, alpha=alpha)
    
    if trajectories is not None:
        for traj in trajectories:
            ax.plot(traj[:, 0], traj[:, 1], 'b-', alpha=0.3, linewidth=0.5)
            ax.plot(traj[0, 0], traj[0, 1], 'go', markersize=2)
            ax.plot(traj[-1, 0], traj[-1, 1], 'ro', markersize=2)
    
    ax.set_title(title)
    ax.set_aspect('equal')
    return ax


def plot_comparison(X_true, Y_true, U_true, V_true,
                    X_est, Y_est, U_est, V_est,
                    true_trajs=None, title_true='True Flow Field',
                    title_est='Estimated Flow Field',
                    save_path=None):
    """Side-by-side comparison of true and estimated flow fields."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    plot_flow_field(X_true, Y_true, U_true, V_true, ax=ax1, title=title_true,
                    trajectories=true_trajs)
    plot_flow_field(X_est, Y_est, U_est, V_est, ax=ax2, title=title_est)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    return fig


def plot_error_field(X, Y, U_true, V_true, U_est, V_est, title='Error Field',
                     save_path=None):
    """Plot error vectors between true and estimated fields."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    U_err = U_true - U_est
    V_err = V_true - V_est
    err_mag = np.sqrt(U_err**2 + V_err**2)
    
    ax1.quiver(X, Y, U_err, V_err, color='red')
    ax1.set_title(title)
    ax1.set_aspect('equal')
    
    c = ax2.pcolormesh(X, Y, err_mag, cmap='hot', shading='auto')
    plt.colorbar(c, ax=ax2)
    ax2.set_title('Error Magnitude')
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    return fig


def plot_convergence(errors_dict, xlabel='Iteration', ylabel='Mean Error',
                     title='Convergence', save_path=None):
    """Plot convergence curves for multiple flow fields."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    for idx, (label, errors) in enumerate(errors_dict.items()):
        ax.plot(range(1, len(errors)+1), errors, 
                marker=markers[idx % len(markers)],
                color=colors[idx % len(colors)],
                label=label, linewidth=2, markersize=6)
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    return fig


def plot_parameter_sweep(param_values, errors, param_name='Parameter',
                         title='Parameter Sweep', save_path=None, log_x=False):
    """Plot error vs parameter value (for σ, λ sweeps)."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    if log_x:
        ax.semilogx(param_values, errors, 'bo-', linewidth=2, markersize=6)
    else:
        ax.plot(param_values, errors, 'bo-', linewidth=2, markersize=6)
    
    ax.set_xlabel(param_name, fontsize=12)
    ax.set_ylabel('Mean Relative Error', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    return fig
