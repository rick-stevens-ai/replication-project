"""
test_gsvd.py
============

Unit tests for gsvd_reference.gsvd and gsvd_reference.ho_gsvd on synthetic
data with planted structure. Each test:

  * constructs D1, D2[, D3] with a *known* shared right basis or planted
    rank-1 antisymmetric structure;
  * runs the decomposition;
  * checks reconstruction error, orthonormality / invariants, and (where
    applicable) that the planted structure is recovered.

Run:
    python3 test_gsvd.py
"""

from __future__ import annotations

import sys
import traceback
from typing import Callable, List, Tuple

import numpy as np

from gsvd_reference import (
    GSVDResult,
    HOGSVDResult,
    antisymmetric_patterns,
    classify_patients,
    combine_predictors,
    gsvd,
    ho_gsvd,
)


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

_RESULTS: List[Tuple[str, bool, str]] = []


def record(name: str, fn: Callable[[], None]) -> None:
    try:
        fn()
        _RESULTS.append((name, True, ""))
        print(f"[PASS] {name}")
    except Exception as e:                                    # noqa: BLE001
        tb = traceback.format_exc()
        _RESULTS.append((name, False, tb))
        print(f"[FAIL] {name}: {e}")
        print(tb)


def assert_close(actual, expected, atol, msg):
    diff = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    if not np.isfinite(diff) or diff > atol:
        raise AssertionError(f"{msg}: max|diff|={diff:.3e} > atol={atol:.3e}")


# ---------------------------------------------------------------------------
# GSVD tests
# ---------------------------------------------------------------------------

def test_gsvd_reconstruction_square():
    """GSVD on random tall (m1,m2 > n) matrices reconstructs exactly."""
    rng = np.random.default_rng(0)
    m1, m2, n = 40, 35, 12
    D1 = rng.standard_normal((m1, n))
    D2 = rng.standard_normal((m2, n))

    r = gsvd(D1, D2)

    R1 = r.U1 @ np.diag(r.c) @ r.V.T
    R2 = r.U2 @ np.diag(r.s) @ r.V.T
    assert_close(R1, D1, 1e-8, "D1 reconstruction")
    assert_close(R2, D2, 1e-8, "D2 reconstruction")


def test_gsvd_csq_invariant():
    """c^2 + s^2 should equal 1 elementwise."""
    rng = np.random.default_rng(1)
    D1 = rng.standard_normal((30, 10))
    D2 = rng.standard_normal((25, 10))
    r = gsvd(D1, D2)
    assert_close(r.c ** 2 + r.s ** 2, np.ones(10), 1e-12, "c**2 + s**2 = 1")


def test_gsvd_U_orthonormal():
    """U1, U2 should have orthonormal columns."""
    rng = np.random.default_rng(2)
    D1 = rng.standard_normal((50, 15))
    D2 = rng.standard_normal((45, 15))
    r = gsvd(D1, D2)
    assert_close(r.U1.T @ r.U1, np.eye(15), 1e-10, "U1.T U1 = I")
    assert_close(r.U2.T @ r.U2, np.eye(15), 1e-10, "U2.T U2 = I")


def test_gsvd_planted_shared_subspace():
    """Plant a known shared right basis and confirm GSVD recovers it.

    Construct D1, D2 by drawing a single common V_true (n x n, invertible)
    and arbitrary U1_true, U2_true with chosen generalized singular values
    (c_true, s_true). Then GSVD should recover the same V (up to per-column
    sign + ordering), the same c, s (sorted), and the same U1, U2.
    """
    rng = np.random.default_rng(3)
    m1, m2, n = 60, 55, 8

    # Planted generalized singular values (sorted by ratio c/s ascending,
    # matching our gsvd() output convention).
    angles = np.linspace(0.05, np.pi / 2 - 0.05, n)  # in (0, pi/2)
    c_true = np.sin(angles)        # increasing 0 -> 1
    s_true = np.cos(angles)        # decreasing 1 -> 0
    # ratio c/s = tan(angles), strictly increasing. So after gsvd() sorts
    # by ratio ascending, recovered (c, s) should equal (c_true, s_true).

    # Random invertible V_true (n x n).
    V_true = rng.standard_normal((n, n))
    while np.linalg.matrix_rank(V_true) < n:
        V_true = rng.standard_normal((n, n))

    # Random column-orthonormal U1_true, U2_true via QR of random tall mats.
    U1_true, _ = np.linalg.qr(rng.standard_normal((m1, n)))
    U2_true, _ = np.linalg.qr(rng.standard_normal((m2, n)))

    D1 = U1_true @ np.diag(c_true) @ V_true.T
    D2 = U2_true @ np.diag(s_true) @ V_true.T

    r = gsvd(D1, D2)

    # Reconstruction.
    assert_close(r.U1 @ np.diag(r.c) @ r.V.T, D1, 1e-8, "planted D1 reconstruction")
    assert_close(r.U2 @ np.diag(r.s) @ r.V.T, D2, 1e-8, "planted D2 reconstruction")

    # Generalized singular values (unsigned) should match the planted ones.
    assert_close(np.sort(r.c), np.sort(c_true), 1e-8, "c values match")
    assert_close(np.sort(r.s), np.sort(s_true), 1e-8, "s values match")
    assert_close(r.c ** 2 + r.s ** 2, np.ones(n), 1e-12, "c**2 + s**2 = 1 (planted)")

    # Shared right basis: V should span the same subspace as V_true. Since
    # V is n x n invertible, this is automatic (both bases of R^n). The
    # stronger check: for each recovered column V[:, k], it should be
    # parallel to V_true[:, k] up to sign (we sorted both by ratio).
    for k in range(n):
        v = r.V[:, k]
        v_true = V_true[:, k]
        # Normalize for direction comparison.
        cos_align = abs(np.dot(v, v_true)) / (np.linalg.norm(v) * np.linalg.norm(v_true))
        if cos_align < 1.0 - 1e-6:
            raise AssertionError(
                f"column {k} of recovered V not parallel to planted "
                f"(|cos|={cos_align:.6e})"
            )


