"""
roa_symmetry.py -- Claims A & B (Watanabe et al., arXiv:2507.09237)

Symmetry / Raman-tensor content of dual-circular ROA:
  Eq (4): chi^(1) = chi1 * diag(1, xi^2, xi),  chi^(2) = chi2 * diag(1, xi, xi^2), xi=exp(2pi i/3)
  Eq (2): I_{ei ef} = |ef^dag . alpha . ei|^2
  Circular vectors defined in the plane perpendicular to the incidence axis.

We test:
  (A) For incidence along [111], chi^(1) contributes to I_LR and chi^(2) to I_RL,
      giving U_CC^[111] = |chi1 Phi1|^2 - |chi2 Phi2|^2   (Eqs 5-7).
  (B) For incidence along [1-11] (= m_perp applied), U_CC flips sign: U_CC^[1-11] = -U_CC^[111] (Eq 8).
"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)
xi = np.exp(2j*np.pi/3)

def circ_vectors(nhat):
    """Right/Left circular polarization vectors in plane perpendicular to nhat.
    Build an orthonormal transverse basis (e1,e2) then e_{R/L}=(e1 +/- i e2)/sqrt2."""
    nhat = np.asarray(nhat, float); nhat = nhat/np.linalg.norm(nhat)
    # pick a reference not parallel to nhat
    ref = np.array([1.0,0,0]) if abs(nhat[0])<0.9 else np.array([0,1.0,0])
    e1 = ref - nhat*(ref@nhat); e1/=np.linalg.norm(e1)
    e2 = np.cross(nhat, e1); e2/=np.linalg.norm(e2)
    eR = (e1 + 1j*e2)/np.sqrt(2)
    eL = (e1 - 1j*e2)/np.sqrt(2)
    return eR, eL

def raman_tensors(chi1, chi2):
    a1 = chi1*np.diag([1, xi**2, xi])   # chi^(1)  (belongs Eg2)
    a2 = chi2*np.diag([1, xi,   xi**2]) # chi^(2)  (belongs Eg1)
    return a1, a2

def intensity(ef, a, ei):
    return abs(ef.conj() @ a @ ei)**2

def U_CC(nhat, chi1, chi2, Phi1=1.0, Phi2=1.0):
    """Cross-circular ROA U_CC = I_LR - I_RL, summed over the two Eg excitations.
    alpha = Phi * chi (Eq: alpha = Phi(dw) chi_Phi). Both modes present."""
    eR, eL = circ_vectors(nhat)
    a1, a2 = raman_tensors(chi1*Phi1, chi2*Phi2)
    # total Raman tensor for the LR channel gets contributions; but the paper's
    # selection rule is that each Eg mode routes one helicity channel. We evaluate
    # both tensors in each channel and report the channel intensities.
    # I_LR: incident L (ei=eL), scattered R (ef=eR): I = |eR^dag alpha eL|^2
    I_LR = intensity(eR, a1, eL) + intensity(eR, a2, eL)
    I_RL = intensity(eL, a1, eR) + intensity(eL, a2, eR)
    return I_LR - I_RL, I_LR, I_RL

if __name__ == "__main__":
    print("=== Claim A/B: facet-dependent cross-circular ROA ===")
    # Use unequal susceptibilities (generic axial octupolar case)
    chi1, chi2 = 1.0+0.3j, 0.6-0.2j
    for label, n in [("[111]", [1,1,1]), ("[1-11]", [-1,1,1]),
                     ("[11-1]", [1,1,-1]), ("[111]dup", [1,1,1])]:
        u, ilr, irl = U_CC(n, chi1, chi2)
        print(f" incidence {label:8s}: U_CC={u:+.4f}  I_LR={ilr:.4f}  I_RL={irl:.4f}")
    u111,_,_ = U_CC([1,1,1], chi1, chi2)
    um,_,_   = U_CC([-1,1,1], chi1, chi2)
    print(f"\n check Eq(1)/(8): U_CC[1-11] / U_CC[111] = {um/u111:+.4f} (expect -1)")
