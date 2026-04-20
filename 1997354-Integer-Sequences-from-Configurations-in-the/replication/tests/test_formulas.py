"""
Test suite: verify formula implementations against brute-force and closed forms.
"""
import sys
sys.path.insert(0, "../src")

from edge_covers import (E, E1, E2_1, E2_2, E2_3,
                          E3_1, E3_2, E3_3, E3_4, E3_5, E3_6,
                          E1_closed, E2_1_closed, E2_2_closed, E2_3_closed)
from brute_force import (E_brute, E1_brute, E2_1_brute, E2_2_brute, E2_3_brute,
                          E3_1_brute, E3_2_brute, E3_3_brute, 
                          E3_4_brute, E3_5_brute, E3_6_brute)


def test_E_vs_brute():
    """Test E(m,n) formula against brute force for small cases."""
    print("Testing E(m,n) vs brute force...")
    for m in range(1, 5):
        for n in range(1, 5):
            formula = E(m, n)
            brute = E_brute(m, n)
            assert formula == brute, f"E({m},{n}): formula={formula}, brute={brute}"
    print("  ✅ E(m,n) matches brute force for m,n ∈ [1,4]")


def test_E_known_values():
    """Test E(m,n) against known values (A048291 for square case)."""
    # A048291: 1, 7, 265, 41503, 24997921, ...
    known_square = [1, 7, 265, 41503, 24997921]
    print("Testing E(n,n) against A048291...")
    for i, expected in enumerate(known_square):
        n = i + 1
        computed = E(n, n)
        assert computed == expected, f"E({n},{n}): computed={computed}, expected={expected}"
    print(f"  ✅ E(n,n) matches A048291 for n=1..{len(known_square)}")


def test_E1_vs_brute():
    """Test E₁(m,n) against brute force."""
    print("Testing E1(m,n) vs brute force...")
    for m in range(2, 5):
        for n in range(m, m + 3):
            formula = E1(m, n)
            brute = E1_brute(m, n)
            assert formula == brute, f"E1({m},{n}): formula={formula}, brute={brute}"
    print("  ✅ E1(m,n) matches brute force")


def test_E1_closed_forms():
    """Test E₁(m,n) recursive formula against closed forms."""
    print("Testing E1(m,n) closed forms...")
    for m in range(2, 7):
        for n in range(m, m + 8):
            recursive = E1(m, n)
            closed = E1_closed(m, n)
            assert recursive == closed, f"E1({m},{n}): recursive={recursive}, closed={closed}"
    print("  ✅ E1(m,n) closed forms match recursive for m=2..6")


def test_E2_vs_brute():
    """Test E_{2_k}(m,n) against brute force."""
    print("Testing E2_k(m,n) vs brute force...")
    
    for m in range(2, 5):
        for n in range(m, m + 2):
            f = E2_1(m, n); b = E2_1_brute(m, n)
            assert f == b, f"E2_1({m},{n}): formula={f}, brute={b}"
    print("  ✅ E2_1 matches brute force")
    
    for m in range(3, 5):
        for n in range(m, m + 2):
            f = E2_2(m, n); b = E2_2_brute(m, n)
            assert f == b, f"E2_2({m},{n}): formula={f}, brute={b}"
    print("  ✅ E2_2 matches brute force")
    
    for m in range(2, 5):
        for n in range(m, m + 2):
            f = E2_3(m, n); b = E2_3_brute(m, n)
            assert f == b, f"E2_3({m},{n}): formula={f}, brute={b}"
    print("  ✅ E2_3 matches brute force")


def test_E2_closed_forms():
    """Test E_{2_k} closed forms."""
    print("Testing E2_k closed forms...")
    
    for m in range(2, 7):
        for n in range(m, m + 6):
            assert E2_1(m, n) == E2_1_closed(m, n), f"E2_1({m},{n}) mismatch"
    print("  ✅ E2_1 closed forms match")
    
    for m in range(3, 7):
        for n in range(m, m + 6):
            assert E2_2(m, n) == E2_2_closed(m, n), f"E2_2({m},{n}) mismatch"
    print("  ✅ E2_2 closed forms match")
    
    for m in range(2, 7):
        for n in range(m, m + 6):
            assert E2_3(m, n) == E2_3_closed(m, n), f"E2_3({m},{n}) mismatch"
    print("  ✅ E2_3 closed forms match")


def test_E3_vs_brute():
    """Test E_{3_k}(m,n) against brute force (small cases only — slow!)."""
    print("Testing E3_k(m,n) vs brute force (small cases)...")
    
    # E3_1: needs n≥3
    for m in range(2, 4):
        for n in range(max(m, 3), max(m, 3) + 2):
            f = E3_1(m, n); b = E3_1_brute(m, n)
            assert f == b, f"E3_1({m},{n}): formula={f}, brute={b}"
    print("  ✅ E3_1 matches brute force")
    
    # E3_2: needs m≥3, n≥3
    for n in range(3, 5):
        f = E3_2(3, n); b = E3_2_brute(3, n)
        assert f == b, f"E3_2(3,{n}): formula={f}, brute={b}"
    print("  ✅ E3_2 matches brute force")
    
    # E3_3: needs m≥3
    for n in range(3, 5):
        f = E3_3(3, n); b = E3_3_brute(3, n)
        assert f == b, f"E3_3(3,{n}): formula={f}, brute={b}"
    print("  ✅ E3_3 matches brute force")
    
    # E3_4: needs m≥2, n≥3
    for m in range(2, 4):
        for n in range(max(m, 3), max(m, 3) + 2):
            f = E3_4(m, n); b = E3_4_brute(m, n)
            assert f == b, f"E3_4({m},{n}): formula={f}, brute={b}"
    print("  ✅ E3_4 matches brute force")
    
    # E3_5: needs m≥3, n≥2
    for n in range(3, 5):
        f = E3_5(3, n); b = E3_5_brute(3, n)
        assert f == b, f"E3_5(3,{n}): formula={f}, brute={b}"
    print("  ✅ E3_5 matches brute force")
    
    # E3_6: needs m≥2, n≥2
    for m in range(2, 4):
        for n in range(m, m + 2):
            f = E3_6(m, n); b = E3_6_brute(m, n)
            assert f == b, f"E3_6({m},{n}): formula={f}, brute={b}"
    print("  ✅ E3_6 matches brute force")


def test_symmetry():
    """E(m,n) should equal E(n,m) by transposition."""
    print("Testing E(m,n) = E(n,m) symmetry...")
    for m in range(1, 8):
        for n in range(m, 8):
            assert E(m, n) == E(n, m), f"E({m},{n}) ≠ E({n},{m})"
    print("  ✅ Symmetry holds")


if __name__ == "__main__":
    print("=" * 60)
    print("FORMULA VERIFICATION TEST SUITE")
    print("=" * 60)
    
    test_E_known_values()
    test_E_vs_brute()
    test_symmetry()
    test_E1_vs_brute()
    test_E1_closed_forms()
    test_E2_vs_brute()
    test_E2_closed_forms()
    test_E3_vs_brute()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)
