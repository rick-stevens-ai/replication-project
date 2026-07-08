#!/usr/bin/env python3
"""
Pressure-projection to enforce discrete div(u)=0 on the structured grid.

The approach:
1. Compute face-centered velocities from cell-center OpenFOAM data
2. Set wall faces to zero normal velocity
3. Compute divergence of face velocity
4. Solve Poisson equation for pressure correction (scipy sparse)
5. Correct face velocities to be divergence-free
6. Reconstruct cell-center velocities from corrected face values
"""
import numpy as np
from scipy.sparse import diags, lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve
import os


def project_divergence_free(Ux, Uy, Uz, xc, yc, zc, inlet_mask, outlet_mask):
    """
    Project cell-center velocity to divergence-free face-center velocity.
    
    Returns corrected cell-center (Ux, Uy, Uz) AND face-center (uf, vf, wf).
    """
    nx, ny, nz = Ux.shape
    dx = xc[1] - xc[0]
    dy = yc[1] - yc[0]
    dz = zc[1] - zc[0]
    N = nx * ny * nz

    # Step 1: Interpolate to face centers
    uf = np.zeros((nx+1, ny, nz))
    vf = np.zeros((nx, ny+1, nz))
    wf = np.zeros((nx, ny, nz+1))

    # Interior faces
    uf[1:-1] = 0.5 * (Ux[:-1] + Ux[1:])
    vf[:, 1:-1, :] = 0.5 * (Uy[:, :-1, :] + Uy[:, 1:, :])
    wf[:, :, 1:-1] = 0.5 * (Uz[:, :, :-1] + Uz[:, :, 1:])

    # Boundary faces
    # x=0: inlet faces get Ux[0], wall faces get 0
    uf[0] = np.where(inlet_mask, Ux[0], 0.0)
    # x=Lx: outlet faces keep Ux[-1], wall faces get 0
    uf[-1] = np.where(outlet_mask, Ux[-1], 0.0)
    # y walls: zero normal velocity
    vf[:, 0, :] = 0.0
    vf[:, -1, :] = 0.0
    # z walls: zero normal velocity
    wf[:, :, 0] = 0.0
    wf[:, :, -1] = 0.0

    # Step 2: Compute divergence
    div = (uf[1:] - uf[:-1]) / dx + \
          (vf[:, 1:, :] - vf[:, :-1, :]) / dy + \
          (wf[:, :, 1:] - wf[:, :, :-1]) / dz

    print(f"  Before projection: max|div| = {np.max(np.abs(div)):.4e}, "
          f"mean|div| = {np.mean(np.abs(div)):.4e}, "
          f"rms(div) = {np.sqrt(np.mean(div**2)):.4e}")

    # Step 3: Build Laplacian matrix for pressure Poisson equation
    # lap(p) = div(u*)
    # With Neumann BC (dp/dn = 0) at all boundaries except:
    #   - inlet: dp/dx = 0 (velocity prescribed)
    #   - outlet: p = 0 (or dp/dx = 0)
    
    def idx(i, j, k):
        return i * ny * nz + j * nz + k

    # Build sparse matrix
    A = lil_matrix((N, N))
    rhs = div.ravel()

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                n = idx(i, j, k)
                diag = 0.0

                # x-direction
                if i > 0:
                    A[n, idx(i-1, j, k)] = 1.0 / dx**2
                    diag -= 1.0 / dx**2
                else:
                    # x=0 boundary: Neumann (ghost = interior) for all faces
                    # dp/dx = 0 → p_ghost = p_interior → nothing to add to off-diag
                    # But the diagonal contribution remains
                    # For Neumann: the face contribution is zero (dp/dn=0)
                    pass  # No off-diagonal, no diagonal contribution

                if i < nx - 1:
                    A[n, idx(i+1, j, k)] = 1.0 / dx**2
                    diag -= 1.0 / dx**2
                else:
                    # x=Lx boundary: Neumann
                    pass

                # y-direction
                if j > 0:
                    A[n, idx(i, j-1, k)] = 1.0 / dy**2
                    diag -= 1.0 / dy**2
                else:
                    pass

                if j < ny - 1:
                    A[n, idx(i, j+1, k)] = 1.0 / dy**2
                    diag -= 1.0 / dy**2
                else:
                    pass

                # z-direction
                if k > 0:
                    A[n, idx(i, j, k-1)] = 1.0 / dz**2
                    diag -= 1.0 / dz**2
                else:
                    pass

                if k < nz - 1:
                    A[n, idx(i, j, k+1)] = 1.0 / dz**2
                    diag -= 1.0 / dz**2
                else:
                    pass

                A[n, n] = diag

    # Pin pressure at one point (remove singularity from pure Neumann)
    # Set p[0,0,0] = 0
    A[0, :] = 0
    A[0, 0] = 1.0
    rhs[0] = 0.0

    # Step 4: Solve
    A_csc = csc_matrix(A)
    print(f"  Solving Poisson equation ({N} unknowns)...")
    p = spsolve(A_csc, rhs)
    p = p.reshape((nx, ny, nz))
    print(f"  Pressure correction: min={np.min(p):.4e}, max={np.max(p):.4e}")

    # Step 5: Correct face velocities
    # Interior x-faces
    uf[1:-1] -= (p[1:] - p[:-1]) / dx
    # Don't correct boundary x-faces (velocity is prescribed there)

    # Interior y-faces
    vf[:, 1:-1, :] -= (p[:, 1:, :] - p[:, :-1, :]) / dy
    # Don't correct boundary y-faces (walls)

    # Interior z-faces
    wf[:, :, 1:-1] -= (p[:, :, 1:] - p[:, :, :-1]) / dz
    # Don't correct boundary z-faces (walls)

    # Step 6: Verify
    div_after = (uf[1:] - uf[:-1]) / dx + \
                (vf[:, 1:, :] - vf[:, :-1, :]) / dy + \
                (wf[:, :, 1:] - wf[:, :, :-1]) / dz

    print(f"  After projection:  max|div| = {np.max(np.abs(div_after)):.4e}, "
          f"mean|div| = {np.mean(np.abs(div_after)):.4e}")

    # Step 7: Reconstruct cell-center velocities
    Ux_c = 0.5 * (uf[:-1] + uf[1:])
    Uy_c = 0.5 * (vf[:, :-1, :] + vf[:, 1:, :])
    Uz_c = 0.5 * (wf[:, :, :-1] + wf[:, :, 1:])

    print(f"  Max velocity change: |dUx|={np.max(np.abs(Ux_c-Ux)):.4e}, "
          f"|dUy|={np.max(np.abs(Uy_c-Uy)):.4e}, |dUz|={np.max(np.abs(Uz_c-Uz)):.4e}")

    # Mass flux check
    inlet_flux = np.sum(uf[0] * dy * dz)
    outlet_flux = np.sum(uf[-1] * dy * dz)
    print(f"  Mass flux: inlet={inlet_flux:.6e}, outlet={outlet_flux:.6e}, "
          f"imbalance={inlet_flux-outlet_flux:.2e}")

    return Ux_c, Uy_c, Uz_c, uf, vf, wf


