"""
Triangular mesh generation for PWDG Helmholtz solver.
Supports: unit square, L-shaped domain.
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class TriMesh:
    """Simple triangular mesh."""
    nodes: np.ndarray        # (n_nodes, 2) node coordinates
    elements: np.ndarray     # (n_elements, 3) node indices per triangle
    edges: np.ndarray        # (n_edges, 2) node indices per edge
    edge_to_elem: list       # edge -> list of (elem_idx, local_edge_idx)
    boundary_edges: np.ndarray  # indices of boundary edges
    interior_edges: np.ndarray  # indices of interior edges
    
    @property
    def n_elements(self):
        return len(self.elements)
    
    @property
    def n_edges(self):
        return len(self.edges)
    
    def element_area(self, elem_idx):
        """Compute area of triangle."""
        v = self.nodes[self.elements[elem_idx]]
        return 0.5 * abs((v[1,0]-v[0,0])*(v[2,1]-v[0,1]) - (v[2,0]-v[0,0])*(v[1,1]-v[0,1]))
    
    def element_diameter(self, elem_idx):
        """Compute diameter (longest edge) of triangle."""
        v = self.nodes[self.elements[elem_idx]]
        d01 = np.linalg.norm(v[1] - v[0])
        d02 = np.linalg.norm(v[2] - v[0])
        d12 = np.linalg.norm(v[2] - v[1])
        return max(d01, d02, d12)
    
    def edge_length(self, edge_idx):
        """Compute length of edge."""
        v = self.nodes[self.edges[edge_idx]]
        return np.linalg.norm(v[1] - v[0])
    
    def edge_normal(self, edge_idx, elem_idx):
        """Compute outward unit normal of edge w.r.t. element."""
        e = self.edges[edge_idx]
        v0, v1 = self.nodes[e[0]], self.nodes[e[1]]
        tangent = v1 - v0
        # Normal perpendicular to tangent
        normal = np.array([tangent[1], -tangent[0]])
        normal = normal / np.linalg.norm(normal)
        # Ensure outward w.r.t. element
        centroid = np.mean(self.nodes[self.elements[elem_idx]], axis=0)
        midpoint = 0.5 * (v0 + v1)
        if np.dot(normal, midpoint - centroid) < 0:
            normal = -normal
        return normal
    
    def edge_midpoint(self, edge_idx):
        """Midpoint of edge."""
        v = self.nodes[self.edges[edge_idx]]
        return 0.5 * (v[0] + v[1])


def make_unit_square_mesh(n_per_side):
    """Create structured triangular mesh on [0,1]^2.
    
    Each square cell is split into 2 triangles.
    n_per_side: number of intervals per side.
    """
    h = 1.0 / n_per_side
    # Nodes
    nodes = []
    for j in range(n_per_side + 1):
        for i in range(n_per_side + 1):
            nodes.append([i * h, j * h])
    nodes = np.array(nodes)
    
    def node_idx(i, j):
        return j * (n_per_side + 1) + i
    
    # Triangles: each square -> 2 triangles
    elements = []
    for j in range(n_per_side):
        for i in range(n_per_side):
            n00 = node_idx(i, j)
            n10 = node_idx(i+1, j)
            n01 = node_idx(i, j+1)
            n11 = node_idx(i+1, j+1)
            # Lower-left triangle
            elements.append([n00, n10, n01])
            # Upper-right triangle
            elements.append([n10, n11, n01])
    elements = np.array(elements)
    
    return _build_mesh(nodes, elements)


def make_l_shaped_mesh(n_per_side):
    """Create structured triangular mesh on L-shaped domain.
    
    L = [-1,1]^2 \ [0,1]x[-1,0] (remove lower-right quadrant).
    """
    h = 2.0 / n_per_side
    half = n_per_side // 2
    
    nodes = []
    node_map = {}
    idx = 0
    for j in range(n_per_side + 1):
        for i in range(n_per_side + 1):
            x = -1.0 + i * h
            y = -1.0 + j * h
            # Skip nodes in removed quadrant interior
            # Keep nodes on boundary of removed quadrant
            if x > 0 + 1e-12 and y < 0 - 1e-12:
                continue
            node_map[(i, j)] = idx
            nodes.append([x, y])
            idx += 1
    nodes = np.array(nodes)
    
    elements = []
    for j in range(n_per_side):
        for i in range(n_per_side):
            # Check if cell is in removed quadrant
            x_mid = -1.0 + (i + 0.5) * h
            y_mid = -1.0 + (j + 0.5) * h
            if x_mid > 0 and y_mid < 0:
                continue
            
            if (i,j) in node_map and (i+1,j) in node_map and \
               (i,j+1) in node_map and (i+1,j+1) in node_map:
                n00 = node_map[(i, j)]
                n10 = node_map[(i+1, j)]
                n01 = node_map[(i, j+1)]
                n11 = node_map[(i+1, j+1)]
                elements.append([n00, n10, n01])
                elements.append([n10, n11, n01])
    elements = np.array(elements)
    
    return _build_mesh(nodes, elements)


def _build_mesh(nodes, elements):
    """Build edge connectivity from nodes and elements."""
    edge_dict = {}
    edge_to_elem = []
    
    for elem_idx, tri in enumerate(elements):
        for local_edge in range(3):
            n0 = tri[local_edge]
            n1 = tri[(local_edge + 1) % 3]
            key = (min(n0, n1), max(n0, n1))
            if key not in edge_dict:
                edge_dict[key] = len(edge_to_elem)
                edge_to_elem.append([])
            edge_to_elem[edge_dict[key]].append((elem_idx, local_edge))
    
    edges = np.array(list(edge_dict.keys()))
    # Reorder edge_to_elem to match edges array
    edge_to_elem_ordered = []
    for key in edge_dict:
        edge_to_elem_ordered.append(edge_to_elem[edge_dict[key]])
    
    boundary_edges = []
    interior_edges = []
    for i, adj in enumerate(edge_to_elem_ordered):
        if len(adj) == 1:
            boundary_edges.append(i)
        else:
            interior_edges.append(i)
    
    return TriMesh(
        nodes=nodes,
        elements=elements,
        edges=edges,
        edge_to_elem=edge_to_elem_ordered,
        boundary_edges=np.array(boundary_edges),
        interior_edges=np.array(interior_edges)
    )
