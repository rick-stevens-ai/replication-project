#!/usr/bin/env python3
"""
Independent replication of arXiv:2304.07917 (Leadbeater et al. 2023)
"Non-unitary Trotter circuits for imaginary time evolution" — Figure 7.

We reproduce the central claim on the 4-site 1D transverse-field Ising model (TIM)
with periodic boundary conditions:

  H = -J * sum_i Z_i Z_{i+1}  -  h * sum_i X_i,   J=0.5, h=0.1,  n=4, PBC

Task:
  (a) Compute exact ground-state energy E_0 via ED.
  (b) Apply "Trotterised" first-order imaginary-time evolution:
        |psi(k+1)> = normalize( exp(-dtau H_local) * ... * |psi(k)> )
      as a product of exp(-dtau * c * P) factors, one per Pauli string in H.
      This is exactly what the paper's block-encoding *post-selects* on the |0>
      ancilla measurement for each Pauli gadget; the block-encoding + successful
      post-selection realizes the non-unitary operator exp(-c*dtau*P) up to the
      known success-probability prefactor.
  (c) Track <E>, |<E>-E_0|, and cumulative probability of "all-|0>" post-selection.
  (d) Compare against paper Figure 7: J=0.5, h=0.1, dtau=0.1, ~40 Trotter steps,
      initial state H^{⊗n}|0..0> = |+>^{⊗n}.
"""
from __future__ import annotations
import json, os, time
import numpy as np
from numpy.linalg import eigh

# --- Pauli matrices ---
I2 = np.eye(2, dtype=complex)
X  = np.array([[0,1],[1,0]], dtype=complex)
Y  = np.array([[0,-1j],[1j,0]], dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)
H1 = (X + Z) / np.sqrt(2)

PAULI = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}

