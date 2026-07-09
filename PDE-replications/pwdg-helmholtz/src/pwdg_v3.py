"""
PWDG solver v3 — Clean implementation following the ultra-weak variational 
formulation (UWVF) / PWDG framework.

For the 2D Helmholtz equation: -Δu - k²u = 0 in Ω

The PWDG formulation (following Gittelson, Hiptmair, Perugia 2009 and
the Trefftz-DG framework) with impedance boundary conditions:

Basis: {exp(i k d_ℓ · x)}_{ℓ=1}^p on each element K.

Key insight for Trefftz methods:
- All basis functions satisfy -Δφ - k²φ = 0 exactly
- Volume terms vanish after integration by parts
- The bilinear form consists ONLY of edge integrals

The UWVF formulation (Cessenat-Després):
  Find u_h such that for all test functions v_h:
  
  Σ_{K} ∫_{∂K} [(-∂u_h/∂n_K + iσu_h)·conj(-∂v_h/∂n_K - iσv_h)] / (2σ) ds = RHS

  where σ = k (wavenumber) and n_K is outward normal from K.

This is equivalent to the PWDG form with specific choice of flux parameters.

Alternative (cleaner) approach: direct assembly of the DG bilinear form.

The sesquilinear form a_h(u,v) on the skeleton:

Interior edges (shared by K+ and K-):
  ∫_e [-{∂u/∂n_e}[v̄] - [u]{∂v̄/∂n_e} + α[u][v̄] + δ[∂u/∂n_e][∂v̄/∂n_e]] ds

  where n_e is a fixed normal (say, from K+ to K-),
  [w] = w|_{K+} - w|_{K-},  {w} = (w|_{K+} + w|_{K-})/2

Boundary edges (on element K, Robin/impedance BC: ∂u/∂n + iku = g):
  ∫_e [iku·v̄ + αu·v̄ - u·∂v̄/∂n] ds

  with RHS:
  ∫_e g·v̄ ds
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class PWDGSolverV3:
    
    def __init__(self, mesh, k, p, flux='PWDG', nq_edge=None):
        self.mesh = mesh
        self.k = float(k)
        self.p = int(p)
        
        # Quadrature: need enough points to integrate products of plane waves
        # Two plane waves: exp(ik d1.x) * exp(-ik d2.x) = exp(ik(d1-d2).x)
        # Max frequency: 2k, over edge of length h. Need nq > 2kh/pi roughly.
        h_max = max(mesh.element_diameter(i) for i in range(mesh.n_elements))
        min_nq = max(int(np.ceil(2 * k * h_max / np.pi)) + 2, p + 2)
        self.nq_edge = nq_edge if nq_edge is not None else max(min_nq, 16)
        
        # Directions
        angles = 2.0 * np.pi * np.arange(p) / p
        self.dirs = np.column_stack([np.cos(angles), np.sin(angles)])
        
        self.ndof = mesh.n_elements * p
        
        # Flux parameters
        if flux == 'PWDG':
            self.alpha = 0.5 * k   # interior stabilization
            self.delta = 0.5 / k   # interior normal deriv stabilization
        elif flux == 'UWVF':
            self.alpha = 0.5 * k
            self.delta = 0.5 / k
    
    def _pw(self, pts):
        """Evaluate all plane waves at points. Returns (nq, p) complex."""
        return np.exp(1j * self.k * (pts @ self.dirs.T))
    
    def _dpw_dn(self, pts, n):
        """Normal derivative of plane waves. Returns (nq, p) complex."""
        # d/dn exp(ikd.x) = ik(d.n) exp(ikd.x)
        dn = self.dirs @ n  # (p,)
        return 1j * self.k * dn[None, :] * self._pw(pts)
    
    def assemble(self, u_exact):
        """
        Assemble A, b for the PWDG system.
        
        u_exact(pts) returns complex solution values at pts (nq, 2).
        u_exact(pts, deriv=normal) returns directional derivative.
        """
        N = self.ndof
        p = self.p
        A = np.zeros((N, N), dtype=complex)
        b = np.zeros(N, dtype=complex)
        
        # ---- Interior edges ----
        for eidx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[eidx]
            Kp, Km = adj[0][0], adj[1][0]
            n_e = self.mesh.edge_normal(eidx, Kp)  # from Kp outward
            
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq_edge)
            
            # All plane waves evaluated at same physical points
            phi = self._pw(pts)        # (nq, p)
            dphi = self._dpw_dn(pts, n_e)  # (nq, p)
            
            # DOF slices
            sp, sm = Kp * p, Km * p
            
            # Vectorized assembly over all quad points
            # For each quad point q with weight w:
            #   jump_trial_{+} = phi[q,:] (from K+)
            #   jump_trial_{-} = -phi[q,:] (from K-)
            #   avg_dtrial_{+} = 0.5 * dphi[q,:] (from K+)
            #   avg_dtrial_{-} = 0.5 * dphi[q,:] (from K-, same normal)
            #
            # Note: phi values are the SAME on both sides (same physical points,
            # same global plane wave functions). The difference comes from which
            # element's DOFs they're attached to.
            
            for q in range(len(pts)):
                w = wts[q]
                ph = phi[q, :]     # (p,) plane wave values
                dph = dphi[q, :]   # (p,) normal derivatives
                ph_c = np.conj(ph)
                dph_c = np.conj(dph)
                
                # Term 1: -∫ {∂u/∂n_e} [v̄] ds
                # {∂u/∂n_e} = 0.5*(∂u+/∂n + ∂u-/∂n) using n_e
                # For trial on K+: contrib to avg = 0.5*dph
                # For trial on K-: contrib to avg = 0.5*dph (same values at same points!)
                # [v̄] = v̄+ - v̄- = ph_c (from K+) - ph_c (from K-) = ph_c for K+, -ph_c for K-
                
                # (test K+, trial K+): -w * ph_c * 0.5*dph
                A[sp:sp+p, sp:sp+p] -= w * np.outer(ph_c, 0.5*dph)
                # (test K+, trial K-): -w * ph_c * 0.5*dph
                A[sp:sp+p, sm:sm+p] -= w * np.outer(ph_c, 0.5*dph)
                # (test K-, trial K+): -w * (-ph_c) * 0.5*dph = +w * ph_c * 0.5*dph
                A[sm:sm+p, sp:sp+p] += w * np.outer(ph_c, 0.5*dph)
                # (test K-, trial K-): +w * ph_c * 0.5*dph
                A[sm:sm+p, sm:sm+p] += w * np.outer(ph_c, 0.5*dph)
                
                # Term 2: -∫ [u] {∂v̄/∂n_e} ds
                # [u] = u+ - u- = ph (K+) - ph (K-) = ph for K+, -ph for K-
                # {∂v̄/∂n_e} = 0.5*(dph_c from K+ + dph_c from K-)
                
                # (test K+, trial K+): -w * 0.5*dph_c * ph
                A[sp:sp+p, sp:sp+p] -= w * np.outer(0.5*dph_c, ph)
                # (test K+, trial K-): -w * 0.5*dph_c * (-ph) = +w * 0.5*dph_c * ph
                A[sp:sp+p, sm:sm+p] += w * np.outer(0.5*dph_c, ph)
                # (test K-, trial K+): -w * 0.5*dph_c * ph
                A[sm:sm+p, sp:sp+p] -= w * np.outer(0.5*dph_c, ph)
                # (test K-, trial K-): +w * 0.5*dph_c * ph
                A[sm:sm+p, sm:sm+p] += w * np.outer(0.5*dph_c, ph)
                
                # Term 3: α ∫ [u][v̄] ds
                # [u]·[v̄] contributions:
                # (K+,K+): α*w * ph_c * ph
                A[sp:sp+p, sp:sp+p] += self.alpha * w * np.outer(ph_c, ph)
                # (K+,K-): -α*w * ph_c * ph
                A[sp:sp+p, sm:sm+p] -= self.alpha * w * np.outer(ph_c, ph)
                # (K-,K+): -α*w * ph_c * ph
                A[sm:sm+p, sp:sp+p] -= self.alpha * w * np.outer(ph_c, ph)
                # (K-,K-): α*w * ph_c * ph
                A[sm:sm+p, sm:sm+p] += self.alpha * w * np.outer(ph_c, ph)
                
                # Term 4: δ ∫ [∂u/∂n][∂v̄/∂n] ds
                # Same structure as term 3 but with dph
                A[sp:sp+p, sp:sp+p] += self.delta * w * np.outer(dph_c, dph)
                A[sp:sp+p, sm:sm+p] -= self.delta * w * np.outer(dph_c, dph)
                A[sm:sm+p, sp:sp+p] -= self.delta * w * np.outer(dph_c, dph)
                A[sm:sm+p, sm:sm+p] += self.delta * w * np.outer(dph_c, dph)
        
        # ---- Boundary edges ----
        # Robin/impedance BC: ∂u/∂n + iku = g on ∂Ω
        for eidx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[eidx]
            K = adj[0][0]
            n_e = self.mesh.edge_normal(eidx, K)
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq_edge)
            
            phi = self._pw(pts)
            dphi = self._dpw_dn(pts, n_e)
            
            s = K * p
            
            # Compute BC data
            u_ex = u_exact(pts)
            du_ex = u_exact(pts, deriv=n_e)
            g = du_ex + 1j * self.k * u_ex  # Robin data
            
            for q in range(len(pts)):
                w = wts[q]
                ph = phi[q, :]
                dph = dphi[q, :]
                ph_c = np.conj(ph)
                dph_c = np.conj(dph)
                
                # On boundary, no jump (single element).
                # The boundary bilinear form:
                #   a_h|_∂Ω(u,v) = ∫_e [-∂u/∂n · v̄ - u · ∂v̄/∂n + αu·v̄ + δ∂u/∂n·∂v̄/∂n] ds
                #
                # Substituting ∂u/∂n = g - iku for the exact solution:
                #   = ∫_e [-(g-iku)v̄ - u∂v̄/∂n + αuv̄ + δ(g-iku)∂v̄/∂n] ds
                #   = ∫_e [ikuv̄ - u∂v̄/∂n + αuv̄ - ikδu∂v̄/∂n] ds
                #     + ∫_e [-gv̄ + δg∂v̄/∂n] ds
                #
                # LHS (bilinear form) contributions from u:
                # (ik + α)u·v̄
                A[s:s+p, s:s+p] += (1j*self.k + self.alpha) * w * np.outer(ph_c, ph)
                # -u·∂v̄/∂n
                A[s:s+p, s:s+p] -= w * np.outer(dph_c, ph)
                # -ikδ·u·∂v̄/∂n
                A[s:s+p, s:s+p] -= 1j*self.k*self.delta * w * np.outer(dph_c, ph)
                
                # Wait — but the full boundary bilinear form should also include
                # the ∂u/∂n terms that DON'T get substituted.
                # 
                # Actually for the direct PWDG approach:
                # We DON'T substitute the BC. Instead, we keep the full bilinear form
                # and the BC enters through the RHS.
                #
                # Let me use the approach where the boundary terms are:
                # a_h|_∂Ω(u,v) = ∫[-∂u/∂n·v̄ - u·∂v̄/∂n + αu·v̄ + δ·∂u/∂n·∂v̄/∂n] ds
                # This is the "natural" DG boundary form, same as interior but without
                # the jump/average (since there's only one element).
                #
                # Then the Robin BC is imposed through:
                # l(v)|_∂Ω = ∫ g·(-v̄ + δ·∂v̄/∂n) ds
                
                # Let me UNDO the above and redo properly.
                A[s:s+p, s:s+p] -= (1j*self.k + self.alpha) * w * np.outer(ph_c, ph)
                A[s:s+p, s:s+p] += w * np.outer(dph_c, ph)
                A[s:s+p, s:s+p] += 1j*self.k*self.delta * w * np.outer(dph_c, ph)
                
                # CORRECT boundary bilinear form (NO BC substitution):
                # a_h(u,v)|_∂Ω = ∫[-∂u/∂n·v̄ - u·∂v̄/∂n + α·u·v̄ + δ·∂u/∂n·∂v̄/∂n] ds
                
                # -∂u/∂n · v̄
                A[s:s+p, s:s+p] -= w * np.outer(ph_c, dph)
                # -u · ∂v̄/∂n
                A[s:s+p, s:s+p] -= w * np.outer(dph_c, ph)
                # α·u·v̄
                A[s:s+p, s:s+p] += self.alpha * w * np.outer(ph_c, ph)
                # δ·∂u/∂n · ∂v̄/∂n
                A[s:s+p, s:s+p] += self.delta * w * np.outer(dph_c, dph)
                
                # RHS for Robin BC ∂u/∂n + iku = g:
                # We need to add the Robin BC contribution to both LHS and RHS.
                # The term ∂u/∂n appears in the bilinear form.
                # We replace it: ∂u/∂n = g - iku
                #
                # Actually, the correct way for Robin BC in DG:
                # The bilinear form has -∂u/∂n·v̄ + δ·∂u/∂n·∂v̄/∂n on boundary.
                # We ADD the Robin condition ∂u/∂n = g - iku:
                #   -∂u/∂n·v̄ → -(g-iku)v̄ = -gv̄ + ikuv̄
                #   δ·∂u/∂n·∂v̄/∂n → δ(g-iku)∂v̄/∂n = δg∂v̄/∂n - ikδu∂v̄/∂n
                #
                # So we need to REPLACE the terms involving ∂u/∂n on boundary:
                # Remove: -∂u/∂n·v̄ and δ·∂u/∂n·∂v̄/∂n from A
                # Add: iku·v̄ and -ikδu·∂v̄/∂n to A
                # Add: -gv̄ + δg∂v̄/∂n to b
                
                # Remove ∂u/∂n terms (they were added above)
                A[s:s+p, s:s+p] += w * np.outer(ph_c, dph)       # undo -∂u/∂n·v̄
                A[s:s+p, s:s+p] -= self.delta * w * np.outer(dph_c, dph)  # undo δ·∂u/∂n·∂v̄/∂n
                
                # Add Robin-substituted terms to A
                A[s:s+p, s:s+p] += 1j*self.k * w * np.outer(ph_c, ph)  # iku·v̄
                A[s:s+p, s:s+p] -= 1j*self.k*self.delta * w * np.outer(dph_c, ph)  # -ikδu·∂v̄/∂n
                
                # RHS
                gq = g[q]
                b[s:s+p] += -w * gq * ph_c                    # -gv̄
                b[s:s+p] += self.delta * w * gq * dph_c        # δg·∂v̄/∂n
        
        return A, b
    
    def solve(self, u_exact):
        A, b = self.assemble(u_exact)
        return np.linalg.solve(A, b)
    
    def L2_error(self, coeffs, u_exact):
        err2 = 0.0
        for K in range(self.mesh.n_elements):
            pts, wts = element_quadrature(self.mesh, K, 8)
            ph = self._pw(pts)
            s = K * self.p
            uh = ph @ coeffs[s:s+self.p]
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
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq_edge)
            
            ph = self._pw(pts)
            dph = self._dpw_dn(pts, ne)
            
            uhp = ph @ coeffs[Kp*p:(Kp+1)*p]
            uhm = ph @ coeffs[Km*p:(Km+1)*p]
            jump = uhp - uhm
            
            duhp = dph @ coeffs[Kp*p:(Kp+1)*p]
            duhm = dph @ coeffs[Km*p:(Km+1)*p]
            djump = duhp - duhm
            
            err2 += self.alpha * np.sum(wts * np.abs(jump)**2)
            err2 += self.delta * np.sum(wts * np.abs(djump)**2)
        
        for eidx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[eidx]
            K = adj[0][0]
            pts, wts = edge_quadrature(self.mesh, eidx, self.nq_edge)
            ph = self._pw(pts)
            uh = ph @ coeffs[K*p:(K+1)*p]
            ue = u_exact(pts)
            err2 += self.alpha * np.sum(wts * np.abs(uh - ue)**2)
        
        return np.sqrt(max(0, np.real(err2)))
