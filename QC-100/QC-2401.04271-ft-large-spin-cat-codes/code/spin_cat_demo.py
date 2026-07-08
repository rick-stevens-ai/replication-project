#!/usr/bin/env python3
"""
Spin-cat code demonstration (Omanakuttan et al., arXiv:2401.04271).

Physical setup
--------------
Encode a logical qubit in a spin-J system (dimension d = 2J+1):
    |0_L> = |J, -J>          (spin coherent state, "south pole")
    |1_L> = |J, +J>          (spin coherent state, "north pole")
    |+_L> = (|0_L> + |1_L>)/sqrt(2)   (a "spin cat")
    |-_L> = (|0_L> - |1_L>)/sqrt(2)

Baseline comparison: an unencoded qubit (J = 1/2, d = 2), i.e. |0>=|-1/2>, |1>=|+1/2>.

Noise model (rank-1 amplitude / "X-like" error, per paper Eq. 9)
----------------------------------------------------------------
    U_X(theta) = exp(-i theta J_x)

For a bare qubit (J = 1/2) this rotates |0> and |1> into a superposition at rate theta.
For the spin-cat code (J = 9/2), the same J_x pulse takes many "steps" to move population
between the north and south poles of the spin, so the bit-flip probability between the
logical basis states is EXPONENTIALLY SUPPRESSED in J.

This is the paper's central bias-preservation claim (Sec. II, "spin-cat encoding").
The full FTQC threshold requires stabilizer concatenation, ancillas, syndrome extraction,
and a rank-preserving CNOT — all beyond a small-instance demo. Here we verify only the
underlying noise-bias inequality that makes the paper's threshold possible.

Metrics
-------
For a given noise angle theta, we compute:
  * P(bit flip)  = probability |0_L> transitions to |1_L> after U_X(theta)
  * P(retain)    = |<0_L | U_X(theta) | 0_L>|^2         (logical fidelity)
  * Also for the |+_L> spin-cat state:
        P(cat flip) = probability |+_L> -> |-_L>  under U_Z(theta) = exp(-i theta J_z)
    which for a spin cat is a PHASE flip; this is the DOMINANT / unbiased error
    (grows with J, since J_z |+/-J> = +/-J |+/-J>) — the paper corrects it with a
    repetition-like phase code (outer layer).

Expected qualitative outcome
----------------------------
  * Bit-flip suppression for spin-cat vs. bare qubit: exponential in J.
  * Phase-flip AMPLIFICATION for spin-cat: grows ~ J^2 * theta^2 for small theta
    (this is why the paper needs an outer phase-flip code).

If both effects show up clearly, the encoding's biased-noise structure is confirmed;
the paper's threshold improvement follows from applying a repetition code to the
(now dominant) phase errors, which we do NOT simulate here.
"""

import json
import time
from pathlib import Path

import numpy as np
import qutip as qt

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def spin_ops(J):
    """Return (Jx, Jy, Jz) as qutip Qobj for a spin-J system, d = 2J+1."""
    d = int(2 * J + 1)
    jx = qt.jmat(J, "x")
    jy = qt.jmat(J, "y")
    jz = qt.jmat(J, "z")
    assert jx.shape == (d, d)
    return jx, jy, jz


def logical_basis(J):
    """|0_L> = |J,-J>, |1_L> = |J,+J>, |+_L>, |-_L>."""
    d = int(2 * J + 1)
    # qutip convention: qt.spin_state(J, m) with m ranging J, J-1, ..., -J
    ket_minus = qt.spin_state(J, -J)   # |0_L>
    ket_plus = qt.spin_state(J, +J)    # |1_L>
    cat_plus = (ket_plus + ket_minus).unit()
    cat_minus = (ket_plus - ket_minus).unit()
    return ket_minus, ket_plus, cat_plus, cat_minus


def apply_unitary(U, psi):
    return U * psi


def prob_amp(bra, ket):
    amp = bra.dag() * ket
    # qutip 5 returns a scalar for <bra|ket>; earlier versions returned a 1x1 Qobj
    if hasattr(amp, "full"):
        amp = amp.full()[0, 0]
    return abs(complex(amp)) ** 2


def sweep_bitflip(J, thetas):
    """
    Apply U_X(theta) = exp(-i theta J_x) to |0_L>; compute P(|1_L>|...|0_L>) as a
    function of theta. Small theta ~ single 'kick'; large theta -> full Bloch rotation.
    """
    jx, _, _ = spin_ops(J)
    ket0, ket1, catP, catM = logical_basis(J)
    results = []
    for th in thetas:
        U = (-1j * th * jx).expm()
        psi = U * ket0
        p_stay = prob_amp(ket0, psi)
        p_flip = prob_amp(ket1, psi)
        # leakage = anything outside {|0_L>, |1_L>}
        p_leak = 1.0 - p_stay - p_flip
        results.append(dict(theta=float(th), p_stay=float(p_stay),
                            p_flip=float(p_flip), p_leak=float(p_leak)))
    return results


def sweep_phaseflip(J, thetas):
    """
    Apply U_Z(theta) = exp(-i theta J_z) to |+_L>; compute P(|-_L>|...|+_L>).
    """
    _, _, jz = spin_ops(J)
    ket0, ket1, catP, catM = logical_basis(J)
    results = []
    for th in thetas:
        U = (-1j * th * jz).expm()
        psi = U * catP
        p_stay = prob_amp(catP, psi)
        p_flip = prob_amp(catM, psi)
        p_leak = 1.0 - p_stay - p_flip
        results.append(dict(theta=float(th), p_stay=float(p_stay),
                            p_flip=float(p_flip), p_leak=float(p_leak)))
    return results


