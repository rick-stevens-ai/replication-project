#!/usr/bin/env python3
"""Independent grep of PGAP GFF for the report's headline gene claims."""
import re, json, sys
from collections import Counter, defaultdict
from pathlib import Path

GFF = Path(sys.argv[1])

# Categories from report; each is a case-insensitive regex over product/gene fields
CATS = {
    "GAD_gadB": r"\bglutamate decarboxylase\b|\bgadB\b",
    "GAD_gadC_transporter": r"glutamate/gamma-aminobutyrate|glutamate/GABA antiporter|\bgadC\b",
    "L-LDH": r"L-lactate dehydrogenase",
    "D-LDH_specific": r"\bD-lactate dehydrogenase\b",
    "D-2-hydroxyacid_DH": r"D-2-hydroxyacid dehydrogenase",
    "BSH_choloylglycine": r"choloylglycine hydrolase|bile salt hydrolase|\bbsh\b",
    "sortase_A": r"sortase (A|class A)",
    "LPXTG_anchor": r"LPXTG",
    "enolase": r"\benolase\b",
    "efTu": r"elongation factor Tu|\btuf\b",
    "cold_shock": r"cold[-\s]shock",
    "GroEL": r"chaperonin GroL|\bgroL\b|GroEL|60 kDa chaperonin",
    "GroES": r"co-chaperonin GroS|\bgroS\b|GroES|10 kDa chaperonin",
    "DnaK": r"\bdnaK\b|DnaK|molecular chaperone DnaK",
    "DnaJ": r"\bdnaJ\b|DnaJ",
    "GrpE": r"\bgrpE\b|GrpE|nucleotide exchange factor GrpE",
    "trpA": r"tryptophan synthase (subunit alpha|alpha chain)|\btrpA\b",
    "trpB": r"tryptophan synthase (subunit beta|beta chain)|\btrpB\b",
    "trpC": r"indole-3-glycerol[- ]phosphate synthase|\btrpC\b",
    "trpD": r"anthranilate phosphoribosyltransferase|\btrpD\b",
    "trpE": r"anthranilate synthase (component I|subunit alpha)|\btrpE\b",
    "fibronectin_binding": r"fibronectin[- ]binding|Rqc2",
    "riboflavin_ribH_ribD": r"riboflavin synthase|riboflavin biosynthesis|\bribH\b|\bribD\b",
    "thiamine_thiT_thiM": r"thiamine|\bthiT\b|\bthiM\b|\bthiF\b|hydroxyethylthiazole",
    "biotin": r"biotin[-\s]|\bbioY\b|\bbioB\b|\baccB\b|biotin ligase",
    "folate": r"folate|\bfolA\b|\bfolC\b|\bfolD\b|dihydrofolate reductase|formate--tetrahydrofolate",
    "pyridoxal_B6": r"pyridoxal|pyridoxine|\bpdxK\b|pyridox",
    "CTP_synthase_pyrG": r"CTP synthase|\bpyrG\b",
    "F0F1_ATP_synthase": r"F0F1|ATP synthase (F0|F1)",
    "GlcN-6-P_deaminase": r"glucosamine-6-phosphate deaminase",
    "IS_transposase": r"transposase",
    "IS6_family": r"IS6 family transposase",
    "IS3_family": r"IS3 family transposase",
    "IS982_family": r"IS982 family transposase",
    "IS5_family": r"IS5 family transposase",
    "IS4_family": r"IS4 family transposase|IS1675",
    "Cas_protein": r"CRISPR-associated|\bCas\d\b|\bcas\d\b",
    "bacteriocin": r"bacteriocin|lactococcin|lantibiotic|enterolysin",
    "sortase_class_C": r"sortase (C|class C)",
    "RepB_plasmid": r"RepB|Rep protein|replication (initiator|initiation)",
    "mobilization": r"mobilization|mobilisation|\bmob\b|conjugative transfer|relaxase",
    "polyketide": r"polyketide synthase|PKS",
    "alpha_amylase": r"alpha-amylase|α-amylase",
    "lipase_esterase": r"\blipase\b|esterase|\blip\b",
    "serine_protease": r"serine (protease|peptidase)",
    "lacA_gal6P_isomerase": r"galactose-6-phosphate isomerase.*(subunit A|alpha)|\blacA\b",
    "lacB_gal6P_isomerase": r"galactose-6-phosphate isomerase.*(subunit B|beta)|\blacB\b",
    "lacC_tagatose_kinase": r"tagatose[-\s]6-phosphate kinase|\blacC\b",
    "lacD_tagatose_aldolase": r"tagatose[-\s]1,6-bisphosphate aldolase|\blacD\b",
    "lacG_pbetagal": r"6-phospho-beta-galactosidase|\blacG\b",
    "beta_galactosidase": r"beta-galactosidase|β-galactosidase",
    "aminoglycoside_intrinsic": r"aminoglycoside",
}

hits = defaultdict(list)
lines = GFF.read_text().splitlines()
for line in lines:
    if not line or line.startswith("#"): continue
    p = line.split("\t")
    if len(p) < 9: continue
    if p[2] not in {"CDS", "gene", "pseudogene", "rRNA", "tRNA"}: continue
    attrs = dict(kv.split("=",1) for kv in p[8].split(";") if "=" in kv)
    product = attrs.get("product","")
    gene = attrs.get("gene","")
    name = attrs.get("Name","")
    haystack = " | ".join([product, gene, name])
    seq = p[0]
    for cat, pat in CATS.items():
        if re.search(pat, haystack, flags=re.IGNORECASE):
            hits[cat].append({"contig": seq, "product": product, "gene": gene, "type": p[2]})

# Deduplicate by (contig, product, gene) so pseudogene+CDS rows for same locus count once
def dedup(rows):
    seen = set(); out = []
    for r in rows:
        k = (r["contig"], r["product"], r["gene"])
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

summary = {cat: {"n_dedup": len(dedup(rows)), "n_raw": len(rows)} for cat,rows in hits.items()}
print(json.dumps({"summary": summary, "detail_first3": {c: hits[c][:3] for c in hits}}, indent=2))
