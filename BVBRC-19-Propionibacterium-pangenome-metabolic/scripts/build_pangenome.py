#!/usr/bin/env python3
"""Build a pangenome from the all-vs-all blastp using a simple OrthoMCL-style pipeline.

Filters (close to the McCubbin 2020 OMCL settings):
  - E-value <= 1e-5  (already from blast)
  - alignment coverage >= 75% of the SHORTER protein (paper used 75% coverage)
  - identity >= 30% (paper did not specify identity floor; we use 30% which is the
    standard OrthoMCL/Get_homologues default of "homology")
  - drop self-hits

Builds an MCL graph weighted by bit-score, runs MCL with inflation = 1.5 (paper's
"granularity parameter of 1.5") and writes one cluster per line: tab-sep gene IDs.

Then computes:
  - core (in all 6 strains)
  - softcore (in >=5 strains)
  - cloud / strain-specific singletons
  - per-strain singleton count
  - total cluster count (= pan-genome size)
  - per-genome accumulation curve (random permutation) for new clusters per genome added.

Compares against paper claims:
  - core: 792-906 clusters (paper Table — inter-species OMCL).
  - +553 new orthologous gene families per new species added (open pan-genome).
  - 4445 strain-specific clusters (~65% of pangenome) [from "S1, Additional file 1"].
"""
import sys
import json
import random
import subprocess
from pathlib import Path
from collections import defaultdict, Counter
from itertools import combinations

BLAST   = Path("data/blast/all_vs_all.tsv")
FAA     = Path("data/proteins/all_proteins.faa")
OUTDIR  = Path("data/pangenome"); OUTDIR.mkdir(parents=True, exist_ok=True)
EVID    = Path("report/evidence/pangenome.json")

MIN_ID  = 30.0
MIN_COV = 0.75
INFLATION = 1.5

STRAINS = ["PAC_4875","PAC_55737","PSHE","PAVI","PACN","PPRO"]


def parse_lengths():
    lengths = {}
    cur = None; seq = []
    with FAA.open() as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                if cur:
                    lengths[cur] = sum(map(len, seq))
                cur = line[1:].split()[0]
                seq = []
            else:
                seq.append(line)
        if cur:
            lengths[cur] = sum(map(len, seq))
    return lengths


def build_abc(lengths):
    """Read blast, filter, write MCL abc file."""
    abc = OUTDIR / "edges.abc"
    n_in = 0; n_out = 0
    # keep best bit-score per directed pair
    best = {}
    with BLAST.open() as f:
        for line in f:
            n_in += 1
            qid, sid, pid, alen, *_rest, evalue, bits = line.split()
            if qid == sid:
                continue
            pid = float(pid)
            if pid < MIN_ID:
                continue
            alen = int(alen)
            ql = lengths.get(qid); sl = lengths.get(sid)
            if not ql or not sl:
                continue
            cov = alen / min(ql, sl)
            if cov < MIN_COV:
                continue
            bits = float(bits)
            key = (qid, sid)
            if bits > best.get(key, 0):
                best[key] = bits
    # symmetrize: keep the min(forward, reverse) only if both present
    sym = {}
    for (a, b), bf in best.items():
        br = best.get((b, a))
        if br is None:
            continue
        if a < b:
            sym[(a, b)] = min(bf, br)
    with abc.open("w") as f:
        for (a, b), w in sym.items():
            f.write(f"{a}\t{b}\t{w:.2f}\n")
            n_out += 1
    print(f"blast lines in={n_in}  edges kept (sym pairs)={n_out}", flush=True)
    return abc, n_out


def run_mcl(abc):
    mci = OUTDIR / "edges.mci"
    tab = OUTDIR / "edges.tab"
    clust = OUTDIR / "clusters.txt"
    print("mcxload...", flush=True)
    subprocess.run(["mcxload","-abc",str(abc),
                    "--stream-mirror","--stream-neg-log10","-stream-tf","ceil(200)",
                    "-o",str(mci),"-write-tab",str(tab)], check=True)
    print(f"mcl with inflation={INFLATION}...", flush=True)
    subprocess.run(["mcl",str(mci),"-I",str(INFLATION),"-use-tab",str(tab),"-o",str(clust)], check=True)
    return clust


