#!/usr/bin/env python3
"""Replication: Cade, Mineh, Montanaro, Stanisic (2020)
"Strategies for solving the Fermi-Hubbard model on near-term quantum computers"

Scope (this script): classical statevector VQE with the Hamiltonian Variational (HV)
ansatz on small 2D Fermi-Hubbard lattices. We replicate the qualitative claim that
energy error vs exact diagonalization decreases (roughly exponentially) with HV
ansatz depth on small lattices.

Approach:
  - Build the FH Hamiltonian H = -t * sum_{<i,j>,sigma} (a_i^d a_j + h.c.)
                                + U * sum_i n_{i,up} n_{i,down}
    via Jordan-Wigner -> sparse Pauli matrices (no quantum framework, no openfermion).
  - Split H into commuting pieces: H_O (onsite), H_H (horizontal hops, all spins),
    H_V (vertical hops, all spins). For 1xN and 2xN this matches the paper's
    O, H, V grouping (collapsed for simplicity; pieces inside each group commute
    among themselves under JW).
  - HV ansatz with L layers, 3 params per layer (theta_O, theta_H, theta_V):
        |psi(theta)> = prod_{l=1..L} e^{-i theta^l_V H_V} e^{-i theta^l_H H_H} e^{-i theta^l_O H_O} |psi_0>
    |psi_0> = ground state of the t-only (U=0) Hamiltonian, projected into the
    target particle-number sector.
  - Restrict to the (N_up, N_down) particle-number sector that contains the global
    ground state (saves memory, matches paper which works in fixed occupation).
  - VQE: scipy.optimize.minimize with L-BFGS-B (paper's choice). Energy gradient
    by finite differences (paper does the same).
  - Compare VQE(L) energy to exact ground-state energy from sparse eigensolver.
"""

from __future__ import annotations
import json, time, itertools, sys
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import minimize

# ---------- Pauli / Jordan-Wigner machinery ----------

I2 = sp.eye(2, format="csr", dtype=complex)
X = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
Y = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
Z = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))

def kron_list(ops):
    out = ops[0]
    for o in ops[1:]:
        out = sp.kron(out, o, format="csr")
    return out

def pauli_string(nq: int, ops: Dict[int, sp.csr_matrix]) -> sp.csr_matrix:
    """Build tensor product across nq qubits; qubits not in ops get I."""
    return kron_list([ops.get(q, I2) for q in range(nq)])

def jw_hop(nq: int, i: int, j: int) -> sp.csr_matrix:
    """a_i^d a_j + a_j^d a_i  ->  (1/2)(X_i X_j + Y_i Y_j) * Z_{i+1}...Z_{j-1}
    Convention: qubit 0 is the first JW mode. i < j."""
    if i > j:
        i, j = j, i
    ops_xx = {i: X, j: X}
    ops_yy = {i: Y, j: Y}
    for k in range(i + 1, j):
        ops_xx[k] = Z
        ops_yy[k] = Z
    return 0.5 * (pauli_string(nq, ops_xx) + pauli_string(nq, ops_yy))

def jw_number(nq: int, i: int) -> sp.csr_matrix:
    """n_i = a_i^d a_i = (I - Z_i)/2"""
    return 0.5 * (pauli_string(nq, {}) - pauli_string(nq, {i: Z}))


# ---------- Fermi-Hubbard Hamiltonian ----------

@dataclass
class Lattice:
    nx: int
    ny: int

    @property
    def n_sites(self) -> int:
        return self.nx * self.ny

    @property
    def n_qubits(self) -> int:
        # 2 qubits per site (spin up + spin down)
        return 2 * self.n_sites

    def site_index(self, x: int, y: int) -> int:
        # row-major snake-ish; for our small grids exact ordering doesn't change
        # the spectrum, only the JW string lengths. Use simple row-major.
        return y * self.nx + x

    def qubit_up(self, site: int) -> int:
        return 2 * site
    def qubit_dn(self, site: int) -> int:
        return 2 * site + 1

    def hop_pairs(self) -> Tuple[List[Tuple[int,int]], List[Tuple[int,int]]]:
        """Return (horizontal, vertical) site-pairs."""
        horiz, vert = [], []
        for y in range(self.ny):
            for x in range(self.nx - 1):
                horiz.append((self.site_index(x, y), self.site_index(x + 1, y)))
        for y in range(self.ny - 1):
            for x in range(self.nx):
                vert.append((self.site_index(x, y), self.site_index(x, y + 1)))
        return horiz, vert


