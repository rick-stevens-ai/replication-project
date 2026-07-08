#!/usr/bin/env python3
"""
Independent replication of Wan, Berta, Campbell (arXiv:2110.12071)
"A randomized quantum algorithm for statistical phase estimation".

We implement the CORE Lin-Tong-style statistical phase estimation
backbone the paper builds on (Algorithm 1, Eqs. (6)-(8) of the paper):

  1. Build a truncated Fourier approximation F(x) = sum_{j in S1} F_j e^{ijx}
     to the Heaviside function Theta(x), on the interval [-pi+delta, -delta]
     union [delta, pi-delta]. (Paper's Lemma 1 uses S1 = {0} U {+/-(2j+1)}_{j=0..d}.)
     We use the standard truncated Fourier series of Heaviside restricted to
     odd frequencies, which matches the paper's family and their Lin-Tong root.

  2. Approximate CDF (paper's Eq. (6)):
        C_tilde(x) = sum_{j in S1} F_j e^{i j x} <rho | e^{i H_hat t_j} | rho>
     with H_hat = H/lambda, t_j = -j * pi / (2 lambda + Delta) * lambda,
     i.e. tau = pi/(2 lambda + Delta), t_j = -j * tau * lambda, so
     the phases j*x live in a rescaled frequency domain.

  3. Sample (j, outcome_of_Hadamard_test) from the algorithm's distribution
     (Alg. 1 lines 4-7): sample j ~ |F_j|/F, run a simulated Hadamard test on
     rho and U_j = e^{i H_hat t_j} to get an unbiased +/- 1 estimator of
     Re<rho|U_j|rho> (or Im, using the S^\dagger phase gate). Average -> estimator
     of C_tilde(x). Sweep x over a grid, get an estimated CDF, and locate jump
     discontinuities -> eigenvalues of tau*H.

We do NOT re-implement the Lemma-2 LCU decomposition of e^{i H_hat t_j} into
random Pauli-rotation strings (that is the algorithm's *reduction of Cgate*).
For a laptop-scale reproducibility test of the statistical phase estimation
CLAIM ITSELF (accuracy + sample-complexity scaling), we simulate the Hadamard
test on the EXACT unitary e^{i H_hat t_j} via statevector. This is the
"quantum oracle" the paper's Lemma 2 approximates, so replication of the
statistical/CDF claim on this oracle is faithful to the paper's Theorem 1.

Runs on a 2-qubit TFIM: H = -J X0X1 - h (Z0 + Z1). Small enough for exact
diagonalization -> we can compare estimated ground-state phase to truth.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from numpy.random import default_rng


# ---------- 2-qubit TFIM Hamiltonian + Pauli-decomposition (paper Eq. (1)) ----------

I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1], [1, 0]], dtype=complex)
Y  = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z  = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def tfim_2qubit(J: float = 1.0, h: float = 0.5):
    """H = -J X0 X1 - h (Z0 + Z1). Return (H, [(alpha_l, P_l_matrix)])."""
    terms = [
        (-J, kron_list([X, X])),   # X0 X1
        (-h, kron_list([Z, I2])),  # Z0
        (-h, kron_list([I2, Z])),  # Z1
    ]
    H = sum(a * P for a, P in terms)
    return H, terms


def eigen_summary(H):
    w, V = np.linalg.eigh(H)
    return w, V


# ---------- Paper's Fourier series approximation of Heaviside (Lemma 1) ----------
#
# S1 = {0} U {+/-(2j+1)}_{j=0..d}, so only ODD nonzero frequencies.
# For a truncated Fourier series of a symmetric-around-zero shifted Heaviside
# theta(x) - 1/2 (which is an odd square wave on [-pi, pi] with period 2pi),
# the analytic Fourier coefficients are:
#     F_0 = 1/2
#     F_{+/-(2k+1)} = 1 / (i pi (2k+1))    for k=0,1,...,d
#     F_{even != 0} = 0
# so |F_{+/-(2k+1)}| = 1/(pi(2k+1)).
#
# On [delta, pi-delta] (and its mirror), this converges to Theta(x). This is
# the standard truncated Fourier series of a Heaviside used by Lin & Tong [6]
# and improved with better constants in the paper's Appendix A. Using it here
# gives us the SAME statistical estimator structure that the paper analyzes.

def heaviside_fourier(d: int):
    """Return (S1, F) where S1 is list of j-indices and F is complex coeffs.

    F(x) = 1/2 + sum_{k=0..d} (1/(i pi (2k+1))) * (e^{i(2k+1)x} - e^{-i(2k+1)x})
         = 1/2 + sum_{k=0..d} (2/(pi(2k+1))) * sin((2k+1)x)
    """
    S1 = [0]
    F = [0.5 + 0j]
    for k in range(d + 1):
        j = 2 * k + 1
        c = 1.0 / (1j * math.pi * j)  # coefficient of e^{ijx}
        S1.append(j);  F.append(c)
        S1.append(-j); F.append(-c)  # coefficient of e^{-ijx} = conj(c) = -c
    return np.array(S1, dtype=int), np.array(F, dtype=complex)


def heaviside_series_value(x, S1, F):
    """Direct sum sum_j F_j e^{i j x}. x may be array."""
    x = np.asarray(x)
    out = np.zeros(x.shape, dtype=complex)
    for j, Fj in zip(S1, F):
        out += Fj * np.exp(1j * j * x)
    return out


# ---------- Simulated Hadamard test on statevector ----------
#
# The Hadamard test on state rho (here pure |psi>) and unitary U produces
# +1/-1 outcomes with:
#   P(+1) = (1 + Re<psi|U|psi>) / 2
#   P(-1) = (1 - Re<psi|U|psi>) / 2   for G=I  (real part)
#   P(+1) = (1 + Im<psi|U|psi>) / 2                for G=S^dagger (imag part)
#
# We compute <psi|U|psi> exactly (statevector) and sample a Bernoulli outcome
# -> unbiased estimator of the real/imag part, matching what a quantum device
# would produce. That is the "shot-noise" the paper's Csample formula quantifies.


def simulate_hadamard_test(psi, U, want_imag: bool, rng) -> float:
    """Return a single +1/-1 sample of Re or Im of <psi|U|psi>."""
    amp = psi.conj() @ (U @ psi)
    val = amp.imag if want_imag else amp.real
    val = float(np.clip(val, -1.0, 1.0))
    p_plus = 0.5 * (1.0 + val)
    return 1.0 if rng.random() < p_plus else -1.0


def unitary_expm(H_hat: np.ndarray, t: float) -> np.ndarray:
    """U = e^{i H_hat t}. Use eigendecomposition of Hermitian H_hat for accuracy."""
    w, V = np.linalg.eigh(H_hat)
    return (V * np.exp(1j * w * t)) @ V.conj().T


# ---------- Approximate CDF estimator (paper's Alg. 1) ----------

@dataclass
class SPEConfig:
    J: float = 1.0
    h: float = 0.5
    d: int = 20          # Fourier series truncation, paper's d parameter
    Delta: float = 0.15  # precision parameter Delta (in units of the raw H)
    n_samples: int = 20000
    x_grid: np.ndarray = field(default_factory=lambda: np.linspace(-math.pi + 0.02, math.pi - 0.02, 2001))
    ansatz: str = "uniform"  # uniform superposition over 2 qubits
    seed: int = 20260703


def make_ansatz(kind: str, dim: int, ground_vec: np.ndarray | None = None) -> np.ndarray:
    if kind == "uniform":
        psi = np.ones(dim, dtype=complex) / math.sqrt(dim)
    elif kind == "random":
        rng = default_rng(0)
        v = rng.normal(size=dim) + 1j * rng.normal(size=dim)
        psi = v / np.linalg.norm(v)
    elif kind == "ground":
        psi = ground_vec.astype(complex).copy()
    else:
        raise ValueError(kind)
    return psi


def run_spe(cfg: SPEConfig, verbose: bool = True):
    """Run the paper's statistical phase estimation on 2-qubit TFIM.

    Returns dict with:
      - true_energies (raw H eigenvalues)
      - overlaps (|<eig_k|psi>|^2)
      - lam (paper's lambda = sum |alpha_l|)
      - tau
      - S1, F, A (total weight)
      - C_est(x) (estimated CDF from n_samples shots)
      - C_analytic(x) (exact approximate CDF from Eq. (6) using true <U_j> values)
      - eigenphase_est (estimated dominant jump location, in units of tau*H)
      - eigenphase_true (true tau * lowest eigenvalue with nontrivial overlap)
    """
    rng = default_rng(cfg.seed)

    # ---- 1. Hamiltonian, spectrum, ansatz ----
    H, terms = tfim_2qubit(cfg.J, cfg.h)
    eigvals, eigvecs = eigen_summary(H)
    lam = sum(abs(a) for a, _ in terms)  # paper's lambda = sum |alpha_l|
    tau = math.pi / (2 * lam + cfg.Delta)
    if verbose:
        print(f"[SPE] TFIM J={cfg.J} h={cfg.h} | H eigenvalues: {eigvals}")
        print(f"[SPE] lambda = {lam:.4f}, tau = {tau:.5f}, tau*eigvals = {tau*eigvals}")

    psi = make_ansatz(cfg.ansatz, H.shape[0], ground_vec=eigvecs[:, 0])
    overlaps = np.abs(eigvecs.conj().T @ psi) ** 2

    # ---- 2. Fourier coeffs (paper's F_j via Heaviside) ----
    S1, F = heaviside_fourier(cfg.d)
    A_weight = float(np.sum(np.abs(F)))  # paper's A(r) with r=oracle unitary

    # ---- 3. Precompute unitaries U_j = e^{i H_hat t_j} for each unique j ----
    H_hat = H / lam
    tj_map = {int(j): -int(j) * tau * lam for j in S1}
    Us = {int(j): unitary_expm(H_hat, tj_map[int(j)]) for j in S1}
    # exact expectation <psi|U_j|psi>
    exact_exp = {int(j): complex(psi.conj() @ (Us[int(j)] @ psi)) for j in S1}

    # ---- 4. Analytic approximate CDF at grid points (Eq. (6)) ----
    xs = cfg.x_grid
    C_analytic = np.zeros_like(xs, dtype=complex)
    for j, Fj in zip(S1, F):
        C_analytic += Fj * np.exp(1j * j * xs) * exact_exp[int(j)]

    # ---- 5. Sampled estimator: sample j ~ |F_j|/A, sample outcome via Hadamard test ----
    p_j = np.abs(F) / A_weight
    idx_of_j = {int(j): i for i, j in enumerate(S1)}

    # Draw n_samples indices into S1
    draws = rng.choice(len(S1), size=cfg.n_samples, p=p_j)

    # For each sample we need both Re and Im estimates because
    # z_i = A * F_j / |F_j| * (Re_estimate + i * Im_estimate) * e^{i j x} for arbitrary x
    # (paper: z_jk = A * e^{i arg(a_jk)} * m_jk; m_jk is one shot on the Hadamard test
    # -- their m estimates one of Re/Im. We take TWO shots per draw, one for Re one for Im,
    # which doubles the sample budget but gives us the complex estimator directly.)
    #
    # For a faithful shot count we'll report n_samples = 2 * cfg.n_samples "Hadamard tests"
    # in the results.

    z_bar = np.zeros_like(xs, dtype=complex)
    # accumulate sum then divide
    # For efficiency we group by j (many draws share j)
    unique, counts = np.unique(draws, return_counts=True)
    total_shots = 0
    for u_idx, n_u in zip(unique, counts):
        j = int(S1[u_idx])
        Fj = F[u_idx]
        Uj = Us[j]
        # phase e^{i arg(F_j)}
        phase = Fj / abs(Fj) if abs(Fj) > 0 else 1.0 + 0j
        # sample n_u Re-shots and n_u Im-shots
        amp = complex(psi.conj() @ (Uj @ psi))
        p_plus_re = 0.5 * (1.0 + max(-1.0, min(1.0, amp.real)))
        p_plus_im = 0.5 * (1.0 + max(-1.0, min(1.0, amp.imag)))
        re_shots = np.where(rng.random(n_u) < p_plus_re, 1.0, -1.0)
        im_shots = np.where(rng.random(n_u) < p_plus_im, 1.0, -1.0)
        total_shots += 2 * n_u
        # unbiased estimator of <U_j> per shot = re + i * im
        est_per_shot = re_shots + 1j * im_shots
        # z contribution per shot at each x: A * phase * est_per_shot * e^{i j x}
        # sum over shots gives: A * phase * (sum_est) * e^{i j x}
        z_bar += A_weight * phase * est_per_shot.sum() * np.exp(1j * j * xs)
    z_bar /= cfg.n_samples  # each "sample" in cfg is one Fj-draw = 2 Hadamard tests

    C_est = z_bar

    # ---- 6. Locate lowest jump (ground-state phase) in the estimated CDF ----
    # C_analytic(x) should look like sum_k overlap_k * F(x - tau * E_k),
    # i.e., a smoothed Heaviside stack jumping at tau * E_k values.
    #
    # Estimate the lowest jump location: derivative of Re[C_est] wrt x, find
    # first x above the noise floor where dC/dx has a large positive peak.
    C_re_smooth = np.real(C_est)
    # Simple binary-search-like: find smallest x where estimated C(x) crosses 0.5*eta.
    # Since our ansatz has some overlap eta with the ground state, C(x) rises past that overlap
    # at x >= tau * E_gs.
    eta = overlaps[0]  # overlap with ground state
    thresh = 0.5 * eta
    xs_sorted_idx = np.argsort(xs)
    xs_s = xs[xs_sorted_idx]; C_s = C_re_smooth[xs_sorted_idx]
    C_ana_s = np.real(C_analytic)[xs_sorted_idx]
    est_jump_x = None
    for i in range(len(xs_s)):
        if C_s[i] > thresh:
            est_jump_x = float(xs_s[i])
            break
    ana_jump_x = None
    for i in range(len(xs_s)):
        if C_ana_s[i] > thresh:
            ana_jump_x = float(xs_s[i])
            break
    true_gs_phase = float(tau * eigvals[0])

    result = dict(
        cfg=dict(J=cfg.J, h=cfg.h, d=cfg.d, Delta=cfg.Delta,
                 n_samples=cfg.n_samples, ansatz=cfg.ansatz, seed=cfg.seed,
                 n_hadamard_tests=total_shots),
        true_energies=eigvals.tolist(),
        overlaps=overlaps.tolist(),
        lam=lam, tau=tau,
        A_weight=A_weight,
        n_S1=len(S1),
        C_est_real=C_re_smooth.tolist(),
        C_est_imag=np.imag(C_est).tolist(),
        C_analytic_real=np.real(C_analytic).tolist(),
        C_analytic_imag=np.imag(C_analytic).tolist(),
        x_grid=xs.tolist(),
        est_jump_x=est_jump_x,
        analytic_jump_x=ana_jump_x,
        true_gs_phase=true_gs_phase,
        err_phase_est=None if est_jump_x is None else abs(est_jump_x - true_gs_phase),
        err_energy_est=None if est_jump_x is None else abs(est_jump_x/tau - eigvals[0]),
        analytic_err_energy=None if ana_jump_x is None else abs(ana_jump_x/tau - eigvals[0]),
    )
    return result


def scaling_study(base_cfg: SPEConfig, sample_counts, n_reps: int = 32):
    """Repeat SPE for varying n_samples and measure the SHOT-NOISE std of the
    CDF estimator C_est(x) at a fixed test point x0.

    Paper claim (Theorem 1 + Hoeffding argument, Alg. 1 line 3):
        Csample >= 4 A(r)^2 / (eta/2 - eps)^2 * ln(1/theta)
    which is equivalent to:  std[ C_est(x) ]  =  A(r) / sqrt(N_samples).
    So the estimator std should scale as N^{-1/2}.
    We measure this directly (not derived-quantity error) so we get a clean
    reproduction of the paper's shot-noise scaling.
    """
    # Pick one fixed x0 in the interesting region (near ground-state jump).
    x0 = None  # decided from analytic CDF of the base config
    from copy import deepcopy
    # first, exact analytic CDF at moderate n to find a good x0
    probe_cfg = SPEConfig(**{**base_cfg.__dict__, "n_samples": 200})
    probe = run_spe(probe_cfg, verbose=False)
    # x0: pick tau*E_gs midpoint, i.e. approximately the true jump location
    x0 = float(probe["true_gs_phase"] + 0.15)  # slightly right of the jump -> real CDF ~ eta

    out = []
    for n in sample_counts:
        vals_re = []; vals_im = []; energy_errs = []
        for rep in range(n_reps):
            c = SPEConfig(**{**base_cfg.__dict__, "n_samples": n, "seed": 20260703 + 1000*rep,
                             "x_grid": np.array([x0])})
            r = run_spe(c, verbose=False)
            vals_re.append(r["C_est_real"][0])
            vals_im.append(r["C_est_imag"][0])
            # also, full-grid energy error for a second config
            c2 = SPEConfig(**{**base_cfg.__dict__, "n_samples": n, "seed": 20260703 + 1000*rep})
            r2 = run_spe(c2, verbose=False)
            if r2["err_energy_est"] is not None:
                energy_errs.append(r2["err_energy_est"])
        vals_re = np.array(vals_re); vals_im = np.array(vals_im)
        std_re = float(np.std(vals_re, ddof=1))
        std_im = float(np.std(vals_im, ddof=1))
        mean_re = float(np.mean(vals_re))
        # analytic value at x0 (from probe)
        # recompute analytic value at x0 exactly
        c_ana_cfg = SPEConfig(**{**base_cfg.__dict__, "n_samples": 10, "x_grid": np.array([x0])})
        c_ana = run_spe(c_ana_cfg, verbose=False)
        ana_re = c_ana["C_analytic_real"][0]
        energy_errs = np.array(energy_errs)
        rms_e = float(np.sqrt(np.mean(energy_errs**2))) if len(energy_errs) else float("nan")
        med_e = float(np.median(energy_errs)) if len(energy_errs) else float("nan")
        out.append(dict(n_samples=int(n), n_reps=int(n_reps), x0=x0,
                        std_C_re=std_re, std_C_im=std_im,
                        mean_C_re=mean_re, analytic_C_re=ana_re,
                        bias=abs(mean_re - ana_re),
                        rms_energy_err=rms_e, median_energy_err=med_e))
        print(f"[scaling] n={n:>7d}  std(C_re)={std_re:.4e}  bias={abs(mean_re - ana_re):.4e}"
              f"  RMS_E={rms_e:.4e}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=".", help="write outputs here")
    ap.add_argument("--n-samples", type=int, default=40000)
    ap.add_argument("--d", type=int, default=20)
    ap.add_argument("--scaling", action="store_true", help="run sample-complexity scan too")
    ap.add_argument("--scan-reps", type=int, default=8)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Wan/Berta/Campbell 2110.12071 — Statistical Phase Estimation replication ===")
    cfg = SPEConfig(n_samples=args.n_samples, d=args.d)
    t0 = time.time()
    result = run_spe(cfg, verbose=True)
    elapsed = time.time() - t0
    result["elapsed_s"] = elapsed

    print()
    print("--- Result summary ---")
    print(f"True eigenvalues:       {result['true_energies']}")
    print(f"Ansatz overlaps:        {result['overlaps']}")
    print(f"tau*E_gs (true):        {result['true_gs_phase']:.5f}")
    print(f"Analytic CDF jump x*:   {result['analytic_jump_x']}")
    print(f"Estimated CDF jump x*:  {result['est_jump_x']}")
    print(f"Analytic energy error:  {result['analytic_err_energy']}")
    print(f"Estimated energy error: {result['err_energy_est']}")
    print(f"A(r) total weight:      {result['A_weight']:.4f}  (|S1|={result['n_S1']})")
    print(f"n Hadamard tests:       {result['cfg']['n_hadamard_tests']}")
    print(f"elapsed:                {elapsed:.2f} s")

    def _to_native(o):
        import numpy as _np
        if isinstance(o, (_np.integer,)):
            return int(o)
        if isinstance(o, (_np.floating,)):
            return float(o)
        if isinstance(o, _np.ndarray):
            return o.tolist()
        raise TypeError(f"not serializable: {type(o).__name__}")

    with open(out_dir / "spe_run.json", "w") as f:
        json.dump(result, f, indent=2, default=_to_native)
    print(f"[wrote] {out_dir / 'spe_run.json'}")

    if args.scaling:
        print()
        print("--- Sample-complexity scaling study ---")
        # sweep in decades: this tests error ~ 1/sqrt(N_samples)
        ns = [500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
        scan_cfg = SPEConfig(d=args.d)
        study = scaling_study(scan_cfg, ns, n_reps=args.scan_reps)
        with open(out_dir / "spe_scaling.json", "w") as f:
            json.dump(dict(base_cfg=dict(J=scan_cfg.J, h=scan_cfg.h, d=scan_cfg.d,
                                          Delta=scan_cfg.Delta, ansatz=scan_cfg.ansatz),
                            study=study), f, indent=2, default=_to_native)
        print(f"[wrote] {out_dir / 'spe_scaling.json'}")

        # Fit log(std_C_re) vs log(n) to extract exponent (Csample ~ 1/eps^2 => eps ~ N^{-1/2})
        arr = np.array([(s["n_samples"], s["std_C_re"]) for s in study if not math.isnan(s["std_C_re"])])
        if len(arr) >= 3:
            logn = np.log10(arr[:, 0]); loge = np.log10(arr[:, 1])
            slope_std, intercept_std = np.polyfit(logn, loge, 1)
            print()
            print(f"[scaling fit CDF std]   log10(std_C_re)     = {slope_std:+.3f} * log10(N) + {intercept_std:+.3f}")
            print(f"                        Paper prediction: slope = -0.500 (shot noise 1/sqrt(N))")
            print(f"                        Observed:         slope = {slope_std:+.3f}")

        arr2 = np.array([(s["n_samples"], s["rms_energy_err"]) for s in study
                         if not math.isnan(s["rms_energy_err"]) and s["rms_energy_err"] > 0])
        if len(arr2) >= 3:
            logn = np.log10(arr2[:, 0]); loge = np.log10(arr2[:, 1])
            slope_e, intercept_e = np.polyfit(logn, loge, 1)
            print(f"[scaling fit energy err] log10(rms_E_err)   = {slope_e:+.3f} * log10(N) + {intercept_e:+.3f}")
            print(f"                        (grid-limited floor may bend this at high N)")


if __name__ == "__main__":
    main()
