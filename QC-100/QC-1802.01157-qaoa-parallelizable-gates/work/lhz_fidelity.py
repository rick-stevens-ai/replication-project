"""
Reproduce Lechner 2018 Fig. 2(a) qualitative claim:
  Fidelity ordering  F(Uc) >= F(Ub) >= F(Ua) at fixed m and readout count.

We use N=4 => K=6 physical qubits and 3 plaquettes (paper's exact case).
State is simulated as a pure 2^K = 64-dim complex vector (statevector).

Protocols (Eqs. 12-14):
  Ua: (Up . Ux)^m |s>              -- classic QAOA with Up = e^{-i gamma H_p}
  Ub: (Uz . Uc(Omega_fixed) . Ux)^m |s>  -- split local fields (Uz) from
                                            constraints (Uc), both with
                                            same iteration index but separate
                                            angles gamma,Omega,beta
  Uc: (Uz . Uc(Omega, C_l) . Ux)^m |s>   -- same as Ub but constraint strengths
                                            C_l also become free params

For each random instance J_{ij} in {-1,...,1}, we run all 3 protocols
with matched Monte-Carlo budget and compare the achieved
  F = |<psi | phi_0>|^2  (ground-state fidelity of H_p)
where phi_0 is the ground state of the *logical* problem Hamiltonian in
the LHZ physical-qubit basis (projected into the constraint-satisfying
subspace).

For tractable runtime we use L = 20 random instances (paper uses 2000),
M = 400 MC steps each (paper uses 4000). This is enough to show the
qualitative ordering.
"""
import json
import time
import numpy as np
from itertools import combinations


N = 4
K = N * (N - 1) // 2   # 6 physical qubits
DIM = 2 ** K            # 64

# ---- LHZ index conventions ----
def build_lhz():
    """Return: physical qubit list of (i,j), spin index map (i,j) -> q,
    and list of 3 plaquettes (tuples of 4 qubit indices)."""
    idx = {}
    q = 0
    edges = []
    for i in range(1, N + 1):
        for j in range(i + 1, N + 1):
            idx[(i, j)] = q
            edges.append((i, j))
            q += 1
    plaqs = []
    for i in range(1, N - 1):
        for j in range(i + 2, N + 1):
            try:
                w = idx[(i, j - 1)]
                n = idx[(i, j)]
                s = idx[(i + 1, j)]
                e = idx[(i + 1, j - 1)]
                plaqs.append((w, n, s, e))
            except KeyError:
                continue
    return idx, edges, plaqs


IDX, EDGES, PLAQS = build_lhz()
print(f"N={N} K={K} edges={EDGES} plaquettes={PLAQS}")

# Diagonal Z operators (Z eigenvalues +-1) on each qubit, precomputed.
# For each qubit q in [0..K-1], z_diag[q] is a length-DIM array of +-1.
z_diag = np.zeros((K, DIM), dtype=np.float64)
for q in range(K):
    for state in range(DIM):
        bit = (state >> q) & 1
        z_diag[q, state] = 1.0 if bit == 0 else -1.0


# ---- Logical problem Hamiltonian in physical basis ----------------------
#
# Logical spins are s_1..s_N in {+-1}.  Each physical qubit q represents the
# relative orientation z_q = s_i * s_j for the edge (i,j).  Given J_{ij},
# the logical energy is E = sum_{i<j} J_{ij} s_i s_j = sum_q J_q z_q  (LHZ).
# On physical qubits, we set  H_p = sum_q J_q  Z_q     acting only in the
# constraint-satisfying subspace (product of plaquette Z's = +1).

def logical_energy(spins, J):
    E = 0.0
    for (i, j), Jij in J.items():
        E += Jij * spins[i - 1] * spins[j - 1]
    return E


