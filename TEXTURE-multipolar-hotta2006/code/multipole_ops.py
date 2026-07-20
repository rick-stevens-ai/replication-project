"""
Multipole operators for j=5/2 sextet (Hotta 2006, cond-mat/0611113, eqs 17-22).

Builds dipole (Gamma_4u), quadrupole (Gamma_3g, Gamma_5g) and octupole
(Gamma_2u, Gamma_4u, Gamma_5u) multipole operators from the J=5/2 angular
momentum matrices, then verifies:

  Claim 3: after orthonormal redefinition Tr(X_g X_g') = delta_{gg'}   (eq below 22)
  Claim 4: for j=5/2 the 4u dipole/octupole do NOT mix with the 5u octupole
           (paper: "in the case of n=5, 4u moment is not mixed with 5u")
           -> Tr(J_4u T_5u) etc. vanish.
  Claim 5: reported mixing coefficients (p,q,r) for the maximized multipole
           states are consistent with unit-norm eigenvectors of the
           susceptibility matrix (p^2+q^2(+r^2)=1).

Pure exact-operator algebra, no fitting.
"""
import numpy as np

def angular_momentum(j):
    """Return Jx, Jy, Jz, dim=2j+1, basis m = j, j-1, ..., -j."""
    dim = int(round(2*j+1))
    m = np.array([j - k for k in range(dim)])  # descending
    Jz = np.diag(m).astype(complex)
    # ladder: J+ |j,m> = sqrt(j(j+1)-m(m+1)) |j,m+1>
    Jp = np.zeros((dim, dim), dtype=complex)
    Jm = np.zeros((dim, dim), dtype=complex)
    for a in range(dim):
        for b in range(dim):
            ma, mb = m[a], m[b]
            if abs(ma - (mb + 1)) < 1e-9:
                Jp[a, b] = np.sqrt(j*(j+1) - mb*(mb+1))
            if abs(ma - (mb - 1)) < 1e-9:
                Jm[a, b] = np.sqrt(j*(j+1) - mb*(mb-1))
    Jx = 0.5*(Jp + Jm)
    Jy = (Jp - Jm)/(2j if False else 2j) if False else (Jp - Jm)/(2*1j)
    return Jx, Jy, Jz, dim

def sym_prod(*ops):
    """Symmetrized product = average over all permutations (the overbar in eq 19,22)."""
    from itertools import permutations
    perms = list(permutations(range(len(ops))))
    acc = np.zeros_like(ops[0])
    for p in perms:
        term = np.eye(ops[0].shape[0], dtype=complex)
        for idx in p:
            term = term @ ops[idx]
        acc += term
    return acc/len(perms)

def build_multipoles(j=2.5):
    Jx, Jy, Jz, dim = angular_momentum(j)
    I = np.eye(dim, dtype=complex)
    ops = {}
    # Dipole Gamma_4u (eq 17)
    ops['J4ux'] = Jx.copy(); ops['J4uy'] = Jy.copy(); ops['J4uz'] = Jz.copy()
    # Quadrupole Gamma_3g (eq 18)
    ops['O3gu'] = (2*Jz@Jz - Jx@Jx - Jy@Jy)/2
    ops['O3gv'] = np.sqrt(3)*(Jx@Jx - Jy@Jy)/2
    # Quadrupole Gamma_5g (eq 19), overbar = symmetrized product
    ops['O5gxi']  = np.sqrt(3)*sym_prod(Jy, Jz)
    ops['O5geta'] = np.sqrt(3)*sym_prod(Jz, Jx)
    ops['O5gzeta']= np.sqrt(3)*sym_prod(Jx, Jy)
    # Octupole Gamma_2u (eq 20)
    ops['T2u'] = np.sqrt(15)*sym_prod(Jx, Jy, Jz)
    # Octupole Gamma_4u (eq 21)
    ops['T4ux'] = (2*Jx@Jx@Jx - sym_prod(Jx,Jy,Jy)*3 - sym_prod(Jx,Jz,Jz)*3)/2
    ops['T4uy'] = (2*Jy@Jy@Jy - sym_prod(Jy,Jz,Jz)*3 - sym_prod(Jy,Jx,Jx)*3)/2
    ops['T4uz'] = (2*Jz@Jz@Jz - sym_prod(Jz,Jx,Jx)*3 - sym_prod(Jz,Jy,Jy)*3)/2
    # Octupole Gamma_5u (eq 22)
    ops['T5ux'] = np.sqrt(15)*(sym_prod(Jx,Jy,Jy) - sym_prod(Jx,Jz,Jz))/2
    ops['T5uy'] = np.sqrt(15)*(sym_prod(Jy,Jz,Jz) - sym_prod(Jy,Jx,Jx))/2
    ops['T5uz'] = np.sqrt(15)*(sym_prod(Jz,Jx,Jx) - sym_prod(Jz,Jy,Jy))/2
    return ops, (Jx, Jy, Jz)

def trace_norm(A):
    return np.real(np.trace(A.conj().T @ A))

def orthonormalize(ops):
    """Rescale each operator so Tr(X X) = 1 (the redefinition below eq 22)."""
    out = {}
    for k, A in ops.items():
        n = trace_norm(A)
        out[k] = A/np.sqrt(n) if n > 1e-12 else A
    return out

if __name__ == '__main__':
    import json
    ops, (Jx, Jy, Jz) = build_multipoles(2.5)
    print("=== j=5/2 multipole operators, dim =", ops['J4ux'].shape[0], "===")
    # raw trace norms
    print("\n-- raw Tr(X^2) --")
    for k in ops:
        print(f"  {k:8s} Tr(X^2)={trace_norm(ops[k]):10.5f}")

    on = orthonormalize(ops)

    # Claim 3: orthonormality Tr(X_g X_g') = delta after normalization
    keys = list(on.keys())
    maxoff = 0.0
    for i in range(len(keys)):
        for jj in range(len(keys)):
            v = np.real(np.trace(on[keys[i]].conj().T @ on[keys[jj]]))
            if i == jj:
                diag_err = abs(v - 1.0)
            else:
                maxoff = max(maxoff, abs(v))
    print(f"\n[Claim 3] after normalization: max |Tr(Xi Xj)| off-diag = {maxoff:.2e}")
    print(f"          (all diagonals = 1 by construction)")

    # Claim 4: 4u does not mix with 5u for j=5/2 (same symmetry label u, checked via overlap)
    print("\n[Claim 4] 4u vs 5u octupole overlap for j=5/2:")
    for a in ['x','y','z']:
        j4 = on[f'J4u{a}']; t4 = on[f'T4u{a}']; t5 = on[f'T5u{a}']
        o_j4_t5 = np.real(np.trace(j4.conj().T @ t5))
        o_t4_t5 = np.real(np.trace(t4.conj().T @ t5))
        print(f"   a={a}: <J4u|T5u>={o_j4_t5:+.3e}   <T4u|T5u>={o_t4_t5:+.3e}")

    # Claim 5: reported (p,q) / (p,q,r) unit norm
    print("\n[Claim 5] reported mixing-coefficient norms (should be ~1):")
    cases = {
        'Fig2a 4u (G5) pa,qa': (0.326, -0.946, None),
        'Fig2c 4u (G67) pa,qa': (0.560, 0.828, None),
        'Fig3d Ma 4u+5u pa,qa,ra': (0.761, 0.428, -0.488),
        'Fig3d Mz pz,qz,rz': (0.67, -0.739, 0.0),
    }
    for name, (p, q, r) in cases.items():
        nrm = p*p + q*q + (r*r if r is not None else 0.0)
        print(f"   {name:28s} norm^2 = {nrm:.4f}")
