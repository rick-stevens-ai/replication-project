#!/usr/bin/env python3
"""
Compute reference solutions for the test PDEs using traditional numerical methods.
These serve as ground truth for computing relative errors E_rel.
"""

import numpy as np
import torch


def burgers_reference(nx=1001, nt=10001, nu=0.01/np.pi):
    """
    Solve Burgers' equation using spectral method (Cole-Hopf transform).
    u_t + u*u_x = nu*u_xx, x in [-1,1], t in [0,1]
    u(0,x) = -sin(pi*x)
    u(t,-1) = u(t,1) = 0
    
    Returns callable that takes (t,x) arrays and returns u(t,x).
    """
    # Cole-Hopf transformation: u = -2*nu * phi_x / phi
    # phi_t = nu * phi_xx
    # IC: phi(0,x) = exp(-1/(2*nu*pi) * (1 - cos(pi*x)))
    
    # For robustness, use Fourier spectral method on the heat equation for phi
    x = np.linspace(-1, 1, nx)
    dx = x[1] - x[0]
    t = np.linspace(0, 1, nt)
    dt = t[1] - t[0]
    
    # Initial condition for phi
    phi0 = np.exp(-1.0 / (2.0 * nu * np.pi) * (1.0 - np.cos(np.pi * x)))
    
    # Solve heat equation for phi using implicit Euler with FFT
    # Since domain is [-1,1], period = 2
    N = nx - 1  # Number of intervals
    k = np.fft.fftfreq(nx, d=dx) * 2 * np.pi  # wavenumbers
    
    phi = phi0.copy()
    u_ref = np.zeros((nt, nx))
    u_ref[0] = -np.sin(np.pi * x)  # IC
    
    for n in range(1, nt):
        # Advance phi: phi_t = nu * phi_xx
        phi_hat = np.fft.fft(phi)
        # Exact integration in Fourier space
        phi_hat *= np.exp(-nu * k**2 * dt)
        phi = np.real(np.fft.ifft(phi_hat))
        
        # Compute u = -2*nu * phi_x / phi
        phi_hat = np.fft.fft(phi)
        dphi_hat = 1j * k * phi_hat
        dphi = np.real(np.fft.ifft(dphi_hat))
        
        # Avoid division by zero
        u_ref[n] = -2.0 * nu * dphi / (phi + 1e-30)
    
    # Create interpolation function
    from scipy.interpolate import RegularGridInterpolator
    interp = RegularGridInterpolator((t, x), u_ref, method='cubic',
                                      bounds_error=False, fill_value=0.0)
    
    return interp, t, x, u_ref


def allen_cahn_reference(nx=201, nt=2001, D=0.001):
    """
    Solve Allen-Cahn using semi-implicit Fourier spectral method.
    u_t = D*u_xx + 5*(u - u^3), x in [-1,1], t in [0,1]
    u(0,x) = x^2*cos(pi*x)
    u(t,-1) = u(t,1) = -1
    
    Returns interpolation function.
    """
    x = np.linspace(-1, 1, nx)
    dx = x[1] - x[0]
    t = np.linspace(0, 1, nt)
    dt = t[1] - t[0]
    
    # IC
    u = x**2 * np.cos(np.pi * x)
    u_ref = np.zeros((nt, nx))
    u_ref[0] = u.copy()
    
    k = np.fft.fftfreq(nx, d=dx) * 2 * np.pi
    
    for n in range(1, nt):
        # Semi-implicit: linear part implicit, nonlinear explicit
        # u_t = D*u_xx + 5*u - 5*u^3
        # Implicit: (I - dt*D*d_xx - dt*5) u^{n+1} = u^n - dt*5*(u^n)^3
        
        nonlinear = -5.0 * u**3
        
        u_hat = np.fft.fft(u + dt * nonlinear)
        
        # Implicit part in Fourier space
        denom = 1.0 + dt * D * k**2 - dt * 5.0
        u_hat /= denom
        
        u = np.real(np.fft.ifft(u_hat))
        
        # Enforce BCs
        u[0] = -1.0
        u[-1] = -1.0
        
        u_ref[n] = u.copy()
    
    from scipy.interpolate import RegularGridInterpolator
    interp = RegularGridInterpolator((t, x), u_ref, method='cubic',
                                      bounds_error=False, fill_value=None)
    
    return interp, t, x, u_ref


