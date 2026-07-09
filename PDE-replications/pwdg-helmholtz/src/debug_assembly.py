"""
Debug the PWDG assembly by checking Galerkin orthogonality.

If u_exact = exp(ik d_0 · x) and d_0 is one of the basis directions,
then c_exact = [1, 0, 0, ..., 0] on each element (repeated).
The residual r = A @ c_exact - b should be zero.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import make_unit_square_mesh, _build_mesh
from pwdg_final import PWDG


k = 2.0
p = 4
mesh = make_unit_square_mesh(2)
solver = PWDG(mesh, k, p)

print(f"Directions:\n{solver.dirs}")

# Exact solution = plane wave in direction d_0 = (1, 0)
d0 = solver.dirs[0]
print(f"\nExact solution direction: {d0}")

def u_exact(pts, deriv=None):
    phase = k * (pts @ d0)
    if deriv is None:
        return np.exp(1j * phase)
    return 1j * k * np.dot(d0, deriv) * np.exp(1j * phase)

# The exact coefficient vector: on each element, coeff for d_0 is 1, others 0
c_exact = np.zeros(solver.ndof, dtype=complex)
for K in range(mesh.n_elements):
    c_exact[K * p] = 1.0  # direction 0

# Assemble
c_computed, A, b = solver.solve(u_exact)

# Check residual with exact coefficients
r = A @ c_exact - b
print(f"\nResidual ||A @ c_exact - b||: {np.linalg.norm(r):.6e}")
print(f"||b||: {np.linalg.norm(b):.6e}")
print(f"Relative residual: {np.linalg.norm(r) / np.linalg.norm(b):.6e}")

# Check what the computed solution residual is
r_comp = A @ c_computed - b
print(f"\n||A @ c_computed - b||: {np.linalg.norm(r_comp):.6e}")

# Let's look at the structure of A and b
print(f"\nA shape: {A.shape}")
print(f"A max: {np.max(np.abs(A)):.6e}")
print(f"b max: {np.max(np.abs(b)):.6e}")

# Check: is b zero when u_exact is a basis function?
# If the formulation is consistent, a_h(u_ex, v) = l_h(v) should hold,
# meaning A c_exact = b exactly.
print(f"\nFirst 8 entries of b: {b[:8]}")
print(f"First 8 entries of A@c_exact: {(A @ c_exact)[:8]}")
print(f"Difference: {(A @ c_exact - b)[:8]}")

# Let's also check: what are the interior edge contributions vs boundary?
# Separate assembly for debugging
print("\n--- Detailed edge analysis ---")
print(f"Interior edges: {len(mesh.interior_edges)}")
print(f"Boundary edges: {len(mesh.boundary_edges)}")

# Check if jump of exact solution across interior edges is zero
# (it should be, since exp(ik d.x) is continuous)
from quadrature import edge_quadrature
for eidx in mesh.interior_edges[:3]:
    adj = mesh.edge_to_elem[eidx]
    Kp, Km = adj[0][0], adj[1][0]
    ne = mesh.edge_normal(eidx, Kp)
    pts, wts = edge_quadrature(mesh, eidx, solver.nq)
    
    phi = solver._pw(pts)
    
    # Exact coefficients for both elements
    cp = c_exact[Kp*p:(Kp+1)*p]
    cm = c_exact[Km*p:(Km+1)*p]
    
    # Numerical solution on both sides
    uhp = phi @ cp
    uhm = phi @ cm
    
    jump = uhp - uhm
    
    # Exact solution
    uex = u_exact(pts)
    
    print(f"\n  Edge {eidx} (K+={Kp}, K-={Km}):")
    print(f"    ||u_h+ - u_ex||_edge = {np.sqrt(np.sum(wts * np.abs(uhp - uex)**2)):.6e}")
    print(f"    ||u_h- - u_ex||_edge = {np.sqrt(np.sum(wts * np.abs(uhm - uex)**2)):.6e}")
    print(f"    ||jump||_edge = {np.sqrt(np.sum(wts * np.abs(jump)**2)):.6e}")
    print(f"    cp = {cp}")
    print(f"    cm = {cm}")

# Let's check boundary contribution
print("\n--- Boundary edge analysis ---")
for eidx in mesh.boundary_edges[:3]:
    K = mesh.edge_to_elem[eidx][0][0]
    ne = mesh.edge_normal(eidx, K)
    pts, wts = edge_quadrature(mesh, eidx, solver.nq)
    
    phi = solver._pw(pts)
    dphi = solver._dpw(pts, ne)
    
    cK = c_exact[K*p:(K+1)*p]
    uh = phi @ cK
    duh = dphi @ cK
    
    uex = u_exact(pts)
    duex = u_exact(pts, deriv=ne)
    g = duex + 1j * k * uex
    
    print(f"\n  Edge {eidx} (K={K}):")
    print(f"    ||u_h - u_ex||_edge = {np.sqrt(np.sum(wts * np.abs(uh - uex)**2)):.6e}")
    print(f"    ||du_h/dn - du_ex/dn||_edge = {np.sqrt(np.sum(wts * np.abs(duh - duex)**2)):.6e}")
    print(f"    ||g|| = {np.sqrt(np.sum(wts * np.abs(g)**2)):.6e}")
