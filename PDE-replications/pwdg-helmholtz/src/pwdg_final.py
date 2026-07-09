"""
PWDG solver — final clean implementation.

Helmholtz: -Δu - k²u = 0 in Ω ⊂ R²
Robin BC: ∂u/∂n + iku = g on ∂Ω

Trefftz DG with plane wave basis {exp(ikd_ℓ·x)}_{ℓ=1}^p per element.

Bilinear form a_h(u_h, v_h):

  Interior edge e between K⁺, K⁻ (normal n from K⁺ to K⁻):
    ∫_e [ -{∂u/∂n}[v̄] - [u]{∂v̄/∂n} + α[u][v̄] + δ[∂u/∂n][∂v̄/∂n] ] ds
    
    where [w] = w⁺ - w⁻,  {w} = ½(w⁺ + w⁻)

  Boundary edge e on K (with Robin BC incorporated):
    ∫_e [ (ik + α)u·v̄ - u·∂v̄/∂n - ikδ·u·∂v̄/∂n ] ds

Linear form l_h(v_h):
  Boundary edge e:
    ∫_e [ -g·v̄ + δ·g·∂v̄/∂n ] ds
    
    where g = ∂u_ex/∂n + ik·u_ex  (Robin data from exact solution)

This follows from: the full DG skeleton bilinear form on boundary has terms
  -∂u/∂n·v̄, -u·∂v̄/∂n, α·u·v̄, δ·∂u/∂n·∂v̄/∂n
and we substitute ∂u/∂n = g - iku in the terms that involve ∂u/∂n:
  -∂u/∂n·v̄ → iku·v̄ - g·v̄     (split to LHS and RHS)
  δ·∂u/∂n·∂v̄/∂n → -ikδu·∂v̄/∂n + δg·∂v̄/∂n  (split to LHS and RHS)
"""
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class PWDG:
    
    def __init__(self, mesh, k, p, nq=None):
        self.mesh = mesh
        self.k = float(k)
        self.p = int(p)
        
        # Quadrature points per edge
        h_max = max(mesh.element_diameter(i) for i in range(mesh.n_elements))
        self.nq = nq or max(int(np.ceil(4 * k * h_max / np.pi)) + 4, 2*p, 16)
        
        # Equispaced directions on unit circle
        angles = 2 * np.pi * np.arange(p) / p
        self.dirs = np.column_stack([np.cos(angles), np.sin(angles)])
        
        self.ndof = mesh.n_elements * p
        
        # Flux parameters (standard PWDG)
        self.alpha = 0.5 * k
        self.delta = 0.5 / k
    
    def _pw(self, pts):
        """(nq, p) plane wave values."""
        return np.exp(1j * self.k * (pts @ self.dirs.T))
    
    def _dpw(self, pts, n):
        """(nq, p) normal derivatives of plane waves."""
        return 1j * self.k * (self.dirs @ n)[None, :] * self._pw(pts)
    
    def solve(self, u_exact):
        """Assemble and solve. Returns coefficient vector."""
        p = self.p
        N = self.ndof
        A = np.zeros((N, N), dtype=complex)
        b = np.zeros(N, dtype=complex)
        
        # ---------- Interior edges ----------
        for eidx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[eidx]
            Kp, Km = adj[0][0], adj[1][0]
            ne = self.mesh.edge_normal(eidx, Kp)
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            
            phi = self._pw(pts)      # (nq, p) — same at both elements
            dphi = self._dpw(pts, ne)  # (nq, p) — same values, different DOFs
            
            ip = slice(Kp*p, (Kp+1)*p)
            im = slice(Km*p, (Km+1)*p)
            
            # Weighted outer products summed over quad points
            # phi^H diag(w) dphi = Σ_q w_q * conj(phi_q) ⊗ dphi_q
            # These are (p, p) matrices
            
            VV = np.einsum('q,qi,qj->ij', wts, np.conj(phi), phi)    # ∫ v̄·u
            VD = np.einsum('q,qi,qj->ij', wts, np.conj(phi), dphi)   # ∫ v̄·∂u/∂n
            DV = np.einsum('q,qi,qj->ij', wts, np.conj(dphi), phi)   # ∫ ∂v̄/∂n·u
            DD = np.einsum('q,qi,qj->ij', wts, np.conj(dphi), dphi)  # ∫ ∂v̄/∂n·∂u/∂n
            
            # Term 1: -∫ {∂u/∂n}[v̄] ds
            # = -∫ ½(∂u⁺/∂n + ∂u⁻/∂n)(v̄⁺ - v̄⁻) ds
            # Note: ∂u/∂n and v̄ have same functional form at the edge points,
            # but belong to different DOF sets.
            A[ip, ip] += -0.5 * VD   # -½ v̄⁺·∂u⁺/∂n
            A[ip, im] += -0.5 * VD   # -½ v̄⁺·∂u⁻/∂n
            A[im, ip] += +0.5 * VD   # +½ v̄⁻·∂u⁺/∂n  (minus from [v̄])
            A[im, im] += +0.5 * VD   # +½ v̄⁻·∂u⁻/∂n
            
            # Term 2: -∫ [u]{∂v̄/∂n} ds
            # = -∫ (u⁺ - u⁻)½(∂v̄⁺/∂n + ∂v̄⁻/∂n) ds
            A[ip, ip] += -0.5 * DV   # -½ ∂v̄⁺/∂n·u⁺
            A[ip, im] += +0.5 * DV   # +½ ∂v̄⁺/∂n·u⁻  (minus from [u])
            A[im, ip] += -0.5 * DV   # -½ ∂v̄⁻/∂n·u⁺
            A[im, im] += +0.5 * DV   # +½ ∂v̄⁻/∂n·u⁻
            
            # Term 3: α ∫ [u][v̄] ds = α ∫ (u⁺-u⁻)(v̄⁺-v̄⁻) ds
            A[ip, ip] += self.alpha * VV
            A[ip, im] -= self.alpha * VV
            A[im, ip] -= self.alpha * VV
            A[im, im] += self.alpha * VV
            
            # Term 4: δ ∫ [∂u/∂n][∂v̄/∂n] ds
            A[ip, ip] += self.delta * DD
            A[ip, im] -= self.delta * DD
            A[im, ip] -= self.delta * DD
            A[im, im] += self.delta * DD
        
        # ---------- Boundary edges (Robin BC) ----------
        for eidx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[eidx]
            K = adj[0][0]
            ne = self.mesh.edge_normal(eidx, K)
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            
            phi = self._pw(pts)
            dphi = self._dpw(pts, ne)
            
            ik = slice(K*p, (K+1)*p)
            
            VV = np.einsum('q,qi,qj->ij', wts, np.conj(phi), phi)
            DV = np.einsum('q,qi,qj->ij', wts, np.conj(dphi), phi)
            
            # LHS: (ik + α)u·v̄ - u·∂v̄/∂n - ikδ·u·∂v̄/∂n
            A[ik, ik] += (1j*self.k + self.alpha) * VV  # (ik+α)u·v̄
            A[ik, ik] -= DV                              # -u·∂v̄/∂n
            A[ik, ik] -= 1j*self.k*self.delta * DV       # -ikδ·u·∂v̄/∂n
            
            # RHS
            u_ex = u_exact(pts)
            du_ex = u_exact(pts, deriv=ne)
            g = du_ex + 1j * self.k * u_ex
            
            # l(v) = ∫ [-g·v̄ + δ·g·∂v̄/∂n] ds
            gw = wts * g  # (nq,) weighted g values
            b[ik] += np.einsum('q,qi->i', -gw, np.conj(phi))        # -g·v̄
            b[ik] += np.einsum('q,qi->i', self.delta*gw, np.conj(dphi))  # δg·∂v̄/∂n
        
        return np.linalg.solve(A, b), A, b
    
    def L2_error(self, coeffs, u_exact):
        err2 = 0.0
        for K in range(self.mesh.n_elements):
            pts, wts = element_quadrature(self.mesh, K, 10)
            ph = self._pw(pts)
            uh = ph @ coeffs[K*self.p:(K+1)*self.p]
            ue = u_exact(pts)
            err2 += np.sum(wts * np.abs(uh - ue)**2)
        return np.sqrt(max(0, np.real(err2)))
    
    def DG_error(self, coeffs, u_exact):
        err2 = 0.0
        p = self.p
        for eidx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[eidx]
            Kp, Km = adj[0][0], adj[1][0]
            ne = self.mesh.edge_normal(eidx, Kp)
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            ph = self._pw(pts)
            dph = self._dpw(pts, ne)
            jump = ph@coeffs[Kp*p:(Kp+1)*p] - ph@coeffs[Km*p:(Km+1)*p]
            djump = dph@coeffs[Kp*p:(Kp+1)*p] - dph@coeffs[Km*p:(Km+1)*p]
            err2 += self.alpha * np.sum(wts * np.abs(jump)**2)
            err2 += self.delta * np.sum(wts * np.abs(djump)**2)
        for eidx in self.mesh.boundary_edges:
            K = self.mesh.edge_to_elem[eidx][0][0]
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq)
            ph = self._pw(pts)
            uh = ph @ coeffs[K*p:(K+1)*p]
            ue = u_exact(pts)
            err2 += self.k * np.sum(wts * np.abs(uh - ue)**2)
        return np.sqrt(max(0, np.real(err2)))