def build_hamiltonian_parts(lat: Lattice, t: float, U: float):
    """Return H_O, H_H, H_V, H_total as sparse matrices (full 2^{2N} space)."""
    nq = lat.n_qubits
    horiz, vert = lat.hop_pairs()

    H_H = sp.csr_matrix((2 ** nq, 2 ** nq), dtype=complex)
    for (a, b) in horiz:
        for spin_q in (lat.qubit_up, lat.qubit_dn):
            qi, qj = spin_q(a), spin_q(b)
            H_H = H_H + (-t) * jw_hop(nq, qi, qj)

    H_V = sp.csr_matrix((2 ** nq, 2 ** nq), dtype=complex)
    for (a, b) in vert:
        for spin_q in (lat.qubit_up, lat.qubit_dn):
            qi, qj = spin_q(a), spin_q(b)
            H_V = H_V + (-t) * jw_hop(nq, qi, qj)

    H_O = sp.csr_matrix((2 ** nq, 2 ** nq), dtype=complex)
    for s in range(lat.n_sites):
        H_O = H_O + U * (jw_number(nq, lat.qubit_up(s)) @ jw_number(nq, lat.qubit_dn(s)))

    H_tot = H_H + H_V + H_O
    return H_O, H_H, H_V, H_tot


# ---------- Particle-number sector projection ----------

def hamming_weight(x: int) -> int:
    return bin(x).count("1")

def number_sector_basis(nq: int, n_up: int, n_dn: int, lat: Lattice) -> np.ndarray:
    """Return indices of basis states with given up/down occupation."""
    up_qubits = [lat.qubit_up(s) for s in range(lat.n_sites)]
    dn_qubits = [lat.qubit_dn(s) for s in range(lat.n_sites)]
    idx = []
    for x in range(2 ** nq):
        n_u = sum(((x >> q) & 1) for q in up_qubits)
        n_d = sum(((x >> q) & 1) for q in dn_qubits)
        if n_u == n_up and n_d == n_dn:
            idx.append(x)
    return np.array(idx, dtype=np.int64)


def find_ground_sector(H_tot: sp.csr_matrix, lat: Lattice):
    """Scan all (n_up, n_dn) sectors, return (n_up, n_dn, E_exact, sector_idx,
    H_sector_full_size_projected, projector_P) where states live in
    full Hilbert space restricted to indices in sector_idx."""
    best = None
    nq = lat.n_qubits
    for n_up in range(lat.n_sites + 1):
        for n_dn in range(lat.n_sites + 1):
            idx = number_sector_basis(nq, n_up, n_dn, lat)
            if len(idx) == 0:
                continue
            Hs = H_tot[idx, :][:, idx].tocsr()
            d = Hs.shape[0]
            if d == 1:
                e = float(Hs.toarray().real[0, 0])
                vec = np.array([1.0+0j])
            elif d <= 100:
                e_full, v_full = np.linalg.eigh(Hs.toarray())
                e = float(e_full[0]); vec = v_full[:, 0]
            else:
                e_arr, v_arr = spla.eigsh(Hs, k=1, which="SA")
                e = float(e_arr[0]); vec = v_arr[:, 0]
            if best is None or e < best["E"]:
                best = {"n_up": n_up, "n_dn": n_dn, "E": e, "idx": idx, "gs": vec, "dim": d}
    return best


# ---------- Sector-restricted operators and VQE ----------

def project(H: sp.csr_matrix, idx: np.ndarray) -> sp.csr_matrix:
    return H[idx, :][:, idx].tocsr()


