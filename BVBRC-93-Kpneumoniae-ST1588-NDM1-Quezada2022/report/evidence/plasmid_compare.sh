#!/bin/bash
eval "$(/home/stevens/bin/micromamba shell hook -s bash)"
cd /data/stevens/bvbrc93-kpneu-st1588-independent
micromamba activate amr

# Extract only the pNDM-1 plasmid contig (NZ_JAMJQY010000002.1) for direct comparison
python3 -c "
seqs={}; name=None; buf=[]
for l in open('UCO361_all_contigs.fasta'):
    if l.startswith('>'):
        if name: seqs[name]=''.join(buf)
        name=l[1:].split()[0]; buf=[]
    else: buf.append(l.strip())
if name: seqs[name]=''.join(buf)
with open('pNDM1_UCO361_only.fasta','w') as f:
    f.write('>pNDM1_UCO361_NZ_JAMJQY010000002.1\n'+seqs['NZ_JAMJQY010000002.1']+'\n')
print('extracted', len(seqs['NZ_JAMJQY010000002.1']),'bp')
"

# BLAST pNDM1_UCO361 vs pNDM1-EC12 (MN598004)
makeblastdb -in pNDM1_EC12_MN598004.fasta -dbtype nucl -out ec12_db 2>&1 | tail -2
blastn -query pNDM1_UCO361_only.fasta -db ec12_db -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -out blast_vs_EC12.tsv 2>&1
echo "=== pNDM-1_UCO361 vs pNDM-1-EC12 (MN598004) — paper claim: common region ~2488 bp ==="
echo "Total HSPs: $(wc -l < blast_vs_EC12.tsv)"
echo "HSPs sorted by length desc:"
sort -k4 -n -r blast_vs_EC12.tsv | head -10 | column -t
echo ""
echo "Sum of aligned length (>=90% id): "
awk '$3>=90 {s+=$4} END {print s, "bp"}' blast_vs_EC12.tsv
echo "Longest single HSP: "
sort -k4 -n -r blast_vs_EC12.tsv | head -1 | awk '{print "  length="$4" bp  pident="$3"%  qspan="$7"-"$8"  sspan="$9"-"$10}'

# BLAST pNDM1_UCO361 vs pRAO166a (CP041388) — paper claim: "different genetic environment"
makeblastdb -in Rornith_megaplasmid_CP041388.fasta -dbtype nucl -out rornith_db 2>&1 | tail -2
blastn -query pNDM1_UCO361_only.fasta -db rornith_db -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -out blast_vs_Rornith.tsv 2>&1
echo ""
echo "=== pNDM-1_UCO361 vs pRAO166a (CP041388) — paper: 'different genetic environment' ==="
echo "Total HSPs: $(wc -l < blast_vs_Rornith.tsv)"
echo "HSPs sorted by length desc (top 10):"
sort -k4 -n -r blast_vs_Rornith.tsv | head -10 | column -t
echo "Sum of aligned length (>=90% id): "
awk '$3>=90 {s+=$4} END {print s, "bp"}' blast_vs_Rornith.tsv
