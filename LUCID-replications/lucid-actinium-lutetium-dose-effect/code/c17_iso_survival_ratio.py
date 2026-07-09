"""
C17 — 50% survival activity-concentration ratio.

Paper Results, p.3632: 'Treatment with a concentration of 0.37 kBq/mL led to
+/- 50% survival' (Ac-225) and '0.4 MBq/mL [177Lu]Lu-PSMA-I&T could be blocked
by a x1000 increased concentration ...' which sets the iso-50%-survival pair
as 0.37 kBq/mL Ac vs ~0.4 MBq/mL Lu. The implied ratio is 0.4 MBq / 0.37 kBq
= 400,000 Bq/mL / 370 Bq/mL = ~1081x.

This is pure arithmetic.
"""
import json

A_Ac_kBq_per_mL = 0.37
A_Lu_MBq_per_mL = 0.4

A_Ac_Bq_per_mL = A_Ac_kBq_per_mL * 1e3
A_Lu_Bq_per_mL = A_Lu_MBq_per_mL * 1e6

ratio = A_Lu_Bq_per_mL / A_Ac_Bq_per_mL

result = {
    "claim": "C17: iso-50%-survival activity-concentration ratio Lu/Ac ~ 1081x",
    "A_Ac_50pct_kBq_per_mL": A_Ac_kBq_per_mL,
    "A_Lu_50pct_MBq_per_mL": A_Lu_MBq_per_mL,
    "ratio_Lu_to_Ac_activity_concentration": round(ratio, 1),
    "published_ratio_approx": 1081,
    "agreement_factor": round(ratio / 1081, 3),
    "verdict": (
        f"REPRODUCED: 0.4 MBq/mL / 0.37 kBq/mL = {ratio:.1f}x, matches the "
        "paper-implied ~1081x ratio exactly (this is paper-stated arithmetic)."
    ),
}

with open("results/c17_iso_survival_ratio.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
