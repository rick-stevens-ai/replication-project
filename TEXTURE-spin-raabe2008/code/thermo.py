"""
Claims C1 & C2: ideal-mixing configurational entropy (Eq. 2) and finite-T free
energy of formation (Eq. 3) for binary Ti_x X_(1-x), and the resulting
temperature-driven shift of the beta-stabilization threshold.

Raabe et al. 2008 (arXiv:0811.0157), Eqs. (2)-(3), Figs. 1c/1d.

  Eq.2:  Sconfig(x) = -kB [ x ln x + (1-x) ln(1-x) ]      (NOTE sign, see below)
  Eq.3:  Ff(x,T)    = <Ef(x)> - T * Sconfig(x)

IMPORTANT sign note: the paper prints Eq.(2) as
    Sconfig = kB[x ln x + (1-x) ln(1-x)]
which is NEGATIVE (a typo/omitted minus that is common in the literature). For
mixing to LOWER the free energy (Ff = <Ef> - T*S must DECREASE as T rises, which
is what the paper's Figs 1a->1c show), the entropy must be POSITIVE, i.e.
    Sconfig = -kB[x ln x + (1-x) ln(1-x)] >= 0.
We use the physically-correct positive form and verify it reproduces the paper's
qualitative claim (finite-T lowers Ef, threshold concentration drops).

We do NOT have the DFT <Ef(x)> curve (that needs VASP). Instead we build a
minimal analytic surrogate for <Ef(x)> that reproduces the two T=0 anchors the
paper states in text, then test whether Eq.(3) reproduces the *stated*
finite-T threshold shifts. This isolates the ENTROPY MODEL (the reproducible
part) from the DFT energies (the non-tractable part).
"""
import numpy as np

kB = 8.617333262e-5  # eV/atom/K
kB_kJ = 8.314462618e-3  # kJ/mol/K  (for reporting in kJ/mol)

# hcp<->bcc transition temperature of pure Ti used as reference in Eq.3
T_TRANS = 882.0 + 273.15  # ~1155 K  (paper: 881-882 C)


def s_config(x):
    """Positive ideal-mixing entropy per atom, eV/K. x in (0,1)."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    m = (x > 0) & (x < 1)
    out[m] = -kB * (x[m] * np.log(x[m]) + (1 - x[m]) * np.log(1 - x[m]))
    return out


def s_config_scalar(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -kB * (x * np.log(x) + (1 - x) * np.log(1 - x))


# ---------------------------------------------------------------------------
# Minimal analytic surrogate for the beta-phase T=0 formation energy <Ef_bcc(x)>
# where x is the Ti fraction... but the paper reports thresholds in terms of the
# SOLUTE (Nb/Mo) concentration. We parametrize by solute fraction c = 1-x.
#
# Anchors from paper TEXT (not fabricated -- quoted):
#   Ti-Nb bcc:  Ef(T=0) becomes negative only for Nb > ~93 at.%.
#   Ti-Mo bcc:  Ef(T=0) becomes exothermic (negative) for Mo > ~25 at.% (xcrit).
# We model Ef_bcc(c) as a simple form that is +ve near c=0 and crosses 0 at the
# stated T=0 root, with a magnitude scale (meV/atom) typical of these systems.
# The ENTROPY term is exact; the energy surrogate only needs the right root and
# slope to test whether Eq.(3) drives the threshold down to the stated finite-T
# values (Nb 25 at.%, Mo 14 at.%).
# ---------------------------------------------------------------------------

def ef_bcc_surrogate(c, root0, emax):
    """
    Formation energy (eV/atom) of bcc phase vs solute fraction c in [0,1].
    Simple concave-down parabola-ish through 0 at c=root0.
    emax = peak positive Ef (eV/atom) near the dilute side. Ef(0)=0 (pure Ti bcc
    reference ~0 by construction of the surrogate baseline).
    """
    c = np.asarray(c, dtype=float)
    # quadratic with Ef(0)=0, root at root0, peak between: Ef = A c (c - root0)*(-1)
    # gives Ef>0 for 0<c<root0, Ef<0 for c>root0. Scale so max ~ emax.
    ef = -1.0 * c * (c - root0)
    # normalize peak (at c=root0/2) which equals root0^2/4
    peak = (root0 ** 2) / 4.0
    return emax * ef / peak


def threshold_root(c_grid, F):
    """First c where F crosses from + to - (sign change)."""
    s = np.sign(F)
    idx = np.where(np.diff(s) < 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    # linear interp
    c0, c1 = c_grid[i], c_grid[i + 1]
    f0, f1 = F[i], F[i + 1]
    return c0 - f0 * (c1 - c0) / (f1 - f0)


def analyze(system, root0_at, emax_eV, target_finiteT_at):
    c = np.linspace(0.001, 0.999, 4000)
    Ef0 = ef_bcc_surrogate(c, root0_at / 100.0, emax_eV)
    S = s_config(c)
    Ff = Ef0 - T_TRANS * S
    r0 = threshold_root(c, Ef0)
    rT = threshold_root(c, Ff)
    r0 = None if r0 is None else r0 * 100
    rT = None if rT is None else rT * 100
    print(f"\n=== {system} ===")
    print(f"  T=0 threshold (surrogate, forced to paper anchor): "
          f"{r0:.1f} at%  (paper text: {root0_at} at%)")
    print(f"  finite-T ({T_TRANS:.0f} K) threshold: "
          f"{rT:.1f} at%  (paper text: {target_finiteT_at} at%)")
    if rT is not None:
        print(f"  => threshold DROPPED by {r0 - rT:.1f} at% due to entropy. "
              f"Paper: drop {root0_at - target_finiteT_at} at%.")
    return r0, rT


def main():
    # sanity: entropy sign & magnitude
    print("Ideal-mixing entropy check (Eq.2, positive form):")
    for x in [0.1, 0.25, 0.5, 0.75, 0.9]:
        s = s_config_scalar(x)
        print(f"  x={x:.2f}  S={s*1e3:.4f} meV/K/atom  "
              f"= {s/kB:.4f} kB   (T*S at {T_TRANS:.0f}K = {T_TRANS*s*1e3:.2f} meV/atom)")
    # max entropy at x=0.5 must equal kB*ln2
    smax = s_config_scalar(0.5)
    print(f"  S(0.5)={smax/kB:.5f} kB ; kB*ln2 expected = {np.log(2):.5f} kB -> "
          f"{'OK' if abs(smax/kB-np.log(2))<1e-6 else 'FAIL'}")

    # Ti-Nb: T=0 root ~93 at% Nb ; finite-T ~25 at% Nb
    analyze("Ti-Nb", root0_at=93, emax_eV=0.10, target_finiteT_at=25)
    # Ti-Mo: T=0 root ~25 at% Mo ; finite-T ~14 at% Mo
    analyze("Ti-Mo", root0_at=25, emax_eV=0.05, target_finiteT_at=14)


if __name__ == "__main__":
    main()
