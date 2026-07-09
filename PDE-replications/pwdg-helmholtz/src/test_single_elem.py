"""Test on a single triangular element to verify UWVF assembly."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mesh import _build_mesh
from uwvf_solver import UWVFSolver


# Single triangle: (0,0), (1,0), (0,1)
nodes = np.array([[0,0],[1,0],[0,1]], dtype=float)
elements = np.array([[0,1,2]])
mesh = _build_mesh(nodes, elements)

print(f"Elements: {mesh.n_elements}")
print(f"Edges: {mesh.n_edges}")
print(f"Boundary edges: {len(mesh.boundary_edges)}")
print(f"Interior edges: {len(mesh.interior_edges)}")

k = 2.0
p = 4

solver = UWVFSolver(mesh, k, p)
print(f"\nDirections:\n{solver.dirs}")

# Exact solution = basis direction 0 = (1, 0)
d0 = solver.dirs[0]

def u_exact(pts, deriv=None):
    phase = k * (pts @ d0)
    if deriv is None:
        return np.exp(1j * phase)
    return 1j * k * np.dot(d0, deriv) * np.exp(1j * phase)

c, A, b = solver.solve(u_exact)

# Exact coefficients: c[0] = 1, c[1:] = 0
c_exact = np.zeros(p, dtype=complex)
c_exact[0] = 1.0

print(f"\nA:\n{A}")
print(f"\nb: {b}")
print(f"\nA @ c_exact: {A @ c_exact}")
print(f"\nResidual: {A @ c_exact - b}")
print(f"||residual||: {np.linalg.norm(A @ c_exact - b):.6e}")

# Now check manually what A should be for a single element.
# All edges are boundary edges.
# For each boundary edge e of K:
#   LHS contribution: ∫_e |X_K(φ)|^2 / (2σ) ds
#   RHS contribution: ∫_e g · conj(X_K(φ)) / (2σ) ds
# where g = ∂u_ex/∂n_K + ik*u_ex (Robin BC data)

# For the exact solution u_ex = φ_0 = exp(ik d_0.x):
#   g = ∂φ_0/∂n_K + ik*φ_0 = ik(d_0·n_K)*φ_0 + ik*φ_0 = ik(1 + d_0·n_K)*φ_0
#   This is Y_K(φ_0) (the incoming trace of φ_0)

# So b_i = Σ_e ∫_e Y_K(φ_0) conj(X_K(φ_i)) / (2σ) ds
# And A_ij = Σ_e ∫_e X_K(φ_j) conj(X_K(φ_i)) / (2σ) ds

# For consistency: A @ c_exact = b means
# Σ_j A_ij c_exact_j = A_i0 (since c_exact = [1,0,0,0])
# and b_i = Σ_e ∫_e Y_K(φ_0) conj(X_K(φ_i)) / (2σ) ds

# So we need: A_i0 = b_i, i.e.,
# Σ_e ∫_e X_K(φ_0) conj(X_K(φ_i)) / (2σ) ds = Σ_e ∫_e Y_K(φ_0) conj(X_K(φ_i)) / (2σ) ds

# This means: Σ_e ∫_e [X_K(φ_0) - Y_K(φ_0)] conj(X_K(φ_i)) / (2σ) ds = 0

# X_K(φ_0) - Y_K(φ_0) = [-∂φ_0/∂n_K + ikφ_0] - [∂φ_0/∂n_K + ikφ_0] = -2∂φ_0/∂n_K

# So we need: Σ_e ∫_e (-2∂φ_0/∂n_K) conj(X_K(φ_i)) / (2σ) ds = 0
# i.e., Σ_e ∫_e (∂φ_0/∂n_K) conj(X_K(φ_i)) ds = 0

# This should hold by Green's theorem for Trefftz functions:
# ∫_∂K ∂φ_0/∂n_K · conj(ψ) ds = ∫_K (∇φ_0·∇conj(ψ) - k^2 φ_0 conj(ψ)) dx = 0
# when ψ is also a Helmholtz solution... BUT X_K(φ_i) is not a Helmholtz solution
# in general. X_K involves n_K which changes from edge to edge.

# Actually, X_K(φ_i) is edge-dependent (through n_K), so it's not a single global function.
# The integral Σ_e ∫_e (∂φ_0/∂n_K) conj(X_K(φ_i)) ds is NOT zero in general.

# Wait — this means the UWVF is NOT consistent for arbitrary boundary conditions?
# No — the point is that for the UWVF with Robin BC, the SYSTEM is different.
# On boundary edges, the term is NOT just A += X·X^H. There should be additional handling.

# Let me re-read the UWVF formulation more carefully.

print("\n\nLet me check each edge contribution separately:")
from quadrature import edge_quadrature

for eidx in range(mesh.n_edges):
    n_K = mesh.edge_normal(eidx, 0)
    pts, wts = edge_quadrature(mesh, eidx, solver.nq)
    
    X = solver._X(pts, n_K)  # (nq, p)
    Y = solver._Y(pts, n_K)  # (nq, p)
    
    sigma = k
    
    # A contribution from this edge
    A_edge = np.einsum('q,qi,qj->ij', wts/(2*sigma), np.conj(X), X)
    
    # b contribution from this edge (boundary, Robin BC)
    u_ex = u_exact(pts)
    du_ex = u_exact(pts, deriv=n_K)
    g = du_ex + 1j * k * u_ex  # This equals Y_K(φ_0)
    
    b_edge = np.einsum('q,q,qi->i', wts/(2*sigma), g, np.conj(X))
    
    # Check: is A_edge @ c_exact = b_edge?
    r = A_edge @ c_exact - b_edge
    
    print(f"\n  Edge {eidx}: normal = {n_K}")
    print(f"    A_edge @ c_exact = {A_edge @ c_exact}")
    print(f"    b_edge = {b_edge}")
    print(f"    residual = {r}")
    print(f"    ||residual|| = {np.linalg.norm(r):.6e}")
    
    # Verify: g should equal Y_K(φ_0) at quad points
    Y_phi0 = Y[:, 0]  # Y_K evaluated on basis function 0
    g_check = g
    print(f"    g vs Y(φ_0): max diff = {np.max(np.abs(g - Y_phi0)):.6e}")
