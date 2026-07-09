#!/usr/bin/env python3
"""
Independent reproduction of the three-qubit perturbation gadget from
Kempe, Kitaev, Regev, "The Complexity of the Local Hamiltonian Problem"
(arXiv:quant-ph/0406180), Section 6.2.

CENTRAL CLAIM WE REPRODUCE (Eq. 14 in the paper):
    ~H = H + V   built from Y (2-local) and B1, B2, B3 (single-qubit, PSD)
    with H a mediator-qubit penalty of gap Delta = delta^{-3}
    and V a specific 2-local coupling on data-plus-mediator qubits.

    Then the lowest eigenvalue of ~H is O(delta)-close to the lowest
    eigenvalue of the 3-local target
        H_target = Y - 6 B1 B2 B3.
    More precisely, restricted to the low-lying subspace M ⊗ C
    (C = span{|000>_m, |111>_m}) the effective Hamiltonian is
        Heff = Y ⊗ I_C  -  6 B1 B2 B3 ⊗ sigma_eff^x + O(delta),
    where sigma_eff^x flips between |000>_m and |111>_m.

    The ground state of Heff lives in the |+>_eff := (|000>+|111>)/sqrt(2)
    subspace, on which Heff acts as (Y - 6 B1 B2 B3), exactly H_target.

METHOD: exact dense diagonalization with numpy.linalg.eigh on
n_data = 3 data qubits + 3 mediator qubits (Hilbert dim = 2^6 = 64).

OUTPUTS in this directory:
    results.json  — machine-readable eigenvalues, errors, log-log fit
    scaling.csv   — Delta vs |E_gadget_low - E_target_low|
    scaling.png   — log-log plot of error vs Delta (if matplotlib available)
"""
import json, csv, os, sys
import numpy as np
from numpy.linalg import eigh

# ---------- basic operators ----------
I2 = np.eye(2)
Z  = np.array([[1, 0], [0, -1]], dtype=complex)
X  = np.array([[0, 1], [1,  0]], dtype=complex)

def kron_list(ops):
    out = np.array([[1.0+0j]])
    for op in ops:
        out = np.kron(out, op)
    return out

def op_on(N, site, op):
    ops = [I2] * N
    ops[site] = op
    return kron_list(ops)

def op_on_two(N, s1, op1, s2, op2):
    ops = [I2] * N
    ops[s1] = op1
    ops[s2] = op2
    return kron_list(ops)


# ---------- target 3-local Hamiltonian ----------
def build_target(n_data, seed=0):
    """
    H_target = Y_2loc  -  6 * B1 B2 B3,   on n_data qubits.
      Y_2loc: fixed random 2-local (ZZ, XX, Z, X) Hamiltonian
      B_j = |0><0|_{b_j} = (I + Z_{b_j})/2  (PSD, ||B||=1)
    Returns (H_target, Y_2loc, B_ops, coeffs, b_qubits).
    """
    if n_data < 3:
        raise ValueError("Need n_data >= 3 for a genuine 3-local target term")
    rng = np.random.default_rng(seed)
    coeffs = {
        'zz': rng.uniform(-0.5, 0.5, size=(n_data, n_data)),
        'xx': rng.uniform(-0.3, 0.3, size=(n_data, n_data)),
        'z':  rng.uniform(-0.2, 0.2, size=n_data),
        'x':  rng.uniform(-0.2, 0.2, size=n_data),
    }
    Y_2loc = np.zeros((2**n_data, 2**n_data), dtype=complex)
    for i in range(n_data):
        Y_2loc += coeffs['z'][i] * op_on(n_data, i, Z)
        Y_2loc += coeffs['x'][i] * op_on(n_data, i, X)
        for j in range(i+1, n_data):
            Y_2loc += coeffs['zz'][i,j] * op_on_two(n_data, i, Z, j, Z)
            Y_2loc += coeffs['xx'][i,j] * op_on_two(n_data, i, X, j, X)

    b_qubits = [0, 1, 2]
    B = [(op_on(n_data, q, I2) + op_on(n_data, q, Z)) / 2.0 for q in b_qubits]
    triple = B[0] @ B[1] @ B[2]
    H_target = Y_2loc - 6.0 * triple
    return H_target, Y_2loc, B, coeffs, b_qubits


