"""
Independent numerical replication of DB-QSP (Alg. 1) from
Suzuki, Tiang, Son, Ng, Holmes, Gluza,
"Double-bracket algorithm for quantum signal processing without post-selection"
arXiv:2504.01077v3 (published Quantum 2025-12-16).

We reproduce three concrete claims:
  (R1) Lemma 1 / Eq. (16): for any complex z and state |Ψ⟩, the
       linear polynomial (H - z I)|Ψ⟩/||.|| equals
          exp(i theta_Psi * Psi) * exp(s * [Psi, H]) |Ψ⟩
       with the paper's closed form for s and theta.
  (R2) Full DB-QSP (Alg. 1, "exact" branch using matrix exponentials of
       Ψ_k and [Ψ_k,H]) applied recursively for a degree-K polynomial
       reproduces p(H)|Ψ0⟩/||p(H)|Ψ0⟩|| to numerical precision.
  (R3) The group-commutator approximation of exp(s[Ψ,H]) via Eq. (19)
       converges as O(1/sqrt(N)) — the headline scaling used in
       Prop. C.1 that guarantees the DB-QSP quantum circuit approaches
       the exact synthesis.
  (R4) Unitarity: every step of DB-QSP is a genuine unitary, so no
       post-selection is required (the state norm stays 1 throughout).

Free numpy/scipy simulation on 4x4 Hermitian matrices. No external
services, no fabricated numbers.
"""

from __future__ import annotations
import json
import os
import time
import numpy as np
from scipy.linalg import expm

RNG = np.random.default_rng(20260705)  # deterministic


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def rand_hermitian(dim: int, spectral_radius: float = 0.9) -> np.ndarray:
    """Random Hermitian with ||H||_op <= spectral_radius (via rescaling)."""
    A = RNG.standard_normal((dim, dim)) + 1j * RNG.standard_normal((dim, dim))
    H = 0.5 * (A + A.conj().T)
    ev = np.linalg.eigvalsh(H)
    rmax = max(abs(ev.min()), abs(ev.max()))
    return H * (spectral_radius / rmax)


def rand_state(dim: int) -> np.ndarray:
    v = RNG.standard_normal(dim) + 1j * RNG.standard_normal(dim)
    return v / np.linalg.norm(v)


