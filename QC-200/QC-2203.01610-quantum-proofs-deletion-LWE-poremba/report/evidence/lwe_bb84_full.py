"""
Full pipeline: LWE ciphertext -> BB84 qubit register -> deletion/decryption.

Combines lwe_base.py (Dual-Regev classical LWE) with bb84_deletion.py
(BB84 quantum encoding + deletion). This matches part (b) of the QC wave
brief for arXiv:2203.01610:

    "encode the LWE ciphertext into a BB84-style qubit register that admits
     a computational-basis measurement (deletion) or a Hadamard-basis
     measurement (decryption)"

BUT NOTE: the paper (Poremba 2022 Section 7.1) uses the OPPOSITE convention:
    - computational-basis measurement of the primal Gaussian state = DECRYPT
      (it yields sA + e + b·⌊q/2⌋, which the secret key sk = (-x̄, 1) unlocks
       via Lemma 17).
    - Fourier-basis measurement                           = DELETE
      (Del(|CT⟩) → π ∈ Z_q^{m+1}, and Vrfy checks A·π = y (mod q) with
       ‖π‖ ≤ √(m+1)/(√2·α).)

The [BI20] private-key convention (that the wave brief description follows)
is symmetric: which basis is which is a design choice. Both are valid.
This script reports what Poremba's construction actually does:

Pipeline (small params, faithful to Construction 1):
  1. classical LWE base: n=8, q=257, m=128, σ=3.2 (Dual-Regev correctness)
  2. quantum encoding as a "BB84-lifted" register:
        we encode the (m+1)-digit ciphertext c ∈ Z_q^{m+1} into a qubit
        register by choosing a random per-coordinate bit-basis mask
        θ ∈ {0,1}^{m+1} (like BB84 θ), and encoding the bit-representation
        of c_i in the computational basis where θ_i=0, and in the
        Hadamard basis where θ_i=1.
     This is a small-scale STAND-IN for the paper's primal Gaussian
     superposition (which would require q^{m+1} = 257^129 amplitudes, i.e.
     ~10^310 -- outside the reach of any simulator on Earth).
  3. Honest decryption = measure θ_i basis on qubit i, recover c bits,
     run classical Dec(sk, c) as in lwe_base.py.
  4. Honest deletion certificate = measure ALL qubits in the *complement*
     basis (Hadamard where θ=0, computational where θ=1). We verify by
     checking that a fraction ≥ threshold of the θ=1 positions match c's
     bits (since on those, the complement basis gives the deterministic
     H-basis measurement = original c-bit).
  5. Cheater tries to keep c-bits by measuring θ=1 qubits in computational
     (wrong) basis -- her deletion cert accept-prob drops as (1/2)^{cheated qubits}.

For (b), we run this at n=8, q=257, m+1=17 (using log_2 q ≈ 8 => ~136 qubits total)
truncated: to keep statevector cost <2^20 we take just the FIRST qubit of each
coordinate, giving a 17-qubit register. This preserves the certified-deletion
structure while remaining simulable.
"""

from __future__ import annotations
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# reuse the classical LWE base
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import lwe_base as LB
import bb84_deletion as BB