def true_ground_state(J):
    """Enumerate 2^N logical configurations, find the ground state,
    then map it into the physical basis and return
      * ground_state_bitstring (2^N space)
      * physical_state_index (2^K)
      * physical_qubit_z_values ({+-1} per qubit)
    """
    best_E = np.inf
    best_conf = None
    for c in range(2 ** N):
        spins = [1 - 2 * ((c >> k) & 1) for k in range(N)]
        E = logical_energy(spins, J)
        if E < best_E:
            best_E = E
            best_conf = spins
    # Map to physical qubit z values
    phys_z = np.zeros(K)
    for (i, j), q in IDX.items():
        phys_z[q] = best_conf[i - 1] * best_conf[j - 1]
    # Physical state index (bit=0 for z=+1, bit=1 for z=-1)
    phys_state = 0
    for q in range(K):
        if phys_z[q] < 0:
            phys_state |= (1 << q)
    # Note: the logical ground state is 2-fold degenerate (flipping all
    # spins gives the same phys_z since z_q = s_i s_j is invariant).
    return best_E, best_conf, phys_state, phys_z


def hp_diag(J):
    """Diagonal of the LHZ physical H_p = sum_q J_q Z_q  (K local fields)."""
    diag = np.zeros(DIM)
    for (i, j), Jij in J.items():
        q = IDX[(i, j)]
        diag += Jij * z_diag[q]
    return diag


def plaq_diag(l):
    """Diagonal of the plaquette Z_a Z_b Z_c Z_d for plaquette l."""
    a, b, c, d = PLAQS[l]
    return z_diag[a] * z_diag[b] * z_diag[c] * z_diag[d]


# ---- Unitary operators as functions on the statevector ------------------

def apply_diag_phase(psi, diag, angle):
    """Apply e^{-i angle * diag}."""
    return psi * np.exp(-1j * angle * diag)


def apply_ux(psi, beta):
    """Ux(beta) = prod_q e^{-i beta X_q}. Apply as 1-qubit gates.
    e^{-i beta X} = cos(beta) I - i sin(beta) X."""
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    for q in range(K):
        # Reshape as (..., 2, ...) at axis q
        # Split state into halves by bit q
        mask = 1 << q
        idx0 = np.array([i for i in range(DIM) if not (i & mask)])
        idx1 = idx0 ^ mask
        a = psi[idx0].copy()
        b = psi[idx1].copy()
        psi[idx0] = c * a + s * b
        psi[idx1] = c * b + s * a
    return psi


def initial_state():
    """|s> = uniform superposition, +1/sqrt(DIM) in every amplitude."""
    return np.ones(DIM, dtype=np.complex128) / np.sqrt(DIM)


# Precompute the ORIGINAL problem-Hamiltonian diagonal (Ua's Up uses this):
# In protocol Ua, Up = e^{-i gamma H_p_full} where H_p_full includes local
# fields + constraint terms with fixed C_l (paper uses C_l initialized to 2).

def hp_full_diag(J, Cs):
    """Local fields + plaquette constraints."""
    diag = hp_diag(J)
    for l, C in enumerate(Cs):
        diag += C * plaq_diag(l)
    return diag


# ---- Protocols ---------------------------------------------------------

def run_ua(J, betas, gammas, C_fixed):
    """Ua: alternating Up(gamma) Ux(beta) with Up = e^{-i gamma H_p_full}."""
    Hp = hp_full_diag(J, C_fixed)
    psi = initial_state()
    m = len(betas)
    # Paper's Eq 12: Up(gamma_0) Ux(beta_1) Up(gamma_1) ...
    # We follow: [Up(gamma_0); (Ux(beta_k) Up(gamma_k))_{k=1..m-1}]
    psi = apply_diag_phase(psi, Hp, gammas[0])
    for k in range(1, m):
        psi = apply_ux(psi, betas[k])
        psi = apply_diag_phase(psi, Hp, gammas[k])
    return psi


