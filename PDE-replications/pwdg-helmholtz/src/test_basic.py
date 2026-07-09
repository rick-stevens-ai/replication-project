"""
Basic tests for the PWDG implementation.

Test 1: If exact solution IS one of the basis functions, 
        error should be zero (or machine precision).
Test 2: Verify assembly correctness with a simple 2-element mesh.
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, TriMesh, _build_mesh
from pwdg_v2 import PWDGSolverV2


def test_exact_reproduction():
    """If exact solution is a plane wave aligned with one basis direction,
    the PWDG solution should reproduce it exactly."""
    print("=== Test: Exact Reproduction of Basis Function ===")
    
    k = 4.0
    p = 8
    mesh = make_unit_square_mesh(2)
    
    solver = PWDGSolverV2(mesh, k, p)
    
    # Exact solution = one of the plane wave basis functions
    # Direction index 0: d = (1, 0)
    d_exact = solver.directions[0]
    
    def u_exact(pts, deriv=None):
        phase = k * (pts @ d_exact)
        if deriv is None:
            return np.exp(1j * phase)
        else:
            return 1j * k * np.dot(d_exact, deriv) * np.exp(1j * phase)
    
    coeffs = solver.solve(u_exact)
    
    err_L2 = solver.compute_L2_error(coeffs, u_exact)
    err_DG = solver.compute_DG_error(coeffs, u_exact)
    
    print(f"  L2 error: {err_L2:.6e}")
    print(f"  DG error: {err_DG:.6e}")
    print(f"  Expected: ~machine epsilon")
    
    # Check that coefficients have expected structure:
    # Each element should have coeff 1.0 for direction 0, 0 for others
    print(f"  Coefficient sample (elem 0): {coeffs[:p]}")
    print(f"  Expected: 1.0 at index 0, ~0 elsewhere")
    
    passed = err_L2 < 1e-6
    print(f"  {'PASS' if passed else 'FAIL'}")
    return passed


def test_plane_wave_not_aligned():
    """Test with plane wave NOT aligned with any basis direction."""
    print("\n=== Test: Plane Wave NOT Aligned with Basis ===")
    
    k = 2.0
    mesh = make_unit_square_mesh(3)
    
    # Direction at angle pi/7 (not aligned with equispaced directions)
    theta_exact = np.pi / 7
    d_exact = np.array([np.cos(theta_exact), np.sin(theta_exact)])
    
    def u_exact(pts, deriv=None):
        phase = k * (pts @ d_exact)
        if deriv is None:
            return np.exp(1j * phase)
        else:
            return 1j * k * np.dot(d_exact, deriv) * np.exp(1j * phase)
    
    for p in [4, 6, 8, 12, 16, 20, 24]:
        solver = PWDGSolverV2(mesh, k, p)
        coeffs = solver.solve(u_exact)
        err = solver.compute_L2_error(coeffs, u_exact)
        print(f"  p = {p:3d}: L2 error = {err:.6e}")
    
    print("  Expected: decreasing (ideally exponential) convergence")


def test_system_consistency():
    """Check that the system matrix has expected properties."""
    print("\n=== Test: System Matrix Properties ===")
    
    k = 2.0
    p = 4
    mesh = make_unit_square_mesh(2)
    
    d_exact = np.array([1.0, 0.0])
    def u_exact(pts, deriv=None):
        phase = k * (pts @ d_exact)
        if deriv is None:
            return np.exp(1j * phase)
        else:
            return 1j * k * np.dot(d_exact, deriv) * np.exp(1j * phase)
    
    solver = PWDGSolverV2(mesh, k, p)
    A, b = solver.assemble(u_exact)
    
    print(f"  System size: {A.shape}")
    print(f"  Condition number: {np.linalg.cond(A):.2e}")
    print(f"  Max |A|: {np.max(np.abs(A)):.6e}")
    print(f"  Max |b|: {np.max(np.abs(b)):.6e}")
    
    # Check if A is "close to" Hermitian (it shouldn't be exactly, but check)
    asym = np.linalg.norm(A - A.conj().T) / np.linalg.norm(A)
    print(f"  Asymmetry ||A - A^H||/||A||: {asym:.6e}")
    
    # Solve and check residual
    c = np.linalg.solve(A, b)
    resid = np.linalg.norm(A @ c - b) / np.linalg.norm(b)
    print(f"  Relative residual: {resid:.6e}")


def test_two_element():
    """Test with minimal 2-element mesh to verify assembly."""
    print("\n=== Test: Two-Element Mesh ===")
    
    # Two triangles forming a unit square
    nodes = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    elements = np.array([[0, 1, 3], [1, 2, 3]])
    mesh = _build_mesh(nodes, elements)
    
    print(f"  Elements: {mesh.n_elements}")
    print(f"  Interior edges: {len(mesh.interior_edges)}")
    print(f"  Boundary edges: {len(mesh.boundary_edges)}")
    
    k = 2.0
    p = 4
    
    d_exact = np.array([np.cos(0.3), np.sin(0.3)])
    def u_exact(pts, deriv=None):
        phase = k * (pts @ d_exact)
        if deriv is None:
            return np.exp(1j * phase)
        else:
            return 1j * k * np.dot(d_exact, deriv) * np.exp(1j * phase)
    
    solver = PWDGSolverV2(mesh, k, p)
    A, b = solver.assemble(u_exact)
    
    print(f"  System size: {A.shape}")
    print(f"  Condition: {np.linalg.cond(A):.2e}")
    
    coeffs = solver.solve(u_exact)
    err = solver.compute_L2_error(coeffs, u_exact)
    print(f"  L2 error: {err:.6e}")


if __name__ == '__main__':
    test_exact_reproduction()
    test_plane_wave_not_aligned()
    test_system_consistency()
    test_two_element()
