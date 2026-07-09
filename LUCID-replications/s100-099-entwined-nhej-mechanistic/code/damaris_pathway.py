"""
DaMaRiS pathway definition — Scenario D ("entwined") + reductions to A, B, C.

Rate constants (time constants in seconds) are taken from the canonical
TOPAS-nBio port of DaMaRiS published by the same authors as the replicated
paper (Ingram et al., Sci Rep 9:6359, 2019).

Source: https://github.com/topas-nbio/TOPAS-nBio
        examples/damaris/pathwayHR.txt   (Scenario D / entwined)
        examples/damaris/pathwayNHEJ.txt (NHEJ-only reduction)

The pathway is a continuous-time Markov chain on DSB-end states with one
bimolecular reaction (DSB end pairing into a synaptic complex).

State alphabet (consistent with TOPAS-nBio):
  DSBEnd                   — naked exposed end
  DSBEnd_Inhibited         — end-cleaning required before protein load
  DSBEnd_Ku                — Ku70/80 loaded
  DSBEnd_PKcs              — Ku+DNA-PKcs loaded
  DSBEnd_MRN               — MRN loaded (HR initiation)
  DSBEnd_Ku_MRN            — Ku co-localised with MRN
  DSBEnd_PK_MRN            — Ku+PKcs co-localised with MRN
  DSBEnd_MRN_RNF138        — RNF138 has removed Ku/PKcs, MRN remains
  DSBEnd_Resected          — CtIP resection done, committed to HR
  DSBEnd_RPA               — RPA coated
  DSB_Fixed_HR             — HR repair complete
  DSBSynaptic              — paired ends (both PKcs)
  DSBSynaptic_MRN          — paired ends with MRN present
  DSBSynaptic_Stable       — synaptic complex stabilised (XLF/XRCC4/Lig4)
  DSB_Fixed                — NHEJ repair complete

Pairwise (second-order) reactions in DaMaRiS are diffusion-limited at a
reaction range of 25 nm.  We approximate them in a well-mixed mean-field
fashion: per-pair encounter rate = k_synapse * n_pair / V_nucleus, where
V_nucleus is a sphere of radius 2.5 um (matches DaMaRiS.run example).  The
effective second-order rate constant k_synapse is fit so the wild-type
Scenario D simulation reproduces the t1/2 ≈ ~30 min for the fast NHEJ
component reported in the paper (Beucher 2009 WT).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class Transition:
    src: str            # source state
    dst: tuple          # 1- or 2-tuple of product states
    tau: float          # mean time constant (s) — rate = 1/tau
    label: str = ""     # human label
    require_clean: bool = False   # only fires once the end is "clean"


# --------------------------------------------------------------------------- #
# Scenario D — the entwined pathway (TOPAS-nBio pathwayHR.txt, 24 transitions)
# --------------------------------------------------------------------------- #
SCENARIO_D: list[Transition] = [
    # 1  End cleaning gate
    Transition("DSBEnd",            ("DSBEnd_Inhibited",), 0.55, "end-cleaning enter"),
    Transition("DSBEnd_Inhibited",  ("DSBEnd",),           3.8,  "end-cleaning exit"),

    # NHEJ pre-synaptic loading
    Transition("DSBEnd",            ("DSBEnd_Ku",),        1.1,  "Ku load"),
    Transition("DSBEnd_Ku",         ("DSBEnd_PKcs",),      1.2,  "DNA-PKcs load on Ku"),

    # HR pre-synaptic loading (MRN co-localisation)
    Transition("DSBEnd",            ("DSBEnd_MRN",),       35.0, "MRN load (independent)"),
    Transition("DSBEnd_Ku",         ("DSBEnd_Ku_MRN",),    35.0, "MRN co-loc with Ku"),
    Transition("DSBEnd_PKcs",       ("DSBEnd_PK_MRN",),    35.0, "MRN co-loc with PK"),
    Transition("DSBEnd_MRN",        ("DSBEnd_Ku_MRN",),    1.1,  "Ku load on MRN-end"),
    Transition("DSBEnd_Ku_MRN",     ("DSBEnd_PK_MRN",),    1.2,  "DNA-PKcs load on Ku+MRN"),

    # Resection (CtIP) — direct
    Transition("DSBEnd_MRN",        ("DSBEnd_Resected",),  1.2,  "CtIP resection (MRN)"),

    # RNF138-dependent Ku/PKcs removal -> RNF138 stage
    Transition("DSBEnd_MRN",        ("DSBEnd_MRN_RNF138",),    100.0, "RNF138 recruit (bare MRN)"),
    Transition("DSBEnd_Ku_MRN",     ("DSBEnd_MRN_RNF138",),    100.0, "RNF138 removes Ku"),
    Transition("DSBEnd_PK_MRN",     ("DSBEnd_MRN_RNF138",),    100.0, "RNF138 removes Ku+PKcs"),
    Transition("DSBEnd_MRN_RNF138", ("DSBEnd_Resected",),      1.2,   "CtIP resection (RNF138)"),

    # HR downstream
    Transition("DSBEnd_Resected",   ("DSBEnd_RPA",),       9.0,    "RPA coat"),
    Transition("DSBEnd_RPA",        ("DSB_Fixed_HR",),     34262.0,"τRR (HR completion)"),

    # NHEJ synaptic stabilisation (post-pairing first-order steps)
    Transition("DSBSynaptic",       ("DSBSynaptic_Stable",), 250.0, "synapsis stabilise"),
    Transition("DSBSynaptic_MRN",   ("DSBSynaptic_Stable",), 250.0, "synapsis stabilise (MRN)"),
    # NB DaMaRiS represents end-cleaning of backbone and base on the stable
    # synapse via two self-loops with require_clean flags; we collapse this
    # into the single sequential first-order ligation step with rate that
    # combines them analytically (means add): 300 + 900 + 1200 = 2400 s, but
    # because DaMaRiS treats them sequentially before the require_clean
    # ligation, we model three serial steps:
    Transition("DSBSynaptic_Stable",("DSBSynaptic_Clean1",), 300.0,  "clean backbone"),
    Transition("DSBSynaptic_Clean1",("DSBSynaptic_Clean2",), 900.0,  "clean base"),
    Transition("DSBSynaptic_Clean2",("DSB_Fixed",),          1200.0, "ligation (Lig4)",
               require_clean=True),

    # NHEJ synaptic dissociation
    Transition("DSBSynaptic",     ("DSBEnd", "DSBEnd"),         140.0, "synapse dissoc"),
    Transition("DSBSynaptic_MRN", ("DSBEnd_MRN", "DSBEnd_MRN"), 140.0, "synapse dissoc (MRN)"),
]

# Pair-forming (second-order) reactions
PAIR_REACTIONS_D: list[tuple[str, str, str]] = [
    # (reactant_a, reactant_b, product_synaptic_state)
    ("DSBEnd_PKcs",   "DSBEnd_PKcs",   "DSBSynaptic"),
    ("DSBEnd_PKcs",   "DSBEnd_PK_MRN", "DSBSynaptic"),
    ("DSBEnd_PK_MRN", "DSBEnd_PK_MRN", "DSBSynaptic"),  # source: TOPAS-nBio
    # Note: a true "DSBSynaptic_MRN" product appears in dissociation but the
    # canonical pathway lists only "DSBSynaptic" as product, so we follow that.
]

# --------------------------------------------------------------------------- #
# Scenario C — continuous competition (no MRN co-localisation, no RNF138)
# --------------------------------------------------------------------------- #
def make_scenario_c() -> tuple[list[Transition], list[tuple[str, str, str]]]:
    """Continuous competition: NHEJ vs HR initial protein loading; on synapse
    dissociation, ends return to bare 'DSBEnd' and can re-compete.  No MRN
    co-localisation with NHEJ proteins, no RNF138-mediated Ku removal."""
    keep_labels = {
        "end-cleaning enter", "end-cleaning exit",
        "Ku load", "DNA-PKcs load on Ku",
        "MRN load (independent)",
        "CtIP resection (MRN)",
        "RPA coat", "τRR (HR completion)",
        "synapsis stabilise",
        "clean backbone", "clean base", "ligation (Lig4)",
        "synapse dissoc",
    }
    trans = [t for t in SCENARIO_D if t.label in keep_labels]
    pairs = [("DSBEnd_PKcs", "DSBEnd_PKcs", "DSBSynaptic")]
    return trans, pairs


# --------------------------------------------------------------------------- #
# Scenario B — no way back (initial protein attachment locks pathway).
# Realised by removing the synapse-dissociation transition (so ends cannot
# return to compete) AND removing MRN co-localisation / RNF138 paths.
# --------------------------------------------------------------------------- #
def make_scenario_b() -> tuple[list[Transition], list[tuple[str, str, str]]]:
    trans_c, pairs_c = make_scenario_c()
    trans = [t for t in trans_c if t.label not in {"synapse dissoc"}]
    return trans, pairs_c


# --------------------------------------------------------------------------- #
# Scenario A — NHEJ first; only on NHEJ failure does HR fire.
# Realised by removing the initial DSBEnd->DSBEnd_MRN loading (no HR initiation
# from a bare end) and routing synapse dissociation directly into
# DSBEnd_Resected (forced HR after NHEJ failure).
# --------------------------------------------------------------------------- #
def make_scenario_a() -> tuple[list[Transition], list[tuple[str, str, str]]]:
    trans_c, pairs_c = make_scenario_c()
    trans = [t for t in trans_c if t.label not in {
        "MRN load (independent)", "CtIP resection (MRN)", "synapse dissoc",
    }]
    # Forced HR on synapse dissociation: products go straight to resected
    trans = trans + [
        Transition("DSBSynaptic", ("DSBEnd_Resected", "DSBEnd_Resected"),
                   140.0, "synapse dissoc -> forced HR"),
    ]
    return trans, pairs_c


SCENARIOS = {
    "A": lambda: make_scenario_a(),
    "B": lambda: make_scenario_b(),
    "C": lambda: make_scenario_c(),
    "D": lambda: (list(SCENARIO_D), list(PAIR_REACTIONS_D)),
}


# --------------------------------------------------------------------------- #
# Deficiency configurations
# --------------------------------------------------------------------------- #
def apply_deficiency(transitions: list[Transition], deficiency: str
                     ) -> list[Transition]:
    """deficiency in {WT, XLF, Lig4}.  XLF-: no synapse stabilisation
    (DSBSynaptic -> DSBSynaptic_Stable removed).  Lig4-: no final ligation
    (DSBSynaptic_Clean2 -> DSB_Fixed removed)."""
    if deficiency == "WT":
        return transitions
    out: list[Transition] = []
    for t in transitions:
        if deficiency == "XLF" and t.label.startswith("synapsis stabilise"):
            continue
        if deficiency == "Lig4" and t.label == "ligation (Lig4)":
            continue
        out.append(t)
    return out


# Final repaired states (count toward "repaired")
REPAIRED_STATES = {"DSB_Fixed", "DSB_Fixed_HR"}

# All end states that are still "broken" (counted in residual-DSB γ-H2AX foci)
# After a synapse forms, two ends become one synaptic complex but the foci
# count is per DSB, not per end, so a synaptic complex counts as ONE DSB.
SYNAPTIC_STATES = {
    "DSBSynaptic", "DSBSynaptic_MRN", "DSBSynaptic_Stable",
    "DSBSynaptic_Clean1", "DSBSynaptic_Clean2",
}
END_STATES_BROKEN = {
    "DSBEnd", "DSBEnd_Inhibited", "DSBEnd_Ku", "DSBEnd_PKcs",
    "DSBEnd_MRN", "DSBEnd_Ku_MRN", "DSBEnd_PK_MRN", "DSBEnd_MRN_RNF138",
    "DSBEnd_Resected", "DSBEnd_RPA",
}


def all_states(transitions: Sequence[Transition],
               pairs: Sequence[tuple[str, str, str]]) -> set[str]:
    s: set[str] = set()
    for t in transitions:
        s.add(t.src)
        for d in t.dst:
            s.add(d)
    for a, b, p in pairs:
        s.update({a, b, p})
    return s
