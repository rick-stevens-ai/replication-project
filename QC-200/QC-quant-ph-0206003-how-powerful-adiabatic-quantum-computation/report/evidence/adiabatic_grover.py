#!/usr/bin/env python3
"""
Numerical replication of van Dam, Mosca, Vazirani (quant-ph/0206003),
Section 5 "Quantum Adiabatic Searching".

Reproduces:
  Claim C1: For H(s) = (1-s) H_0 + s H_u where H_u marks 1 item of N=2^n,
            the spectral gap is g(s) = sqrt( (2^n + 4(2^n-1)(s^2 - s)) / 2^n )   (Eq. 1)
            with g(1/2) = 1/sqrt(2^n) = 1/sqrt(N).
  Claim C2: Δ_min ∝ 1/sqrt(N) → fit log(Δ_min) vs log(N) yields slope ≈ -0.5.
  Claim C3: With constant-schedule adiabatic evolution and T = c/Δ_min^2 = c*N,
            success probability -> 1 as c grows (adiabatic theorem), and
            required T is Ω(N) = Ω(2^n)  -- confirming "no speedup" for the
            *constant-schedule* naive adiabatic Grover (the paper then shows
            a *varying* schedule recovers O(sqrt(N))).

Everything is dense-matrix exact diagonalization + Schrödinger integration
via matrix exponential of the piecewise-constant Hamiltonian (Trotter-free
first-order product formula on a fine s-grid). No approximations beyond
grid discretization.
"""
import json
import time
import numpy as np
from numpy.linalg import eigh
from scipy.linalg import expm

OUTDIR = "/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0206003-how-powerful-adiabatic-quantum-computation/report/evidence"


def hadamard_state(n):
    """|0̂^n> = H^{⊗n}|0^n> = uniform superposition over all 2^n basis states."""
    N = 2 ** n
    return np.ones(N, dtype=complex) / np.sqrt(N)


def build_H0(n):
    """H_0 = I - |0̂^n><0̂^n|  (identity in Hadamard basis minus projector on ground = uniform state).
    Ground state is uniform superposition, with eigenvalue 0; all orthogonal Hadamard basis vectors have eigenvalue 1."""
    N = 2 ** n
    psi0 = hadamard_state(n)
    H0 = np.eye(N, dtype=complex) - np.outer(psi0, psi0.conj())
    return H0


def build_Hu(n, u):
    """H_u = I - |u><u|. Ground state |u> with eigenvalue 0."""
    N = 2 ** n
    Hu = np.eye(N, dtype=complex)
    Hu[u, u] -= 1.0
    return Hu


def H_of_s(s, H0, Hu):
    return (1.0 - s) * H0 + s * Hu


def gap_at(s, H0, Hu):
    H = H_of_s(s, H0, Hu)
    ev = np.linalg.eigvalsh(H)
    ev.sort()
    return float(ev[1] - ev[0])


def paper_gap_formula(s, n):
    """Eq. (1) of the paper: g(s) = sqrt( (2^n + 4(2^n-1)(s^2 - s)) / 2^n )."""
    N = 2 ** n
    val = (N + 4.0 * (N - 1) * (s * s - s)) / N
    return float(np.sqrt(val))


def find_min_gap(n, u=0, ns=2001):
    H0 = build_H0(n)
    Hu = build_Hu(n, u)
    s_grid = np.linspace(0.0, 1.0, ns)
    gaps = np.array([gap_at(s, H0, Hu) for s in s_grid])
    imin = int(np.argmin(gaps))
    return {
        "n": n,
        "N": 2 ** n,
        "u": u,
        "s_min": float(s_grid[imin]),
        "delta_min_numeric": float(gaps[imin]),
        "delta_min_paper_formula_at_half": paper_gap_formula(0.5, n),
        "delta_min_paper_formula_at_smin": paper_gap_formula(float(s_grid[imin]), n),
        "s_grid": s_grid,
        "gaps": gaps,
    }


def compare_gap_curve(n, ns=201):
    """Compare numeric gap g(s) to paper formula g(s)=sqrt((N+4(N-1)(s^2-s))/N) at many s."""
    H0 = build_H0(n)
    Hu = build_Hu(n, u=0)
    s_grid = np.linspace(0.0, 1.0, ns)
    g_num = np.array([gap_at(s, H0, Hu) for s in s_grid])
    g_pap = np.array([paper_gap_formula(s, n) for s in s_grid])
    max_abs_err = float(np.max(np.abs(g_num - g_pap)))
    return {
        "n": n,
        "ns": ns,
        "max_abs_err_vs_paper_formula": max_abs_err,
        "min_gap_numeric": float(g_num.min()),
        "min_gap_paper": float(g_pap.min()),
    }


