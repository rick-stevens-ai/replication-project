#!/usr/bin/env python3
"""Second pass: for each primer pair, fetch ALL transcripts for the gene
from Ensembl and try to find a forward + reverse-complement match.

Many qPCR designs span exon junctions in the canonical isoform; a
forward-only hit + reverse-only hit (separated) on the *unspliced* genomic
sequence with a small intron skip is the usual case. This script just
checks if any transcript carries both primers in cis.
"""
import json, os, time, urllib.request, urllib.error

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "qpcr_amplicon_audit.json")
IN  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "qpcr_primer_audit.json")

def rev_comp(s):
    return s.translate(str.maketrans("ACGTacgt","TGCAtgca"))[::-1]

def ensembl_get(url, accept="application/json", timeout=20):
    req = urllib.request.Request(url, headers={"Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode()
            return json.loads(data) if accept == "application/json" else data
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        return None

def main():
    with open(IN) as f:
        prev = json.load(f)
    out = []
    for rec in prev["audit"]:
        gene = rec["gene"]
        ensid = rec.get("ensembl_id")
        fwd = rec["forward"]
        rrc = rev_comp(rec["reverse"])
        result = {"gene": gene, "ensembl_id": ensid, "transcripts_checked": 0, "amplicon_hits": []}
        if not ensid:
            out.append(result)
            continue
        # List transcripts via overlap endpoint
        url = f"https://rest.ensembl.org/overlap/id/{ensid}?feature=transcript;content-type=application/json"
        ts = ensembl_get(url)
        time.sleep(0.4)
        if not ts:
            out.append(result)
            continue
        for t in ts:
            tid = t.get("transcript_id") or t.get("id")
            if not tid:
                continue
            result["transcripts_checked"] += 1
            seq = ensembl_get(f"https://rest.ensembl.org/sequence/id/{tid}?type=cdna", accept="text/x-fasta")
            time.sleep(0.4)
            if not seq:
                continue
            cdna = "".join(line.strip() for line in seq.splitlines() if not line.startswith(">")).upper()
            f_idx = cdna.find(fwd)
            r_idx = cdna.find(rrc)
            if f_idx >= 0 and r_idx >= 0 and r_idx > f_idx:
                amp = r_idx + len(rrc) - f_idx
                result["amplicon_hits"].append({
                    "transcript": tid,
                    "amplicon_len_bp": amp,
                    "fwd_pos": f_idx,
                    "rev_rc_pos": r_idx,
                })
        out.append(result)
        n = len(result["amplicon_hits"])
        print(f"[gene] {gene:8s}  transcripts={result['transcripts_checked']:2d}  amplicons_found={n}", flush=True)

    summary = {
        "n_genes": len(out),
        "n_with_amplicon_in_any_transcript": sum(1 for r in out if r["amplicon_hits"]),
    }
    with open(OUT, "w") as f:
        json.dump({"per_gene": out, "summary": summary}, f, indent=2)
    print("[summary]", json.dumps(summary, indent=2))
    print(f"[saved] {OUT}")

if __name__ == "__main__":
    main()
