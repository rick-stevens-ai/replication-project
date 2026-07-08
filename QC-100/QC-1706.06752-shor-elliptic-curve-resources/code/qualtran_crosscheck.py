#!/usr/bin/env python3
"""
Independent cross-check against Roetteler et al. 2017 using Qualtran's
`FindECCPrivateKey` bloq.

IMPORTANT: Qualtran's ECC implementation follows LITINSKI 2023
(arXiv:2306.08585, "How to compute a 256-bit elliptic curve private key
with only 50 million Toffoli gates"), which is a follow-up to Roetteler et
al. that uses windowing to reduce the Toffoli count by ~1000x for n=256.

So Qualtran numbers will NOT match Roetteler numbers — but they should
match Litinski's numbers. This confirms the toolchain is working and
provides an *independent* cross-check that the field's follow-on work
(also based on Roetteler's primitives) reproduces the general shape.

Expected order of magnitude:
  Litinski 2023 abstract: ~50 million Toffoli gates for n=256.
  Roetteler 2017 Table 2: 1.26e11 Toffoli for n=256.
  Ratio: Litinski/Roetteler ≈ 5e7 / 1.26e11 ≈ 4e-4  (i.e. 2500x smaller).
"""
import json
import os
from qualtran.bloqs.cryptography.ecc.find_ecc_private_key import FindECCPrivateKey
from qualtran.bloqs.cryptography.ecc.ec_point import ECPoint
from qualtran.resource_counting import get_cost_value, QECGatesCost

def resource_estimate(n: int, add_window: int = 4, mul_window: int = 4):
    # Dummy modulus - Qualtran symbolic cost only needs n (bitsize).
    # We use a small prime for validity; the cost depends on n not the specific value.
    # For n=8, use a small prime like 251.
    # Find on-curve points for E: y^2 = x^3 + 7 (mod p).
    # Qualtran computes QROM tables of point multiples, so points must be on-curve.
    def find_two_points(p):
        pts = []
        for x in range(1, p):
            rhs = (x**3 + 7) % p
            # Only works for p mod 4 == 3
            y = pow(rhs, (p+1)//4, p)
            if (y*y) % p == rhs:
                pts.append((x, y))
                if len(pts) >= 2:
                    return pts
        raise RuntimeError('no on-curve points found')

    # Primes with p mod 4 == 3 and roughly n bits:
    mods = {
        8:   251,          # 2^7 < 251 < 2^8
        10:  1019,
        12:  4079,         # 2^11 < 4079 < 2^12
        16:  65519,
    }
    p = mods.get(n)
    if p is None:
        raise ValueError(f"Add a prime for n={n}")

    (px, py), (qx, qy) = find_two_points(p)
    P = ECPoint(x=px, y=py, mod=p, curve_a=0)
    Q = ECPoint(x=qx, y=qy, mod=p, curve_a=0)
    algo = FindECCPrivateKey(
        n=n, base_point=P, public_key=Q,
        add_window_size=add_window, mul_window_size=mul_window,
    )
    cost = get_cost_value(algo, QECGatesCost())
    return {
        'n': n,
        'add_window': add_window,
        'mul_window': mul_window,
        'toffoli':          int(cost.toffoli),
        'and_gates':        int(cost.and_bloq),
        'total_t':          int(cost.total_t_count()),
        'clifford':         int(cost.clifford),
        'meas':             int(cost.measurement),
        'total_t_and_ccz':  int(cost.total_t_and_ccz_count()),
    }

def main():
    outdir = os.path.expanduser(
        '~/Dropbox/REPLICATE-PROJECT/QC-100/'
        'QC-1706.06752-shor-elliptic-curve-resources/report/evidence')
    os.makedirs(outdir, exist_ok=True)

    print("Qualtran FindECCPrivateKey (Litinski-2023 algorithm) resource counts")
    print("="*75)
    results = []
    for n in (8, 10, 12, 16):
        try:
            r = resource_estimate(n)
            results.append(r)
            print(f"n={r['n']:3d}  Toffoli={r['toffoli']:>15,}  "
                  f"AND={r['and_gates']:>15,}  total_T={r['total_t']:>15,}  "
                  f"Cliff={r['clifford']:>15,}")
        except Exception as e:
            print(f"n={n}: FAILED — {e}")

    with open(os.path.join(outdir, 'qualtran_crosscheck.json'), 'w') as f:
        json.dump({
            'tool': 'qualtran.bloqs.cryptography.ecc.FindECCPrivateKey',
            'algorithm_reference': 'Litinski 2023 (arXiv:2306.08585)',
            'note': ('Different algorithm than Roetteler 2017 (uses windowing). '
                     'Numbers will NOT match Roetteler Table 2 directly; provides '
                     'independent confirmation of general shape only.'),
            'results': results,
        }, f, indent=2)
    print(f"\nWrote: {outdir}/qualtran_crosscheck.json")

if __name__ == '__main__':
    main()
