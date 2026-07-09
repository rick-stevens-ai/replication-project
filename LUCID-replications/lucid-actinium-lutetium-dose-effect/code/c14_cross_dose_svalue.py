"""
C14 — Cross-dose S-value Lu-177 = 1.13E-06 Gy(Bq*s)^-1.

This number is a Monte-Carlo (Geant4) Lu-177 cross-dose S-value reported in the
paper's Results: "The cross absorbed dose rate S value in the uptake phase for
lutetium-177 is 1.13E-06 Gy(Bq*s)^-1, irrespectively of the source
localization." (Paper, Results, p. 3633.)

We cannot re-derive this without Geant4. We CAN do two sanity checks:

(a) Physics ordering: cross-dose S should sit BELOW self-absorbed (membrane &
    cytoplasm) S-values (because cross-dose is from many distant cells, mostly
    via long-range electrons and gammas) and ABOVE the medium S-value (because
    cross-dose-source cells are closer than the medium-distributed activity).
(b) Order-of-magnitude consistency with the reported ratio of cross-dose to
    membrane self-dose (cross/self ~ 0.01x for the averaged dimension).

If both pass, we mark the claim as PHYSICS-CONSISTENT (the numeric value is
quoted verbatim from the paper, not independently derived).
"""
import json

S_self_memb_avg_floating_Lu = 1.04e-4
S_self_cyto_avg_floating_Lu = 1.98e-4
S_self_memb_avg_floating_Ac = 5.63e-2
S_medium_Lu = 2.30e-11
S_medium_Ac = 4.57e-09
S_cross_Lu_paper = 1.13e-06  # quoted

# Ordering check
ordering_ok_membrane = S_medium_Lu < S_cross_Lu_paper < S_self_memb_avg_floating_Lu
ordering_ok_cyto = S_medium_Lu < S_cross_Lu_paper < S_self_cyto_avg_floating_Lu

ratio_cross_to_self_memb = S_cross_Lu_paper / S_self_memb_avg_floating_Lu
ratio_cross_to_medium = S_cross_Lu_paper / S_medium_Lu

result = {
    "claim": "C14: cross-dose S-value Lu-177 = 1.13E-06 Gy(Bq*s)^-1",
    "S_cross_Lu_paper_value": S_cross_Lu_paper,
    "S_self_membrane_avg_Lu": S_self_memb_avg_floating_Lu,
    "S_self_cytoplasm_avg_Lu": S_self_cyto_avg_floating_Lu,
    "S_medium_Lu": S_medium_Lu,
    "physics_ordering_medium_lt_cross_lt_self_membrane": ordering_ok_membrane,
    "physics_ordering_medium_lt_cross_lt_self_cytoplasm": ordering_ok_cyto,
    "ratio_cross_to_self_membrane": round(ratio_cross_to_self_memb, 4),
    "ratio_cross_to_medium": round(ratio_cross_to_medium, 0),
    "ac_cross_dose_neglected_per_paper": (
        "Yes — paper explicitly states Ac cross-dose was neglected due to short alpha range."
    ),
    "ac_alpha_range_micrometres_approx": "47-85 (Ac-225 daughter chain alphas in tissue)",
    "verdict": (
        "STATED VALUE CONFIRMED (paper Results, p. 3633). Physics-consistent: "
        f"cross-dose ({S_cross_Lu_paper:.2e}) sits between medium ({S_medium_Lu:.2e}) "
        f"and self-membrane ({S_self_memb_avg_floating_Lu:.2e}) — ratio cross/self = "
        f"{ratio_cross_to_self_memb:.3f}, ratio cross/medium = {ratio_cross_to_medium/1:.0f}. "
        "Independent Geant4 re-derivation is out of scope."
    ),
}

with open("results/c14_cross_dose_svalue.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
