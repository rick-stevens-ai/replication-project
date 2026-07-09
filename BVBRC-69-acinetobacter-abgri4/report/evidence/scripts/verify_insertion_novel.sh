#!/usr/bin/env bash
# Verify novel insertion site: the α/β-hydrolase + azoreductase gene pair should be
# ADJACENT (uninterrupted) in a reference A. baumannii genome (e.g. ATCC 17978 CP000521,
# ACICU CP000863, AB0057 CP001182, or A118 CP021782).
# Paper Table 1 also lists "AB0057" (CP001182) and "AB994" (CP003856) - use those as controls.
set -eo pipefail
set +u; source ~/env.sh || true; set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH

BASE=/data/stevens/bvbrc69-abgri4
cd $BASE
mkdir -p refgenomes

# Reference genomes: AB0057 (paper's own comparator) + ATCC 17978 (canonical ref)
for acc in CP001182 CP000521; do
  if [[ ! -s refgenomes/${acc}.fna ]]; then
    efetch -db nuccore -id "$acc" -format fasta > refgenomes/${acc}.fna
    ls -la refgenomes/${acc}.fna
  fi
done

# Extract the flanking α/β-hydrolase and azoreductase proteins from ABUH796 GBK, use tblastn
/data/stevens/envs/bvbrc14/bin/python << 'PY'
from Bio import SeqIO
gbk = "/data/stevens/bvbrc69-abgri4/genomes/ABUH796/CP035043.gbk"
rec = next(SeqIO.parse(gbk, "genbank"))
targets = ("alpha/beta fold hydrolase", "FMN-dependent NADH-azoreductase")
with open("/data/stevens/bvbrc69-abgri4/results/verify/flank_prots.faa","w") as out:
    for f in rec.features:
        if f.type != "CDS": continue
        prod = f.qualifiers.get("product",["-"])[0]
        s,e = int(f.location.start), int(f.location.end)
        if any(t in prod for t in targets):
            # Include only ones flanking AbGRI4 (positions ~1.5 Mb)
            if 1500000 <= s <= 1540000:
                trans = f.qualifiers.get("translation",[""])[0]
                if trans:
                    out.write(f">{prod.replace(' ','_')}_{s}_{e} strand={f.location.strand}\n{trans}\n")
                    print(prod, s, e, len(trans), "aa")
PY

echo ""
echo "=== tblastn flanking proteins against AB0057 (paper comparator) and ATCC 17978 ==="
for acc in CP001182 CP000521; do
  echo "-- $acc --"
  makeblastdb -in refgenomes/${acc}.fna -dbtype nucl -out refgenomes/${acc}_db -logfile /dev/null 2>&1
  tblastn -db refgenomes/${acc}_db -query results/verify/flank_prots.faa \
    -outfmt "6 qseqid sseqid pident length qlen sstart send evalue" \
    -evalue 1e-30 2>/dev/null | sort -k7,7n | head -20
done

echo ""
echo "=== Also BLAST full AbGRI4 region against AB0057 ==="
# Paper: AbGRI4 is absent from AB0057 (comparator strain). Any hit >1 kb indicates presence.
for acc in CP001182 CP000521; do
  echo "-- AbGRI4 vs $acc --"
  blastn -query results/abgri4/ABUH796_AbGRI4.fna -db refgenomes/${acc}_db \
    -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue" \
    -evalue 1e-30 -perc_identity 90 2>/dev/null | awk '$4>=200' | head -10
done
