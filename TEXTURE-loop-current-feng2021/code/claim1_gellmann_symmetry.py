"""
claim1_gellmann_symmetry.py
============================
Replicates the D6h symmetry classification of the SU(3) Gell-Mann order
parameters in the vH (psi_M) basis of Feng, Zhang, Jiang, Hu,
"Low-energy effective theory and symmetry classification of flux phases on
Kagome lattice", arXiv:2106.04395 (2021).

CENTRAL CLAIMS CHECKED
----------------------
(A) The 8 SU(3) Gell-Mann generators Gamma_i, transformed by the D6h
    operations given in Eq.(3) as D(R) Gamma_i D(R)^{-1}, reproduce Table I,
    and thereby split into THREE closed classes:
        Delta_b   = {Gamma1, Gamma4, Gamma6}   (real off-diagonal, bond order)
        Delta_phi = {Gamma2, Gamma5, Gamma7}   (imaginary off-diagonal, FLUX)
        Delta_s   = {Gamma3, Gamma8}           (diagonal, charge)
(B) The chiral flux phase (CFP) order parameter Delta_phi,1 = Gamma2 - Gamma5
    + Gamma7 is invariant (A1g) under C6, C3 (up to the tabulated signs that
    close within the flux class), consistent with its A1g(D*6h) assignment.
(C) The C6, C3, sigma_v operators of Eq.(3) are genuine order-3 / order-2
    permutation representations acting on psi_M = (psi_M1, psi_M2, psi_M3).

Provenance: symmetry-operator machinery adapted from the shared kagome
loop-current kernel's spirit (Gell-Mann handling in
triangle_flux_from_config / patch logic), but the Gamma-matrix transformation
table is implemented fresh here because this paper's core result is the
GROUP-THEORY table, which the kernel did not contain.
"""
import numpy as np

# ---- Gell-Mann matrices (paper Eq. 5) -------------------------------------
G = {}
G[1] = np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex)
G[2] = np.array([[0,-1j,0],[1j,0,0],[0,0,0]], dtype=complex)
G[3] = np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex)
G[4] = np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex)
G[5] = np.array([[0,0,-1j],[0,0,0],[1j,0,0]], dtype=complex)
G[6] = np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex)
G[7] = np.array([[0,0,0],[0,0,-1j],[0,1j,0]], dtype=complex)
G[8] = (1/np.sqrt(3))*np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex)

# ---- D6h operations in psi_M basis (paper Eq. 3) --------------------------
C6 = np.array([[0,1,0],[0,0,1],[1,0,0]], dtype=complex)
C3 = np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=complex)
sv = np.array([[0,0,1],[0,1,0],[1,0,0]], dtype=complex)
svp = np.array([[0,1,0],[1,0,0],[0,0,1]], dtype=complex)     # sigma_v'
svpp = np.array([[1,0,0],[0,0,1],[0,1,0]], dtype=complex)    # sigma_v''

OPS = {"C6":C6, "C3":C3, "sv":sv, "svp":svp, "svpp":svpp}


def transform(R, Gi):
    """D(R) Gamma_i D(R)^{-1}."""
    return R @ Gi @ np.linalg.inv(R)


def decompose(M):
    """Express a traceless-ish 3x3 Hermitian matrix in the Gamma basis.
    Returns dict i->coeff (real if Hermitian). Uses Tr(Gi Gj)=2 delta_ij."""
    coeffs = {}
    for i in range(1, 9):
        c = np.trace(G[i].conj().T @ M) / 2.0
        if abs(c) > 1e-9:
            coeffs[i] = complex(np.round(c, 6))
    return coeffs


def fmt(coeffs):
    parts = []
    for i, c in sorted(coeffs.items()):
        cr = c.real
        ci = c.imag
        if abs(ci) < 1e-9:
            s = f"{cr:+.3g}"
        else:
            s = f"({cr:+.3g}{ci:+.3g}i)"
        parts.append(f"{s}*G{i}")
    return " ".join(parts) if parts else "0"