def kron_all(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

def pauli_string(n, sites_ops):
    """Return the 2^n x 2^n operator for a Pauli string.
    sites_ops: dict {site_index: 'X'|'Y'|'Z'}, all others identity."""
    ops = [PAULI['I']] * n
    for s, p in sites_ops.items():
        ops[s] = PAULI[p]
    return kron_all(ops)


def build_tim_hamiltonian(n, J, h, pbc=True):
    """H = -J * sum_i Z_i Z_{i+1}  -  h * sum_i X_i  (PBC if pbc=True)
    Returns:
      H (dense 2^n x 2^n),
      terms = list of (coeff, {site: 'X'|'Z'}) — the Pauli string decomposition.
    """
    dim = 2**n
    H = np.zeros((dim, dim), dtype=complex)
    terms = []
    # ZZ terms
    end = n if pbc else n - 1
    for i in range(end):
        j = (i + 1) % n
        op = pauli_string(n, {i: 'Z', j: 'Z'})
        H += (-J) * op
        terms.append((-J, {i: 'Z', j: 'Z'}))
    # X terms
    for i in range(n):
        op = pauli_string(n, {i: 'X'})
        H += (-h) * op
        terms.append((-h, {i: 'X'}))
    return H, terms


def apply_nonunitary_pauli_expm(psi_normalized, coeff, sites_ops, n, dtau):
    """Apply the non-unitary operator exp(-coeff*dtau * P) to a NORMALIZED psi,
    then renormalize (post-selection on ancilla=|0>), and return
    (psi_new_normalized, success_probability_of_this_gadget).

    The paper's block encoding (Figs. 3-5) implements the operator
       (1/alpha) * exp(-coeff*dtau*P)   with alpha = exp(|coeff|*dtau)
    on the system qubits, conditioned on measuring |0> on the ancilla.
    The per-gadget success probability is
       p_s = || (1/alpha) * exp(-coeff*dtau*P) |psi> ||^2
           = || exp(-coeff*dtau*P) |psi> ||^2 / alpha^2.

    Since P^2 = I for any single Pauli string, exp(-c*dtau*P) has the
    closed form  cosh(c*dtau)*I - sinh(c*dtau)*P.

    NOTE: The physical mid-circuit reset means each gadget starts from the
    (post-selected, renormalized) state produced by the previous gadget. So
    we renormalize here and multiply the p_s's from consecutive gadgets
    to get the cumulative success probability.
    """
    c = coeff
    a = np.cosh(c * dtau)
    b = -np.sinh(c * dtau)
    P = pauli_string(n, sites_ops)
    psi_raw = a * psi_normalized + b * (P @ psi_normalized)
    alpha = np.exp(abs(c) * dtau)
    norm_sq = float(np.vdot(psi_raw, psi_raw).real)
    # psi_normalized is normalized, so ||exp(-c*dt*P) psi||^2 / alpha^2 \in [0,1]
    p_success = norm_sq / (alpha ** 2)
    # Renormalize post-selected state
    psi_new = psi_raw / np.sqrt(norm_sq)
    return psi_new, p_success


def trotter_ite_step(psi_normalized, terms, n, dtau):
    """One first-order Trotter ITE step: apply exp(-c_k*dtau*P_k) for each term,
    with post-selection/renormalization after each gadget.
    Returns (psi_after_step_normalized, cumulative_success_prob_of_this_step)."""
    p_step = 1.0
    psi = psi_normalized
    for coeff, sites_ops in terms:
        psi, ps = apply_nonunitary_pauli_expm(psi, coeff, sites_ops, n, dtau)
        p_step *= ps
    return psi, p_step


def expectation_energy(psi, H):
    nrm = float(np.vdot(psi, psi).real)
    if nrm < 1e-300:
        return float('nan')
    return float((np.vdot(psi, H @ psi).real) / nrm)


def initial_plus_state(n):
    """|+>^{⊗n} = H^{⊗n} |0..0>."""
    return kron_all([np.array([1.0, 1.0], dtype=complex) / np.sqrt(2)] * n)


def run_ite(n, J, h, dtau, n_steps, pbc=True):
    H, terms = build_tim_hamiltonian(n, J, h, pbc=pbc)
    # Exact spectrum
    evals, evecs = eigh(H)
    E0 = float(evals[0])
    E1 = float(evals[1])
    psi = initial_plus_state(n)
    # Normalize (already normalized but be safe)
    psi = psi / np.linalg.norm(psi)
    history = []
    p_cum = 1.0
    E = expectation_energy(psi, H)
    history.append({
        'step': 0, 'beta': 0.0, 'E': E, 'E_minus_E0': E - E0,
        'p_success_step': 1.0, 'p_success_cumulative': p_cum,
    })
    for k in range(1, n_steps + 1):
        psi, p_step = trotter_ite_step(psi, terms, n, dtau)
        p_cum *= p_step
        E = expectation_energy(psi, H)
        history.append({
            'step': k, 'beta': k * dtau, 'E': E, 'E_minus_E0': E - E0,
            'p_success_step': p_step, 'p_success_cumulative': p_cum,
        })
    return {
        'n': n, 'J': J, 'h': h, 'dtau': dtau, 'n_steps': n_steps, 'pbc': pbc,
        'E0_exact': E0, 'E1_exact': E1, 'gap': E1 - E0,
        'history': history,
        'all_eigenvalues': evals.tolist(),
    }


def main():
    out_dir = os.environ.get('OUT_DIR', '.')
    os.makedirs(out_dir, exist_ok=True)

    # ==== Paper Figure 7 parameters ====
    n = 4
    J = 0.5
    h = 0.1
    dtau = 0.1
    n_steps = 45  # paper x-axis goes to ~40-45

    t0 = time.time()
    res = run_ite(n, J, h, dtau, n_steps, pbc=True)
    elapsed = time.time() - t0

    E0 = res['E0_exact']
    E_last = res['history'][-1]['E']
    dE_last = abs(E_last - E0)
    p_cum_last = res['history'][-1]['p_success_cumulative']

    # Also do a second run at different dtau to demonstrate convergence robustness
    print(f"# 4-site TIM, J={J}, h={h}, PBC, dtau={dtau}, {n_steps} Trotter steps")
    print(f"# Exact E0 = {E0:.10f}")
    print(f"# Exact E1 = {res['E1_exact']:.10f}")
    print(f"# Gap E1-E0 = {res['gap']:.10f}")
    print(f"# Runtime: {elapsed:.3f}s")
    print()
    print("step   beta    <E>            <E>-E0          p_step         p_cumulative")
    for h_row in res['history'][::5] + [res['history'][-1]]:
        print(f"{h_row['step']:4d}  {h_row['beta']:5.2f}  {h_row['E']:+.8f}  {h_row['E_minus_E0']:+.4e}  {h_row['p_success_step']:.6e}  {h_row['p_success_cumulative']:.6e}")

    # Save JSON
    with open(os.path.join(out_dir, 'ite_tim_result.json'), 'w') as f:
        json.dump(res, f, indent=2)

    # Save CSV
    with open(os.path.join(out_dir, 'ite_tim_history.csv'), 'w') as f:
        f.write("step,beta,E,E_minus_E0,p_success_step,p_success_cumulative\n")
        for r in res['history']:
            f.write(f"{r['step']},{r['beta']},{r['E']},{r['E_minus_E0']},{r['p_success_step']},{r['p_success_cumulative']}\n")

    # ---- Verdict summary ----
    # Paper Figure 7 (visual): by ~40 Trotter steps, |<E>-E0| < ~1e-2 (curve reaches
    # the lower part of the log plot ~10^-3), and cumulative success probability
    # is ~10^-3 to 10^-4.
    summary = {
        'model': f'{n}-site 1D TIM, PBC',
        'params': {'J': J, 'h': h, 'dtau': dtau, 'n_steps': n_steps},
        'E0_exact_ED': E0,
        'E_ITE_final': E_last,
        'abs_error_final': dE_last,
        'p_success_cumulative_final': p_cum_last,
        'converged_within_1e-2': bool(dE_last < 1e-2),
        'converged_within_1e-3': bool(dE_last < 1e-3),
        'runtime_seconds': elapsed,
    }
    with open(os.path.join(out_dir, 'ite_tim_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print()
    print("SUMMARY:")
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
