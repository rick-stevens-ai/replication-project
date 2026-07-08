#!/usr/bin/env python
"""Theoretical predictions for f_std and b_real under our real-diagonal noise
channel, to compare to simulation fits.

Noise: E(rho) = (1-p) rho + (p/2) X rho X + (p/2) Z rho Z
Pauli error probs: p_I = 1-p, p_X = p/2, p_Y = 0, p_Z = p/2.

Standard 1-qubit Clifford RB fitted decay rate (Magesan et al.):
  f_std = 1 - (2*r), where r = (d-1)/d * (1 - F_avg)
  For a Pauli channel:  F_avg = 1 - (d-1)/(d) * sum_{P != I} p_P
                       = 1 - (1/2) * (p_X + p_Y + p_Z)  for d=2
                       = 1 - (1/2) * p
  So r = (1/2) * (1 - F_avg) = (1/2) * (1/2) * p  = p/4
  f_std = 1 - 2r = 1 - p/2

Wait that's not what we see (f_std=0.9737 for p=0.02 would predict 1 - 0.01 = 0.99).
Let me redo more carefully.

The standard "average gate infidelity" r under a Pauli channel is:
   r = (d-1)/(d(d+1)) * sum_{P != I} 2 * p_P   (from Magesan derivation for Cliffords twirl)
Actually the simplest is:
   For depolarizing channel D_p(rho) = (1-p) rho + p * I/d,
   Clifford twirl gives f = 1 - p * d/(d-1)  ->  r = (d-1)/d * (1-f) = p
   So r = p directly for standard depolarizing.

Our noise is *not* fully depolarizing (missing Y). Under a general Pauli channel with
weights (p_I, p_X, p_Y, p_Z), the Pauli-twirl equals itself (Clifford twirl on a Pauli
channel returns a depolarizing channel with same average):
   avg-fidelity F = <psi|E(|psi><psi|)|psi> avg over Haar states
                  = (1/(d+1)) * (Tr(E) / d + 1)   [Nielsen formula]
   where Tr(E) is the trace of the process matrix.
For a Pauli channel, F = sum_P p_P * |Tr(P^2)|^2 / (d^2*(d+1)) ... complicated.

Cleaner: for a single-qubit Pauli channel with probs (p_I, p_X, p_Y, p_Z),
   entanglement fidelity F_e = p_I
   average gate fidelity F_avg = (d * F_e + 1) / (d + 1) = (2*p_I + 1)/3
   average gate infidelity r = 1 - F_avg = (2*(1-p_I))/3 = 2p/3  where p = p_X+p_Y+p_Z
   standard RB decay f = 1 - r * d/(d-1) = 1 - 2r = 1 - 4p/3

For our channel: p = p_X + p_Z = 0.02, so
   f_std = 1 - 4*0.02/3 = 1 - 0.02667 = 0.9733

That matches our fit (0.9737 +/- 0.0005) beautifully.

Real Clifford RB decay parameter b:
Paper eq. (35): F_R(E, id) = (b*(d-1) + 1)/d
For d=2:  F_R = (b + 1)/2  ->  b = 2 F_R - 1
F_R (real fidelity, averaged over real states) for a Pauli channel with only
X and Z errors... Real states |psi> have real amplitudes, so
   E(|psi><psi|) = (1-p)|psi><psi| + (p_X/1)X|psi><psi|X + (p_Z/1)Z|psi><psi|Z
where the Y term is 0.
   F(psi) = <psi|E(|psi><psi|)|psi> = 1 - p + p_X |<psi|X|psi>|^2 + p_Z |<psi|Z|psi>|^2
Averaging over the real orthogonal group O(2) acting on |psi>:
   avg |<psi|X|psi>|^2 = 1/d for depolarizing over real states... but the trick is that
   for real qubit states parameterized by |psi> = cos(t)|0> + sin(t)|1>,
     |<psi|X|psi>|^2 = |2 sin t cos t|^2 = sin^2(2t)   -> avg over t in [0, 2pi) = 1/2
     |<psi|Z|psi>|^2 = |cos^2 - sin^2|^2 = cos^2(2t)   -> avg over t in [0, 2pi) = 1/2
     |<psi|Y|psi>|^2 = 0 for real psi
Sum: F_R = 1 - p + p_X * (1/2) + p_Z * (1/2) = 1 - p + p/2 = 1 - p/2
So b = 2 * F_R - 1 = 2*(1 - p/2) - 1 = 1 - p = 0.98 for p=0.02.

Our fit: b = 0.9795 +/- 0.0004  -> essentially matches 0.98 (well within stat error).

Real-RB average infidelity: r_R = (d-1)/d * (1 - b) = (1/2)(1 - 0.98) = 0.01.
Our fit: r_R = 0.0103 +/- 0.0002.

Summary:
   Standard RB:  predicted f = 0.9733, fitted f = 0.9737 +/- 0.0005  -> MATCH
                 predicted r = 0.01333, fitted r = 0.0132  +/- 0.0002 -> MATCH
   Real RB:      predicted b = 0.98,   fitted b = 0.9795 +/- 0.0004  -> MATCH
                 predicted r_R = 0.01, fitted r_R = 0.0103 +/- 0.0002 -> MATCH
   Efficiency: real RB with 10 sequences/length gave same b (0.9795 +/- 0.0004)
              as with 30 sequences. Standard RB with 30 sequences gave r+/-0.0002.
              Real RB with 10 sequences (3x fewer, matching group size ratio 8/24)
              still gave r_R +/- 0.0002. => Comparable-or-better statistical
              precision per unit of experimental effort => confirms paper's
              efficiency claim.
"""

import numpy as np

p = 0.02
d = 2

# Standard Clifford RB predictions
f_std_pred = 1 - 4 * p / 3
r_std_pred = (d - 1) / d * (1 - f_std_pred)

# Real Clifford RB predictions
b_real_pred = 1 - p
r_real_pred = (d - 1) / d * (1 - b_real_pred)

# Fitted values from run
f_std_fit, f_std_err = 0.9737, 0.0005
r_std_fit, r_std_err = 0.0132, 0.0002
b_real_fit, b_real_err = 0.9795, 0.0004
r_real_fit, r_real_err = 0.0103, 0.0002

def report(label, pred, fit, err):
    delta = fit - pred
    sigmas = abs(delta) / err if err > 0 else float('inf')
    verdict = 'MATCH' if sigmas < 3.0 else 'MISMATCH'
    print(f"  {label:20s}  pred={pred:.4f}  fit={fit:.4f} +/- {err:.4f}  (delta={delta:+.4f}, {sigmas:.1f}sigma)  {verdict}")

print(f"Injected p = {p}\n")
print("Standard Clifford RB:")
report("f_std",  f_std_pred, f_std_fit, f_std_err)
report("r_std",  r_std_pred, r_std_fit, r_std_err)
print("Real Clifford RB:")
report("b_real", b_real_pred, b_real_fit, b_real_err)
report("r_real", r_real_pred, r_real_fit, r_real_err)

print("\nSeparation:")
print(f"  r_std ({r_std_fit:.4f}) != r_real ({r_real_fit:.4f})  ->  real RB isolates the")
print(f"  'real-diagonal' error component; the difference r_std - r_real = {r_std_fit - r_real_fit:.4f}")
print(f"  reflects the fact that standard RB averages over all 3 Pauli directions while")
print(f"  real RB averages only over the real X,Z sector.")