def run_ub(J, betas, gammas, omegas, C_fixed):
    """Ub: Uz(gamma_0) Uc(Omega_0) Ux(beta_1) Uz(gamma_1) Uc(Omega_1) ..."""
    Hz = hp_diag(J)                              # local-field diagonal
    Hcs = [plaq_diag(l) for l in range(len(C_fixed))]
    psi = initial_state()
    m = len(betas)
    # First: Uz(gamma_0) Uc(omega_0)
    psi = apply_diag_phase(psi, Hz, gammas[0])
    for l, C in enumerate(C_fixed):
        psi = apply_diag_phase(psi, C * Hcs[l], omegas[0])
    for k in range(1, m):
        psi = apply_ux(psi, betas[k])
        psi = apply_diag_phase(psi, Hz, gammas[k])
        for l, C in enumerate(C_fixed):
            psi = apply_diag_phase(psi, C * Hcs[l], omegas[k])
    return psi


def run_uc(J, betas, gammas, omegas, Cs_per_iter):
    """Uc: same as Ub but C_l varies per iteration (paper allows it)."""
    Hz = hp_diag(J)
    Hcs = [plaq_diag(l) for l in range(len(Cs_per_iter[0]))]
    psi = initial_state()
    m = len(betas)
    psi = apply_diag_phase(psi, Hz, gammas[0])
    for l, C in enumerate(Cs_per_iter[0]):
        psi = apply_diag_phase(psi, C * Hcs[l], omegas[0])
    for k in range(1, m):
        psi = apply_ux(psi, betas[k])
        psi = apply_diag_phase(psi, Hz, gammas[k])
        for l, C in enumerate(Cs_per_iter[k]):
            psi = apply_diag_phase(psi, C * Hcs[l], omegas[k])
    return psi


# ---- Fidelity ---------------------------------------------------------

def fidelity_to_ground(psi, gnd_phys_state):
    """<psi | phi_0>|^2 where phi_0 = |gnd_phys_state>."""
    return abs(psi[gnd_phys_state]) ** 2


def energy_expectation(psi, Hp_diag_):
    """<psi|H_p|psi> = sum |psi_x|^2 * Hp(x) (Hp is diagonal)."""
    return float(np.sum((np.abs(psi) ** 2) * Hp_diag_).real)


# ---- Monte-Carlo optimizer -----------------------------------------

def mc_optimize(J, protocol, m, M_steps, rng, C_fixed=None):
    """Random-walk MC on parameters, minimizing <H_p> (paper's target)."""
    Cs_init = C_fixed if C_fixed is not None else [2.0] * len(PLAQS)
    Hp_target_diag = hp_full_diag(J, [2.0] * len(PLAQS))  # target uses fixed C=2

    if protocol == "Ua":
        betas = np.ones(m); gammas = np.ones(m); omegas = None
        state = {"betas": betas, "gammas": gammas}
        def apply(state):
            return run_ua(J, state["betas"], state["gammas"], [2.0] * len(PLAQS))
        keys = ["betas", "gammas"]
    elif protocol == "Ub":
        betas = np.ones(m); gammas = np.ones(m); omegas = np.ones(m)
        state = {"betas": betas, "gammas": gammas, "omegas": omegas}
        def apply(state):
            return run_ub(J, state["betas"], state["gammas"], state["omegas"], [2.0] * len(PLAQS))
        keys = ["betas", "gammas", "omegas"]
    else:  # Uc
        betas = np.ones(m); gammas = np.ones(m); omegas = np.ones(m)
        Cs = [[2.0] * len(PLAQS) for _ in range(m)]
        state = {"betas": betas, "gammas": gammas, "omegas": omegas, "Cs": Cs}
        def apply(state):
            return run_uc(J, state["betas"], state["gammas"], state["omegas"], state["Cs"])
        keys = ["betas", "gammas", "omegas", "Cs"]

    psi = apply(state)
    curE = energy_expectation(psi, Hp_target_diag)
    for step in range(M_steps):
        key = rng.choice(keys)
        val = state[key]
        if key == "Cs":
            # 2D: update every 10th step per paper
            if step % 10 != 0:
                continue
            i = rng.integers(m)
            j = rng.integers(len(PLAQS))
            old = val[i][j]
            val[i][j] = old + rng.uniform(-1, 1)
        else:
            i = rng.integers(m)
            old = val[i]
            val[i] = old + rng.uniform(-1, 1)
        psi_new = apply(state)
        newE = energy_expectation(psi_new, Hp_target_diag)
        if newE < curE:
            curE = newE
            psi = psi_new
        else:
            if key == "Cs":
                state[key][i][j] = old
            else:
                state[key][i] = old
    return psi, curE, state


