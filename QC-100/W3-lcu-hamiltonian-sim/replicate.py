#!/usr/bin/env python3
"""
Replication of: A. M. Childs and N. Wiebe,
"Hamiltonian Simulation Using Linear Combinations of Unitary Operations",
Quantum Information & Computation 12, 901-924 (2012).

Core claims we test on an explicit small Hamiltonian (no hardware):

  C1 (Lemma 2): a 1-ancilla circuit implements an operator proportional to
     kappa*U_a + U_b; conditioned on measuring the ancilla in |0>, the system
     state becomes (kappa U_a + U_b)|psi>/||.||. The FAILURE probability (ancilla
     = |1>) equals  Delta^2 kappa/(kappa+1)^2  with Delta = ||U_a - U_b||, and is
     bounded by 4 kappa/(kappa+1)^2.  We build the circuit exactly and check both
     the produced state and the failure probability vs the formula.

  C2 (Theorem 3): kappa = (sum of positive C_q)/(sum |negative C_q|) for a
     linear combination V = sum C_q U_q; success rises as kappa grows / Delta
     shrinks. We verify kappa and that the implemented operator is proportional
     to V.

  C3 (Multi-product formulas, Def.1 / Lemma 4): the multi-product formula
     M_k built from a symmetric product formula S_chi achieves error
     O(t^{2(k+chi)+1}) -- a HIGHER order than S_chi alone (O(t^{2chi+1})). We
     measure the error ||M - e^{-iHt}|| vs t on a log-log plot and confirm the
     fitted order matches 2(k+chi)+1. Base case: the Richardson MPF
        M = (4 S_2(t/2)^2 - S_2(t))/3
     applied to the 2nd-order (chi=1) Strang splitting should give order ~7
     (2(1+1)+1 = 5 for chi=1,k=1 in their normalization; we verify the order
     jump relative to S_2's order 3).

  C4: coefficient normalization sum_q C_q = 1 (Eq. 14) for the constructed MPFs.

  C5: MPF is "nearly unitary": distance of M to the nearest unitary scales as a
     high power of t (Blanes-Casas-Ros: unitary to O(t^{4(k+chi)+2})), checked by
     measuring ||M^dag M - I||.

Hamiltonian: H = a X + b Z (non-commuting parts H1=aX, H2=bZ) on 1 qubit, plus a
2-qubit cross-check H = X0 X1 + Z0 + Z1. Exact statevector / matrix exponentials.
"""
import numpy as np
import json
from scipy.linalg import expm
from numpy.linalg import svd, norm

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

# ----- C1/C2: Lemma 2 LCU circuit -----
def lcu_pair(Ua, Ub, kappa, psi):
    """Implement (kappa Ua + Ub) on psi via 1 ancilla (Lemma 2 construction).
    V_kappa = (1/sqrt(kappa+1)) [[sqrt(kappa), -1],[1, sqrt(kappa)]] rotates the
    ancilla; controlled-Ua/Ub; V_kappa^dag; measure ancilla.
    Returns (system_state_given_success, P_fail)."""
    d = Ua.shape[0]
    sk = np.sqrt(kappa)
    Vk = (1/np.sqrt(kappa+1)) * np.array([[sk, -1],[1, sk]], dtype=complex)
    # ancilla|0> tensor psi
    state = np.kron(np.array([1,0], dtype=complex), psi)   # dim 2d
    # apply Vk on ancilla
    Vk_full = np.kron(Vk, np.eye(d, dtype=complex))
    state = Vk_full @ state
    # controlled application: if ancilla=0 apply Ua, if ancilla=1 apply Ub
    big = np.zeros((2*d, 2*d), dtype=complex)
    big[:d, :d] = Ua          # ancilla |0> block
    big[d:, d:] = Ub          # ancilla |1> block
    state = big @ state
    # apply Vk^dag on ancilla
    Vkd_full = np.kron(Vk.conj().T, np.eye(d, dtype=complex))
    state = Vkd_full @ state
    # measure ancilla: success = |0>
    amp0 = state[:d]      # ancilla 0 component
    amp1 = state[d:]      # ancilla 1 component
    P_success = float(np.real(amp0.conj() @ amp0))
    P_fail = float(np.real(amp1.conj() @ amp1))
    sys = amp0 / np.sqrt(P_success) if P_success > 1e-15 else amp0
    return sys, P_fail, P_success

