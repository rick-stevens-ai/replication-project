"""
PWDG solver v2 — Careful reimplementation of the Plane Wave DG method.

Reference: Hiptmair, Moiola, Perugia, SIAM J. Numer. Anal. 49(1), 2011.

Key equations from the paper (Section 2):

Helmholtz: -Delta u - k^2 u = 0 in Omega
Impedance BC: du/dn + i*k*u = g on Gamma (first-order absorbing BC)

Note: The paper uses the sign convention du/dn + ik*u = g (not minus).

PWDG sesquilinear form a_h(u, v):
  For interior edges e between K+ and K-:
    a_h += int_e ( -{du/dn_e} [v_bar] - [u] {dv_bar/dn_e} 
                   + alpha [u][v_bar] + delta [du/dn_e][dv_bar/dn_e] ) ds

  For boundary edges e on element K:
    a_h += int_e ( -du/dn * v_bar + i*k*u*v_bar
                   + alpha*u*v_bar + delta*du/dn*dv_bar/dn ) ds
    ... but with impedance BC incorporated

The bilinear form is sesquilinear: linear in first argument (u), 
conjugate-linear in second (v). So the matrix entry is:
  A[i,j] = a_h(phi_j, phi_i)

with phi_i being basis for test and phi_j for trial.

Plane wave basis: phi_l(x) = exp(i*k*d_l . x)
  d phi_l/dn = i*k*(d_l . n) * phi_l
"""
import numpy as np
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class PWDGSolverV2:
    """Improved PWDG solver with careful bilinear form."""
    
    def __init__(self, mesh, k, p, 
                 flux_type='PWDG',
                 quad_order_edge=16, quad_order_vol=8):
        """
        Parameters:
            mesh: TriMesh
            k: wavenumber (positive real)
            p: number of plane wave directions per element
            flux_type: 'PWDG' (standard from paper) or 'UWVF' (ultra-weak)
            quad_order_edge: quadrature points per edge
            quad_order_vol: volume quadrature order
        """
        self.mesh = mesh
        self.k = float(k)
        self.p = int(p)
        self.quad_order_edge = quad_order_edge
        self.quad_order_vol = quad_order_vol
        
        # Plane wave directions
        angles = np.array([2.0 * np.pi * l / p for l in range(p)])
        self.directions = np.column_stack([np.cos(angles), np.sin(angles)])
        
        self.n_dof = mesh.n_elements * p
        
        # Flux parameters
        if flux_type == 'PWDG':
            # Standard PWDG: alpha = k/2, delta = 1/(2k) on interior
            # On boundary: alpha = k, delta = 0
            self.alpha_int = 0.5 * k
            self.alpha_bdy = k
            self.delta_int = 0.5 / k
            self.delta_bdy = 0.0
        elif flux_type == 'UWVF':
            # Ultra-weak: alpha = k/2, delta = 1/(2k)
            self.alpha_int = 0.5 * k
            self.alpha_bdy = 0.5 * k
            self.delta_int = 0.5 / k
            self.delta_bdy = 0.5 / k
        else:
            raise ValueError(f"Unknown flux type: {flux_type}")
    
    def _plane_wave_values(self, pts, directions):
        """Evaluate exp(i*k*d.x) for all directions at all points.
        
        pts: (nq, 2)
        directions: (p, 2)
        Returns: (nq, p) complex
        """
        phase = self.k * (pts @ directions.T)  # (nq, p)
        return np.exp(1j * phase)
    
    def _plane_wave_normal_deriv(self, pts, directions, normal):
        """Evaluate d/dn exp(i*k*d.x) = i*k*(d.n) * exp(i*k*d.x).
        
        Returns: (nq, p) complex
        """
        vals = self._plane_wave_values(pts, directions)
        dn = directions @ normal  # (p,)
        return 1j * self.k * dn[np.newaxis, :] * vals
    
    def assemble(self, u_exact):
        """Assemble PWDG system.
        
        u_exact: callable(pts, deriv=None) returning complex values.
            u_exact(pts) -> u values at pts
            u_exact(pts, deriv=n) -> du/dn at pts (directional derivative in direction n)
        
        Returns A, b such that A @ c = b.
        """
        n = self.n_dof
        A = np.zeros((n, n), dtype=complex)
        b = np.zeros(n, dtype=complex)
        nq = self.quad_order_edge
        
        # ============================================================
        # Interior edges
        # ============================================================
        for edge_idx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K_plus = adj[0][0]
            K_minus = adj[1][0]
            
            # Fixed normal n_e from K+ toward K-
            n_e = self.mesh.edge_normal(edge_idx, K_plus)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            # Trial basis values
            u_plus = self._plane_wave_values(pts, self.directions)   # (nq, p)
            u_minus = self._plane_wave_values(pts, self.directions)  # (nq, p)
            du_plus = self._plane_wave_normal_deriv(pts, self.directions, n_e)   # (nq, p)
            du_minus = self._plane_wave_normal_deriv(pts, self.directions, n_e)  # (nq, p)
            
            # DOF ranges
            s_p = K_plus * self.p
            s_m = K_minus * self.p
            sl_p = slice(s_p, s_p + self.p)
            sl_m = slice(s_m, s_m + self.p)
            
            # For each quadrature point, accumulate contributions
            # Using vectorized outer product approach
            for q in range(len(pts)):
                w = wts[q]
                
                # Trial function values at quad point
                # On K+: u_j = u_plus[q,j],  du_j/dn = du_plus[q,j]
                # On K-: u_j = u_minus[q,j], du_j/dn = du_minus[q,j]
                
                up = u_plus[q, :]    # trial on K+, (p,)
                um = u_minus[q, :]   # trial on K-, (p,)
                dup = du_plus[q, :]  # d/dn trial on K+ using n_e
                dum = du_minus[q, :] # d/dn trial on K- using n_e
                
                # Test function values (conjugated in sesquilinear form)
                vp_c = np.conj(u_plus[q, :])    # conj(test) on K+
                vm_c = np.conj(u_minus[q, :])   # conj(test) on K-
                dvp_c = np.conj(du_plus[q, :])  # conj(d/dn test) on K+
                dvm_c = np.conj(du_minus[q, :]) # conj(d/dn test) on K-
                
                # Jump [u] = u|K+ - u|K- (note: jump across edge, n_e from + to -)
                # Average {du/dn} = 0.5*(du+/dn_e + du-/dn_e)
                # Note: du-/dn_e means derivative in direction n_e evaluated from K- side
                
                # ---- Term 1: -int_e {du/dn} [v_bar] ds ----
                # {du/dn_e} = 0.5*(du+/dn_e + du-/dn_e) where dn_e uses fixed normal n_e
                # [v_bar] = conj(v+) - conj(v-)
                # For trial on K+: contribution to {du/dn} = 0.5 * du+/dn_e
                # For trial on K-: contribution to {du/dn} = 0.5 * du-/dn_e
                # For test on K+: contribution to [v_bar] = conj(v+) = vp_c
                # For test on K-: contribution to [v_bar] = -conj(v-) = -vm_c
                
                # A[test on K+, trial on K+] += -w * vp_c . (0.5 * dup)
                A[sl_p, sl_p] += -0.5 * w * np.outer(vp_c, dup)
                # A[test on K+, trial on K-] += -w * vp_c . (0.5 * dum)
                A[sl_p, sl_m] += -0.5 * w * np.outer(vp_c, dum)
                # A[test on K-, trial on K+] += -w * (-vm_c) . (0.5 * dup)
                A[sl_m, sl_p] += 0.5 * w * np.outer(vm_c, dup)
                # A[test on K-, trial on K-] += -w * (-vm_c) . (0.5 * dum)
                A[sl_m, sl_m] += 0.5 * w * np.outer(vm_c, dum)
                
                # ---- Term 2: -int_e [u] {dv_bar/dn} ds ----
                # [u] = u+ - u-
                # {dv_bar/dn} = 0.5*(conj(dv+/dn) + conj(dv-/dn))
                
                A[sl_p, sl_p] += -0.5 * w * np.outer(dvp_c, up)
                A[sl_p, sl_m] += 0.5 * w * np.outer(dvp_c, um)
                A[sl_m, sl_p] += -0.5 * w * np.outer(dvm_c, up)
                A[sl_m, sl_m] += 0.5 * w * np.outer(dvm_c, um)
                
                # ---- Term 3: alpha * int_e [u] [v_bar] ds ----
                # [u] = u+ - u-, [v_bar] = vp_c - vm_c
                alpha = self.alpha_int
                A[sl_p, sl_p] += alpha * w * np.outer(vp_c, up)
                A[sl_p, sl_m] += -alpha * w * np.outer(vp_c, um)
                A[sl_m, sl_p] += -alpha * w * np.outer(vm_c, up)
                A[sl_m, sl_m] += alpha * w * np.outer(vm_c, um)
                
                # ---- Term 4: delta * int_e [du/dn] [dv_bar/dn] ds ----
                # [du/dn] = du+/dn - du-/dn
                # [dv_bar/dn] = dvp_c - dvm_c
                delta = self.delta_int
                A[sl_p, sl_p] += delta * w * np.outer(dvp_c, dup)
                A[sl_p, sl_m] += -delta * w * np.outer(dvp_c, dum)
                A[sl_m, sl_p] += -delta * w * np.outer(dvm_c, dup)
                A[sl_m, sl_m] += delta * w * np.outer(dvm_c, dum)
        
        # ============================================================
        # Boundary edges — impedance BC: du/dn + i*k*u = g
        # ============================================================
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K = adj[0][0]
            n_e = self.mesh.edge_normal(edge_idx, K)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            u_vals = self._plane_wave_values(pts, self.directions)
            du_vals = self._plane_wave_normal_deriv(pts, self.directions, n_e)
            
            s = K * self.p
            sl = slice(s, s + self.p)
            
            # Compute boundary data from exact solution
            u_ex = u_exact(pts)
            du_ex_dn = u_exact(pts, deriv=n_e)
            g_vals = du_ex_dn + 1j * self.k * u_ex  # impedance data
            
            for q in range(len(pts)):
                w = wts[q]
                u_q = u_vals[q, :]    # trial, (p,)
                du_q = du_vals[q, :]  # d trial/dn, (p,)
                v_c = np.conj(u_vals[q, :])   # conj(test)
                dv_c = np.conj(du_vals[q, :]) # conj(d test/dn)
                
                # Boundary bilinear form from the PWDG formulation:
                # On Gamma (boundary), the BC du/dn + ik*u = g is enforced weakly.
                # 
                # From the paper's formulation (combining with impedance BC):
                # a_h(u,v)|_Gamma = int_Gamma (du/dn * v_bar + i*k*u*v_bar) ds
                #                 = int_Gamma g * v_bar ds  (when u = u_exact)
                #
                # But in the PWDG framework, we have:
                # a_h(u,v)|_e = -du/dn * v_bar + alpha*u*v_bar + delta*du/dn*dv_bar/dn
                #             + terms from impedance BC substitution
                
                # The complete boundary contribution for PWDG with impedance BC:
                # We substitute du/dn = g - ik*u into the consistency term:
                # -du/dn * v_bar = -(g - ik*u)*v_bar = -g*v_bar + ik*u*v_bar
                #
                # So: a_h(u,v)|_bdy = ik*u*v_bar + alpha*u*v_bar
                #     l_h(v)|_bdy = g*v_bar
                #
                # But this is incomplete. The full boundary term from the DG formulation:
                # a_h|_bdy = -du/dn * v_bar - u * dv_bar/dn + alpha*u*v_bar + delta*du/dn*dv_bar/dn
                # Using impedance BC: du/dn = g - ik*u
                # -> -(g-ik*u)*v_bar - u*dv_bar/dn + alpha*u*v_bar + delta*(g-ik*u)*dv_bar/dn
                # = ik*u*v_bar - u*dv_bar/dn + alpha*u*v_bar + delta*(-ik*u)*dv_bar/dn
                #   + g*(-v_bar + delta*dv_bar/dn)
                
                # Bilinear form contributions (from u):
                # (ik + alpha) * u * v_bar
                A[sl, sl] += (1j * self.k + self.alpha_bdy) * w * np.outer(v_c, u_q)
                # - u * dv_bar/dn
                A[sl, sl] += -w * np.outer(dv_c, u_q)
                # - ik * delta * u * dv_bar/dn
                A[sl, sl] += -1j * self.k * self.delta_bdy * w * np.outer(dv_c, u_q)
                
                # RHS contributions (from g):
                # g * v_bar
                g_q = g_vals[q]
                b[sl] += w * g_q * v_c
                # - delta * g * dv_bar/dn  ... wait, let me reconsider
                # Actually: g*(-v_bar + delta*dv_bar/dn) ... sign issue.
                # Let me use a cleaner derivation.
                
        # Actually, let me redo the boundary terms more carefully.
        # I'll use a clean approach based on the standard PWDG formulation.
        
        # Reset and redo boundary contributions
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K = adj[0][0]
            n_e = self.mesh.edge_normal(edge_idx, K)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            u_vals = self._plane_wave_values(pts, self.directions)
            du_vals = self._plane_wave_normal_deriv(pts, self.directions, n_e)
            
            s = K * self.p
            sl = slice(s, s + self.p)
            
            u_ex = u_exact(pts)
            du_ex_dn = u_exact(pts, deriv=n_e)
            g_vals = du_ex_dn + 1j * self.k * u_ex
            
            for q in range(len(pts)):
                w = wts[q]
                u_q = u_vals[q, :]
                du_q = du_vals[q, :]
                v_c = np.conj(u_vals[q, :])
                dv_c = np.conj(du_vals[q, :])
                g_q = g_vals[q]
                
                # UNDO previous boundary contributions (they were already added above)
                A[sl, sl] -= (1j * self.k + self.alpha_bdy) * w * np.outer(v_c, u_q)
                A[sl, sl] -= -w * np.outer(dv_c, u_q)
                A[sl, sl] -= -1j * self.k * self.delta_bdy * w * np.outer(dv_c, u_q)
                b[sl] -= w * g_q * v_c
        
        # Now redo boundary with the complete, correct formulation
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K = adj[0][0]
            n_e = self.mesh.edge_normal(edge_idx, K)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            u_vals = self._plane_wave_values(pts, self.directions)
            du_vals = self._plane_wave_normal_deriv(pts, self.directions, n_e)
            
            s = K * self.p
            sl = slice(s, s + self.p)
            
            u_ex_vals = u_exact(pts)
            du_ex_dn_vals = u_exact(pts, deriv=n_e)
            g_vals = du_ex_dn_vals + 1j * self.k * u_ex_vals
            
            for q in range(len(pts)):
                w = wts[q]
                u_q = u_vals[q, :]
                du_q = du_vals[q, :]
                v_c = np.conj(u_vals[q, :])
                dv_c = np.conj(du_vals[q, :])
                
                # Impedance BC: du/dn + ik*u = g on boundary
                # 
                # The PWDG boundary bilinear form (from the DG perspective,
                # treating boundary as a "half-edge" with just one element):
                #
                # On boundary, there's no neighbor. The formulation has:
                #   a_h|_bdy(u, v) = int_e [-du/dn * v_bar - u * dv_bar/dn 
                #                          + alpha * u * v_bar + delta * du/dn * dv_bar/dn] ds
                #
                # But we want to incorporate the impedance BC. We do this by
                # replacing du/dn with (g - ik*u) in the consistency term:
                #
                # Approach: Direct Nitsche-type imposition of impedance BC.
                # Simply use:
                #   a_h|_bdy(u, v) = int_e (ik*u + alpha*u) * v_bar ds
                #                  - int_e u * dv_bar/dn ds
                #                  + int_e delta * du/dn * dv_bar/dn ds
                #                  - int_e ik * delta * u * dv_bar/dn ds
                #
                #   l_h(v)|_bdy = int_e g * (v_bar - delta * dv_bar/dn) ds
                
                g_q = g_vals[q]
                
                # LHS: (ik + alpha)*u*v_bar
                A[sl, sl] += (1j * self.k + self.alpha_bdy) * w * np.outer(v_c, u_q)
                
                # LHS: -u * dv_bar/dn
                A[sl, sl] += -w * np.outer(dv_c, u_q)
                
                # LHS: delta * du/dn * dv_bar/dn
                A[sl, sl] += self.delta_bdy * w * np.outer(dv_c, du_q)
                
                # LHS: -ik*delta * u * dv_bar/dn (from substituting du/dn = g - ik*u in delta term)
                A[sl, sl] += -1j * self.k * self.delta_bdy * w * np.outer(dv_c, u_q)
                
                # RHS: g * v_bar
                b[sl] += w * g_q * v_c
                
                # RHS: -delta * g * dv_bar/dn (from consistency term)
                b[sl] += -self.delta_bdy * w * g_q * dv_c
        
        return A, b
    
    def solve(self, u_exact):
        """Solve the PWDG system."""
        A, b = self.assemble(u_exact)
        
        # Condition number check
        # cond = np.linalg.cond(A)
        # print(f"  Condition number: {cond:.2e}")
        
        coeffs = np.linalg.solve(A, b)
        return coeffs
    
    def compute_L2_error(self, coeffs, u_exact):
        """Compute element-wise L2 error."""
        err_sq = 0.0
        for K in range(self.mesh.n_elements):
            pts, wts = element_quadrature(self.mesh, K, self.quad_order_vol)
            s = K * self.p
            phi = self._plane_wave_values(pts, self.directions)
            u_h = phi @ coeffs[s:s+self.p]
            u_ex = u_exact(pts)
            diff = u_h - u_ex
            err_sq += np.sum(wts * np.abs(diff)**2)
        return np.sqrt(np.real(err_sq))
    
    def compute_DG_error(self, coeffs, u_exact):
        """Compute DG skeleton-based error norm."""
        err_sq = 0.0
        nq = self.quad_order_edge
        
        # Interior edges: penalty on jump
        for edge_idx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K_p, K_m = adj[0][0], adj[1][0]
            n_e = self.mesh.edge_normal(edge_idx, K_p)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            phi_p = self._plane_wave_values(pts, self.directions)
            phi_m = self._plane_wave_values(pts, self.directions)
            
            u_h_p = phi_p @ coeffs[K_p*self.p:(K_p+1)*self.p]
            u_h_m = phi_m @ coeffs[K_m*self.p:(K_m+1)*self.p]
            
            # u_exact is continuous -> jump of error = jump of u_h
            jump = u_h_p - u_h_m
            err_sq += self.alpha_int * np.sum(wts * np.abs(jump)**2)
            
            # Normal derivative jump
            dphi_p = self._plane_wave_normal_deriv(pts, self.directions, n_e)
            dphi_m = self._plane_wave_normal_deriv(pts, self.directions, n_e)
            du_h_p = dphi_p @ coeffs[K_p*self.p:(K_p+1)*self.p]
            du_h_m = dphi_m @ coeffs[K_m*self.p:(K_m+1)*self.p]
            jump_dn = du_h_p - du_h_m
            err_sq += self.delta_int * np.sum(wts * np.abs(jump_dn)**2)
        
        # Boundary edges
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            K = adj[0][0]
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq)
            
            phi = self._plane_wave_values(pts, self.directions)
            u_h = phi @ coeffs[K*self.p:(K+1)*self.p]
            u_ex = u_exact(pts)
            diff = u_h - u_ex
            err_sq += self.alpha_bdy * np.sum(wts * np.abs(diff)**2)
        
        return np.sqrt(np.real(err_sq))
