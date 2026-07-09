#!/usr/bin/env python3
"""
Spot-check of the LQ survival predictions in Matsuya et al. 2019,
"Intensity Modulated Radiation Fields Induce Protective Effects and Reduce
Importance of Dose-Rate Effects", Sci Rep 9:9533, DOI 10.1038/s41598-019-45960-z.

The paper fits an Integrated Microdosimetric-Kinetic (IMK) model with
parameters (alpha_0, beta_0, a+c) reported in Table 1 for two cell lines
(AGO1522, DU145) under modulated-field (MF) and uniform-field (UF) exposures,
plus an intercellular-communication branch (alpha_b, beta_b, delta).

For the *acute single-dose* limit (T -> 0, N=1) the IMK reduces to standard
LQ form for the DNA-TE term:

    -ln S_T(D) = alpha_0 * D + beta_0 * D^2

The paper plots survival curves D in [0, 6] Gy.  We compute LQ S(D) with
Table 1 parameters and verify that survival is *higher* under MF than UF for
AGO1522 (the paper's headline qualitative claim (i)), and we also extract the
SLDR-related repair half-time from (a+c) for AGO1522 UF.
"""
import json, math, os
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(OUT, exist_ok=True)

# Table 1 parameters
params = {
    "AGO1522_MF": {"alpha0": 0.363, "beta0": 0.011, "a_plus_c": 0.034},
    "AGO1522_UF": {"alpha0": 0.388, "beta0": 0.081, "a_plus_c": 1.684},
    "DU145_MF"  : {"alpha0": 0.032, "beta0": 0.039, "a_plus_c": 2.509},
    "DU145_UF"  : {"alpha0": 0.022, "beta0": 0.041, "a_plus_c": 1.506},
}

# Acute LQ survival in [0, 6] Gy
doses = [0, 1, 2, 3, 4, 5, 6]
surv = {k: [round(math.exp(-(p["alpha0"]*D + p["beta0"]*D**2)), 4) for D in doses]
        for k,p in params.items()}

# Headline check (i): AGO1522 MF > UF in-field survival
ago_mf_survival_at_6Gy = surv["AGO1522_MF"][-1]
ago_uf_survival_at_6Gy = surv["AGO1522_UF"][-1]
mf_higher_than_uf = ago_mf_survival_at_6Gy > ago_uf_survival_at_6Gy

# Repair half-time from (a+c): t_1/2 = ln2/(a+c)
repair_half_h = {k: round(math.log(2)/p["a_plus_c"], 3) if p["a_plus_c"]>0 else None
                 for k,p in params.items()}

# Headline check (ii): SLDR rate reduced under MF vs UF for AGO1522
ago_sldr_reduced_mf_vs_uf = params["AGO1522_MF"]["a_plus_c"] < params["AGO1522_UF"]["a_plus_c"]

out = {
    "table1_params": params,
    "doses_Gy": doses,
    "LQ_survival": surv,
    "repair_t_half_h_from_aplusc": repair_half_h,
    "PASS_MF_survival_higher_than_UF_at_6Gy_AGO1522": bool(mf_higher_than_uf),
    "AGO1522_MF_survival_at_6Gy": ago_mf_survival_at_6Gy,
    "AGO1522_UF_survival_at_6Gy": ago_uf_survival_at_6Gy,
    "ratio_MF_over_UF_at_6Gy": round(ago_mf_survival_at_6Gy / ago_uf_survival_at_6Gy, 3),
    "paper_qualitative_claim_i": "MF in-field survival > UF in-field survival for the same delivered dose (AGO1522)",
    "PASS_SLDR_rate_reduced_under_MF_AGO1522": bool(ago_sldr_reduced_mf_vs_uf),
    "paper_qualitative_claim_ii": "SLDR importance reduced under MF exposure for AGO1522",
    "notes": "Acute LQ limit of IMK (Eq 1, N=1, T->0). Direct evaluation of Table 1 parameters; survival at large dose is the published-form check, not a refit. Intercellular-communication branch (alpha_b,beta_b,delta) not exercised here.",
}
with open(os.path.join(OUT, "lq_spotcheck.json"), "w") as f:
    json.dump(out, f, indent=2)

print(json.dumps(out, indent=2))
print("\nWrote:", os.path.join(OUT, "lq_spotcheck.json"))
