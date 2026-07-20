"""
Quantitative verification of machine-checkable claims from arXiv:1807.09258.

Claims tested:
  C1. Biquadratic operator identity  (Si.Sj)^2 = (Qi.Qj)/2 - (Si.Sj)/2 + (Si^2 Sj^2)/3
      and the Supplemental form       Qi.Qj    = 2 (Si.Sj)^2 + (Si.Sj) - 8/3.
  C2. d-vector -> spin/quadrupole maps (Eqs. S16-S22) reproduce direct 3x3 operator
      expectation values for the corresponding coherent states, and the ground-state
      directors are pure quadrupolar (zero dipole moment, |Q|=finite).
  C3. (pi,pi)-AFQ ground state dA=(1,0,0), dB=(0,1,0) gives staggered <Q^{x2-y2}> ~ (-1)^j
      and, at the SU(3) point, MINIMIZES the nearest-neighbor bond energy while a
      ferro-director arrangement does NOT (verifies "minimize nn |di.conj(dj)|").
  C4. Gell-Mann global rotation U(phi)=exp(i sum lambda_j phi_j) is unitary and, at the
      SU(3) point, leaves the two-director ground-state energy invariant (flat/marginal
      direction -> the Goldstone/marginality structure the RG rests on).
  C5. Spin-1 BLBQ SU(3) point: at J1=K1 the two-site spectrum organizes into SU(3)
      multiplets (degeneracies 3 (fund. sym? ) etc.) -> we check the two-site energy
      levels collapse to 2 distinct values (the SU(3)-symmetric structure), whereas
      away from SU(3) they split.

All numbers printed with tolerances; PASS/FAIL emitted per check.
"""

import json
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from model import (Sx, Sy, Sz, I3, quad_ops, SdotS, QdotQ,
                   spin_from_d, quad_from_d, normalize_d,
                   bond_energy, gell_mann_4, global_rotation)

TOL = 1e-9
results = {}


def check(name, passed, detail):
    results[name] = {"pass": bool(passed), "detail": detail}
    tag = "PASS" if passed else "FAIL"
    print(f"[{tag}] {name}: {detail}")
    return passed


# ------------------------------------------------------------------
# C1. Biquadratic identities (operator level, exact on 9-dim space)
# ------------------------------------------------------------------
def c1():
    SS = SdotS()
    QQ = QdotQ()
    S2 = (Sx @ Sx + Sy @ Sy + Sz @ Sz)  # = 2 I for S=1
    S2i_S2j = np.kron(S2, S2)
    # identity 1: (S.S)^2 == Q.Q/2 - S.S/2 + (Si^2 Sj^2)/3
    lhs1 = SS @ SS
    rhs1 = QQ / 2 - SS / 2 + S2i_S2j / 3
    err1 = np.max(np.abs(lhs1 - rhs1))
    # identity 2 (Supplemental):  Q.Q == 2 (S.S)^2 + S.S - 8/3 * I
    lhs2 = QQ
    rhs2 = 2 * (SS @ SS) + SS - (8.0 / 3.0) * np.eye(9)
    err2 = np.max(np.abs(lhs2 - rhs2))
    ok = check("C1_biquadratic_identity_main",
               err1 < TOL, f"max|LHS-RHS| = {err1:.2e} (S=1, S^2=2)")
    ok &= check("C1_biquadratic_identity_supp",
                err2 < TOL, f"max|Q.Q - (2(S.S)^2+S.S-8/3)| = {err2:.2e}")
    return ok


