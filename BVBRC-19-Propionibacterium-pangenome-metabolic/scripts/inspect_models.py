#!/usr/bin/env python3
"""Inspect McCubbin 2020 Propionibacterium GEMs and run FBA sanity checks."""
import cobra
import os, sys

base = "/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-19-Propionibacterium-pangenome-metabolic/data/PMC7650540/Final version of supplementary material/Supplementary file 4 S7/Model_XML_files/Model_XML_files/models"

species = {
    "P_freudenreichii_shermanii":  "P_sherm_model.xml",
    "P_acidipropionici_4875":      "PAC_4875_model.xml",
    "P_acidipropionici_55737":     "PAC_55737_model.xml",
    "P_acnes":                     "P_acnes_model.xml",
    "P_avidum":                    "P_avidum_model.xml",
    "P_propionicum":               "P_propionicum_model.xml",
}

print("=== McCubbin 2020 Propionibacterium GEMs — load + structure ===\n")
for name, fn in species.items():
    path = os.path.join(base, fn)
    if not os.path.exists(path):
        print(f"MISSING {name}: {path}"); continue
    m = cobra.io.read_sbml_model(path)
    print(f"{name}: rxns={len(m.reactions)}, mets={len(m.metabolites)}, genes={len(m.genes)}, objective={m.objective.expression}")
    # Default FBA (model's own medium)
    try:
        s = m.optimize()
        print(f"   default-FBA: status={s.status}  obj={s.objective_value:.6f}" if s.objective_value is not None else f"   default-FBA: status={s.status}")
    except Exception as e:
        print(f"   default-FBA ERROR: {e}")
    # find biomass-ish reaction
    bms = [r for r in m.reactions if 'biomass' in r.id.lower() or 'biomass' in (r.name or '').lower() or r.id.lower().startswith('bio')]
    print(f"   biomass-like rxns: {[r.id for r in bms][:5]}")
    # find exchange reactions and currently open intake bounds
    ex = [r for r in m.reactions if r.id.startswith('EX_') or len(r.metabolites)==1]
    intake = [(r.id, r.lower_bound) for r in ex if r.lower_bound < 0]
    print(f"   exchanges total={len(ex)} | open intakes (lb<0)={len(intake)} | sample={intake[:6]}")
    print()
