"""
Deterministic mean-field implementation of the Jonak et al. 2016
ATM/p53/NF-kB/Wip1 ODE model (doi:10.1186/s12918-016-0293-0).

All "stochastic" gene-state and DSB/receptor variables are evolved as continuous
ODEs of the form  dX/dt = (sum of activation propensities) - (sum of inactivation
propensities). This is the standard mean-field equivalent the authors explicitly
allow (paper states the deterministic gene state is in [0, 2]).

State vector ordering (43 variables). Index constants below.
Inputs IR(t) [Gy/s] and TNF(t) [ng/ml] are caller-provided.
"""
from __future__ import annotations
import numpy as np
import parameters as p

# ------------------- index map (43 ODEs) -------------------
NAMES = [
    "DSB",       # 0   number of double-strand breaks
    "Ra",        # 1   active TNF receptors
    # ATM module gene + transcripts + proteins
    "Gatm",      # 2
    "ATMt",      # 3
    "ATMn",      # 4
    "ATMpn",     # 5
    "ATMan",     # 6
    "Gchk2",     # 7
    "CHK2t",     # 8
    "CHK2n",     # 9
    "CHK2pn",    # 10
    "MRNpn",     # 11
    "CREBpn",    # 12
    # Wip1 module
    "Gwip1",     # 13
    "WIP1t",     # 14
    "WIP1n",     # 15
    "KSRPp",     # 16
    "KSRPpn",    # 17
    "PreMiR16",  # 18
    "MiR16",     # 19
    # Cell fate
    "Gbax",      # 20
    "BAXt",      # 21
    "BAX",       # 22
    "Gp21",      # 23
    "P21t",      # 24
    "P21",       # 25
    # p53 module
    "Gp53",      # 26
    "P53t",      # 27
    "P53n",      # 28
    "P53pn",     # 29
    "Gmdm2",     # 30
    "MDM2t",     # 31
    "MDM2",      # 32
    "MDM2p",     # 33
    "MDM2pn",    # 34
    "MDM2ppn",   # 35
    "Gpten",     # 36
    "PTENt",     # 37
    "PTEN",      # 38
    "PIP3",      # 39
    "AKTp",      # 40
    # NF-kB module
    "NFKB",      # 41
    "NFKBn",     # 42
    "IKBANFKB",  # 43
    "IKBApNFKB", # 44
    "IKBAnNFKBn",# 45
    "Gikba",     # 46
    "IKBAt",     # 47
    "IKBA",      # 48
    "IKBAp",     # 49
    "IKBAn",     # 50
    "Ga20",      # 51
    "A20t",      # 52
    "A20",       # 53
    "IKKK",      # 54
    "IKKKa",     # 55
    "IKK",       # 56
    "IKKa",      # 57
    "IKKi",      # 58
    "IKKii",     # 59
]
IDX = {n: i for i, n in enumerate(NAMES)}
N_STATES = len(NAMES)