def sweep_bitflip_dephasing_channel(J, gammas):
    """
    Model J_x dephasing as a Lindblad channel: dr/dt = gamma * (Jx r Jx - {Jx^2, r}/2 )
    Solve for time t=1 (so effective 'dose' = gamma) and read out logical bit-flip prob.
    This is a STOCHASTIC noise model (not a coherent rotation) closer to physical Larmor
    fluctuations along x.
    """
    jx, _, _ = spin_ops(J)
    ket0, _, _, _ = logical_basis(J)
    rho0 = ket0 * ket0.dag()
    results = []
    ket_minus_J = ket0
    ket_plus_J = qt.spin_state(J, +J)
    Pi0 = ket_minus_J * ket_minus_J.dag()
    Pi1 = ket_plus_J * ket_plus_J.dag()
    for g in gammas:
        # single-step Lindblad evolution: rho(t=1) = mesolve
        H = 0 * jx
        c_ops = [np.sqrt(g) * jx]
        tlist = np.linspace(0, 1, 5)
        out = qt.mesolve(H, rho0, tlist, c_ops=c_ops, e_ops=[Pi0, Pi1])
        p_stay = float(out.expect[0][-1])
        p_flip = float(out.expect[1][-1])
        p_leak = 1.0 - p_stay - p_flip
        results.append(dict(gamma=float(g), p_stay=p_stay,
                            p_flip=p_flip, p_leak=p_leak))
    return results


def main():
    t0 = time.time()
    thetas = np.linspace(0.0, 0.6, 25)  # small-to-moderate rotation
    gammas = np.logspace(-4, -0.5, 15)

    Js = [0.5, 3 / 2, 5 / 2, 7 / 2, 9 / 2]

    all_results = dict(
        paper="arXiv:2401.04271",
        title="Fault-tolerant quantum computation using large spin cat-codes",
        code_note=("Small-instance demonstration of the biased-noise property "
                   "underlying the spin-cat code: bit-flip suppression under J_x, "
                   "phase-flip amplification under J_z, comparing several spin-J "
                   "encodings against the bare qubit J=1/2."),
        thetas=[float(x) for x in thetas],
        gammas=[float(x) for x in gammas],
        bitflip_coherent={},
        phaseflip_coherent={},
        bitflip_dephasing={},
    )

    print("=" * 70)
    print("SPIN-CAT CODE REPLICATION — arXiv:2401.04271")
    print("=" * 70)

    for J in Js:
        d = int(2 * J + 1)
        label = f"J={J}(d={d})"
        print(f"\n--- {label} ---")
        bf = sweep_bitflip(J, thetas)
        pf = sweep_phaseflip(J, thetas)
        deph = sweep_bitflip_dephasing_channel(J, gammas)
        all_results["bitflip_coherent"][label] = bf
        all_results["phaseflip_coherent"][label] = pf
        all_results["bitflip_dephasing"][label] = deph
        # small print
        # small theta point (idx 2 corresponds to ~ 0.05)
        idx = 2
        th = thetas[idx]
        print(f"  theta={th:.4f}: "
              f"bit-flip P={bf[idx]['p_flip']:.3e}  "
              f"cat phase-flip P={pf[idx]['p_flip']:.3e}  "
              f"bit-flip leakage={bf[idx]['p_leak']:.3e}")

    # Headline numbers: at a fixed small theta, ratio of bit-flip suppression
    # for spin-cat vs. bare qubit.
    print("\n" + "=" * 70)
    print("HEADLINE: bit-flip suppression at theta = 0.05")
    print("=" * 70)
    ref_theta_idx = int(np.argmin(np.abs(thetas - 0.05)))
    baseline_flip = all_results["bitflip_coherent"]["J=0.5(d=2)"][ref_theta_idx]["p_flip"]
    print(f"Bare qubit (J=1/2): P(bit flip) = {baseline_flip:.4e}")
    ratios = {}
    for J in Js:
        d = int(2 * J + 1)
        label = f"J={J}(d={d})"
        pflip = all_results["bitflip_coherent"][label][ref_theta_idx]["p_flip"]
        r = pflip / baseline_flip if baseline_flip > 0 else float("inf")
        print(f"  {label}: P(flip)={pflip:.4e}  ratio vs bare = {r:.4e}")
        ratios[label] = dict(p_flip=pflip, ratio=r)
    all_results["headline_ratios_theta_0p05"] = dict(theta=float(thetas[ref_theta_idx]),
                                                     bare=baseline_flip, ratios=ratios)

    # Phase-flip amplification headline
    print("\nHEADLINE: cat phase-flip amplification at theta = 0.05")
    baseline_pflip = all_results["phaseflip_coherent"]["J=0.5(d=2)"][ref_theta_idx]["p_flip"]
    for J in Js:
        d = int(2 * J + 1)
        label = f"J={J}(d={d})"
        pflip = all_results["phaseflip_coherent"][label][ref_theta_idx]["p_flip"]
        print(f"  {label}: P(phase flip)={pflip:.4e}  ratio vs bare = "
              f"{pflip / baseline_pflip if baseline_pflip > 0 else float('inf'):.4e}")

    dt = time.time() - t0
    all_results["wall_seconds"] = dt
    out_json = OUT / "spin_cat_results.json"
    with out_json.open("w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nWrote {out_json}  ({dt:.1f}s)")


if __name__ == "__main__":
    main()