# ---- Reference Table I (paper) --------------------------------------------
# Encoded as: op -> {i: expected result string} using the paper's own entries.
# We verify the CLASS closure and the specific transformed generators.
REFERENCE_TABLE_I = {
    "C6": {1:"G4", 2:"-G5", 4:"G6", 5:"-G7", 6:"G1", 7:"G2"},
    "C3": {1:"G6", 2:"G7", 4:"G1", 5:"-G2", 6:"G4", 7:"G5"},
    "sv": {1:"G6", 2:"-G7", 4:"G4", 5:"-G5", 6:"G1", 7:"-G2"},
    "svp":{1:"G1", 2:"-G2", 4:"G6", 5:"G7", 6:"G4", 7:"G5"},
    "svpp":{1:"G4", 2:"G5", 4:"G1", 5:"G2", 6:"G6", 7:"-G7"},
}


def check():
    results = {"per_op": {}, "classes": {}, "cfp": {}, "table_match": {}}
    class_b = {1, 4, 6}
    class_phi = {2, 5, 7}
    class_s = {3, 8}

    # (A)+(C) class closure: transform each Gamma and record which Gammas appear
    for name, R in OPS.items():
        row = {}
        table_ok = True
        for i in range(1, 9):
            Mt = transform(R, G[i])
            coeffs = decompose(Mt)
            row[i] = fmt(coeffs)
            # verify closure within class for off-diagonal generators
            appearing = set(coeffs.keys())
            if i in class_b:
                if not appearing <= class_b:
                    table_ok = False
            elif i in class_phi:
                if not appearing <= class_phi:
                    table_ok = False
            elif i in class_s:
                if not appearing <= class_s:
                    table_ok = False
        results["per_op"][name] = row
        # compare against reference Table I entries where the paper lists a
        # single-generator (or signed single-generator) result
        if name in REFERENCE_TABLE_I:
            match = {}
            for i, expected in REFERENCE_TABLE_I[name].items():
                got = row[i].replace(" ", "")
                # normalize "+1*G4" -> "G4", "-1*G5" -> "-G5"
                got_n = got.replace("+1*", "").replace("-1*", "-").replace("*", "")
                exp_n = expected.replace("+", "")
                match[i] = (got_n == exp_n or got_n == "+"+exp_n)
            results["table_match"][name] = match
        results["classes"][name] = table_ok

    # (B) CFP order parameter Delta_phi,1 = G2 - G5 + G7 invariance under C6/C3
    cfp = G[2] - G[5] + G[7]
    for name in ["C6", "C3"]:
        R = OPS[name]
        cfp_t = transform(R, cfp)
        results["cfp"][name] = fmt(decompose(cfp_t))
        results["cfp"][name + "_invariant"] = bool(
            np.allclose(cfp_t, cfp, atol=1e-9))

    # Verify operator orders
    results["op_orders"] = {
        "C6^6=I": bool(np.allclose(np.linalg.matrix_power(C6, 6), np.eye(3))),
        "C6^3": "C2-like" if not np.allclose(np.linalg.matrix_power(C6,3), np.eye(3)) else "I",
        "C3^3=I": bool(np.allclose(np.linalg.matrix_power(C3, 3), np.eye(3))),
        "sv^2=I": bool(np.allclose(sv @ sv, np.eye(3))),
    }
    return results


if __name__ == "__main__":
    import json
    r = check()
    print("=== D6h transformation of Gamma_i (D(R) Gi D(R)^-1) ===")
    for name, row in r["per_op"].items():
        print(f"\n[{name}]  class-closed={r['classes'][name]}")
        for i in range(1, 9):
            print(f"   G{i} -> {row[i]}")
    print("\n=== Table I match (paper's tabulated single-generator results) ===")
    for name, match in r["table_match"].items():
        allok = all(match.values())
        print(f"  {name}: {'ALL MATCH' if allok else match}")
    print("\n=== CFP Delta_phi,1 = G2 - G5 + G7 ===")
    for name in ["C6", "C3"]:
        print(f"  {name}: -> {r['cfp'][name]}   invariant={r['cfp'][name+'_invariant']}")
    print("\n=== operator orders ===")
    print(" ", r["op_orders"])