def initial_state(rnai: str = "Ctr") -> np.ndarray:
    """Return initial-condition vector. rnai in {'Ctr', 'Wip1'} (Additional file 3)."""
    y = np.zeros(N_STATES)
    if rnai == "Ctr":
        ic = {
            "DSB": 0, "Ra": 0,
            "Gatm": 1, "ATMt": 132, "ATMn": 16130, "ATMpn": 0, "ATMan": 0,
            "Gchk2": 1, "CHK2t": 215, "CHK2n": 71290, "CHK2pn": 0,
            "MRNpn": 0, "CREBpn": 0,
            "Gwip1": 0, "WIP1t": 29, "WIP1n": 11770,
            "KSRPp": 0, "KSRPpn": 0, "PreMiR16": 0, "MiR16": 0,
            "Gbax": 0, "BAXt": 27, "BAX": 7691,
            "Gp21": 0, "P21t": 16, "P21": 7993,
            "Gp53": 1, "P53t": 353, "P53n": 30615, "P53pn": 6097,
            "Gmdm2": 0, "MDM2t": 31, "MDM2": 34496, "MDM2p": 15485,
            "MDM2pn": 163854, "MDM2ppn": 0,
            "Gpten": 0, "PTENt": 16, "PTEN": 31225,
            "PIP3": 189556, "AKTp": 1378,
            "NFKB": 174, "NFKBn": 184, "IKBANFKB": 99629, "IKBApNFKB": 0,
            "IKBAnNFKBn": 35,
            "Gikba": 0, "IKBAt": 35, "IKBA": 819, "IKBAp": 0, "IKBAn": 1077,
            "Ga20": 0, "A20t": 35, "A20": 14659,
            "IKKK": 10000, "IKKKa": 0, "IKK": 200000, "IKKa": 0,
            "IKKi": 0, "IKKii": 0,
        }
    elif rnai == "Wip1":
        ic = {
            "DSB": 0, "Ra": 0,
            "Gatm": 1, "ATMt": 132, "ATMn": 16130, "ATMpn": 0, "ATMan": 0,
            "Gchk2": 1, "CHK2t": 215, "CHK2n": 71290, "CHK2pn": 0,
            "MRNpn": 0, "CREBpn": 0,
            "Gwip1": 0, "WIP1t": 7, "WIP1n": 2918,
            "KSRPp": 0, "KSRPpn": 0, "PreMiR16": 0, "MiR16": 0,
            "Gbax": 0, "BAXt": 27, "BAX": 7683,
            "Gp21": 0, "P21t": 16, "P21": 7990,
            "Gp53": 1, "P53t": 353, "P53n": 30478, "P53pn": 6251,
            "Gmdm2": 0, "MDM2t": 31, "MDM2": 34596, "MDM2p": 15511,
            "MDM2pn": 164176, "MDM2ppn": 0,
            "Gpten": 0, "PTENt": 16, "PTEN": 31261,
            "PIP3": 189389, "AKTp": 1376,
            "NFKB": 174, "NFKBn": 177, "IKBANFKB": 99599, "IKBApNFKB": 0,
            "IKBAnNFKBn": 35,
            "Gikba": 0, "IKBAt": 36, "IKBA": 840, "IKBAp": 0, "IKBAn": 1115,
            "Ga20": 0, "A20t": 36, "A20": 14775,
            "IKKK": 10000, "IKKKa": 0, "IKK": 200000, "IKKa": 0,
            "IKKi": 0, "IKKii": 0,
        }
    else:
        raise ValueError(rnai)
    for k, v in ic.items():
        y[IDX[k]] = v
    return y