def apply_expm(H_sec, theta: float, psi: np.ndarray) -> np.ndarray:
    """Compute exp(-i theta H_sec) @ psi. If H_sec is a precomputed eigendecomp
    tuple (evals, evecs), use dense diagonalization (fast for small sectors)."""
    if isinstance(H_sec, tuple):
        evals, evecs = H_sec
        coeffs = evecs.conj().T @ psi
        coeffs = np.exp(-1j * theta * evals) * coeffs
        return evecs @ coeffs
    return spla.expm_multiply(-1j * theta * H_sec, psi)


def ansatz_state(theta: np.ndarray, psi0: np.ndarray,
                 H_O_sec, H_H_sec,
                 H_V_sec, has_V: bool) -> np.ndarray:
    """HV ansatz with L layers. params per layer:
       (theta_O, theta_H, theta_V) if has_V else (theta_O, theta_H).
       Order per layer: e^{-i tO H_O} then e^{-i tH H_H} then e^{-i tV H_V}."""
    per = 3 if has_V else 2
    L = len(theta) // per
    psi = psi0.copy()
    for l in range(L):
        tO = theta[per*l + 0]
        tH = theta[per*l + 1]
        psi = apply_expm(H_O_sec, tO, psi)
        psi = apply_expm(H_H_sec, tH, psi)
        if has_V:
            tV = theta[per*l + 2]
            psi = apply_expm(H_V_sec, tV, psi)
    return psi


def energy(theta, psi0, H_O_sec, H_H_sec, H_V_sec, H_tot_sec, has_V):
    psi = ansatz_state(theta, psi0, H_O_sec, H_H_sec, H_V_sec, has_V)
    return float(np.real(np.vdot(psi, H_tot_sec @ psi)))


# ---------- Main experiment ----------

def run_lattice(nx: int, ny: int, t: float, U: float, depths: List[int],
                n_restarts: int = 3, seed: int = 0) -> Dict:
    lat = Lattice(nx, ny)
    print(f"\n=== Lattice {nx}x{ny}  (qubits={lat.n_qubits})  t={t} U={U} ===", flush=True)
    t0 = time.time()

    H_O, H_H, H_V, H_tot = build_hamiltonian_parts(lat, t, U)
    print(f"  built H in {time.time()-t0:.2f}s (dim={H_tot.shape[0]})", flush=True)

    # Find ground sector via exact diagonalization
    best = find_ground_sector(H_tot, lat)
    E_exact = best["E"]; idx = best["idx"]; gs_exact = best["gs"]; dim = best["dim"]
    print(f"  exact ground sector: (n_up={best['n_up']}, n_dn={best['n_dn']})  dim={dim}  E_exact={E_exact:.8f}", flush=True)

    # Project operators
    H_O_sec = project(H_O, idx)
    H_H_sec = project(H_H, idx)
    H_V_sec = project(H_V, idx)
    H_tot_sec = project(H_tot, idx)
    has_V = (ny > 1)

    # Precompute eigendecompositions of each piece for fast e^{-i theta H} action.
    # For our sector dims (<= a few hundred), this is much faster than Krylov.
    def eigdec(Hs):
        d = Hs.shape[0]
        if d <= 1500:
            ev, vv = np.linalg.eigh(Hs.toarray())
            return (ev, vv.astype(complex))
        return Hs  # fall back to sparse expm_multiply
    H_O_op = eigdec(H_O_sec)
    H_H_op = eigdec(H_H_sec)
    H_V_op = eigdec(H_V_sec) if has_V else None

    # Initial state: non-interacting ground state in this sector
    H_noninter_sec = H_H_sec + H_V_sec
    if dim == 1:
        psi0 = np.array([1.0+0j])
    elif dim <= 100:
        ev, vv = np.linalg.eigh(H_noninter_sec.toarray())
        psi0 = vv[:, 0].astype(complex)
    else:
        ev, vv = spla.eigsh(H_noninter_sec, k=1, which="SA")
        psi0 = vv[:, 0].astype(complex)
    psi0 /= np.linalg.norm(psi0)
    E_noninter = float(np.real(np.vdot(psi0, H_tot_sec @ psi0)))
    print(f"  non-interacting GS energy in full H: {E_noninter:.6f}  (delta to exact: {E_noninter - E_exact:+.6f})", flush=True)

    rng = np.random.default_rng(seed)
    per = 3 if has_V else 2

    results_per_depth = []
    for L in depths:
        nparams = per * L
        # Multi-start: deterministic 1/L init + (n_restarts-1) random
        best_E = None
        best_theta = None
        for r in range(n_restarts):
            if r == 0:
                x0 = np.full(nparams, 1.0 / max(L, 1))
            else:
                x0 = rng.uniform(0, 2*np.pi/100.0, size=nparams)
            try:
                res = minimize(
                    energy, x0,
                    args=(psi0, H_O_op, H_H_op, H_V_op, H_tot_sec, has_V),
                    method="L-BFGS-B",
                    options={"maxiter": 150, "ftol": 1e-9, "gtol": 1e-6},
                )
                E_r = res.fun
            except Exception as e:
                print(f"    depth {L} restart {r}: optimizer failed: {e}", flush=True)
                continue
            if best_E is None or E_r < best_E:
                best_E = E_r
                best_theta = res.x
        err = best_E - E_exact
        # Fidelity to exact ground state
        psi_v = ansatz_state(best_theta, psi0, H_O_op, H_H_op, H_V_op, has_V)
        fid = float(abs(np.vdot(gs_exact, psi_v))**2)
        print(f"  depth {L:2d}  params={nparams:3d}  E_vqe={best_E:.6f}  err={err:+.2e}  fidelity={fid:.4f}", flush=True)
        results_per_depth.append({
            "depth": L,
            "n_params": nparams,
            "E_vqe": best_E,
            "energy_error": err,
            "fidelity": fid,
        })

    return {
        "lattice": f"{nx}x{ny}",
        "nx": nx, "ny": ny,
        "n_sites": lat.n_sites,
        "n_qubits": lat.n_qubits,
        "t": t, "U": U,
        "n_up": best["n_up"], "n_dn": best["n_dn"],
        "sector_dim": dim,
        "E_exact": E_exact,
        "E_noninteracting_in_full_H": E_noninter,
        "has_vertical_hopping": has_V,
        "params_per_layer": per,
        "depths": results_per_depth,
        "wall_time_s": time.time() - t0,
    }


