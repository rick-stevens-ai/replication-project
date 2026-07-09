"""Quick test of the final PWDG solver."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, _build_mesh
from pwdg_final import PWDG


def make_pw_exact(k, theta):
    """Make exact plane wave solution at angle theta."""
    d = np.array([np.cos(theta), np.sin(theta)])
    def u(pts, deriv=None):
        phase = k * (pts @ d)
        if deriv is None:
            return np.exp(1j * phase)
        return 1j * k * np.dot(d, deriv) * np.exp(1j * phase)
    return u


print("=" * 60)
print("Test 1: Exact reproduction (basis-aligned plane wave)")
print("=" * 60)
k = 2.0
for p in [4, 6, 8]:
    mesh = make_unit_square_mesh(2)
    solver = PWDG(mesh, k, p)
    # Use direction 0 (which IS a basis direction)
    theta = 0.0  # d = (1, 0) which is directions[0]
    u_ex = make_pw_exact(k, theta)
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    cond = np.linalg.cond(A)
    print(f"  p={p:2d}: L2 err = {err:.6e}, cond = {cond:.2e}")
    # Show coefficients for first element
    print(f"         c[0:p] = {c[:p]}")

print("\n" + "=" * 60)
print("Test 2: p-convergence (non-aligned plane wave)")
print("=" * 60)
k = 2.0
theta = np.pi / 7  # not aligned with any basis direction
u_ex = make_pw_exact(k, theta)
mesh = make_unit_square_mesh(3)
for p in [3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 24, 30]:
    solver = PWDG(mesh, k, p)
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    dg_err = solver.DG_error(c, u_ex)
    cond = np.linalg.cond(A)
    print(f"  p={p:3d}: L2={err:.6e}  DG={dg_err:.6e}  cond={cond:.2e}")

print("\n" + "=" * 60)
print("Test 3: Different k values")
print("=" * 60)
mesh = make_unit_square_mesh(4)
for k in [1.0, 2.0, 4.0, 8.0]:
    theta = np.pi / 7
    u_ex = make_pw_exact(k, theta)
    print(f"\n  k = {k}:")
    for p in [4, 8, 12, 16, 20]:
        solver = PWDG(mesh, k, p)
        c, _, _ = solver.solve(u_ex)
        err = solver.L2_error(c, u_ex)
        print(f"    p={p:3d}: L2={err:.6e}")

print("\n" + "=" * 60)
print("Test 4: Tiny mesh (2 triangles)")
print("=" * 60)
nodes = np.array([[0,0],[1,0],[1,1],[0,1]], dtype=float)
elements = np.array([[0,1,3],[1,2,3]])
mesh = _build_mesh(nodes, elements)
k = 2.0
u_ex = make_pw_exact(k, np.pi/7)
for p in [3, 4, 6, 8, 12, 16]:
    solver = PWDG(mesh, k, p)
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    print(f"  p={p:3d}: L2={err:.6e}  cond={np.linalg.cond(A):.2e}")
