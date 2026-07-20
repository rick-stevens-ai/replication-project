"""
claim2c_chern_phase_diagram.py
==============================
Maps the Chern number of the LOWEST band of the uniform-flux (Nagaosa) kagome
model versus the Peierls flux phi, to demonstrate the paper's central QAH
claim: the chiral flux phase carries a nonzero (quantized) anomalous Hall
conductance over a robust range of flux.

Physics note (honest): the Ohgushi-Murakami-Nagaosa kagome flux model does NOT
carry a nonzero Chern for ALL phi. At phi=0 and phi=pi/2 (and pi) the model
sits at TR-symmetric / band-touching special points where the lowest band gap
either closes or the net Chern is 0. For generic 0<phi<pi/2 the lowest band is
GAPPED and carries C=+/-1 -> QAH. We locate this window numerically.

Uses the shared kernel's non-abelian FHS (via occ_chern here) and per-band gap.
"""
import numpy as np
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from kagome_loopcurrent_kernel import KagomeModel, B1, B2

def lowest_band_chern_and_gap(model, nk=48):
    f = np.linspace(0.0, 1.0, nk, endpoint=False)
    U = np.empty((nk, nk, 3), dtype=complex)
    Ev = np.empty((nk, nk, 3))
    for i, u in enumerate(f):
        for j, v in enumerate(f):
            k = u*B1 + v*B2
            w, V = np.linalg.eigh(model.hamiltonian(k[0], k[1]))
            Ev[i, j] = w.real
            U[i, j] = V[:, 0]
    def link(a, b):
        z = np.vdot(a, b)
        return z/abs(z) if abs(z) > 1e-12 else 1.0+0j
    F = 0.0
    for i in range(nk):
        for j in range(nk):
            Ux = link(U[i, j], U[(i+1)%nk, j])
            Uy = link(U[(i+1)%nk, j], U[(i+1)%nk, (j+1)%nk])
            Uxp = link(U[i, (j+1)%nk], U[(i+1)%nk, (j+1)%nk])
            Uyp = link(U[i, j], U[i, (j+1)%nk])
            F += np.angle(Ux*Uy/(Uxp*Uyp))
    C = int(np.round(F/(2*np.pi)))
    gap = float(np.min(Ev[:, :, 1] - Ev[:, :, 0]))
    return C, gap

if __name__ == "__main__":
    fluxes = np.linspace(0.02, np.pi-0.02, 25)
    table = []
    qah_window = []
    for phi in fluxes:
        m = KagomeModel(t=1.0, flux=phi, flux_pattern='uniform')
        C, gap = lowest_band_chern_and_gap(m, nk=48)
        table.append(dict(phi=round(float(phi), 4), C=C, gap=round(gap, 5)))
        gapped = gap > 0.05
        nonzero = C != 0
        print(f"  phi={phi:5.3f}  C_lowest={C:+d}  gap={gap:.5f}  "
              f"{'<-- QAH' if (gapped and nonzero) else ''}")
        if gapped and nonzero:
            qah_window.append(round(float(phi), 4))

    out = {"table": table, "qah_flux_values": qah_window,
           "qah_exists": len(qah_window) > 0,
           "max_C_observed": max(abs(t["C"]) for t in table)}
    print("\n=== VERDICT ===")
    print(f"  QAH (gapped lowest band with C!=0) found at flux values: {qah_window}")
    print(f"  QAH phase exists: {out['qah_exists']}   max|C|={out['max_C_observed']}")
    with open(os.path.join(os.path.dirname(__file__), "..", "work",
              "claim2c_output.json"), "w") as fh:
        json.dump(out, fh, indent=2)
