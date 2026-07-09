#!/usr/bin/env python3
"""
Independent replication of the Toffoli gate construction from
Wang, Sørensen, Mølmer, "Multi-bit gates for quantum computing", quant-ph/0012055.

Paper's central concrete claim (Eq. 5):
    H = Omega * [ (sig_z1 + sig_z2 + 1)/(4 sqrt(K)) * x  -  sig_x3 * (n + 1/(32K)) ]
where x = (a + a^dag)/sqrt(2) and n = a^dag a.
After time tau = K * 2*pi / Omega, the propagator equals
    exp(-i pi (sig_z1 + 1)(sig_z2 + 1) sig_x3 / 8)
which (up to a global phase) is the CCNOT (Toffoli) gate acting on qubit 3
controlled by qubits 1 and 2. In particular the total unitary is claimed to
disentangle the qubits from the oscillator and be independent of the oscillator's
initial state (works for ground, excited, or thermal).

Reproduction plan
-----------------
1. Build H numerically in (2 x 2 x 2 x N_fock) Hilbert space via QuTiP.
2. Time-evolve U(tau) via exact matrix exponential.
3. Project onto oscillator |0><0| (or any Fock |k><k|) and compare the
   resulting 8x8 qubit operator to the ideal Toffoli.
4. Report:
     - Average gate fidelity F_avg(K) of the *ideal-oscillator-return* channel
       to the ideal Toffoli, for K in {1,2,4}.
     - Verify insensitivity to oscillator initial state: run for |0>, |1>, |2>
       and thermal (n_bar=1). Check fidelity of the reduced qubit channel.

QuTiP >= 5 API.
"""
import json, sys, os, time
from pathlib import Path
import numpy as np
import qutip as qt

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


# --- Ideal Toffoli in the paper's convention -----------------------------------
# Paper convention: |0>, |1> are sig_z = -1, +1 eigenstates respectively.
# The stated effective evolution is exp(-i pi (sig_z1+1)(sig_z2+1) sig_x3 / 8).
# (sig_z+1) equals 0 on |0> and 2 on |1>. So the exponent is
#   -i pi (2 c1)(2 c2) sig_x3 / 8 = -i (pi/2) c1 c2 sig_x3
# which flips qubit 3 (up to a phase i) iff both control qubits are |1>.
# The full 8x8 unitary in the standard basis |q1 q2 q3> is
#   Toffoli_paper = exp(-i (pi/2) |11><11|_{12} tensor sig_x3)
#
# Multiplying by a global phase exp(+i pi/4) on the |11> subspace makes it a
# perfect CCNOT with phase +1. We compare to Toffoli_paper directly (any global
# phase on the |11> subspace is exactly what the paper's expression says), and
# separately to the canonical CCNOT.

I2 = qt.qeye(2)
sx = qt.sigmax()
sy = qt.sigmay()
sz = qt.sigmaz()

def _kron(a, b, c):
    return qt.tensor(a, b, c)

# Projectors |1><1| in paper convention (sig_z = +1)
P1 = 0.5 * (qt.qeye(2) + sz)  # |1><1|

# Ideal "paper Toffoli" = exp(-i (pi/2) P1_1 P1_2 sx_3)
_op = (np.pi / 2) * qt.tensor(P1, P1, sx)
U_toffoli_paper = (-1j * _op).expm()  # 8x8 operator

# Canonical CCNOT matrix (for reference)
CCNOT = qt.Qobj(np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,1,0],
], dtype=complex), dims=[[2,2,2],[2,2,2]])


def avg_gate_fidelity_unitary(U, V):
    """Average gate fidelity between two unitaries of equal dim (Nielsen 2002):
        F_avg = (|Tr(U V^dag)|^2 + d) / (d(d+1))
    """
    d = U.shape[0]
    tr = (U * V.dag()).tr()
    return (abs(tr)**2 + d) / (d * (d + 1))


def process_fidelity(U, V):
    """Process (average state) fidelity: |Tr(U V^dag)|^2 / d^2."""
    d = U.shape[0]
    tr = (U * V.dag()).tr()
    return abs(tr)**2 / d**2


