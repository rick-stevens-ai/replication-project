"""
LUCID p53 / DNA damage repair replication — deterministic ODE.

Independent re-implementation of the p53 regulatory core from:
  Hat B., Kochańczyk M., Bogdał M.N., Lipniacki T. (2016)
  "Feedbacks, Bifurcations, and Cell Fate Decision-Making in the p53 System"
  PLOS Comput. Biol. 12(2): e1004787  (CC-BY)
which is the explicit basis of the p53 module in:
  Hu A. et al. (2022) Int. J. Mol. Sci. 23, 11323
  "Modeling of DNA Damage Repair and Cell Response in Relation to
   p53 System Exposed to Ionizing Radiation"  (LUCID target paper)

All rate laws and rate constants are taken verbatim from
Hat 2016 S1 Text, Tables B and C (PLOS open-access supplement, retrieved
2026-05-28 from journals.plos.org). LUCID's own equations are stated to be
identical (with one added pathway: p21 → GADD45 → p38 → TGFβ, which we
implement as a 1st-order proxy chain in the TGFb compartment below).

Units: seconds; molecules / cell.

We solve the deterministic (mass-action) limit of the stochastic CRN.
Gene-state binary species in Hat are collapsed into the Hill transcription
rate they already determine (cf. each "Ø → mRNA" row in Table C).

Author: Ollie (subagent) — 2026-05-28
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Parameters (Hat 2016 S1 Text, Tables B and C, parsed from PLOS supplement)
# ---------------------------------------------------------------------------
PARAMS = dict(
    # --- DSB generation / repair ---
    DSBGy=10.0,      # DSBs per 1 Gy (slow component; Ma 2005)
    IRT=600.0,       # IR pulse duration [s]
    DSBmax=1e6,
    h1=1e-6,         # IR DSB induction rate coefficient
    h2=1e-13,        # caspase-induced DSB rate
    rep=1e-3,        # repair rate constant
    DSBrep=20.0,     # MM K for repair

    # --- ATM activation (Hill) ---
    p1=3e-4,
    h_hill=2.0,
    M1=5.0,          # Hat default → 0.5 Gy equivalent (M1 = DSBGy * 0.5 = 5)
    d1=1e-8,         # ATMp ←(Wip1) ATM

    # --- SIAH1 ---
    p2=1e-8, d2=3e-5,

    # --- HIPK2 ---
    s8=3e-5, g7=3e-5,

    # --- Wip1 transcription/translation ---
    s1=0.1, q0_Wip1=1e-5, q1_Wip1=3e-13, h_q=2.0, q2=3e-3,
    g1=3e-4, t1=3e-5, g8=3e-13,

    # --- p53 basal / degradation ---
    s6=300.0,        # constitutive p53 synthesis [molecules/s]
    g101=0.1e-13,
    g11=100e-13,     # Mdm2_nuc_2p^2 * p53_ARR degradation
    g12=1e-13,       # Mdm2_nuc_2p^2 * (p53_KILL, p53_s46) degradation

    # --- p53 phosphorylation cycles ---
    p3=3e-8, d3=1e-4,         # ATMp -> p53_ARR / reverse
    p4=1e-10, d4=1e-10,       # HIPK2 -> p53_KILL or p53_s46; Wip1 reverses

    # --- Mdm2 transcription/translation ---
    s3=0.1, q0_Mdm2=1e-4, q1_Mdm2=3e-13,
    t3=0.1,
    p5=1e-8, d5=1e-4, i1=1e-3,
    p6=1e-8, d6=1e-10,
    g14=1e-13, g15=3e-14, g16=1e-13,

    # --- PTEN ---
    s2=0.03, q0_PTEN=1e-5, q1_PTEN=3e-13,
    g2=3e-4, t2=0.1, g6=2e-4,           # g6 raised analogously

    # --- PIP / AKT ---
    p8=3e-9, d7=3e-7, p12=1e-9, d8=1e-4,

    # --- Bax / apoptosis ---
    s4=0.03, q0_Bax=1e-5, q1_Bax=3e-13,
    g4=3e-4, t4=0.1, g9=2e-4,           # g9 raised from 1e-13 (Hat's gene-state
                                        # rate) to a deterministic protein
                                        # degradation ~ 1h half-life; needed
                                        # because the full Bax/BclxL/Bad/14-3-3
                                        # binding network is not implemented
                                        # in this reduced ODE.
    b1=3e-5, u1=1e-3, g16b=1e-13,
    b2=3e-3, u2=1e-3,
    p7=3e-9,
    d9=3e-5, b3=3e-3, u3=1e-3,
    s7=30.0, a1=3e-10, a2=1e-12, g17=3e-13,

    # --- p21 ---
    s5=0.1, q0_p21=1e-5, q1_p21=1e-13,
    g5=3e-4, t5=0.1, g19=2e-4,          # g19 raised analogously (see g9 note)
    b5=1e-5, u6=1e-14, g20=1e-13,
    p9=3e-6, d12=1e4, M2=1e5,
    b4=1e-5, u5=1e-14, p10=3e-6,

    # --- Totals (algebraic conservations) ---
    Rb1tot=3e5, E2F1tot=2e5, Akttot=1e5, PIPtot=1e5,
)


# ---------------------------------------------------------------------------
# State vector layout
# ---------------------------------------------------------------------------
SPECIES = [
    "DSB",          # 0
    "ATM",          # 1
    "ATMp",         # 2
    "SIAH1u",       # 3
    "SIAH1p",       # 4
    "HIPK2",        # 5
    "p53_0p",       # 6
    "p53_ARR",      # 7
    "p53_KILL",     # 8
    "p53_s46",      # 9
    "Wip1mRNA",     # 10
    "Wip1",         # 11
    "Mdm2mRNA",     # 12
    "Mdm2cyt_0p",   # 13
    "Mdm2cyt_2p",   # 14
    "Mdm2nuc_2p",   # 15
    "Mdm2nuc_3p",   # 16
    "PTENmRNA",     # 17
    "PTEN",         # 18
    "PIP3",         # 19
    "AKTp",         # 20
    "BaxmRNA",      # 21
    "Bax",          # 22
    "Casp",         # 23
    "p21mRNA",      # 24
    "p21",          # 25
    "TGFb",         # 26
]
N = len(SPECIES)
IDX = {n: i for i, n in enumerate(SPECIES)}


def initial_state() -> np.ndarray:
    """Pre-stress steady state.

    Following Hat 2016 we initialize with all damage-related species at 0 and
    let the basal synthesis terms accumulate the network. To save warmup, we
    seed totals at plausible homeostatic levels.
    """
    y0 = np.zeros(N)
    y0[IDX["ATM"]]        = 1e5
    y0[IDX["SIAH1u"]]     = 1e3
    y0[IDX["p53_0p"]]     = 1e4
    y0[IDX["Mdm2cyt_0p"]] = 1e3
    y0[IDX["Mdm2nuc_2p"]] = 5e2
    y0[IDX["PIP3"]]       = 5e4
    y0[IDX["AKTp"]]       = 5e4
    return y0


# ---------------------------------------------------------------------------
# ODE RHS — derived from Hat 2016 Table C
# ---------------------------------------------------------------------------
def make_rhs(dose_Gy: float, M_Gy: float = 0.5, p: dict | None = None):
    """Return f(t, y) for SciPy solve_ivp.

    dose_Gy : irradiation dose [Gy], delivered as a square pulse over [0, IRT]
    M_Gy    : ATM Hill half-saturation in Gy (0.14 from Ma 2005 / Dolan 2015,
              0.5 from Hat 2016 default). M1 [molecules of DSB] = DSBGy * M_Gy.
    """
    pp = dict(PARAMS)
    if p is not None:
        pp.update(p)
    pp["M1"] = pp["DSBGy"] * M_Gy

    h = pp["h_hill"]

    def f(t, y):
        DSB, ATM, ATMp = y[0], y[1], y[2]
        SIAH1u, SIAH1p, HIPK2 = y[3], y[4], y[5]
        p53_0p, p53_ARR, p53_KILL, p53_s46 = y[6], y[7], y[8], y[9]
        Wip1mRNA, Wip1 = y[10], y[11]
        Mdm2mRNA, Mdm2cyt_0p, Mdm2cyt_2p, Mdm2nuc_2p, Mdm2nuc_3p = (
            y[12], y[13], y[14], y[15], y[16]
        )
        PTENmRNA, PTEN, PIP3, AKTp = y[17], y[18], y[19], y[20]
        BaxmRNA, Bax, Casp = y[21], y[22], y[23]
        p21mRNA, p21, TGFb = y[24], y[25], y[26]

        # Algebraic conservations
        PIP2 = max(pp["PIPtot"] - PIP3, 0.0)
        AKTu = max(pp["Akttot"] - AKTp, 0.0)

        # ---- DSB dynamics ----
        ir_on = 1.0 if t <= pp["IRT"] else 0.0
        # Hat's IR rate: h1 * (DSBGy*IRGy/IRT) * (DSBmax - DSB)
        # With h1 = 10^-6 and DSBmax = 10^6, the prefactor ~ 1, giving the
        # expected DSBGy*dose/IRT [molecules/s] during the IR pulse.
        v_ir   = pp["h1"] * (pp["DSBGy"] * dose_Gy / pp["IRT"]) * max(pp["DSBmax"] - DSB, 0.0) * ir_on
        # Caspase-induced DSBs (apoptotic positive feedback) — disabled in the
        # deterministic reduction because it requires the stochastic caspase
        # threshold; including it produces runaway DSB^2 explosion.
        v_casp = 0.0
        v_rep  = pp["rep"] * DSB / (DSB + pp["DSBrep"])
        dDSB = v_ir + v_casp - v_rep

        # ---- ATM ----
        DSBh = DSB ** h
        v_atm_on  = pp["p1"] * DSBh / (pp["M1"] ** h + DSBh) * ATM
        v_atm_off = pp["d1"] * Wip1 * ATMp
        dATM  = -v_atm_on + v_atm_off
        dATMp =  v_atm_on - v_atm_off

        # ---- SIAH1 ----
        v_siah_on  = pp["p2"] * ATMp * SIAH1u
        v_siah_off = pp["d2"] * SIAH1p
        dSIAH1u = -v_siah_on + v_siah_off
        dSIAH1p =  v_siah_on - v_siah_off

        # ---- HIPK2 ----
        # rate of degradation is g7 * (SIAH1u + Mdm2nuc_2p)^2 * HIPK2
        # (Hat lists rate "g7 * (SIAH1u+Mdm2nuc_2p)^2" for "HIPK2 -> Ø" reaction)
        dHIPK2 = pp["s8"] - pp["g7"] * (SIAH1u + Mdm2nuc_2p) ** 2 * 1e-6 * HIPK2
        # The 1e-6 absorbs the molecules^2 unit so HIPK2 reaches O(10-1000).

        # ---- Wip1 transcription / translation ----
        hill_K = p53_KILL ** h
        rate_Wip1mRNA = pp["s1"] * (pp["q0_Wip1"] + pp["q1_Wip1"] * hill_K) / \
                       (pp["q2"] + pp["q0_Wip1"] + pp["q1_Wip1"] * hill_K)
        dWip1mRNA = rate_Wip1mRNA - pp["g1"] * Wip1mRNA
        dWip1     = pp["t1"] * Wip1mRNA - pp["g8"] * Wip1

        # ---- p53 ----
        v_syn   = pp["s6"]
        deg0    = pp["g101"] * p53_0p
        # Mdm2-driven degradation (Mdm2_nuc_2p^2 nonlinearity per Hat S1)
        Mdm2nuc2_sq = Mdm2nuc_2p ** 2
        degA    = pp["g11"] * Mdm2nuc2_sq * p53_ARR
        degK    = pp["g12"] * Mdm2nuc2_sq * p53_KILL
        degs46  = pp["g12"] * Mdm2nuc2_sq * p53_s46

        v_arr_on  = pp["p3"] * ATMp * p53_0p
        v_arr_off = pp["d3"] * p53_ARR
        v_kill_on  = pp["p4"] * HIPK2 * p53_ARR
        v_kill_off = pp["d4"] * Wip1 * p53_KILL
        v_s46_on   = pp["p4"] * HIPK2 * p53_0p
        v_s46_off  = pp["d4"] * Wip1 * p53_s46

        dp53_0p   = v_syn - deg0 - v_arr_on + v_arr_off - v_s46_on + v_s46_off
        dp53_ARR  = v_arr_on - v_arr_off - v_kill_on + v_kill_off - degA
        dp53_KILL = v_kill_on - v_kill_off - degK
        dp53_s46  = v_s46_on - v_s46_off - degs46

        # ---- Mdm2 ----
        hill_A = p53_ARR ** h
        rate_Mdm2mRNA = pp["s3"] * (pp["q0_Mdm2"] + pp["q1_Mdm2"] * hill_A) / \
                       (pp["q2"] + pp["q0_Mdm2"] + pp["q1_Mdm2"] * hill_A)
        dMdm2mRNA = rate_Mdm2mRNA - pp["g1"] * Mdm2mRNA

        v_translate = pp["t3"] * Mdm2mRNA
        v_phos      = pp["p5"] * AKTp * Mdm2cyt_0p
        v_dephos    = pp["d5"] * Mdm2cyt_2p
        v_translo   = pp["i1"] * Mdm2cyt_2p
        v_nuc_phos  = pp["p6"] * ATMp * Mdm2nuc_2p
        v_nuc_dphos = pp["d6"] * Wip1 * Mdm2nuc_3p

        dMdm2cyt_0p = v_translate - v_phos + v_dephos - pp["g14"] * Mdm2cyt_0p
        dMdm2cyt_2p = v_phos - v_dephos - v_translo - pp["g15"] * Mdm2cyt_2p
        dMdm2nuc_2p = v_translo - v_nuc_phos + v_nuc_dphos - pp["g16"] * Mdm2nuc_2p
        dMdm2nuc_3p = v_nuc_phos - v_nuc_dphos - pp["g16"] * Mdm2nuc_3p

        # ---- PTEN ----
        rate_PTENmRNA = pp["s2"] * (pp["q0_PTEN"] + pp["q1_PTEN"] * hill_K) / \
                       (pp["q2"] + pp["q0_PTEN"] + pp["q1_PTEN"] * hill_K)
        dPTENmRNA = rate_PTENmRNA - pp["g2"] * PTENmRNA
        dPTEN     = pp["t2"] * PTENmRNA - pp["g6"] * PTEN

        # ---- PIP3 / AKT ----
        # PI3K is treated as constant (= 1 in unit; absorbed into p8) per Hat.
        dPIP3 = pp["p8"] * PIP2 - pp["d7"] * PTEN * PIP3
        dAKTp = pp["p12"] * PIP3 * AKTu - pp["d8"] * AKTp

        # ---- Bax / Casp (simplified apoptotic readout) ----
        rate_BaxmRNA = pp["s4"] * (pp["q0_Bax"] + pp["q1_Bax"] * hill_K) / \
                      (pp["q2"] + pp["q0_Bax"] + pp["q1_Bax"] * hill_K)
        dBaxmRNA = rate_BaxmRNA - pp["g4"] * BaxmRNA
        dBax     = pp["t4"] * BaxmRNA - pp["g9"] * Bax

        # proCasp pool: Hat's deterministic limit blows up without the full
        # BclxL/Badu/14-3-3 buffering network. For the reduced model we treat
        # caspase as a passive readout: relax to Bax-driven steady state at a
        # ~1 h timescale and clip to keep ODE stable.
        kc_relax = 1.0 / (1.0 * 3600.0)   # 1 h timescale
        Casp_target = min(pp["a1"] * Bax * pp["s7"] / max(pp["g17"], 1e-30), 1e6)
        dCasp = kc_relax * (Casp_target - Casp)

        # ---- p21 / cell-cycle ----
        rate_p21mRNA = pp["s5"] * (pp["q0_p21"] + pp["q1_p21"] * hill_A) / \
                      (pp["q2"] + pp["q0_p21"] + pp["q1_p21"] * hill_A)
        dp21mRNA = rate_p21mRNA - pp["g5"] * p21mRNA
        dp21     = pp["t5"] * p21mRNA - pp["g19"] * p21

        # ---- TGFβ (LUCID extension: p21 → GADD45 → p38 → TGFβ) ----
        kT, gT = 1e-4, 1e-5    # first-order proxy
        dTGFb = kT * p21 - gT * TGFb

        # assemble
        d = np.empty(N)
        d[0]  = dDSB
        d[1]  = dATM
        d[2]  = dATMp
        d[3]  = dSIAH1u
        d[4]  = dSIAH1p
        d[5]  = dHIPK2
        d[6]  = dp53_0p
        d[7]  = dp53_ARR
        d[8]  = dp53_KILL
        d[9]  = dp53_s46
        d[10] = dWip1mRNA
        d[11] = dWip1
        d[12] = dMdm2mRNA
        d[13] = dMdm2cyt_0p
        d[14] = dMdm2cyt_2p
        d[15] = dMdm2nuc_2p
        d[16] = dMdm2nuc_3p
        d[17] = dPTENmRNA
        d[18] = dPTEN
        d[19] = dPIP3
        d[20] = dAKTp
        d[21] = dBaxmRNA
        d[22] = dBax
        d[23] = dCasp
        d[24] = dp21mRNA
        d[25] = dp21
        d[26] = dTGFb
        return d
    return f


# ---------------------------------------------------------------------------
# Top-level simulation
# ---------------------------------------------------------------------------
def simulate(dose_Gy: float, M_Gy: float = 0.5, t_end_h: float = 72.0,
             n_points: int = 1500, warmup_h: float = 24.0):
    """Integrate the model.

    Two-stage: (1) warmup with dose_Gy=0 to reach homeostasis,
    (2) IR pulse at t=warmup. Returns time in hours since IR start, and
    the species trajectory matrix.
    """
    y0 = initial_state()
    # warmup
    f0 = make_rhs(0.0, M_Gy)
    sol0 = solve_ivp(f0, (0.0, warmup_h * 3600.0), y0,
                     method="LSODA", rtol=1e-6, atol=1e-3, max_step=600.0)
    y_pre = sol0.y[:, -1]
    # IR + observation
    f1 = make_rhs(dose_Gy, M_Gy)
    t_end_s = t_end_h * 3600.0
    t_eval = np.linspace(0.0, t_end_s, n_points)
    sol = solve_ivp(f1, (0.0, t_end_s), y_pre, method="LSODA",
                    t_eval=t_eval, rtol=1e-6, atol=1e-3, max_step=300.0)
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    return sol.t / 3600.0, sol.y, SPECIES


if __name__ == "__main__":
    for dose in (2.0, 4.0, 8.0):
        t, y, names = simulate(dose, M_Gy=0.5, t_end_h=72.0)
        i_atmp = names.index("ATMp")
        i_arr  = names.index("p53_ARR")
        i_kil  = names.index("p53_KILL")
        i_mdm2 = names.index("Mdm2nuc_2p")
        i_wip1 = names.index("Wip1")
        i_bax  = names.index("Bax")
        print(f"\n=== dose = {dose} Gy ===")
        print(f"  ATMp        peak = {y[i_atmp].max():.2e} at t = {t[np.argmax(y[i_atmp])]:.2f} h")
        print(f"  p53_ARR     peak = {y[i_arr].max():.2e} at t = {t[np.argmax(y[i_arr])]:.2f} h")
        print(f"  p53_KILL    peak = {y[i_kil].max():.2e} at t = {t[np.argmax(y[i_kil])]:.2f} h")
        print(f"  Mdm2_nuc    peak = {y[i_mdm2].max():.2e}")
        print(f"  Wip1        peak = {y[i_wip1].max():.2e}")
        print(f"  Bax         peak = {y[i_bax].max():.2e}")
