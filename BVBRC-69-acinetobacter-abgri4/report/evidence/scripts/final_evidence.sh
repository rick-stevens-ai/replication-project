#!/usr/bin/env bash
# Consolidated evidence bundle.
set -eo pipefail
set +u; source ~/env.sh || true; set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH
BASE=/data/stevens/bvbrc69-abgri4

# Extract the pseudogene α/β-hydrolase (EP550_07220) fragment and the full-length
# α/β-hydrolase from ABUH796 (both), then BLAST both against AB0057 to check
# whether the target-site α/β-hydrolase + azoreductase are adjacent in AB0057.
/data/stevens/envs/bvbrc14/bin/python << 'PY'
from Bio import SeqIO
rec = next(SeqIO.parse(f"/data/stevens/bvbrc69-abgri4/genomes/ABUH796/CP035043.gbk","genbank"))
# EP550_07220 (α/β-hydrolase pseudo, 1515737..1516111) — flanks integron 5' side
# EP550_07290 (FMN-NADH-azoreductase pseudo, 1524268..1524576) — flanks integron 3' side
# ABUH796 AbGRI4 is 1515737..1524576
# The two flanking pseudogene fragments (nucleotide, from CP035043)
lo1,hi1 = 1515737, 1516111  # α/β-hydrolase fragment (5' flank)
lo2,hi2 = 1524268, 1524576  # azoreductase fragment (3' flank)
with open("/data/stevens/bvbrc69-abgri4/results/verify/flanks_nt.fna","w") as fh:
    fh.write(f">EP550_07220_alphabeta_hydrolase_5flank CP035043:{lo1}-{hi1}\n")
    fh.write(str(rec.seq[lo1-1:hi1])+"\n")
    fh.write(f">EP550_07290_FMN_azoreductase_3flank CP035043:{lo2}-{hi2}\n")
    fh.write(str(rec.seq[lo2-1:hi2])+"\n")

# Also grab the near-full-length α/β-hydrolase copy from elsewhere in ABUH796 chromosome for reference
# and a full-length azoreductase
fullhits=[]
for f in rec.features:
    if f.type!="CDS": continue
    prod=f.qualifiers.get("product",[""])[0]
    if "alpha/beta fold hydrolase" in prod or "FMN-dependent NADH-azoreductase" in prod:
        s,e = int(f.location.start), int(f.location.end)
        # skip the two pseudogene fragments
        if (s,e) in [(1515736,1516111),(1524267,1524576)]:  # 0-based
            continue
        fullhits.append((prod, s, e, f.location.strand))

with open("/data/stevens/bvbrc69-abgri4/results/verify/full_hydrolases_and_azoreductases.tsv","w") as fh:
    fh.write("product\tstart\tend\tstrand\tlen\n")
    for prod,s,e,st in fullhits:
        fh.write(f"{prod}\t{s}\t{e}\t{st}\t{e-s}\n")
print(f"Found {len(fullhits)} intact copies of α/β-hydrolase or FMN-NADH-azoreductase elsewhere in the chromosome (these are unrelated paralogs)")
PY

echo ""
echo "=== BLAST the two pseudogene flanks (5' α/β-hydrolase + 3' azoreductase) against AB0057 ==="
# If adjacent in AB0057 (i.e. the intact target-site pair), we'd expect the two flank hits at very close positions
makeblastdb -in $BASE/refgenomes/CP001182.fna -dbtype nucl -out $BASE/refgenomes/CP001182_db -logfile /dev/null 2>&1
blastn -query $BASE/results/verify/flanks_nt.fna -db $BASE/refgenomes/CP001182_db \
  -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue" \
  -evalue 1e-30 -perc_identity 90 2>/dev/null | sort -k1,1 -k9g,9g | head -20

echo ""
echo "=== Same on ATCC 17978 (CP000521) ==="
makeblastdb -in $BASE/refgenomes/CP000521.fna -dbtype nucl -out $BASE/refgenomes/CP000521_db -logfile /dev/null 2>&1
blastn -query $BASE/results/verify/flanks_nt.fna -db $BASE/refgenomes/CP000521_db \
  -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue" \
  -evalue 1e-30 -perc_identity 90 2>/dev/null | sort -k1,1 -k9g,9g | head -20

echo ""
echo "=== Check IS26 presence via annotation: how many IS26 copies flank/surround the AbGRI4 ==="
/data/stevens/envs/bvbrc14/bin/python << 'PY'
from Bio import SeqIO
for strain,acc in [("ABUH763","CP035051"),("ABUH793","CP035045"),("ABUH796","CP035043")]:
    rec = next(SeqIO.parse(f"/data/stevens/bvbrc69-abgri4/genomes/{strain}/{acc}.gbk","genbank"))
    is26=0
    for f in rec.features:
        if f.type!="CDS": continue
        prod=f.qualifiers.get("product",[""])[0]
        if "IS26 family transposase" in prod or "IS6-like element IS26" in prod:
            is26+=1
    print(f"{strain} {acc}: total IS26 CDS on chromosome = {is26}")
PY
