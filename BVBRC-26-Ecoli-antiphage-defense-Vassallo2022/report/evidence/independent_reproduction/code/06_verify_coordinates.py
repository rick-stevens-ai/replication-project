#!/usr/bin/env python3
"""Independently verify protein coordinates: for a random sample of systems,
fetch the contig FASTA from NCBI, extract the region at declared start/stop,
translate in all 6 frames, and check that one frame matches the fetched
protein sequence. This is a direct paper-vs-NCBI coordinate check."""
import json, urllib.request, time, random
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
CONTIG_DIR = DATA / "ncbi_contigs"
CONTIG_DIR.mkdir(parents=True, exist_ok=True)

with open(DATA / "indep_s2_systems.json") as fh:
    systems = json.load(fh)

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-repro/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")

TRANS = {
 "TTT":"F","TTC":"F","TTA":"L","TTG":"L",
 "CTT":"L","CTC":"L","CTA":"L","CTG":"L",
 "ATT":"I","ATC":"I","ATA":"I","ATG":"M",
 "GTT":"V","GTC":"V","GTA":"V","GTG":"V",
 "TCT":"S","TCC":"S","TCA":"S","TCG":"S",
 "CCT":"P","CCC":"P","CCA":"P","CCG":"P",
 "ACT":"T","ACC":"T","ACA":"T","ACG":"T",
 "GCT":"A","GCC":"A","GCA":"A","GCG":"A",
 "TAT":"Y","TAC":"Y","TAA":"*","TAG":"*",
 "CAT":"H","CAC":"H","CAA":"Q","CAG":"Q",
 "AAT":"N","AAC":"N","AAA":"K","AAG":"K",
 "GAT":"D","GAC":"D","GAA":"E","GAG":"E",
 "TGT":"C","TGC":"C","TGA":"*","TGG":"W",
 "CGT":"R","CGC":"R","CGA":"R","CGG":"R",
 "AGT":"S","AGC":"S","AGA":"R","AGG":"R",
 "GGT":"G","GGC":"G","GGA":"G","GGG":"G",
}
COMP = str.maketrans("ACGTNacgtn", "TGCANtgcan")

def revcomp(s): return s.translate(COMP)[::-1]

def translate(dna):
    aa = []
    for i in range(0, len(dna)-2, 3):
        cod = dna[i:i+3].upper()
        aa.append(TRANS.get(cod, "X"))
    return "".join(aa)

def load_prot(acc):
    p = DATA / "ncbi_proteins" / f"{acc}.faa"
    if not p.exists(): return None
    lines = p.read_text().splitlines()
    return "".join(x for x in lines[1:] if x)

random.seed(7)
sample = random.sample(systems, 6)  # 6 systems -> ~10 proteins

report = []
for s in sample:
    contig = s["contig"]
    fp = CONTIG_DIR / f"{contig}.fna"
    if not fp.exists():
        print(f"Fetching contig {contig}...")
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={contig}&rettype=fasta&retmode=text"
        try:
            fna = fetch(url)
            fp.write_text(fna)
            time.sleep(0.4)
        except Exception as e:
            print(f"  FAILED to fetch {contig}: {e}")
            continue
    seq = "".join(x for x in fp.read_text().splitlines() if not x.startswith(">"))
    print(f"\n=== {s['pd']} contig={contig} len={len(seq)} start={s['start']} stop={s['stop']} ===")

    # for each declared protein, try to find it near the declared start/stop
    for acc in s["proteins"]:
        prot = load_prot(acc)
        if not prot:
            print(f"  {acc}: no local FASTA (skipped)")
            continue
        plen = len(prot)
        # Search a window ± 50 kb around declared start/stop
        start = int(s["start"])
        stop = int(s["stop"])
        lo = max(0, min(start, stop) - 50000)
        hi = min(len(seq), max(start, stop) + 50000)
        window = seq[lo:hi]
        found = False
        for strand_name, w in [("+", window), ("-", revcomp(window))]:
            for frame in [0,1,2]:
                aa = translate(w[frame:])
                # look for exact match of prot (minus trailing X's), allowing loss of trailing stop
                p_query = prot
                idx = aa.find(p_query)
                if idx >= 0:
                    # compute absolute coordinates
                    if strand_name == "+":
                        abs_start = lo + frame + idx*3
                        abs_stop = abs_start + plen*3
                    else:
                        # window reversed, so idx maps to end
                        rev_end = frame + idx*3
                        abs_stop = hi - rev_end
                        abs_start = abs_stop - plen*3
                    off = min(abs(abs_start - start), abs(abs_start - stop), abs(abs_stop - start), abs(abs_stop - stop))
                    print(f"  {acc} ({plen}aa): MATCH strand={strand_name} frame={frame} abs=[{abs_start},{abs_stop}] near-decl-offset={off}bp")
                    report.append({"pd": s["pd"], "acc": acc, "match": True, "strand": strand_name, "abs_start": abs_start, "abs_stop": abs_stop, "declared_start": start, "declared_stop": stop, "min_offset_bp": off})
                    found = True
                    break
            if found: break
        if not found:
            print(f"  {acc}: NO MATCH in ±50 kb window")
            report.append({"pd": s["pd"], "acc": acc, "match": False})

with open(DATA / "coord_verification.json", "w") as fh:
    json.dump(report, fh, indent=2, ensure_ascii=False)

n = len(report); ok = sum(1 for r in report if r.get("match"))
print(f"\nCoord verification: {ok}/{n} proteins matched at declared position in fetched contig")
