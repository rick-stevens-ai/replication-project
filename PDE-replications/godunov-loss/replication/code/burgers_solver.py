"""
High-resolution finite-volume Godunov solver for 1D inviscid Burgers equation.
  u_t + (u^2/2)_x = 0
Uses exact Godunov flux (trivial for scalar convex flux) with MUSCL reconstruction.

Reference ground truth generator for the Godunov-loss replication study.
Paper: Cassia & Kerswell, "Godunov Loss Functions for Modelling of Hyperbolic
Conservation Laws", CMAME 2024/2025, arXiv:2405.11674.
"""

import numpy as np
import json
import os


def godunov_flux_burgers(uL, uR):
    """
    Exact Godunov flux for Burgers equation f(u) = u^2/2.
    For convex flux:
      F = max(f(uL), f(uR))  if uL > uR  (shock)
      F = min(f(uL), f(uR))  if uL <= uR but need to check sonic
    Exact formula (Toro, Riemann Solvers ch. 6):
      if uL >= uR (shock/compression):
          s = (uL + uR)/2   (shock speed)
          F = f(uL) if s >= 0, else f(uR)
      if uL < uR (rarefaction):
          if uL >= 0: F = f(uL)
          elif uR <= 0: F = f(uR)
          else: F = 0  (sonic point, f(0) = 0)
    """
    fL = 0.5 * uL ** 2
    fR = 0.5 * uR ** 2

    F = np.where(
        uL >= uR,
        # Shock case
        np.where((uL + uR) / 2.0 >= 0, fL, fR),
        # Rarefaction case
        np.where(uL >= 0, fL, np.where(uR <= 0, fR, 0.0))
    )
    return F


def minmod(a, b):
    """Minmod slope limiter."""
    return np.where(
        a * b > 0,
        np.where(np.abs(a) < np.abs(b), a, b),
        0.0
    )


def solve_burgers_godunov(u0, x, T, cfl=0.5, order=1):
    """
    Solve 1D Burgers with Godunov flux.
    
    Args:
        u0: initial condition array (Nx,)
        x: cell centers (Nx,)
        T: final time
        cfl: CFL number
        order: 1 or 2 (MUSCL reconstruction)
    
    Returns:
        u_final: solution at time T
        t_history: list of times
        u_history: list of solution snapshots
    """
    dx = x[1] - x[0]
    Nx = len(x)
    u = u0.copy()
    t = 0.0
    
    t_history = [0.0]
    u_history = [u.copy()]
    
    while t < T - 1e-14:
        # CFL condition
        amax = np.max(np.abs(u)) + 1e-10
        dt = cfl * dx / amax
        dt = min(dt, T - t)
        
        if order == 1:
            # Piecewise constant: uL_{i+1/2} = u_i, uR_{i+1/2} = u_{i+1}
            uL = u[:-1]  # u_i for i=0,...,Nx-2
            uR = u[1:]   # u_{i+1} for i=0,...,Nx-2
        else:
            # MUSCL reconstruction with minmod limiter
            # Slopes
            du = np.zeros(Nx)
            du[1:-1] = minmod(u[2:] - u[1:-1], u[1:-1] - u[:-2])
            
            # Reconstructed values at interfaces
            uL = u[:-1] + 0.5 * du[:-1]   # right-side of cell i
            uR = u[1:] - 0.5 * du[1:]     # left-side of cell i+1
        
        # Compute Godunov flux at each interface (Nx-1 interfaces)
        F = godunov_flux_burgers(uL, uR)
        
        # Update (transmissive BCs)
        lam = dt / dx
        u[1:-1] = u[1:-1] - lam * (F[1:] - F[:-1])
        # Transmissive (outflow) boundary conditions
        u[0] = u[1]
        u[-1] = u[-2]
        
        t += dt
        t_history.append(t)
        u_history.append(u.copy())
    
    return u, t_history, u_history


