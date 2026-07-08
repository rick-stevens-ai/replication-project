#!/usr/bin/env python3
"""
Sanity check for the F_XEB numbers:
  E_{x~q}[2^n q(x) - 1] = 2^n * Sum_x q(x)^2 - 1 = 2^n * CP(q) - 1

For deep Haar-random circuits (Porter-Thomas):
  E[CP(q)] = 2 / (2^n + 1)   =>   E[F] = 2*2^n/(2^n+1) - 1  ->  1

For shallow circuits the distribution q is much more concentrated (higher CP),
so exact-sampling F_XEB is > 1. This is the very effect the paper's spoofer
exploits: shallow q has structure => a small-light-cone algorithm can pin
that structure and get F >> 0.
"""
import numpy as np
import cirq
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xeb_experiment import brickwall_1d_circuit, probabilities

def main():
    rng = np.random.default_rng(20260703)
    print(f"{'n':>3} {'d':>3} {'CP(q)':>10} {'2^n*CP-1':>12} {'PT_expect':>12}")
    for n in [4, 6, 8]:
        for d in [1, 2, 3, 4, 6, 10]:
            cps, fs = [], []
            for _ in range(40):
                circ = brickwall_1d_circuit(n, d, rng)
                q = probabilities(circ, n)
                cp = float(np.sum(q * q))
                cps.append(cp)
                fs.append((1 << n) * cp - 1.0)
            pt_expect = 2.0 * (1 << n) / ((1 << n) + 1) - 1.0
            print(f"{n:>3} {d:>3} {np.mean(cps):>10.4f} "
                  f"{np.mean(fs):>12.4f} {pt_expect:>12.4f}")

if __name__ == "__main__":
    main()