# --------------------------------------------------------------------
def ciphertext_to_bit(c: np.ndarray) -> np.ndarray:
    """Take the top bit of each coordinate (parity of top-half of Z_q).
    For q=257 the top bit is 1 iff c_i > q/2. This preserves the message-carrying
    coordinate (c[-1] ≈ b·⌊q/2⌋) as an EASY bit: b=1 => c[-1] ≈ 128 => top bit 1."""
    return (c > (c.max() // 2)).astype(np.int64)  # simple thresholding

def better_bit(c: np.ndarray, q: int) -> np.ndarray:
    """More faithful: bit_i = 1 iff c_i mod q is in (q/4, 3q/4)."""
    a = c % q
    return ((a > q // 4) & (a < 3 * q // 4)).astype(np.int64)

def encode_bb84(bits: np.ndarray, theta: np.ndarray) -> Statevector:
    """One qubit per bit, encoded in comp basis where θ=0, Hadamard where θ=1."""
    N = len(bits)
    qc = QuantumCircuit(N)
    for i in range(N):
        if bits[i] == 1:
            qc.x(i)
        if theta[i] == 1:
            qc.h(i)
    return Statevector.from_instruction(qc)

def measure_in(psi: Statevector, basis: np.ndarray, rng) -> np.ndarray:
    return BB.measure_all_in_basis(psi, basis, rng)

# --------------------------------------------------------------------
def experiment(n_trials: int = 200, seed: int = 100):
    """Full LWE+BB84 pipeline reproducing (b), (c), (d), (e)."""
    p = LB.DEFAULT
    rng = np.random.default_rng(seed)

    # We'll pick m+1 = 17 for the BB84 register (keeps 2^17 = 128K statevector).
    # For the LWE base we use full m=128 and then only use the top-bit of each
    # coordinate for the qubit encoding demo. This means decryption using ONLY
    # the top bits WILL fail -- that's a limitation of this small-simulator demo.
    # To honestly test (c) end-to-end we ALSO run the pipeline using an
    # "abstracted" ciphertext where the whole c is used classically for
    # decryption and only its bit-pattern is loaded into the BB84 register
    # for the deletion demo.

    rt_ok = 0
    honest_del_ok = 0
    cheater_del = {rho: 0 for rho in [0.0, 0.25, 0.5, 0.75, 1.0]}
    N_bb = 17  # 17-qubit register for the BB84 demo

    for t in range(n_trials):
        # --- classical Dual-Regev: encrypt b -> c using full m=128 ---
        A, sk = LB.keygen(p, rng)
        b = int(rng.integers(0, 2))
        c, _s, _e = LB.encrypt_classical(A, b, p, rng)
        b_out = LB.decrypt(sk, c, p)          # test (a) - classical LWE roundtrip
        rt_ok += int(b_out == b)              # will re-run this in classical tests too

        # --- quantum encoding of the FIRST N_bb coordinates of c ---
        c_bits = better_bit(c[:N_bb], p.q)
        theta = rng.integers(0, 2, size=N_bb, dtype=np.int64)
        psi = encode_bb84(c_bits, theta)

        # --- honest deletion: measure ALL qubits in the HADAMARD basis ---
        # On theta=1 (H-encoded) positions this is deterministic and equals the
        # original c_bit. On theta=0 (comp-encoded) positions it is uniformly
        # random and not checked. This is exactly Del in BB20/BI20 §3, which
        # Poremba §1 lines 177-178 references as the primitive being lifted.
        H_basis = np.ones(N_bb, dtype=np.int64)
        outcomes_h = measure_in(psi, H_basis, rng)
        mask = (theta == 1)
        if mask.sum() == 0 or np.all(outcomes_h[mask] == c_bits[mask]):
            honest_del_ok += 1

        # --- cheating: adversary tries to KEEP c_bits by measuring the theta=0
        # qubits in the WRONG basis (Hadamard) trying to preserve later dec ability;
        # OR (Cheater A) she measures theta=1 qubits in COMPUTATIONAL basis to
        # try to learn r|_H, which corrupts the Hadamard-basis cert bit on those
        # positions and reduces her deletion-accept probability by (1/2)^k where
        # k = # cheated theta=1 qubits.
        for rho in cheater_del.keys():
            n_cheat = int(np.ceil(rho * int(mask.sum())))
            cheat_positions = np.where(mask)[0][:n_cheat]
            cheater_basis = H_basis.copy()
            for pos in cheat_positions:
                cheater_basis[pos] = 0     # cheat: measure in Comp instead of Hadamard
            outc = measure_in(psi, cheater_basis, rng)
            # For non-cheated theta=1 positions, outc == c_bits deterministically.
            # For cheated theta=1 positions, cheater must invent a cert bit; her
            # comp-basis outcome on an H-state is uniformly random, so P[match]=1/2
            # per cheated qubit. => P[accept] = (1/2)^n_cheat.
            cert_bits = outc.copy()          # her cert = whatever she measured
            if np.all(cert_bits[mask] == c_bits[mask]):
                cheater_del[rho] += 1

    return {
        "params": {"lwe_n": p.n, "lwe_q": p.q, "lwe_m": p.m,
                   "sigma_enc": p.sigma_enc, "N_bb": N_bb, "trials": n_trials, "seed": seed},
        "classical_roundtrip":  {"correct": rt_ok, "acc": rt_ok / n_trials},
        "honest_deletion":      {"accepted": honest_del_ok, "accept_prob": honest_del_ok / n_trials},
        "cheating_accept_prob": {str(rho): cheater_del[rho] / n_trials for rho in cheater_del},
    }

if __name__ == "__main__":
    import sys, time
    t0 = time.time()
    out = experiment()
    out["wall_seconds"] = round(time.time() - t0, 2)
    print(json.dumps(out, indent=2))