def generate_training_data(Nx=512, num_ic=50, T_final=0.5, num_snapshots=20, seed=42):
    """
    Generate training dataset: pairs of (u^n, u^{n+1}) from Godunov solver.
    
    Multiple initial conditions:
      - Step functions (Riemann problems)
      - Smooth bumps that steepen into shocks
      - Sinusoidal ICs
    
    Returns dict with:
      x: spatial grid
      dx, dt: grid spacings
      samples: list of dicts with 'u_n', 'u_np1', 'ic_type', 't'
    """
    rng = np.random.RandomState(seed)
    x = np.linspace(0, 1, Nx)
    dx = x[1] - x[0]
    
    samples = []
    
    for ic_idx in range(num_ic):
        ic_type_id = ic_idx % 4
        
        if ic_type_id == 0:
            # Step function (Riemann problem)
            x0 = 0.3 + 0.4 * rng.rand()
            uL = 0.5 + 1.5 * rng.rand()
            uR = -0.5 + rng.rand()
            u0 = np.where(x < x0, uL, uR)
            ic_type = 'step'
        elif ic_type_id == 1:
            # Smooth Gaussian bump -> shock
            x0 = 0.2 + 0.3 * rng.rand()
            A = 1.0 + rng.rand()
            sigma = 0.05 + 0.1 * rng.rand()
            u0 = A * np.exp(-((x - x0) / sigma) ** 2)
            ic_type = 'bump'
        elif ic_type_id == 2:
            # Sinusoidal
            k = rng.choice([1, 2, 3])
            A = 0.5 + rng.rand()
            u0 = A * np.sin(2 * np.pi * k * x)
            ic_type = 'sine'
        else:
            # Two-step (more complex)
            x1 = 0.25 + 0.1 * rng.rand()
            x2 = 0.6 + 0.1 * rng.rand()
            u0 = np.where(x < x1, 1.0 + rng.rand(), 
                          np.where(x < x2, -0.5 + rng.rand(), 0.5 * rng.rand()))
            ic_type = 'two_step'
        
        # Run solver
        u_final, t_hist, u_hist = solve_burgers_godunov(u0, x, T_final, cfl=0.4, order=2)
        
        # Sample snapshots
        total_steps = len(u_hist)
        if total_steps < 3:
            continue
        
        # Take pairs at regular intervals
        step_indices = np.linspace(0, total_steps - 2, min(num_snapshots, total_steps - 1), dtype=int)
        for si in step_indices:
            samples.append({
                'u_n': u_hist[si],
                'u_np1': u_hist[si + 1],
                't_n': t_hist[si],
                't_np1': t_hist[si + 1],
                'ic_type': ic_type,
                'ic_idx': int(ic_idx),
            })
    
    # Compute a representative dt from CFL
    dt_repr = 0.4 * dx / 2.0  # typical dt for max |u| ~ 2
    
    return {
        'x': x,
        'dx': dx,
        'dt': dt_repr,
        'Nx': Nx,
        'samples': samples,
    }


def generate_test_cases(Nx=512):
    """Generate held-out test cases for evaluation."""
    x = np.linspace(0, 1, Nx)
    dx = x[1] - x[0]
    test_cases = []
    
    # Test 1: Classic Sod-like step (strong shock)
    u0_step = np.where(x < 0.5, 1.5, -0.5)
    u_ref, t_hist, u_hist = solve_burgers_godunov(u0_step, x, 0.3, cfl=0.4, order=2)
    test_cases.append({
        'name': 'strong_step',
        'u0': u0_step,
        'u_ref': u_ref,
        'T': 0.3,
        'description': 'Strong shock from step IC u=1.5/u=-0.5 at x=0.5'
    })
    
    # Test 2: Smooth bump -> shock
    u0_bump = 2.0 * np.exp(-((x - 0.3) / 0.1) ** 2)
    u_ref2, t_hist2, u_hist2 = solve_burgers_godunov(u0_bump, x, 0.4, cfl=0.4, order=2)
    test_cases.append({
        'name': 'bump_to_shock',
        'u0': u0_bump,
        'u_ref': u_ref2,
        'T': 0.4,
        'description': 'Gaussian bump steepening into shock'
    })
    
    # Test 3: N-wave (sine)
    u0_sine = np.sin(2 * np.pi * x)
    u_ref3, t_hist3, u_hist3 = solve_burgers_godunov(u0_sine, x, 0.3, cfl=0.4, order=2)
    test_cases.append({
        'name': 'n_wave',
        'u0': u0_sine,
        'u_ref': u_ref3,
        'T': 0.3,
        'description': 'Sine wave forming N-wave shock'
    })
    
    return x, dx, test_cases


if __name__ == '__main__':
    print("Generating training data...")
    data = generate_training_data(Nx=256, num_ic=60, T_final=0.5, num_snapshots=25)
    print(f"  Grid: Nx={data['Nx']}, dx={data['dx']:.6f}")
    print(f"  Representative dt={data['dt']:.6f}")
    print(f"  Total training samples: {len(data['samples'])}")
    
    # Save
    outdir = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(os.path.dirname(outdir), 'data')
    os.makedirs(datadir, exist_ok=True)
    
    np.savez(os.path.join(datadir, 'training_data.npz'),
             x=data['x'],
             dx=data['dx'],
             dt=data['dt'],
             u_n=np.array([s['u_n'] for s in data['samples']]),
             u_np1=np.array([s['u_np1'] for s in data['samples']]),
             t_n=np.array([s['t_n'] for s in data['samples']]),
             t_np1=np.array([s['t_np1'] for s in data['samples']]),
             ic_types=np.array([s['ic_type'] for s in data['samples']]),
             ic_idxs=np.array([s['ic_idx'] for s in data['samples']]))
    
    print("\nGenerating test cases...")
    x_test, dx_test, test_cases = generate_test_cases(Nx=256)
    for tc in test_cases:
        print(f"  {tc['name']}: {tc['description']}")
    
    np.savez(os.path.join(datadir, 'test_cases.npz'),
             x=x_test,
             dx=dx_test,
             names=[tc['name'] for tc in test_cases],
             u0s=np.array([tc['u0'] for tc in test_cases]),
             u_refs=np.array([tc['u_ref'] for tc in test_cases]),
             Ts=np.array([tc['T'] for tc in test_cases]),
             descriptions=[tc['description'] for tc in test_cases])
    
    print(f"\nData saved to {datadir}/")
