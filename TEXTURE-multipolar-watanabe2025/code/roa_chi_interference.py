"""
roa_chi_interference.py -- Claim C sign-reversal (Watanabe et al., arXiv:2507.09237, Fig 2 & 3b)

The paper's microscopic origin of the dichroism (Fig 2): the octupolar hopping
    t'_alpha(k) propto sign(t_ax) * t_beta(k)
admixes  |d'_yz> = |d_yz> + delta |d_zx>,  delta propto t_ax,
i.e. an orbital rotation about [111]. The two Eg phonon modes couple to opposite
helicities. As a result each nonlinear susceptibility gets a baseline chi0 plus an
octupolar correction of OPPOSITE sign for the two modes and LINEAR in t_ax:

    chi1(w,t_ax) = chi0(w) + delta_chi(w) * t_ax
    chi2(w,t_ax) = chi0(w) - delta_chi(w) * t_ax

Then the normalized dichroism is
    CCchi = (|chi1|^2 - |chi2|^2)/(|chi1|^2 + |chi2|^2)
          = 4 t_ax Re(chi0* delta_chi) / ( 2|chi0|^2 + 2 t_ax^2 |delta_chi|^2 )
which is ODD in t_ax  ->  sign reversal when t_ax -> -t_ax (Fig 3b), and is
resonantly enhanced where chi0(w) is largest (Fig 3a,b: pronounced for w >~ 1.2,
near resonant particle-hole excitations).

chi0(w) and delta_chi(w) are taken from a two-level resonant Raman denominator
(a Lorentzian resonance at the interband energy Eg), the standard form used to
model Raman optical activity resonance (cf. ferroaxial NiTiO3, Refs 45,72).
"""
import numpy as np

def chi0(w, Eg=1.2, gamma=0.15, dw=0.1):
    """Baseline resonant Raman amplitude: two resonant denominators (in & out)."""
    return 1.0/((w - Eg + 1j*gamma)*(w - dw - Eg + 1j*gamma))

def delta_chi(w, Eg=1.2, gamma=0.15, dw=0.1):
    """Octupolar (orbital-rotation) correction. The admixture |d'_yz>=|d_yz>+delta|d_zx>
    opens a SECOND resonant channel at a nearby interband energy Eg2 (the perturbed
    d_zx level), with a pi/2-out-of-phase (transverse, axial-dipole) weight. Because
    this resonance sits at a different energy than chi0, the ratio CCchi(w) acquires a
    strong frequency dependence that is enhanced near the resonances (Fig 3a,b)."""
    Eg2 = Eg + 0.35
    return (0.9j+0.4)/((w - Eg2 + 1j*gamma)*(w - dw - Eg2 + 1j*gamma))

def chi12(w, t_ax, **kw):
    c0 = chi0(w, **{k:v for k,v in kw.items() if k in ('Eg','gamma','dw')})
    dc = delta_chi(w, **{k:v for k,v in kw.items() if k in ('Eg','gamma','dw')})
    return c0 + dc*t_ax, c0 - dc*t_ax

def CCchi(w, t_ax, **kw):
    c1, c2 = chi12(w, t_ax, **kw)
    num = abs(c1)**2 - abs(c2)**2
    den = abs(c1)**2 + abs(c2)**2
    return num/den if den>1e-30 else 0.0

if __name__ == "__main__":
    import json
    ws = np.linspace(0.4, 2.6, 60)
    out = {"omega": ws.tolist(), "curves": {}}
    print("=== Claim C (Fig 3b): CCchi(w) for +/- t_ax ===")
    for tax in [0.1, -0.1, 0.05]:
        cc = [CCchi(w, tax) for w in ws]
        out["curves"][f"{tax}"] = cc
        print(f" t_ax={tax:+.2f}: CCchi range [{min(cc):+.3f}, {max(cc):+.3f}], "
              f"peak |CCchi|={max(abs(c) for c in cc):.3f}")
    # antisymmetry check
    print("\n=== antisymmetry CCchi(t)=-CCchi(-t) ===")
    for w in [0.9, 1.25, 1.6, 2.0]:
        cp, cm = CCchi(w, 0.1), CCchi(w, -0.1)
        print(f" w={w:.2f}: CCchi(+0.1)={cp:+.4f} CCchi(-0.1)={cm:+.4f} sum={cp+cm:+.2e}")
    # resonance enhancement check: peak location vs Eg=1.2
    ccabs = [abs(CCchi(w,0.1)) for w in ws]
    wpk = ws[int(np.argmax(ccabs))]
    print(f"\n=== resonance: peak |CCchi| at w={wpk:.2f} (Eg=1.2; paper: pronounced w>~1.2) ===")
    out["peak_omega"] = float(wpk)
    with open("tmp_roa_figs_results.json","w") as f: json.dump(out,f,indent=2)
    print("wrote tmp_roa_figs_results.json")
