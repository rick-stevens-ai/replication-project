"""
Full p-convergence study for PWDG replication.

Reproduces key results from Hiptmair, Moiola, Perugia (2011):
1. Exponential p-convergence for smooth solutions on convex domains
2. Effect of wavenumber k on convergence
3. Comparison across mesh resolutions
4. Circular wave (Hankel function) benchmark
"""
import numpy as np
import json
import time
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, make_l_shaped_mesh
from pwdg_dirichlet import TrefftzDGLS


def make_pw(k, theta):
    """Plane wave exact solution."""
    d = np.array([np.cos(theta), np.sin(theta)])
    def u(pts, deriv=None):
        phase = k * (pts @ d)
        if deriv is None:
            return np.exp(1j * phase)
        return 1j * k * np.dot(d, deriv) * np.exp(1j * phase)
    return u


def make_hankel(k, center=None):
    """Circular wave (Hankel function) exact solution."""
    from scipy.special import hankel1
    if center is None:
        center = np.array([-0.5, -0.5])
    
    def u(pts, deriv=None):
        rv = pts - center[None, :]
        r = np.sqrt(rv[:,0]**2 + rv[:,1]**2)
        r = np.maximum(r, 1e-15)
        if deriv is None:
            return hankel1(0, k * r)
        dr_dn = (rv @ deriv) / r
        return -k * hankel1(1, k * r) * dr_dn
    return u


def run_study():
    results = {}
    base = os.path.dirname(os.path.dirname(__file__))
    results_dir = os.path.join(base, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # ========================================================
    # Study 1: p-convergence for plane wave, multiple k values
    # ========================================================
    print("=" * 70)
    print("Study 1: p-convergence for plane wave solution")
    print("=" * 70)
    
    k_values = [1.0, 2.0, 4.0, 8.0]
    p_values = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]
    n_mesh = 4
    theta = np.pi / 7  # non-aligned direction
    
    for k in k_values:
        mesh = make_unit_square_mesh(n_mesh)
        u_ex = make_pw(k, theta)
        print(f"\n  k = {k}, mesh: {mesh.n_elements} elements")
        
        data = {'k': k, 'n_mesh': n_mesh, 'theta': theta,
                'n_elements': mesh.n_elements,
                'p': [], 'L2': [], 'DG': [], 'cond': [], 'time': []}
        
        for p in p_values:
            t0 = time.time()
            solver = TrefftzDGLS(mesh, k, p)
            c, A, _ = solver.solve(u_ex)
            elapsed = time.time() - t0
            
            err_L2 = solver.L2_error(c, u_ex)
            err_DG = solver.DG_error(c, u_ex)
            cond = np.linalg.cond(A)
            
            data['p'].append(p)
            data['L2'].append(float(err_L2))
            data['DG'].append(float(err_DG))
            data['cond'].append(float(cond))
            data['time'].append(float(elapsed))
            
            print(f"    p={p:3d}: L2={err_L2:.4e}  DG={err_DG:.4e}  cond={cond:.2e}  ({elapsed:.2f}s)")
        
        results[f'pw_k{k}'] = data
    
    # ========================================================
    # Study 2: Effect of mesh resolution
    # ========================================================
    print("\n" + "=" * 70)
    print("Study 2: Effect of mesh resolution (fixed k=4)")
    print("=" * 70)
    
    k = 4.0
    u_ex = make_pw(k, theta)
    
    for n_mesh in [2, 3, 4, 6, 8]:
        mesh = make_unit_square_mesh(n_mesh)
        h = 1.0 / n_mesh
        print(f"\n  n={n_mesh} (h={h:.4f}, {mesh.n_elements} elements):")
        
        data = {'k': k, 'n_mesh': n_mesh, 'h': h, 
                'n_elements': mesh.n_elements,
                'p': [], 'L2': [], 'DG': [], 'cond': []}
        
        p_max = min(16, 14)  # avoid excessive conditioning issues
        for p in range(3, p_max + 1):
            solver = TrefftzDGLS(mesh, k, p)
            c, A, _ = solver.solve(u_ex)
            err = solver.L2_error(c, u_ex)
            dg = solver.DG_error(c, u_ex)
            cond = np.linalg.cond(A)
            
            data['p'].append(p)
            data['L2'].append(float(err))
            data['DG'].append(float(dg))
            data['cond'].append(float(cond))
            
            print(f"    p={p:3d}: L2={err:.4e}  DG={dg:.4e}")
        
        results[f'mesh_n{n_mesh}'] = data
    
    # ========================================================
    # Study 3: h-convergence (fixed p)
    # ========================================================
    print("\n" + "=" * 70)
    print("Study 3: h-convergence (fixed p)")
    print("=" * 70)
    
    k = 4.0
    u_ex = make_pw(k, theta)
    
    for p in [6, 8, 10]:
        print(f"\n  p = {p}:")
        data = {'k': k, 'p': p, 'n': [], 'h': [], 'L2': [], 'DG': []}
        
        for n in [2, 3, 4, 5, 6, 8, 10]:
            mesh = make_unit_square_mesh(n)
            h = 1.0 / n
            solver = TrefftzDGLS(mesh, k, p)
            c, _, _ = solver.solve(u_ex)
            err = solver.L2_error(c, u_ex)
            dg = solver.DG_error(c, u_ex)
            
            data['n'].append(n)
            data['h'].append(h)
            data['L2'].append(float(err))
            data['DG'].append(float(dg))
            
            print(f"    n={n:3d} (h={h:.4f}): L2={err:.4e}  DG={dg:.4e}")
        
        results[f'hconv_p{p}'] = data
    
    # ========================================================
    # Study 4: Circular wave (non-plane-wave solution)
    # ========================================================
    print("\n" + "=" * 70)
    print("Study 4: Circular wave (Hankel function)")
    print("=" * 70)
    
    try:
        from scipy.special import hankel1
        
        for k in [2.0, 4.0]:
            u_ex = make_hankel(k)
            mesh = make_unit_square_mesh(4)
            print(f"\n  k = {k}, Hankel source at (-0.5, -0.5):")
            
            data = {'k': k, 'n_mesh': 4, 'type': 'hankel',
                    'p': [], 'L2': [], 'DG': []}
            
            for p in range(3, 17):
                solver = TrefftzDGLS(mesh, k, p)
                c, _, _ = solver.solve(u_ex)
                err = solver.L2_error(c, u_ex)
                dg = solver.DG_error(c, u_ex)
                
                data['p'].append(p)
                data['L2'].append(float(err))
                data['DG'].append(float(dg))
                
                print(f"    p={p:3d}: L2={err:.4e}  DG={dg:.4e}")
            
            results[f'hankel_k{k}'] = data
    
    except ImportError:
        print("  scipy not available, skipping Hankel tests")
    
    # Save all results
    out_file = os.path.join(results_dir, 'full_study.json')
    with open(out_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_file}")
    
    return results


if __name__ == '__main__':
    run_study()
