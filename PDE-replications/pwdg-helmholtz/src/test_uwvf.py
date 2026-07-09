"""Test UWVF solver."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, _build_mesh
from uwvf_solver import UWVFSolver


def make_pw(k, theta):
    d = np.array([np.cos(theta), np.sin(theta)])
    def u(pts, deriv=None):
        phase = k * (pts @ d)
        if deriv is None:
            return np.exp(1j * phase)
        return 1j * k * np.dot(d, deriv) * np.exp(1j * phase)
    return u


# Test 1: Exact reproduction
print("=" * 60)
print("Test 1: Exact reproduction (basis-aligned)")
print("=" * 60)
k = 2.0
for p in [4, 6, 8]:
    mesh = make_unit_square_mesh(2)
    solver = UWVFSolver(mesh, k, p)
    u_ex = make_pw(k, 0.0)  # direction (1,0) = dirs[0]
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    
    # Check Galerkin orthogonality
    c_exact = np.zeros(solver.ndof, dtype=complex)
    for K in range(mesh.n_elements):
        c_exact[K*p] = 1.0
    resid = np.linalg.norm(A @ c_exact - b)
    
    print(f"  p={p}: L2 err={err:.6e}, ||A c_exact - b||={resid:.6e}, cond={np.linalg.cond(A):.2e}")

# Test 2: p-convergence
print("\n" + "=" * 60)
print("Test 2: p-convergence (non-aligned plane wave)")
print("=" * 60)
k = 2.0
mesh = make_unit_square_mesh(3)
u_ex = make_pw(k, np.pi / 7)
for p in [3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 30]:
    solver = UWVFSolver(mesh, k, p)
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    dg = solver.DG_error(c, u_ex)
    cond = np.linalg.cond(A)
    print(f"  p={p:3d}: L2={err:.6e}  DG={dg:.6e}  cond={cond:.2e}")

# Test 3: Multiple k values
print("\n" + "=" * 60)
print("Test 3: Different wavenumbers")
print("=" * 60)
mesh = make_unit_square_mesh(4)
for k in [1, 2, 4, 8]:
    u_ex = make_pw(k, np.pi/7)
    print(f"\n  k={k}:")
    for p in [4, 8, 12, 16, 20]:
        solver = UWVFSolver(mesh, k, p)
        c, _, _ = solver.solve(u_ex)
        err = solver.L2_error(c, u_ex)
        print(f"    p={p:3d}: L2={err:.6e}")
