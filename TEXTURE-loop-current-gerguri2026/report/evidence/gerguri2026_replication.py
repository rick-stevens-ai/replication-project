#!/usr/bin/env python3
"""
Replication surrogate for Gerguri et al. (2026), arXiv:2603.27408
"Correlated charge order ... in the dual flat band kagome superconductor CeRu3Si2".

HEADLINE CLAIM (recipe): DFT+U reproduces the experimentally DOMINANT q=1/2 (Pmma)
charge order in CeRu3Si2 only for Ce-4f Hubbard U > 6 eV; the weaker q=1/3 (Imma)
order stays nearly degenerate near the crossover; treating Ce-4f as CORE fails to
stabilize q=1/2 as the ground state (q=1/3 suppressed, a q=1/4 "CO*" appears).

We do NOT run DFT+U (scoped out). We build a from-scratch tight-binding + Hartree
mean-field SURROGATE: a kagome layer of Ru (3 sites/cell) hybridized with one heavy
Ce-4f flat level per cell. We compute the mean-field CHARGE-ORDER SUSCEPTIBILITY
(Landau quadratic coefficient) at commensurate wavevectors q = 1/2, 1/3, 1/4 as a
function of the Hubbard U that controls the Ce-4f flat-band position (4f^0, above
E_F; larger U pushes it further up). The order that condenses is the q with the
largest susceptibility chi_q (most negative Landau curvature of the band energy).

Mechanism modelled: the Ru kagome M-point van Hove nesting drives q=1/2. When the
Ce-4f flat band sits near E_F (small U) it donates spectral weight at E_F, detuning
the Ru bands from the van Hove filling and letting q=1/3 win. Raising U lifts the f
band away, restoring the Ru van Hove condition -> q=1/2 overtakes q=1/3.

Kernel credit:
  - loop_current_kagome_kernel.py : kagome geometry, primitive vectors A1,A2, the
    half-bond Bloch/real-space NN convention, occupied-band bookkeeping.
  - loop_current_meanfield_kernel.py : occupied_density / sum-of-occupied-energies
    pattern used for the total electronic energy.
This is a SURROGATE (single kagome+f layer), qualitative not first-principles.
"""
from __future__ import annotations
import json, time
import numpy as np

t0 = time.time()
SQ3 = np.sqrt(3.0)
A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, SQ3 / 2.0])
BASIS = np.array([0.5 * A1, 0.5 * A2, 0.5 * (A1 + A2)])  # kagome sublattice offsets


def build_supercell(nx, ny, with_f=True):
    """Kagome supercell (nx x ny cells). 3 Ru + optional 1 Ce-f per cell. Periodic."""
    pos, sub, cellx = [], [], []
    ncell_orb = 4 if with_f else 3
    for y in range(ny):
        for x in range(nx):
            R = x * A1 + y * A2
            for s in range(3):
                pos.append(R + BASIS[s]); sub.append(s); cellx.append(x)
            if with_f:
                pos.append(R.copy()); sub.append(3); cellx.append(x)
    pos = np.array(pos); sub = np.array(sub); cellx = np.array(cellx)
    N = len(sub)
    ru = np.where(sub < 3)[0]
    L1 = nx * A1; L2 = ny * A2
    bonds = []
    for a in range(len(ru)):
        for b in range(a + 1, len(ru)):
            i, j = ru[a], ru[b]
            d0 = pos[i] - pos[j]; best = 1e9
            for m in (-1, 0, 1):
                for n in (-1, 0, 1):
                    best = min(best, np.hypot(*(d0 + m * L1 + n * L2)))
            if best < 0.55:
                bonds.append((i, j))
    fbonds = []
    if with_f:
        for y in range(ny):
            for x in range(nx):
                fi = (y * nx + x) * 4 + 3
                for s in range(3):
                    fbonds.append((fi, (y * nx + x) * 4 + s))
    return pos, sub, cellx, bonds, fbonds


def build_H(pos, sub, cellx, bonds, fbonds, t, tf, eps_f, delta, qfrac):
    N = len(sub); H = np.zeros((N, N), complex)
    for (i, j) in bonds:
        H[i, j] += -t; H[j, i] += -t
    for (fi, ri) in fbonds:
        H[fi, ri] += -tf; H[ri, fi] += -tf
    for i in range(N):
        if sub[i] == 3:
            H[i, i] += eps_f
    if delta != 0.0:
        for i in range(N):
            if sub[i] < 3:
                H[i, i] += delta * np.cos(2 * np.pi * qfrac * cellx[i])
    return H


def band_energy(H, filling):
    ev = np.linalg.eigvalsh(H)
    nocc = int(round(filling * len(ev)))
    return float(np.sum(ev[:nocc])) / len(ev)


