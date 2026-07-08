#!/usr/bin/env python3
"""
Replication of the core claim of:
  Temme, Bravyi, Gambetta, "Error mitigation for short-depth quantum circuits",
  PRL 119, 180509 (2017).

Core claim tested here (the Zero-Noise Extrapolation / ZNE method):
  By running a noisy circuit at SEVERAL amplified noise levels lambda = c*lambda0
  and Richardson-extrapolating the measured expectation value E(lambda) to
  lambda -> 0, one obtains an estimate of the noiseless expectation value whose
  bias is suppressed to high order in the base noise rate, dramatically reducing
  error vs the raw noisy value.

Method: exact density-matrix simulator (numpy), depolarizing noise channel.
No quantum framework needed -> fully reproducible.

We:
  1. Build a small circuit (n=2 qubits) preparing a Bell-ish state and measure
     <Z0 Z1> (and a single-qubit <Z> test).
  2. Apply a depolarizing channel after each gate with base rate p0, and amplify
     noise by integer "stretch" factors c (the canonical unitary-folding idea:
     noise scales ~ linearly with circuit depth, so folding G->G G^dag G triples
     the accumulated depolarizing error). We emulate that by setting per-circuit
     effective rate p_eff(c) = c * p0.
  3. Measure E(c) for c = 1,2,3 (and more), Richardson + linear + exponential
     extrapolate to c->0, compare to ideal.
  4. Report error-reduction factor.
"""
import numpy as np
import itertools, json

# ---- single/two qubit operators ----
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

def kron(*ops):
    out = np.array([[1]], dtype=complex)
    for o in ops:
        out = np.kron(out, o)
    return out

def depolarize_1q(rho, q, n, p):
    """Apply single-qubit depolarizing channel with prob p on qubit q (of n)."""
    paulis = [I2, X, Y, Z]
    # depolarizing: (1-p) rho + p/3 (X rho X + Y rho Y + Z rho Z)
    full = lambda op: kron(*[op if i==q else I2 for i in range(n)])
    out = (1-p)*rho
    for P in (X, Y, Z):
        FP = full(P)
        out = out + (p/3.0)*(FP @ rho @ FP.conj().T)
    return out

def apply_unitary(rho, U):
    return U @ rho @ U.conj().T

def run_circuit(p):
    """
    2-qubit circuit: H on q0, CNOT(0->1)  -> Bell state |00>+|11>.
    Depolarizing noise rate p applied after each gate on the involved qubit(s).
    Returns <Z0 Z1> expectation (ideal = +1) and <Z0> (ideal = 0).
    """
    n = 2
    # initial |00><00|
    rho = np.zeros((4,4), dtype=complex); rho[0,0] = 1.0
    # gate 1: H on q0
    U_H0 = kron(H, I2)
    rho = apply_unitary(rho, U_H0)
    rho = depolarize_1q(rho, 0, n, p)
    # gate 2: CNOT 0->1
    CNOT = np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,0,1],
                     [0,0,1,0]], dtype=complex)
    rho = apply_unitary(rho, CNOT)
    rho = depolarize_1q(rho, 0, n, p)
    rho = depolarize_1q(rho, 1, n, p)
    # observables
    Z0Z1 = kron(Z, Z)
    Z0   = kron(Z, I2)
    ezz = np.real(np.trace(rho @ Z0Z1))
    ez0 = np.real(np.trace(rho @ Z0))
    return ezz, ez0

def richardson_extrapolate(cs, ys):
    """
    Richardson extrapolation to c=0 using the standard finite-difference
    coefficients for the set of scale factors cs (Mitiq's RichardsonFactory).
    Fit a degree (len-1) polynomial in c, evaluate at 0.
    """
    coeffs = np.polyfit(cs, ys, deg=len(cs)-1)
    return np.polyval(coeffs, 0.0)

def linear_extrapolate(cs, ys):
    coeffs = np.polyfit(cs, ys, deg=1)
    return np.polyval(coeffs, 0.0)

