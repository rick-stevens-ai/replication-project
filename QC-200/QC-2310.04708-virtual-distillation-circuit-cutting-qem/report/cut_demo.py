"""
Circuit-cutting reconstruction demo (Peng et al. 2019).

Wire-cut identity (Peng-Horsman-Rudolph-Ying-Zhao):
   rho_out  =  sum_i c_i  * rho_prep_i  *  <M_meas_i, rho_in>
For a QPD of the identity channel across one wire, the standard 8-term
decomposition uses the 6 Pauli eigenstates as prep, and Z, X, Y as measurements:

   Id(rho) = sum_{P in {Z,X,Y}} [ (|+P><+P| - |-P><-P|)  Tr( P rho ) ]
   equivalent to:
   Id(rho) = 0.5 * sum_{P in {I,X,Y,Z}} P rho P    (Pauli twirl form — NOT the wire cut)

The Pauli twirl gives the identity CHANNEL (rho -> rho), so for cutting a wire
BEFORE any gate we can use it. But for an <O>_uncut = <O_A x O_B>_full split
across a cut wire, the correct identity is:

   <O_A x O_B> = sum_P Tr( P_A rho_A ) * Tr( P_B rho_B ) / 2^n_cut       (wrong: only for maximally mixed states)

Correct expectation-value cutting for an operator O on state |psi> where the
circuit crosses one wire:
   <psi| U^dag O U |psi> = 0.5 * sum_{P in {I,X,Y,Z}}
       Tr( U_A^dag (O_A x P) U_A rho_A ) * Tr( U_B^dag (P x O_B) U_B rho_B )
   where rho_A = |0>_A<0|_A x  ...  and same for B, with the "cut wire" state
   restored via P injection.

But wait — this ONLY works if the cut is on a wire that starts in |0> on the B
side (so the "input" to B's slice on that wire is |0>). If B's input on the cut
wire is a general state coming from A, we need the measure-and-prepare form.

Correct wire-cut QPD (see Perlin et al. 2021 / Peng 2019 eq. 6):
   Id(rho) = (1/2) sum_{i=1}^{8} c_i sigma_i^prep Tr( sigma_i^meas rho )
with the 8 terms:
   (prep basis: {|0>,|1>,|+>,|->,|+i>,|-i>}, meas: {I,Z,X,Y})
   Explicit:
     Id(rho) =   |0><0| Tr((I+Z)/2 . rho)  +  |1><1| Tr((I-Z)/2 . rho)
              +  |+><+| Tr((I+X)/2 . rho)  +  |-><-| Tr((I-X)/2 . rho)
              +  |+i><+i| Tr((I+Y)/2 . rho) + |-i><-i| Tr((I-Y)/2 . rho)
              -  (1/2)( I . Tr(I . rho) )  ...
Actually the cleanest is:
   Id = sum_{P in {I,X,Y,Z}} (1/2) P (.) P

Verify: sum_P P rho P / 2 for rho = |0><0|:
   I|0><0|I = |0><0|
   X|0><0|X = |1><1|
   Y|0><0|Y = |1><1|
   Z|0><0|Z = |0><0|
   Sum/2 = (|0><0| + |1><1|)/2 * 2/2 = (2|0><0| + 2|1><1|)/2 = I  -- WRONG, that's not rho.

The Pauli twirl is Id only for MAXIMALLY MIXED input. Otherwise it's the
completely depolarizing channel to I/2.

OK, the RIGHT identity for cutting a wire in a UNITARY circuit and reconstructing
EXPECTATION VALUES (Peng 2019 eq 4-5):

  Given circuit U = U_B (I x V x I) U_A crossing one wire between two subsystems,
  and observable O = O_A x O_B, the expectation <psi|U^dag O U|psi> can be
  written as:

     <O> = sum_{i=1}^{8} c_i  <O_A^{(i)}>_{A}  *  <O_B^{(i)}>_{B'}

  where {c_i, prep basis on B's cut wire, meas basis on A's cut wire} form the
  QPD of the SWAP-through-wire operator (essentially the identity map on that wire).

The 8-term decomp with c_i in {+1/2, -1/2} etc. is:

  Id(rho) = (1/2) [ |0><0| (<0|rho|0> + <1|rho|1>)   -- nope, that's Tr(rho) |0><0|/2 which is 0 or ...

Let me just cite Mitiq / Qiskit-Addon-cutting docs and use the 6-term
QPD for a wire cut:

   Id ⊗ Id = sum_{i in {1..6}} c_i (M_i o P_i)
where M_i are single-qubit POVM elements and P_i are state preps.

For an expectation-value computation, the practical decomposition is:

   <O_A x O_B> = sum_{P in {I,X,Y,Z}} <O_A x P>_A  *  <O_B; input=|P^+> - |P^->>_B
                                                                          [normalized]

Concretely (from Peng 2019 & Perlin 2021):

   <O> = 0.5 * sum_{P in {X,Y,Z}} [ <O_A x P>_A * ( <O_B; prep=|P+>>_B - <O_B; prep=|P->>_B ) ]
       + <O_A x I>_A * ( 0.5 * <O_B; prep=|0>>_B + 0.5 * <O_B; prep=|1>>_B )

which is 8 terms total: 2 (I-prep) + 2 (X-eigen-prep) + 2 (Y-eigen-prep) + 2 (Z-eigen-prep).

Actually the correct 8-term expression is:

   <O> = sum over 8 basis choices, with coefficients summing to overhead 4^k,
         where each term is <(O_A on A with cut-wire measured in Pauli P)>_A
                              * <(O_B on B with cut-wire prepared in eigenstate of P)>_B

I'll implement this directly using measurement operators and state preps and
verify numerical closure against the uncut expectation.
"""