# ---------- gadget 2-local Hamiltonian ----------
def build_gadget(n_data, Y_2loc, B_ops, b_qubits, delta):
    """
    Build 2-local gadget ~H on N = n_data + 3 qubits.
    Mediator qubits: indices n_data, n_data+1, n_data+2.
    Delta := delta^{-3}.
    """
    N = n_data + 3
    m1, m2, m3 = n_data, n_data + 1, n_data + 2
    Delta = delta**(-3)

    # H: penalty on mediators, projecting onto C = span{|000>_m, |111>_m}
    ZZ12 = op_on_two(N, m1, Z, m2, Z)
    ZZ13 = op_on_two(N, m1, Z, m3, Z)
    ZZ23 = op_on_two(N, m2, Z, m3, Z)
    I_N  = np.eye(2**N, dtype=complex)
    H_pen = -(Delta / 4.0) * (ZZ12 + ZZ13 + ZZ23 - 3.0 * I_N)

    # V = X ⊗ I_m  -  delta^{-2} sum_j B_j ⊗ sigma^x_{m_j}
    # where X = Y + delta^{-1}(B1^2 + B2^2 + B3^2), acting on data register.
    B_sq_sum = sum(Bi @ Bi for Bi in B_ops)
    X_op = Y_2loc + (1.0/delta) * B_sq_sum

    dim_med = 2**3
    def embed_data(op_data):
        return np.kron(op_data, np.eye(dim_med, dtype=complex))

    V = embed_data(X_op)
    for j, Bj in enumerate(B_ops):
        med_site = [m1, m2, m3][j]
        sx_med = op_on(N, med_site, X)
        Bj_full = embed_data(Bj)
        V += -(delta**(-2)) * (Bj_full @ sx_med)

    H_full = H_pen + V
    return H_full, H_pen, V, Delta


# ---------- effective-qubit projectors ----------
def C_projectors(n_data):
    """
    Return P_plus, P_minus: projectors onto |+>_eff := (|000>+|111>)/sqrt2
    and |->_eff := (|000>-|111>)/sqrt2 on the 3-mediator subspace, extended
    to identity on the n_data data qubits.
    Convention: total qubit order is [data qubits ... mediators],
    so total dim = 2^n_data * 8.
    """
    dim_data = 2**n_data
    m000 = np.zeros(8, dtype=complex); m000[0] = 1.0     # index 0 = |000>
    m111 = np.zeros(8, dtype=complex); m111[7] = 1.0     # index 7 = |111>
    m_plus  = (m000 + m111) / np.sqrt(2)
    m_minus = (m000 - m111) / np.sqrt(2)
    P_plus_med  = np.outer(m_plus,  m_plus.conj())
    P_minus_med = np.outer(m_minus, m_minus.conj())
    I_data = np.eye(dim_data, dtype=complex)
    return np.kron(I_data, P_plus_med), np.kron(I_data, P_minus_med)


def project_low_subspace_energy(H_full, n_data):
    """
    Diagonalize H_full and return the ground-state energy of the low-lying
    subspace corresponding to |+>_eff — the subspace whose effective
    Hamiltonian equals H_target.

    We do it by (a) computing the full spectrum, (b) picking eigenstates
    whose overlap with the C = span{|000>,|111>} mediator subspace is high
    (weight > 0.5), and (c) further separating |+>_eff vs |->_eff via
    the sign of the amplitude ratio on |000> vs |111>.
    """
    ev, vec = eigh(H_full)
    dim_data = 2**n_data
    # projector onto C = M ⊗ span{|000>, |111>}
    P_plus, P_minus = C_projectors(n_data)
    P_C = P_plus + P_minus

    low_plus_energies = []
    low_minus_energies = []
    for i in range(len(ev)):
        v = vec[:, i]
        w_C = float(np.real(v.conj() @ P_C @ v))
        if w_C < 0.5:
            continue  # this eigenstate lives mostly outside C (excited manifold)
        w_p = float(np.real(v.conj() @ P_plus  @ v))
        w_m = float(np.real(v.conj() @ P_minus @ v))
        if w_p > w_m:
            low_plus_energies.append((ev[i], w_C, w_p))
        else:
            low_minus_energies.append((ev[i], w_C, w_m))

    low_plus_energies.sort(key=lambda t: t[0])
    low_minus_energies.sort(key=lambda t: t[0])
    return ev, low_plus_energies, low_minus_energies