# ------------------------------------------------------------------
# C2. d-vector maps vs direct operator expectation on coherent states
# ------------------------------------------------------------------
def c2():
    """The TRI basis (Eq. S10): |x>=i(|1>-|-1>)/sqrt2, |y>=(|1>+|-1>)/sqrt2, |z>=-i|0>.
    A director d=(dx,dy,dz) corresponds to state |psi> = dx|x>+dy|y>+dz|z>.
    We compute <S^a>, <Q^a> via the 3x3 operators and compare to spin_from_d/quad_from_d."""
    # TRI basis vectors in the |+1>,|0>,|-1> basis
    ket = {}
    ket['x'] = np.array([1j, 0, -1j]) / np.sqrt(2)   # i(|1>-|-1>)/sqrt2
    ket['y'] = np.array([1, 0, 1]) / np.sqrt(2)      # (|1>+|-1>)/sqrt2
    ket['z'] = np.array([0, -1j, 0])                 # -i|0>
    B = np.column_stack([ket['x'], ket['y'], ket['z']])  # columns = |x>,|y>,|z>

    Qlist = quad_ops()
    rng = np.random.default_rng(1807)
    max_serr = 0.0
    max_qerr = 0.0
    for _ in range(200):
        d = rng.normal(size=3) + 1j * rng.normal(size=3)
        d = normalize_d(d)
        psi = B @ d                      # state in |+1,0,-1> basis
        psi = psi / np.linalg.norm(psi)
        # direct expectation values
        S_dir = np.array([np.vdot(psi, Sx @ psi).real,
                          np.vdot(psi, Sy @ psi).real,
                          np.vdot(psi, Sz @ psi).real])
        Q_dir = np.array([np.vdot(psi, Q @ psi).real for Q in Qlist])
        # from d-vector formulas
        S_d = spin_from_d(d)
        Q_d = quad_from_d(d)
        max_serr = max(max_serr, np.max(np.abs(S_dir - S_d)))
        max_qerr = max(max_qerr, np.max(np.abs(Q_dir - Q_d)))
    ok = check("C2_spin_map", max_serr < 1e-8,
               f"max|S_operator - S(d)| over 200 randoms = {max_serr:.2e}")
    ok &= check("C2_quad_map", max_qerr < 1e-8,
                f"max|Q_operator - Q(d)| over 200 randoms = {max_qerr:.2e}")
    # ground-state directors are pure-quadrupolar (no dipole)
    dA = np.array([1, 0, 0], dtype=complex)
    dB = np.array([0, 1, 0], dtype=complex)
    SA = spin_from_d(dA); SB = spin_from_d(dB)
    ok &= check("C2_gs_no_dipole",
                np.max(np.abs(SA)) < TOL and np.max(np.abs(SB)) < TOL,
                f"|S(dA)|={np.max(np.abs(SA)):.2e}, |S(dB)|={np.max(np.abs(SB)):.2e}")
    return ok


# ------------------------------------------------------------------
# C3. (pi,pi)-AFQ ground state: staggered Q^{x2-y2} and nn energy minimization
# ------------------------------------------------------------------
def c3():
    dA = np.array([1, 0, 0], dtype=complex)
    dB = np.array([0, 1, 0], dtype=complex)
    QA = quad_from_d(dA)
    QB = quad_from_d(dB)
    # Q^{x2-y2} is component 0
    qA = QA[0]; qB = QB[0]
    staggered = np.isclose(qA, -qB) and abs(qA) > 0.5
    ok = check("C3_staggered_Qx2y2", staggered,
               f"<Q^x2-y2>_A={qA:+.3f}, _B={qB:+.3f} -> staggered (-1)^j pattern")

    # At the SU(3) point J1=K1=1: nn bond energy uses only |di.conj(dj)|^2 (Kn-Jn=0).
    J1 = K1 = 1.0
    e_afq = bond_energy(dA, dB, J1, K1)          # orthogonal directors -> |dA.conj(dB)|^2 = 0
    e_ferro = bond_energy(dA, dA, J1, K1)        # same director -> |dA.conj(dA)|^2 = 1
    ok &= check("C3_afq_minimizes_nn",
                e_afq < e_ferro - 0.5,
                f"E_nn(AFQ orthogonal)={e_afq:.3f} < E_nn(ferro)={e_ferro:.3f} "
                f"(minimizing nn |di.conj(dj)| as required)")
    # 2nd-neighbor: same-sublattice directors are PARALLEL -> maximize |di.conj(dj)|
    e_2nd_same = bond_energy(dA, dA, J1, K1)
    ok &= check("C3_2nd_neighbor_max",
                np.isclose(e_2nd_same, 1.0 * J1),
                f"E_2nd(same-sublattice parallel)={e_2nd_same:.3f} = J2*1 (maximized overlap)")
    return ok


