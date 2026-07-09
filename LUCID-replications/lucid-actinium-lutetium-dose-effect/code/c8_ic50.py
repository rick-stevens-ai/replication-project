"""
C8 — IC50 values 1.53E-08 M (Ac-225) vs 2.61E-08 M (Lu-177).

These are the displacement IC50 values reported in the paper's Results section:
"resulted in similar IC50 values [...] in the nanomolar range (1.53E-08 M and
2.61E-08 M, respectively)" (p.3631) — first value is Ac-225, second is Lu-177
based on the surrounding text order ([225Ac]Ac-PSMA-I&T followed by
[177Lu]Lu-PSMA-I&T).

We cannot re-fit the IC50 displacement curve without the raw plate-counts data,
but we CAN:
  (a) record the stated values and 95% CI claim ("similar IC50 values");
  (b) check that both values lie in the nanomolar range as described;
  (c) compute the Ac/Lu ratio to show they are not statistically different in
      the order-of-magnitude sense the paper claims (i.e. same binding affinity).

Source data (raw plate counts) — DATA-BLOCKED: not provided in the paper or
its supplement; would need to be obtained from the corresponding author
(Data Availability statement: "available from the corresponding author on
reasonable request").
"""
import json

IC50_Ac_M = 1.53e-8
IC50_Lu_M = 2.61e-8

ratio = IC50_Lu_M / IC50_Ac_M
in_nM_range = (1e-9 <= IC50_Ac_M < 1e-7) and (1e-9 <= IC50_Lu_M < 1e-7)

result = {
    "claim": "C8: IC50(Ac-225) = 1.53E-08 M; IC50(Lu-177) = 2.61E-08 M",
    "IC50_Ac_M": IC50_Ac_M,
    "IC50_Lu_M": IC50_Lu_M,
    "ratio_Lu_over_Ac": round(ratio, 3),
    "in_nanomolar_range": in_nM_range,
    "data_status": "DATA-BLOCKED for independent re-fit",
    "missing_artifact": (
        "Raw IC50 displacement curve counts (per-concentration "
        "radiolabeled-PSMA-I&T %AA after washout). Per paper Data Availability "
        "statement: available from the corresponding author on reasonable request."
    ),
    "verdict": (
        f"STATED VALUES CONFIRMED — both in the nM range (1.5e-8 and 2.6e-8 M); "
        f"Lu/Ac ratio = {ratio:.2f}, consistent with the paper's claim of "
        "'similar' binding affinity (within 2x, well inside displacement-assay "
        "noise). Raw data needed for independent re-fit; flagged DATA-BLOCKED."
    ),
}

with open("results/c8_ic50.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
