"""Classical reference implementation of the reduced SIMON from
Anand, Maitra, Mukhopadhyay 2020 (arXiv:2004.10686), Section 3.3 / Fig 10.

Reduced SIMON parameters:
    word size n = 3
    block size 2n = 6
    key size mn = 6, m = 2 (two 3-bit round keys k0, k1)
    number of rounds T = 4

State update:
    (L_{j+1}, R_{j+1}) = ( R_j XOR (S^1(L_j) & S^2(L_j)) XOR S^0(L_j) XOR k_j , L_j )

Key expansion:
    k_{j+2} = c_j XOR k_j XOR S^{-1}(k_{j+1}) XOR S^{-2}(k_{j+1})
with round constants c_2 = c_3 = [0,0,1].

We represent an n-bit word as a Python int in [0, 2**n). We treat bit 0 as the
LEAST-significant bit of the int (bit-list index 0 == integer bit 0). The
paper's Grover test vectors are given as 6-bit lists in "concatenated" form,
which we take to be [K_bits] = [k0(0), k0(1), k0(2), k1(0), k1(1), k1(2)]
and similarly for plaintext/ciphertext = [L(0), L(1), L(2), R(0), R(1), R(2)].

We rotate on n=3 bits: S^i(x) = ((x << i) | (x >> (n - i))) & mask.
"""

from typing import Tuple, List

N = 3
MASK = (1 << N) - 1  # 0b111


def bits_to_int(bits: List[int]) -> int:
    """Convert a bit-list [b0, b1, b2, ...] (b0 = bit 0 = LSB) to an int."""
    v = 0
    for i, b in enumerate(bits):
        if b:
            v |= (1 << i)
    return v


def int_to_bits(v: int, width: int) -> List[int]:
    return [(v >> i) & 1 for i in range(width)]


def rotl(x: int, i: int) -> int:
    i = i % N
    return ((x << i) | (x >> (N - i))) & MASK


def rotr(x: int, i: int) -> int:
    return rotl(x, N - (i % N))


def round_function(L: int, R: int, k: int) -> Tuple[int, int]:
    """One round of reduced SIMON.

    (L', R') = ( R XOR (S^1(L) & S^2(L)) XOR S^0(L) XOR k , L )
    """
    f = (rotl(L, 1) & rotl(L, 2)) ^ L ^ k  # S^0(L) is L itself
    return (R ^ f, L)


def key_expansion(k0: int, k1: int, num_rounds: int,
                  round_constants=None) -> List[int]:
    """Generate `num_rounds` round keys starting from k0, k1.

    Default round constants c_j (for j >= 2, i.e. producing k_j) are:
      c_2 = c_3 = [0,0,1] = int 4? or int 1?
    The paper writes [0,0,1] in bit-list form. Under our LSB-first convention,
    [0,0,1] = 1*2^2 = 4. We keep it symbolic and let the caller pass values.
    """
    if round_constants is None:
        # c_j is a list keyed by round index j; only c_2, c_3 matter for T=4
        round_constants = {2: 4, 3: 4}  # [0,0,1] in LSB-first
    keys = [k0, k1]
    for j in range(2, num_rounds):
        c = round_constants.get(j, 0)
        prev = keys[j - 1]
        # S^{-1}(prev) = rotr(prev, 1), S^{-2}(prev) = rotr(prev, 2)
        k_new = c ^ keys[j - 2] ^ rotr(prev, 1) ^ rotr(prev, 2)
        keys.append(k_new)
    return keys


def encrypt(L0: int, R0: int, k0: int, k1: int, num_rounds: int = 4,
            round_constants=None) -> Tuple[int, int]:
    keys = key_expansion(k0, k1, num_rounds, round_constants)
    L, R = L0, R0
    for j in range(num_rounds):
        L, R = round_function(L, R, keys[j])
    return L, R


# ---- Test vectors from the paper ----

def paper_test_vector_1():
    """Section 3.3 / Fig 11:

    L0 = [0,1,1], R0 = [1,0,1]
    k0 = [0,0,1], k1 = [1,1,0]
    After 4 rounds -> L4 = [0,1,1], R4 = [1,1,1]
    """
    L0 = bits_to_int([0, 1, 1])  # = 6
    R0 = bits_to_int([1, 0, 1])  # = 5
    k0 = bits_to_int([0, 0, 1])  # = 4
    k1 = bits_to_int([1, 1, 0])  # = 3
    expected_L4 = bits_to_int([0, 1, 1])  # 6
    expected_R4 = bits_to_int([1, 1, 1])  # 7
    return dict(L0=L0, R0=R0, k0=k0, k1=k1,
                expected_L4=expected_L4, expected_R4=expected_R4)


