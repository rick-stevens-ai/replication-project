"""
Trajectory generation for motion tomography.

Generates trajectories of the form:
    dr/dt = s * [cos(theta), sin(theta)] + F(r)

where s is speed, theta is heading angle, and F is the unknown flow field.
Dead-reckoned trajectories use F=0.
"""

import numpy as np
from scipy.integrate import solve_ivp


def generate_true_trajectory(r0, speed, theta, flow_func, T=1.0, n_steps=100):
    """Generate true trajectory under flow field.
    
    dr/dt = s*[cos(theta), sin(theta)] + F(r)
    
    Parameters
    ----------
    r0 : array (2,) - initial position
    speed : float - vehicle speed
    theta : float - heading angle (radians)
    flow_func : callable(x) -> (2,) - flow field
    T : float - final time
    n_steps : int - number of output time steps
    
    Returns
    -------
    trajectory : array (n_steps+1, 2)
    times : array (n_steps+1,)
    """
    def rhs(t, r):
        drift = speed * np.array([np.cos(theta), np.sin(theta)])
        return drift + flow_func(r)
    
    times = np.linspace(0, T, n_steps + 1)
    sol = solve_ivp(rhs, [0, T], r0, t_eval=times, method='RK45', 
                    rtol=1e-10, atol=1e-12)
    
    return sol.y.T, sol.t


def generate_dead_reckoned_trajectory(r0, speed, theta, T=1.0, n_steps=100):
    """Generate dead-reckoned (anticipated) trajectory with no flow.
    
    dr_tilde/dt = s*[cos(theta), sin(theta)]
    
    This is a straight line.
    """
    times = np.linspace(0, T, n_steps + 1)
    drift = speed * np.array([np.cos(theta), np.sin(theta)])
    trajectory = r0[np.newaxis, :] + np.outer(times, drift)
    return trajectory, times


def generate_trajectory_with_estimate(r0, speed, theta, F_hat, T=1.0, n_steps=100):
    """Generate trajectory under estimated flow field F_hat.
    
    dr/dt = s*[cos(theta), sin(theta)] + F_hat(r)
    """
    def rhs(t, r):
        drift = speed * np.array([np.cos(theta), np.sin(theta)])
        return drift + F_hat(r)
    
    times = np.linspace(0, T, n_steps + 1)
    sol = solve_ivp(rhs, [0, T], r0, t_eval=times, method='RK45',
                    rtol=1e-10, atol=1e-12)
    
    return sol.y.T, sol.t


def generate_random_trajectories(n_trajs, flow_func, domain=(0, 1, 0, 1),
                                  T=1.0, n_steps=100, speed=1.0, seed=42):
    """Generate multiple random trajectories.
    
    Parameters
    ----------
    n_trajs : int
    flow_func : callable
    domain : tuple (x_min, x_max, y_min, y_max)
    T : float
    n_steps : int
    speed : float
    seed : int
    
    Returns
    -------
    true_trajs : list of (n_steps+1, 2) arrays
    dr_trajs : list of (n_steps+1, 2) arrays (dead-reckoned)
    times_list : list of (n_steps+1,) arrays
    displacements : array (n_trajs, 2)
    r0s : array (n_trajs, 2) - initial positions
    thetas : array (n_trajs,) - heading angles
    """
    rng = np.random.RandomState(seed)
    x_min, x_max, y_min, y_max = domain
    
    r0s = np.column_stack([
        rng.uniform(x_min, x_max, n_trajs),
        rng.uniform(y_min, y_max, n_trajs)
    ])
    thetas = rng.uniform(0, 2 * np.pi, n_trajs)
    
    true_trajs = []
    dr_trajs = []
    times_list = []
    displacements = np.zeros((n_trajs, 2))
    
    for i in range(n_trajs):
        true_traj, times = generate_true_trajectory(
            r0s[i], speed, thetas[i], flow_func, T, n_steps)
        dr_traj, _ = generate_dead_reckoned_trajectory(
            r0s[i], speed, thetas[i], T, n_steps)
        
        true_trajs.append(true_traj)
        dr_trajs.append(dr_traj)
        times_list.append(times)
        displacements[i] = true_traj[-1] - dr_traj[-1]
    
    return true_trajs, dr_trajs, times_list, displacements, r0s, thetas
