#!/usr/bin/env python3
"""Pass-2 claim test: CAZyme presence as a *proxy* (paper does not give CAZyme counts directly,
but Section 3.5 states "carbohydrate metabolism and transport (139)" CDS in core-genome
by eggNOG-mapperv2 functional class G.

We provide a FREE substitute using Pfam-A keyword matching on Prokka annotation product strings
for canonical CAZyme-family Pfam-like keywords. Caveats: this is a coarse proxy because
Prokka's UniProt-derived product strings are not as authoritative as dbCAN HMMER output,
but it provides ground-truth carbohydrate-activity gene COUNTS per genome for sanity-checking
the paper's COG-G claim.

Authoritative dbCAN run would need the dbCAN HMM database (not bundled in the env).
"""
import os, csv, re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022")
PROKKA = ROOT / "analysis" / "prokka"
OUT = ROOT / "results" / "repass"
OUT.mkdir(parents=True, exist_ok=True)

# CAZyme family keywords (covers glycoside hydrolases, glycosyltransferases, polysaccharide
# lyases, carbohydrate esterases, AA, CBM)
CAZ_KEYS = re.compile(
    r"glycos(?:ide hydrolase|yl transfera|yltransfera)|"
    r"glucos(?:idase|amine|yltransfera)|"
    r"galact(?:osidase|okinase|onate|oside)|"
    r"mannos(?:idase|yltransfera|e-6-phos)|"
    r"xylos|xylan|"
    r"fucos|fucoside|"
    r"sialid|neurami|"
    r"trehalo|"
    r"alpha-amylase|beta-amylase|amylase|"
    r"cellul(?:ase|ose)|"
    r"chitin|chitinase|"
    r"pectin|pectate lyase|polysaccharide lyase|"
    r"carbohydrate-binding|carbohydrate.binding|"
    r"hexose|pentose|"
    r"acetylgluc|UDP-glucose|UDP-N-acetyl|UDP-glucuron|"
    r"phosphoglyceromutase|"  # exclude later
    r"sugar transport|carbohydrate transport|"
    r"PTS system|EIIC|EIIB|EIIA",
    re.IGNORECASE
)
# Words that look CAZyme-ish but aren't (filter out)
NOT_CAZ = re.compile(r"phosphoglyceromutase|fructose-bisphosph|RNA glycos|tRNA", re.IGNORECASE)

rows = []
for d in sorted(PROKKA.iterdir()):
    if not d.is_dir(): continue
    s = d.name
    tsv = d / f"{s}.tsv"
    if not tsv.exists(): continue
    caz_total = 0
    caz_examples = []
    with open(tsv) as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 7: continue
            ftype = parts[1]
            product = parts[6] if len(parts) > 6 else ""
            if ftype != "CDS": continue
            if not product: continue
            if NOT_CAZ.search(product): continue
            if CAZ_KEYS.search(product):
                caz_total += 1
                if len(caz_examples) < 5:
                    caz_examples.append(product[:60])
    rows.append(dict(strain=s, caz_cds=caz_total, examples="|".join(caz_examples)))

# Write
with open(OUT / "cazyme_proxy_counts.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["strain","caz_cds","examples"], delimiter="\t")
    w.writeheader(); w.writerows(rows)

print(f"Strain       Carb.metab+transport CDS (proxy)")
print(f"-----------  ------------------------------")
n_total = 0
for r in rows:
    print(f"{r['strain']:12s} {r['caz_cds']:>4d}")
    n_total += r['caz_cds']
print(f"-----------")
print(f"Mean per-strain: {n_total/len(rows):.1f}")
print(f"Paper claim: core-genome COG-G = 139 CDS (carbohydrate metabolism + transport).")
print(f"This is a per-strain proxy, not a core-genome value; for direct comparison")
print(f"we would need to compute COG-G annotation on the Roary-derived core-genome FAA.")
