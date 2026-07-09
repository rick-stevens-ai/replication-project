"""
Replication of the minimal kinetic model from
Tobias et al., "Spatiotemporal Dynamics of Early DNA Damage Response Proteins
on Complex DNA Lesions", PLOS ONE 8(2):e57953 (2013), CC-BY.

Source for equations and parameters: Supporting Information S1 of the paper
(downloaded from PLOS open-access endpoint, file s006 -> FileS1_MathematicalModel.doc).

Species (numbers, not concentrations):
   DSB   : Double-strand break ends available for inner-focus MRN binding
   MRN   : free MRN complex
   MRNi  : MRN bound to a DSB end                    (inner focus)
   ATM   : free, inactive ATM
   AMRNi : ATM bound to MRNi (transient complex during activation)
   ATMp  : activated ATM
   H2AX  : unmodified H2AX in the focus
   gH2AX : phosphorylated H2AX (gamma-H2AX) in the focus
   MDC1  : free MDC1
   MgH2AX  : MDC1 bound to gH2AX                     (outer focus)
   MMgH2AX : MRN bound to MDC1 in the outer focus
   AMgH2AX : ATMp bound to MgH2AX                    (outer focus)
   AMMgH2AX: ATMp + MRN bound to MgH2AX              (outer focus)

Reactions (9), with rate-constant assignment (FRAP-derived rates marked *):
   (1)  MRN + DSB  --k1f-->   MRNi         k1f = 1.01616e-07
        MRNi       --k1r-->   MRN + DSB    k1r = 0.007       *  (CK2-inhib koff)
   (2)  ATM + MRNi --k2-->    AMRNi        k2  = 3.75473e-06
   (3)  AMRNi      --k3-->    ATMp + MRNi  k3  = 0.989102
   (4)  H2AX + ATMp --k4-->   gH2AX + ATMp k4  = 0.000159441 (catalytic)
   (5)  MDC1 + gH2AX --k5f--> MgH2AX       k5f = 3.62805e-08
        MgH2AX      --k5r-->  MDC1 + gH2AX k5r = 0.00425     *  (FRAP MDC1 koff)
   (6)  MRN + MgH2AX  --k6f--> MMgH2AX     k6f = 6.64206e-07
        MMgH2AX      --k6r-->  MRN + MgH2AX k6r = 0.047      *  (X-ray NBS1 koff)
   (7)  MgH2AX + ATMp --k7--> AMgH2AX      k7  = 3.18033e-07
   (8)  MMgH2AX + ATMp --k7--> AMMgH2AX    (same k7 by symmetry)
   (9)  MRN + AMgH2AX --k6f--> AMMgH2AX    (same k6f as (6) by symmetry)
        AMMgH2AX     --k6r--> MRN + AMgH2AX (same k6r as (6) by symmetry)

Note on parameter mapping for k6f: The supplement lists one optimized value
(6.64206e-07) for an "and"-joined pair of reactions that, taken literally, are
asymmetric (a reverse of reaction 5 plus the forward of reaction 9). We
interpret this in parallel with the experimental "MMgH2AX -> MRN + MgH2AX and
AMMgH2AX -> MRN + AMgH2AX: 0.047" line, which clearly pairs the two reverse
reactions in the outer focus that share koff_MRN_o. By symmetry the optimized
value 6.64206e-07 is the *forward* on-rate that the same two reactions (6f and
9f) share. With this reading, k5r (reaction 5 reverse) is fully provided by the
FRAP value 0.00425 and there is no inconsistency. This interpretation also
yields the same number of unique rate constants (7 optimized + 3 FRAP) that the
supplement reports.

Initial conditions (numbers):
   ATM(0)  = 221859        MDC1(0) = 162208
   MRN(0)  = 129056        H2AX(0) = 3363
   All other species = 0.
   DSB(0)  = 2 * Nbreaks,  Nbreaks = 28 * (LET / 170 keV/um)
                          (linear with LET; 28 DSBs at LET=170 keV/um)

Numerical integration: stiff ODE solver (LSODA). The original paper used
Runge-Kutta Cash-Karp via the authors' `netdyn` python package; for our
purposes LSODA handles the broad timescale range (k3=0.99 1/s vs
k1f=1e-7 1/s) more robustly.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Published parameters (Supporting Information S1, Tobias et al. 2013)
# ---------------------------------------------------------------------------

# Optimized rate constants [1/s]
K1F = 1.01616e-07   # MRN + DSB -> MRNi
K2  = 3.75473e-06   # ATM + MRNi -> AMRNi
K3  = 0.989102      # AMRNi -> ATMp + MRNi
K4  = 0.000159441   # H2AX + ATMp -> gH2AX + ATMp (catalytic)
K5F = 3.62805e-08   # MDC1 + gH2AX -> MgH2AX
K6F = 6.64206e-07   # MRN + (M|AM)gH2AX -> MMgH2AX | AMMgH2AX
K7  = 3.18033e-07   # MgH2AX + ATMp -> AMgH2AX; MMgH2AX + ATMp -> AMMgH2AX

# FRAP-derived rate constants [1/s]
K1R = 0.007         # MRNi -> MRN + DSB  (NBS1 koff under CK2 inhibition)
K5R = 0.00425       # MgH2AX -> MDC1 + gH2AX  (MDC1 koff)
K6R = 0.047         # MMgH2AX/AMMgH2AX -> MRN + ...  (NBS1 koff at X-ray)

# Initial concentrations (numbers)
ATM_0   = 221859
MDC1_0  = 162208
MRN_0   = 129056
H2AX_0  = 3363    # H2AX molecules available in the focus

# DSB scaling: linear with LET, 28 DSBs at 170 keV/um
DSB_PER_LET = 28.0 / 170.0     # DSBs per keV/um per ion track

# Per-data-set scaling factors (numbers) -- Figure S1 panels A..L for NBS1,
# plus the single ATM data set.
SCALE_NBS1: Dict[str, float] = {
    "A": 2032, "B": 2149, "C": 2059, "D": 2667,
    "E": 2289, "F": 1963, "G": 2196, "H": 2164,
    "I": 2688, "J": 2850, "K": 3414, "L": 4030,
}
SCALE_ATM_HIGH_LET = 3263.0


# Species index map
SPECIES = [
    "MRN",   "DSB",   "MRNi",
    "ATM",   "AMRNi", "ATMp",
    "H2AX",  "gH2AX",
    "MDC1",  "MgH2AX", "MMgH2AX", "AMgH2AX", "AMMgH2AX",
]
IDX = {s: i for i, s in enumerate(SPECIES)}


def num_dsb_for_let(let_keV_um: float) -> float:
    """Number of DSB ends available for inner-focus binding.

    Each DSB has two ends; the supplement uses "DSBs" to mean the number of
    double-strand ends (DSEs), i.e. 2 * Nbreaks. We follow that convention.
    """
    nbreaks = DSB_PER_LET * let_keV_um
    return 2.0 * nbreaks


def initial_state(let_keV_um: float) -> np.ndarray:
    y0 = np.zeros(len(SPECIES))
    y0[IDX["MRN"]]   = MRN_0
    y0[IDX["DSB"]]   = num_dsb_for_let(let_keV_um)
    y0[IDX["ATM"]]   = ATM_0
    y0[IDX["H2AX"]]  = H2AX_0
    y0[IDX["MDC1"]]  = MDC1_0
    return y0


def rhs(t: float, y: np.ndarray) -> np.ndarray:
    """Right-hand side of the ODE system."""
    (MRN, DSB, MRNi,
     ATM, AMRNi, ATMp,
     H2AX, gH2AX,
     MDC1, MgH2AX, MMgH2AX, AMgH2AX, AMMgH2AX) = y

    # Reaction velocities
    v1f = K1F * MRN * DSB
    v1r = K1R * MRNi
    v2  = K2  * ATM * MRNi
    v3  = K3  * AMRNi
    v4  = K4  * H2AX * ATMp
    v5f = K5F * MDC1 * gH2AX
    v5r = K5R * MgH2AX
    v6f = K6F * MRN * MgH2AX
    v6r = K6R * MMgH2AX
    v7  = K7  * MgH2AX * ATMp        # MgH2AX + ATMp -> AMgH2AX
    v8  = K7  * MMgH2AX * ATMp       # MMgH2AX + ATMp -> AMMgH2AX
    v9f = K6F * MRN * AMgH2AX
    v9r = K6R * AMMgH2AX

    d = np.zeros_like(y)
    # MRN
    d[IDX["MRN"]]    = -v1f + v1r - v6f + v6r - v9f + v9r
    # DSB
    d[IDX["DSB"]]    = -v1f + v1r
    # MRNi (consumed by 2, regenerated by 3)
    d[IDX["MRNi"]]   = +v1f - v1r - v2 + v3
    # ATM
    d[IDX["ATM"]]    = -v2
    # AMRNi
    d[IDX["AMRNi"]]  = +v2 - v3
    # ATMp (released by 3, catalytic in 4, consumed in 7,8)
    d[IDX["ATMp"]]   = +v3 - v7 - v8
    # H2AX
    d[IDX["H2AX"]]   = -v4
    # gH2AX
    d[IDX["gH2AX"]]  = +v4 - v5f + v5r
    # MDC1
    d[IDX["MDC1"]]   = -v5f + v5r
    # MgH2AX
    d[IDX["MgH2AX"]] = +v5f - v5r - v6f + v6r - v7
    # MMgH2AX
    d[IDX["MMgH2AX"]] = +v6f - v6r - v8
    # AMgH2AX
    d[IDX["AMgH2AX"]] = +v7 - v9f + v9r
    # AMMgH2AX
    d[IDX["AMMgH2AX"]] = +v8 + v9f - v9r

    return d


@dataclass
class SimResult:
    let_keV_um: float
    t: np.ndarray              # seconds
    y: np.ndarray              # (nspecies, ntime)

    def get(self, name: str) -> np.ndarray:
        return self.y[IDX[name]]

    # Recruited-signal helpers ----------------------------------------------
    def nbs1_inner(self) -> np.ndarray:
        """NBS1 (=MRN) molecules bound in the inner focus."""
        return self.get("MRNi") + self.get("AMRNi")

    def nbs1_outer(self) -> np.ndarray:
        """NBS1 molecules bound in the outer focus (via MDC1)."""
        return self.get("MMgH2AX") + self.get("AMMgH2AX")

    def nbs1_total(self) -> np.ndarray:
        return self.nbs1_inner() + self.nbs1_outer()

    def atm_inner(self) -> np.ndarray:
        return self.get("AMRNi")

    def atm_outer(self) -> np.ndarray:
        return self.get("AMgH2AX") + self.get("AMMgH2AX")

    def atm_total(self) -> np.ndarray:
        return self.atm_inner() + self.atm_outer()

    def mdc1_total(self) -> np.ndarray:
        return (self.get("MgH2AX") + self.get("MMgH2AX")
                + self.get("AMgH2AX") + self.get("AMMgH2AX"))

    def atm_activated(self) -> np.ndarray:
        """All activated ATM (free + bound)."""
        return self.get("ATMp") + self.atm_outer() + self.atm_inner()


def simulate(let_keV_um: float,
             t_end: float = 700.0,
             n_out: int = 701) -> SimResult:
    """Integrate the model for the given LET."""
    y0 = initial_state(let_keV_um)
    t_eval = np.linspace(0.0, t_end, n_out)
    sol = solve_ivp(
        rhs, (0.0, t_end), y0,
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-8, atol=1e-3,
        max_step=1.0,
    )
    if not sol.success:
        raise RuntimeError(f"ODE integration failed at LET={let_keV_um}: {sol.message}")
    return SimResult(let_keV_um=let_keV_um, t=sol.t, y=sol.y)


# ---------------------------------------------------------------------------
# The twelve NBS1 data sets and the ATM data set:
# LET values are taken from the paper Figure 11 captions and Figure S1.
# We cover the full reported LET range from 170 to ~10290 keV/um.
# ---------------------------------------------------------------------------

# Figure 11 in the main text shows panels A (LET=170), B (3590), C (10290) for
# NBS1 and panel D (LET=14350) for ATM. The 12 NBS1 data sets in Figure S1
# correspond to the 12 LETs that the paper varies; the exact assignment of
# letters A..L to LETs is in the figure. We will work primarily with the three
# LETs whose curves are reproduced in the main text (Figure 11) plus the one
# ATM LET, since those are the curves the authors explicitly chose as
# representative.

REPRESENTATIVE_NBS1_LETS = [
    ("A", 170.0,   "low LET, C-ions"),
    ("B", 3590.0,  "intermediate, Ni-ions ~3500"),
    ("C", 10290.0, "high LET, Au-ions"),
]
ATM_LET = 14350.0  # U-ions, panel D in Figure 11
ATM_SCALE = SCALE_ATM_HIGH_LET


if __name__ == "__main__":
    # Quick smoke test
    for label, let, desc in REPRESENTATIVE_NBS1_LETS:
        r = simulate(let)
        print(f"[{label}] LET={let} ({desc})")
        print(f"   t=0:    NBS1_total={r.nbs1_total()[0]:.1f}   "
              f"inner={r.nbs1_inner()[0]:.1f}   outer={r.nbs1_outer()[0]:.1f}")
        print(f"   t=700s: NBS1_total={r.nbs1_total()[-1]:.1f}   "
              f"inner={r.nbs1_inner()[-1]:.1f}   outer={r.nbs1_outer()[-1]:.1f}")
        print(f"           ATM_active={r.atm_activated()[-1]:.1f} / {ATM_0}  "
              f"({100*r.atm_activated()[-1]/ATM_0:.1f}%)")
        print(f"           gH2AX={r.get('gH2AX')[-1]:.1f} / {H2AX_0}")
        print()

    r = simulate(ATM_LET)
    print(f"[ATM] LET={ATM_LET}  ATM activated fraction over time:")
    for tt in [60, 120, 180, 300, 600]:
        idx = int(tt)
        print(f"   t={tt:4d}s : {100*r.atm_activated()[idx]/ATM_0:5.1f}%   "
              f"ATM_total_recruited={r.atm_total()[idx]:.1f}")