def advection_diffusion_reference(nx=201, ny=201, mu=1e-2):
    """
    Solve advection-diffusion steady-state using finite differences.
    -mu*(u_xx + u_yy) + u_x + u_y = 1, (x,y) in (0,1)^2
    u = 0 on boundary
    
    Uses central differences with upwinding for advection.
    Returns interpolation function.
    """
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    hx = x[1] - x[0]
    hy = y[1] - y[0]
    
    # Interior points
    nix = nx - 2
    niy = ny - 2
    N = nix * niy
    
    # Build sparse system
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve
    
    A = lil_matrix((N, N))
    b = np.ones(N)
    
    def idx(i, j):
        return i * niy + j
    
    for i in range(nix):
        for j in range(niy):
            k = idx(i, j)
            
            # -mu * u_xx ≈ -mu * (u_{i-1,j} - 2u_{i,j} + u_{i+1,j}) / hx^2
            # -mu * u_yy ≈ -mu * (u_{i,j-1} - 2u_{i,j} + u_{i,j+1}) / hy^2
            # u_x ≈ (u_{i+1,j} - u_{i-1,j}) / (2*hx) [central]
            # u_y ≈ (u_{i,j+1} - u_{i,j-1}) / (2*hy)
            
            # Center coefficient
            A[k, k] = 2.0 * mu / hx**2 + 2.0 * mu / hy**2
            
            # x-direction
            if i > 0:
                A[k, idx(i-1, j)] = -mu / hx**2 - 1.0 / (2.0 * hx)
            if i < nix - 1:
                A[k, idx(i+1, j)] = -mu / hx**2 + 1.0 / (2.0 * hx)
            
            # y-direction
            if j > 0:
                A[k, idx(i, j-1)] = -mu / hy**2 - 1.0 / (2.0 * hy)
            if j < niy - 1:
                A[k, idx(i, j+1)] = -mu / hy**2 + 1.0 / (2.0 * hy)
    
    A = A.tocsr()
    u_flat = spsolve(A, b)
    
    u_ref = np.zeros((nx, ny))
    for i in range(nix):
        for j in range(niy):
            u_ref[i+1, j+1] = u_flat[idx(i, j)]
    
    from scipy.interpolate import RegularGridInterpolator
    interp = RegularGridInterpolator((x, y), u_ref, method='cubic',
                                      bounds_error=False, fill_value=0.0)
    
    return interp, x, y, u_ref


def compute_relative_error_with_ref(model, problem, bc_transform, ref_interp,
                                     n_test=10000, device='cpu'):
    """
    Compute E_rel = ||u_pred - u_ref||_2 / ||u_ref||_2
    using the reference solution interpolator.
    """
    with torch.no_grad():
        X_test = problem.generate_collocation_points(n_int=n_test, device=device)
        u_raw = model(X_test)
        u_pred = bc_transform(u_raw, X_test)
        
        # Get reference values
        X_np = X_test.cpu().numpy()
        u_ref_vals = ref_interp(X_np)
        u_ref_tensor = torch.tensor(u_ref_vals, dtype=torch.float32, device=device).reshape(-1, 1)
        
        err = torch.norm(u_pred - u_ref_tensor) / (torch.norm(u_ref_tensor) + 1e-30)
    return err.item()


if __name__ == '__main__':
    print("Computing reference solutions...")
    
    print("\n1. Burgers' equation...")
    interp_b, t_b, x_b, u_b = burgers_reference()
    print(f"   Solution range: [{u_b.min():.4f}, {u_b.max():.4f}]")
    print(f"   IC check u(0,0) = {u_b[0, len(x_b)//2]:.4f} (should be ~0)")
    
    print("\n2. Allen-Cahn equation...")
    interp_ac, t_ac, x_ac, u_ac = allen_cahn_reference()
    print(f"   Solution range: [{u_ac.min():.4f}, {u_ac.max():.4f}]")
    
    print("\n3. Advection-diffusion...")
    interp_ad, x_ad, y_ad, u_ad = advection_diffusion_reference()
    print(f"   Solution range: [{u_ad.min():.4f}, {u_ad.max():.4f}]")
    
    print("\nDone computing references.")
    
    # Save references
    np.savez('/data/stevens/projects-active/pinn-dd-precond/results/references.npz',
             burgers_u=u_b, burgers_t=t_b, burgers_x=x_b,
             allen_cahn_u=u_ac, allen_cahn_t=t_ac, allen_cahn_x=x_ac,
             advdiff_u=u_ad, advdiff_x=x_ad, advdiff_y=y_ad)
    print("Saved to references.npz")