def paper_test_vector_grover():
    """Section 3.4 (Grover): under key K = [0,0,1,1,1,0],
    plaintext M = [0,1,1,1,0,1] encrypts to C = [0,1,1,1,1,1].

    The 6-bit key is split as K = [k0(0..2), k1(0..2)] = [0,0,1] || [1,1,0]
    which matches the 3.3 test vector's keys. The plaintext M is split as
    M = [L0(0..2), R0(0..2)] = [0,1,1] || [1,0,1] — again matches 3.3.
    So the Grover test vector is the SAME instance as vector 1. Good.
    """
    return paper_test_vector_1()


def paper_test_vector_grover_pair2():
    """Second (M1, C1) pair for the two-pair Grover test:
      M1 = [0,0,1,1,0,1], C1 = [1,1,0,0,1,1]
    under the same key K = [0,0,1,1,1,0].
    """
    L0 = bits_to_int([0, 0, 1])  # 4
    R0 = bits_to_int([1, 0, 1])  # 5
    k0 = bits_to_int([0, 0, 1])  # 4
    k1 = bits_to_int([1, 1, 0])  # 3
    expected_L4 = bits_to_int([1, 1, 0])  # 3
    expected_R4 = bits_to_int([0, 1, 1])  # 6
    return dict(L0=L0, R0=R0, k0=k0, k1=k1,
                expected_L4=expected_L4, expected_R4=expected_R4)


def test_all_round_constant_conventions():
    """Try both bit conventions for the round constants and both plausible
    endian conventions for the bit-lists. Return which combination matches
    the paper's stated test vector 1.
    """
    L0_bits = [0, 1, 1]; R0_bits = [1, 0, 1]
    k0_bits = [0, 0, 1]; k1_bits = [1, 1, 0]
    L4_exp = [0, 1, 1]; R4_exp = [1, 1, 1]

    # Convention A: bit-list index 0 = LSB
    A_L0 = bits_to_int(L0_bits); A_R0 = bits_to_int(R0_bits)
    A_k0 = bits_to_int(k0_bits); A_k1 = bits_to_int(k1_bits)
    A_L4_exp = bits_to_int(L4_exp); A_R4_exp = bits_to_int(R4_exp)

    # Convention B: bit-list index 0 = MSB
    def bits_msb(bits):
        v = 0
        for b in bits:
            v = (v << 1) | b
        return v
    B_L0 = bits_msb(L0_bits); B_R0 = bits_msb(R0_bits)
    B_k0 = bits_msb(k0_bits); B_k1 = bits_msb(k1_bits)
    B_L4_exp = bits_msb(L4_exp); B_R4_exp = bits_msb(R4_exp)

    results = []
    for conv_name, L0, R0, k0, k1, L4e, R4e in [
        ("LSB-first (idx 0 = bit 0)", A_L0, A_R0, A_k0, A_k1, A_L4_exp, A_R4_exp),
        ("MSB-first (idx 0 = high bit)", B_L0, B_R0, B_k0, B_k1, B_L4_exp, B_R4_exp),
    ]:
        for rc_bits in [[0, 0, 1]]:
            for rc_conv_name, rc_int in [("LSB-first",
                                           bits_to_int(rc_bits)),
                                          ("MSB-first",
                                           bits_msb(rc_bits))]:
                rc_map = {2: rc_int, 3: rc_int}
                L4, R4 = encrypt(L0, R0, k0, k1, num_rounds=4,
                                 round_constants=rc_map)
                ok = (L4 == L4e and R4 == R4e)
                results.append((conv_name, rc_conv_name, rc_int,
                                L4, R4, L4e, R4e, ok))
    return results


if __name__ == "__main__":
    import json
    print("=== SIMON classical reference — sanity checks ===")
    tv = paper_test_vector_1()
    print(f"Input:  L0={tv['L0']:03b} R0={tv['R0']:03b} "
          f"k0={tv['k0']:03b} k1={tv['k1']:03b}")
    L4, R4 = encrypt(tv['L0'], tv['R0'], tv['k0'], tv['k1'], num_rounds=4)
    print(f"Got:    L4={L4:03b} R4={R4:03b}")
    print(f"Want:   L4={tv['expected_L4']:03b} R4={tv['expected_R4']:03b}")
    print(f"MATCH:  {L4 == tv['expected_L4'] and R4 == tv['expected_R4']}")
    print()

    print("Trying all conventions to find the one that matches:")
    for r in test_all_round_constant_conventions():
        (conv, rc_conv, rc_int, L4, R4, L4e, R4e, ok) = r
        marker = "  <-- MATCH" if ok else ""
        print(f"  state={conv:35s} rc={rc_conv:12s} (int={rc_int}) "
              f"=> L4={L4:03b} R4={R4:03b} vs {L4e:03b} {R4e:03b}{marker}")