# --- Wang-Sorensen-Molmer Hamiltonian ------------------------------------------
def build_hamiltonian(K: int, N_fock: int, Omega: float = 1.0):
    """H (Eq. 5 of quant-ph/0012055) on (qubit x qubit x qubit x oscillator)."""
    a = qt.destroy(N_fock)
    Iq = qt.qeye(2)
    Iosc = qt.qeye(N_fock)
    # x = (a + a^dag)/sqrt(2)
    x = (a + a.dag()) / np.sqrt(2)
    n = a.dag() * a

    sz1 = qt.tensor(sz, Iq, Iq, Iosc)
    sz2 = qt.tensor(Iq, sz, Iq, Iosc)
    sx3 = qt.tensor(Iq, Iq, sx, Iosc)
    I_all = qt.tensor(Iq, Iq, Iq, Iosc)

    X = qt.tensor(Iq, Iq, Iq, x)
    N_op = qt.tensor(Iq, Iq, Iq, n)

    prefactor_A = 1.0 / (4.0 * np.sqrt(K))
    prefactor_C = 1.0 / (32.0 * K)

    A_qubits = prefactor_A * (sz1 + sz2 + I_all)  # (sz1+sz2+1)/(4 sqrt K)
    # H = Omega * [ A_qubits * X  -  sx3 * (N_op + 1/(32K)) ]
    H = Omega * (A_qubits * X - sx3 * (N_op + prefactor_C * I_all))
    return H


def evolve_and_project(K: int, N_fock: int, osc_state="ground"):
    """Simulate for time tau = K*2pi/Omega, then extract the effective 8x8
    qubit unitary conditional on the oscillator returning to its initial
    Fock state |k> (which the paper claims happens exactly).

    Returns
    -------
    dict with keys: U_eff (8x8 Qobj), leakage (1 - trace of qubit reduced density
    starting from equal superposition), F_avg vs U_toffoli_paper, F_avg vs CCNOT.
    """
    Omega = 1.0
    tau = K * 2 * np.pi / Omega
    H = build_hamiltonian(K, N_fock, Omega=Omega)
    U_full = (-1j * H * tau).expm()  # unitary on 8*N_fock dim space

    # Project oscillator onto its initial Fock state |k><k|.
    if osc_state == "ground":
        k = 0
    elif osc_state == "excited1":
        k = 1
    elif osc_state == "excited2":
        k = 2
    else:
        k = 0

    # Build |k><k| on oscillator
    ket_k = qt.basis(N_fock, k)
    # Build 8-dim effective operator U_eff[i,j] = <q_i, k| U_full |q_j, k>
    # Trick: for each basis qubit state |j>, apply U_full to |q_j> tensor |k>,
    # then overlap with |q_i> tensor |k>.
    qubit_dim = 8
    U_eff = np.zeros((qubit_dim, qubit_dim), dtype=complex)
    leakage_probs = []
    for j in range(qubit_dim):
        # decompose j into (b1, b2, b3)
        b1 = (j >> 2) & 1
        b2 = (j >> 1) & 1
        b3 = j & 1
        psi_in = qt.tensor(qt.basis(2, b1), qt.basis(2, b2), qt.basis(2, b3), ket_k)
        psi_out = U_full * psi_in
        # amplitude of oscillator remaining in |k>: <k|_osc psi_out is a 8-dim vec
        # Reshape the full state into (qubit_dim, N_fock) then take column k.
        arr = psi_out.full().reshape(qubit_dim, N_fock)
        col = arr[:, k]  # oscillator-in-|k> component, dim 8
        U_eff[:, j] = col
        # Leakage prob: 1 - |col|^2
        stay = np.sum(np.abs(arr[:, k]) ** 2)
        leakage_probs.append(1.0 - stay)

    U_eff_q = qt.Qobj(U_eff, dims=[[2,2,2],[2,2,2]])

    # Fidelity vs paper's stated ideal
    F_paper = avg_gate_fidelity_unitary(U_eff_q, U_toffoli_paper)
    F_ccnot = avg_gate_fidelity_unitary(U_eff_q, CCNOT)

    # Unitarity of the extracted map (should be near-unitary iff oscillator disentangles)
    UUd = (U_eff_q * U_eff_q.dag()).full()
    unitarity = np.linalg.norm(UUd - np.eye(qubit_dim))

    return {
        "K": K,
        "N_fock": N_fock,
        "osc_state": osc_state,
        "U_eff": U_eff_q,
        "F_avg_vs_paper_Toffoli": float(F_paper),
        "F_avg_vs_CCNOT": float(F_ccnot),
        "unitarity_deviation_frobenius": float(unitarity),
        "max_leakage_prob": float(max(leakage_probs)),
        "mean_leakage_prob": float(np.mean(leakage_probs)),
    }


