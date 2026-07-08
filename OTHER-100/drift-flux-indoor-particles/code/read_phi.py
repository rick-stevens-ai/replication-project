#!/usr/bin/env python3
"""
Read OpenFOAM's phi (face flux) field and decompose into structured face arrays.

OpenFOAM stores phi as a surfaceScalarField — one value per internal face,
plus boundary patches. The face ordering follows blockMesh conventions:
within each block, faces are ordered by direction (x, y, z) with the inner
index varying fastest.

For our 15-block mesh with 16000 cells:
- 46000 internal faces (from checkMesh)
- 4000 boundary faces (inlet=4, outlet=4, walls=3992)

The face numbering in multi-block OpenFOAM is complex. Instead of trying
to reconstruct it exactly, we'll use a simpler approach:

1. Read phi + boundary phi
2. For each cell, compute the NET flux = sum of phi on all faces
3. This should be ~0 for all cells (divergence-free)
4. Use cell-center U for the transport, but add a correction term to
   enforce mass conservation cell-by-cell

Actually, the simplest correct approach: export face velocities from OpenFOAM
using postProcess, or compute face interpolated U from phi/Sf.

BUT — the cleanest fix for our solver is different:
Instead of fighting with face indexing, we enforce conservation by
subtracting the local divergence from the convection term at each step.
"""
import numpy as np
import os


def read_phi_field(case_dir, time_dir='5000'):
    """Read phi surfaceScalarField. Returns flat array of internal face fluxes."""
    fpath = os.path.join(case_dir, time_dir, 'phi')
    values = []
    in_data = False
    count = 0
    expected = 0

    with open(fpath) as f:
        for line in f:
            line = line.strip()
            if not in_data:
                # Look for the count line before the data block
                try:
                    n = int(line)
                    expected = n
                    continue
                except ValueError:
                    pass
                if line == '(':
                    in_data = True
                    continue
            else:
                if line == ')':
                    break
                try:
                    values.append(float(line))
                except ValueError:
                    pass

    phi = np.array(values)
    print(f"Read {len(phi)} internal face fluxes (expected {expected})")
    return phi


def verify_divergence_from_phi(case_dir, time_dir='5000'):
    """
    Read phi and verify divergence-free.
    
    For a structured hex mesh, the face owner/neighbour can be read from
    constant/polyMesh/owner and constant/polyMesh/neighbour.
    """
    phi = read_phi_field(case_dir, time_dir)
    
    # Read owner and neighbour lists
    owner = read_label_list(os.path.join(case_dir, 'constant/polyMesh/owner'))
    neighbour = read_label_list(os.path.join(case_dir, 'constant/polyMesh/neighbour'))
    
    n_cells = max(max(owner), max(neighbour)) + 1
    n_internal = len(neighbour)
    
    print(f"Cells: {n_cells}, Internal faces: {n_internal}, Total faces: {len(owner)}")
    
    # Compute divergence: sum of phi over all faces of each cell
    div = np.zeros(n_cells)
    
    # Internal faces
    for f in range(n_internal):
        div[owner[f]] += phi[f]
        div[neighbour[f]] -= phi[f]
    
    # Boundary faces  
    # Read boundary phi from the file
    bphi = read_boundary_phi(case_dir, time_dir, len(owner) - n_internal)
    
    for f in range(n_internal, len(owner)):
        bf = f - n_internal
        if bf < len(bphi):
            div[owner[f]] += bphi[bf]
    
    print(f"Divergence from phi: max|div| = {np.max(np.abs(div)):.4e}, "
          f"mean|div| = {np.mean(np.abs(div)):.4e}")
    
    return div


def read_label_list(filepath):
    """Read an OpenFOAM label list file (owner, neighbour)."""
    values = []
    in_data = False
    
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not in_data:
                try:
                    int(line)
                    continue
                except ValueError:
                    pass
                if line == '(':
                    in_data = True
                    continue
            else:
                if line == ')':
                    break
                try:
                    values.append(int(line))
                except ValueError:
                    pass
    
    return values


def read_boundary_phi(case_dir, time_dir, n_boundary):
    """Read boundary face phi values from the phi file."""
    # Parse boundary section of phi file
    fpath = os.path.join(case_dir, time_dir, 'phi')
    bphi = np.zeros(n_boundary)
    
    with open(fpath) as f:
        content = f.read()
    
    # For inlet: fixedValue, value should be present
    # For outlet: calculated, value should be present
    # For walls: calculated, phi = 0
    
    # Simple approach: parse the boundaryField section
    # For now, assume boundary phi values come after internalField
    
    # Actually, let's just read ALL numbers from the boundary sections
    # The format is:
    #   boundaryField
    #   {
    #     inlet { type calculated; value nonuniform List<scalar> 4 (...); }
    #     ...
    #   }
    
    import re
    
    # Find boundaryField section
    bf_match = re.search(r'boundaryField\s*\{', content)
    if bf_match:
        bf_content = content[bf_match.end():]
        
        # Find each patch
        patch_pattern = re.compile(r'(\w+)\s*\{([^}]*)\}')
        offset = 0
        
        for patch_match in patch_pattern.finditer(bf_content):
            patch_name = patch_match.group(1)
            patch_body = patch_match.group(2)
            
            # Extract nFaces from polyMesh boundary
            # For now, extract values from the phi file
            if 'nonuniform' in patch_body:
                vals = re.findall(r'[-+]?\d*\.?\d+[eE][-+]?\d+|[-+]?\d*\.?\d+', 
                                  patch_body.split('(')[-1].split(')')[0])
                patch_values = [float(v) for v in vals if v]
                for i, v in enumerate(patch_values):
                    if offset + i < n_boundary:
                        bphi[offset + i] = v
                offset += len(patch_values)
            elif 'uniform' in patch_body:
                # Extract uniform value and nFaces
                val_match = re.search(r'uniform\s+([-+]?\d*\.?\d+[eE][-+]?\d+|[-+]?\d*\.?\d+)', 
                                      patch_body)
                if val_match:
                    val = float(val_match.group(1))
                    # Need nFaces — get from boundary file
                    # Skip for now, uniform 0 is most common
    
    return bphi


if __name__ == '__main__':
    import sys
    case_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/stevens/projects/drift-flux/case1'
    verify_divergence_from_phi(case_dir)
