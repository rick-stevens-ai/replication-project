"""
Error functionals matching paper §4 Fig 4.2-4.6:

1. L^2(Omega) error:        sqrt( int_Omega |u_h - u|^2 dx )
2. Broken H^1 seminorm:     sqrt( sum_K int_K |grad u_h - grad u|^2 dx )
3. L^2-norm of jumps on skeleton:  sqrt( int_{F_h^I} |[u_h]|^2 ds )

Also: best L^2 projection of u onto the plane-wave space (per element)
to compare PWDG error against best-approx error (the "proj." curve in paper).
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from quadrature import edge_quadrature, element_quadrature


def l2_error_omega(mesh, solver, coeffs, u_exact, nq=12):
    """L^2(Omega) error."""
    err2 = 0.0
    p = solver.p
    for K in range(mesh.n_elements):
        pts, wts = element_quadrature(mesh, K, nq)
        phi = solver._pw(pts)
        uh = phi @ coeffs[K*p:(K+1)*p]
        ue = u_exact(pts)
        err2 += np.sum(wts * np.abs(uh - ue)**2)
    return np.sqrt(max(0, np.real(err2)))


def l2_norm_omega(mesh, u_exact, nq=14):
    """L^2(Omega) norm of u_exact (for relative errors)."""
    s = 0.0
    for K in range(mesh.n_elements):
        pts, wts = element_quadrature(mesh, K, nq)
        ue = u_exact(pts)
        s += np.sum(wts * np.abs(ue)**2)
    return np.sqrt(max(0, np.real(s)))


def broken_h1_seminorm_error(mesh, solver, coeffs, u_exact, nq=12):
    """sqrt( sum_K int_K |grad u_h - grad u|^2 dx ).

    grad of plane wave e^{i k d.x} is i k d e^{i k d.x}.
    grad of u_exact: we compute by directional derivative along (1,0) and (0,1).
    """
    err2 = 0.0
    p = solver.p
    k = solver.k
    dirs = solver.dirs  # (p,2)
    ex = np.array([1.0, 0.0])
    ey = np.array([0.0, 1.0])
    for K in range(mesh.n_elements):
        pts, wts = element_quadrature(mesh, K, nq)
        # PWDG grad: i k d * phi
        phi = solver._pw(pts)  # (nq, p)
        # grad_x_h = sum_l c_l * i*k*d_l[0] * phi[:,l]
        c = coeffs[K*p:(K+1)*p]
        grad_x_h = phi @ (1j * k * dirs[:, 0] * c)
        grad_y_h = phi @ (1j * k * dirs[:, 1] * c)
        grad_x_e = u_exact(pts, deriv=ex)
        grad_y_e = u_exact(pts, deriv=ey)
        err2 += np.sum(wts * (np.abs(grad_x_h - grad_x_e)**2 + np.abs(grad_y_h - grad_y_e)**2))
    return np.sqrt(max(0, np.real(err2)))


def jump_l2_skeleton(mesh, solver, coeffs, nq=20):
    """sqrt( sum_{e in interior edges} int_e |[u_h]|^2 ds )."""
    err2 = 0.0
    p = solver.p
    for eidx in mesh.interior_edges:
        adj = mesh.edge_to_elem[eidx]
        Kp, Km = adj[0][0], adj[1][0]
        pts, wts = edge_quadrature(mesh, eidx, nq)
        phi = solver._pw(pts)
        jump = phi @ coeffs[Kp*p:(Kp+1)*p] - phi @ coeffs[Km*p:(Km+1)*p]
        err2 += np.sum(wts * np.abs(jump)**2)
    return np.sqrt(max(0, np.real(err2)))


def l2_projection_errors(mesh, solver, u_exact, nq=14):
    """Compute element-wise best L^2 projection of u onto plane-wave space.

    Returns the L^2(Omega) error of the L^2 projection (the "proj." curve).
    """
    p = solver.p
    proj_coeffs = np.zeros(mesh.n_elements * p, dtype=complex)
    for K in range(mesh.n_elements):
        pts, wts = element_quadrature(mesh, K, nq)
        phi = solver._pw(pts)  # (nq, p)
        # M_ij = int phi_i* phi_j ; b_i = int phi_i* u
        M = np.einsum('q,qi,qj->ij', wts, np.conj(phi), phi)
        b = np.einsum('q,qi,q->i', wts, np.conj(phi), u_exact(pts))
        # Regularize tiny basis ill-conditioning
        c = np.linalg.lstsq(M, b, rcond=1e-14)[0]
        proj_coeffs[K*p:(K+1)*p] = c
    err2 = 0.0
    for K in range(mesh.n_elements):
        pts, wts = element_quadrature(mesh, K, nq)
        phi = solver._pw(pts)
        c = proj_coeffs[K*p:(K+1)*p]
        diff = phi @ c - u_exact(pts)
        err2 += np.sum(wts * np.abs(diff)**2)
    return np.sqrt(max(0, np.real(err2))), proj_coeffs