import json
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)

# Eigenstates
ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)
ketp = (ket0 + ket1) / np.sqrt(2)
ketm = (ket0 - ket1) / np.sqrt(2)
ketpi = (ket0 + 1j * ket1) / np.sqrt(2)
ketmi = (ket0 - 1j * ket1) / np.sqrt(2)


def kron(*ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def outer(v):
    return np.outer(v, v.conj())


def uncut_expectation():
    """Full 4-qubit circuit. |0000> -> H(q0), CX(q0,q1), CX(q1,q2), CX(q2,q3). Measure Z0 Z3."""
    psi = np.zeros(16, dtype=complex)
    psi[0] = 1.0
    psi = kron(H, I2, I2, I2) @ psi
    psi = kron(CX, I2, I2) @ psi
    psi = kron(I2, CX, I2) @ psi
    psi = kron(I2, I2, CX) @ psi
    O = kron(Z, I2, I2, Z)
    return float(np.real(psi.conj() @ O @ psi))


def cut_reconstruction():
    """
    Cut the wire between q1 and q2 (after CX(q0,q1), before CX(q1,q2)).
    Fragment A: qubits {q0, q1}. Circuit: H(q0), CX(q0,q1). Then measure q1 in Pauli P.
                Compute <Z0 x P_q1>_A.
    Fragment B: qubits {q2, q3}. Prep q2 in an eigenstate of P, then apply
                CX(q2,q3). Compute <Z_q3>_B.

    Wire-cut identity (Peng 2019, using 8-term decomp with 4 Paulis on measure side
    and their eigenstate preps on prep side):

        Id(rho_cut) = 0.5 * sum_{P in {I,X,Y,Z}} P * rho_cut * P     -- WRONG (that's dephasing to I/2)

    The correct QPD (Perlin 2021, eq 6-10) for wire cut is:

        Id(rho) = sum_i c_i |psi_i><phi_i| * <phi_i| rho |phi_i>

    or equivalently, for expectation values:

        <O_A o O_B> = 0.5 * sum_P Tr( (O_A x P) rho_A ) * ( <O_B>_{prep = |P+>} - <O_B>_{prep = |P->} )
                    + 1.0 * Tr( (O_A x I) rho_A ) * 0.5 * ( <O_B>_{prep=|0>} + <O_B>_{prep=|1>} )

    (I-part uses the fact that I = |0><0| + |1><1|, so <I> = <0|.|0> + <1|.|1>,
     and no sign; X-eigenstates give X = |+><+| - |-><-|, hence the difference form.)

    So the 8 terms:
      (I, prep |0>)  coeff +0.5    -- from I = P(|0>) + P(|1>) with P(|k>) = |k><k|
      (I, prep |1>)  coeff +0.5
      (X, prep |+>)  coeff +0.5
      (X, prep |->)  coeff -0.5
      (Y, prep |+i>) coeff +0.5
      (Y, prep |-i>) coeff -0.5
      (Z, prep |0>)  coeff +0.5
      (Z, prep |1>)  coeff -0.5

    Total: 8 terms, sum of |coeff| = 4  (= overhead 4^1 for 1 cut).
    """
    terms = [
        (I2, ket0, +0.5, "I, |0>"),
        (I2, ket1, +0.5, "I, |1>"),
        (X, ketp, +0.5, "X, |+>"),
        (X, ketm, -0.5, "X, |->"),
        (Y, ketpi, +0.5, "Y, |+i>"),
        (Y, ketmi, -0.5, "Y, |-i>"),
        (Z, ket0, +0.5, "Z, |0>"),
        (Z, ket1, -0.5, "Z, |1>"),
    ]

    # Fragment A state (before cut): |0>,|0> -> H(q0) -> CX(q0,q1)
    psi_A = np.zeros(4, dtype=complex)
    psi_A[0] = 1.0
    psi_A = kron(H, I2) @ psi_A
    psi_A = CX @ psi_A

    total = 0.0
    contribs = []
    for P_meas, ket_prep, coeff, label in terms:
        # <Z_q0 x P_q1>_A
        OA = kron(Z, P_meas)
        aval = float(np.real(psi_A.conj() @ OA @ psi_A))

        # Fragment B: prep q2 in ket_prep, q3 in |0>. Apply CX(q2,q3). Measure Z_q3.
        psi_B = np.kron(ket_prep, ket0)
        psi_B = CX @ psi_B
        OB = kron(I2, Z)
        bval = float(np.real(psi_B.conj() @ OB @ psi_B))

        term = coeff * aval * bval
        total += term
        contribs.append({
            "term": label,
            "coeff": coeff,
            "a_val": round(aval, 6),
            "b_val": round(bval, 6),
            "contribution": round(term, 6),
        })
    return total, contribs


def main():
    uncut = uncut_expectation()
    reconstructed, contribs = cut_reconstruction()
    diff = abs(uncut - reconstructed)
    result = {
        "task": "1-cut wire-cutting reconstruction of <Z0 Z3>, 4-qubit chain circuit",
        "circuit": "|0000> -> H(q0), CX(q0,q1), CX(q1,q2), CX(q2,q3); cut wire between q1 and q2",
        "cut_placement": "on wire q1<->q2, between CX(q0,q1) and CX(q1,q2)",
        "uncut_expectation": round(uncut, 8),
        "reconstructed_expectation": round(reconstructed, 8),
        "abs_difference": diff,
        "n_terms": len(contribs),
        "overhead_sum_abs_coeff": 4.0,
        "per_term": contribs,
        "identity_used": (
            "Peng-2019 wire-cut QPD with 8 terms: 2 (I-prep) + 2 (X-eigen) + 2 (Y-eigen) + 2 (Z-eigen), "
            "coefficients ±0.5 summing to overhead 4."
        ),
        "verdict": "CONFIRMED" if diff < 1e-9 else "MISMATCH",
    }
    with open("report/cut_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
