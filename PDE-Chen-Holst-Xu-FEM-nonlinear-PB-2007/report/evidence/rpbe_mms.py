"""
RPBE manufactured-solution convergence test (2D).

Independent replication test of Theorem 6.2 (Chen, Holst, Xu 2007):
    ||u - u_h||_1  <~  inf_{v_h in V^h} ||u - v_h||_1  =  O(h)  (P1, u in H^2)

We solve, on Omega = (0,1)^2 with Dirichlet BC,
    -div(eps grad u) + kappabar^2 sinh(u + G) = f
using P1 finite elements. The exact regularized solution is chosen as
    u_ex(x,y) = sin(pi x) sin(pi y)  ,
G(x) = q / (eps_m |x - x0|) with x0 OUTSIDE Omega (so G is smooth on Omega,
matching the paper's smoothness setup), eps piecewise constant (uniform here
so we isolate the pure convergence-rate test), kappabar^2 = eps_s * kappa^2.

f is computed in closed form:
    f = -eps * lap(u_ex) + kappabar^2 * sinh(u_ex + G)

We measure ||u - u_h||_L2, |u - u_h|_H1_semi, ||u - u_h||_H1 across a
sequence of uniformly refined triangulations and report the empirical
convergence rates.
"""
from __future__ import annotations
import json, math, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from skfem import (MeshTri, Basis, ElementTriP1, BilinearForm, LinearForm,
                   condense, asm, solve)
from skfem.helpers import dot, grad

# ---------------- coefficients ----------------
EPS_M = 2.0
EPS_S = 80.0
KAPPA = 1.0
KAPPABAR2 = EPS_S * KAPPA * KAPPA       # = 80
EPS_UNIFORM = EPS_S                     # uniform on Omega (interface-free)

X0 = np.array([-1.5, -1.5])
Q  = 1.0

def G_val_xy(x, y):
    return Q / (EPS_M * np.sqrt((x - X0[0])**2 + (y - X0[1])**2))

def u_ex_xy(x, y):
    return np.sin(np.pi * x) * np.sin(np.pi * y)

def u_ex_grad_xy(x, y):
    return (np.pi * np.cos(np.pi*x) * np.sin(np.pi*y),
            np.pi * np.sin(np.pi*x) * np.cos(np.pi*y))

def u_ex_lap_xy(x, y):
    return -2.0 * np.pi * np.pi * np.sin(np.pi*x) * np.sin(np.pi*y)

def rhs_f_xy(x, y):
    return -EPS_UNIFORM * u_ex_lap_xy(x, y) + KAPPABAR2 * np.sinh(u_ex_xy(x, y) + G_val_xy(x, y))


# ---------------- weak forms (skfem 12) ----------------

@BilinearForm
def stiff(u, v, w):
    return EPS_UNIFORM * dot(grad(u), grad(v))

@BilinearForm
def reaction(u, v, w):
    # Jacobian block: int  kappabar^2 * cosh(u_h + G) * u * v  dx
    return KAPPABAR2 * w['cosh_arg'] * u * v

@LinearForm
def rhs_load(v, w):
    return w['fval'] * v

@LinearForm
def rhs_sinh(v, w):
    # For residual R(u_h) we need  + int kappabar^2 sinh(u_h + G) v
    return KAPPABAR2 * w['sinh_arg'] * v


def newton_solve(mesh, tol=1e-10, itmax=40, verbose=False):
    basis = Basis(mesh, ElementTriP1(), intorder=4)
    x_q, y_q = basis.global_coordinates()

    fval_q = rhs_f_xy(x_q, y_q)
    G_q    = G_val_xy(x_q, y_q)

    # Dirichlet BC on boundary DOFs
    D = basis.get_dofs()      # boundary DOF handle
    # nodal values of u_ex on mesh vertices (P1)
    xn, yn = mesh.p[0], mesh.p[1]
    u_ex_nodal = u_ex_xy(xn, yn)

    u = np.zeros(basis.N)
    # set boundary DOFs to u_ex
    bnodes = D.nodal['u']
    u[bnodes] = u_ex_nodal[bnodes]

    K_lin = asm(stiff, basis)
    fh    = asm(rhs_load, basis, fval=fval_q)

    for it in range(itmax):
        uh_q     = basis.interpolate(u).value if hasattr(basis.interpolate(u), 'value') else basis.interpolate(u)
        # basis.interpolate returns a DiscreteField; we want the ndarray of values
        uh_q     = np.asarray(basis.interpolate(u))     # shape (n_elems, n_quad)
        arg_q    = uh_q + G_q
        sinh_q   = np.sinh(arg_q)
        cosh_q   = np.cosh(arg_q)

        Rnl = asm(rhs_sinh, basis, sinh_arg=sinh_q)
        R   = K_lin @ u + Rnl - fh

        Jnl = asm(reaction, basis, cosh_arg=cosh_q)
        J   = K_lin + Jnl

        # Newton: solve J du = -R with Dirichlet on bnodes (du = 0 there)
        # Use skfem condense
        JJ, rhs_r, u_out, I = condense(J, -R, D=bnodes)
        du_int = spla.spsolve(JJ, rhs_r)
        du = np.zeros(basis.N); du[I] = du_int
        u  = u + du
        rn = np.linalg.norm(R[I])
        dn = np.linalg.norm(du_int)
        if verbose:
            print(f"  Newton it {it}:  |R_int|={rn:.3e}  |du_int|={dn:.3e}")
        if dn < tol:
            break
    return basis, u