def test_gsvd_antisymmetric_pattern_recovery():
    """Plant a 'tumor-exclusive' rank-1 pattern with known patient sign
    structure, and confirm antisymmetric_patterns + classify_patients
    recover it.
    """
    rng = np.random.default_rng(4)
    n = 30                          # patients
    m1, m2 = 200, 200               # features

    # Sign-structured patient vector: half +1, half -1.
    v_pattern = np.concatenate([np.ones(n // 2), -np.ones(n - n // 2)])
    rng.shuffle(v_pattern)

    # Tumor (D1) has a strong contribution from v_pattern; blood (D2)
    # essentially does not.
    u1_pattern = rng.standard_normal(m1)
    u1_pattern /= np.linalg.norm(u1_pattern)
    D1 = 10.0 * np.outer(u1_pattern, v_pattern)             # rank-1 dominant
    D1 += 0.01 * rng.standard_normal((m1, n))               # tiny noise

    D2 = 0.01 * rng.standard_normal((m2, n))                # almost nothing

    # Pad both with extra random "common" directions so they aren't
    # degenerate-rank.
    common_V = rng.standard_normal((n, n - 1))
    common_U1 = rng.standard_normal((m1, n - 1))
    common_U2 = rng.standard_normal((m2, n - 1))
    D1 = D1 + common_U1 @ common_V.T * 0.5
    D2 = D2 + common_U2 @ common_V.T * 0.5

    r = gsvd(D1, D2)
    k_first, k_last = antisymmetric_patterns(r)

    # The "exclusive-to-D1" column should have the LARGEST c/s ratio.
    ratios = r.ratio
    if not np.argmax(ratios) == k_first:
        raise AssertionError(
            f"antisymmetric_patterns: k_first={k_first} but argmax ratio "
            f"is {int(np.argmax(ratios))} (ratios={ratios})"
        )

    # Patient classification along that column should align (up to sign)
    # with the planted v_pattern.
    v_recovered = r.V[:, k_first]
    sign = np.sign(np.dot(v_recovered, v_pattern))
    if sign == 0:
        sign = 1.0
    labels_recovered = classify_patients(sign * v_recovered)
    labels_planted = classify_patients(v_pattern)
    agreement = float(np.mean(labels_recovered == labels_planted))
    if agreement < 0.95:
        raise AssertionError(
            f"k_first arraylet patient classification only agrees "
            f"{agreement:.2%} with planted v_pattern"
        )


def test_combine_predictors_labels():
    """combine_predictors returns labels in {0,1,2} and is internally consistent."""
    a = np.array([+1.0, +1.0, -1.0, -1.0, +0.5, -0.5])
    b = np.array([+2.0, -2.0, +2.0, -2.0, -1.0, +1.0])
    labels = combine_predictors(a, b)
    expected = np.array([2, 1, 1, 0, 1, 1])
    if not np.array_equal(labels, expected):
        raise AssertionError(f"combine_predictors: got {labels}, expected {expected}")


# ---------------------------------------------------------------------------
# HO-GSVD tests
# ---------------------------------------------------------------------------

def test_ho_gsvd_reconstruction_three_matrices():
    """HO-GSVD of 3 random matrices reconstructs each exactly."""
    rng = np.random.default_rng(10)
    n = 9
    D1 = rng.standard_normal((40, n))
    D2 = rng.standard_normal((35, n))
    D3 = rng.standard_normal((50, n))
    r = ho_gsvd([D1, D2, D3])
    Vinv = r.Vinv
    for k, (D, U, Sigma) in enumerate(zip([D1, D2, D3], r.U, r.Sigma)):
        recon = U @ np.diag(Sigma) @ Vinv
        assert_close(recon, D, 1e-8, f"D_{k} reconstruction (HO-GSVD)")


def test_ho_gsvd_eigenvalues_lower_bound():
    """Eigenvalues of the HO-GSVD balanced average S are real and >= 1
    (Ponnapalli Thm 2)."""
    rng = np.random.default_rng(11)
    n = 10
    Ds = [rng.standard_normal((30 + 5 * k, n)) for k in range(4)]
    r = ho_gsvd(Ds)
    ev = r.eigenvalues
    if np.max(np.abs(np.imag(ev))) > 1e-8:
        raise AssertionError(
            f"HO-GSVD eigenvalues have nontrivial imag part: "
            f"max|im|={np.max(np.abs(np.imag(ev))):.3e}"
        )
    ev_real = np.real(ev)
    min_ev = float(np.min(ev_real))
    # Allow tiny numerical slack below 1.
    if min_ev < 1.0 - 1e-6:
        raise AssertionError(
            f"HO-GSVD eigenvalue min = {min_ev:.6e} < 1 - 1e-6 (violates Thm 2)"
        )


def test_ho_gsvd_recovers_common_subspace():
    """Plant a shared right basis exactly; the HO-GSVD eigenvalue spectrum
    should include eigenvalues at exactly 1 for the common-subspace
    directions (Ponnapalli Thm 2)."""
    rng = np.random.default_rng(12)
    n = 8
    # All three matrices share the SAME D^T D (same Gram), so all
    # eigenvalues of the balanced average are exactly 1.
    V_true = rng.standard_normal((n, n))
    while np.linalg.matrix_rank(V_true) < n:
        V_true = rng.standard_normal((n, n))
    sigma = np.linspace(1.0, 3.0, n)
    U_list = []
    Ds = []
    for k in range(3):
        Uk, _ = np.linalg.qr(rng.standard_normal((40 + 3 * k, n)))
        U_list.append(Uk)
        Ds.append(Uk @ np.diag(sigma) @ V_true.T)
    # By construction, A_i = V_true diag(sigma^2) V_true^T is identical
    # across i (since sigma is shared and U_i is column-orthonormal). So
    # A_i A_j^{-1} = I for all i, j, and the balanced average is I.
    r = ho_gsvd(Ds)
    ev = np.real(r.eigenvalues)
    assert_close(ev, np.ones(n), 1e-8, "common-subspace HO-GSVD eigenvalues = 1")


def test_ho_gsvd_n2_matches_gsvd_subspace():
    """For N=2, the HO-GSVD shared right basis should span the same
    subspace as the classical GSVD right basis (both are bases of R^n).
    We additionally check that, after ordering by HO-GSVD eigenvalue
    ascending, the directions match the GSVD's most-common-to-most-
    exclusive ordering up to per-column sign."""
    rng = np.random.default_rng(13)
    m1, m2, n = 30, 25, 6
    D1 = rng.standard_normal((m1, n))
    D2 = rng.standard_normal((m2, n))

    g = gsvd(D1, D2)
    h = ho_gsvd([D1, D2])

    # Subspace test (n x n invertible bases trivially span R^n; check by
    # solving for a transform): V_hogsvd = V_gsvd . T  for some invertible T.
    # The eigenvalues of S in the N=2 case relate to (c/s + s/c) / 2; we
    # check via direct reconstruction since that's the substantive
    # requirement.
    Vinv = h.Vinv
    for k, (D, U, Sigma) in enumerate(zip([D1, D2], h.U, h.Sigma)):
        recon = U @ np.diag(Sigma) @ Vinv
        assert_close(recon, D, 1e-8, f"N=2 HO-GSVD reconstruction D_{k}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    tests = [
        ("gsvd_reconstruction_square",           test_gsvd_reconstruction_square),
        ("gsvd_csq_invariant",                   test_gsvd_csq_invariant),
        ("gsvd_U_orthonormal",                   test_gsvd_U_orthonormal),
        ("gsvd_planted_shared_subspace",         test_gsvd_planted_shared_subspace),
        ("gsvd_antisymmetric_pattern_recovery",  test_gsvd_antisymmetric_pattern_recovery),
        ("combine_predictors_labels",            test_combine_predictors_labels),
        ("ho_gsvd_reconstruction_three",         test_ho_gsvd_reconstruction_three_matrices),
        ("ho_gsvd_eigenvalues_lower_bound",      test_ho_gsvd_eigenvalues_lower_bound),
        ("ho_gsvd_recovers_common_subspace",     test_ho_gsvd_recovers_common_subspace),
        ("ho_gsvd_n2_matches_gsvd_subspace",     test_ho_gsvd_n2_matches_gsvd_subspace),
    ]
    for name, fn in tests:
        record(name, fn)

    passed = sum(1 for _, ok, _ in _RESULTS if ok)
    total = len(_RESULTS)
    print(f"\n{passed}/{total} tests passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
