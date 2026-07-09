"""
Quadrature rules for triangles and line segments.
"""
import numpy as np


def gauss_line(n_pts):
    """Gauss-Legendre quadrature on [0, 1].
    
    Returns (points, weights) arrays.
    """
    pts_ref, wts_ref = np.polynomial.legendre.leggauss(n_pts)
    # Map from [-1,1] to [0,1]
    pts = 0.5 * (pts_ref + 1.0)
    wts = 0.5 * wts_ref
    return pts, wts


def gauss_triangle(order):
    """Gauss quadrature on reference triangle with vertices (0,0), (1,0), (0,1).
    
    Returns (points, weights) where points is (n_pts, 2).
    Uses Duffy transform from tensor product Gauss rule.
    """
    if order <= 1:
        # 1-point rule
        return np.array([[1/3, 1/3]]), np.array([0.5])
    elif order <= 2:
        # 3-point rule
        pts = np.array([[1/6, 1/6], [2/3, 1/6], [1/6, 2/3]])
        wts = np.array([1/6, 1/6, 1/6])
        return pts, wts
    elif order <= 3:
        # 4-point rule (Hammer-Stroud)
        pts = np.array([
            [1/3, 1/3],
            [1/5, 1/5],
            [3/5, 1/5],
            [1/5, 3/5]
        ])
        wts = np.array([-27/96, 25/96, 25/96, 25/96])
        return pts, wts
    else:
        # Duffy transform: tensor product Gauss on [0,1]^2 -> triangle
        n = max(order, 4)
        pts_1d, wts_1d = gauss_line(n)
        pts_2d = []
        wts_2d = []
        for i in range(n):
            for j in range(n):
                xi = pts_1d[i]
                eta = pts_1d[j] * (1 - xi)
                w = wts_1d[i] * wts_1d[j] * (1 - xi)
                pts_2d.append([xi, eta])
                wts_2d.append(w)
        return np.array(pts_2d), np.array(wts_2d)


def edge_quadrature(mesh, edge_idx, n_pts):
    """Quadrature points and weights on a mesh edge.
    
    Returns (phys_pts, weights) where phys_pts is (n_pts, 2),
    weights include the edge length Jacobian.
    """
    v0 = mesh.nodes[mesh.edges[edge_idx][0]]
    v1 = mesh.nodes[mesh.edges[edge_idx][1]]
    length = np.linalg.norm(v1 - v0)
    
    t_pts, t_wts = gauss_line(n_pts)
    
    phys_pts = np.outer(1.0 - t_pts, v0) + np.outer(t_pts, v1)
    weights = t_wts * length
    
    return phys_pts, weights


def element_quadrature(mesh, elem_idx, order):
    """Quadrature points and weights on a mesh triangle.
    
    Returns (phys_pts, weights) where phys_pts is (n_pts, 2),
    weights include the area Jacobian.
    """
    v = mesh.nodes[mesh.elements[elem_idx]]
    # Jacobian: 2 * area
    jac = abs((v[1,0]-v[0,0])*(v[2,1]-v[0,1]) - (v[2,0]-v[0,0])*(v[1,1]-v[0,1]))
    
    ref_pts, ref_wts = gauss_triangle(order)
    
    # Map from reference to physical triangle
    phys_pts = (np.outer(1.0 - ref_pts[:,0] - ref_pts[:,1], v[0]) +
                np.outer(ref_pts[:,0], v[1]) +
                np.outer(ref_pts[:,1], v[2]))
    weights = ref_wts * jac
    
    return phys_pts, weights