def error_norms(basis, u_h):
    """L2, H1-semi, H1 errors, computed via quadrature using skfem's interpolate."""
    x_q, y_q = basis.global_coordinates()
    u_ex_q    = u_ex_xy(x_q, y_q)
    dux_q, duy_q = u_ex_grad_xy(x_q, y_q)

    uh_field  = basis.interpolate(u_h)                # DiscreteField
    uh_q      = np.asarray(uh_field)                  # (n_elems, n_quad)
    duh_x_q, duh_y_q = uh_field.grad                  # (n_elems, n_quad) each

    dx = basis.dx                                     # (n_elems, n_quad)
    err_q  = uh_q - u_ex_q
    L2     = np.sqrt(np.sum(err_q**2 * dx))
    dex_q  = duh_x_q - dux_q
    dey_q  = duh_y_q - duy_q
    H1s    = np.sqrt(np.sum((dex_q**2 + dey_q**2) * dx))
    H1     = np.sqrt(L2*L2 + H1s*H1s)
    return float(L2), float(H1s), float(H1)


def run_convergence(levels=range(1, 8)):
    results = []
    m = MeshTri()
    for lvl in levels:
        m = m.refined()
        h = 1.0 / (2 ** lvl)
        t0 = time.time()
        basis, u_h = newton_solve(m, verbose=(lvl <= 2))
        el = time.time() - t0
        L2, H1s, H1 = error_norms(basis, u_h)
        results.append({'level': lvl, 'h': h, 'ndof': int(basis.N),
                        'L2': L2, 'H1_semi': H1s, 'H1': H1,
                        'wall_sec': round(el, 3)})
        print(f"lvl {lvl}  h={h:.5f}  ndof={basis.N:>7d}  "
              f"|e|_L2={L2:.3e}  |e|_H1={H1:.3e}  ({el:.2f}s)")

    print("\nEmpirical rates (theory: L2 -> 2, H1 -> 1):")
    print(f"{'lvl':>3} {'h':>10} {'L2':>12} {'rL2':>6}  {'H1':>12} {'rH1':>6}")
    for i, r in enumerate(results):
        if i == 0:
            rL2 = rH1 = float('nan')
        else:
            pr = results[i-1]
            rL2 = math.log(pr['L2']/r['L2']) / math.log(pr['h']/r['h'])
            rH1 = math.log(pr['H1']/r['H1']) / math.log(pr['h']/r['h'])
            r['rate_L2'] = rL2
            r['rate_H1'] = rH1
        print(f"{r['level']:>3} {r['h']:>10.5f} {r['L2']:>12.3e} {rL2:>6.3f}  "
              f"{r['H1']:>12.3e} {rH1:>6.3f}")
    return results


if __name__ == "__main__":
    print("=" * 78)
    print("RPBE manufactured-solution FEM convergence test")
    print(f"eps={EPS_UNIFORM}, kappabar^2={KAPPABAR2}, atom outside at {X0.tolist()}")
    print("Exact u = sin(pi x) sin(pi y);  Omega = (0,1)^2;  P1 elements")
    print("=" * 78)
    results = run_convergence()
    out = {'setup': {'EPS': EPS_UNIFORM, 'KAPPABAR2': KAPPABAR2,
                     'X0': X0.tolist(), 'Q': Q,
                     'u_ex': 'sin(pi x) sin(pi y)',
                     'element': 'P1 Lagrange on MeshTri (refined 2-tri unit square)'},
           'results': results}
    with open('rpbe_mms_results.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("\nSaved rpbe_mms_results.json")
