"""
Ultra-Weak Variational Formulation (UWVF) for 2D Helmholtz.

Following Cessenat & Després (1998) and Huttunen, Monk, Kaipio (2002).

The UWVF is the original and best-understood Trefftz-DG method for Helmholtz.

Formulation:
  For each element K, define the impedance trace operators:
    X_K = -∂u/∂n_K + iσu  (outgoing impedance trace from K)
    Y_K = ∂u/∂n_K + iσu   (incoming impedance trace to K)
  
  where n_K is the outward normal from K and σ = k (wavenumber).
  
  These satisfy: X_K + Y_K = 2iσu (on ∂K)
                 X_K - Y_K = -2∂u/∂n_K (on ∂K)

The UWVF seeks u_h such that on each element K:
  ∫_∂K X_K(u_h) · conj(X_K(v_h)) / (2σ) ds
  = ∫_{∂K∩Γ_I} Y_K(u_h^{ext}) · conj(X_K(v_h)) / (2σ) ds  (interior)
  + ∫_{∂K∩∂Ω} Q·X_K(u_h) · conj(X_K(v_h)) / (2σ) ds  (reflection BC)
  + ∫_{∂K∩∂Ω} g · conj(X_K(v_h)) / (2σ) ds  (source)

For interior edges shared by K and K':
  Y_K(u_h^{ext}) = X_{K'}(u_h)  (the incoming wave to K is the outgoing wave from K')

For Robin BC (∂u/∂n + iku = g on ∂Ω):
  On the boundary, Y_K = ∂u/∂n_K + iσu = g (the Robin data IS the incoming trace)
  So Q = 0 (no reflection) and the source term is g.

For plane wave basis φ_ℓ(x) = exp(ik d_ℓ · x):
  X_K(φ_ℓ) = -∂φ_ℓ/∂n_K + ikφ_ℓ = (-ik(d_ℓ·n_K) + ik)φ_ℓ = ik(1 - d_ℓ·n_K)φ_ℓ
"""
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class UWVFSolver:
    
    def __init__(self, mesh, k, p, nq=None):
        self.mesh = mesh
        self.k = float(k)
        self.p = int(p)
        
        h_max = max(mesh.element_diameter(i) for i in range(mesh.n_elements))
        self.nq = nq or max(int(np.ceil(4 * k * h_max / np.pi)) + 4, 2*p, 16)
        
        angles = 2 * np.pi * np.arange(p) / p
        self.dirs = np.column_stack([np.cos(angles), np.sin(angles)])
        
        self.ndof = mesh.n_elements * p
    
    def _pw(self, pts):
        """(nq, p) plane wave values."""
        return np.exp(1j * self.k * (pts @ self.dirs.T))
    
    def _X(self, pts, n_K):
        """Outgoing impedance trace: X_K(φ) = ik(1 - d·n_K)φ.
        Returns (nq, p) complex."""
        phi = self._pw(pts)
        dn = self.dirs @ n_K  # (p,)
        coeff = 1j * self.k * (1.0 - dn)  # (p,)
        return coeff[None, :] * phi  # (nq, p)
    
    def _Y(self, pts, n_K):
        """Incoming impedance trace: Y_K(φ) = ik(1 + d·n_K)φ.
        Returns (nq, p) complex.
        
        Note: Y_K(φ) = ∂φ/∂n_K + ikφ = ik(d·n_K)φ + ikφ = ik(1 + d·n_K)φ
        """
        phi = self._pw(pts)
        dn = self.dirs @ n_K  # (p,)
        coeff = 1j * self.k * (1.0 + dn)  # (p,)
        return coeff[None, :] * phi  # (nq, p)
    
    def solve(self, u_exact):
        """Assemble and solve the UWVF system.
        
        u_exact(pts) -> solution values
        u_exact(pts, deriv=n) -> normal derivative
        """
        p = self.p
        N = self.ndof
        sigma = self.k
        
        A = np.zeros((N, N), dtype=complex)
        b = np.zeros(N, dtype=complex)
        
        # For each element K, we need to integrate over ∂K.
        # ∂K consists of edges that are either interior or boundary.
        
        # Build element-to-edge map
        elem_edges = [[] for _ in range(self.mesh.n_elements)]
        for eidx in range(self.mesh.n_edges):
            for (elem, _) in self.mesh.edge_to_elem[eidx]:
                elem_edges[elem].append(eidx)
        
        interior_set = set(self.mesh.interior_edges.tolist())
        boundary_set = set(self.mesh.boundary_edges.tolist())
        
        for K in range(self.mesh.n_elements):
            sK = slice(K*p, (K+1)*p)
            
            for eidx in elem_edges[K]:
                n_K = self.mesh.edge_normal(eidx, K)  # outward normal from K
                pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
                
                X_K = self._X(pts, n_K)  # (nq, p) outgoing from K
                
                # LHS: ∫ X_K(u) · conj(X_K(v)) / (2σ) ds
                # = Σ_q w_q * X_K(φ_j)[q] * conj(X_K(φ_i))[q] / (2σ)
                # A[sK, sK] += (1/(2σ)) * Σ_q w_q * conj(X_K)^T X_K
                
                M = np.einsum('q,qi,qj->ij', wts/(2*sigma), np.conj(X_K), X_K)
                A[sK, sK] += M
                
                if eidx in interior_set:
                    # Find neighbor element K'
                    adj = self.mesh.edge_to_elem[eidx]
                    if adj[0][0] == K:
                        Kp = adj[1][0]
                    else:
                        Kp = adj[0][0]
                    
                    sKp = slice(Kp*p, (Kp+1)*p)
                    
                    # n_{K'} = -n_K (outward from K' at this edge)
                    n_Kp = -n_K
                    
                    # RHS (bilinear): Y_K(u_ext) = X_{K'}(u_h)
                    # The incoming wave to K from K' is the outgoing wave from K'
                    # X_{K'}(φ) = ik(1 - d·n_{K'})φ = ik(1 + d·n_K)φ
                    X_Kp = self._X(pts, n_Kp)  # outgoing from K' (= incoming to K)
                    
                    # ∫ X_{K'}(u) · conj(X_K(v)) / (2σ) ds
                    # A[test=K, trial=K'] += (1/(2σ)) * Σ_q w_q * conj(X_K) * X_{K'}
                    M_cross = np.einsum('q,qi,qj->ij', wts/(2*sigma), np.conj(X_K), X_Kp)
                    A[sK, sKp] -= M_cross  # negative because moved to LHS
                
                elif eidx in boundary_set:
                    # Robin BC: ∂u/∂n_K + iku = g
                    # Y_K(u) = ∂u/∂n_K + iku = g (Robin data)
                    # So the RHS gets: ∫ g · conj(X_K(v)) / (2σ) ds
                    
                    # No reflection (Q = 0 for absorbing BC)
                    
                    # Compute g from exact solution
                    u_ex = u_exact(pts)
                    du_ex = u_exact(pts, deriv=n_K)
                    g = du_ex + 1j * self.k * u_ex
                    
                    # b[sK] += (1/(2σ)) * Σ_q w_q * g_q * conj(X_K(φ_i)_q)
                    b[sK] += np.einsum('q,q,qi->i', wts/(2*sigma), g, np.conj(X_K))
        
        coeffs = np.linalg.solve(A, b)
        return coeffs, A, b
    
    def L2_error(self, coeffs, u_exact):
        err2 = 0.0
        for K in range(self.mesh.n_elements):
            pts, wts = element_quadrature(self.mesh, K, 10)
            phi = self._pw(pts)
            uh = phi @ coeffs[K*self.p:(K+1)*self.p]
            ue = u_exact(pts)
            err2 += np.sum(wts * np.abs(uh - ue)**2)
        return np.sqrt(max(0, np.real(err2)))
    
    def DG_error(self, coeffs, u_exact):
        """Compute error in UWVF/impedance norm on skeleton."""
        err2 = 0.0
        p = self.p
        sigma = self.k
        
        for eidx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[eidx]
            Kp, Km = adj[0][0], adj[1][0]
            n_Kp = self.mesh.edge_normal(eidx, Kp)
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            
            phi = self._pw(pts)
            
            uhp = phi @ coeffs[Kp*p:(Kp+1)*p]
            uhm = phi @ coeffs[Km*p:(Km+1)*p]
            ue = u_exact(pts)
            
            # Jump of u_h (exact solution is continuous)
            jump = uhp - uhm
            err2 += sigma * np.sum(wts * np.abs(jump)**2)
        
        for eidx in self.mesh.boundary_edges:
            K = self.mesh.edge_to_elem[eidx][0][0]
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            phi = self._pw(pts)
            uh = phi @ coeffs[K*p:(K+1)*p]
            ue = u_exact(pts)
            err2 += sigma * np.sum(wts * np.abs(uh - ue)**2)
        
        return np.sqrt(max(0, np.real(err2)))
