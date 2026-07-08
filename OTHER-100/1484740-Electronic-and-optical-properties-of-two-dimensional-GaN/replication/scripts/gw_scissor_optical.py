"""GW-scissor + analytic 2D Wannier-Mott exciton + IPA optical analysis for 2D GaN.

Reads mono_bands.dat (PBE band-structure path) from the existing replication and:
  - finds DFT VBM/CBM and gap
  - computes JDOS-based ε₂(ω) under independent-particle approximation
  - applies paper's reported scissor shift (Δgw = 3.37 eV monolayer)
  - uses 2D Mott-Wannier (Olsen-Thygesen / Cudazzo) to estimate exciton
    binding from in-plane reduced mass and dielectric
  - predicts optical gap = E_g(GW) - E_b
  - compares to paper's reported BSE optical gap (5.01 eV)
"""
import numpy as np, sys, os, json

bands_path = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/1484740-Electronic-and-optical-properties-of-two-dimensional-GaN/replication/outputs/mono_bands.dat")

def parse_bands(path):
    with open(path) as f:
        head = f.readline()
    # header like ' &plot nbnd=  30, nks=   121 /'
    nbnd = int(head.split("nbnd=")[1].split(",")[0])
    nks  = int(head.split("nks=")[1].split("/")[0])
    eigs = np.zeros((nks, nbnd))
    with open(path) as f:
        f.readline()
        for ik in range(nks):
            kline = f.readline().split()
            # eigenvalues across multiple lines
            vals = []
            while len(vals) < nbnd:
                line = f.readline()
                vals += [float(x) for x in line.split()]
            eigs[ik] = vals[:nbnd]
    return eigs  # (nks, nbnd) eV

def find_gap(eigs, nelec=20):
    nocc = nelec // 2
    vbm = eigs[:, nocc-1].max()
    cbm = eigs[:, nocc].min()
    return vbm, cbm, cbm-vbm

def jdos_ipa(eigs, nocc, wmin=0, wmax=12, nw=600, sigma=0.10):
    om = np.linspace(wmin, wmax, nw)
    e2 = np.zeros_like(om)
    for ik in range(eigs.shape[0]):
        eo = eigs[ik, :nocc]
        eu = eigs[ik, nocc:]
        de = (eu[None,:] - eo[:,None]).flatten()
        de = de[(de>0)&(de<wmax+1)]
        for d in de:
            # gaussian; weight ~1/d^2 for absorption proxy
            e2 += np.exp(-((om-d)/sigma)**2) / (sigma*np.sqrt(np.pi))
    e2 /= eigs.shape[0]
    return om, e2

def wannier_mott_2d(mu_red=0.42, eps_eff=4.5):
    """Olsen et al. 2D screened-Wannier-Mott analytic E_b.
    For thin 2D system, E_b = (8/3) * E_b^3D; here we use simple Rydberg-like
    expression as an order-of-magnitude estimate.
    Args:
      mu_red: reduced effective mass in units of m_e
      eps_eff: effective in-plane dielectric (paper reports ε_∥ ≈ 4 for 2D GaN)
    Returns binding energy in eV.
    """
    Ry_3D = 13.6057  # eV
    Eb3D = Ry_3D * mu_red / eps_eff**2
    Eb2D = 4.0 * Eb3D  # 2D Rydberg series ground state: factor 4 vs 3D
    return Eb2D, Eb3D

def main():
    eigs = parse_bands(bands_path)
    print(f"[bands] nks={eigs.shape[0]} nbnd={eigs.shape[1]}")
    vbm, cbm, gap = find_gap(eigs, nelec=20)
    print(f"[DFT] VBM={vbm:.3f} CBM={cbm:.3f} gap={gap:.3f} eV")

    # paper values (Bayerl 2017)
    paper = {
        "dft_gap_LDA": 2.95,
        "GW_correction": 3.37,
        "GW_gap": 6.32,
        "BSE_binding": 1.31,
        "optical_gap": 5.01,
        "in_plane_eps": 4.0,
        "mu_red": 0.42,
    }

    # Apply paper's GW scissor to our PBE
    gw_gap_us = gap + paper["GW_correction"]
    print(f"[GW scissor] gap_GW = {gap:.3f} + {paper['GW_correction']} = {gw_gap_us:.3f} eV  (paper {paper['GW_gap']})")

    # Analytic exciton binding using paper's reduced mass and dielectric
    Eb2D, Eb3D = wannier_mott_2d(paper["mu_red"], paper["in_plane_eps"])
    print(f"[Wannier-Mott 2D] Eb3D={Eb3D:.3f} eV  Eb2D~{Eb2D:.3f} eV  (paper BSE {paper['BSE_binding']} eV)")

    # Predicted optical gap
    opt_us = gw_gap_us - Eb2D
    print(f"[optical] predicted optical gap = GW - Eb = {opt_us:.3f} eV  (paper {paper['optical_gap']})")

    # Use paper's reported binding instead
    opt_us_paperEb = gw_gap_us - paper["BSE_binding"]
    print(f"[optical, scissor + paper Eb] = {opt_us_paperEb:.3f} eV  (paper {paper['optical_gap']})")

    # Compute IPA absorption
    om, e2 = jdos_ipa(eigs, nocc=10)
    # Apply scissor shift to the spectrum: shift in energy by GW correction
    om_gw = om + paper["GW_correction"]

    # Save
    out = {
        "dft_gap_eV": gap,
        "vbm_eV": vbm,
        "cbm_eV": cbm,
        "gw_gap_us_eV": float(gw_gap_us),
        "wannier_mott_Eb_eV": float(Eb2D),
        "predicted_optical_gap_eV": float(opt_us),
        "predicted_optical_gap_paperEb_eV": float(opt_us_paperEb),
        "paper": paper,
        "abs_ratio_predicted_vs_paper": float(opt_us_paperEb / paper["optical_gap"])
    }
    print("\n=== summary ===")
    print(json.dumps(out, indent=2))
    np.savetxt("/tmp/gan_eps2_ipa.dat", np.c_[om, e2, om_gw, e2], header="omega_PBE eps2 omega_GWshift eps2")
    json.dump(out, open("/tmp/gan_optical.json","w"), indent=2)
    print(f"\nsaved: /tmp/gan_eps2_ipa.dat /tmp/gan_optical.json")

if __name__ == "__main__":
    main()
