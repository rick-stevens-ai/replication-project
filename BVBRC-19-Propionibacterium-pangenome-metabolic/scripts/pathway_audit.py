#!/usr/bin/env python3
"""Audit specific metabolic-pathway claims from McCubbin et al. 2020 against the
authors' own GenBank annotations.

We scan each strain's per-CDS /function= and /note= and /product= text for the
enzymes the paper highlights, and tally presence per strain.

Claims we test (numbered for the report):
  M1 Methylmalonyl-CoA mutase (EC 5.4.99.16, the Wood-Werkman defining enzyme)
     "the only core functionality across all species"  -> expect: in all 6
  M2 Transaldolase (EC 2.2.1.2)
     "found in all genomes with the exception of P. avidum"  -> expect: 5/6, NOT PAVI
  M3 NADH-dependent L-lactate dehydrogenase (EC 1.1.1.27)
     "found in all strains"  -> expect: in all 6
  M4 Xylose isomerase or xylulokinase / xylose-degradation (EC 5.3.1.5 / 2.7.1.17)
     "ability to degrade xylose was only found in P. acidipropionici species"
     -> expect: PAC_4875 and PAC_55737 only
  M5 Sucrose-specific degradative capability (sucrose-6-P hydrolase 3.2.1.B3 / 3.2.1.26
     / 6-phosphosucrose fructohydrolase)
     "only observed in P. acidipropionici and P. propionicum"
     -> expect: PAC_4875, PAC_55737, PPRO only
  M6 Pyruvate:ferredoxin oxidoreductase (PFOR, EC 1.2.7.1) / nifJ
     paper knocks out nifJ1 in P. freudenreichii shermanii; "found in all propionibacteria
     studied" (the polyP-dependent variant is across all)  -> expect: in all 6 at minimum
"""
import re
import json
from pathlib import Path
from collections import defaultdict

