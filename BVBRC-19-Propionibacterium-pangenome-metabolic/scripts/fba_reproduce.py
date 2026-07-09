#!/usr/bin/env python3
"""
Reproduce McCubbin et al. 2020 FBA-derived claims locally.

CLAIMS TESTED:
  C1. All 6 species' GEMs solve to a positive growth rate on the model's
      shipped (paper-shipped) medium → 'all models predict growth' (paper §
      "Reconstructions" + Table 1).
  C2. Glucose is the carbon source enabling growth (cpd00027). Removing
      glucose should abolish growth → confirms glucose dependency.
  C3. Propionate is produced as a major fermentation product (paper Discussion;
      'fermentative for propionate' and the paper's defining genus phenotype).
  C4. Auxotrophy contrast (Table 3): commensal P. acnes / P. avidum have MORE
      strict nutrient requirements than the dairy strains P. freudenreichii
      and P. acidipropionici. Operationally: count the open import (lb<0)
      exchanges in each model's shipped medium → commensals should have ≥ dairy.
  C5. P. propionicum requires UTP (cpd00062) and CTP (cpd00052) added
      externally per Table 3 → cpd00062 and/or cpd00052 should appear in its
      open intake set but NOT in the dairy strains'.
"""
import cobra, os, json, collections

base = "/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-19-Propionibacterium-pangenome-metabolic/data/PMC7650540/Final version of supplementary material/Supplementary file 4 S7/Model_XML_files/Model_XML_files/models"

species = collections.OrderedDict([
    ("P_freudenreichii_shermanii",  "P_sherm_model.xml"),
    ("P_acidipropionici_4875",      "PAC_4875_model.xml"),
    ("P_acidipropionici_55737",     "PAC_55737_model.xml"),
    ("P_acnes",                     "P_acnes_model.xml"),
    ("P_avidum",                    "P_avidum_model.xml"),
    ("P_propionicum",               "P_propionicum_model.xml"),
])

# ModelSEED compound ids of interest
CPD = {
    "glucose":      "cpd00027",
    "phosphate":    "cpd00009",
    "water":        "cpd00001",
    "NH3":          "cpd00013",
    "sulfate":      "cpd00048",
    "biotin":       "cpd00104",
    "pantothenate": "cpd00644",   # D-pantothenate
    "thiamin":      "cpd00305",
    "riboflavin":   "cpd00220",
    "B12_cobalamin":"cpd03424",   # vitamin B12 — note alternates exist
    "B12_alt":      "cpd01826",
    "UTP":          "cpd00062",
    "CTP":          "cpd00052",
    "ATP":          "cpd00002",
    "GTP":          "cpd00038",
    "propionate":   "cpd00141",
    "acetate":      "cpd00029",
    "lactate":      "cpd00159",   # L-lactate
    "succinate":    "cpd00036",
}

results = {}
print("=" * 90)
print("McCubbin 2020 GEM replication — FBA, glucose dependency, propionate, auxotrophy")
print("=" * 90)

dairy = {"P_freudenreichii_shermanii", "P_acidipropionici_4875", "P_acidipropionici_55737"}
commensal = {"P_acnes", "P_avidum"}
opportunist = {"P_propionicum"}

for name, fn in species.items():
    m = cobra.io.read_sbml_model(os.path.join(base, fn))
    res = {"file": fn, "rxns": len(m.reactions), "mets": len(m.metabolites)}
    # C1: default FBA
    s = m.optimize()
    res["growth_default"] = float(s.objective_value) if s.objective_value is not None else None
    # C2: knock out glucose
    glc_ex = next((r for r in m.reactions if CPD["glucose"] in r.id and r.id.startswith("Ex_")), None)
    if glc_ex:
        with m as mm:
            mm.reactions.get_by_id(glc_ex.id).lower_bound = 0.0
            s2 = mm.optimize()
            res["growth_no_glucose"] = float(s2.objective_value) if s2.objective_value is not None else None
    else:
        res["growth_no_glucose"] = "no_glucose_exchange"
    # C3: propionate secretion at optimum
    pro_ex = next((r for r in m.reactions if CPD["propionate"] in r.id and r.id.startswith("Ex_")), None)
    if pro_ex:
        with m as mm:
            s3 = mm.optimize()
            res["propionate_secretion"] = float(mm.reactions.get_by_id(pro_ex.id).flux) if s3.status=="optimal" else None
    else:
        res["propionate_secretion"] = "no_propionate_exchange"
    # other byproducts
    for tag,cid in [("acetate",CPD["acetate"]),("lactate",CPD["lactate"]),("succinate",CPD["succinate"])]:
        ex = next((r for r in m.reactions if cid in r.id and r.id.startswith("Ex_")), None)
        if ex and s.status == "optimal":
            with m as mm:
                ss = mm.optimize()
                res[f"{tag}_secretion"] = float(mm.reactions.get_by_id(ex.id).flux) if ss.status=="optimal" else None
        else:
            res[f"{tag}_secretion"] = None
    # C4: open intake exchanges = nutrient requirements signature
    intakes = sorted([r.id for r in m.reactions if r.id.startswith("Ex_") and r.lower_bound < 0])
    res["n_open_intakes"] = len(intakes)
    res["open_intakes"] = intakes
    # C5: check which vitamins/NTPs are required (in open intakes)
    flag = {}
    for tag, cid in CPD.items():
        in_intake = any(cid in r for r in intakes)
        flag[tag] = in_intake
    res["intake_flags"] = flag
    results[name] = res

# ---------- Pretty print ----------
print(f"\n{'species':30s} | {'μ (h-1)':>10s} | {'μ no-glc':>10s} | {'propionate':>11s} | {'acetate':>9s} | {'lactate':>9s} | {'#intakes':>8s}")
print("-" * 110)
for n, r in results.items():
    print(f"{n:30s} | {r['growth_default']:>10.4f} | {str(r['growth_no_glucose'])[:10]:>10s} | "
          f"{(r['propionate_secretion'] if isinstance(r['propionate_secretion'],float) else 0):>11.4f} | "
          f"{(r['acetate_secretion'] if isinstance(r['acetate_secretion'],float) else 0):>9.4f} | "
          f"{(r['lactate_secretion'] if isinstance(r['lactate_secretion'],float) else 0):>9.4f} | "
          f"{r['n_open_intakes']:>8d}")

print("\n--- C4: open-intake counts (proxy for auxotrophy strictness) ---")
print(f"  dairy mean      = {sum(results[n]['n_open_intakes'] for n in dairy)/len(dairy):.1f}")
print(f"  commensal mean  = {sum(results[n]['n_open_intakes'] for n in commensal)/len(commensal):.1f}")
print(f"  opportunist     = {results['P_propionicum']['n_open_intakes']}")

print("\n--- C5: vitamin / NTP intake flags ---")
header = ["species","biotin","pantothenate","thiamin","riboflavin","B12_cobalamin","B12_alt","UTP","CTP"]
print(" | ".join(f"{h:14s}" for h in header))
for n, r in results.items():
    row = [n[:14]] + [("Y" if r['intake_flags'][k] else "—") for k in header[1:]]
    print(" | ".join(f"{x:14s}" for x in row))

# Save raw json
out = "/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-19-Propionibacterium-pangenome-metabolic/report/evidence/fba_replication.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
def jclean(o):
    if isinstance(o,float): return o
    if isinstance(o,(list,tuple)): return [jclean(x) for x in o]
    if isinstance(o,dict): return {k:jclean(v) for k,v in o.items()}
    return o
with open(out,"w") as f:
    json.dump(jclean(results), f, indent=2)
print(f"\nWrote {out}")
