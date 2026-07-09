#!/bin/bash
eval "$(/home/stevens/bin/micromamba shell hook -s bash)"
cd /data/stevens/bvbrc93-kpneu-st1588-independent
micromamba activate amr
blastn -query UCO361_all_contigs.fasta -db pfinder_db -perc_identity 60 \
  -outfmt "6 qseqid sseqid pident length qlen slen qstart qend sstart send evalue bitscore" \
  -out pfinder_hits.tsv 2>&1

echo "=== All hits (identity>=60%) ==="
column -t pfinder_hits.tsv | head -40

echo
echo "=== PF-standard threshold: >=95% id, >=60% ref cov ==="
awk 'BEGIN{OFS="\t"; print "contig","replicon","pident","pcov","slen"}
     $3>=95 && ($4/$6)*100>=60 {printf "%s\t%s\t%.2f\t%.1f\t%d\n",$1,$2,$3,($4/$6)*100,$6}' pfinder_hits.tsv | column -t

echo
echo "=== Per contig hit counts (all >=60%) ==="
awk '{print $1}' pfinder_hits.tsv | sort | uniq -c
