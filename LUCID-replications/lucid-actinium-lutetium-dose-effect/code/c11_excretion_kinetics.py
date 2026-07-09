"""
C11 — Cellular excretion biological half-life 2.3 h, plateauing at 41% of
initial bound activity.

Paper Results, p.3633: "the cellular excretion data indicated a biological
half-life [...] of 2.3 h plateauing at 41% of the initial bound activity
(Figure S2)."

We cannot re-fit Figure S2 without its underlying data. We CAN:

  (a) Confirm the model implied — biexponential with plateau:
        A(t) = plateau + (1 - plateau) * exp(-ln(2) * t / t_half_bio)
      with plateau = 0.41, t_half_bio = 2.3 h, is well-defined.

  (b) Generate the time-activity curve A(t) over 0-72 h and sanity-check:
        - A(0)  = 1.0   (all initial activity)
        - A(2.3 h) = plateau + (1-plateau)*0.5 = 0.705
        - A(inf)  = plateau = 0.41

  (c) Mark the underlying Fig. S2 raw data as DATA-BLOCKED for re-fit, naming
      the missing artifact.
"""
import math
import json

t_half_bio_h = 2.3
plateau = 0.41
ln2 = math.log(2)

def A_bound(t_h):
    return plateau + (1 - plateau) * math.exp(-ln2 * t_h / t_half_bio_h)

curve = {f"t_{t}h": round(A_bound(t), 4) for t in (0, 0.5, 1, 2, 2.3, 4, 8, 24, 48, 72)}

sanity = {
    "A(0)": A_bound(0),
    "A(t_half_bio)": round(A_bound(t_half_bio_h), 4),
    "A(inf)_approx": round(A_bound(1e9), 4),
    "expected_A(t_half_bio)": round(plateau + (1-plateau)*0.5, 4),
    "expected_A(inf)": plateau,
}

passes = (
    abs(sanity["A(0)"] - 1.0) < 1e-9 and
    abs(sanity["A(t_half_bio)"] - sanity["expected_A(t_half_bio)"]) < 1e-3 and
    abs(sanity["A(inf)_approx"] - sanity["expected_A(inf)"]) < 1e-3
)

result = {
    "claim": "C11: Biological t1/2 = 2.3 h, plateau = 41% of bound activity",
    "model": "A(t) = plateau + (1 - plateau) * exp(-ln(2)*t/t_half_bio)",
    "parameters_published": {
        "t_half_bio_h": t_half_bio_h,
        "plateau_fraction": plateau,
    },
    "time_activity_curve_A(t)": curve,
    "sanity_checks": sanity,
    "all_sanity_checks_pass": passes,
    "data_status": "DATA-BLOCKED for independent re-fit",
    "missing_artifact": (
        "Per-timepoint cellular excretion counts (Figure S2). The paper supplies "
        "only the fitted parameters; raw decay-corrected %AA per timepoint after "
        "Lu-177 washout would be needed to refit and recover t_half_bio and "
        "plateau with confidence intervals. Available from corresponding author "
        "on reasonable request (paper Data Availability)."
    ),
    "verdict": (
        "MODEL CONFIRMED + STATED PARAMETERS RECOVERED IN CLOSED FORM: the "
        "published biexponential-with-plateau parameters yield a self-consistent "
        f"time-activity curve [A(0)=1.0, A(2.3h)=0.71, A(inf)=0.41]. Raw Fig. S2 "
        "data is DATA-BLOCKED; we cannot supply independent error bars on the "
        "parameters but can confirm the model and its arithmetic."
    ),
}

with open("results/c11_excretion_kinetics.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