GBK_DIR = Path("data/genbank/Genbank_files")
OUT = Path("report/evidence/pathway_audit.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

STRAINS = {
    "PAC_4875":  "Propionibacterium_acidipropionici_ATCC_4875.gbk",
    "PAC_55737": "Propionibacterium_acidipropionici_55737.gbk",
    "PSHE":      "Propionibacterium_freudenreichii_subsp._shermanii_CIRM-BIA1.gbk",
    "PAVI":      "Propionibacterium_avidum_44067.gbk",
    "PACN":      "Propionibacterium_acnes_6609.gbk",
    "PPRO":      "Propionibacterium_propionicum_F0230a.gbk",
}

# patterns for each claim — multiple synonyms; case-insensitive
CLAIM_PATTERNS = {
    "M1_methylmalonyl_CoA_mutase": [
        r"methylmalonyl[- ]?coa mutase", r"\b5\.4\.99\.[12]\b", r"\bmcm\b", r"methylmalonyl[- ]coenzyme a mutase",
    ],
    "M2_transaldolase": [
        r"transaldolase", r"\b2\.2\.1\.2\b", r"\btalA\b", r"\btalB\b",
    ],
    "M3_L_lactate_dehydrogenase": [
        r"\bl-?lactate dehydrogenase\b", r"\b1\.1\.1\.27\b", r"\bldh\b(?!-[a-z])",
    ],
    "M4_xylose_degradation": [
        r"xylose isomerase", r"\b5\.3\.1\.5\b",
        r"xylulokinase", r"xylulose kinase", r"\b2\.7\.1\.17\b",
        r"xylose abc", r"xylose transport", r"\bxylA\b", r"\bxylB\b",
    ],
    "M5_sucrose_degradation": [
        r"sucrose[- ]?6[- ]?phosphate hydrolase", r"sucrose-6-phosphate",
        r"sucrose hydrolase", r"\b3\.2\.1\.B3\b", r"\b3\.2\.1\.26\b",
        r"sucrose-6-p", r"fructohydrolase", r"sucrose phosphorylase", r"\b2\.4\.1\.7\b",
        r"\bscrB\b", r"\bsacA\b",
    ],
    "M6_pyruvate_ferredoxin_oxidoreductase": [
        r"pyruvate[- ]?ferredoxin oxidoreductase",
        r"pyruvate synthase",
        r"\b1\.2\.7\.1\b",
        r"\bporA\b", r"\bporB\b", r"\bnifJ\b",
    ],
}

# match-string is built from /function /note /product /gene fields per CDS
def cds_blocks(text):
    feat_re = re.compile(r"^ {5}(CDS)\s+([^\n]+)", re.M)
    starts = [(m.start(), m.end()) for m in feat_re.finditer(text)]
    feat_re_all = re.compile(r"^ {5}([A-Za-z_]+)\s+", re.M)
    all_starts = [m.start() for m in feat_re_all.finditer(text)]
    for s, _e in starts:
        # end = next feature start strictly after s
        nxt = next((x for x in all_starts if x > s), len(text))
        yield text[s:nxt]

def field(block, name):
    m = re.search(rf'/{name}="([^"]*)"', block, re.S)
    return re.sub(r"\s+", " ", m.group(1)) if m else ""

per_strain_hits = {tag: {c: [] for c in CLAIM_PATTERNS} for tag in STRAINS}
n_cds_per_strain = {}

for tag, fname in STRAINS.items():
    text = (GBK_DIR / fname).read_text()
    n = 0
    for block in cds_blocks(text):
        n += 1
        blob = " ".join([
            field(block, "function"),
            field(block, "note"),
            field(block, "product"),
            field(block, "gene"),
            field(block, "EC_number"),
        ]).lower()
        if not blob.strip():
            continue
        gene_or_loc = field(block, "gene") or field(block, "locus_tag") or field(block, "protein_id")
        for claim, pats in CLAIM_PATTERNS.items():
            for pat in pats:
                if re.search(pat, blob, re.I):
                    per_strain_hits[tag][claim].append({
                        "id": gene_or_loc,
                        "matched_pattern": pat,
                        "text": blob[:240],
                    })
                    break  # one hit per CDS per claim is enough
    n_cds_per_strain[tag] = n

# Summarize counts per claim per strain
summary = {"strains_cds_total": n_cds_per_strain, "claims": {}}
for claim in CLAIM_PATTERNS:
    summary["claims"][claim] = {
        tag: {
            "n_hits": len(per_strain_hits[tag][claim]),
            "ids": [h["id"] for h in per_strain_hits[tag][claim][:5]],
        }
        for tag in STRAINS
    }

# evaluate paper claims
expectations = {
    "M1_methylmalonyl_CoA_mutase":          {"present": list(STRAINS.keys()),                 "absent": []},
    "M2_transaldolase":                     {"present": [t for t in STRAINS if t!="PAVI"],    "absent": ["PAVI"]},
    "M3_L_lactate_dehydrogenase":           {"present": list(STRAINS.keys()),                 "absent": []},
    "M4_xylose_degradation":                {"present": ["PAC_4875","PAC_55737"],             "absent": ["PSHE","PAVI","PACN","PPRO"]},
    "M5_sucrose_degradation":               {"present": ["PAC_4875","PAC_55737","PPRO"],      "absent": ["PSHE","PAVI","PACN"]},
    "M6_pyruvate_ferredoxin_oxidoreductase":{"present": list(STRAINS.keys()),                 "absent": []},
}
verdicts = {}
for claim, exp in expectations.items():
    hits = {tag: summary["claims"][claim][tag]["n_hits"] for tag in STRAINS}
    ok_present = all(hits[t] >= 1 for t in exp["present"])
    ok_absent  = all(hits[t] == 0 for t in exp["absent"])
    verdicts[claim] = {
        "expected_present": exp["present"],
        "expected_absent":  exp["absent"],
        "observed_hits":    hits,
        "all_present_ok":   ok_present,
        "all_absent_ok":    ok_absent,
        "verdict":          "MATCH" if (ok_present and ok_absent) else "PARTIAL" if ok_present or ok_absent else "MISS",
    }

OUT.write_text(json.dumps({
    "n_cds_per_strain": n_cds_per_strain,
    "claims": summary["claims"],
    "verdicts": verdicts,
    "evidence_samples": {
        tag: {c: per_strain_hits[tag][c][:3] for c in CLAIM_PATTERNS}
        for tag in STRAINS
    },
}, indent=2))

print(f"\nWrote {OUT}\n")
print(f"{'CLAIM':45s} {'VERDICT':9s}  hits-per-strain")
for claim, v in verdicts.items():
    h = v["observed_hits"]
    h_str = " ".join(f"{t}={h[t]}" for t in STRAINS)
    print(f"{claim:45s} {v['verdict']:9s}  {h_str}")