def rhs(t: float, y: np.ndarray, IR_func, TNF_func, siR: int = 0) -> np.ndarray:
    """Right-hand side of the 60-D ODE system.

    IR_func(t)  -> dose rate in Gy/s
    TNF_func(t) -> TNF concentration in ng/ml
    siR         -> Wip1 shRNA switch (0 = Ctr, 1 = Wip1-RNAi)
    """
    (DSB, Ra,
     Gatm, ATMt, ATMn, ATMpn, ATMan,
     Gchk2, CHK2t, CHK2n, CHK2pn, MRNpn, CREBpn,
     Gwip1, WIP1t, WIP1n, KSRPp, KSRPpn, PreMiR16, MiR16,
     Gbax, BAXt, BAX, Gp21, P21t, P21,
     Gp53, P53t, P53n, P53pn,
     Gmdm2, MDM2t, MDM2, MDM2p, MDM2pn, MDM2ppn,
     Gpten, PTENt, PTEN, PIP3, AKTp,
     NFKB, NFKBn, IKBANFKB, IKBApNFKB, IKBAnNFKBn,
     Gikba, IKBAt, IKBA, IKBAp, IKBAn,
     Ga20, A20t, A20, IKKK, IKKKa, IKK, IKKa, IKKi, IKKii) = y

    IR = IR_func(t)
    TNF = TNF_func(t)

    # ---- propensities (eqs. 1-24) ----
    a1 = p.ma1 * IR                                                   # DSB creation
    # Eq. 2 uses P53pn squared in numerator AND denominator; ensure non-neg DSB
    DSB_safe = max(DSB, 0.0)
    a2 = (p.mc1 * DSB_safe / (DSB_safe + p.mm1)) * \
         ((p.pq2 + p.pq3 * P53pn**2) / (p.pq4 + p.pq2 + p.pq3 * P53pn**2))
    a3 = p.na7 * TNF                                                  # receptor activation
    a4 = p.nc3                                                        # receptor inactivation per unit Ra
    a5 = p.mq1 + p.pq3 * P53pn**2 + p.mq2 * CREBpn                    # ATM gene on
    a6 = p.mq3                                                        # ATM gene off
    a7 = p.mq1                                                        # Chk2 gene on
    a8 = p.mq3                                                        # Chk2 gene off
    wip_block = p.nm1 / (p.nm1 + WIP1n)
    a9 = (p.pq2 + p.pq3 * P53pn**2 + p.mq2 * CREBpn + p.nq1 * NFKBn * wip_block)
    a10 = p.wq1
    a11 = p.pq1 + p.nq1 * NFKBn * wip_block                           # p53 gene on
    a12 = p.pq5
    a13 = p.nq1 * NFKBn * wip_block                                   # ikba gene on
    a14 = p.nq2 * IKBAn
    a15 = p.nq1 * NFKBn * wip_block                                   # a20 gene on
    a16 = p.nq2 * IKBAn
    a17 = p.pq2 + p.pq3 * P53pn**2                                    # bax gene on
    a18 = p.pq4
    a19 = p.pq2 + p.pq3 * P53pn**2                                    # p21 gene on
    a20 = p.pq4
    a21 = p.pq2 + p.pq3 * P53pn**2                                    # mdm2 gene on
    a22 = p.pq4
    a23 = p.pq2 + p.pq3 * P53pn**2                                    # pten gene on
    a24 = p.pq4

    dy = np.zeros_like(y)

    # ---- DSB (mean-field: dDSB/dt = creation - repair) ----
    dy[IDX["DSB"]] = a1 - a2

    # ---- Active receptors (mean-field) ----
    dy[IDX["Ra"]] = a3 * (p.Mtot - Ra) - a4 * Ra

    # ---- Gene states (mean-field): dG/dt = a_on*(NA-G) - a_off*G ----
    dy[IDX["Gatm"]]  = a5 * (p.NAatm - Gatm) - a6 * Gatm
    dy[IDX["Gchk2"]] = a7 * (p.NAchk2 - Gchk2) - a8 * Gchk2
    dy[IDX["Gwip1"]] = a9 * (p.NAwip1 - Gwip1) - a10 * Gwip1
    dy[IDX["Gp53"]]  = a11 * (p.NAp53 - Gp53)  - a12 * Gp53
    dy[IDX["Gikba"]] = a13 * (p.NAikba - Gikba) - a14 * Gikba
    dy[IDX["Ga20"]]  = a15 * (p.NAa20 - Ga20)  - a16 * Ga20
    dy[IDX["Gbax"]]  = a17 * (p.NAbax - Gbax)  - a18 * Gbax
    dy[IDX["Gp21"]]  = a19 * (p.NAp21 - Gp21)  - a20 * Gp21
    dy[IDX["Gmdm2"]] = a21 * (p.NAmdm2 - Gmdm2) - a22 * Gmdm2
    dy[IDX["Gpten"]] = a23 * (p.NApten - Gpten) - a24 * Gpten

    # ---- Transcripts ----
    # Eq.25: ATMt
    dy[IDX["ATMt"]] = p.ms1 * Gatm - p.md1 * ATMt
    # Eq.26: CHK2t with p53 repression
    dy[IDX["CHK2t"]] = p.ms2 * Gchk2 * (p.pm3 / (p.pm3 + P53pn)) - p.md3 * CHK2t
    # Eq.27: WIP1t
    dy[IDX["WIP1t"]] = p.ws1 * Gwip1 - (p.wd1 + siR * p.wd2 + p.wd3 * MiR16) * WIP1t
    # Eq.28: P53t
    dy[IDX["P53t"]] = p.ps1 * Gp53 - p.pd1 * P53t
    # Eq.29: BAXt
    dy[IDX["BAXt"]] = p.bs1 * Gbax - p.bd1 * BAXt
    # Eq.30: P21t
    dy[IDX["P21t"]] = p.bs2 * Gp21 - p.bd3 * P21t
    # Eq.31: MDM2t
    dy[IDX["MDM2t"]] = p.ps2 * Gmdm2 - p.pd6 * MDM2t
    # Eq.32: PTENt
    dy[IDX["PTENt"]] = p.ps3 * Gpten - p.pd10 * PTENt
    # Eq.33: IKBAt
    dy[IDX["IKBAt"]] = p.ns1 * Gikba * (p.pm3 / (p.pm3 + P53pn)) - p.nd2 * IKBAt
    # Eq.34: A20t
    dy[IDX["A20t"]] = p.ns1 * Ga20 * (p.pm3 / (p.pm3 + P53pn)) - p.nd2 * A20t

    # ---- ATM proteins (Eqs.35-37) ----
    dsb_term_atm = DSB / (DSB + p.mm2)
    dy[IDX["ATMn"]] = (p.mt1 * ATMt + p.mc2 * WIP1n * ATMpn
                       - ATMn * p.ma3 * dsb_term_atm - p.md2 * ATMn)
    dy[IDX["ATMpn"]] = (ATMn * p.ma3 * dsb_term_atm
                        + p.mc2 * WIP1n * ATMan
                        - p.ma4 * ATMpn * MRNpn
                        - p.mc2 * WIP1n * ATMpn
                        - p.md2 * ATMpn)
    dy[IDX["ATMan"]] = (p.ma4 * ATMpn * MRNpn
                        - p.mc2 * WIP1n * ATMan
                        - p.md2 * ATMan)

    # ---- Chk2 (Eqs.38-39) ----
    dy[IDX["CHK2n"]] = (p.mt2 * CHK2t + p.mc3 * WIP1n * CHK2pn
                        - p.ma5 * ATMan * CHK2n - p.md4 * CHK2n)
    dy[IDX["CHK2pn"]] = (p.ma5 * ATMan * CHK2n
                         - p.mc3 * WIP1n * CHK2pn
                         - p.md4 * CHK2pn)

    # ---- MRN (Eq.40) ----
    dsb_term_mrn = DSB / (DSB + p.mm3)
    dy[IDX["MRNpn"]] = ((p.ma6 * ATMpn + p.ma7 * dsb_term_mrn)
                        * (p.MRNtot - MRNpn) - p.mc4 * MRNpn)

    # ---- CREB (Eq.41) ----
    dy[IDX["CREBpn"]] = p.ma5 * ATMan * (p.CREBtot - CREBpn) - p.mc5 * CREBpn

    # ---- Wip1 protein (Eq.42) ----
    dy[IDX["WIP1n"]] = p.wt1 * WIP1t - p.wd4 * WIP1n

    # ---- KSRP & miRNAs (Eqs.43-46) ----
    dy[IDX["KSRPp"]] = (p.wa1 * ATMan * (p.KSRPtot - KSRPp - KSRPpn)
                        + p.we1 * KSRPpn - p.wc1 * KSRPp - p.wi1 * KSRPp)
    dy[IDX["KSRPpn"]] = p.wi1 * KSRPp - p.we1 * KSRPpn
    dy[IDX["PreMiR16"]] = p.ws2 * KSRPpn - p.wd5 * PreMiR16
    dy[IDX["MiR16"]] = p.wa2 * PreMiR16 - p.wd6 * MiR16

    # ---- PIP3 (Eq.47) and Bax/p21 proteins (Eqs.48-49) ----
    dy[IDX["PIP3"]] = p.pa7 * (p.PIPtot - PIP3) - p.pc3 * PTEN * PIP3
    dy[IDX["BAX"]] = p.bt1 * BAXt - p.bd2 * BAX
    dy[IDX["P21"]] = p.bt2 * P21t - p.bd4 * P21

    # ---- p53 nuclear forms (Eqs.50-51) ----
    activation_p53 = (p.pa1
                      + p.pa2 * ATMan / (ATMan + p.pm1)
                      + p.pa3 * CHK2pn / (CHK2pn + p.pm2))
    dy[IDX["P53n"]] = (p.pt1 * P53t + p.pc1 * P53pn * WIP1n
                       - activation_p53 * P53n
                       - (p.pd2 + p.pd3 * MDM2pn**2) * P53n)
    dy[IDX["P53pn"]] = (activation_p53 * P53n
                        - p.pc1 * P53pn * WIP1n
                        - (p.pd4 + p.pd5 * MDM2pn**2) * P53pn)

    # ---- Mdm2 forms (Eqs.52-55) ----
    chk_term = CHK2pn / (CHK2pn + p.pm2)
    dy[IDX["MDM2"]] = (p.pt2 * MDM2t + p.pc2 * MDM2p
                       - p.pa4 * MDM2 * AKTp
                       - (p.pd7 + p.pd9 * chk_term) * MDM2)
    dy[IDX["MDM2p"]] = (p.pa4 * MDM2 * AKTp - p.pc2 * MDM2p - p.pi1 * MDM2p
                        - (p.pd8 + p.pd9 * chk_term) * MDM2p)
    dy[IDX["MDM2pn"]] = (p.pi1 * MDM2p + p.pa5 * WIP1n * MDM2ppn
                         - p.pa6 * MDM2pn * ATMan
                         - (p.pd8 + p.pd9 * p.kv * chk_term) * MDM2pn)
    dy[IDX["MDM2ppn"]] = (p.pa6 * MDM2pn * ATMan
                          - p.pa5 * WIP1n * MDM2ppn
                          - (p.pd8 + p.pd9 * p.kv * chk_term) * MDM2ppn)

    # ---- Akt (Eq.56) ----
    dy[IDX["AKTp"]] = (p.pa8 * PIP3 * (1 + p.pa9 * ATMan) * (p.AKTtot - AKTp)
                       - p.pc4 * AKTp)

    # ---- PTEN protein (Eq.59) ----
    dy[IDX["PTEN"]] = p.pt3 * PTENt - p.pd11 * PTEN

    # ---- IKK module (Eqs.57-58, 69-72) ----
    dy[IDX["IKK"]] = p.na4 * IKKii - (p.na5 * IKKKa + p.na6 * ATMan) * IKK
    dy[IDX["IKKa"]] = ((p.na5 * IKKKa + p.na6 * ATMan) * IKK
                       - p.nc2 * IKKa * (p.nm4 + A20) / p.nm4)
    a20_term = p.nm2 / (p.nm2 + A20)
    dy[IDX["IKKK"]] = p.nc1 * IKKKa - p.na3 * Ra * IKKK * a20_term
    dy[IDX["IKKKa"]] = p.na3 * Ra * IKKK * a20_term - p.nc1 * IKKKa
    dy[IDX["IKKi"]] = p.nc2 * IKKa * (p.nm4 + A20) / p.nm4 - p.na4 * IKKi
    dy[IDX["IKKii"]] = p.na4 * IKKi - p.na4 * IKKii

    # ---- NF-kB module (Eqs.60-68) ----
    dy[IDX["NFKB"]] = (p.nk1 * IKBANFKB + p.nd1 * IKBApNFKB
                       - p.nk2 * NFKB * IKBA - p.ni1 * NFKB)
    dy[IDX["NFKBn"]] = p.ni1 * NFKB - p.nk2 * p.kv * NFKBn * IKBAn
    dy[IDX["IKBANFKB"]] = (p.nk2 * NFKB * IKBA + p.ne2 * IKBAnNFKBn
                           - p.nk1 * IKBANFKB - p.na1 * IKKa * IKBANFKB)
    dy[IDX["IKBApNFKB"]] = p.na1 * IKKa * IKBANFKB - p.nd1 * IKBApNFKB
    dy[IDX["IKBAnNFKBn"]] = p.nk2 * p.kv * NFKBn * IKBAn - p.ne2 * IKBAnNFKBn
    dy[IDX["IKBA"]] = (p.nt1 * IKBAt + p.ne1 * IKBAn
                       - p.na2 * IKKa * IKBA - p.nk2 * NFKB * IKBA
                       - p.ni2 * IKBA - p.nd3 * IKBA)
    dy[IDX["IKBAp"]] = p.na2 * IKKa * IKBA - p.nd1 * IKBAp
    dy[IDX["IKBAn"]] = (p.ni2 * IKBA - p.nk2 * p.kv * NFKBn * IKBAn
                        - p.ne1 * IKBAn)
    dy[IDX["A20"]] = p.nt2 * A20t - p.nd4 * A20

    return dy
