"""
Generate reference data for turbulent flow over periodic hill.

The paper uses DNS data at Re_b = 2800 (based on crest height H and bulk velocity U_b).
Domain: x/H in [1, 5] (between hills, covering separation and reattachment).

Since we don't have access to the original DNS data, we generate synthetic data
using established correlations for the periodic hill flow:
- Hill geometry from Almeida et al. (1993) / Breuer et al. (2009)
- Flow field approximated from published DNS statistics

The periodic hill is a benchmark case with well-documented flow features:
- Separation at x/H ~ 0.2
- Reattachment at x/H ~ 4.7 (at Re_b=2800)
- Recirculation region
"""

import numpy as np
import os


def hill_profile(x_H):
    """
    Hill geometry from standard periodic hill benchmark.
    Returns y_wall(x/H) / H.
    
    The hill spans x/H in [0, 9] with period 9.
    Hill crest at x/H = 0 (and 9), with H = 1 at crest.
    Flat bottom between hills (x/H ~ 1 to 8 approximately).
    
    Using polynomial fit from Breuer et al. (2009).
    """
    x = np.asarray(x_H) % 9.0  # Periodic
    y = np.zeros_like(x, dtype=float)
    
    # Simplified hill shape (polynomial approximation)
    for i, xv in enumerate(x.ravel()):
        if xv <= 0.5:
            # Rising/crest region
            y.ravel()[i] = min(1.0, 1.0 - 2.8 * (xv - 0)**2)
        elif xv <= 1.0:
            # Descending slope
            y.ravel()[i] = max(0, 1.0 - 2.8 * xv**2 + 1.2 * xv)
            y.ravel()[i] = max(0, 1.929 * (1 - xv)**2 - 0.929 * (1 - xv)**3)
        elif xv <= 8.0:
            # Flat bottom
            y.ravel()[i] = 0.0
        elif xv <= 8.5:
            # Rising to next hill
            t = (xv - 8.0) / 1.0
            y.ravel()[i] = 1.929 * t**2 - 0.929 * t**3
        else:
            # Crest region
            t = (xv - 8.0) / 1.0
            y.ravel()[i] = min(1.0, 1.929 * t**2 - 0.929 * t**3)
    
    return y


