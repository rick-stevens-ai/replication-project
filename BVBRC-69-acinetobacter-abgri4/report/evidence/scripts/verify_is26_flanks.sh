#!/usr/bin/env bash
# 1) Confirm IS26 flanks
# 2) Confirm flanking α/β-hydrolase (EP550_07220) & FMN-NADH-azoreductase (EP550_07290)
# 3) Confirm all 3 AbGRI4 regions are identical (or nearly so)
set -eo pipefail
set +u; source ~/env.sh || true; set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH

BASE=/data/stevens/bvbrc69-abgri4
cd $BASE
mkdir -p results/verify

# IS26 reference from NCBI: efetch nucleotide X00011 (IS26 in Tn6, ~820 bp) or use tnpA gene AAA98209
if [[ ! -s results/verify/IS26.fna ]]; then
  # Fetch tnpA (IS26 transposase) protein from a canonical IS26 record
  # IS26 tnpA protein is 234 aa; nucleotide IS26 canonical is HM749966 or similar. Use J01730 X00011 as fallback.
  efetch -db nuccore -id "HM749966.1" -format fasta 2>/dev/null > results/verify/IS26.fna || true
  if [[ ! -s results/verify/IS26.fna ]]; then
    efetch -db nuccore -id "X00011.1" -format fasta > results/verify/IS26.fna
  fi
fi
head -1 results/verify/IS26.fna
wc -c results/verify/IS26.fna

echo "=== IS26 BLAST on AbGRI4 regions ==="
for s in ABUH763 ABUH793 ABUH796; do
  fa=results/abgri4/${s}_AbGRI4.fna
  makeblastdb -in $fa -dbtype nucl -out results/verify/${s}_db -logfile /dev/null 2>&1
  echo "-- $s --"
  blastn -db results/verify/${s}_db -query results/verify/IS26.fna \
    -outfmt "6 qseqid sseqid pident length mismatch qstart qend sstart send evalue bitscore" \
    -evalue 1e-30 -perc_identity 90 2>/dev/null | sort -k7,7n
done

echo ""
echo "=== Test identity of AbGRI4 regions across the 3 strains ==="
# Multi-sequence FASTA + pairwise stretcher
cat results/abgri4/ABUH763_AbGRI4.fna results/abgri4/ABUH793_AbGRI4.fna results/abgri4/ABUH796_AbGRI4.fna > results/verify/three_AbGRI4.fna
# ABUH793 is on rev strand per paper; test rev-complementing it and compare to ABUH796
/data/stevens/envs/bvbrc14/bin/python << 'PY'
from Bio import SeqIO
recs = list(SeqIO.parse('/data/stevens/bvbrc69-abgri4/results/abgri4/ABUH763_AbGRI4.fna','fasta'))
rec763 = recs[0]
rec793 = next(SeqIO.parse('/data/stevens/bvbrc69-abgri4/results/abgri4/ABUH793_AbGRI4.fna','fasta'))
rec796 = next(SeqIO.parse('/data/stevens/bvbrc69-abgri4/results/abgri4/ABUH796_AbGRI4.fna','fasta'))
# ABUH793 was reverse-oriented in paper — test both
rc793 = rec793.seq.reverse_complement()
s763 = str(rec763.seq); s793f = str(rec793.seq); s793r = str(rc793); s796 = str(rec796.seq)
def hamming_and_lengths(a,b):
    if len(a)!=len(b): return None, (len(a),len(b))
    return sum(x!=y for x,y in zip(a,b)), (len(a),len(b))
print("ABUH763 vs ABUH796:", hamming_and_lengths(s763, s796))
print("ABUH763 vs ABUH793 (as-is):", hamming_and_lengths(s763, s793f))
print("ABUH763 vs ABUH793 (rev-comp):", hamming_and_lengths(s763, s793r))
print("ABUH796 vs ABUH793 (rev-comp):", hamming_and_lengths(s796, s793r))
PY