# ---------- main ----------
def main():
    n_data = 3
    H_target, Y_2loc, B_ops, coeffs, b_qubits = build_target(n_data, seed=0)
    E_target = np.sort(eigh(H_target)[0])
    print(f"n_data = {n_data}")
    print(f"H_target dim = {H_target.shape}")
    print(f"H_target lowest 4 eigs = {E_target[:4]}")
    print(f"H_target promise gap (E1-E0) = {E_target[1]-E_target[0]:.4f}")

    # Reasonable Delta sweep. Very large Delta makes eigh ill-conditioned
    # (spectrum spans ~ Delta), so stop at ~ 1e6.
    Delta_targets = [5.0, 10.0, 50.0, 200.0, 500.0, 1000.0, 5000.0,
                     20000.0, 100000.0, 500000.0]

    rows = []
    for Delta_req in Delta_targets:
        delta = Delta_req**(-1.0/3.0)
        H_full, H_pen, V, Delta_actual = build_gadget(
            n_data, Y_2loc, B_ops, b_qubits, delta)

        ev, low_plus, low_minus = project_low_subspace_energy(H_full, n_data)

        # Number of paired levels expected: |+>_eff sector has 2^n_data levels,
        # |->_eff sector has 2^n_data levels.  Compare the |+>_eff spectrum
        # to H_target's spectrum.
        E_plus_low  = np.array([t[0] for t in low_plus])
        E_minus_low = np.array([t[0] for t in low_minus])

        # If we didn't cleanly separate, fall back to naive ground state
        k = 2**n_data
        if len(E_plus_low) < 1:
            # fallback: cannot reproduce |+>_eff cleanly
            E_gs_plus_est = float(np.sort(ev)[0])
            plus_ok = False
        else:
            E_gs_plus_est = float(E_plus_low[0])
            plus_ok = True

        err_gs = abs(E_gs_plus_est - E_target[0])

        # Also compare full |+>_eff sector to H_target
        n_matched = min(len(E_plus_low), k)
        E_plus_matched = E_plus_low[:n_matched]
        E_target_matched = E_target[:n_matched]
        elem_err = np.abs(E_plus_matched - E_target_matched).tolist()

        # First-gap error inside |+>_eff sector
        if n_matched >= 2:
            gap_gadget = float(E_plus_low[1] - E_plus_low[0])
            gap_target = float(E_target[1] - E_target[0])
            err_gap = abs(gap_gadget - gap_target)
        else:
            err_gap = float('nan')

        rows.append({
            'Delta_requested': float(Delta_req),
            'delta':           float(delta),
            'Delta_actual':    float(Delta_actual),
            'plus_sector_recovered': plus_ok,
            'n_plus_states_found':   len(E_plus_low),
            'n_minus_states_found':  len(E_minus_low),
            'E_target_low4':   E_target[:4].tolist(),
            'E_gadget_plus_low4': E_plus_low[:4].tolist(),
            'E_gadget_minus_low4': E_minus_low[:4].tolist(),
            'err_groundstate_plus_sector': float(err_gs),
            'err_first_gap_plus_sector':   float(err_gap),
            'elementwise_low_errs_plus_sector': elem_err,
        })
        print(f"Delta={Delta_req:8.1f}  delta={delta:.4f}  "
              f"|E0_+ - E0_target| = {err_gs:.4e}  "
              f"|Δgap+| = {err_gap:.4e}  "
              f"(n_+={len(E_plus_low)},n_-={len(E_minus_low)})")

    # ---------- log-log scaling fit ----------
    # Paper predicts error ~ O(delta) = O(Delta^{-1/3}) per Eq. 14 remainder.
    Deltas = np.array([r['Delta_requested'] for r in rows])
    errs   = np.array([r['err_groundstate_plus_sector'] for r in rows])
    mask   = (Deltas >= 200.0) & (Deltas <= 100000.0)
    if mask.sum() >= 2:
        logD = np.log(Deltas[mask])
        logE = np.log(errs[mask])
        slope, intercept = np.polyfit(logD, logE, 1)
        # convert to delta scaling: err ~ delta^p  where delta ~ Delta^{-1/3}
        # slope_D * (-3) = slope_delta
        slope_delta = -3.0 * slope
        fit = {'slope_vs_Delta':  float(slope),
               'slope_vs_delta':  float(slope_delta),
               'intercept':       float(intercept),
               'note': ('err ~ Delta^{slope_vs_Delta} = delta^{slope_vs_delta}; '
                        'paper predicts slope_vs_delta = +1 (O(delta)), '
                        'equivalently slope_vs_Delta = -1/3.')}
    else:
        fit = None
    print("\nlog-log fit (asymptotic, 200 <= Delta <= 100000):")
    print(fit)

    # ---------- Promise-gap preservation ----------
    # For a QMA-style promise, we check that the |+>_eff sector's low-two
    # eigenvalue gap matches H_target's gap within tolerance ~ err_gap.
    # (Formal Def. 3 of the paper: promise gap b-a = poly(1/n).)
    print("\nPromise-gap preservation check:")
    for r in rows:
        print(f"  Delta={r['Delta_requested']:8.1f}  "
              f"gap_target={E_target[1]-E_target[0]:.4f}  "
              f"gadget_gap={r['E_gadget_plus_low4'][1]-r['E_gadget_plus_low4'][0]:.4f}  "
              f"err_gap={r['err_first_gap_plus_sector']:.4e}")

    results = {
        'paper':     'arXiv:quant-ph/0406180',
        'authors':   'Julia Kempe, Alexei Kitaev, Oded Regev',
        'section':   '6.2 (Three-Qubit Gadget)',
        'n_data':    n_data,
        'total_qubits': n_data + 3,
        'hilbert_dim':  2 ** (n_data + 3),
        'gadget_form': ('H = -(delta^{-3}/4)(ZZ12 + ZZ13 + ZZ23 - 3I); '
                        'V = X ⊗ I - delta^{-2}(B1 ⊗ sigma^x_1 + B2 ⊗ sigma^x_2 '
                        '+ B3 ⊗ sigma^x_3); X = Y + delta^{-1}(B1^2 + B2^2 + B3^2); '
                        'H_target = Y - 6 B1 B2 B3'),
        'Delta_relation':   'Delta = delta^{-3}',
        'B_operators':      'B_j = (I + Z_{b_j})/2 = |0><0|_{b_j},  b_j = 0,1,2',
        'Y_2loc_coeffs_seed': 0,
        'rows':      rows,
        'loglog_fit_ground_state_error_vs_Delta_asymptotic': fit,
        'expected_scaling_paper': (
            'ground-state error ~ O(delta) = O(Delta^{-1/3}) per Eq. (14)'),
        'notes': [
            'Task brief mentioned O(V^3/Delta^2) scaling; the paper actually '
            'predicts O(delta) = O(Delta^{-1/3}) for the residual after the '
            'X = Y + delta^{-1} sum(B^2) counter-term is included.',
            'The gadget has TWO low sectors: |+>_eff maps to H_target (Y-6B1B2B3), '
            '|->_eff maps to Y+6B1B2B3.  Ground state lives in |+>_eff.',
        ],
    }

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(outdir, 'scaling.csv'), 'w') as f:
        w = csv.writer(f)
        w.writerow(['Delta', 'delta', 'err_groundstate_plus_sector',
                    'err_first_gap_plus_sector'])
        for r in rows:
            w.writerow([r['Delta_requested'], r['delta'],
                        r['err_groundstate_plus_sector'],
                        r['err_first_gap_plus_sector']])
    print(f"\nWrote {outdir}/results.json and scaling.csv")

    # ---------- plot ----------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.loglog(Deltas, errs, 'o-', color='C0', label='|E0_gadget - E0_target|')
        # Overlay the paper's O(delta) = O(Delta^{-1/3}) prediction line
        Dref, eref = Deltas[len(Deltas)//2], errs[len(Deltas)//2]
        ax.loglog(Deltas, eref * (Dref / Deltas)**(1/3),
                  '--', color='k', alpha=0.6,
                  label=r'O(δ)=O(Δ$^{-1/3}$) (paper Eq. 14)')
        ax.set_xlabel('Δ (penalty scale)')
        ax.set_ylabel('|E₀(H_gadget, |+⟩_eff) − E₀(H_target)|')
        ax.set_title('Kempe-Kitaev-Regev 3→2-local gadget: ground-state error')
        ax.legend()
        ax.grid(True, which='both', ls=':', alpha=0.5)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, 'scaling.png'), dpi=150)
        print(f"Wrote {outdir}/scaling.png")
    except Exception as e:
        print(f"(matplotlib skipped: {e})")


if __name__ == '__main__':
    main()
