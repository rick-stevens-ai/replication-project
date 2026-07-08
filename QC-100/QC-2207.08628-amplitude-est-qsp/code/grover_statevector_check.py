"""Verify the Chebyshev identity for the Grover operator using a real numpy statevector simulator.

For a state |psi> = a|good> + sqrt(1-a^2)|bad> and Grover operator G = -Z_psi Z_Pi
(reflection about |psi> followed by reflection about |good>, times -1),
the probability of measuring |good> after k applications of G on |psi> is:

    P_meas(k) = sin^2((2k+1) theta)   where a = sin(theta)

In the paper's phrasing, sampling from the polynomial P(a) = T_{2k+1}(a) gives
Pr[heads] = |T_{2k+1}(a)|^2 ... but the exact identity used is
    sin((2k+1) theta) = U_{2k}(cos theta) * sin(theta), etc.

Here we just verify the *cos-form* Chebyshev relation on which IQAE/ChebAE sample:
    Pr[T_d has value squared] = |T_d(a)|^2   for d odd (via the standard Grover-good-measurement)

We do it with an EXPLICIT statevector on 1 qubit (the trivial two-level subspace)
and confirm that repeated Grover iterations produce the Chebyshev-of-arcsin relation.
"""
import numpy as np

def build_grover_ops(a):
    """Build the 2x2 Grover reflections on the {|good>, |bad>} subspace.

    |psi> = a|good> + sqrt(1-a^2)|bad>
    Z_Pi = I - 2|good><good|   (reflection about the bad-space)
    Z_psi = 2|psi><psi| - I    (reflection about psi)
    G = -Z_psi Z_Pi            (Grover iterate; standard convention)
    """
    good = np.array([1.0, 0.0])
    psi  = np.array([a, np.sqrt(1.0 - a*a)])
    Z_Pi  = np.eye(2) - 2*np.outer(good, good)
    Z_psi = 2*np.outer(psi, psi) - np.eye(2)
    G = -Z_psi @ Z_Pi
    return psi, G

def grover_good_prob(a, k):
    """Probability of measuring |good> after k Grover iterations starting from |psi>."""
    psi, G = build_grover_ops(a)
    state = psi.copy()
    for _ in range(k):
        state = G @ state
    # amplitude on |good> is state[0]
    return float(state[0]**2)

def theory_prob(a, k):
    """Theoretical: sin^2((2k+1) arcsin a)."""
    theta = np.arcsin(a)
    return float(np.sin((2*k+1)*theta)**2)

def main():
    print("=" * 72)
    print("Statevector-Grover -> Chebyshev-of-arcsin identity check")
    print("=" * 72)
    print(f"{'a':>8} {'k':>4} {'P_sv(good)':>14} {'sin^2((2k+1)θ)':>18} {'|diff|':>12}")
    max_err = 0.0
    for a in [0.1, 0.3, 0.5, 0.7, 0.9]:
        for k in [0, 1, 2, 3, 5, 8]:
            p_sv    = grover_good_prob(a, k)
            p_theo  = theory_prob(a, k)
            diff    = abs(p_sv - p_theo)
            max_err = max(max_err, diff)
            print(f"{a:>8.3f} {k:>4d} {p_sv:>14.8f} {p_theo:>18.8f} {diff:>12.2e}")
    print("=" * 72)
    print(f"Max |P_statevector - P_theory| = {max_err:.3e}")
    print(f"Identity verified: {'YES' if max_err < 1e-10 else 'NO'}")
    return max_err

if __name__ == "__main__":
    err = main()
    import json, sys, pathlib
    out = {"max_err": err, "identity_verified": err < 1e-10}
    p = pathlib.Path(__file__).resolve().parent.parent / "report" / "evidence"
    p.mkdir(parents=True, exist_ok=True)
    (p / "grover_chebyshev_identity.json").write_text(json.dumps(out, indent=2))
    print(f"[wrote] {p/'grover_chebyshev_identity.json'}")
    sys.exit(0 if err < 1e-10 else 1)
