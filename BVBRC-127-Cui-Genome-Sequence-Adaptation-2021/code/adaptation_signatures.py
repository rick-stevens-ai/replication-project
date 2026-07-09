#!/usr/bin/env python3
"""
adaptation_signatures.py — method-level SPOT-CHECK of the reproducible core of a
bacterial "genome sequence adaptation" comparative-genomics study (Cui 2021,
exact paper not uniquely identifiable from the shell — see report caveat).

We quantify the classic GENOMIC SIGNATURES OF ADAPTATION that any such study
computes, on a small public surrogate contrasting free-living generalists vs
host-restricted / host-adapted lineages (where genome reduction, GC/AT shift,
and altered codon-usage bias are textbook adaptation hallmarks):

  free-living generalists : E. coli K-12, Pseudomonas putida KT2440
  host-adapted / restricted: Salmonella Typhi, Mycobacterium tuberculosis,
                             Buchnera aphidicola (obligate endosymbiont, extreme
                             genome reduction)
  generalist reference     : Salmonella Typhimurium

Signatures computed per genome:
  - genome size (bp), GC%
  - protein-coding gene count, mean protein length, coding density proxy
  - codon usage bias: ENC (effective number of codons, Wright 1990) from CDS-
    derived proteins is not directly possible from protein.faa, so we compute
    amino-acid usage entropy + GC-driven codon expectation and, where nucleotide
    CDS are extractable, GC3-style bias. Here we use genome GC and amino-acid
    composition bias as adaptation proxies.

Testable expectation (from the adaptation literature):
  host-restricted/reduced genomes -> smaller genome, fewer genes, often lower GC
  (Buchnera extreme), reduced coding repertoire -> a clear multivariate
  separation of adaptation state from raw genome statistics.

Free tools: pure Python + Biopython. Small & fast.
"""
import sys, os, glob, json, math
from collections import Counter

CATEGORY = {
    "GCF_000005845.2": ("E. coli K-12", "free-living"),
    "GCF_000007565.2": ("P. putida KT2440", "free-living"),
    "GCF_000006945.2": ("S. Typhimurium LT2", "generalist"),
    "GCF_000007545.1": ("S. Typhi Ty2", "host-restricted"),
    "GCF_000195955.2": ("M. tuberculosis H37Rv", "host-adapted"),
    "GCF_000009605.1": ("Buchnera aphidicola", "obligate-endosymbiont"),
}

def genome_stats(fna):
    from Bio import SeqIO
    total = 0; gc = 0; ncontig = 0
    for r in SeqIO.parse(fna, "fasta"):
        s = str(r.seq).upper()
        total += len(s)
        gc += s.count("G") + s.count("C")
        ncontig += 1
    return total, gc/total if total else 0, ncontig

def protein_stats(faa):
    from Bio import SeqIO
    lengths = []
    aa = Counter()
    for r in SeqIO.parse(faa, "fasta"):
        s = str(r.seq).replace("*", "")
        lengths.append(len(s))
        aa.update(s)
    n = len(lengths)
    total_aa = sum(aa.values())
    # amino-acid usage Shannon entropy (bits); lower = more biased usage
    H = 0.0
    for c, cnt in aa.items():
        if c in "ACDEFGHIKLMNPQRSTVWY" and cnt > 0:
            p = cnt/total_aa
            H -= p*math.log2(p)
    Hmax = math.log2(20)
    return dict(n_proteins=n,
                mean_prot_len=sum(lengths)/n if n else 0,
                total_aa=total_aa,
                aa_entropy_bits=H,
                aa_entropy_norm=H/Hmax)

def main(gdir, out_json):
    accdirs = sorted(glob.glob(os.path.join(gdir, "GCF_*")))
    rows = []
    for d in accdirs:
        acc = os.path.basename(d)
        fna = glob.glob(os.path.join(d, "*.fna"))
        faa = os.path.join(d, "protein.faa")
        if not fna:
            continue
        size, gcf, ncontig = genome_stats(fna[0])
        ps = protein_stats(faa) if os.path.exists(faa) else {}
        name, cat = CATEGORY.get(acc, (acc, "unknown"))
        coding_density = (ps.get("total_aa", 0)*3) / size if size else 0
        row = dict(acc=acc, name=name, category=cat,
                   genome_bp=size, gc_pct=round(100*gcf, 2), n_contigs=ncontig,
                   n_proteins=ps.get("n_proteins"),
                   mean_prot_len=round(ps.get("mean_prot_len", 0), 1),
                   coding_density=round(coding_density, 3),
                   aa_entropy_norm=round(ps.get("aa_entropy_norm", 0), 4),
                   genes_per_mbp=round(ps.get("n_proteins", 0)/(size/1e6), 1) if size else 0)
        rows.append(row)
    # print table
    hdr = ["name","category","genome_bp","gc_pct","n_proteins","genes_per_mbp","coding_density","mean_prot_len","aa_entropy_norm"]
    print(f"{'name':<22}{'category':<22}{'Mbp':>7}{'GC%':>7}{'genes':>7}{'g/Mbp':>7}{'cod.den':>8}{'protlen':>8}{'aaH':>7}")
    for r in sorted(rows, key=lambda x: -x["genome_bp"]):
        print(f"{r['name']:<22}{r['category']:<22}{r['genome_bp']/1e6:7.2f}{r['gc_pct']:7.1f}"
              f"{r['n_proteins']:7d}{r['genes_per_mbp']:7.1f}{r['coding_density']:8.3f}"
              f"{r['mean_prot_len']:8.1f}{r['aa_entropy_norm']:7.4f}")
    # simple adaptation-state separation: rank by genome size & gene count
    free = [r for r in rows if r["category"] in ("free-living","generalist")]
    adap = [r for r in rows if r["category"] in ("host-restricted","host-adapted","obligate-endosymbiont")]
    def mean(xs,k): return sum(x[k] for x in xs)/len(xs) if xs else 0
    summary = dict(
        free_living_mean_Mbp=round(mean(free,"genome_bp")/1e6,3),
        adapted_mean_Mbp=round(mean(adap,"genome_bp")/1e6,3),
        free_living_mean_genes=round(mean(free,"n_proteins"),0),
        adapted_mean_genes=round(mean(adap,"n_proteins"),0),
        free_living_mean_gc=round(mean(free,"gc_pct"),2),
        adapted_mean_gc=round(mean(adap,"gc_pct"),2),
    )
    print("\n=== adaptation-state contrast (free/generalist vs host-adapted/reduced) ===")
    for k,v in summary.items(): print(f"  {k}: {v}")
    json.dump({"rows": rows, "summary": summary}, open(out_json,"w"), indent=2)
    print(f"\nwrote {out_json}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "allgenomes",
         sys.argv[2] if len(sys.argv)>2 else "adaptation.json")
