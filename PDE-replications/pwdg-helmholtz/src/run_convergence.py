"""
p-convergence study for PWDG method on 2D Helmholtz equation.

Reproduces the key results from Hiptmair, Moiola, Perugia (2011):
- Exponential convergence in p (number of plane wave directions)
- Tests on unit square with plane wave exact solution
- Tests with different wavenumbers k
"""
import numpy as np
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, make_l_shaped_mesh
from pwdg_solver import PWDGSolver


def plane_wave_solution(k, direction):
    """Create an exact plane wave solution u(x) = exp(i*k*d.x).
    
    This is a Helmholtz solution for any direction d on unit circle.
    """
    d = np.array(direction) / np.linalg.norm(direction)
    
    def u_exact(pts, deriv=None):
        phase = k * (pts @ d)
        vals = np.exp(1j * phase)
        if deriv is not None:
            # Directional derivative in direction 'deriv'
            return 1j * k * np.dot(d, deriv) * vals
        return vals
    
    return u_exact


def circular_wave_solution(k, center=None):
    """Create exact Hankel function solution (circular wave).
    
    u(x) = H_0^(1)(k|x - x0|) - outgoing circular wave.
    Source at center (default outside domain).
    """
    from scipy.special import hankel1
    
    if center is None:
        center = np.array([-0.5, -0.5])  # source outside unit square
    
    def u_exact(pts, deriv=None):
        r_vec = pts - center[np.newaxis, :]
        r = np.sqrt(r_vec[:, 0]**2 + r_vec[:, 1]**2)
        r = np.maximum(r, 1e-15)
        
        if deriv is None:
            return hankel1(0, k * r)
        else:
            # Normal derivative
            dr_dn = (r_vec @ deriv) / r
            return -k * hankel1(1, k * r) * dr_dn
    
    return u_exact


def run_p_convergence_plane_wave(k_values, p_values, n_mesh, results_dir):
    """Run p-convergence study with plane wave exact solution.
    
    Fix mesh (h fixed), vary p.
    """
    results = {}
    
    for k in k_values:
        print(f"\n=== Wavenumber k = {k} ===")
        mesh = make_unit_square_mesh(n_mesh)
        print(f"Mesh: {mesh.n_elements} elements, {len(mesh.interior_edges)} interior edges, "
              f"{len(mesh.boundary_edges)} boundary edges")
        
        # Exact solution: plane wave NOT aligned with any basis direction
        # Use direction at angle pi/7 (not a multiple of 2*pi/p for any reasonable p)
        d_exact = np.array([np.cos(np.pi/7), np.sin(np.pi/7)])
        u_exact = plane_wave_solution(k, d_exact)
        
        errors_L2 = []
        errors_DG = []
        times = []
        
        for p in p_values:
            print(f"  p = {p:3d} (DOF = {mesh.n_elements * p:6d})", end="", flush=True)
            
            t0 = time.time()
            try:
                solver = PWDGSolver(mesh, k, p, quad_order_edge=max(12, p+4))
                coeffs = solver.solve(u_exact=u_exact)
                
                err_L2 = solver.compute_error(coeffs, u_exact, norm_type='L2')
                err_DG = solver.compute_error(coeffs, u_exact, norm_type='DG')
                
                elapsed = time.time() - t0
                errors_L2.append(float(err_L2))
                errors_DG.append(float(err_DG))
                times.append(elapsed)
                
                print(f"  L2 err = {err_L2:.6e}  DG err = {err_DG:.6e}  ({elapsed:.1f}s)")
            except Exception as e:
                elapsed = time.time() - t0
                print(f"  FAILED: {e} ({elapsed:.1f}s)")
                errors_L2.append(float('nan'))
                errors_DG.append(float('nan'))
                times.append(elapsed)
        
        results[f'k={k}'] = {
            'k': k,
            'n_mesh': n_mesh,
            'p_values': [int(x) for x in p_values],
            'errors_L2': errors_L2,
            'errors_DG': errors_DG,
            'times': times,
            'n_elements': mesh.n_elements,
            'exact_solution': f'plane wave, direction=({d_exact[0]:.6f}, {d_exact[1]:.6f})'
        }
    
    # Save results
    out_file = os.path.join(results_dir, 'p_convergence_plane_wave.json')
    with open(out_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_file}")
    
    return results


