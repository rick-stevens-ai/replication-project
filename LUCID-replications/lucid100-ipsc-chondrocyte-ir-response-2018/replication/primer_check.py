"""
Verify primer sequences in S6 Table by BLAST-like local checks:
  - Sanity: 18-24 nt, primer GC content reasonable, no obvious errors
  - For each gene, expected human transcript: search the primer 5'-3' sequence
    against the canonical RefSeq mRNA via NCBI Entrez (free; no rate-limit
    concern for 8 queries).
"""
import urllib.request, urllib.parse, json, time, re

# Manually transcribed from S6
primers = [
    ("BRCA2","F","cctgatgcctgtacacctctt"),
    ("BRCA2","R","gcaggccgagtactgttagc"),
    ("RAD51","F","atcactaatcaggtggtagctcaa"),
    ("RAD51","R","cccctcttcctttcctcaga"),
    ("PRKDC","F","agaggctgggagcatcact"),
    ("PRKDC","R","caccaaggcttcaaacacaa"),
    ("XRCC4","F","tggtgaactgagaaaagcattg"),
    ("XRCC4","R","tgaaggaaccaagtctgaatga"),
]

def gc(s):
    s=s.upper()
    return 100*(s.count("G")+s.count("C"))/len(s)

print("Primer sanity checks:")
print(f"{'gene':8} {'dir':4} {'len':4} {'GC%':6} {'seq'}")
for g,d,s in primers:
    print(f"{g:8} {d:4} {len(s):4d} {gc(s):6.1f} {s}")

# Search each primer against NCBI nucleotide database via the official esearch+efetch
# but a faster check: use BLAST? overkill. Instead, fetch the canonical RefSeq
# mRNA for each gene and substring-search.
REFSEQ = {
    "BRCA2": "NM_000059",
    "RAD51": "NM_002875",
    "PRKDC": "NM_006904",
    "XRCC4": "NM_022406",
}

import socket
socket.setdefaulttimeout(20)

def fetch_refseq(acc):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={acc}&rettype=fasta&retmode=text"
    req = urllib.request.Request(url, headers={"User-Agent":"replication-audit/1.0"})
    try:
        with urllib.request.urlopen(req) as r:
            text = r.read().decode()
        # strip header + newlines
        lines = text.splitlines()
        return "".join(l for l in lines if not l.startswith(">"))
    except Exception as e:
        return None

def revcomp(s):
    comp = str.maketrans("ACGTacgt","TGCAtgca")
    return s.translate(comp)[::-1]

print("\nBLAST-style match against canonical RefSeq mRNA:")
results = []
for gene, acc in REFSEQ.items():
    seq = fetch_refseq(acc)
    time.sleep(0.4)
    if seq is None:
        print(f"  {gene} ({acc}): FETCH FAILED")
        continue
    print(f"  {gene} ({acc}): {len(seq)} nt fetched")
    for g, d, p in primers:
        if g != gene: continue
        p_up = p.upper()
        # Forward primers should match the sense strand; reverse should match the antisense (i.e. its revcomp matches sense)
        if d == "F":
            hit = p_up in seq.upper()
            note = "exact F match in sense"
        else:
            target = revcomp(p_up)
            hit = target in seq.upper()
            note = "revcomp(R) match in sense"
        amplicon = ""
        # If both primers hit, compute amplicon length
        results.append({"gene":gene,"dir":d,"hit":hit,"note":note})
        print(f"     {gene} {d} ({p}): hit={hit}  [{note}]")

# Amplicon-length sanity per gene
print("\nAmplicon length per gene:")
for gene, acc in REFSEQ.items():
    seq = fetch_refseq(acc)
    if seq is None: continue
    seq = seq.upper()
    F = next(p for g,d,p in primers if g==gene and d=="F").upper()
    R = next(p for g,d,p in primers if g==gene and d=="R").upper()
    Rc = revcomp(R)
    if F in seq and Rc in seq:
        i = seq.find(F)
        j = seq.find(Rc, i)
        if j > i:
            amp = j + len(Rc) - i
            print(f"  {gene}: amplicon = {amp} nt (F at {i}, R-rc at {j})")
        else:
            print(f"  {gene}: F at {i}, R-rc at {seq.find(Rc)} (R-rc upstream of F or only present elsewhere)")
    else:
        print(f"  {gene}: F_hit={F in seq}  Rc_hit={Rc in seq}")