def exp_extrapolate(cs, ys, ideal_guess=1.0):
    """E(c) = a - b*exp(k*c) style; fit log of (offset - y). Fall back to linear."""
    cs = np.asarray(cs, float); ys = np.asarray(ys, float)
    # model y = A + B*exp(-r c). Use a simple 3-param fit via least squares grid on r.
    best = None
    for r in np.linspace(0.05, 3.0, 200):
        Bbasis = np.exp(-r*cs)
        M = np.vstack([np.ones_like(cs), Bbasis]).T
        sol, res, *_ = np.linalg.lstsq(M, ys, rcond=None)
        pred = M @ sol
        err = np.sum((pred-ys)**2)
        if best is None or err < best[0]:
            best = (err, sol[0] + sol[1]*1.0, r)  # value at c=0 is A + B
    return best[1]

def main():
    p0 = 0.02   # base depolarizing rate per gate
    scales = [1, 2, 3]            # noise stretch factors c
    rich_scales = [1, 2, 3, 4, 5]

    ideal_zz, ideal_z0 = run_circuit(0.0)
    print(f"Ideal  <Z0Z1>={ideal_zz:+.6f}  <Z0>={ideal_z0:+.6f}")

    # measured at each scale (effective rate = c*p0)
    meas_zz = {}
    for c in rich_scales:
        zz, z0 = run_circuit(c*p0)
        meas_zz[c] = zz
        print(f"  c={c}  p_eff={c*p0:.3f}  <Z0Z1>={zz:+.6f}  (err {abs(zz-ideal_zz):.4f})")

    raw = meas_zz[1]
    cs3 = scales; ys3 = [meas_zz[c] for c in scales]
    lin = linear_extrapolate(cs3, ys3)
    rich = richardson_extrapolate(rich_scales, [meas_zz[c] for c in rich_scales])
    rich3 = richardson_extrapolate(cs3, ys3)
    expx = exp_extrapolate(rich_scales, [meas_zz[c] for c in rich_scales])

    def err(v): return abs(v - ideal_zz)
    results = {
        "ideal_ZZ": ideal_zz,
        "base_rate_p0": p0,
        "raw_noisy_c1": raw,
        "linear_extrap_c123": lin,
        "richardson_extrap_c123": rich3,
        "richardson_extrap_c12345": rich,
        "exp_extrap": expx,
        "err_raw": err(raw),
        "err_linear": err(lin),
        "err_richardson3": err(rich3),
        "err_richardson5": err(rich),
        "err_exp": err(expx),
        "reduction_factor_richardson5": err(raw)/max(err(rich),1e-12),
        "reduction_factor_linear": err(raw)/max(err(lin),1e-12),
    }
    print("\n=== ZNE results (observable <Z0Z1>, ideal=+1) ===")
    print(f"raw noisy (c=1)        : {raw:+.6f}   error {err(raw):.5f}")
    print(f"linear extrap (c=1,2,3): {lin:+.6f}   error {err(lin):.5f}")
    print(f"Richardson (c=1,2,3)   : {rich3:+.6f}   error {err(rich3):.5f}")
    print(f"Richardson (c=1..5)    : {rich:+.6f}   error {err(rich):.5f}")
    print(f"exp extrap (c=1..5)    : {expx:+.6f}   error {err(expx):.5f}")
    print(f"\nError-reduction factor (raw/Richardson5): {results['reduction_factor_richardson5']:.1f}x")
    print(f"Error-reduction factor (raw/linear)     : {results['reduction_factor_linear']:.1f}x")

    # sweep base rate to show robustness
    print("\n=== robustness sweep: reduction factor vs base rate ===")
    sweep = []
    for p in [0.005, 0.01, 0.02, 0.04, 0.08]:
        iz, _ = run_circuit(0.0)
        ys = [run_circuit(c*p)[0] for c in rich_scales]
        r5 = richardson_extrapolate(rich_scales, ys)
        rawp = ys[0]
        rf = abs(rawp-iz)/max(abs(r5-iz),1e-12)
        sweep.append({"p": p, "raw_err": abs(rawp-iz), "rich_err": abs(r5-iz), "reduction": rf})
        print(f"  p0={p:.3f}: raw_err={abs(rawp-iz):.5f}  rich_err={abs(r5-iz):.6f}  reduction={rf:.1f}x")
    results["sweep"] = sweep

    json.dump(results, open("results.json","w"), indent=2)
    print("\nWrote results.json")

if __name__ == "__main__":
    main()
