"""Test robust PWDG solver with TSVD and Tikhonov."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh
from pwdg_robust import RobustPWDG


def make_pw(k, theta):
    d = np.array([np.cos(theta), np.sin(theta)])
    def u(pts, deriv=None):
        phase = k * (pts @ d)
        if deriv is None:
            return np.exp(1j * phase)
        return 1j * k * np.dot(d, deriv) * np.exp(1j * phase)
    return u


print("=" * 70)
print("Test 1: p-convergence with TSVD (non-aligned plane wave)")
print("=" * 70)
k = 2.0
mesh = make_unit_square_mesh(3)
u_ex = make_pw(k, np.pi/7)

print(f"  mesh: {mesh.n_elements} elements, k={k}")
print(f"\n  {'p':>4s}  {'L2 (direct)':>12s}  {'L2 (TSVD)':>12s}  {'L2 (Tikh)':>12s}  {'cond':>10s}")
print("  " + "-"*65)

for p in [3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20]:
    for tol in [1e-12]:
        solver = RobustPWDG(mesh, k, p, svd_tol=tol)
        
        c_dir, A, b = solver.solve(u_ex, method='direct')
        e_dir = solver.L2_error(c_dir, u_ex)
        
        c_tsvd, _, _ = solver.solve(u_ex, method='tsvd')
        e_tsvd = solver.L2_error(c_tsvd, u_ex)
        
        c_tikh, _, _ = solver.solve(u_ex, method='tikhonov')
        e_tikh = solver.L2_error(c_tikh, u_ex)
        
        cond = np.linalg.cond(A)
        print(f"  {p:4d}  {e_dir:12.4e}  {e_tsvd:12.4e}  {e_tikh:12.4e}  {cond:10.2e}")


print("\n" + "=" * 70)
print("Test 2: Effect of SVD tolerance on accuracy")
print("=" * 70)
k = 4.0
mesh = make_unit_square_mesh(4)
u_ex = make_pw(k, np.pi/7)
p = 12

print(f"  mesh: {mesh.n_elements} elements, k={k}, p={p}")
print(f"\n  {'tol':>10s}  {'L2 error':>12s}  {'DG error':>12s}")
print("  " + "-"*40)

for tol in [1e-6, 1e-8, 1e-10, 1e-12, 1e-14]:
    solver = RobustPWDG(mesh, k, p, svd_tol=tol)
    c, _, _ = solver.solve(u_ex, method='tsvd')
    e_L2 = solver.L2_error(c, u_ex)
    e_DG = solver.DG_error(c, u_ex)
    print(f"  {tol:10.0e}  {e_L2:12.4e}  {e_DG:12.4e}")


print("\n" + "=" * 70)
print("Test 3: p-convergence for multiple k (TSVD)")
print("=" * 70)
mesh = make_unit_square_mesh(4)

for k in [1.0, 2.0, 4.0, 8.0]:
    u_ex = make_pw(k, np.pi/7)
    print(f"\n  k = {k}:")
    for p in [4, 6, 8, 10, 12, 14, 16, 20]:
        solver = RobustPWDG(mesh, k, p, svd_tol=1e-10)
        c, _, _ = solver.solve(u_ex, method='tsvd')
        err = solver.L2_error(c, u_ex)
        dg = solver.DG_error(c, u_ex)
        print(f"    p={p:3d}: L2={err:.6e}  DG={dg:.6e}")