def simulate_adiabatic(n, T, u=0, n_steps=400):
    """Simulate |ψ(t)> for constant-linear schedule s(t)=t/T from t=0 to t=T.
    Piecewise-constant approximation: for each of n_steps intervals of width dt=T/n_steps
    apply U_k = exp(-i H(s_k) dt) where s_k = (k+0.5)/n_steps.
    Return P_success = |<u|ψ(T)>|^2.
    """
    H0 = build_H0(n)
    Hu = build_Hu(n, u)
    psi = hadamard_state(n)
    dt = T / n_steps
    for k in range(n_steps):
        s = (k + 0.5) / n_steps
        H = H_of_s(s, H0, Hu)
        U = expm(-1j * H * dt)
        psi = U @ psi
    p_success = float(np.abs(psi[u]) ** 2)
    return p_success


def main():
    t0 = time.time()
    results = {"paper": "van Dam, Mosca, Vazirani, quant-ph/0206003",
               "section": "5 Quantum Adiabatic Searching (constant-schedule)",
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # -------- C1: verify Eq. (1) at many s for several n --------
    c1 = []
    for n in [2, 3, 4]:
        c1.append(compare_gap_curve(n, ns=201))
    results["C1_gap_formula_check"] = c1

    # -------- C2: Δ_min scaling with N=2^n --------
    scans = []
    for n in [2, 3, 4]:
        d = find_min_gap(n, u=0, ns=4001)
        scans.append({k: v for k, v in d.items() if k not in ("s_grid", "gaps")})
    results["C2_min_gap_scan"] = scans
    logN = np.log(np.array([s["N"] for s in scans], dtype=float))
    logD = np.log(np.array([s["delta_min_numeric"] for s in scans], dtype=float))
    slope, intercept = np.polyfit(logN, logD, 1)
    results["C2_fit_log_delta_vs_log_N"] = {
        "slope": float(slope),
        "intercept": float(intercept),
        "expected_slope_paper": -0.5,
        "abs_slope_error": float(abs(slope - (-0.5))),
    }

    # -------- C3: adiabatic success probability vs T for n=3 (N=8) --------
    n_c3 = 3
    delta = find_min_gap(n_c3, u=0, ns=4001)["delta_min_numeric"]
    Ts = [1.0 / (delta ** 2) * c for c in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]]
    sim_rows = []
    for c, T in zip([0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0], Ts):
        p = simulate_adiabatic(n_c3, T, u=0, n_steps=800)
        sim_rows.append({"c": c, "T": T, "P_success": p})
        print(f"[C3] n={n_c3} c={c:6.2f} T={T:10.4f} P={p:.6f}")
    results["C3_adiabatic_convergence"] = {
        "n": n_c3, "N": 2 ** n_c3, "delta_min": delta,
        "rows": sim_rows,
    }

    # -------- C3b: T required to reach P>=0.9 scales with N --------
    scaling_rows = []
    for n in [2, 3, 4]:
        delta_n = find_min_gap(n, u=0, ns=4001)["delta_min_numeric"]
        # find smallest c such that P>=0.9
        c_grid = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        p_c = []
        c_hit = None
        for c in c_grid:
            T = c / delta_n ** 2
            p = simulate_adiabatic(n, T, u=0, n_steps=800)
            p_c.append({"c": c, "T": T, "P": p})
            if c_hit is None and p >= 0.9:
                c_hit = c
        scaling_rows.append({
            "n": n, "N": 2 ** n, "delta_min": delta_n,
            "P_by_c": p_c,
            "c_first_P_ge_0.9": c_hit,
            "T_at_c_hit": (c_hit / delta_n ** 2) if c_hit is not None else None,
        })
        print(f"[C3b] n={n} delta_min={delta_n:.6f} c_hit={c_hit}")
    results["C3b_T_scaling_with_N"] = scaling_rows

    # -------- write raw JSON + gap-curve arrays --------
    def _default(o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(str(type(o)))

    with open(f"{OUTDIR}/results.json", "w") as f:
        json.dump(results, f, indent=2, default=_default)

    # dump gap-curve for n=3 for the record
    d3 = find_min_gap(3, u=0, ns=4001)
    np.savez(f"{OUTDIR}/gap_curve_n3.npz",
             s=d3["s_grid"], gap_numeric=d3["gaps"],
             gap_paper=np.array([paper_gap_formula(s, 3) for s in d3["s_grid"]]))

    elapsed = time.time() - t0
    print(f"[DONE] elapsed={elapsed:.2f}s. Wrote {OUTDIR}/results.json")


if __name__ == "__main__":
    main()
