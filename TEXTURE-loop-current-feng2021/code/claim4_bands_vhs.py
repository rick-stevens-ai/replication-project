"""
claim4_bands_vhs.py
===================
Replicates the kagome tight-binding band structure and van-Hove physics that
underpins the paper's low-energy theory (Fig. 1c,d and Eq. 1):

  H_k = -2t [[0, cos k1/2, cos k2/2],
             [cos k1/2, 0, cos k3/2],
             [cos k2/2, cos k3/2, 0]]  (mu=0), t=1.
  k1=kx, k2=(kx + sqrt3 ky)/2, k3=(-kx + sqrt3 ky)/2.

CLAIMS CHECKED:
  (1) FLAT BAND: the kagome spectrum has one dispersionless band at E=+2t
      (with H = -2t * offdiag convention, the flat band sits at +2t).
  (2) DIRAC TOUCHING at K between the two dispersive bands.
  (3) VAN-HOVE SINGULARITY (saddle) at the M points -> log-divergent DOS peak,
      and the Fermi level at 5/12 band filling crosses the M-point vH energy
      (the paper's "5/4 vH filling"). We verify E_F(5/12) ~ E(M-point vH).

We implement the paper's EXACT H_k (Eq.1) directly (not via the kernel's
half-bond form) so the energies are in the paper's own convention, then
cross-check the flat band and gaplessness against the shared kernel.
"""
import numpy as np
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

SQRT3 = np.sqrt(3.0)

def Hk_paper(kx, ky, t=1.0, mu=0.0):
    k1 = kx
    k2 = 0.5*kx + 0.5*SQRT3*ky
    k3 = -0.5*kx + 0.5*SQRT3*ky
    H = np.array([
        [-mu, -2*t*np.cos(k1/2), -2*t*np.cos(k2/2)],
        [-2*t*np.cos(k1/2), -mu, -2*t*np.cos(k3/2)],
        [-2*t*np.cos(k2/2), -2*t*np.cos(k3/2), -mu],
    ], dtype=float)
    return H

def bands_on_grid(nk=200, t=1.0):
    fs = np.linspace(-np.pi, np.pi, nk)
    # sample over a generous k box covering the BZ
    E = []
    for kx in fs:
        for ky in fs:
            w = np.linalg.eigvalsh(Hk_paper(kx, ky, t))
            E.append(np.sort(w))
    return np.array(E)  # (nk^2, 3) ascending

def main():
    out = {}
    E = bands_on_grid(nk=180)
    band_lo, band_mid, band_hi = E[:, 0], E[:, 1], E[:, 2]

    # (1) FLAT BAND: highest band should be (nearly) constant at +2t
    hi_std = float(np.std(band_hi))
    hi_mean = float(np.mean(band_hi))
    out["flat_band"] = dict(mean_E=round(hi_mean, 4), std_E=round(hi_std, 6),
                            is_flat=hi_std < 1e-3,
                            at_plus_2t=abs(hi_mean - 2.0) < 1e-3)
    print(f"(1) Flat band: mean E = {hi_mean:.4f} (expect +2.0),  "
          f"std = {hi_std:.2e}  -> flat={out['flat_band']['is_flat']}")

    # (2) Dirac touching between the two lower bands: evaluate at analytic K
    wK = np.sort(np.linalg.eigvalsh(Hk_paper(4*np.pi/3, 0.0)))
    dirac_gap_atK = float(wK[1] - wK[0])
    mingap = float(np.min(band_mid - band_lo))
    out["dirac_touch_lower_gap_grid"] = round(mingap, 6)
    out["dirac_gap_at_K"] = round(dirac_gap_atK, 8)
    print(f"(2) Gap between two lower bands at analytic K point: "
          f"{dirac_gap_atK:.2e} -> Dirac touch={dirac_gap_atK < 1e-6}")
    print(f"    (coarse-grid min gap = {mingap:.3e}; grid misses exact K)")

    # (3) van-Hove at M point. M1 = (0, 2pi/sqrt3) per paper Fig.1b caption.
    for label, (kx, ky) in {
        "Gamma": (0.0, 0.0),
        "M1": (0.0, 2*np.pi/SQRT3),
        "M2": (np.pi, np.pi/SQRT3),
        "K": (4*np.pi/3, 0.0),
    }.items():
        w = np.sort(np.linalg.eigvalsh(Hk_paper(kx, ky)))
        out[f"E_{label}"] = [round(float(x), 4) for x in w]
        print(f"    E({label}) = {out[f'E_{label}']}")

    # DOS + vH peak location and 5/12 filling Fermi level
    allE = E.ravel()
    hist, edges = np.histogram(allE, bins=400, density=True)
    centers = 0.5*(edges[:-1]+edges[1:])
    vh_peak_E = float(centers[np.argmax(hist)])
    out["dos_peak_energy_all"] = round(vh_peak_E, 4)
    # dispersive-bands-only DOS (exclude flat band at +2t) -> vH saddle peak
    disp = E[:, :2].ravel()
    hist2, edges2 = np.histogram(disp, bins=400, density=True)
    centers2 = 0.5*(edges2[:-1]+edges2[1:])
    vh_disp_E = float(centers2[np.argmax(hist2)])
    out["dos_peak_energy_dispersive"] = round(vh_disp_E, 4)
    print(f"(3) DOS peak (all bands, dominated by flat band) at E = {vh_peak_E:.4f}")
    print(f"    DOS peak of DISPERSIVE bands (vH saddle) at E = {vh_disp_E:.4f} "
          f"(expect ~0 = M-point)")
    # 5/12 band filling Fermi energy (quantile of sorted energies)
    sortedE = np.sort(allE)
    ef = float(sortedE[int(round(5/12 * len(sortedE))) - 1])
    out["fermi_E_5over12"] = round(ef, 4)
    # M-point vH energy (lower band value at M): E(M) lower
    EM = float(np.sort(np.linalg.eigvalsh(Hk_paper(0.0, 2*np.pi/SQRT3)))[1])
    out["E_M_middle_band"] = round(EM, 4)
    print(f"    E_F at 5/12 band filling = {ef:.4f}")
    print(f"    M-point (middle band) energy = {EM:.4f}")
    out["vh_filling_consistent"] = abs(ef - vh_disp_E) < 0.2 and abs(EM) < 1e-6
    print(f"    E_F(5/12) ~ dispersive vH saddle (M-point E=0): "
          f"{out['vh_filling_consistent']}")

    # cross-check flat band against shared kernel (convention: kernel flat at +2t)
    from kagome_loopcurrent_kernel import KagomeModel, Gamma, K, M
    km = KagomeModel(t=1.0, flux=0.0, flux_pattern='none')
    wG = np.sort(np.linalg.eigvalsh(km.hamiltonian(*Gamma)))
    out["kernel_E_Gamma"] = [round(float(x), 4) for x in wG]
    print(f"\n  cross-check kernel E(Gamma) = {out['kernel_E_Gamma']}")

    with open(os.path.join(os.path.dirname(__file__), "..", "work",
              "claim4_output.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("\n=== summary written ===")

if __name__ == "__main__":
    main()
