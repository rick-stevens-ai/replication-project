#!/usr/bin/env bash
# Independent reproduction of BVBRC-27 (Egan et al. 2020) — subagent, 2026-07-03.
# Re-runs the report's computational core from scratch with a DIFFERENT tool
# (abricate v1.4.0) instead of the report's raw blastn-against-AMRFinderPlus_CDS.
# Free public NCBI Datasets/E-utilities only.
#
# Reproduces:
#   C1: AMR gene screen (optrA/poxtA/cfr(D)/fexA/erm(B)/tet(M)/tet(L)/ant(9)-Ia)
#   C2: MN831410 vs pE394 (KP399637) full-length identity
#   C3: MN831411 vs MN831412 shared poxtA-IS1216E cassette + 21849 bp size
#   C4: optrA nt-diff variant table vs canonical NG_048023
# Out of reach (deposited data limit): C5 (22.7% prevalence), C6 (cgMLST/wgMLST/STs),
# C7 (23S G2576T). All require raw reads never deposited.
set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
DL="$BASE/downloads"
LOG="$BASE/logs"
mkdir -p "$DL" "$LOG"

ACCS=(MN831410 MN831411 MN831412 MN831413 MN831414 MN831415 MN831416 MN831417 MN831418 MN831419)

# 1) Fresh downloads from NCBI E-utilities (free, no auth)
cd "$DL"
for a in "${ACCS[@]}"; do
  curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${a}&rettype=fasta&retmode=text" -o "${a}.fasta"
  curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${a}&rettype=gb&retmode=text" -o "${a}.gb"
  sleep 0.4
done
curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=KP399637&rettype=fasta&retmode=text" -o "pE394_KP399637.fasta"
curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NG_048023&rettype=fasta&retmode=text" -o "optrA_NG_048023.fasta"

# 2) Log lengths + SHA256s
: > "$LOG/seq_lengths.tsv"
for a in "${ACCS[@]}" pE394_KP399637; do
  python3 - "$a" <<'PY' >> "$LOG/seq_lengths.tsv"
import sys
from Bio import SeqIO
acc=sys.argv[1]
r=next(SeqIO.parse(f'{acc}.fasta','fasta'))
print(f"{acc}\t{len(r.seq)}\t{r.description}")
PY
done
shasum -a 256 *.fasta *.gb > "$LOG/downloads.sha256"

# 3) C1: independent AMR screen with abricate (NCBI + ResFinder cross-check)
abricate --db ncbi      --minid 80 --mincov 60 --quiet "${ACCS[@]/%/.fasta}" > "$LOG/abricate_ncbi.tsv"      2> "$LOG/abricate_ncbi.stderr"
abricate --db resfinder --minid 80 --mincov 60 --quiet "${ACCS[@]/%/.fasta}" > "$LOG/abricate_resfinder.tsv" 2> "$LOG/abricate_resfinder.stderr"

# 4) C2: MN831410 vs pE394 full-length BLAST
makeblastdb -in pE394_KP399637.fasta -dbtype nucl -out pE394_db >/dev/null
blastn -query MN831410.fasta -db pE394_db \
  -outfmt "6 qseqid sseqid pident length qlen slen mismatch gapopen evalue bitscore" \
  > "$LOG/c2_mn831410_vs_pE394.tsv"

# 5) C3: MN831411 vs MN831412 shared blocks + poxtA/IS1216E feature parse
makeblastdb -in MN831412.fasta -dbtype nucl -out MN831412_db >/dev/null
blastn -query MN831411.fasta -db MN831412_db \
  -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue bitscore" \
  | awk '$4 >= 500' > "$LOG/c3_poxtA_shared_blocks.tsv"

# 6) C4: extract optrA CDS from each GenBank + blast vs canonical NG_048023
python3 - <<'PY'
from Bio import SeqIO
records={}
for acc in ['MN831410','MN831411','MN831412','MN831413','MN831414','MN831415','MN831416','MN831417','MN831418','MN831419']:
    rec=next(SeqIO.parse(f'{acc}.gb','genbank'))
    for f in rec.features:
        if f.type=='CDS' and f.qualifiers.get('gene',[''])[0].lower()=='optra':
            records[acc]=str(f.extract(rec.seq)); break
with open('optra_cds_all.fasta','w') as fh:
    for a,s in records.items(): fh.write(f'>{a}_optrA\n{s}\n')
PY
makeblastdb -in optrA_NG_048023.fasta -dbtype nucl -out optrA_db >/dev/null
blastn -query optra_cds_all.fasta -db optrA_db \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen qlen slen" \
  > "$LOG/c4_optrA_vs_canonical.tsv"

echo "Done. See $LOG/ for all outputs."
