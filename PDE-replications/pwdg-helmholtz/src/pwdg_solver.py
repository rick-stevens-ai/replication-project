"""
Plane Wave Discontinuous Galerkin (PWDG) solver for the 2D Helmholtz equation.

Reference: Hiptmair, Moiola, Perugia, "Plane Wave Discontinuous Galerkin 
Methods for the 2D Helmholtz Equation: Analysis of the p-Version",
SIAM J. Numer. Anal., 49(1), 264-284, 2011.

The Helmholtz equation:  -Delta u - k^2 u = 0  in Omega
with impedance (Robin) BC:  du/dn - i*k*u = g  on Gamma

PWDG uses plane wave basis functions: phi_l(x) = exp(i*k*d_l . x)
where d_l are uniformly distributed directions on the unit circle.
"""
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from mesh import TriMesh
from quadrature import edge_quadrature, element_quadrature


class PWDGSolver:
    """PWDG solver for 2D Helmholtz equation."""
    
    def __init__(self, mesh, k, p, 
                 alpha=None, beta=None, delta=None,
                 quad_order_edge=10, quad_order_vol=6):
        """
        Parameters:
            mesh: TriMesh object
            k: wavenumber
            p: number of plane wave directions per element
            alpha, beta, delta: flux parameters (None = use defaults from paper)
            quad_order_edge: number of quadrature points per edge
            quad_order_vol: quadrature order for volume integrals
        """
        self.mesh = mesh
        self.k = k
        self.p = p
        self.quad_order_edge = quad_order_edge
        self.quad_order_vol = quad_order_vol
        
        # Plane wave directions: uniformly distributed on unit circle
        angles = np.array([2 * np.pi * l / p for l in range(p)])
        self.directions = np.column_stack([np.cos(angles), np.sin(angles)])
        
        # Total DOFs
        self.n_dof = mesh.n_elements * p
        
        # Flux parameters (following the paper's notation)
        # Default: standard PWDG flux parameters
        if alpha is None:
            # Stabilization parameter for [u] terms
            # alpha = k/2 on interior, k on boundary (impedance)
            self.alpha_int = 0.5 * k
            self.alpha_bdy = k
        else:
            self.alpha_int = alpha
            self.alpha_bdy = alpha
            
        if beta is None:
            # Parameter for {grad u . n} terms
            self.beta_int = 0.5
            self.beta_bdy = 1.0
        else:
            self.beta_int = beta
            self.beta_bdy = beta
            
        if delta is None:
            # Parameter for [grad u . n] terms  
            # delta = 1/(2k) on interior, 0 on boundary
            self.delta_int = 0.5 / k
            self.delta_bdy = 0.0
        else:
            self.delta_int = delta
            self.delta_bdy = delta
    
    def _dof_range(self, elem_idx):
        """DOF indices for element."""
        start = elem_idx * self.p
        return start, start + self.p
    
    def _eval_basis(self, elem_idx, pts):
        """Evaluate plane wave basis functions at points.
        
        Returns (n_pts, p) complex array.
        """
        # phi_l(x) = exp(i * k * d_l . x)
        # pts: (n_pts, 2), directions: (p, 2)
        phase = self.k * (pts @ self.directions.T)  # (n_pts, p)
        return np.exp(1j * phase)
    
    def _eval_basis_grad(self, elem_idx, pts):
        """Evaluate gradient of plane wave basis functions.
        
        Returns (n_pts, p, 2) complex array.
        grad phi_l = i*k*d_l * exp(i*k*d_l.x)
        """
        vals = self._eval_basis(elem_idx, pts)  # (n_pts, p)
        # grad_x phi_l = i*k*d_l[0] * phi_l, grad_y phi_l = i*k*d_l[1] * phi_l
        grad = np.zeros((len(pts), self.p, 2), dtype=complex)
        for d in range(2):
            grad[:, :, d] = 1j * self.k * self.directions[:, d][np.newaxis, :] * vals
        return grad
    
    def _eval_basis_normal_deriv(self, elem_idx, pts, normal):
        """Evaluate normal derivative of basis functions.
        
        Returns (n_pts, p) complex array.
        d phi_l/dn = i*k*(d_l.n) * phi_l
        """
        vals = self._eval_basis(elem_idx, pts)
        dn = self.directions @ normal  # (p,)
        return 1j * self.k * dn[np.newaxis, :] * vals
    
    def assemble(self, u_exact=None, g_func=None):
        """Assemble the PWDG linear system.
        
        The PWDG variational formulation (from Eq. (2.7) in the paper):
        
        For interior edges e shared by elements K+ and K-:
          a_h(u,v) contributions:
            - {grad_h u . n_e} [v]  (consistency)
            - beta * {grad_h v . n_e} [u]  (symmetry, beta=+1/2 for PWDG)  
            - alpha * [u] [v]  (penalty/stabilization)
            - delta * [grad_h u . n_e] [grad_h v . n_e]  (if delta > 0)
        
        For boundary edges:
            - impedance BC terms
        
        Parameters:
            u_exact: exact solution function (for manufacturing BC data)
            g_func: impedance BC data function (overrides u_exact)
        """
        n = self.n_dof
        A = np.zeros((n, n), dtype=complex)
        b = np.zeros(n, dtype=complex)
        
        nq_edge = self.quad_order_edge
        
        # Interior edge contributions
        for edge_idx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            elem_plus = adj[0][0]
            elem_minus = adj[1][0]
            
            normal = self.mesh.edge_normal(edge_idx, elem_plus)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq_edge)
            
            # Evaluate basis functions and normal derivatives
            phi_plus = self._eval_basis(elem_plus, pts)      # (nq, p)
            phi_minus = self._eval_basis(elem_minus, pts)     # (nq, p)
            dphi_plus = self._eval_basis_normal_deriv(elem_plus, pts, normal)   # (nq, p)
            dphi_minus = self._eval_basis_normal_deriv(elem_minus, pts, -normal) # (nq, p) 
            # Note: normal derivative from K- uses -normal (outward from K-)
            # but dphi_minus is already d/d(n_e) from K- side
            # Actually: the normal n_e is fixed, and from K- perspective, outward normal is -n_e
            # So {grad u . n_e} = 0.5*(grad u+.n_e + grad u-.n_e)
            # where grad u-.n_e is the normal deriv using n_e direction
            
            dphi_minus_ne = self._eval_basis_normal_deriv(elem_minus, pts, normal)
            
            i_plus_start, i_plus_end = self._dof_range(elem_plus)
            i_minus_start, i_minus_end = self._dof_range(elem_minus)
            
            # Jump [v] = v+ - v- , Average {grad u.n} = 0.5*(grad u+.n + grad u-.n)
            # where n is the fixed normal from K+ to K-
            
            for q in range(len(pts)):
                w = wts[q]
                
                # Basis values at this quad point
                pp = phi_plus[q, :]    # (p,) from K+
                pm = phi_minus[q, :]   # (p,) from K-
                dpp = dphi_plus[q, :]  # (p,) d/dn from K+ (using n_e)
                dpm = dphi_minus_ne[q, :]  # (p,) d/dn from K- (using n_e)
                
                # Jump [u] = u+ - u-
                # Average {du/dn} = 0.5*(du+/dn + du-/dn) using same normal n_e
                
                # 1. Consistency: - {dv/dn} [u]
                # avg_dv = 0.5 * [dv+, dv-] applied to [u+ - u-]
                # -> -0.5 * (conj(dv+) * (u+ - u-) + conj(dv-) * (u+ - u-)) * w
                
                # A[v+, u+] += -0.5 * conj(dv+) * u+ * w = -0.5 * dv+^H u+ w
                # etc.
                
                # Term 1: -int {dv/dn} [u] ds  (consistency)
                avg_dv_plus = 0.5 * np.conj(dpp)   # contribution from v+
                avg_dv_minus = 0.5 * np.conj(dpm)  # contribution from v-
                jump_u_plus = pp                     # u+ part of [u]
                jump_u_minus = -pm                   # u- part of [u]
                
                # v+ contributions (test from K+)
                A[i_plus_start:i_plus_end, i_plus_start:i_plus_end] += \
                    -w * np.outer(avg_dv_plus, jump_u_plus)
                A[i_plus_start:i_plus_end, i_minus_start:i_minus_end] += \
                    -w * np.outer(avg_dv_plus, jump_u_minus)
                
                # v- contributions (test from K-)
                A[i_minus_start:i_minus_end, i_plus_start:i_plus_end] += \
                    -w * np.outer(avg_dv_minus, jump_u_plus)
                A[i_minus_start:i_minus_end, i_minus_start:i_minus_end] += \
                    -w * np.outer(avg_dv_minus, jump_u_minus)
                
                # Term 2: -beta * int {du/dn} [v] ds  (adjoint consistency)
                # [v] = v+ - v-
                avg_du_plus = 0.5 * dpp
                avg_du_minus = 0.5 * dpm
                jump_v_plus = np.conj(pp)
                jump_v_minus = -np.conj(pm)
                
                A[i_plus_start:i_plus_end, i_plus_start:i_plus_end] += \
                    -self.beta_int * w * np.outer(jump_v_plus, avg_du_plus)
                A[i_plus_start:i_plus_end, i_minus_start:i_minus_end] += \
                    -self.beta_int * w * np.outer(jump_v_plus, avg_du_minus)
                A[i_minus_start:i_minus_end, i_plus_start:i_plus_end] += \
                    -self.beta_int * w * np.outer(jump_v_minus, avg_du_plus)
                A[i_minus_start:i_minus_end, i_minus_start:i_minus_end] += \
                    -self.beta_int * w * np.outer(jump_v_minus, avg_du_minus)
                
                # Term 3: alpha * int [u] [v] ds  (penalty)
                A[i_plus_start:i_plus_end, i_plus_start:i_plus_end] += \
                    self.alpha_int * w * np.outer(jump_v_plus, jump_u_plus)
                A[i_plus_start:i_plus_end, i_minus_start:i_minus_end] += \
                    self.alpha_int * w * np.outer(jump_v_plus, jump_u_minus)
                A[i_minus_start:i_minus_end, i_plus_start:i_plus_end] += \
                    self.alpha_int * w * np.outer(jump_v_minus, jump_u_plus)
                A[i_minus_start:i_minus_end, i_minus_start:i_minus_end] += \
                    self.alpha_int * w * np.outer(jump_v_minus, jump_u_minus)
                
                # Term 4: delta * int [du/dn] [dv/dn] ds
                # [du/dn] = du+/dn - du-/dn (using same normal)
                jump_du_plus = dpp
                jump_du_minus = -dpm
                jump_dv_plus = np.conj(dpp)
                jump_dv_minus = -np.conj(dpm)
                
                A[i_plus_start:i_plus_end, i_plus_start:i_plus_end] += \
                    self.delta_int * w * np.outer(jump_dv_plus, jump_du_plus)
                A[i_plus_start:i_plus_end, i_minus_start:i_minus_end] += \
                    self.delta_int * w * np.outer(jump_dv_plus, jump_du_minus)
                A[i_minus_start:i_minus_end, i_plus_start:i_plus_end] += \
                    self.delta_int * w * np.outer(jump_dv_minus, jump_du_plus)
                A[i_minus_start:i_minus_end, i_minus_start:i_minus_end] += \
                    self.delta_int * w * np.outer(jump_dv_minus, jump_du_minus)
        
        # Boundary edge contributions (impedance BC)
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            elem = adj[0][0]
            normal = self.mesh.edge_normal(edge_idx, elem)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq_edge)
            
            phi = self._eval_basis(elem, pts)
            dphi = self._eval_basis_normal_deriv(elem, pts, normal)
            
            i_start, i_end = self._dof_range(elem)
            
            for q in range(len(pts)):
                w = wts[q]
                p_val = phi[q, :]
                dp_val = dphi[q, :]
                
                # Impedance BC: du/dn - i*k*u = g on boundary
                # From the PWDG formulation, boundary terms:
                
                # Term: -dv/dn * u  (consistency on boundary)
                A[i_start:i_end, i_start:i_end] += \
                    -w * np.outer(np.conj(dp_val), p_val)
                
                # Term: -beta * du/dn * v  (adjoint consistency on boundary)
                A[i_start:i_end, i_start:i_end] += \
                    -self.beta_bdy * w * np.outer(np.conj(p_val), dp_val)
                
                # Term: alpha * u * v  (penalty on boundary)
                A[i_start:i_end, i_start:i_end] += \
                    self.alpha_bdy * w * np.outer(np.conj(p_val), p_val)
                
                # Impedance BC contribution to bilinear form:
                # i*k*u*v (from impedance BC: du/dn = i*k*u + g)
                A[i_start:i_end, i_start:i_end] += \
                    1j * self.k * self.beta_bdy * w * np.outer(np.conj(p_val), p_val)
                
                # RHS from boundary data
                if g_func is not None:
                    g_val = g_func(pts[q:q+1, :])[0]
                elif u_exact is not None:
                    # Compute g from exact solution: g = du_ex/dn - i*k*u_ex
                    u_ex = u_exact(pts[q:q+1, :])[0]
                    du_ex_dn = u_exact(pts[q:q+1, :], deriv=normal)[0]
                    g_val = du_ex_dn - 1j * self.k * u_ex
                else:
                    g_val = 0.0
                
                # RHS: (alpha - i*k*beta) * g * v + beta * g * dv/dn
                # Simplified: contributions from boundary data
                b[i_start:i_end] += w * (self.alpha_bdy + 1j * self.k * self.beta_bdy) * \
                    g_val * np.conj(p_val)
                b[i_start:i_end] += w * self.beta_bdy * g_val * np.conj(dp_val)
        
        return A, b
    
    def solve(self, u_exact=None, g_func=None):
        """Assemble and solve the PWDG system.
        
        Returns coefficient vector.
        """
        A, b = self.assemble(u_exact=u_exact, g_func=g_func)
        coeffs = np.linalg.solve(A, b)
        return coeffs
    
    def evaluate(self, coeffs, pts):
        """Evaluate PWDG solution at arbitrary points.
        
        For each point, find the containing element and evaluate.
        Returns complex array of solution values.
        """
        result = np.zeros(len(pts), dtype=complex)
        
        for i, pt in enumerate(pts):
            elem = self._find_element(pt)
            if elem is not None:
                start, end = self._dof_range(elem)
                phi = self._eval_basis(elem, pt.reshape(1, 2))  # (1, p)
                result[i] = phi[0, :] @ coeffs[start:end]
        
        return result
    
    def _find_element(self, pt):
        """Find element containing point (brute force)."""
        for elem_idx in range(self.mesh.n_elements):
            if self._point_in_triangle(pt, elem_idx):
                return elem_idx
        return None
    
    def _point_in_triangle(self, pt, elem_idx):
        """Check if point is in triangle using barycentric coordinates."""
        v = self.mesh.nodes[self.mesh.elements[elem_idx]]
        v0 = v[2] - v[0]
        v1 = v[1] - v[0]
        v2 = pt - v[0]
        
        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)
        
        inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01 + 1e-30)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v_coord = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        return (u >= -1e-10) and (v_coord >= -1e-10) and (u + v_coord <= 1 + 1e-10)
    
    def compute_error(self, coeffs, u_exact, norm_type='L2'):
        """Compute error in specified norm.
        
        Parameters:
            coeffs: PWDG coefficient vector
            u_exact: callable(pts) -> complex values, exact solution
            norm_type: 'L2' or 'DG'
        
        Returns:
            error value
        """
        if norm_type == 'L2':
            return self._compute_L2_error(coeffs, u_exact)
        elif norm_type == 'DG':
            return self._compute_DG_error(coeffs, u_exact)
        else:
            raise ValueError(f"Unknown norm type: {norm_type}")
    
    def _compute_L2_error(self, coeffs, u_exact):
        """Compute L2 error over all elements."""
        error_sq = 0.0
        
        for elem_idx in range(self.mesh.n_elements):
            pts, wts = element_quadrature(self.mesh, elem_idx, self.quad_order_vol)
            
            # PWDG solution
            start, end = self._dof_range(elem_idx)
            phi = self._eval_basis(elem_idx, pts)
            u_h = phi @ coeffs[start:end]
            
            # Exact solution
            u_ex = u_exact(pts)
            
            # Error
            diff = u_h - u_ex
            error_sq += np.sum(wts * np.abs(diff)**2)
        
        return np.sqrt(np.real(error_sq))
    
    def _compute_DG_error(self, coeffs, u_exact):
        """Compute DG (skeleton-based) error norm.
        
        DG norm includes:
        - alpha * ||[u-u_h]||^2_{L2(edges)}
        - delta * ||[d(u-u_h)/dn]||^2_{L2(edges)}
        """
        error_sq = 0.0
        nq_edge = self.quad_order_edge
        
        # Interior edges
        for edge_idx in self.mesh.interior_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            elem_plus = adj[0][0]
            elem_minus = adj[1][0]
            normal = self.mesh.edge_normal(edge_idx, elem_plus)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq_edge)
            
            # PWDG solution on both sides
            s_p, e_p = self._dof_range(elem_plus)
            s_m, e_m = self._dof_range(elem_minus)
            
            phi_p = self._eval_basis(elem_plus, pts)
            phi_m = self._eval_basis(elem_minus, pts)
            
            u_h_plus = phi_p @ coeffs[s_p:e_p]
            u_h_minus = phi_m @ coeffs[s_m:e_m]
            
            # Exact solution (continuous, so no jump)
            u_ex = u_exact(pts)
            
            # Jump of error: [u_h - u_ex] = (u_h+ - u_ex) - (u_h- - u_ex) = u_h+ - u_h-
            jump_err = u_h_plus - u_h_minus
            
            # alpha term
            error_sq += self.alpha_int * np.sum(wts * np.abs(jump_err)**2)
            
            # Normal derivative jumps
            dphi_p = self._eval_basis_normal_deriv(elem_plus, pts, normal)
            dphi_m = self._eval_basis_normal_deriv(elem_minus, pts, normal)
            
            du_h_plus = dphi_p @ coeffs[s_p:e_p]
            du_h_minus = dphi_m @ coeffs[s_m:e_m]
            
            # For exact solution, du_ex/dn is continuous across interior edges
            # So jump of normal derivative of error = du_h+/dn - du_h-/dn
            jump_dn_err = du_h_plus - du_h_minus
            
            error_sq += self.delta_int * np.sum(wts * np.abs(jump_dn_err)**2)
        
        # Boundary edges
        for edge_idx in self.mesh.boundary_edges:
            adj = self.mesh.edge_to_elem[edge_idx]
            elem = adj[0][0]
            normal = self.mesh.edge_normal(edge_idx, elem)
            pts, wts = edge_quadrature(self.mesh, edge_idx, nq_edge)
            
            s, e = self._dof_range(elem)
            phi = self._eval_basis(elem, pts)
            u_h = phi @ coeffs[s:e]
            u_ex = u_exact(pts)
            
            diff = u_h - u_ex
            error_sq += self.alpha_bdy * np.sum(wts * np.abs(diff)**2)
        
        return np.sqrt(np.real(error_sq))
