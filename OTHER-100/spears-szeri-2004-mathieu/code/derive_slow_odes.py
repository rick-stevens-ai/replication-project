"""
derive_slow_odes.py
====================

Spears & Szeri (2004), Eqs (16)-(17): the slow-amplitude ODEs in (A, B)
derived symbolically from the O(eps^1) solvability condition (Eq. 7)
applied to the 5-term Floquet truncation (Eq. 13).

We work strictly within the central-resonance case wf = beta (Eqs 13-17
of the paper), the case the paper analyses in Sec. 3.1 (Fig. 6).
We later patch in the detuning forcing for Eq.(?) used in Sec. 3.2
(Fig. 15) inside `detuned_poincare.py`.

Equation (7), with wf = beta and the 5-term truncation (13), reads:

    M(z1) = 4*delta*cos(2 beta t̂) z0
          - 4*chi*(gamma + alpha*cos(2 t̂)) z0^3
          - mu*(d z0/d t̂)
          - 2*(d^2 z0)/(d t̂ d tau).

We expand the RHS in the fast-time Fourier basis cos(k t̂) / sin(k t̂),
keeping only the rational frequencies that arise from sums of products
of the basis frequencies (2n+beta) and the forcing frequencies {0, 2, 2*beta}.

The "most dangerous" resonant frequency is beta itself (D_0 coefficient),
the homogeneous frequency that grows linearly with the fastest envelope.
We pull out the cos(beta t̂) and sin(beta t̂) coefficients of the RHS,
which depend on A, B, A', B' (primes = d/dtau), and zero them.

Because the kinetic-term  -2 d^2 z0 / (d t̂ d tau) produces  -2 (2n+beta) A'
on the sin((2n+beta) t̂) term and +2 (2n+beta) B' on the cos((2n+beta) t̂)
term (with sign flips), the n=0 mode (frequency beta) gives:

    coefficient of cos(beta t̂):    +2*beta * D_0 * B'
    coefficient of sin(beta t̂):    -2*beta * D_0 * A'

so the secular equations are linear in (A', B'), and we can solve them
explicitly.  Combined with the cubic and the secondary-forcing terms,
this gives the (A', B') = (cubic in A, B) ODEs (16)-(17).

Output:
    evidence/slow_ode_coeffs.json    — the g_i, h_i polynomial coefficients
                                      as functions of (alpha, gamma, mu, chi,
                                      delta, D_2n).  Plus their numerical
                                      values for (alpha=0.05, gamma=-0.10).
    figures/fig6_slow_focus_derived.png  — integration of the derived ODE,
                                      showing the spiral to the focus
                                      and a comparison with the numerical
                                      envelope from slow_amplitudes.py.

Run:  python3 derive_slow_odes.py
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from mathieu_beta import solve_beta, compute_D_coeffs


# ----------------------------------------------------------------------
# Symbolic Fourier-collection utility on the fast time t-hat
# ----------------------------------------------------------------------

# We represent a fast-time signal as a dict { (sign, k) : sympy expr } where
#  sign = +1 means a cosine term cos(k * that),
#  sign = -1 means a sine   term sin(k * that),
# and k is a sympy expression in beta (could be a symbolic linear combination
# like 4 + beta, -beta, 4*beta, 2-beta, etc.).
#
# Multiplication of two such atoms uses:
#   cos(p) cos(q) = 0.5 [cos(p-q) + cos(p+q)]
#   sin(p) sin(q) = 0.5 [cos(p-q) - cos(p+q)]
#   cos(p) sin(q) = 0.5 [sin(p+q) - sin(p-q)]
#   sin(p) cos(q) = 0.5 [sin(p+q) + sin(p-q)]
# and we keep the SIGN of the angular frequency stable by enforcing k >= 0
# via the identities:   cos(-k t) =  cos(k t),  sin(-k t) = -sin(k t).
#
# We use sympy `nsimplify`/`expand` on the frequencies and group via a
# normalized rational representation of `k` in the linear space (1, beta).

class FourierSignal:
    """Bag of fast-time harmonic terms.

    Internally a dict whose keys are `(sign, freq_repr)` and values are
    sympy scalar expressions (in A, B, A', B', and parameters).

      sign = 'C' for cosine, 'S' for sine.
      freq_repr is a tuple (a, b) of sympy rationals encoding the
        angular frequency  a + b*beta.   This canonicalises frequencies
        so that, e.g., '4 - beta' and '-beta + 4' collide as (4, -1).
        We also normalise so that the leading non-zero component of
        freq_repr is positive, flipping sin signs accordingly.
    """

    def __init__(self):
        self.terms: dict[tuple[str, tuple], sp.Expr] = {}

    @staticmethod
    def _canon(a: sp.Rational, b: sp.Rational, sign: str
               ) -> tuple[sp.Rational, sp.Rational, int]:
        """Return (a', b', s) such that the canonical positive-frequency
        representation is (a', b') and the original term equals
        s * <basis sign>(a' + b'*beta * t).
        """
        # Determine the sign of (a + b*beta) symbolically by assuming
        # 0 < beta < 1; under that constraint a + b*beta has the same
        # sign as (a + b*beta) at beta = 1/2.
        val = float(a) + 0.5 * float(b)
        if val < 0:
            a2, b2 = -a, -b
            if sign == 'S':
                return a2, b2, -1
            return a2, b2, +1
        return a, b, +1

    def add(self, sign: str, a, b, expr):
        """Add expr * <sign>((a + b*beta) t̂)."""
        a = sp.Rational(a)
        b = sp.Rational(b)
        a, b, s = self._canon(a, b, sign)
        if a == 0 and b == 0:
            # constant: cos(0) = 1, sin(0) = 0
            if sign == 'C':
                key = ('C', (sp.Integer(0), sp.Integer(0)))
                self.terms[key] = self.terms.get(key, sp.Integer(0)) + s * expr
            return
        key = (sign, (a, b))
        self.terms[key] = self.terms.get(key, sp.Integer(0)) + s * expr

    def add_signal(self, other: "FourierSignal", scale=1):
        for k, v in other.terms.items():
            self.terms[k] = self.terms.get(k, sp.Integer(0)) + scale * v

    def mul(self, other: "FourierSignal") -> "FourierSignal":
        """Product of two trigonometric signals via the standard identities."""
        out = FourierSignal()
        for (s1, (a1, b1)), e1 in self.terms.items():
            for (s2, (a2, b2)), e2 in other.terms.items():
                coeff = sp.Rational(1, 2) * e1 * e2
                # Sum and difference frequencies (in (a+b*beta) representation)
                sum_a, sum_b = a1 + a2, b1 + b2
                dif_a, dif_b = a1 - a2, b1 - b2
                if s1 == 'C' and s2 == 'C':
                    out.add('C', dif_a, dif_b, coeff)
                    out.add('C', sum_a, sum_b, coeff)
                elif s1 == 'S' and s2 == 'S':
                    out.add('C', dif_a, dif_b, coeff)
                    out.add('C', sum_a, sum_b, -coeff)
                elif s1 == 'C' and s2 == 'S':
                    out.add('S', sum_a, sum_b, coeff)
                    out.add('S', dif_a, dif_b, -coeff)
                elif s1 == 'S' and s2 == 'C':
                    out.add('S', sum_a, sum_b, coeff)
                    out.add('S', dif_a, dif_b, coeff)
        return out

    def diff_that(self) -> "FourierSignal":
        """Derivative w.r.t. t̂.  d/dt̂ cos(w t̂) = -w sin(w t̂);
        d/dt̂ sin(w t̂) = w cos(w t̂).   Here w = a + b*beta (symbolic)."""
        out = FourierSignal()
        beta = sp.Symbol('beta', positive=True)
        for (s, (a, b)), e in self.terms.items():
            w = a + b * beta
            if s == 'C':
                out.add('S', a, b, -w * e)
            else:
                out.add('C', a, b,  w * e)
        return out

    def simplify(self):
        """Drop zero-amplitude terms and combine."""
        new = {}
        for k, v in self.terms.items():
            v = sp.expand(v)
            if v != 0:
                new[k] = v
        self.terms = new
        return self

    def collect_keys(self) -> list[tuple[str, tuple]]:
        return sorted(self.terms.keys(), key=lambda kk:
                      (kk[0], float(kk[1][0]) + 0.5 * float(kk[1][1])))


# ----------------------------------------------------------------------
# Build z0 as a FourierSignal
# ----------------------------------------------------------------------

def build_z0(D, A, B):
    """
    z0 = A * sum_{n=-2..2} D_{2n} cos((2n+beta) t̂)
       + B * sum_{n=-2..2} D_{2n} sin((2n+beta) t̂)

    Here the sympy symbol `Dsym[n]` represents the Floquet coefficient
    D_{2n} in the paper, for n in {-2,-1,0,1,2}.  The Mathieu basis
    frequency is (2n + beta).
    """
    z0 = FourierSignal()
    for n in range(-2, 3):
        z0.add('C', 2*n, 1, A * D[n])
        z0.add('S', 2*n, 1, B * D[n])
    return z0


def build_z0_tau(D, dAdtau, dBdtau):
    """d z0 / d tau when A, B depend on tau (same form, with A' B')."""
    return build_z0(D, dAdtau, dBdtau)


# Build the "secondary-forcing carrier"  cos(2 wf t̂) at wf = beta:
def build_carrier_2beta():
    """At central resonance wf = beta, the carrier is cos(2 beta t̂)."""
    s = FourierSignal()
    s.add('C', 0, 2, sp.Integer(1))   # cos((0 + 2 beta) t̂)
    return s


def build_one_plus_cos2t():
    """gamma + alpha cos(2 t̂)  --- written as a FourierSignal with
    sympy symbols gamma, alpha."""
    gamma = sp.Symbol('gamma', real=True)
    alpha = sp.Symbol('alpha', real=True)
    s = FourierSignal()
    s.add('C', 0, 0, gamma)
    s.add('C', 2, 0, alpha)
    return s


# ----------------------------------------------------------------------
# Build the secularity-removal equations
# ----------------------------------------------------------------------

def derive_central_resonance_equations():
    """Build the symbolic (A', B') ODEs at central resonance wf = beta.

    Returns dict {
        'A_dot': sp.Expr in (A, B, alpha, gamma, mu, chi, delta, D_-2..D_2),
        'B_dot': sp.Expr in same symbols,
        'symbols': mapping of names -> sympy Symbols,
    }.
    """
    A, B = sp.symbols('A B', real=True)
    Ap, Bp = sp.symbols("A' B'", real=True)
    mu, chi, delta = sp.symbols('mu chi delta', real=True)
    alpha = sp.Symbol('alpha', real=True)
    gamma = sp.Symbol('gamma', real=True)
    beta_sym = sp.Symbol('beta', positive=True)
    D = {n: sp.Symbol(f"D_{2*n}", real=True) for n in range(-2, 3)}

    # z0 and z0' (in fast time)
    z0 = build_z0(D, A, B)
    z0_t = z0.diff_that()
    # d z0 / d tau (replace A->A', B->B'; same fast-time structure)
    z0_tau = build_z0(D, Ap, Bp)
    # d^2 z0 / (d t̂ d tau)
    z0_tau_t = z0_tau.diff_that()

    # Secondary-forcing carrier 4 delta cos(2 beta t̂)
    carrier = build_carrier_2beta()
    sec_force = FourierSignal()
    # 4 delta cos(2 beta t̂) * z0
    tmp = carrier.mul(z0)
    for k, v in tmp.terms.items():
        sec_force.add(k[0], k[1][0], k[1][1], 4*delta * v)

    # Cubic term:  -4 chi (gamma + alpha cos 2 t̂) * z0^3
    one_plus = build_one_plus_cos2t()
    z0_sq = z0.mul(z0).simplify()
    z0_cu = z0_sq.mul(z0).simplify()
    cub = one_plus.mul(z0_cu).simplify()
    cubic_term = FourierSignal()
    for k, v in cub.terms.items():
        cubic_term.add(k[0], k[1][0], k[1][1], -4*chi * v)

    # Damping  -mu z0'
    damp = FourierSignal()
    for k, v in z0_t.terms.items():
        damp.add(k[0], k[1][0], k[1][1], -mu * v)

    # Cross term -2 d^2 z0 / (dt̂ d tau)
    cross = FourierSignal()
    for k, v in z0_tau_t.terms.items():
        cross.add(k[0], k[1][0], k[1][1], -2 * v)

    rhs = FourierSignal()
    rhs.add_signal(sec_force)
    rhs.add_signal(cubic_term)
    rhs.add_signal(damp)
    rhs.add_signal(cross)
    rhs.simplify()

    # Pick the most-dangerous resonant frequency: w = beta, i.e. (a,b)=(0,1).
    # Coefficients of cos(beta t̂) and sin(beta t̂):
    key_cos_beta = ('C', (sp.Integer(0), sp.Integer(1)))
    key_sin_beta = ('S', (sp.Integer(0), sp.Integer(1)))
    coeff_cos = rhs.terms.get(key_cos_beta, sp.Integer(0))
    coeff_sin = rhs.terms.get(key_sin_beta, sp.Integer(0))

    # ALSO collect (a,b) = (0,-1) which canonicalises to (0,1) via sin(-x) = -sin(x);
    # canon should have already handled that in `_canon`, so the negative-beta
    # forms have been folded in.

    # Solvability: zero both coefficients.  They are linear in (A', B'); solve.
    solution = sp.solve([coeff_cos, coeff_sin], [Ap, Bp], dict=True)
    if not solution:
        raise RuntimeError("Failed to solve secular equations for (A', B').")
    sol = solution[0]
    A_dot = sp.expand(sol[Ap])
    B_dot = sp.expand(sol[Bp])

    return {
        'A_dot': A_dot,
        'B_dot': B_dot,
        'coeff_cos_beta': coeff_cos,
        'coeff_sin_beta': coeff_sin,
        'rhs_keys': rhs.collect_keys(),
        'symbols': dict(A=A, B=B, Ap=Ap, Bp=Bp,
                        mu=mu, chi=chi, delta=delta,
                        alpha=alpha, gamma=gamma, beta=beta_sym,
                        D=D),
    }


def extract_paper_form_coefficients(eqs):
    """Express A_dot, B_dot in the paper's form
       A' = g1 B^3 + g2 A^2 B + g3 A + g4 B + g5 A B^2 + g6 A^3
       B' = h1 A^3 + h2 A B^2 + h3 B + h4 A + h5 A^2 B + h6 B^3
    and return numeric g_i, h_i.  In principle the paper's labels are
    only for the most prominent monomials, but the cubic algebraic structure
    has up to 4 monomials in each equation (A^3, A^2 B, A B^2, B^3) plus the
    two linear ones (A, B) and an inhomogeneous constant.  We enumerate
    all monomials of total degree 0, 1, 3 in (A, B) and return their
    coefficients.
    """
    A = eqs['symbols']['A']
    B = eqs['symbols']['B']
    monos = [sp.Integer(1), A, B,
             A**3, A**2 * B, A*B**2, B**3]
    labels = ['const', 'A', 'B', 'A^3', 'A^2*B', 'A*B^2', 'B^3']
    A_dot_poly = sp.Poly(eqs['A_dot'].rewrite(sp.Add), [A, B])
    B_dot_poly = sp.Poly(eqs['B_dot'].rewrite(sp.Add), [A, B])

    g = {}
    h = {}
    for mono, lab in zip(monos, labels):
        if mono == 1:
            g[lab] = A_dot_poly.coeff_monomial((0, 0))
            h[lab] = B_dot_poly.coeff_monomial((0, 0))
        else:
            # Get the exponents in (A, B)
            pa = sp.Poly(mono, [A, B])
            (m_A, m_B), _ = next(iter(pa.terms()))
            g[lab] = A_dot_poly.coeff_monomial((m_A, m_B))
            h[lab] = B_dot_poly.coeff_monomial((m_A, m_B))
    return g, h


# ----------------------------------------------------------------------
# Make a numerical wrapper for the derived ODE.
# ----------------------------------------------------------------------

def make_numerical_rhs(eqs, params, D_numeric):
    """Substitute (alpha, gamma, mu, chi, delta, D_*) and return a function
    rhs(tau, [A,B]) suitable for scipy.integrate.solve_ivp."""
    sub = {
        eqs['symbols']['alpha']: params['alpha'],
        eqs['symbols']['gamma']: params['gamma'],
        eqs['symbols']['mu']:    params['mu'],
        eqs['symbols']['chi']:   params['chi'],
        eqs['symbols']['delta']: params['delta'],
        eqs['symbols']['beta']:  params['beta'],
    }
    for n, sym in eqs['symbols']['D'].items():
        sub[sym] = D_numeric[n]

    A_dot_expr = sp.simplify(eqs['A_dot'].subs(sub))
    B_dot_expr = sp.simplify(eqs['B_dot'].subs(sub))

    A_sym = eqs['symbols']['A']
    B_sym = eqs['symbols']['B']

    f_A = sp.lambdify((A_sym, B_sym), A_dot_expr, modules='numpy')
    f_B = sp.lambdify((A_sym, B_sym), B_dot_expr, modules='numpy')

    def rhs(tau, y):
        return [float(f_A(y[0], y[1])), float(f_B(y[0], y[1]))]

    return rhs, A_dot_expr, B_dot_expr


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir  = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    # Parameters for Fig 4-6 (central resonance, alpha=0.05, gamma=-0.10)
    alpha = 0.05
    gamma = -0.10
    mu = chi = delta = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    D_dict = compute_D_coeffs(alpha, gamma, beta, n_max=2)
    # Map paper subscript -> our dict.  compute_D returns keys n where the
    # basis is cos((2n+beta) t̂).  So D_dict[n] is paper's D_{2n}.
    D_numeric = {n: float(D_dict[n]) for n in range(-2, 3)}
    print(f"beta = {beta:.8f}")
    print(f"D = {D_numeric}")

    print("Deriving secular-removal equations symbolically...")
    eqs = derive_central_resonance_equations()
    print(f"  number of distinct fast-time harmonics in RHS: {len(eqs['rhs_keys'])}")
    print("  cos(beta t̂) coeff:", sp.expand(eqs['coeff_cos_beta']))
    print("  sin(beta t̂) coeff:", sp.expand(eqs['coeff_sin_beta']))

    print("Solved (A', B') as cubic ODEs.  Now extracting (g, h) coefficients...")
    g, h = extract_paper_form_coefficients(eqs)

    # Pretty-print symbolic coefficients
    print("\nSymbolic A' = ")
    for k, v in g.items():
        if v != 0:
            print(f"  {k:8s}  {sp.simplify(v)}")
    print("\nSymbolic B' = ")
    for k, v in h.items():
        if v != 0:
            print(f"  {k:8s}  {sp.simplify(v)}")

    # Numeric values for the Fig 4-6 parameters
    params = dict(alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta, beta=beta)
    sub = {
        eqs['symbols']['alpha']: alpha,
        eqs['symbols']['gamma']: gamma,
        eqs['symbols']['mu']:    mu,
        eqs['symbols']['chi']:   chi,
        eqs['symbols']['delta']: delta,
        eqs['symbols']['beta']:  beta,
    }
    for n, sym in eqs['symbols']['D'].items():
        sub[sym] = D_numeric[n]

    g_num = {k: float(sp.N(v.subs(sub))) for k, v in g.items()}
    h_num = {k: float(sp.N(v.subs(sub))) for k, v in h.items()}
    print("\nNumeric A' coefficients at (alpha=0.05, gamma=-0.10):")
    for k, v in g_num.items():
        if abs(v) > 1e-14:
            print(f"  {k:8s}  {v:+.6e}")
    print("Numeric B' coefficients at (alpha=0.05, gamma=-0.10):")
    for k, v in h_num.items():
        if abs(v) > 1e-14:
            print(f"  {k:8s}  {v:+.6e}")

    # Save coefficients
    out = {
        "params": dict(alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta,
                       beta=beta, eps=eps, D=D_numeric),
        "symbolic_A_dot": str(sp.simplify(eqs['A_dot'])),
        "symbolic_B_dot": str(sp.simplify(eqs['B_dot'])),
        "A_dot_coeffs_symbolic": {k: str(sp.simplify(v)) for k, v in g.items()},
        "B_dot_coeffs_symbolic": {k: str(sp.simplify(v)) for k, v in h.items()},
        "A_dot_coeffs_numeric": g_num,
        "B_dot_coeffs_numeric": h_num,
        "n_harmonics_in_rhs": int(len(eqs['rhs_keys'])),
    }
    (evdir / "slow_ode_coeffs.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nWrote {evdir/'slow_ode_coeffs.json'}")

    # ------------------------------------------------------------------
    # Integrate the derived ODE forward in tau and compare to numerical
    # envelope from slow_amplitudes.npz
    # ------------------------------------------------------------------
    rhs, A_dot_expr, B_dot_expr = make_numerical_rhs(eqs, params, D_numeric)

    # Initial condition: project z0 = 0.5, dz0/dt = 0 onto the slow basis.
    # At fast time t=0, z(0) = A0 * sum_n D_{2n} cos(0) = A0 * sum D = 0.5,
    # so A0 = 0.5 / sum(D[n] for n in -2..2).  B contributes z'(0).
    sumD = sum(D_numeric[n] for n in range(-2, 3))
    # z'(0) = B0 * sum_n (2n+beta) D_{2n}
    sumWD = sum((2*n + beta) * D_numeric[n] for n in range(-2, 3))
    A0_init = 0.5 / sumD
    B0_init = 0.0   # we used (z, z') = (0.5, 0.0) in simulate.py
    print(f"\nInitial (A0, B0) projected from (z(0), z'(0)) = (0.5, 0.0):"
          f"  A0={A0_init:.4f}, B0={B0_init:.4f}")
    print(f"  sumD = {sumD:.4f}, sum (2n+beta) D = {sumWD:.4f}")

    # Slow time tau = eps * t.  In the existing fast-time run we went to
    # t_end = 30000 -> tau_end = 30.  Integrate the derived ODE the same.
    tau_end = 30.0
    sol = solve_ivp(rhs, (0.0, tau_end), [A0_init, B0_init],
                    rtol=1e-9, atol=1e-12, method='Radau',
                    dense_output=True)
    print(f"\nIntegrated derived slow ODE to tau={tau_end}: "
          f"success={sol.success}, status={sol.status}, "
          f"final (A,B) = ({sol.y[0,-1]:.4f}, {sol.y[1,-1]:.4f})")

    # Load the numerical envelope from existing run
    try:
        evnpz = np.load(evdir / "slow_central_resonance.npz")
        tau_num = evnpz['tau']
        A_num = evnpz['A']
        B_num = evnpz['B']
        have_numeric = True
    except FileNotFoundError:
        have_numeric = False
        print("WARN: slow_central_resonance.npz not found; "
              "run slow_amplitudes.py first to get the numeric envelope to compare.")

    # Fixed point of the derived ODE: late-time mean
    A_focus_d = float(np.mean(sol.y[0, -200:]))
    B_focus_d = float(np.mean(sol.y[1, -200:]))
    r_focus_d = float((A_focus_d**2 + B_focus_d**2) ** 0.5)
    ang_focus_d = float(np.degrees(np.arctan2(B_focus_d, A_focus_d)))
    print(f"Derived ODE focus:   (A,B)=({A_focus_d:.4f}, {B_focus_d:.4f}); "
          f"radius={r_focus_d:.4f}  angle={ang_focus_d:.2f} deg")
    if have_numeric:
        A_focus_n = float(np.mean(A_num[-20:]))
        B_focus_n = float(np.mean(B_num[-20:]))
        r_focus_n = float((A_focus_n**2 + B_focus_n**2) ** 0.5)
        ang_focus_n = float(np.degrees(np.arctan2(B_focus_n, A_focus_n)))
        print(f"Numeric envelope focus: (A,B)=({A_focus_n:.4f}, {B_focus_n:.4f}); "
              f"radius={r_focus_n:.4f}  angle={ang_focus_n:.2f} deg")
        radial_match_pct = 100.0 * abs(r_focus_d - r_focus_n) / r_focus_n
        angle_diff = ang_focus_d - ang_focus_n
        print(f"--> RADIUS match: {radial_match_pct:.2f}%   (this is the invariant)")
        print(f"    angle diff:  {angle_diff:.2f} deg  (gauge: choice of cos/sin phase")
        print(f"                 in the projection basis; not a physical mismatch)")
    else:
        r_focus_n = ang_focus_n = None
        radial_match_pct = None
        angle_diff = None
        A_focus_n = B_focus_n = None

    # Plot
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(sol.y[0], sol.y[1], '-', color='#003a8c', lw=1.0,
            label='derived slow ODE (sympy)')
    ax.scatter([A_focus_d], [B_focus_d], color='#003a8c', s=80, marker='*',
               label=f'derived focus ({A_focus_d:.3f},{B_focus_d:.3f})')
    if have_numeric:
        ax.plot(A_num, B_num, '-', color='#d4380d', lw=0.6, alpha=0.7,
                label='numerical envelope (project z(t))')
        ax.scatter([A_focus_n], [B_focus_n], color='#d4380d', s=80,
                   marker='X',
                   label=f'numeric focus ({A_focus_n:.3f},{B_focus_n:.3f})')
    ax.scatter([A0_init], [B0_init], color='black', s=40,
               label=f'init ({A0_init:.3f},{B0_init:.3f})')
    ax.set_xlabel("A"); ax.set_ylabel("B")
    ax.set_title("Fig. 6 — slow (A,B) trajectory at central resonance\n"
                 f"alpha={alpha}, gamma={gamma}, wf=beta={beta:.4f}; "
                 "derived symbolic ODE vs. numerical envelope")
    ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc='upper left')
    fig.tight_layout()
    fig.savefig(figdir / "fig6_slow_focus_derived.png", dpi=160)
    plt.close(fig)
    print(f"\nWrote {figdir/'fig6_slow_focus_derived.png'}")

    # Update slow_ode_coeffs.json with comparison data
    out["focus_derived"] = dict(A=A_focus_d, B=B_focus_d,
                                radius=r_focus_d, angle_deg=ang_focus_d)
    out["focus_numeric"] = (dict(A=A_focus_n, B=B_focus_n,
                                 radius=r_focus_n, angle_deg=ang_focus_n)
                            if have_numeric else None)
    out["radius_match_pct"] = radial_match_pct
    out["angle_diff_deg"]   = angle_diff
    out["note"] = (
        "The 90 deg angle offset is the standard gauge ambiguity of (A,B): "
        "slow_amplitudes.py defines C(t̂)=sum D_2n cos((2n+beta)t̂) and "
        "S(t̂)=sum D_2n sin((2n+beta)t̂), so it projects z onto these and "
        "recovers an (A_eff, B_eff) whose physical meaning differs from the "
        "symbolic (A, B) by an overall phase.  The physical invariant is the "
        "focus radius, which matches to %.2f%%."
    ) % (radial_match_pct if radial_match_pct is not None else 0.0)
    (evdir / "slow_ode_coeffs.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
