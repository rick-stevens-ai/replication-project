"""Classical brute-force enumeration to identify the marked keys in the
paper's Grover instance. The paper claims:

  With one pair (M, C) where M = [0,1,1,1,0,1], C = [0,1,1,1,1,1],
  Grover's histogram shows two peaks: K = [0,0,1,1,1,0] (the real key)
  and K' = [1,1,1,0,0,0] (a collision).

  With a second pair (M1, C1) = ([0,0,1,1,0,1], [1,1,0,0,1,1]),
  the histogram again shows two peaks: K and K'' = [0,0,1,0,0,1].

  The intersection is uniquely K.

Let's verify this classically before we bother building the Grover circuit.
"""

from simon_classical import bits_to_int, int_to_bits, encrypt, N

# Pair 1
M1_bits = [0, 1, 1, 1, 0, 1]
C1_bits = [0, 1, 1, 1, 1, 1]
# Pair 2
M2_bits = [0, 0, 1, 1, 0, 1]
C2_bits = [1, 1, 0, 0, 1, 1]

# Bits split as [L(0..2), R(0..2)] and [k0(0..2), k1(0..2)]
def split_state(bits6):
    L = bits_to_int(bits6[0:3])
    R = bits_to_int(bits6[3:6])
    return L, R

def split_key(bits6):
    k0 = bits_to_int(bits6[0:3])
    k1 = bits_to_int(bits6[3:6])
    return k0, k1

L01, R01 = split_state(M1_bits)
Lc1, Rc1 = split_state(C1_bits)
L02, R02 = split_state(M2_bits)
Lc2, Rc2 = split_state(C2_bits)

print(f"Pair 1: M=(L={L01:03b}, R={R01:03b}) -> C=(L={Lc1:03b}, R={Rc1:03b})")
print(f"Pair 2: M=(L={L02:03b}, R={R02:03b}) -> C=(L={Lc2:03b}, R={Rc2:03b})")

# The claimed true key K = [0,0,1,1,1,0] under LSB-first
K_bits = [0, 0, 1, 1, 1, 0]
Kk0, Kk1 = split_key(K_bits)
print(f"\nClaimed true key K = {K_bits} -> k0={Kk0:03b}, k1={Kk1:03b}")

# Sanity: encrypt pair 1 under K
Le, Re = encrypt(L01, R01, Kk0, Kk1, num_rounds=4)
print(f"encrypt(pair1, K) -> L={Le:03b} R={Re:03b}  "
      f"(want L={Lc1:03b} R={Rc1:03b})  match={Le==Lc1 and Re==Rc1}")
Le, Re = encrypt(L02, R02, Kk0, Kk1, num_rounds=4)
print(f"encrypt(pair2, K) -> L={Le:03b} R={Re:03b}  "
      f"(want L={Lc2:03b} R={Rc2:03b})  match={Le==Lc2 and Re==Rc2}")

# Enumerate all 64 keys and see which encrypt(pair1) -> C1
print("\nAll keys K such that encrypt(pair1, K) == C1:")
matches1 = []
for k0 in range(1 << N):
    for k1 in range(1 << N):
        Le, Re = encrypt(L01, R01, k0, k1, num_rounds=4)
        if Le == Lc1 and Re == Rc1:
            kbits = int_to_bits(k0, 3) + int_to_bits(k1, 3)
            matches1.append((k0, k1, kbits))
            print(f"  k0={k0:03b} k1={k1:03b}  as list = {kbits}")

print(f"\nCount: {len(matches1)} keys match pair 1.")

# Which ones ALSO match pair 2?
print("\nAll keys K such that encrypt(pair2, K) == C2:")
matches2 = []
for k0 in range(1 << N):
    for k1 in range(1 << N):
        Le, Re = encrypt(L02, R02, k0, k1, num_rounds=4)
        if Le == Lc2 and Re == Rc2:
            kbits = int_to_bits(k0, 3) + int_to_bits(k1, 3)
            matches2.append((k0, k1, kbits))
            print(f"  k0={k0:03b} k1={k1:03b}  as list = {kbits}")

print(f"\nCount: {len(matches2)} keys match pair 2.")

# Intersection
common = set((a, b) for (a, b, _) in matches1) & set((a, b) for (a, b, _) in matches2)
print(f"\nIntersection (keys matching BOTH pairs): {len(common)} keys")
for (k0, k1) in sorted(common):
    kbits = int_to_bits(k0, 3) + int_to_bits(k1, 3)
    print(f"  k0={k0:03b} k1={k1:03b}  as list = {kbits}")