def chi_cdw(nx, eps_f, filling, t=1.0, tf=0.30, with_f=True, ny=4, d=0.03):
    """Mean-field CDW susceptibility at q=1/nx = Landau curvature:
       chi_q = -(E(+d)+E(-d)-2E(0))/d^2   (positive => ordering tendency)."""
    pos, sub, cellx, bonds, fbonds = build_supercell(nx, ny, with_f)
    E0 = band_energy(build_H(pos, sub, cellx, bonds, fbonds, t, tf, eps_f, 0.0, 1.0 / nx), filling)
    Ep = band_energy(build_H(pos, sub, cellx, bonds, fbonds, t, tf, eps_f, +d, 1.0 / nx), filling)
    Em = band_energy(build_H(pos, sub, cellx, bonds, fbonds, t, tf, eps_f, -d, 1.0 / nx), filling)
    return -(Ep + Em - 2 * E0) / d ** 2


# --- Model parameters (surrogate; f flat band above E_F -> 4f^0) ------------
t = 1.0
tf = 0.30            # Ru-f hybridization
eps_f0 = 0.15        # f level at U=0: sits close to E_F -> competes, detunes Ru
kU = 0.10            # f level rises with U (eV) : eps_f = eps_f0 + kU*U
filling = 0.62       # near Ru kagome M-point van Hove (q=1/2 nesting) incl. f orbital
qmap = {"q=1/2": 2, "q=1/3": 3, "q=1/4": 4}
U_values = [0, 2, 4, 5, 6, 7, 8, 9]

results = {"U_sweep": [], "core_control": {}, "meta": {}}
crossover_U = None
for U in U_values:
    eps_f = eps_f0 + kU * U
    chis = {name: chi_cdw(nx, eps_f, filling, t, tf, with_f=True) for name, nx in qmap.items()}
    winner = max(chis, key=chis.get)
    row = {"U_eV": U, "eps_f_over_t": round(eps_f, 4),
           "chi": {k: round(v, 5) for k, v in chis.items()},
           "ground_state": winner,
           "chi(1/2)-chi(1/3)": round(chis["q=1/2"] - chis["q=1/3"], 5)}
    results["U_sweep"].append(row)
    if winner == "q=1/2" and crossover_U is None:
        crossover_U = U

# --- Control: Ce-4f as CORE (no f valence states) --------------------------
chis_core = {name: chi_cdw(nx, 0.0, filling, t, tf, with_f=False) for name, nx in qmap.items()}
core_winner = max(chis_core, key=chis_core.get)
results["core_control"] = {
    "treatment": "Ce-4f as CORE (f orbitals removed from valence)",
    "chi": {k: round(v, 5) for k, v in chis_core.items()},
    "ground_state": core_winner,
    "note": "paper: f-as-core suppresses q=1/3 and fails to make q=1/2 the ground state; a q=1/4 CO* appears",
}

results["meta"] = {
    "paper": "Gerguri et al. 2026, arXiv:2603.27408, CeRu3Si2",
    "headline_claim": ("DFT+U reproduces experimentally dominant q=1/2 (Pmma) charge order only "
                       "for Ce-4f U>6 eV; q=1/3 (Imma) nearly degenerate near crossover; f-as-core "
                       "fails to stabilize q=1/2."),
    "method": "tight-binding + Hartree mean-field kagome+Ce4f SURROGATE (NOT DFT+U); "
              "order selection via CDW Landau susceptibility chi_q",
    "kernels_credited": ["loop_current_kagome_kernel.py (kagome geometry / TB conventions)",
                         "loop_current_meanfield_kernel.py (occupied-energy / density pattern)"],
    "model": {"t": t, "tf_Ru_f_hyb": tf, "eps_f0_over_t": eps_f0, "kU_per_eV": kU,
              "filling": filling, "U_to_eps_f": "eps_f = eps_f0 + kU*U"},
    "wavevectors": {"q=1/2": "Pmma CO (dominant, expt)",
                    "q=1/3": "Imma CO-II (weaker, expt)",
                    "q=1/4": "CO* (f-as-core DFT artifact)"},
    "crossover_U_eV_surrogate": crossover_U,
    "paper_crossover_U_eV": 6,
    "surrogate_disclaimer": "Parameters chosen to expose the QUALITATIVE mechanism; not "
                            "first-principles total energies. DFT+U scoped out of this run.",
}
results["meta"]["runtime_s"] = round(time.time() - t0, 2)

out = "/home/stevens/textures-100/corpus/textures-loop-current-gerguri2026/work/gerguri2026_result.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("SAVED", out)
for r in results["U_sweep"]:
    print(r["U_eV"], r["eps_f_over_t"], r["chi"], "->", r["ground_state"])
print("CORE:", results["core_control"]["chi"], "->", results["core_control"]["ground_state"])
print("crossover_U(surrogate)=", crossover_U, " runtime=", results["meta"]["runtime_s"])
