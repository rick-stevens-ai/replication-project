"""
Robust PWDG/UWVF solver with regularization for ill-conditioned systems.

The plane wave basis {exp(ikd_l·x)} becomes increasingly ill-conditioned
as p increases (many nearly-parallel directions). This is a known issue
for all Trefftz methods and is addressed through:
1. Truncated SVD (TSVD) solving
2. Proper scaling/preconditioning

Reference: Hiptmair, Moiola, Perugia, SIAM J. Numer. Anal. 49(1), 2011
Also: Huttunen, Monk, Kaipio, J. Comput. Acoust., 2002
"""
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class RobustPWDG:
    """PWDG solver using the UWVF formulation with robust linear algebra."""
    
    def __init__(self, mesh, k, p, nq=None, svd_tol=1e-12):
        self.mesh = mesh
        self.k = float(k)
        self.p = int(p)
        self.svd_tol = svd_tol
        
        h_max = max(mesh.element_diameter(i) for i in range(mesh.n_elements))
        self.nq = nq or max(int(np.ceil(4 * k * h_max / np.pi)) + 4, 2*p, 20)
        
        angles = 2 * np.pi * np.arange(p) / p
        self.dirs = np.column_stack([np.cos(angles), np.sin(angles)])
        
        self.ndof = mesh.n_elements * p
        
        # Build element -> edge map
        self.elem_edges = [[] for _ in range(mesh.n_elements)]
        for eidx in range(mesh.n_edges):
            for (elem, _) in mesh.edge_to_elem[eidx]:
                self.elem_edges[elem].append(eidx)
        
        self.interior_set = set(mesh.interior_edges.tolist())
        self.boundary_set = set(mesh.boundary_edges.tolist())
    
    def _pw(self, pts):
        return np.exp(1j * self.k * (pts @ self.dirs.T))
    
    def _X(self, pts, n_K):
        """Outgoing impedance trace: X_K(φ) = ik(1 - d·n_K)φ"""
        phi = self._pw(pts)
        dn = self.dirs @ n_K
        return 1j * self.k * (1.0 - dn)[None, :] * phi
    
    def assemble(self, u_exact):
        """Assemble UWVF system with proper element-by-element structure."""
        p = self.p
        N = self.ndof
        sigma = self.k
        
        A = np.zeros((N, N), dtype=complex)
        b = np.zeros(N, dtype=complex)
        
        for K in range(self.mesh.n_elements):
            sK = slice(K*p, (K+1)*p)
            
            for eidx in self.elem_edges[K]:
                n_K = self.mesh.edge_normal(eidx, K)
                pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
                w_scaled = wts / (2 * sigma)
                
                XK = self._X(pts, n_K)  # (nq, p)
                
                # LHS: ∫ X_K(u) conj(X_K(v)) / (2σ) ds
                A[sK, sK] += np.einsum('q,qi,qj->ij', w_scaled, np.conj(XK), XK)
                
                if eidx in self.interior_set:
                    # Find neighbor
                    adj = self.mesh.edge_to_elem[eidx]
                    Kp = adj[1][0] if adj[0][0] == K else adj[0][0]
                    sKp = slice(Kp*p, (Kp+1)*p)
                    n_Kp = -n_K
                    
                    # X_{K'}(u) outgoing from K' = incoming to K
                    XKp = self._X(pts, n_Kp)  # (nq, p)
                    
                    # Move RHS coupling to LHS: A[K,K'] -= coupling
                    A[sK, sKp] -= np.einsum('q,qi,qj->ij', w_scaled, np.conj(XK), XKp)
                
                elif eidx in self.boundary_set:
                    # Robin BC: g = ∂u/∂n_K + iku
                    u_ex = u_exact(pts)
                    du_ex = u_exact(pts, deriv=n_K)
                    g = du_ex + 1j * self.k * u_ex
                    
                    b[sK] += np.einsum('q,q,qi->i', w_scaled, g, np.conj(XK))
        
        return A, b
    
    def solve(self, u_exact, method='tsvd'):
        """Solve with regularization.
        
        Methods:
          'direct': np.linalg.solve (no regularization)
          'tsvd': truncated SVD
          'tikhonov': Tikhonov regularization
        """
        A, b = self.assemble(u_exact)
        
        if method == 'direct':
            return np.linalg.solve(A, b), A, b
        
        elif method == 'tsvd':
            U, s, Vh = np.linalg.svd(A)
            # Truncate small singular values
            s_max = s[0]
            mask = s / s_max > self.svd_tol
            s_inv = np.zeros_like(s)
            s_inv[mask] = 1.0 / s[mask]
            n_kept = np.sum(mask)
            
            coeffs = Vh.conj().T @ (np.diag(s_inv) @ (U.conj().T @ b))
            return coeffs, A, b
        
        elif method == 'tikhonov':
            # Tikhonov: (A^H A + λI)x = A^H b
            lam = self.svd_tol * np.linalg.norm(A, 2)**2
            AHA = A.conj().T @ A + lam * np.eye(A.shape[0])
            AHb = A.conj().T @ b
            return np.linalg.solve(AHA, AHb), A, b
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
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
        err2 = 0.0
        p = self.p
        sigma = self.k
        
        for eidx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[eidx]
            Kp, Km = adj[0][0], adj[1][0]
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            phi = self._pw(pts)
            jump = phi@coeffs[Kp*p:(Kp+1)*p] - phi@coeffs[Km*p:(Km+1)*p]
            err2 += sigma * np.sum(wts * np.abs(jump)**2)
        
        for eidx in self.mesh.boundary_edges:
            K = self.mesh.edge_to_elem[eidx][0][0]
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            phi = self._pw(pts)
            uh = phi @ coeffs[K*p:(K+1)*p]
            ue = u_exact(pts)
            err2 += sigma * np.sum(wts * np.abs(uh - ue)**2)
        
        return np.sqrt(max(0, np.real(err2)))