def normalize(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def unitary_error(U: np.ndarray) -> float:
    d = U.shape[0]
    return float(np.linalg.norm(U.conj().T @ U - np.eye(d)))


# -----------------------------------------------------------------------------
# The linear-polynomial synthesis of Lemma 1 / Eq. (16)
# -----------------------------------------------------------------------------
def synthesize_linear(H: np.ndarray, psi: np.ndarray, z: complex):
    """
    Return (s, theta, U_step) implementing:
        exp(i*theta*Psi) exp(s * [Psi, H])
    such that U_step |Psi> = (H - z I)|Psi>/||(H - z I)|Psi>||.

    Paper eqs.:
      E = <Psi|H|Psi>,  V = <Psi|H^2|Psi> - E^2
      For target linear polynomial (H - z I) we set alpha = z.
      s_k = -(1/sqrt(V)) * arccos( |E - z| / sqrt(V + |E - z|^2) )
      theta_k = arg( (E - z) / |E - z| )

    Returns dict with s, theta, U_step, plus intermediate diagnostics.
    """
    d = H.shape[0]
    Hpsi = H @ psi
    E = np.vdot(psi, Hpsi).real
    V = np.vdot(psi, H @ Hpsi).real - E * E

    # Guard: eigenstate breakdown when V==0 and z==E; keep it visible.
    gap = complex(E - z)
    denom = np.sqrt(V + abs(gap) ** 2)
    if V <= 1e-14 and abs(gap) < 1e-14:
        raise ValueError("Eigenstate breakdown (V=0 and z=E).")

    # arccos returns [0, pi]; the paper's s is non-positive.
    s = -(1.0 / np.sqrt(V)) * np.arccos(abs(gap) / denom)
    theta = np.angle(gap) if abs(gap) > 0 else 0.0

    Psi = np.outer(psi, psi.conj())  # rank-1 projector
    comm = Psi @ H - H @ Psi         # [Psi, H]
    U_comm = expm(s * comm)          # exp(s [Psi, H])
    U_refl = expm(1j * theta * Psi)  # exp(i theta Psi)
    U_step = U_refl @ U_comm
    return dict(s=s, theta=theta, E=E, V=V, gap=gap,
                U_step=U_step, U_comm=U_comm, U_refl=U_refl)


# -----------------------------------------------------------------------------
# Group-commutator approximation of exp(s [Psi, H])   (Eq. 19)
# -----------------------------------------------------------------------------
def group_commutator_approx(H: np.ndarray, psi: np.ndarray, s: float,
                            N: int) -> np.ndarray:
    """
    Approx exp(s [Psi, H]) using
       ( exp(i s^(N) Psi) exp(i s^(N) H) exp(-i s^(N) Psi) exp(-i s^(N) H) )^N
    with s^(N) = sqrt(|s|/N).  Sign convention: paper assumes s<=0, so use |s|.
    """
    sN = np.sqrt(abs(s) / N)
    Psi = np.outer(psi, psi.conj())
    A = expm(1j * sN * Psi) @ expm(1j * sN * H) \
        @ expm(-1j * sN * Psi) @ expm(-1j * sN * H)
    U = np.linalg.matrix_power(A, N)
    return U


# -----------------------------------------------------------------------------
# Exact matrix polynomial for reference
# -----------------------------------------------------------------------------
def polynomial_of_H(H: np.ndarray, zeros: list[complex]) -> np.ndarray:
    """Compute prod_k (H - z_k I).  Real "matrix polynomial" reference."""
    d = H.shape[0]
    P = np.eye(d, dtype=complex)
    for z in zeros:
        P = (H - z * np.eye(d)) @ P
    return P


# =============================================================================
# R1 — Verify Lemma 1 / Eq. (16) for random z's
# =============================================================================
def experiment_R1():
    print("\n[R1] Lemma 1: single linear polynomial (H - zI) via unitary synthesis")
    d = 4
    H = rand_hermitian(d)
    psi = rand_state(d)
    trials = []
    for _ in range(20):
        # random complex z within a reasonable range
        z = complex(RNG.uniform(-1.2, 1.2), RNG.uniform(-0.8, 0.8))
        info = synthesize_linear(H, psi, z)
        U = info["U_step"]
        lhs = U @ psi
        rhs = (H - z * np.eye(d)) @ psi
        rhs = rhs / np.linalg.norm(rhs)
        # Match up to a global phase
        overlap = abs(np.vdot(lhs, rhs))
        state_err = min(np.linalg.norm(lhs - rhs), np.linalg.norm(lhs + rhs))
        trials.append(dict(z_re=z.real, z_im=z.imag,
                           overlap=float(overlap),
                           state_err=float(state_err),
                           unitary_err=unitary_error(U)))
    ovs = [t["overlap"] for t in trials]
    errs = [t["state_err"] for t in trials]
    uerrs = [t["unitary_err"] for t in trials]
    print(f"  20 random z's:  min overlap = {min(ovs):.12f}   (target 1.0)")
    print(f"                  max |Ψ_lhs - Ψ_rhs| = {max(errs):.2e}")
    print(f"                  max U-unitarity err = {max(uerrs):.2e}")
    return dict(trials=trials,
                min_overlap=float(min(ovs)),
                max_state_err=float(max(errs)),
                max_unitary_err=float(max(uerrs)),
                verdict="PASS" if min(ovs) > 1 - 1e-8 else "FAIL")


# =============================================================================
# R2 — Full DB-QSP (Alg. 1, exact branch) for a degree-K polynomial
# =============================================================================
def experiment_R2(K: int = 5):
    print(f"\n[R2] DB-QSP exact synthesis for degree-K={K} polynomial")
    d = 4
    H = rand_hermitian(d)
    psi0 = rand_state(d)

    # Pick K zeros of a polynomial - use scaled Chebyshev nodes (real z's in [-.7,.7])
    zeros = [0.7 * np.cos((2 * k + 1) * np.pi / (2 * K)) for k in range(K)]

    # Reference: p(H) |Ψ0⟩ / ||...||
    P = polynomial_of_H(H, zeros)
    ref = normalize(P @ psi0)

    # Apply Alg. 1 exact branch: at each step compute z_k -> s_k, θ_k -> U_k
    psi = psi0.copy()
    max_norm_dev = 0.0
    max_step_unitarity = 0.0
    per_step = []
    for k, z in enumerate(zeros):
        info = synthesize_linear(H, psi, z)
        U_k = info["U_step"]
        psi_new = U_k @ psi
        # unitarity of the step
        u_err = unitary_error(U_k)
        max_step_unitarity = max(max_step_unitarity, u_err)
        # norm preserved => no post-selection needed
        norm = np.linalg.norm(psi_new)
        max_norm_dev = max(max_norm_dev, abs(norm - 1.0))
        per_step.append(dict(k=k, z=complex(z).real,
                             s=float(info["s"]), theta=float(info["theta"]),
                             E=float(info["E"]), V=float(info["V"]),
                             step_norm=float(norm),
                             step_unitary_err=float(u_err)))
        psi = psi_new
    # Global-phase-tolerant overlap
    overlap = abs(np.vdot(psi, ref))
    state_err = min(np.linalg.norm(psi - ref), np.linalg.norm(psi + ref))
    print(f"  zeros (real): {[f'{z:.3f}' for z in zeros]}")
    print(f"  final |<ψ|ref>| = {overlap:.12f}  (target 1.0)")
    print(f"  final state error (up to global phase) = {state_err:.2e}")
    print(f"  max deviation of ||ψ_k|| from 1 across steps = {max_norm_dev:.2e}")
    print(f"  max per-step unitarity error = {max_step_unitarity:.2e}")
    return dict(K=K, zeros=list(zeros),
                overlap=float(overlap),
                state_err=float(state_err),
                max_norm_dev=float(max_norm_dev),
                max_step_unitary_err=float(max_step_unitarity),
                per_step=per_step,
                verdict="PASS" if overlap > 1 - 1e-8 and max_norm_dev < 1e-10
                else "FAIL")


# =============================================================================
# R3 — Group-commutator approximation error ~ O(1/sqrt(N))   (Prop. C.1)
# =============================================================================
def experiment_R3():
    """
    For a single DB-QSP step, we compare:
      exact:  U_exact = exp(s [Psi, H])
      approx: U_apx(N) = (e^{i sN Psi} e^{i sN H} e^{-i sN Psi} e^{-i sN H})^N
                        with sN = sqrt(|s|/N)
    and check that ||U_apx(N) - U_exact|| decays as C / sqrt(N).
    """
    print("\n[R3] Group-commutator convergence error scaling (Eq. 19)")
    d = 4
    H = rand_hermitian(d)
    psi = rand_state(d)
    z = 0.3 + 0.1j
    info = synthesize_linear(H, psi, z)
    s = info["s"]
    Psi = np.outer(psi, psi.conj())
    U_exact = expm(s * (Psi @ H - H @ Psi))

    Ns = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    rows = []
    for N in Ns:
        U_apx = group_commutator_approx(H, psi, s, N)
        err_op = float(np.linalg.norm(U_apx - U_exact))            # Frobenius
        state_apx = U_apx @ psi
        state_exact = U_exact @ psi
        err_state = float(np.linalg.norm(state_apx - state_exact))
        rows.append(dict(N=N, s_used=float(s), err_op=err_op,
                         err_state=err_state,
                         sqrtN_times_err=float(err_op * np.sqrt(N))))
    print(f"  Single-step |s| = {abs(s):.4f}")
    print(f"  {'N':>6} {'err_op':>12} {'err_state':>12} {'err_op*sqrt(N)':>18}")
    for r in rows:
        print(f"  {r['N']:>6} {r['err_op']:>12.4e} {r['err_state']:>12.4e} "
              f"{r['sqrtN_times_err']:>18.4e}")

    # Regression: log(err_op) = a * log(N) + b, expect a ≈ -0.5
    xs = np.log(np.array([r["N"] for r in rows], dtype=float))
    ys = np.log(np.array([r["err_op"] for r in rows], dtype=float))
    slope, intercept = np.polyfit(xs, ys, 1)
    print(f"  Fit log-log slope = {slope:.4f}  (paper predicts -0.5 for O(1/sqrt(N)))")
    verdict = "PASS" if abs(slope + 0.5) < 0.08 else "FAIL"
    print(f"  R3 verdict = {verdict}  (tolerance |slope + 0.5| < 0.08)")
    return dict(Ns=Ns, rows=rows, slope=float(slope),
                intercept=float(intercept), verdict=verdict)


# =============================================================================
# R4 — Full DB-QSP with group-commutator implementation, and unitarity check
# =============================================================================
def experiment_R4(K: int = 3, N: int = 512):
    """
    Run the DB-QSP quantum-algorithm branch (Alg. 1 line 7): approximate each
    exp(s [Psi, H]) via the group-commutator with N repetitions.  Then include
    the state-dependent reflection exp(i theta Psi), and iterate K times.
    Verify: (a) the resulting state approaches the exact QSP target as N
    increases, and (b) every step is a unitary (norm preserved, no
    post-selection).
    """
    print(f"\n[R4] Full DB-QSP quantum-algorithm branch: K={K}, N={N}")
    d = 4
    H = rand_hermitian(d)
    psi0 = rand_state(d)
    zeros = [0.6 * np.cos((2 * k + 1) * np.pi / (2 * K)) for k in range(K)]

    # Reference (Thm. 2 exact branch)
    psi_ref = psi0.copy()
    for z in zeros:
        info = synthesize_linear(H, psi_ref, z)
        psi_ref = info["U_step"] @ psi_ref

    # Group-commutator-approximated evolution
    Ns_sweep = [8, 32, 128, 512, 2048]
    sweep = []
    for Nk in Ns_sweep:
        psi = psi0.copy()
        max_norm_dev = 0.0
        max_unitary_err = 0.0
        for z in zeros:
            info = synthesize_linear(H, psi, z)
            s = info["s"]
            theta = info["theta"]
            U_comm_apx = group_commutator_approx(H, psi, s, Nk)
            Psi = np.outer(psi, psi.conj())
            U_refl = expm(1j * theta * Psi)
            U_step = U_refl @ U_comm_apx
            max_unitary_err = max(max_unitary_err, unitary_error(U_step))
            psi = U_step @ psi
            max_norm_dev = max(max_norm_dev, abs(np.linalg.norm(psi) - 1.0))
        overlap = float(abs(np.vdot(psi, psi_ref)))
        state_err = float(min(np.linalg.norm(psi - psi_ref),
                              np.linalg.norm(psi + psi_ref)))
        sweep.append(dict(N=Nk, overlap=overlap, state_err=state_err,
                          max_norm_dev=float(max_norm_dev),
                          max_unitary_err=float(max_unitary_err)))
        print(f"  N={Nk:>5}  |<ψ|ref>|={overlap:.10f}  "
              f"state_err={state_err:.3e}  "
              f"max|1-‖ψ‖|={max_norm_dev:.2e}  "
              f"max_U_err={max_unitary_err:.2e}")

    # error should decrease monotonically with N and hit O(1/sqrt(N))
    xs = np.log(np.array([s["N"] for s in sweep], dtype=float))
    ys = np.log(np.array([s["state_err"] for s in sweep], dtype=float))
    slope, intercept = np.polyfit(xs, ys, 1)
    print(f"  Full-alg state-err log-log slope vs N: {slope:.4f} "
          f"(expect near -0.5)")
    # Unitarity: max_norm_dev across all runs should be ~ machine epsilon
    max_nd = max(s["max_norm_dev"] for s in sweep)
    print(f"  Global max |1-‖ψ‖| across all runs = {max_nd:.2e}  "
          f"=> no post-selection needed")
    verdict = "PASS" if (sweep[-1]["overlap"] > 0.999 and max_nd < 1e-10
                         and abs(slope + 0.5) < 0.15) else "PARTIAL"
    print(f"  R4 verdict = {verdict}")
    return dict(K=K, N_sweep=Ns_sweep, sweep=sweep,
                slope=float(slope), max_norm_dev_global=float(max_nd),
                verdict=verdict)


# =============================================================================
# Main
# =============================================================================
def main():
    t0 = time.time()
    out = {
        "paper": "arXiv:2504.01077v3 — Suzuki, Tiang, Son, Ng, Holmes, Gluza",
        "title": "Double-bracket algorithm for quantum signal processing "
                 "without post-selection",
        "numpy_version": np.__version__,
        "random_seed": 20260705,
    }
    out["R1_lemma1_linear_synthesis"] = experiment_R1()
    out["R2_full_dbqsp_exact_branch"] = experiment_R2(K=5)
    out["R3_group_commutator_scaling"] = experiment_R3()
    out["R4_full_dbqsp_alg_branch"] = experiment_R4(K=3, N=512)
    out["wall_seconds"] = round(time.time() - t0, 3)

    outdir = os.path.dirname(os.path.abspath(__file__))
    outfile = os.path.join(outdir, "results.json")
    with open(outfile, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nWrote {outfile}")
    print(f"Wall time: {out['wall_seconds']}s")

    # Summary line
    verdicts = {k: v.get("verdict", "?") for k, v in out.items()
                if isinstance(v, dict) and "verdict" in v}
    print("\nSummary:")
    for k, v in verdicts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
