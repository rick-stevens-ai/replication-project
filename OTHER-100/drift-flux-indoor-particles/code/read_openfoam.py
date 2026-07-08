#!/usr/bin/env python3
"""
Read OpenFOAM fields from ascii format and map to structured grid.
For the drift-flux replication (Chen et al. 2006).
"""
import numpy as np
import re
import os
import json

# Grid parameters matching blockMeshDict
NX, NY, NZ = 40, 20, 20
LX, LY, LZ = 0.8, 0.4, 0.4


def read_openfoam_vector_field(filepath):
    """Read an OpenFOAM volVectorField from ascii file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the internalField data
    # Pattern: internalField nonuniform List<vector> N ( ... )
    match = re.search(r'internalField\s+nonuniform\s+List<vector>\s*\n(\d+)\s*\n\(', content)
    if not match:
        raise ValueError(f"Cannot parse vector field from {filepath}")

    n_cells = int(match.group(1))
    # Extract vectors
    start = match.end()
    vectors = []
    for line in content[start:].split('\n'):
        line = line.strip()
        if line == ')':
            break
        if line.startswith('(') and line.endswith(')'):
            vals = line[1:-1].split()
            vectors.append([float(v) for v in vals])

    return np.array(vectors)


def read_openfoam_scalar_field(filepath):
    """Read an OpenFOAM volScalarField from ascii file."""
    with open(filepath, 'r') as f:
        content = f.read()

    match = re.search(r'internalField\s+nonuniform\s+List<scalar>\s*\n(\d+)\s*\n\(', content)
    if not match:
        # Try uniform
        match_uni = re.search(r'internalField\s+uniform\s+([\d.eE+-]+)', content)
        if match_uni:
            val = float(match_uni.group(1))
            return np.full(NX * NY * NZ, val)
        raise ValueError(f"Cannot parse scalar field from {filepath}")

    n_cells = int(match.group(1))
    start = match.end()
    values = []
    for line in content[start:].split('\n'):
        line = line.strip()
        if line == ')':
            break
        if line and not line.startswith('/'):
            try:
                values.append(float(line))
            except ValueError:
                pass

    return np.array(values)


def map_to_structured(flat_data, nx=NX, ny=NY, nz=NZ):
    """
    Map flat OpenFOAM cell data to structured 3D array.

    OpenFOAM blockMesh with multiple blocks orders cells block-by-block.
    Our blockMeshDict has 15 blocks (5 z-layers × 3 y-segments).

    Block ordering in blockMeshDict:
    z-layer 0 (z=0..0.02):    blocks 0,1,2   (y: 0..0.18, 0.18..0.22, 0.22..0.4)
    z-layer 1 (z=0.02..0.06): blocks 3,4,5
    z-layer 2 (z=0.06..0.34): blocks 6,7,8
    z-layer 3 (z=0.34..0.38): blocks 9,10,11
    z-layer 4 (z=0.38..0.4):  blocks 12,13,14

    Within each block: i varies fastest (x), then j (y), then k (z)
    """
    # Block structure: (nx, ny_cells, nz_cells)
    # y segments: 9, 2, 9 cells
    # z segments: 1, 2, 14, 2, 1 cells
    ny_segs = [9, 2, 9]
    nz_segs = [1, 2, 14, 2, 1]

    result = np.zeros((nx, ny, nz))
    idx = 0

    for iz_seg, nz_blk in enumerate(nz_segs):
        for iy_seg, ny_blk in enumerate(ny_segs):
            # This block has nx × ny_blk × nz_blk cells
            n_blk = nx * ny_blk * nz_blk

            # Starting indices in the structured grid
            iy_start = sum(ny_segs[:iy_seg])
            iz_start = sum(nz_segs[:iz_seg])

            # Extract and reshape block data
            blk_data = flat_data[idx:idx + n_blk]

            # OpenFOAM orders: i fastest, then j, then k
            blk_3d = blk_data.reshape((nz_blk, ny_blk, nx))

            # Map to structured grid
            for kk in range(nz_blk):
                for jj in range(ny_blk):
                    for ii in range(nx):
                        result[ii, iy_start + jj, iz_start + kk] = blk_3d[kk, jj, ii]

            idx += n_blk

    return result


def extract_fields(case_dir, time_dir='5000'):
    """Extract U, nut, k, epsilon from OpenFOAM case."""
    td = os.path.join(case_dir, time_dir)

    print(f"Reading fields from {td}")

    # Velocity
    U_flat = read_openfoam_vector_field(os.path.join(td, 'U'))
    print(f"  U: {len(U_flat)} vectors")

    Ux = map_to_structured(U_flat[:, 0])
    Uy = map_to_structured(U_flat[:, 1])
    Uz = map_to_structured(U_flat[:, 2])

    # Turbulent viscosity
    nut_flat = read_openfoam_scalar_field(os.path.join(td, 'nut'))
    nut = map_to_structured(nut_flat)
    print(f"  nut: {len(nut_flat)} values, range [{np.min(nut):.2e}, {np.max(nut):.2e}]")

    # k and epsilon for friction velocity calculation
    k_flat = read_openfoam_scalar_field(os.path.join(td, 'k'))
    k = map_to_structured(k_flat)

    eps_flat = read_openfoam_scalar_field(os.path.join(td, 'epsilon'))
    eps = map_to_structured(eps_flat)

    # Cell centers
    dx, dy, dz = LX/NX, LY/NY, LZ/NZ
    xc = np.linspace(dx/2, LX-dx/2, NX)
    yc = np.linspace(dy/2, LY-dy/2, NY)
    zc = np.linspace(dz/2, LZ-dz/2, NZ)

    # Friction velocity estimate from k: u* = Cmu^0.25 * k^0.5
    Cmu = 0.0845
    u_star = Cmu**0.25 * np.sqrt(k)

    print(f"\nField statistics:")
    print(f"  Ux: [{np.min(Ux):.4f}, {np.max(Ux):.4f}] m/s")
    print(f"  Uy: [{np.min(Uy):.4f}, {np.max(Uy):.4f}] m/s")
    print(f"  Uz: [{np.min(Uz):.4f}, {np.max(Uz):.4f}] m/s")
    print(f"  |U|_max: {np.max(np.sqrt(Ux**2 + Uy**2 + Uz**2)):.4f} m/s")
    print(f"  nut: [{np.min(nut):.2e}, {np.max(nut):.2e}] m^2/s")
    print(f"  k: [{np.min(k):.2e}, {np.max(k):.2e}] m^2/s^2")
    print(f"  u*: [{np.min(u_star):.4f}, {np.max(u_star):.4f}] m/s")

    # Save as numpy arrays
    output_dir = os.path.join(case_dir, 'exported_fields')
    os.makedirs(output_dir, exist_ok=True)

    np.save(os.path.join(output_dir, 'Ux.npy'), Ux)
    np.save(os.path.join(output_dir, 'Uy.npy'), Uy)
    np.save(os.path.join(output_dir, 'Uz.npy'), Uz)
    np.save(os.path.join(output_dir, 'nut.npy'), nut)
    np.save(os.path.join(output_dir, 'k.npy'), k)
    np.save(os.path.join(output_dir, 'epsilon.npy'), eps)
    np.save(os.path.join(output_dir, 'u_star.npy'), u_star)
    np.save(os.path.join(output_dir, 'xc.npy'), xc)
    np.save(os.path.join(output_dir, 'yc.npy'), yc)
    np.save(os.path.join(output_dir, 'zc.npy'), zc)

    # Quick velocity profile extraction at validation locations
    iy_center = NY // 2
    profiles = {}
    for x_loc in [0.2, 0.4, 0.6]:
        ix = np.argmin(np.abs(xc - x_loc))
        profiles[str(x_loc)] = {
            'z': zc.tolist(),
            'Ux': Ux[ix, iy_center, :].tolist()
        }

    with open(os.path.join(output_dir, 'velocity_profiles.json'), 'w') as f:
        json.dump(profiles, f, indent=2)

    print(f"\nVelocity profiles at center plane (y=0.2m):")
    for x_loc in [0.2, 0.4, 0.6]:
        p = profiles[str(x_loc)]
        ux_arr = np.array(p['Ux'])
        print(f"  x={x_loc}m: Ux range [{np.min(ux_arr):.4f}, {np.max(ux_arr):.4f}]")

    print(f"\nFields saved to {output_dir}")
    return Ux, Uy, Uz, nut, u_star, xc, yc, zc


if __name__ == '__main__':
    import sys
    case_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/stevens/projects/drift-flux/case1'
    extract_fields(case_dir)
