#!/bin/bash
set -euo pipefail

eval "$(conda shell.bash hook)"
conda activate ralstonia

WORKDIR="$HOME/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021"
cd "$WORKDIR"

# All 18 strains with SRR accessions
STRAINS=(
"551632:SRR11285251"
"551635:SRR11285250"
"535634:SRR11285249"
"535633:SRR11285248"
"551633:SRR11285247"
"535635:SRR11285246"
"545260:SRR11285245"
"545261:SRR11285244"
"535638:SRR11285243"
"543498:SRR11285242"
"551634:SRR11285241"
"551637:SRR11285240"
"551636:SRR11285239"
"551631:SRR11285238"
"535637:SRR11285237"
"543504:SRR11285236"
"543514:SRR11285235"
"535632:SRR11285234"
)

echo "=== STEP 1: Download SRA reads ==="
mkdir -p data/sra
for entry in "${STRAINS[@]}"; do
    strain="${entry%%:*}"
    srr="${entry##*:}"
    if [ -f "data/sra/${srr}_1.fastq.gz" ] && [ -f "data/sra/${srr}_2.fastq.gz" ]; then
        echo "  Already have $srr (strain $strain)"
        continue
    fi
    echo "  Downloading $srr (strain $strain)..."
    cd data/sra
    fasterq-dump "$srr" --split-files --threads 4 2>&1 | tail -1 || echo "WARN: fasterq-dump failed for $srr, trying fastq-dump"
    # Compress if not already
    for f in ${srr}_1.fastq ${srr}_2.fastq; do
        [ -f "$f" ] && gzip "$f"
    done
    cd "$WORKDIR"
done
echo "Downloaded reads: $(ls data/sra/*_1.fastq.gz 2>/dev/null | wc -l) pairs"

echo "=== STEP 2: Assemble with SPAdes ==="
mkdir -p data/genomes data/assemblies
for entry in "${STRAINS[@]}"; do
    strain="${entry%%:*}"
    srr="${entry##*:}"
    fasta="data/genomes/${strain}.fasta"
    if [ -f "$fasta" ]; then
        echo "  Already assembled strain $strain"
        continue
    fi
    echo "  Assembling strain $strain..."
    outdir="data/assemblies/${strain}"
    mkdir -p "$outdir"
    spades.py --careful \
        -1 "data/sra/${srr}_1.fastq.gz" \
        -2 "data/sra/${srr}_2.fastq.gz" \
        -o "$outdir" -t 4 --memory 8 2>&1 | tail -3
    
    # Filter contigs >= 500 bp with >= 10x coverage
    python3 -c "
from Bio import SeqIO
records = []
for r in SeqIO.parse('${outdir}/scaffolds.fasta', 'fasta'):
    if len(r.seq) >= 500:
        # Parse coverage from header (e.g., NODE_1_length_X_cov_Y)
        cov = float(r.description.split('cov_')[1]) if 'cov_' in r.description else 0
        if cov >= 10:
            records.append(r)
SeqIO.write(records, '${fasta}', 'fasta')
total_len = sum(len(r.seq) for r in records)
print(f'  Strain ${strain}: {len(records)} contigs, {total_len} bp total')
" 2>&1
done
echo "Assembled genomes: $(ls data/genomes/*.fasta 2>/dev/null | wc -l)"

echo "=== STEP 3: Compute genome statistics ==="
python3 << 'PYSTATS'
from Bio import SeqIO
import os, glob

genomes = sorted(glob.glob("data/genomes/*.fasta"))
print(f"{'Strain':<12} {'Contigs':>8} {'Total_bp':>12} {'GC%':>8} {'N50':>10}")
for gf in genomes:
    strain = os.path.basename(gf).replace('.fasta','')
    records = list(SeqIO.parse(gf, 'fasta'))
    lengths = sorted([len(r.seq) for r in records], reverse=True)
    total = sum(lengths)
    gc_count = sum(str(r.seq).upper().count('G') + str(r.seq).upper().count('C') for r in records)
    gc_pct = gc_count / total * 100 if total > 0 else 0
    # N50
    cumul = 0
    n50 = 0
    for l in lengths:
        cumul += l
        if cumul >= total/2:
            n50 = l
            break
    print(f"{strain:<12} {len(records):>8} {total:>12,} {gc_pct:>8.2f} {n50:>10,}")
PYSTATS

echo "=== Pipeline Steps 1-3 complete ==="
