#!/usr/bin/env python3
"""
Second test: 2-site Hubbard dimer (canonical q-chem toy — mimics H2 in a minimal
basis when U~2t and half-filled). Split H = T (hopping / kinetic) + V (Coulomb).

Confirms the same predicted scaling on a truly q-chem-flavored Hamiltonian.
"""
import json, numpy as np
from scipy.linalg import expm
from pathlib import Path

# 4 spin-orbitals: (site0-up, site0-down, site1-up, site1-down)  → dim 16 Fock space
# Basis: |n0up n0dn n1up n1dn>, n∈{0,1}. We use 2nd-quantized c/c† via Jordan-Wigner.

def jw_ops(n_modes):
    """Return list of c_i (annihilation) operators as 2^n × 2^n matrices via JW."""
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    Sminus = np.array([[0, 1], [0, 0]], dtype=complex)  # |0><1|
    ops = []
    for i in range(n_modes):
        parts = [Z] * i + [Sminus] + [I] * (n_modes - i - 1)
        op = parts[0]
        for p in parts[1:]:
            op = np.kron(op, p)
        ops.append(op)
    return ops

def build_hubbard_dimer(t_hop=1.0, U=2.0):
    n_modes = 4  # 2 sites × 2 spins
    c = jw_ops(n_modes)
    cd = [ci.conj().T for ci in c]

    # T (kinetic / hopping): -t (c†_{0σ} c_{1σ} + h.c.) for σ = up (mode0↔mode2), down (mode1↔mode3)
    T = np.zeros_like(c[0])
    for (i, j) in [(0, 2), (1, 3)]:
        T += -t_hop * (cd[i] @ c[j] + cd[j] @ c[i])

    # V (Coulomb): U * n_{0up} n_{0dn} + U * n_{1up} n_{1dn}
    n = [cd[i] @ c[i] for i in range(n_modes)]
    V = U * (n[0] @ n[1] + n[2] @ n[3])
    return T, V

def op_norm(M): return np.linalg.norm(M, ord=2)

def trotter_step(A, B, dt):
    return expm(-1j * A * dt) @ expm(-1j * B * dt)
def strang_step(A, B, dt):
    eA = expm(-1j * A * dt / 2)
    return eA @ expm(-1j * B * dt) @ eA

def evolve(fn, A, B, t, r):
    Us = fn(A, B, t / r)
    U = np.eye(A.shape[0], dtype=complex)
    for _ in range(r):
        U = Us @ U
    return U

def fit_slope(r, e):
    r = np.array(r); e = np.array(e)
    m = e > 0
    s, b = np.polyfit(np.log(r[m]), np.log(e[m]), 1)
    pred = s * np.log(r[m]) + b
    return float(s), float(b), float(np.sqrt(np.mean((np.log(e[m]) - pred) ** 2)))

def main():
    T, V = build_hubbard_dimer(t_hop=1.0, U=2.0)
    print(f"# Hubbard dimer dim={T.shape[0]} ||T||={op_norm(T):.3f} ||V||={op_norm(V):.3f} ||[T,V]||={op_norm(T@V - V@T):.3f}")
    t = 1.0
    r_list = [2, 4, 8, 16, 32, 64, 128, 256]

    # Half-filled reference product state (Hartree-Fock-like): |1010> = c†_0 c†_2 |vac>
    dim = T.shape[0]
    # Superposition of half-filled states (has nontrivial overlap with V's excited subspace)
    # so that state error is nonzero and physically meaningful.
    psi0 = np.zeros(dim, dtype=complex)
    for bits in ["1010", "0101", "1100", "0011"]:
        psi0[int(bits, 2)] = 1.0
    psi0 = psi0 / np.linalg.norm(psi0)

    U_exact = expm(-1j * (T + V) * t)
    psi_ex = U_exact @ psi0

    rows = []
    for r in r_list:
        Utr = evolve(trotter_step, T, V, t, r)
        Ust = evolve(strang_step,  T, V, t, r)
        rows.append({
            "r": r,
            "op_tr": float(op_norm(U_exact - Utr)),
            "op_st": float(op_norm(U_exact - Ust)),
            "st_tr": float(np.linalg.norm(psi_ex - Utr @ psi0)),
            "st_st": float(np.linalg.norm(psi_ex - Ust @ psi0)),
        })
        print(f"  r={r:4d} opTR={rows[-1]['op_tr']:.3e} opST={rows[-1]['op_st']:.3e} stTR={rows[-1]['st_tr']:.3e} stST={rows[-1]['st_st']:.3e}")

    fits = {}
    for key in ["op_tr", "op_st", "st_tr", "st_st"]:
        s, b, rmse = fit_slope([x["r"] for x in rows], [x[key] for x in rows])
        fits[key] = {"slope": s, "intercept": b, "rmse": rmse}
    print("\nSlopes (pred: TR=-1, ST=-2):")
    for k, v in fits.items():
        pred = -1 if "tr" in k else -2
        print(f"  {k}: {v['slope']:+.4f} (pred {pred}) rmse={v['rmse']:.2e}")

    out = Path(__file__).resolve().parent.parent / "results/hubbard_dimer.json"
    out.write_text(json.dumps({
        "model": {"type": "Hubbard dimer (2 sites, 2 spins, half-filled)", "t_hop": 1.0, "U": 2.0, "t": t},
        "initial_state": "|1010> (half-filled HF-like product state)",
        "rows": rows,
        "fits": fits,
    }, indent=2))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
