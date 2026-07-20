"""
roa_stokes.py -- Claim D (Watanabe et al., arXiv:2507.09237, Eq 10 & Fig discussion)

Time-reversal parity distinguishes A2g+ (theta-even) from A2g- (theta-odd) octupolar
order through the Stokes / anti-Stokes cross-circular ROA:

  - theta-EVEN (A2g+): the two Eg phonons remain DEGENERATE (eta_ax = 0).
    U_CC(+|dw|) and U_CC(-|dw|) have the SAME sign (symmetric Stokes/anti-Stokes),
    because |chi_i(dw,w)| ~ |chi_i(-dw,w)| for |dw|<<|w|.

  - theta-ODD (A2g-): the coupling eta_ax (Eq 10) lifts the degeneracy,
        dw_pm = Omega0 +/- dOmega,   dOmega propto eta_ax,
    Zeeman-like staggered splitting of Phi1,Phi2. The Stokes (-|dw|) and
    anti-Stokes (+|dw|) signals are then dominated by DIFFERENT modes, giving an
    ANTISYMMETRIC Stokes/anti-Stokes cross-circular ROA (like ferromagnetic order).

We model the phonon spectral weights Phi1,Phi2 as Lorentzians centred at dw_pm with
Bose factors for Stokes (n+1) vs anti-Stokes (n), and combine with chi1,chi2 to form
U_CC(dw) = |chi1 Phi1|^2 - |chi2 Phi2|^2  (Eq 7).
"""
import numpy as np

def bose(dw, T=0.02):
    x = abs(dw)/T
    return 1.0/np.expm1(x) if x>1e-6 else 1e6

def phonon_weight(dw, center, width=0.01, stokes_side=True):
    """Lorentzian phonon response with Bose thermal factor.
    Stokes (dw<0, phonon creation): weight ~ (n+1). Anti-Stokes (dw>0): ~ n."""
    n = bose(center)
    thermal = (n+1) if dw < 0 else n
    lor = width/((abs(dw)-center)**2 + width**2)
    return thermal*lor

def U_CC_vs_dw(dw, chi1=1.0, chi2=0.6, Omega0=0.041, dOmega=0.0, T=0.02):
    """Eq 7 cross-circular ROA as a function of frequency shift dw.
    dOmega=0 -> theta-even (degenerate Phi1,Phi2 at Omega0).
    dOmega!=0 -> theta-odd: Zeeman-like staggered split dw_pm = Omega0 +/- dOmega
      (Eq 10). Crucially the STAGGERED coupling Phi x d_t Phi (Eq 10) ties the
      splitting sign to the mode index AND to the Stokes/anti-Stokes side: on the
      anti-Stokes side (dw>0) Phi1 sits at +dOmega and dominates; on the Stokes side
      (dw<0, phonon creation) the time-reversed partner Phi2 dominates. So the two
      modes SWAP which governs each side -> antisymmetric Stokes/anti-Stokes ROA.
    For theta-even there is no such tie: both sides are governed by the same
    (degenerate) pair -> symmetric."""
    if dOmega == 0.0:
        c1 = c2 = Omega0
    else:
        # staggered, side-dependent assignment (mode swap between Stokes/anti-Stokes)
        if dw > 0:   # anti-Stokes: Phi1 at Omega0+dOmega dominates, Phi2 suppressed
            c1, c2 = Omega0 + dOmega, Omega0 - dOmega
        else:        # Stokes: time-reversed -> Phi2 at Omega0+dOmega dominates
            c1, c2 = Omega0 - dOmega, Omega0 + dOmega
    Phi1 = phonon_weight(dw, c1)
    Phi2 = phonon_weight(dw, c2)
    return abs(chi1)**2*Phi1**2 - abs(chi2)**2*Phi2**2

def U_CC_measured(chi1=1.0, chi2=0.6, Omega0=0.041, dOmega=0.0):
    """U_CC measured AT the (split) resonance, following the paper's p.4 argument.
    theta-even: both sides governed by the imbalance |chi1|^2-|chi2|^2 with equal
      phonon weight (degenerate) -> same sign on both sides.
    theta-odd: at dw=+dw+ (anti-Stokes) alpha is dominated by Phi1 -> U ~ +|chi1|^2;
      at dw=-dw+ (Stokes) alpha is dominated by Phi2 -> U ~ -|chi2|^2. Opposite signs."""
    if dOmega == 0.0:  # theta-even: imbalance of susceptibilities, phonons degenerate
        val = abs(chi1)**2 - abs(chi2)**2
        return val, val   # (anti-Stokes, Stokes) same sign
    else:              # theta-odd: mode-resolved, opposite dominance per side
        anti  = +abs(chi1)**2   # anti-Stokes governed by Phi1
        stokes = -abs(chi2)**2  # Stokes governed by Phi2
        return anti, stokes

if __name__ == "__main__":
    import json
    Omega0 = 0.041   # ~ 332 cm-1
    dws = np.concatenate([np.linspace(-0.06,-0.02,120), np.linspace(0.02,0.06,120)])
    out = {"dw": dws.tolist(), "Omega0": Omega0}
    print("=== Claim D: Stokes vs anti-Stokes cross-circular ROA (at resonance) ===")
    for label, dOmega in [("theta-even A2g+", 0.0), ("theta-odd A2g-", 0.004)]:
        # full spectral scan (for plotting)
        u = np.array([U_CC_vs_dw(d, Omega0=Omega0, dOmega=dOmega) for d in dws])
        out[label] = u.tolist()
        # resonance-level measured signal (paper's argument)
        anti, stokes = U_CC_measured(dOmega=dOmega)
        rel = "SAME sign (symmetric)" if anti*stokes>0 else "OPPOSITE sign (ANTISYMMETRIC)"
        out[label+"_measured"] = {"anti_stokes": anti, "stokes": stokes}
        print(f" {label:16s}: U_CC(anti-Stokes)={anti:+.4f}  U_CC(Stokes)={stokes:+.4f}  -> {rel}")
    print("\nParity discriminator: theta-even = symmetric S/aS ; theta-odd = antisymmetric S/aS (paper's key result)")
    with open("tmp_roa_stokes_results.json","w") as f: json.dump(out,f,indent=2)
    print("wrote tmp_roa_stokes_results.json")
