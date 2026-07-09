"""Test least-squares Trefftz-DG solver."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh
from pwdg_dirichlet import TrefftzDGLS


def make_pw(k, theta):
    d = np.array([np.cos(theta), np.sin(theta)])
    def u(pts, deriv=None):
        phase = k * (pts @ d)
        if deriv is None:
            return np.exp(1j * phase)
        return 1j * k * np.dot(d, deriv) * np.exp(1j * phase)
    return u


print("=" * 70)
print("Test 1: Exact reproduction (basis-aligned)")
print("=" * 70)
k = 2.0
mesh = make_unit_square_mesh(2)
for p in [4, 6, 8]:
    solver = TrefftzDGLS(mesh, k, p)
    u_ex = make_pw(k, 0.0)  # aligned with dirs[0]
    c, A, b = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    cond = np.linalg.cond(A)
    print(f"  p={p}: L2={err:.6e}  cond={cond:.2e}  c[:4]={c[:4]}")


print("\n" + "=" * 70)
print("Test 2: p-convergence (non-aligned plane wave)")
print("=" * 70)
for k in [1.0, 2.0, 4.0]:
    print(f"\n  k = {k}:")
    for n_mesh in [3, 4, 6]:
        mesh = make_unit_square_mesh(n_mesh)
        u_ex = make_pw(k, np.pi/7)
        print(f"    mesh n={n_mesh} ({mesh.n_elements} elements):")
        for p in [3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 24]:
            solver = TrefftzDGLS(mesh, k, p)
            c, A, b = solver.solve(u_ex)
            err = solver.L2_error(c, u_ex)
            dg = solver.DG_error(c, u_ex)
            cond = np.linalg.cond(A)
            print(f"      p={p:3d}: L2={err:.6e}  DG={dg:.6e}  cond={cond:.2e}")


print("\n" + "=" * 70) 
print("Test 3: Convergence check - should be exponential")
print("=" * 70)
k = 4.0
mesh = make_unit_square_mesh(4)
u_ex = make_pw(k, np.pi/7)
p_vals = []
errs = []
for p in [4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]:
    solver = TrefftzDGLS(mesh, k, p)
    c, _, _ = solver.solve(u_ex)
    err = solver.L2_error(c, u_ex)
    p_vals.append(p)
    errs.append(err)
    print(f"  p={p:3d}: L2={err:.6e}")

# Estimate convergence rate
import numpy as np
p_arr = np.array(p_vals[2:7], dtype=float)  # mid range before conditioning issues
e_arr = np.array(errs[2:7])
valid = e_arr > 0
if np.sum(valid) >= 2:
    fit = np.polyfit(p_arr[valid], np.log(e_arr[valid]), 1)
    print(f"\n  Estimated rate: error ~ exp({fit[0]:.3f} * p)")
    print(f"  (theoretical: exponential convergence expected)")