# ------------------------------------------------------------------
# C4. Gell-Mann global rotation: unitarity + SU(3)-point energy invariance (marginal)
# ------------------------------------------------------------------
def c4():
    gens = gell_mann_4()
    # hermiticity of generators
    herm = all(np.max(np.abs(g - g.conj().T)) < TOL for g in gens)
    ok = check("C4_generators_hermitian", herm,
               "all 4 generators Hermitian -> U=exp(i lambda phi) unitary")

    rng = np.random.default_rng(925)
    dA = np.array([1, 0, 0], dtype=complex)
    dB = np.array([0, 1, 0], dtype=complex)
    J1 = K1 = J2 = K2_val = 1.0  # SU(3) point on BOTH neighbor shells (Jn=Kn)
    # baseline SU(3)-point two-director energy (nn + 2nd-neighbor within a plaquette)
    def su3_energy(da, db):
        # nn bond (A-B): coefficient J1; 2nd-neighbor bond (A-A or B-B): coeff J2
        e_nn = bond_energy(da, db, J1, K1)
        e_2A = bond_energy(da, da, J2, K2_val)
        e_2B = bond_energy(db, db, J2, K2_val)
        return e_nn + 0.5 * (e_2A + e_2B)
    e0 = su3_energy(dA, dB)

    max_dev_unit = 0.0
    max_dev_energy = 0.0
    for _ in range(200):
        phis = rng.normal(size=4) * 0.7
        U = global_rotation(phis, gens)
        max_dev_unit = max(max_dev_unit,
                           np.max(np.abs(U.conj().T @ U - np.eye(3))))
        dAp = U @ dA
        dBp = U @ dB
        e1 = su3_energy(dAp, dBp)
        max_dev_energy = max(max_dev_energy, abs(e1 - e0))
    ok &= check("C4_U_unitary", max_dev_unit < 1e-8,
                f"max|U^dU - I| over 200 = {max_dev_unit:.2e}")
    ok &= check("C4_su3_energy_invariant_marginal", max_dev_energy < 1e-8,
                f"max|E(U d)-E(d)| over 200 SU(3)-point rotations = {max_dev_energy:.2e} "
                f"(flat direction -> Goldstone/marginal structure)")
    return ok


# ------------------------------------------------------------------
# C5. Two-site BLBQ spectrum: SU(3) symmetry at J=K; splitting away from it
# ------------------------------------------------------------------
def c5():
    SS = SdotS()
    QQ = QdotQ()
    S2 = (Sx @ Sx + Sy @ Sy + Sz @ Sz)
    S2i_S2j = np.kron(S2, S2)

    def H_two_site(J, K):
        # H = J S.S + K (S.S)^2, and (S.S)^2 = Q.Q/2 - S.S/2 + Si^2Sj^2/3
        return J * SS + K * (SS @ SS)

    # At SU(3) point J=K: spectrum should have exactly 2 distinct eigenvalues
    # (the two-site product 3 x 3 = 6 (sym) + 3bar (antisym) of SU(3)).
    H_su3 = H_two_site(1.0, 1.0)
    ev_su3 = np.round(np.linalg.eigvalsh(H_su3), 8)
    distinct_su3 = len(set(ev_su3.tolist()))
    # degeneracy multiset
    vals, counts = np.unique(ev_su3, return_counts=True)
    ok = check("C5_su3_two_levels", distinct_su3 == 2,
               f"J=K SU(3) point: {distinct_su3} distinct 2-site levels, "
               f"degeneracies={sorted(counts.tolist())} (expect 6+3)")

    # Away from SU(3): more distinct levels (symmetry broken to SU(2))
    H_break = H_two_site(1.0, 1.2)
    ev_break = np.round(np.linalg.eigvalsh(H_break), 8)
    distinct_break = len(set(ev_break.tolist()))
    ok &= check("C5_su2_more_levels", distinct_break > distinct_su3,
                f"J=1,K=1.2 (away from SU(3)): {distinct_break} distinct levels "
                f"(> {distinct_su3}) -> symmetry lowered as paper states")
    return ok


def main():
    print("=" * 72)
    print("Verification of arXiv:1807.09258 machine-checkable claims")
    print("=" * 72)
    all_ok = True
    for fn in (c1, c2, c3, c4, c5):
        print(f"\n--- {fn.__name__.upper()} ---")
        all_ok &= fn()
    print("\n" + "=" * 72)
    print("OVERALL:", "ALL PASS" if all_ok else "SOME FAILED")
    print("=" * 72)
    summary = {
        "overall_pass": bool(all_ok),
        "n_checks": len(results),
        "n_passed": sum(1 for v in results.values() if v["pass"]),
        "checks": results,
    }
    outdir = os.path.join(os.path.dirname(__file__), "..", "work")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "verification_results.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {os.path.join(outdir, 'verification_results.json')}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
