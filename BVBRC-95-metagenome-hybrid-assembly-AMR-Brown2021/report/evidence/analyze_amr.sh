#!/bin/bash
set -eu
cd /data/stevens/BVBRC-95/work
python3 <<'PY'
import os, json, csv
from collections import defaultdict, Counter

# 1) Load assembly stats
stats = {}
with open('assembly_stats.jsonl') as f:
    for line in f:
        d = json.loads(line)
        stats[d['assembler']] = d

# 2) Load AMR results  
assemblers = ['Megahit','metaSpades','IDBA-UD','HybridSpades','Canu','Flye','OPERA-MS']
amr = {}
for a in assemblers:
    path = f'amr_out/{a}.1kb.amr.tsv'
    rows = list(csv.DictReader(open(path), delimiter='\t'))
    amr[a] = rows

# 3) Load contig lengths per assembler
contig_lens = {}
for a, acc_name in [('Megahit','SRR12664619'),('metaSpades','SRR13105837'),
                    ('IDBA-UD','SRR12664620'),('HybridSpades','SRR12664586'),
                    ('Canu','SRR12664608'),('Flye','SRR12664575'),('OPERA-MS','SRR12664597')]:
    fa = f'assemblies/{acc_name}.1kb.fa'
    lens = {}
    with open(fa) as f:
        name, seq = None, []
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                if name is not None:
                    lens[name] = len(''.join(seq))
                name = line[1:].split()[0]
                seq = []
            else:
                seq.append(line)
        if name is not None:
            lens[name] = len(''.join(seq))
    contig_lens[a] = lens

# 4) Per-assembler ARG summary + ARG-carrying contig lengths
summary = []
per_arg = defaultdict(dict)  # arg -> {assembler: count}
for a in assemblers:
    rows = amr[a]
    n_arg = len(rows)
    arg_names = Counter(r.get('Gene symbol') for r in rows)
    # ARG-carrying contigs
    contig_col = 'Contig id'
    contigs_with_arg = set(r.get(contig_col) for r in rows if r.get(contig_col))
    # length distribution of these contigs
    lens_of_arg_contigs = [contig_lens[a].get(c, None) for c in contigs_with_arg]
    lens_of_arg_contigs = [L for L in lens_of_arg_contigs if L]
    if lens_of_arg_contigs:
        lens_of_arg_contigs.sort()
        n = len(lens_of_arg_contigs)
        median_len = lens_of_arg_contigs[n//2]
        mean_len = sum(lens_of_arg_contigs)/n
        max_len = max(lens_of_arg_contigs)
        ge10k = sum(1 for L in lens_of_arg_contigs if L>=10000)
        ge50k = sum(1 for L in lens_of_arg_contigs if L>=50000)
    else:
        median_len=mean_len=max_len=ge10k=ge50k=0
    summary.append(dict(
        assembler=a,
        n_arg_hits=n_arg,
        n_unique_arg_symbols=len(arg_names),
        n_arg_carrying_contigs=len(contigs_with_arg),
        median_arg_contig_bp=median_len,
        mean_arg_contig_bp=int(mean_len),
        max_arg_contig_bp=max_len,
        arg_contigs_ge_10kb=ge10k,
        arg_contigs_ge_50kb=ge50k,
        assembly_n_contigs_1kb=stats[a]['ge_1kb'],
        assembly_total_bp=stats[a]['total_bp'],
        assembly_n50=stats[a]['n50'],
        assembly_max_len=stats[a]['max_len'],
    ))
    for g, c in arg_names.items():
        per_arg[g][a] = c

# 5) Print summary table
print("=== BVBRC-95: USA-1-influent sample, 7 assemblers, AMRFinder+ v3.12.8 (2024-07-22 DB), contigs >=1kb ===")
print()
hdr = ['assembler','n_arg','n_uniq','arg_contigs','med_arg_bp','max_arg_bp','arg_ctg>=10k','arg_ctg>=50k','asm_ctg>=1k','asm_N50']
fmt = "{:14s} {:>6s} {:>7s} {:>12s} {:>11s} {:>11s} {:>13s} {:>13s} {:>12s} {:>8s}"
print(fmt.format(*hdr))
for s in summary:
    print(fmt.format(s['assembler'], str(s['n_arg_hits']), str(s['n_unique_arg_symbols']),
                     str(s['n_arg_carrying_contigs']), str(s['median_arg_contig_bp']),
                     str(s['max_arg_contig_bp']), str(s['arg_contigs_ge_10kb']),
                     str(s['arg_contigs_ge_50kb']), str(s['assembly_n_contigs_1kb']),
                     str(s['assembly_n50'])))

# 6) ARG symbol overlap (Jaccard between assemblers)
arg_sets = {a: set(g for g,c in per_arg.items() if a in c) for a in assemblers}
print()
print("=== ARG SYMBOL OVERLAP (Jaccard) ===")
print("             " + " ".join(f"{a[:11]:>11s}" for a in assemblers))
for a in assemblers:
    row = [f"{a[:11]:11s}"]
    for b in assemblers:
        u = arg_sets[a] | arg_sets[b]
        i = arg_sets[a] & arg_sets[b]
        j = len(i)/len(u) if u else 0
        row.append(f"{j:>11.3f}")
    print(" ".join(row))

# 7) Save JSON evidence
with open('summary.json','w') as f:
    json.dump(dict(assembly_stats=stats, amr_summary=summary), f, indent=2)
with open('arg_symbols_by_assembler.json','w') as f:
    json.dump({a: sorted(arg_sets[a]) for a in assemblers}, f, indent=2)

# 8) Correlation short-read vs long-read vs hybrid ARG SYMBOL SETS
def js(A,B): u=A|B; return len(A&B)/len(u) if u else 0
short = ['Megahit','metaSpades','IDBA-UD']
long = ['Canu','Flye']
hybrid = ['HybridSpades','OPERA-MS']
print()
print("=== ARG-symbol Jaccard among CATEGORIES (mean pairwise) ===")
def cat_mean(cat):
    pairs = [(a,b) for i,a in enumerate(cat) for b in cat[i+1:]]
    if not pairs: return None
    return sum(js(arg_sets[a],arg_sets[b]) for a,b in pairs)/len(pairs)
print(f"within short  : {cat_mean(short):.3f}")
print(f"within long   : {cat_mean(long):.3f}")
print(f"within hybrid : {cat_mean(hybrid):.3f}")
# cross
def cross_mean(c1,c2):
    pairs=[(a,b) for a in c1 for b in c2]
    return sum(js(arg_sets[a],arg_sets[b]) for a,b in pairs)/len(pairs)
print(f"short vs hybrid: {cross_mean(short,hybrid):.3f}")
print(f"short vs long : {cross_mean(short,long):.3f}")
print(f"hybrid vs long: {cross_mean(hybrid,long):.3f}")
PY