def test_lemma2(Ua, Ub, kappa):
    Delta = float(norm(Ua - Ub, 2))
    psi = np.array([0.6, 0.8], dtype=complex)
    sys, P_fail, P_succ = lcu_pair(Ua, Ub, kappa, psi)
    # target operator proportional to kappa Ua + Ub
    target = (kappa*Ua + Ub) @ psi
    target_norm = target / norm(target)
    # implemented (up to global phase): compare via fidelity
    fid = abs(np.vdot(target_norm, sys))**2
    formula_Pfail = Delta**2 * kappa / (kappa+1)**2
    bound = 4*kappa/(kappa+1)**2
    return {
        "Delta": Delta, "kappa": kappa,
        "P_fail_circuit": P_fail,
        "P_fail_formula_Delta2_k_over_k1sq": formula_Pfail,
        "P_fail_matches_formula": bool(abs(P_fail - formula_Pfail) < 1e-9),
        "P_fail_within_bound_4k_over_k1sq": bool(P_fail <= bound + 1e-12),
        "state_fidelity_to_(kUa+Ub)psi": float(fid),
        "implements_target": bool(fid > 1 - 1e-9),
    }

# ----- C3/C4/C5: product & multi-product formulas -----
def H_parts_1q(a=0.7, b=1.3):
    return [a*X, b*Z]

def S2(parts, t):
    """2nd-order symmetric (Strang) product formula for exp(-i (H1+H2) t)."""
    H1, H2 = parts
    return expm(-1j*H1*t/2) @ expm(-1j*H2*t) @ expm(-1j*H1*t/2)

def S1(parts, t):
    """1st-order Lie-Trotter."""
    H1, H2 = parts
    return expm(-1j*H1*t) @ expm(-1j*H2*t)

def exact_U(parts, t):
    return expm(-1j*(parts[0]+parts[1])*t)

def MPF_richardson_S2(parts, t):
    """Richardson multi-product on the 2nd-order formula:
       M = (4 S2(t/2)^2 - S2(t)) / 3.
    Cancels the leading O(t^3) error of S2 -> higher order."""
    M = (4*(S2(parts, t/2) @ S2(parts, t/2)) - S2(parts, t)) / 3.0
    coeffs = [4.0/3.0, -1.0/3.0]
    return M, coeffs

def MPF_richardson_S1(parts, t):
    """Richardson multi-product on the 1st-order formula:
       M = (2 S1(t/2)^2 - S1(t))  (coeffs sum to 1)."""
    M = 2*(S1(parts, t/2) @ S1(parts, t/2)) - S1(parts, t)
    coeffs = [2.0, -1.0]
    return M, coeffs

def fit_order(ts, errs):
    """log-log slope of error vs t -> empirical order p (err ~ t^p)."""
    mask = (errs > 1e-13) & (errs < 1e-1)
    lt = np.log(ts[mask]); le = np.log(errs[mask])
    p, c = np.polyfit(lt, le, 1)
    return float(p)

def nearest_unitary_distance(M):
    """min over unitaries U of ||M - U|| = ||Sigma - I|| where M = W Sigma V^dag."""
    U_, S_, Vh = svd(M)
    return float(np.max(np.abs(S_ - 1.0)))

# =================== RUN ===================
results = {}

# C1/C2: Lemma 2 over several (close) unitary pairs & kappa
parts = H_parts_1q()
lem2 = {}
cases = []
for eps in [0.05, 0.1, 0.2]:
    Ua = expm(-1j*X*0.0)              # identity-ish
    Ub = expm(-1j*X*eps)             # nearby unitary
    for kappa in [1.0, 3.0, 10.0]:
        key = f"eps={eps},kappa={kappa}"
        r = test_lemma2(Ua, Ub, kappa)
        lem2[key] = r
results["C1_lemma2_LCU"] = lem2
# C2 kappa definition check for a 3-term combination
Cq = [4.0/3.0, -1.0/3.0]
kappa_def = sum(c for c in Cq if c > 0) / sum(abs(c) for c in Cq if c < 0)
results["C2_theorem3_kappa"] = {
    "coeffs": Cq, "kappa_pos_over_negabs": kappa_def,
    "expected_(4/3)/(1/3)": 4.0,
    "matches": bool(abs(kappa_def - 4.0) < 1e-12),
}

# C3: order improvement — S1, S2, and their Richardson MPFs
ts = np.geomspace(0.01, 0.4, 18)
def errs_of(fn):
    return np.array([float(norm(fn(parts, t) - exact_U(parts, t), 2)) for t in ts])
