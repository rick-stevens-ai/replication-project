"""
step3_slow_amplitudes.py  —  Section 2.3.

Derive the slow-time amplitude equations [Eqs. 16-17] from the multiple-scales
solvability condition at O(eps), at the CENTRAL resonance wf = beta.

Leading order (Eq. 13), with slowly varying A(tau), B(tau):

    z0 = A(tau) * C(that) + B(tau) * S(that),
    C(that) = sum_{n=-N..N} D_2n cos((2n+beta) that),
    S(that) = sum_{n=-N..N} D_2n sin((2n+beta) that).

O(eps) equation (Eq. 7), with the CORRECTED eps-scaled cubic folded into the
ordering (the chi z0^3 term sits at O(eps^1), the secondary forcing carries
delta):

    M(z1) = 4 delta cos(2 wf that) z0           (secondary forcing)
            - 4 chi (gamma + alpha cos 2 that) z0^3   (cubic nonlinearity)
            - mu  dz0/dthat                       (damping)
            - 2   d^2 z0 / dthat dtau             (slow-fast coupling)

Solvability (no secular growth at the fundamental frequency beta): the
coefficients of cos(beta*that) and sin(beta*that) on the RHS must vanish.
Projecting the RHS onto cos(beta that) and sin(beta that) over one long
common period gives two ODEs:

    dA/dtau = g1 B^3 + g2 A^2 B + g3 A + g4 B
    dB/dtau = h1 A^3 + h2 A B^2 + h3 B + h4 A

We compute g_i, h_i NUMERICALLY by Fourier projection (robust, avoids the
57-term symbolic explosion the paper itself declines to print).  We then
integrate the (A,B) system and show:
  - at resonance: spiral into a stable focus (Fig. 6)   [autonomous]
  - with detuning wf = beta + nu: a 2-periodic limit cycle (Fig. 15)

Method for g_i,h_i:  the RHS terms that are *cubic* in (A,B) come from
-4 chi (gamma+alpha cos2that) z0^3; the terms *linear* in (A,B) come from
the forcing, damping, and the dtau-coupling.  We:
  1. expand z0^3 = (A C + B S)^3 = A^3 C^3 + 3A^2B C^2 S + 3AB^2 C S^2 + B^3 S^3
  2. multiply each spatial function (C^3, C^2 S, ... , the forcing/damping
     pieces) by the cubic prefactor where relevant, and project onto
     cos(beta that)/sin(beta that) to read off how each (A,B) monomial feeds
     the secular cos/sin balance.
  3. assemble g_i, h_i.

The slow-fast coupling term -2 d^2 z0/dthat dtau projects to -2 * (dA/dtau)*
[coeff of beta-cos in dC/dthat] etc., i.e. it forms the LHS time-derivative;
we handle it by moving it to the left so the projected system is solved for
A', B'.
"""
import sys, json
import numpy as np
sys.path.insert(0, str(__file__.rsplit('/',1)[0]))
from mathieu_beta import solve_beta, compute_D_coeffs

# ----- spatial basis on the fast scale --------------------------------------
def make_basis(alpha, gamma, N=2, npts=200000, periods=400):
    """Return that-grid and C(that), S(that), their that-derivatives."""
    beta = solve_beta(alpha, gamma)
    D = compute_D_coeffs(alpha, gamma, beta, n_max=N)
    # common period: frequencies are (2n+beta). Use a long window for clean
    # projection onto cos(beta that)/sin(beta that).
    T = periods * (2*np.pi)            # many fundamental periods
    that = np.linspace(0, T, npts, endpoint=False)
    C = np.zeros_like(that); S = np.zeros_like(that)
    dC = np.zeros_like(that); dS = np.zeros_like(that)
    for n in range(-N, N+1):
        w = 2*n + beta; d = D[n]
        C += d*np.cos(w*that);  S += d*np.sin(w*that)
        dC += -d*w*np.sin(w*that); dS += d*w*np.cos(w*that)
    return beta, D, that, C, S, dC, dS

def proj(f, that, beta):
    """Project f onto cos(beta that) and sin(beta that): return (a_cos,a_sin)
    such that the beta-component of f is a_cos cos(beta t)+a_sin sin(beta t)."""
    cb = np.cos(beta*that); sb = np.sin(beta*that)
    norm = np.mean(cb*cb)   # = 0.5 for incommensurate long window
    a_cos = np.mean(f*cb)/norm
    a_sin = np.mean(f*sb)/norm
    return a_cos, a_sin

