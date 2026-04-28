"""
ref8_scattering_comparator.py
==============================

First-principles "reference" scattering-theory calculation for the 40Ca+
metastable-qubit Raman/Rayleigh/leakage rates used in:

  Lotshaw, Sawyer, Herold, Buchs, "Exactly-solved model of light scattering
  errors in quantum simulations with metastable trapped-ion qubits"
  (OSTI 2441075).

CONTEXT
-------
The original replication report flagged: "the paper compares against
numerically-exact scattering theory (Ref [8])".  On re-reading the paper:

  Ref [8] = Kang, Campbell, Brown, PRX Quantum 4:020358 (2023) — that paper
  is about *erasure conversion* and is cited in the introduction (line "error
  correction schemes utilizing 'erasure conversion' [7,8]").  It is NOT a
  scattering-theory reference.

The actual "exact scattering theory" inputs to the paper are:

  - Eqs. (11)–(12)  : second-order perturbative scattering rates,
                      Gamma^{(0->b)} = A_{P3/2 -> b} * |Omega^{(0)}/Delta|^2,
                      following Wineland et al. 2003 [Ref 19].
  - Branching ratios: 94.5% leakage / 3.9% Raman / 1.6% elastic, taken from
                      the precision measurement of Gerritsma et al. 2008
                      [Ref 18].
  - Elastic Rayleigh decoherence: Uys/Biercuk/.../Ozeri/Bollinger PRL 2010
                      [Ref 11] — closest to a "scattering-theory" reference.

The canonical "exactly-solved scattering theory" for hyperfine/Zeeman-resolved
Raman/Rayleigh processes is the Kramers-Heisenberg dispersion formula combined
with Wigner-Eckart Clebsch-Gordan factors.  It was developed in:

  - Cline, Heinzen, Wineland, "Spontaneous emission limit on coherence times"
    (and follow-ups by the NIST group),
  - Ozeri et al., PRA 75:042329 (2007), "Errors in trapped-ion quantum gates
    due to spontaneous photon scattering",
  - Wineland 2003 (Ref [19] in this paper).

This module implements that calculation from scratch and compares to the
rates / branching ratios actually used in the paper (and in our replication).

METHOD
------
For 40Ca+ addressed by a pi-polarized beam at 854 nm (D5/2 -> P3/2 transition)
with detuning Delta_P3/2 from resonance:

  qubit = { |0> = |D5/2, mJ = -3/2>, |1> = |D5/2, mJ = -5/2> }, |g> = |S1/2>.

Pi polarization (Delta mJ = 0) drives only |0> -> |P3/2, mJ' = -3/2>; the
|1> = mJ=-5/2 state is dark since |P3/2| has max |mJ'| = 3/2.

Once population reaches |P3/2, mJ'=-3/2>, it spontaneously decays.  The
branching is determined by:

  (i)  the partial Einstein-A coefficients of P3/2 to each fine-structure
       manifold (S1/2, D3/2, D5/2), measured in Gerritsma et al. 2008,
  (ii) the Wigner-Eckart Clebsch-Gordan factors |<J_f m_f | J' m'; 1 q>|^2
       for the magnetic sublevel branching, which we compute exactly from
       Wigner 3j symbols.

The total scattering rate from |0> is set by the second-order Kramers-
Heisenberg formula

  Gamma^(0 -> b) = A_{P3/2 -> b'-manifold}  *  P(b'-mJ -> b-mJ)
                  * |Omega^{(0)} / Delta_P3/2|^2

where the Clebsch-Gordan factor P(...) is the conditional probability that a
P3/2-mJ' decay event reaches the specific final magnetic sublevel of the
specified manifold.

We then compute the qubit-frame channels:
  - Elastic (|0> -> |0>):    final = |D5/2, mJ=-3/2>
  - Raman   (|0> -> |1>):    final = |D5/2, mJ=-5/2>
  - Leakage (|0> -> |g>):    final NOT in {mJ=-3/2, -5/2} of D5/2
                             (includes S1/2, D3/2, and D5/2 mJ=-1/2)

These are compared head-to-head against the paper's own branching ratios
(taken from Gerritsma 2008 Ref [18]) and the rates used in our replication.

USAGE
-----
  python ref8_scattering_comparator.py

  Generates:
    figures/this_paper_vs_ref8_scattering.png
    (and prints an agreement table to stdout)
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

try:
    from sympy.physics.wigner import wigner_3j
    from sympy import Rational
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False


# --------------------------------------------------------------------------
# 1. Atomic data for 40Ca+
# --------------------------------------------------------------------------
# Source: NIST ASD + Gerritsma et al. 2008 (Ref [18] in the paper).
# Partial Einstein-A coefficients out of 4P3/2.

A_P32_S12 = 1.350e8     # s^-1, P3/2 -> S1/2 (393 nm).  Dominant.
A_P32_D52 = 8.48e6      # s^-1, P3/2 -> D5/2 (854 nm).  Used in Eq. (11).
A_P32_D32 = 9.42e5      # s^-1, P3/2 -> D3/2 (850 nm).
A_P32_TOT = A_P32_S12 + A_P32_D52 + A_P32_D32   # ~ 1.444e8 s^-1

# Branching of P3/2 across fine-structure manifolds
B_P32_S12 = A_P32_S12 / A_P32_TOT
B_P32_D52 = A_P32_D52 / A_P32_TOT
B_P32_D32 = A_P32_D32 / A_P32_TOT


# --------------------------------------------------------------------------
# 2. Wigner-Eckart magnetic-sublevel branching from |P3/2, mJ'=-3/2>
# --------------------------------------------------------------------------
# For an electric-dipole decay |J', m'> -> |J_f, m_f> + photon(q),
# the (squared) line strength is
#
#     S(m', m_f, q)  =  (2 J_f + 1) * | wigner_3j(J',1,J_f; -m', q, m_f) |^2 ,
#
# nonzero only when q = m' - m_f.  Within a fixed J_f manifold, the
# conditional branching from m' to m_f is
#
#     P(m_f | J_f, m')  =  S(m', m_f, q) / sum_{m_f'} S(m', m_f', q').

def _cg2(Jp, mp, Jf, mf):
    """ |<J_f m_f | J' m'; 1, q>|^2  (q = m' - m_f). """
    q = mp - mf
    if abs(q) > 1:
        return 0.0
    if HAVE_SYMPY:
        Jp_ = Rational(int(2*Jp), 2); mp_ = Rational(int(2*mp), 2)
        Jf_ = Rational(int(2*Jf), 2); mf_ = Rational(int(2*mf), 2)
        q_  = Rational(int(2*q),  2)
        w = wigner_3j(Jp_, 1, Jf_, -mp_, q_, mf_)
        return float((2*Jf + 1) * w**2)
    # Closed-form fallback for the few cases we need (P3/2 -> D5/2 / D3/2 / S1/2)
    return _cg2_explicit(Jp, mp, Jf, mf, q)


def _cg2_explicit(Jp, mp, Jf, mf, q):
    """Hard-coded values for J' = 3/2, mp = -3/2 (the only case we need)."""
    if not (Jp == 1.5 and mp == -1.5):
        raise NotImplementedError("install sympy for general Wigner-3j")
    table = {
        # (J_f, m_f, q) : |CG|^2
        (2.5, -2.5, -1): 1.0,         # to D5/2 mJ=-5/2 via sigma- emission
        (2.5, -1.5,  0): 0.4,         # to D5/2 mJ=-3/2 via pi
        (2.5, -0.5,  1): 0.1,         # to D5/2 mJ=-1/2 via sigma+
        (1.5, -1.5, -1): 0.6,         # to D3/2 mJ=-3/2 via sigma-
        (1.5, -0.5,  0): 0.4,         # to D3/2 mJ=-1/2 via pi
        (1.5,  0.5,  1): 0.0,         # forbidden
        (0.5, -0.5, -1): 0.5,         # to S1/2 mJ=-1/2 via sigma-
        (0.5,  0.5,  0): 0.0,
    }
    return table.get((Jf, mf, q), 0.0)


def _branching_from_mp(mp, Jf):
    """Conditional probabilities P(m_f | J_f, m') for decay from |J'=3/2, m'>."""
    Jp = 1.5
    mf_list = [-Jf + k for k in range(int(2*Jf)+1)]
    weights = {mf: _cg2(Jp, mp, Jf, mf) for mf in mf_list}
    Z = sum(weights.values())
    if Z == 0:
        return {mf: 0.0 for mf in mf_list}
    return {mf: w / Z for mf, w in weights.items()}


# --------------------------------------------------------------------------
# 3. Reference scattering-theory calculation
# --------------------------------------------------------------------------
@dataclass
class ScatteringResult:
    """Branching ratios + absolute rates for the qubit channels."""
    f_leak: float       # fraction of total scatter that ends up as leakage
    f_raman: float      # fraction Raman (|0> -> |1>)
    f_elastic: float    # fraction elastic (|0> -> |0>)
    Gamma_total: float  # total scattering rate from |0> (s^-1)
    Gamma_leak: float
    Gamma_raman: float
    Gamma_elastic: float
    breakdown: dict     # detailed sub-channel breakdown


def reference_branching_from_clebsch_gordan() -> dict:
    """
    First-principles branching of light scattering from |0> = |D5/2, mJ=-3/2>
    under pi-polarized 854-nm pumping.

    Returns the conditional probabilities for the **qubit-frame** channels
    {leakage, Raman, elastic}, plus a sub-channel breakdown.
    """
    # Pi pump excites only |P3/2, mp=-3/2> (single virtual state).
    mp = -1.5

    # Sub-channel branching = (P3/2 -> manifold) * (mp -> mf within manifold)
    P_S12 = _branching_from_mp(mp, 0.5)
    P_D52 = _branching_from_mp(mp, 2.5)
    P_D32 = _branching_from_mp(mp, 1.5)

    sub = {}

    # Channel: D5/2 mJ=-3/2  =>  ELASTIC (|0> -> |0>)
    sub['D5/2 mJ=-3/2 (elastic)'] = B_P32_D52 * P_D52[-1.5]
    # Channel: D5/2 mJ=-5/2  =>  RAMAN (|0> -> |1>)
    sub['D5/2 mJ=-5/2 (Raman)']   = B_P32_D52 * P_D52[-2.5]
    # Channel: D5/2 mJ=-1/2  =>  LEAKAGE (out of qubit subspace)
    sub['D5/2 mJ=-1/2 (leak)']    = B_P32_D52 * P_D52[-0.5]
    # Channel: S1/2 -> all   =>  LEAKAGE
    sub['S1/2 (leak, 393 nm)']    = B_P32_S12 * sum(P_S12.values())
    # Channel: D3/2 -> all   =>  LEAKAGE
    sub['D3/2 (leak, 850 nm)']    = B_P32_D32 * sum(P_D32.values())

    f_elastic = sub['D5/2 mJ=-3/2 (elastic)']
    f_raman   = sub['D5/2 mJ=-5/2 (Raman)']
    f_leak    = (sub['D5/2 mJ=-1/2 (leak)']
                 + sub['S1/2 (leak, 393 nm)']
                 + sub['D3/2 (leak, 850 nm)'])

    Z = f_elastic + f_raman + f_leak
    return {
        'f_elastic': f_elastic / Z,
        'f_raman':   f_raman   / Z,
        'f_leak':    f_leak    / Z,
        'sub':       sub,
        'Z':         Z,
    }


def reference_rates(Omega_over_Delta: float = 1e-3,
                    A_branching=A_P32_D52) -> ScatteringResult:
    """
    Absolute scattering rates from |0> via the Kramers-Heisenberg / Eq. (12)
    second-order formula, with the **first-principles** branching from
    Wigner-Eckart.

    Parameters
    ----------
    Omega_over_Delta : Rabi-frequency / detuning ratio  (dimensionless, real).
                       Eq. (12): Gamma ~ A * (Omega/Delta)^2.
    A_branching      : partial A coefficient setting the prefactor (s^-1).
                       Default = A(P3/2 -> D5/2) used in the paper Eq. (11).

    Returns
    -------
    ScatteringResult
    """
    # Total scatter rate from |0> = sum over all final manifolds, weighted by
    # their partial A.  Equivalent to A_total * (Omega/Delta)^2  IF the Rabi
    # rate is referred to the *full* P3/2 line.  The paper's convention is to
    # refer Omega^(0) to A_{P3/2->D5/2} (Eq. 11), so the total rate uses the
    # same A_{P3/2->D5/2} prefactor times the inverse of f_elastic+...+f_leak
    # measured in units of B_P32_D52.  We expose both conventions.
    br = reference_branching_from_clebsch_gordan()
    sub = br['sub']

    # Per-channel absolute rates: Gamma_chan = sub[chan] * A_total * (O/D)^2
    # (where A_total picks up *all* P3/2 decay channels).
    pref = A_P32_TOT * Omega_over_Delta**2
    rate_elastic = sub['D5/2 mJ=-3/2 (elastic)']      * pref
    rate_raman   = sub['D5/2 mJ=-5/2 (Raman)']        * pref
    rate_leak    = (sub['D5/2 mJ=-1/2 (leak)']
                    + sub['S1/2 (leak, 393 nm)']
                    + sub['D3/2 (leak, 850 nm)'])     * pref
    rate_total   = rate_elastic + rate_raman + rate_leak

    return ScatteringResult(
        f_leak=br['f_leak'],
        f_raman=br['f_raman'],
        f_elastic=br['f_elastic'],
        Gamma_total=rate_total,
        Gamma_leak=rate_leak,
        Gamma_raman=rate_raman,
        Gamma_elastic=rate_elastic,
        breakdown=sub,
    )


# --------------------------------------------------------------------------
# 4. Comparator: paper-used vs reference-theory
# --------------------------------------------------------------------------
# Paper's branching ratios (from Ref [18], Gerritsma 2008):
PAPER_F_LEAK    = 0.945
PAPER_F_RAMAN   = 0.039
PAPER_F_ELASTIC = 0.016


def comparator_table(Omega_over_Delta: float = 1e-3) -> str:
    """Return a Markdown agreement table comparing the two."""
    ref = reference_rates(Omega_over_Delta)

    rows = [
        ("Channel", "Paper Ref [18]", "Ref scattering theory", "Rel. diff."),
        ("Leakage  (|0> -> |g>, all)", f"{PAPER_F_LEAK:.4f}",
            f"{ref.f_leak:.4f}",
            f"{(ref.f_leak - PAPER_F_LEAK)/PAPER_F_LEAK*100:+.2f}%"),
        ("Raman    (|0> -> |1>)",      f"{PAPER_F_RAMAN:.4f}",
            f"{ref.f_raman:.4f}",
            f"{(ref.f_raman - PAPER_F_RAMAN)/PAPER_F_RAMAN*100:+.2f}%"),
        ("Elastic  (|0> -> |0>)",      f"{PAPER_F_ELASTIC:.4f}",
            f"{ref.f_elastic:.4f}",
            f"{(ref.f_elastic - PAPER_F_ELASTIC)/PAPER_F_ELASTIC*100:+.2f}%"),
    ]

    # Build markdown
    out = []
    out.append("| " + " | ".join(rows[0]) + " |")
    out.append("|" + "|".join("---" for _ in rows[0]) + "|")
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")

    return "\n".join(out)


# --------------------------------------------------------------------------
# 5. Propagate through the analytic correlation function (Eqs. 6-10)
# --------------------------------------------------------------------------
# We use the existing project module to evaluate <P^{otimes 2m}>_no-leak +
# <P^{otimes 2m}>_leak (Eqs. 16-17 of the paper) under both branching
# assumptions and show the curves agree.

def _Pavg_simple(N, Gamma0g, t, m):
    """Eq. (16) approximation:
        <P^{otimes 2m}> = e^{-N Gamma_0g t} +
                         (1 - e^{-N Gamma_0g t}) * Gamma(1/2+m) / [sqrt(pi) Gamma(1+m)]
    """
    leak_prob = 1.0 - np.exp(-N * Gamma0g * t)
    coef = math.gamma(0.5 + m) / (math.sqrt(math.pi) * math.gamma(1 + m))
    return np.exp(-N * Gamma0g * t) + leak_prob * coef


def comparison_data(N=20, m=2, Omega_over_Delta=1e-3, t_max=0.4):
    """Compute <P^{2m}> vs t under (a) paper branching, (b) ref-theory branching."""
    ref = reference_rates(Omega_over_Delta)
    # Total scattering rate from |0> (same for both, as both rescale to match
    # absolute Eq. 11/12); only branching differs.
    Gamma_tot = ref.Gamma_total

    # Leakage rate for the two models
    G0g_paper = PAPER_F_LEAK * Gamma_tot
    G0g_ref   = ref.f_leak    * Gamma_tot

    t = np.linspace(0, t_max, 400)
    P_paper = _Pavg_simple(N, G0g_paper, t, m)
    P_ref   = _Pavg_simple(N, G0g_ref,   t, m)
    return t, P_paper, P_ref, dict(
        Gamma_tot=Gamma_tot,
        G0g_paper=G0g_paper, G0g_ref=G0g_ref,
        f_leak_paper=PAPER_F_LEAK, f_leak_ref=ref.f_leak)


# --------------------------------------------------------------------------
# 6. Plot
# --------------------------------------------------------------------------
def make_figure(out_path):
    ref = reference_rates(Omega_over_Delta=1e-3)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

    # --- panel (a): branching-ratio bar chart ---
    ax = axes[0]
    labels = ['Leakage', 'Raman\n(|0>->|1>)', 'Elastic\n(|0>->|0>)']
    paper_v = [PAPER_F_LEAK, PAPER_F_RAMAN, PAPER_F_ELASTIC]
    ref_v   = [ref.f_leak,    ref.f_raman,    ref.f_elastic]
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w/2, paper_v, w, label='This paper [Ref 18, Gerritsma 2008]',
           color='#1f77b4', alpha=0.85)
    ax.bar(x + w/2, ref_v, w, label='Reference scattering theory\n(Wigner-Eckart + NIST A)',
           color='#d62728', alpha=0.85)
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Branching fraction')
    ax.set_title('(a) Branching ratios from |0> = |D5/2, m=-3/2>\nunder pi-polarized 854 nm pump')
    ax.legend(loc='lower left', fontsize=8)
    ax.grid(True, which='both', axis='y', alpha=0.3)

    # value labels
    for i, (p, r) in enumerate(zip(paper_v, ref_v)):
        ax.text(i - w/2, p, f' {p:.3f}', ha='center', va='bottom', fontsize=8)
        ax.text(i + w/2, r, f' {r:.3f}', ha='center', va='bottom', fontsize=8)

    # --- panel (b): correlation function vs t ---
    ax = axes[1]
    for m, color in [(1, '#1f77b4'), (5, '#2ca02c'), (10, '#d62728')]:
        t, Pp, Pr, info = comparison_data(N=20, m=m, t_max=0.4)
        ax.plot(t, Pp, '-',  color=color, lw=2.0, label=f'Paper, m={m}')
        ax.plot(t, Pr, '--', color=color, lw=1.5, label=f'Ref-theory, m={m}')
    ax.set_xlabel(r'$t$  [units of $1/\Gamma_{\rm tot}$]')
    ax.set_ylabel(r'$\langle P^{\otimes 2m}\rangle$  (Eq. 16)')
    ax.set_title('(b) Correlation functions: paper vs ref scattering-theory branching\n'
                 f'(N=20; total Gamma fixed; only leakage fraction differs)')
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches='tight')
    plt.close(fig)
    return out_path


