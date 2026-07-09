#!/usr/bin/env python3
"""
pangenome.py — Method-level replication of the pan-genome / core-genome estimate
of Bazinet (2017). The paper uses Prokka (annotation) + Roary (pan-genome).
Roary clusters proteins with CD-HIT + BLAST at (default) 95% identity and calls
a gene "core" if present in >=99% of taxa.

Here we use the NCBI-PGAP protein annotations (protein.faa, functionally the
Prokka step) and cluster them with CD-HIT at 95% identity across the B. cereus
sensu lato genomes only (outgroups excluded), then compute:
  - pan-genome size  = number of clusters (union of gene families)
  - core-genome size = clusters present in ALL genomes (100%) and >=99% taxa
  - a Heaps'-law-style accumulation curve (pan grows, core shrinks) as genomes
    are added -> qualitative match to the paper's open pan-genome finding.

Scaled to a small surrogate set (6 genomes), so absolute numbers are far below
the paper's 498-genome ~60,000-gene pan-genome; we test the METHOD and the
qualitative/relative claims (open pan-genome, few hundred core genes per genome
scale, core fraction).
"""
import sys, os, glob, subprocess, json, itertools
from collections import defaultdict

def load_bcsl_proteins(gdir, exclude_substr=("subtilis", "Clostridium")):
    """Concatenate protein.faa across B. cereus s.l. genomes, tag headers by acc."""
    rep = glob.glob(os.path.join(gdir, "**", "assembly_data_report.jsonl"), recursive=True)
    names = {}
    if rep:
        for line in open(rep[0]):
            d = json.loads(line); names[d["accession"]] = d.get("organism", {}).get("organismName", "")
    faas = sorted(glob.glob(os.path.join(gdir, "**", "protein.faa"), recursive=True))
    combined = []
    accs = []
    counts = {}
    for f in faas:
        acc = os.path.basename(os.path.dirname(f))
        org = names.get(acc, acc)
        if any(x.lower() in org.lower() for x in exclude_substr):
            continue
        accs.append(acc)
        n = 0
        for line in open(f):
            if line.startswith(">"):
                pid = line[1:].split()[0]
                combined.append(f">{acc}|{pid}\n")
                n += 1
            else:
                combined.append(line)
        counts[acc] = n
    return combined, accs, counts, names

def run_cdhit(in_faa, out_faa, ident=0.95):
    # word size per CD-HIT identity bands
    n = 5 if ident >= 0.7 else 4
    cmd = ["cd-hit", "-i", in_faa, "-o", out_faa, "-c", str(ident),
           "-n", str(n), "-M", "2000", "-T", "2", "-d", "0"]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_faa + ".clstr"

def parse_clusters(clstr_path):
    """Return list of clusters; each cluster = set of accessions present."""
    clusters = []
    cur = None
    for line in open(clstr_path):
        if line.startswith(">Cluster"):
            if cur is not None:
                clusters.append(cur)
            cur = []
        else:
            # ...>ACC|PID... 
            gt = line.split(">", 1)
            if len(gt) > 1:
                acc = gt[1].split("|")[0]
                cur.append(acc)
    if cur:
        clusters.append(cur)
    return clusters

def analyze(clusters, accs):
    Ntax = len(accs)
    presence = []  # per cluster: set of accs
    for c in clusters:
        presence.append(set(c))
    pan = len(presence)
    core100 = sum(1 for p in presence if len(p) == Ntax)
    core99 = sum(1 for p in presence if len(p) >= 0.99*Ntax)
    softcore95 = sum(1 for p in presence if len(p) >= 0.95*Ntax)
    shell = sum(1 for p in presence if 2 <= len(p) < 0.95*Ntax)
    cloud = sum(1 for p in presence if len(p) == 1)
    return dict(n_genomes=Ntax, pan=pan, core_100pct=core100,
                core_99pct=core99, softcore_95pct=softcore95,
                shell=shell, cloud_singletons=cloud,
                core_fraction=core100/pan if pan else 0)

def accumulation(clusters, accs, order=None):
    """Pan & core accumulation as genomes are added (single ordering)."""
    if order is None:
        order = list(accs)
    pan_curve, core_curve = [], []
    seen = set()
    # build per-cluster acc-set once
    csets = [set(c) for c in clusters]
    for i, a in enumerate(order, 1):
        seen.add(a)
        pan = sum(1 for cs in csets if cs & seen)
        core = sum(1 for cs in csets if seen <= cs)  # present in all seen so far
        pan_curve.append(pan); core_curve.append(core)
    return pan_curve, core_curve

def main(gdir, workdir, out_json):
    combined, accs, counts, names = load_bcsl_proteins(gdir)
    in_faa = os.path.join(workdir, "bcsl_all_proteins.faa")
    open(in_faa, "w").writelines(combined)
    print(f"B. cereus s.l. genomes used ({len(accs)}):")
    for a in accs:
        print(f"  {a}  {names.get(a,'')}  proteins={counts[a]}")
    total_prot = sum(counts.values())
    print(f"total input proteins: {total_prot}")
    out_faa = os.path.join(workdir, "bcsl_cdhit95.faa")
    clstr = run_cdhit(in_faa, out_faa, 0.95)
    clusters = parse_clusters(clstr)
    res = analyze(clusters, accs)
    pan_c, core_c = accumulation(clusters, accs)
    res["pan_accumulation"] = pan_c
    res["core_accumulation"] = core_c
    res["mean_genes_per_genome"] = total_prot / len(accs)
    print("\n=== Pan/core-genome (CD-HIT 95% identity) ===")
    for k, v in res.items():
        if "accum" not in k:
            print(f"  {k}: {v}")
    print(f"  pan accumulation:  {pan_c}")
    print(f"  core accumulation: {core_c}")
    json.dump(res, open(out_json, "w"), indent=2)
    print(f"\nwrote {out_json}")

if __name__ == "__main__":
    gdir = sys.argv[1] if len(sys.argv) > 1 else "genomes"
    workdir = sys.argv[2] if len(sys.argv) > 2 else "."
    out = sys.argv[3] if len(sys.argv) > 3 else "pangenome.json"
    main(gdir, workdir, out)