def qubit_channel_from_thermal(K: int, N_fock: int, n_bar: float):
    """
    Insensitivity-to-oscillator-state test.
    Feed the joint system a product state (qubit maximally-mixed x thermal_osc),
    evolve, trace out oscillator, and compare to the reduced qubit channel that
    the ideal Toffoli would induce. We use process fidelity in the Choi picture.
    """
    Omega = 1.0
    tau = K * 2 * np.pi / Omega
    H = build_hamiltonian(K, N_fock, Omega=Omega)
    U_full = (-1j * H * tau).expm()

    # Thermal state of oscillator (truncated).
    rho_osc = qt.thermal_dm(N_fock, n_bar)

    # Choi matrix of the qubit->qubit channel:
    # Prepare max-entangled pair on aux qubits (|Phi+>) tensor rho_osc; apply I(aux) x U_full;
    # then take partial trace over the oscillator to get an (aux x sys) density on 8x8=64.
    dim_q = 8
    # Full initial state on 8 (aux) x 8 (sys qubits) x N_fock (osc):
    #   rho_init = |Phi+><Phi+|_{aux,sys} tensor rho_osc
    ket_phi = sum(qt.tensor(qt.basis(dim_q, i), qt.basis(dim_q, i)) for i in range(dim_q))
    ket_phi = ket_phi / np.sqrt(dim_q)
    rho_pair = ket_phi * ket_phi.dag()
    # dims trick: reshape via numpy
    rho_pair_arr = rho_pair.full()
    rho_osc_arr = rho_osc.full()

    # We will compute Choi = Tr_osc[ (I_aux tensor U_full) (rho_pair tensor rho_osc) (I_aux tensor U_full^dag) ]
    U_full_arr = U_full.full()

    # Build the full operator directly (small enough: 8*8*N_fock = 8*8*N_fock; for N_fock<=20 fine)
    I_aux = np.eye(dim_q)
    op = np.kron(I_aux, U_full_arr)  # shape (8*8*N_fock, 8*8*N_fock)
    # Initial density
    rho_init = np.kron(rho_pair_arr, rho_osc_arr)
    rho_final = op @ rho_init @ op.conj().T

    # Now trace out the oscillator (last register of dim N_fock).
    # rho_final is on dim_aux (8) * dim_sys (8) * dim_osc (N_fock).
    D = dim_q * dim_q * N_fock
    assert rho_final.shape == (D, D)
    rho_reshape = rho_final.reshape(dim_q, dim_q, N_fock, dim_q, dim_q, N_fock)
    # Trace over N_fock index (positions 2 and 5).
    choi = np.einsum('abcdec->abde', rho_reshape.reshape(dim_q, dim_q, N_fock, dim_q, dim_q, N_fock))
    # Wait we need trace over the two osc indices being equal:
    choi = np.einsum('abkdek->abde', rho_reshape.reshape(dim_q, dim_q, N_fock, dim_q, dim_q, N_fock))
    choi = choi.reshape(dim_q * dim_q, dim_q * dim_q)

    # Ideal Choi from U_toffoli_paper
    U_id = U_toffoli_paper.full()
    ket_phi_id = np.zeros((dim_q * dim_q,), dtype=complex)
    for i in range(dim_q):
        for j in range(dim_q):
            ket_phi_id[i * dim_q + j] = (1/np.sqrt(dim_q)) * U_id[j, i] if i == i else 0
    # Simpler: Choi(U) = (I tensor U) |Phi+><Phi+| (I tensor U^dag)
    ket_phi_ideal = np.zeros((dim_q * dim_q,), dtype=complex)
    for i in range(dim_q):
        e_i = np.zeros(dim_q); e_i[i] = 1.0
        col = U_id @ e_i
        for j in range(dim_q):
            ket_phi_ideal[i * dim_q + j] = (1.0 / np.sqrt(dim_q)) * col[j]
    choi_ideal = np.outer(ket_phi_ideal, ket_phi_ideal.conj())

    # State fidelity between choi and choi_ideal
    # F = (Tr sqrt( sqrt(rho_ideal) rho sqrt(rho_ideal) ))^2 ; but choi_ideal is rank 1,
    # so F = <phi_ideal | choi | phi_ideal>.
    F_state = float(np.real(ket_phi_ideal.conj() @ choi @ ket_phi_ideal))
    # Entanglement fidelity equals Choi state fidelity to |phi_U><phi_U|.
    # Average gate fidelity from entanglement fidelity: F_avg = (d F_e + 1) / (d + 1)
    F_avg = (dim_q * F_state + 1.0) / (dim_q + 1.0)
    return {"n_bar": n_bar, "F_e_choi": F_state, "F_avg_channel": F_avg}


