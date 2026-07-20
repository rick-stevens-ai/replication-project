"""
claim2_nagaosa_qah.py
=====================
Replicates the paper's statement (Sec. III.A) that the 1x1 "Nagaosa solution"
chiral flux phase -- flux +phi through each triangle and -2phi through each
hexagon [Ohgushi-Murakami-Nagaosa, PRB 62 R6065 (2000), paper ref 44] --
BREAKS time-reversal symmetry and yields a QUANTUM ANOMALOUS HALL effect
(nonzero Chern number / anomalous Hall conductance).

Uses the SHARED KERNEL (code/kagome_loopcurrent_kernel.py, from
~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py):
  KagomeModel(flux, flux_pattern='uniform') builds exactly the uniform-directed
  Peierls-phase kagome model = Ohgushi-Murakami-Nagaosa flux state, with net
  flux 3*phi through each triangle. We report:
    - triangle flux and hexagon flux (should be phi and -2phi up to convention)
    - band gap between the two lower bands (0 for plain kagome, opens with flux)
    - Chern number of the lowest band (Fukui-Hatsugai-Suzuki) -> QAH marker
    - loop-current order parameter Im<c_A^dag c_B> (nonzero => TRS broken)

MACHINE-CHECKABLE CLAIMS
  C2a: plain kagome (flux=0) -> gapless (Dirac touch), current=0, Chern=0.
  C2b: Nagaosa flux (flux=pi/2 uniform) -> gap>0, current!=0, |Chern|=1 for a
       lower band => nonzero anomalous Hall (QAH), as stated in the paper.
"""
import numpy as np
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from kagome_loopcurrent_kernel import KagomeModel

def analyze(flux, pattern):
    m = KagomeModel(t=1.0, flux=flux, flux_pattern=pattern)
    fu, fd = m.plaquette_fluxes()
    gap = m.gap(nk=90)
    # Chern of each band
    cherns = [m.chern_number(band=b, nk=42) for b in range(3)]
    bc = m.bond_current_and_charge(nk=120, fillings=(1,))
    return dict(flux=flux, pattern=pattern,
                triangle_flux=float(fu), down_flux=float(fd),
                gap=float(gap), cherns=[int(c) for c in cherns],
                current_ab=float(bc["current_ab"]),
                charge_ab=float(bc["charge_ab"]))

if __name__ == "__main__":
    out = {}
    print("=== Plain kagome (flux=0, TRS preserved) ===")
    r0 = analyze(0.0, 'none')
    out["plain"] = r0
    print(json.dumps(r0, indent=2))

    print("\n=== Nagaosa chiral flux state (flux=pi/2, uniform directed) ===")
    r1 = analyze(np.pi/2, 'uniform')
    out["nagaosa"] = r1
    print(json.dumps(r1, indent=2))

    print("\n=== Intermediate flux sweep (gap opening + Chern) ===")
    sweep = []
    for f in [0.0, 0.1, 0.3, 0.5, np.pi/4, np.pi/2, 1.2]:
        r = analyze(f, 'uniform' if f > 0 else 'none')
        sweep.append(dict(flux=round(f,4), gap=round(r["gap"],5),
                          C0=r["cherns"][0], current=round(r["current_ab"],5)))
        print(f"  flux={f:.4f}  gap={r['gap']:.5f}  C_lower={r['cherns'][0]}  "
              f"Im<AB>={r['current_ab']:+.5f}")
    out["sweep"] = sweep

    # Verdicts
    verdict = {
        "plain_gapless": r0["gap"] < 1e-3,
        "plain_no_current": abs(r0["current_ab"]) < 1e-6,
        "plain_chern0": r0["cherns"][0] == 0,
        "nagaosa_gapped": r1["gap"] > 1e-2,
        "nagaosa_has_current": abs(r1["current_ab"]) > 1e-3,
        "nagaosa_QAH": abs(r1["cherns"][0]) >= 1,
    }
    out["verdict"] = verdict
    print("\n=== VERDICT ===")
    print(json.dumps(verdict, indent=2))
    with open(os.path.join(os.path.dirname(__file__), "..", "work",
              "claim2_output.json"), "w") as fh:
        json.dump(out, fh, indent=2)