err_S1 = errs_of(S1)
err_S2 = errs_of(S2)
err_M1 = errs_of(lambda p,t: MPF_richardson_S1(p,t)[0])
err_M2 = errs_of(lambda p,t: MPF_richardson_S2(p,t)[0])
order_S1 = fit_order(ts, err_S1)
order_S2 = fit_order(ts, err_S2)
order_M1 = fit_order(ts, err_M1)
order_M2 = fit_order(ts, err_M2)
results["C3_order_scaling"] = {
    "S1_first_order_trotter_empirical_order": order_S1,   # expect ~2 (err O(t^2))
    "S2_strang_empirical_order": order_S2,                # expect ~3 (err O(t^3))
    "MPF_richardson_on_S1_empirical_order": order_M1,     # expect ~3
    "MPF_richardson_on_S2_empirical_order": order_M2,     # expect ~5
    "MPF_S2_higher_order_than_S2": bool(order_M2 > order_S2 + 0.8),
    "MPF_S1_higher_order_than_S1": bool(order_M1 > order_S1 + 0.8),
    "ts": ts.tolist(),
    "err_S1": err_S1.tolist(), "err_S2": err_S2.tolist(),
    "err_MPF_S1": err_M1.tolist(), "err_MPF_S2": err_M2.tolist(),
}

# C4: coefficient sums = 1
_, c_m2 = MPF_richardson_S2(parts, 0.1)
_, c_m1 = MPF_richardson_S1(parts, 0.1)
results["C4_coeff_sum_equals_1"] = {
    "MPF_S2_coeffs": c_m2, "MPF_S2_sum": float(sum(c_m2)),
    "MPF_S1_coeffs": c_m1, "MPF_S1_sum": float(sum(c_m1)),
    "both_sum_to_1": bool(abs(sum(c_m2)-1) < 1e-12 and abs(sum(c_m1)-1) < 1e-12),
}

# C5: nearly-unitary — distance of MPF to nearest unitary vs t (should be high order)
dist = np.array([nearest_unitary_distance(MPF_richardson_S2(parts, t)[0]) for t in ts])
order_unit = fit_order(ts, dist)
results["C5_nearly_unitary"] = {
    "nearest_unitary_distance_vs_t_order": order_unit,   # expect high (>= ~6)
    "max_distance_over_t_range": float(np.max(dist)),
    "is_high_order_unitary": bool(order_unit > order_M2),  # unitary error >> spectral order
    "dist": dist.tolist(),
}

# 2-qubit cross check (Theorem 1 superiority context): MPF beats S2 at fixed small t
def H_parts_2q():
    XX = np.kron(X, X); Z0 = np.kron(Z, I2); Z1 = np.kron(I2, Z)
    return [XX, Z0 + Z1]
p2 = H_parts_2q()
t_chk = 0.2
e_s2 = norm(S2(p2, t_chk) - exact_U(p2, t_chk), 2)
e_m2 = norm(MPF_richardson_S2(p2, t_chk)[0] - exact_U(p2, t_chk), 2)
results["C3b_2qubit_crosscheck"] = {
    "t": t_chk, "S2_error": float(e_s2), "MPF_S2_error": float(e_m2),
    "MPF_more_accurate": bool(e_m2 < e_s2),
    "improvement_factor": float(e_s2/e_m2),
}

with open("results.json","w") as fh:
    json.dump(results, fh, indent=2)

print("=== LCU Hamiltonian Simulation (Childs-Wiebe) — replication ===")
print("C1 Lemma 2 (failure prob = Delta^2 kappa/(kappa+1)^2; implements kUa+Ub):")
for k,v in lem2.items():
    print(f"  {k}: Pfail_circ={v['P_fail_circuit']:.6f} "
          f"formula={v['P_fail_formula_Delta2_k_over_k1sq']:.6f} "
          f"match={v['P_fail_matches_formula']} impl={v['implements_target']}")
print(f"C2 Theorem 3 kappa = (4/3)/(1/3) = {kappa_def:.4f} (expect 4.0) "
      f"match={results['C2_theorem3_kappa']['matches']}")
print(f"C3 empirical orders (err ~ t^p):")
print(f"   S1(1st-order)={order_S1:.2f}  S2(Strang)={order_S2:.2f}  "
      f"MPF/S1={order_M1:.2f}  MPF/S2={order_M2:.2f}")
print(f"   MPF raises order over base: S1->{results['C3_order_scaling']['MPF_S1_higher_order_than_S1']}, "
      f"S2->{results['C3_order_scaling']['MPF_S2_higher_order_than_S2']}")
print(f"C4 coeff sums to 1: MPF/S2 sum={sum(c_m2):.6f}, MPF/S1 sum={sum(c_m1):.6f}  "
      f"both=1: {results['C4_coeff_sum_equals_1']['both_sum_to_1']}")
print(f"C5 nearest-unitary distance order = {order_unit:.2f} (>> spectral order {order_M2:.2f}: "
      f"{results['C5_nearly_unitary']['is_high_order_unitary']})")
print(f"C3b 2-qubit: S2 err={e_s2:.2e}  MPF err={e_m2:.2e}  "
      f"MPF better={results['C3b_2qubit_crosscheck']['MPF_more_accurate']} "
      f"(x{results['C3b_2qubit_crosscheck']['improvement_factor']:.0f})")
print("\nWrote results.json")