def project_fields(fields_dir, output_dir=None):
    """Load, project, save."""
    if output_dir is None:
        output_dir = fields_dir

    Ux = np.load(os.path.join(fields_dir, 'Ux.npy'))
    Uy = np.load(os.path.join(fields_dir, 'Uy.npy'))
    Uz = np.load(os.path.join(fields_dir, 'Uz.npy'))
    xc = np.load(os.path.join(fields_dir, 'xc.npy'))
    yc = np.load(os.path.join(fields_dir, 'yc.npy'))
    zc = np.load(os.path.join(fields_dir, 'zc.npy'))

    nx, ny, nz = Ux.shape

    inlet_mask = np.zeros((ny, nz), dtype=bool)
    outlet_mask = np.zeros((ny, nz), dtype=bool)
    for iy in range(ny):
        for iz in range(nz):
            if abs(yc[iy] - 0.2) <= 0.02 and abs(zc[iz] - 0.36) <= 0.02:
                inlet_mask[iy, iz] = True
            if abs(yc[iy] - 0.2) <= 0.02 and abs(zc[iz] - 0.04) <= 0.02:
                outlet_mask[iy, iz] = True

    Ux_c, Uy_c, Uz_c, uf, vf, wf = project_divergence_free(
        Ux, Uy, Uz, xc, yc, zc, inlet_mask, outlet_mask
    )

    # Save corrected cell-center fields
    np.save(os.path.join(output_dir, 'Ux.npy'), Ux_c)
    np.save(os.path.join(output_dir, 'Uy.npy'), Uy_c)
    np.save(os.path.join(output_dir, 'Uz.npy'), Uz_c)
    # Save face velocities for solver
    np.save(os.path.join(output_dir, 'uf.npy'), uf)
    np.save(os.path.join(output_dir, 'vf.npy'), vf)
    np.save(os.path.join(output_dir, 'wf.npy'), wf)

    print(f"  Saved to {output_dir}")


if __name__ == '__main__':
    BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')

    for label, subdir in [('Case 1 (U=0.225)', 'openfoam_fields'),
                           ('Case 2 (U=0.45)', 'openfoam_fields_case2')]:
        fdir = os.path.join(BASE, 'data', subdir)
        if os.path.exists(os.path.join(fdir, 'Ux.npy')):
            print(f"\n{'='*60}")
            print(f"  {label}")
            print(f"{'='*60}")
            project_fields(fdir)
        else:
            print(f"Skipping {label}: no fields found")