def main():
    t = 1.0
    U = 2.0  # paper's standard choice
    # Lattices: 1x2 (4q), 2x2 (8q), 1x4 (8q), 1x6 (12q), 2x3 (12q)
    configs = [
        (1, 2, [1, 2, 3, 4, 5, 6], 3),
        (2, 2, [1, 2, 3, 4, 5, 6, 8], 3),
        (1, 4, [1, 2, 3, 4, 5, 6, 8], 2),
        (1, 6, [1, 2, 3, 4, 5, 6, 8], 2),
        (2, 3, [1, 2, 3, 4, 5, 6, 8], 2),
    ]
    all_results = []
    for (nx, ny, depths, nrest) in configs:
        try:
            r = run_lattice(nx, ny, t, U, depths, n_restarts=nrest, seed=42)
            all_results.append(r)
            # WRITE INTERMEDIATE RESULTS after each lattice (timeout hardening)
            with open("results.json", "w") as f:
                json.dump({
                    "paper": "Cade, Mineh, Montanaro, Stanisic (2020) — Strategies for solving the Fermi-Hubbard model on near-term quantum computers",
                    "scope": "small-lattice classical statevector VQE with HV ansatz (depth scan), comparison to exact diagonalization",
                    "params": {"t": t, "U": U, "optimizer": "L-BFGS-B",
                               "ansatz": "HV (Hamiltonian Variational): per-layer params (theta_O, theta_H[, theta_V])",
                               "initial_state": "ground state of non-interacting (U=0) H projected to ground particle-number sector",
                               "n_restarts_per_depth": 3,
                               "encoding": "Jordan-Wigner, hand-built sparse Pauli operators"},
                    "results": all_results,
                }, f, indent=2)
            print(f"  -> wrote intermediate results.json ({len(all_results)} lattices done)", flush=True)
        except Exception as e:
            print(f"!! lattice {nx}x{ny} FAILED: {e}", flush=True)
            import traceback; traceback.print_exc()

    print("\nALL DONE")


if __name__ == "__main__":
    main()