def run_p_convergence_circular_wave(k, p_values, n_mesh, results_dir):
    """Run p-convergence study with circular wave (Hankel function) exact solution."""
    from scipy.special import hankel1
    
    print(f"\n=== Circular wave, k = {k} ===")
    mesh = make_unit_square_mesh(n_mesh)
    print(f"Mesh: {mesh.n_elements} elements")
    
    u_exact = circular_wave_solution(k, center=np.array([-0.5, -0.5]))
    
    errors_L2 = []
    errors_DG = []
    
    for p in p_values:
        print(f"  p = {p:3d}", end="", flush=True)
        try:
            solver = PWDGSolver(mesh, k, p, quad_order_edge=max(12, p+4))
            coeffs = solver.solve(u_exact=u_exact)
            
            err_L2 = solver.compute_error(coeffs, u_exact, norm_type='L2')
            err_DG = solver.compute_error(coeffs, u_exact, norm_type='DG')
            
            errors_L2.append(float(err_L2))
            errors_DG.append(float(err_DG))
            print(f"  L2 err = {err_L2:.6e}  DG err = {err_DG:.6e}")
        except Exception as e:
            print(f"  FAILED: {e}")
            errors_L2.append(float('nan'))
            errors_DG.append(float('nan'))
    
    result = {
        'k': k,
        'n_mesh': n_mesh,
        'p_values': [int(x) for x in p_values],
        'errors_L2': errors_L2,
        'errors_DG': errors_DG,
        'n_elements': mesh.n_elements,
        'exact_solution': 'Hankel H_0^(1)(k|x-x0|), x0=(-0.5,-0.5)'
    }
    
    out_file = os.path.join(results_dir, 'p_convergence_circular_wave.json')
    with open(out_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    return result


def run_h_convergence(k, p, n_values, results_dir):
    """Run h-convergence study (fixed p, refine mesh)."""
    print(f"\n=== h-convergence, k = {k}, p = {p} ===")
    
    d_exact = np.array([np.cos(np.pi/7), np.sin(np.pi/7)])
    u_exact = plane_wave_solution(k, d_exact)
    
    errors_L2 = []
    errors_DG = []
    h_values = []
    
    for n in n_values:
        mesh = make_unit_square_mesh(n)
        h = 1.0 / n
        h_values.append(h)
        
        print(f"  n = {n:3d} (h = {h:.4f}, DOF = {mesh.n_elements * p:6d})", end="", flush=True)
        try:
            solver = PWDGSolver(mesh, k, p, quad_order_edge=max(12, p+4))
            coeffs = solver.solve(u_exact=u_exact)
            
            err_L2 = solver.compute_error(coeffs, u_exact, norm_type='L2')
            err_DG = solver.compute_error(coeffs, u_exact, norm_type='DG')
            
            errors_L2.append(float(err_L2))
            errors_DG.append(float(err_DG))
            print(f"  L2 err = {err_L2:.6e}  DG err = {err_DG:.6e}")
        except Exception as e:
            print(f"  FAILED: {e}")
            errors_L2.append(float('nan'))
            errors_DG.append(float('nan'))
    
    result = {
        'k': k,
        'p': p,
        'n_values': [int(x) for x in n_values],
        'h_values': h_values,
        'errors_L2': errors_L2,
        'errors_DG': errors_DG,
    }
    
    out_file = os.path.join(results_dir, 'h_convergence.json')
    with open(out_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    return result


if __name__ == '__main__':
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 70)
    print("PWDG p-Convergence Study for 2D Helmholtz Equation")
    print("Replicating Hiptmair, Moiola, Perugia (SIAM J. Numer. Anal., 2011)")
    print("=" * 70)
    
    # Test 1: p-convergence with plane wave solution
    # Paper tests with various k values
    k_values = [1.0, 4.0, 8.0]
    p_values = np.array([3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20])
    n_mesh = 4  # Fixed coarse mesh (4x4 = 32 triangles)
    
    results_pw = run_p_convergence_plane_wave(k_values, p_values, n_mesh, results_dir)
    
    # Test 2: p-convergence with circular wave (non-plane-wave solution)
    results_cw = run_p_convergence_circular_wave(4.0, p_values, n_mesh, results_dir)
    
    # Test 3: h-convergence for fixed p
    results_h = run_h_convergence(4.0, 8, [2, 3, 4, 6, 8, 10, 12], results_dir)
    
    print("\n" + "=" * 70)
    print("All tests complete!")
    print("=" * 70)