def analyze(clust_file):
    clusters = []
    singletons_in_clusters = set()
    with clust_file.open() as f:
        for line in f:
            members = line.strip().split("\t")
            if not members or members == [""]:
                continue
            clusters.append(members)
            for m in members:
                singletons_in_clusters.add(m)
    # add lonely genes (proteins not in any cluster) as singleton clusters
    all_proteins = set()
    with FAA.open() as f:
        for line in f:
            if line.startswith(">"):
                all_proteins.add(line[1:].split()[0])
    for p in all_proteins - singletons_in_clusters:
        clusters.append([p])

    # categorize
    n_per_strain = Counter()
    strain_of = lambda gid: gid.split("|",1)[0]
    cluster_strains = []
    for c in clusters:
        s = set(strain_of(g) for g in c)
        cluster_strains.append(s)
    n_pan = len(clusters)
    n_core = sum(1 for s in cluster_strains if s == set(STRAINS))
    n_softcore = sum(1 for s in cluster_strains if len(s) >= 5)
    n_shell = sum(1 for s in cluster_strains if 2 <= len(s) <= 4)
    n_cloud = sum(1 for s in cluster_strains if len(s) == 1)
    # strain-specific singletons (cluster with 1 gene, 1 strain)
    n_singleton_per_strain = Counter()
    for c, s in zip(clusters, cluster_strains):
        if len(c) == 1:
            n_singleton_per_strain[strain_of(c[0])] += 1
    # genes per strain
    n_genes_per_strain = Counter(strain_of(g) for c in clusters for g in c)

    # accumulation curve via 30 random orderings
    rng = random.Random(42)
    curves = []
    for _ in range(30):
        order = rng.sample(STRAINS, len(STRAINS))
        cumul = set()
        curve = []
        for i, st in enumerate(order, 1):
            for c_idx, s in enumerate(cluster_strains):
                if st in s and c_idx not in cumul:
                    cumul.add(c_idx)
            curve.append(len(cumul))
        curves.append(curve)
    # average increments
    avg_curve = [sum(c[i] for c in curves)/len(curves) for i in range(len(STRAINS))]
    increments = [avg_curve[0]] + [avg_curve[i]-avg_curve[i-1] for i in range(1, len(STRAINS))]

    # core/pan vs strains added (also avg over random orderings)
    pan_curve = avg_curve
    core_curves = []
    for _ in range(30):
        order = rng.sample(STRAINS, len(STRAINS))
        seen_strains = []
        core_curve = []
        for st in order:
            seen_strains.append(st)
            seen_set = set(seen_strains)
            nc = sum(1 for s in cluster_strains if seen_set.issubset(s))
            core_curve.append(nc)
        core_curves.append(core_curve)
    avg_core_curve = [sum(c[i] for c in core_curves)/len(core_curves) for i in range(len(STRAINS))]

    return {
        "n_pangenome_clusters":   n_pan,
        "n_core_in_all_6":        n_core,
        "n_softcore_in_5plus":    n_softcore,
        "n_shell_in_2to4":        n_shell,
        "n_cloud_strain_specific":n_cloud,
        "n_singletons_per_strain": dict(n_singleton_per_strain),
        "n_genes_per_strain":      dict(n_genes_per_strain),
        "pan_avg_curve":          pan_curve,
        "pan_avg_increments":     increments,
        "core_avg_curve":         avg_core_curve,
    }


def main():
    print("Reading protein lengths...", flush=True)
    lengths = parse_lengths()
    abc, n_edges = build_abc(lengths)
    clust = run_mcl(abc)
    print("Analyzing clusters...", flush=True)
    res = analyze(clust)
    res["filters"] = {"min_identity": MIN_ID, "min_coverage_of_shorter": MIN_COV,
                      "max_evalue": 1e-5, "mcl_inflation": INFLATION}
    res["n_edges_after_filter"] = n_edges

    # Compare to paper
    paper = {
        "core_in_all_strains_range": [792, 906],   # paper said 792-906
        "new_orthologs_per_new_species": 553,
        "strain_specific_clusters_inter": 4445,
        "strain_specific_fraction": 0.65,
    }
    inc_after_first = res["pan_avg_increments"][1:]   # increments for genome 2..6
    avg_increment = sum(inc_after_first)/len(inc_after_first) if inc_after_first else 0
    in_core_range = paper["core_in_all_strains_range"][0] <= res["n_core_in_all_6"] <= paper["core_in_all_strains_range"][1]
    # fraction strain-specific of pan
    frac_specific = res["n_cloud_strain_specific"] / res["n_pangenome_clusters"]

    res["paper_comparisons"] = {
        "P1_core_in_paper_range_792_to_906":     {"observed": res["n_core_in_all_6"], "in_range": in_core_range},
        "P2_avg_new_clusters_per_added_genome":  {"observed": round(avg_increment,1), "paper_value": 553},
        "P3_strain_specific_fraction":           {"observed": round(frac_specific,3), "paper_value": 0.65, "paper_count": 4445},
    }
    EVID.write_text(json.dumps(res, indent=2))
    print(f"\nWrote {EVID}")
    print(json.dumps({k: res[k] for k in ["n_pangenome_clusters","n_core_in_all_6","n_softcore_in_5plus","n_shell_in_2to4","n_cloud_strain_specific","n_singletons_per_strain","pan_avg_curve","pan_avg_increments","core_avg_curve","paper_comparisons"]}, indent=2))


if __name__ == "__main__":
    main()