# ---- Main experiment -----------------------------------------

def random_instance(rng):
    J = {}
    for (i, j) in EDGES:
        J[(i, j)] = rng.uniform(-1, 1)
    return J


def run_experiment(L, M, m, seed=42):
    rng = np.random.default_rng(seed)
    results = {"Ua": [], "Ub": [], "Uc": []}
    Fs = {"Ua": [], "Ub": [], "Uc": []}
    Es = {"Ua": [], "Ub": [], "Uc": []}
    t0 = time.time()
    for l in range(L):
        J = random_instance(rng)
        E_gs, conf_gs, phys_state_gs, _ = true_ground_state(J)
        for proto in ["Ua", "Ub", "Uc"]:
            psi, E, _ = mc_optimize(J, proto, m, M, rng)
            F = fidelity_to_ground(psi, phys_state_gs)
            # Include the degenerate all-flipped ground state
            flipped = phys_state_gs   # In LHZ, phys state is same for flipped
            Fs[proto].append(F)
            Es[proto].append(E)
        if l % 5 == 0:
            print(f"  instance {l+1}/{L}  "
                  f"F(Ua)={np.mean(Fs['Ua']):.3f} "
                  f"F(Ub)={np.mean(Fs['Ub']):.3f} "
                  f"F(Uc)={np.mean(Fs['Uc']):.3f}  "
                  f"({time.time()-t0:.1f}s)")
    return Fs, Es


if __name__ == "__main__":
    ALL = {}
    for m in [1, 2, 3]:
        print(f"\n=== m = {m} iteration cycles ===")
        Fs, Es = run_experiment(L=20, M=400, m=m, seed=42 + m)
        row = {
            "m": m,
            "L_instances": 20,
            "M_mc_steps": 400,
            "mean_F": {k: float(np.mean(v)) for k, v in Fs.items()},
            "std_F":  {k: float(np.std(v))  for k, v in Fs.items()},
            "mean_E": {k: float(np.mean(v)) for k, v in Es.items()},
        }
        ALL[str(m)] = row
        print(f"  RESULT m={m}: "
              f"F(Ua)={row['mean_F']['Ua']:.3f}, "
              f"F(Ub)={row['mean_F']['Ub']:.3f}, "
              f"F(Uc)={row['mean_F']['Uc']:.3f}")

    with open("../report/evidence/fidelity_results.json", "w") as f:
        json.dump(ALL, f, indent=2)
    print("\nWrote ../report/evidence/fidelity_results.json")

    # Summary check
    print("\nPaper claim: F(Uc) >= F(Ub) >= F(Ua) for all m")
    print("Our result:")
    for m in [1, 2, 3]:
        r = ALL[str(m)]["mean_F"]
        order = f"F(Uc)={r['Uc']:.3f} vs F(Ub)={r['Ub']:.3f} vs F(Ua)={r['Ua']:.3f}"
        holds_uc_ub = r["Uc"] >= r["Ub"]
        holds_ub_ua = r["Ub"] >= r["Ua"]
        print(f"  m={m}: {order}  "
              f"[Uc>=Ub:{holds_uc_ub}] [Ub>=Ua:{holds_ub_ua}]")