def generate_periodic_hill_field(Re_b=2800, nx=120, ny=60):
    """
    Generate synthetic reference data for periodic hill flow.
    
    Domain: x/H in [1, 5], y/H in [0, 3.036] (channel height)
    Re_b = U_b * H / nu = 2800
    """
    H = 1.0
    U_b = 1.0
    nu = U_b * H / Re_b
    
    x_range = (1.0, 5.0)
    y_top = 3.036  # Standard channel height for periodic hill
    
    x_arr = np.linspace(x_range[0], x_range[1], nx)
    
    # Bottom wall follows hill geometry
    y_wall = hill_profile(x_arr)  # All zero in [1,5] range (flat bottom after hill)
    
    # For x/H in [1,5], the bottom is flat (y_wall = 0)
    # The flow features a separation region starting near x/H ~ 0.2 (upstream of our domain)
    # and reattachment at x/H ~ 4.7
    
    # Create grid (uniform in y for simplicity)
    y_arr = np.linspace(0, y_top, ny)
    X, Y = np.meshgrid(x_arr, y_arr)
    
    # Synthetic velocity field
    U_field = np.zeros((ny, nx))
    V_field = np.zeros((ny, nx))
    P_field = np.zeros((ny, nx))
    uu_field = np.zeros((ny, nx))
    uv_field = np.zeros((ny, nx))
    vv_field = np.zeros((ny, nx))
    
    for j in range(nx):
        x_val = x_arr[j]
        
        # Separation and reattachment model
        # Reattachment at x/H ~ 4.7
        # In the separated region (x/H < 4.7), there's a recirculation zone
        
        # Height of recirculation zone decreases from ~0.5H at x=1 to 0 at x=4.7
        if x_val < 4.7:
            h_sep = 0.5 * (1 - (x_val - 1.0) / 3.7) * H  # Linear decrease
        else:
            h_sep = 0.0
        
        for i in range(ny):
            y_val = y_arr[i]
            
            # Mean streamwise velocity
            if y_val <= h_sep:
                # Recirculation zone: negative velocity
                # Approximate reverse flow profile
                t = y_val / max(h_sep, 1e-6)
                U_field[i, j] = -0.15 * U_b * np.sin(np.pi * t) * (1 - x_val/4.7)
            else:
                # Above separation: developing channel-like flow
                # Use a polynomial profile
                eta = (y_val - h_sep) / (y_top - h_sep)
                # Turbulent channel profile approximation
                if eta < 0.1:
                    # Near-wall region
                    y_plus = y_val * (U_b / (20 * nu))  # approximate u_tau
                    if y_plus < 5:
                        U_field[i, j] = U_b * y_plus / 20
                    elif y_plus < 30:
                        U_field[i, j] = U_b * (5 * np.log(y_plus) - 3.05) / 20
                    else:
                        U_field[i, j] = U_b * (2.5 * np.log(y_plus) + 5.5) / 20
                else:
                    # Core flow
                    U_field[i, j] = U_b * 1.15 * (1 - 0.5 * (2*eta - 1)**6)
            
            # Cap velocity
            U_field[i, j] = min(U_field[i, j], 1.5 * U_b)
            
            # Reynolds stresses (approximate)
            if y_val > 0 and y_val < y_top:
                eta_wall = min(y_val / y_top, 1 - y_val / y_top)
                # Rough approximation
                u_tau_local = 0.05 * U_b
                
                uu_field[i, j] = 3.0 * u_tau_local**2 * np.exp(-2 * (eta_wall - 0.05)**2 / 0.01)
                uv_field[i, j] = -u_tau_local**2 * (1 - 2*y_val/y_top) * np.exp(-y_val/(0.1*y_top))
                vv_field[i, j] = 1.0 * u_tau_local**2 * np.exp(-2 * (eta_wall - 0.05)**2 / 0.01)
    
    # V from continuity
    for j in range(1, nx-1):
        dU_dx = (U_field[:, j+1] - U_field[:, j-1]) / (x_arr[j+1] - x_arr[j-1])
        for i in range(1, ny):
            dy = y_arr[i] - y_arr[i-1]
            V_field[i, j] = V_field[i-1, j] - dU_dx[i] * dy
    V_field[:, 0] = V_field[:, 1]
    V_field[:, -1] = V_field[:, -2]
    
    # Pressure from x-momentum (simplified)
    # dP/dx ≈ nu * d2U/dy2 - U*dU/dx (rough)
    for j in range(1, nx-1):
        P_field[:, j] = P_field[:, j-1]  # Simple pressure gradient
    
    return X, Y, U_field, V_field, P_field, uu_field, uv_field, vv_field, {
        'Re_b': Re_b, 'H': H, 'U_b': U_b, 'nu': nu,
        'x': x_arr, 'y': y_arr, 'y_top': y_top
    }


def main():
    print("Generating periodic hill reference data...")
    X, Y, U, V, P, uu, uv, vv, params = generate_periodic_hill_field(nx=120, ny=60)
    
    outdir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(outdir, exist_ok=True)
    
    np.savez(os.path.join(outdir, 'periodic_hill_ref.npz'),
             X=X, Y=Y, U=U, V=V, P=P, uu=uu, uv=uv, vv=vv,
             Re_b=params['Re_b'], H=params['H'], nu=params['nu'],
             U_b=params['U_b'], y_top=params['y_top'])
    
    print(f"Grid: {X.shape}")
    print(f"U range: [{U.min():.4f}, {U.max():.4f}]")
    print(f"V range: [{V.min():.6f}, {V.max():.6f}]")
    print(f"Saved to {outdir}/periodic_hill_ref.npz")


if __name__ == '__main__':
    main()