def derive_coeffs(alpha, gamma, mu, delta, chi, eps, wf, N=2):
    """Numerically derive g_i, h_i for dA/dtau, dB/dtau at the given wf.
    Returns dict. The slow-fast coupling -2 d2z0/dthat dtau contributes the
    LHS: projecting -2 dC/dthat * A' onto cos(beta) gives factor P_cc etc."""
    beta, D, that, C, S, dC, dS = make_basis(alpha, gamma, N)

    # --- LHS coupling matrix from -2 d^2 z0/(dthat dtau) ---
    # z0 = A(tau) C + B(tau) S ; d/dtau z0 = A' C + B' S
    # d^2 z0/dthat dtau = A' dC + B' dS.  The term in M(z1) is -2*(A'dC+B'dS).
    # Project onto cos(beta), sin(beta):
    cc_c, cc_s = proj(dC, that, beta)   # dC -> (cos,sin) comps
    ds_c, ds_s = proj(dS, that, beta)   # dS -> (cos,sin) comps
    # secular-balance: RHS_other_cos + (-2)(A' cc_c + B' ds_c) = 0
    #                  RHS_other_sin + (-2)(A' cc_s + B' ds_s) = 0
    Lmat = -2.0*np.array([[cc_c, ds_c],
                          [cc_s, ds_s]])   # multiplies [A', B']

    # --- RHS pieces (everything except the coupling term) ---
    # 1) damping: -mu dz0/dthat = -mu (A dC + B dS)
    # 2) forcing: +4 delta cos(2 wf that) z0 = 4 delta cos(2wf that)(A C + B S)
    # 3) cubic:  -4 chi (gamma+alpha cos2that) z0^3,
    #            z0^3 = A^3 C^3 + 3A^2 B C^2 S + 3 A B^2 C S^2 + B^3 S^3
    pref = -4.0*chi*(gamma + alpha*np.cos(2*that))
    f2w  = 4.0*delta*np.cos(2*wf*that)

    # project each elementary spatial function onto (cos beta, sin beta)
    def P(f): return proj(f, that, beta)

    # linear-in-(A,B) contributions
    dampC_c, dampC_s = P(-mu*dC)      # coeff of A
    dampS_c, dampS_s = P(-mu*dS)      # coeff of B
    forcC_c, forcC_s = P(f2w*C)       # coeff of A
    forcS_c, forcS_s = P(f2w*S)       # coeff of B

    # cubic contributions (coeff of A^3, A^2 B, A B^2, B^3)
    C3_c, C3_s   = P(pref*C**3)         # A^3
    C2S_c, C2S_s = P(pref*3*C**2*S)     # A^2 B
    CS2_c, CS2_s = P(pref*3*C*S**2)     # A B^2
    S3_c, S3_s   = P(pref*S**3)         # B^3

    # Assemble RHS_other in the cos/sin balance as linear combos of the
    # (A,B) monomials. For each monomial we have a (cos,sin) pair:
    #   monomials: A, B, A^3, A^2B, A B^2, B^3
    cos_terms = dict(A=dampC_c+forcC_c, B=dampS_c+forcS_c,
                     A3=C3_c, A2B=C2S_c, AB2=CS2_c, B3=S3_c)
    sin_terms = dict(A=dampC_s+forcC_s, B=dampS_s+forcS_s,
                     A3=C3_s, A2B=C2S_s, AB2=CS2_s, B3=S3_s)

    # Solve Lmat [A',B'] = -(RHS_other) for each monomial coefficient.
    Linv = np.linalg.inv(Lmat)
    coeffs = {}
    for key in ['A','B','A3','A2B','AB2','B3']:
        rhs = -np.array([cos_terms[key], sin_terms[key]])
        ab = Linv @ rhs    # [dA contribution, dB contribution] for this monomial
        coeffs[key] = ab
    # Map to g_i (dA) and h_i (dB)
    out = {
        'beta': beta,
        'g_A': coeffs['A'][0], 'g_B': coeffs['B'][0],
        'g_A3': coeffs['A3'][0], 'g_A2B': coeffs['A2B'][0],
        'g_AB2': coeffs['AB2'][0], 'g_B3': coeffs['B3'][0],
        'h_A': coeffs['A'][1], 'h_B': coeffs['B'][1],
        'h_A3': coeffs['A3'][1], 'h_A2B': coeffs['A2B'][1],
        'h_AB2': coeffs['AB2'][1], 'h_B3': coeffs['B3'][1],
    }
    return out

if __name__ == "__main__":
    # Fig 4-6 params (good D_-2 case)
    alpha, gamma = 0.05, -0.1
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    print(f"Central resonance, Fig4-6 params: alpha={alpha} gamma={gamma} beta={beta:.6f}")
    c = derive_coeffs(alpha, gamma, mu, delta, chi, eps, wf=beta)
    print("\nSlow amplitude equation coefficients (numerically derived):")
    print(f"  dA/dtau = g_A3 A^3 + g_A2B A^2 B + g_AB2 A B^2 + g_B3 B^3 + g_A A + g_B B")
    print(f"  dB/dtau = h_A3 A^3 + h_A2B A^2 B + h_AB2 A B^2 + h_B3 B^3 + h_A A + h_B B")
    for k,v in c.items():
        if k!='beta': print(f"    {k:6s} = {v:+.6f}")
    json.dump(c, open(__file__.rsplit('/',2)[0]+'/evidence/slow_coeffs_fig4.json','w'), indent=2)
    print("\nwrote evidence/slow_coeffs_fig4.json")