def scan():
    results = {"paper": "quant-ph/0012055",
               "description": "Wang-Sorensen-Molmer single-Hamiltonian Toffoli reproduction",
               "cases": []}

    # Sanity: print target ideals.
    print("Ideal Toffoli (paper convention) trace with CCNOT:",
          (U_toffoli_paper * CCNOT.dag()).tr())
    print("|Ideal Toffoli - CCNOT|_F =",
          np.linalg.norm(U_toffoli_paper.full() - CCNOT.full()))

    # Main scan: several K, several Fock truncations.
    for K in [1, 2, 4]:
        for N_fock in [8, 12, 16, 20]:
            t0 = time.time()
            res = evolve_and_project(K, N_fock, "ground")
            dt = time.time() - t0
            res["wall_seconds"] = dt
            print(f"K={K:2d} N_fock={N_fock:2d} osc=ground  "
                  f"F_paper={res['F_avg_vs_paper_Toffoli']:.6f} "
                  f"F_ccnot={res['F_avg_vs_CCNOT']:.6f} "
                  f"leak_max={res['max_leakage_prob']:.2e} "
                  f"unitarity={res['unitarity_deviation_frobenius']:.2e}  "
                  f"({dt:.2f}s)")
            # Remove non-serializable Qobj before dumping.
            res_pure = {k: v for k, v in res.items() if k != "U_eff"}
            results["cases"].append(res_pure)

    # Insensitivity: run for K=2, N_fock=16, several oscillator states.
    for state in ["ground", "excited1", "excited2"]:
        res = evolve_and_project(2, 16, state)
        res_pure = {k: v for k, v in res.items() if k != "U_eff"}
        results["cases"].append(res_pure)
        print(f"K=2 N_fock=16 osc={state:9s}  "
              f"F_paper={res['F_avg_vs_paper_Toffoli']:.6f}")

    # Thermal insensitivity (channel fidelity)
    thermal_results = []
    for n_bar in [0.0, 0.5, 1.0, 2.0]:
        res = qubit_channel_from_thermal(2, 16, n_bar)
        thermal_results.append(res)
        print(f"THERMAL n_bar={n_bar:.2f}  F_avg_channel={res['F_avg_channel']:.6f}  F_choi={res['F_e_choi']:.6f}")
    results["thermal"] = thermal_results

    # Write outputs
    with open(OUT / "wsm_toffoli_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT/'wsm_toffoli_results.json'}")
    return results


if __name__ == "__main__":
    scan()
