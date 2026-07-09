"""
Build the EXACT mesh used in Hiptmair-Moiola-Perugia 2011 §4 (Fig 4.1):
- Domain Ω = [0,1] × [-0.5, 0.5]
- 8 triangles
- h = 1/sqrt(2)
- Singularity vertex (the origin (0,0)) lies on the boundary as a mesh node.

We build it as a 2x1 grid of unit squares (each split into 2 triangles using
the long diagonal that meets at the origin) for a total of 4*2 = 8 triangles.
Actually the paper's mesh on [0,1]x[-0.5,0.5] needs origin as a node and h=1/sqrt(2).

We construct: nodes at (0,-0.5), (1,-0.5), (0,0.5), (1,0.5), (0.5,0), and corners.
The simplest 8-triangle mesh that matches the figure: split each rectangle
[0,0.5]x[-0.5,0.5], [0.5,1]x[-0.5,0.5] into 4 triangles via center points.

Actually the figure shows a 2x2 arrangement of squares cut diagonally:
nodes at corners and midpoints, giving 8 triangles total with the origin as a node.

We use the construction:
  Cells = [0,0.5]x[-0.5,0], [0.5,1]x[-0.5,0], [0,0.5]x[0,0.5], [0.5,1]x[0,0.5]
  Each cell split into 2 triangles by the appropriate diagonal so that:
   - longest edge = sqrt(0.5^2 + 0.5^2) = 1/sqrt(2)  -> matches h = 1/sqrt(2) ✓
   - (0,0) is a node.
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mesh import _build_mesh, TriMesh


def make_paper_mesh():
    """8-triangle mesh on Ω = [0,1]×[-1/2,1/2] with (0,0) as a node.

    Layout (nodes):
        (0,1/2) — (1/2,1/2) — (1,1/2)
           |        |          |
        (0,0)  — (1/2,0)  — (1,0)
           |        |          |
        (0,-1/2)— (1/2,-1/2)—(1,-1/2)

    Each 1/2×1/2 cell is split into 2 triangles by the "/" diagonal so that
    the longest edge is sqrt(2)/2 = 1/sqrt(2).
    """
    nodes = np.array([
        [0.0,  -0.5],   # 0
        [0.5,  -0.5],   # 1
        [1.0,  -0.5],   # 2
        [0.0,   0.0],   # 3   <-- origin (singularity vertex for J_xi)
        [0.5,   0.0],   # 4
        [1.0,   0.0],   # 5
        [0.0,   0.5],   # 6
        [0.5,   0.5],   # 7
        [1.0,   0.5],   # 8
    ])

    # Each 0.5x0.5 cell -> 2 triangles via "/" diagonal (lower-right + upper-left)
    # Cell with lower-left node (i,j) of the 3x3 grid:
    def cell_tris(LL, LR, UL, UR):
        # "/" diagonal: LL-UR splits cell into (LL,LR,UR) and (LL,UR,UL)
        return [[LL, LR, UR], [LL, UR, UL]]

    elements = []
    # bottom row of cells
    elements += cell_tris(0, 1, 3, 4)
    elements += cell_tris(1, 2, 4, 5)
    # top row of cells
    elements += cell_tris(3, 4, 6, 7)
    elements += cell_tris(4, 5, 7, 8)
    elements = np.array(elements)

    return _build_mesh(nodes, elements)


if __name__ == "__main__":
    m = make_paper_mesh()
    print(f"Nodes: {len(m.nodes)}")
    print(f"Elements: {m.n_elements}")
    print(f"Edges: {m.n_edges}  (interior={len(m.interior_edges)}, boundary={len(m.boundary_edges)})")
    diams = [m.element_diameter(i) for i in range(m.n_elements)]
    areas = [m.element_area(i) for i in range(m.n_elements)]
    print(f"Element diameters: min={min(diams):.4f} max={max(diams):.4f} (target 1/sqrt(2)={1/np.sqrt(2):.4f})")
    print(f"Total area: {sum(areas):.4f}  (target 1.0)")
    # Check origin is a node
    has_origin = any(np.allclose(n, [0,0]) for n in m.nodes)
    print(f"Origin (0,0) is a node: {has_origin}")
