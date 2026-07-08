"""Check that U_H applied to |0^m>|psi> is norm-preserving even if U_H
isn't a full unitary on the larger space.

Specifically: compute U_H[:, 0:64] (all columns with anc=0), check that
its 8192 x 64 slice satisfies M^dagger M = I_64.

This is the isometry condition that makes U_H a valid block encoding
on the encoding subspace.
"""
import numpy as np
from block_encoding import build_U_H_sparse, DIM_SYS, DIM_TOT, build_H_full

U_H, unit_err = build_U_H_sparse()
print(f"Global unitarity error: ||U U^T - I||_F = {unit_err:.3e}")

# Restrict to input columns |v=0,a=00,sel=00> |j>: cols 0..63
M = U_H[:, :DIM_SYS].toarray()
print(f"M shape: {M.shape}")
Mstar_M = M.T @ M
iso_err = np.linalg.norm(Mstar_M - np.eye(DIM_SYS))
print(f"||M^T M - I_64||_F = {iso_err:.6e}   (isometry check)")

# Also check M M^T for column space
if iso_err > 1e-10:
    print("Columns not orthonormal. Diagnosing...")
    # Print diag of M^T M
    diag_norms = np.diag(Mstar_M)
    print(f"  column-norm squares: min={diag_norms.min():.6f}, max={diag_norms.max():.6f}")

# Also check the block encoding
H = build_H_full()
block = M[:DIM_SYS, :]   # first 64 rows: anc=0 output
print(f"\n||16 * block - H||_F = {np.linalg.norm(16 * block - H):.3e}")