# --------------------------------------------------------------------------
# 7. CLI
# --------------------------------------------------------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    fig_dir = os.path.normpath(os.path.join(here, '..', 'figures'))
    os.makedirs(fig_dir, exist_ok=True)
    out_fig = os.path.join(fig_dir, 'this_paper_vs_ref8_scattering.png')

    print("=" * 72)
    print("Reference scattering-theory comparator for OSTI 2441075")
    print("=" * 72)
    print()

    # Branching breakdown
    br = reference_branching_from_clebsch_gordan()
    print("Sub-channel breakdown of P3/2(m'=-3/2) decay:")
    for k, v in br['sub'].items():
        print(f"  {k:30s}  {v:.5f}")
    print()
    print(f"  ==> total qubit-frame branching:")
    print(f"      leakage  = {br['f_leak']:.4f}   (paper: {PAPER_F_LEAK})")
    print(f"      Raman    = {br['f_raman']:.4f}   (paper: {PAPER_F_RAMAN})")
    print(f"      elastic  = {br['f_elastic']:.4f}   (paper: {PAPER_F_ELASTIC})")
    print()

    print("Agreement table:")
    print(comparator_table())
    print()

    # Absolute rate sanity check at "Omega/Delta = sqrt(11/A_total)" ~ paper bound
    # Paper: total Gamma < 11 s^-1.  Solve for Omega/Delta:
    target_Gamma = 11.0  # s^-1
    Omega_over_Delta = math.sqrt(target_Gamma / A_P32_TOT)
    res = reference_rates(Omega_over_Delta)
    print(f"At Omega/Delta = {Omega_over_Delta:.3e}  (=> paper's <11 s^-1 bound):")
    print(f"  Gamma_total = {res.Gamma_total:.3f} s^-1")
    print(f"  Gamma_leak  = {res.Gamma_leak:.3f} s^-1")
    print(f"  Gamma_raman = {res.Gamma_raman:.3f} s^-1")
    print(f"  Gamma_elast = {res.Gamma_elastic:.3f} s^-1")
    print()

    out = make_figure(out_fig)
    print(f"Wrote figure: {out}")


if __name__ == '__main__':
    main()
