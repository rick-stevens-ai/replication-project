#!/bin/bash
set -euo pipefail

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate ralstonia

WORKDIR="$HOME/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021"
cd "$WORKDIR"

# Strain to SRR mapping
declare -A STRAIN_SRR
STRAIN_SRR[551632]=SRR11285251
STRAIN_SRR[551635]=SRR11285250
STRAIN_SRR[535634]=SRR11285249
STRAIN_SRR[535633]=SRR11285248
STRAIN_SRR[551633]=SRR11285247
STRAIN_SRR[535635]=SRR11285246
STRAIN_SRR[545260]=SRR11285245
STRAIN_SRR[545261]=SRR11285244
STRAIN_SRR[535638]=SRR11285243
STRAIN_SRR[543498]=SRR11285242
STRAIN_SRR[551634]=SRR11285241
STRAIN_SRR[551637]=SRR11285240
STRAIN_SRR[551636]=SRR11285239
STRAIN_SRR[551631]=SRR11285238
STRAIN_SRR[535637]=SRR11285237
STRAIN_SRR[543504]=SRR11285236
STRAIN_SRR[543514]=SRR11285235
STRAIN_SRR[535632]=SRR11285234

echo "=== Step 1: Download SRA reads ==="
mkdir -p data/sra
for strain in "${!STRAIN_SRR[@]}"; do
    srr="${STRAIN_SRR[$strain]}"
    if [ ! -f "data/sra/${srr}_1.fastq.gz" ]; then
        echo "Downloading $srr (strain $strain)..."
        fastq-dump --split-files --gzip --outdir data/sra "$srr" 2>&1 || echo "FAILED: $srr"
    else
        echo "Already have $srr"
    fi
done

echo "=== Step 2: Assemble with SPAdes ==="
mkdir -p data/genomes
for strain in "${!STRAIN_SRR[@]}"; do
    srr="${STRAIN_SRR[$strain]}"
    outdir="data/assemblies/${strain}"
    fasta="data/genomes/${strain}.fasta"
    if [ ! -f "$fasta" ]; then
        echo "Assembling strain $strain ($srr)..."
        mkdir -p "$outdir"
        spades.py --careful -1 "data/sra/${srr}_1.fastq.gz" -2 "data/sra/${srr}_2.fastq.gz" \
            -o "$outdir" -t 4 --memory 8 2>&1 | tail -3
        # Filter contigs >= 500 bp
        python3 -c "
from Bio import SeqIO
import sys
records = [r for r in SeqIO.parse('${outdir}/scaffolds.fasta', 'fasta') if len(r.seq) >= 500]
SeqIO.write(records, '${fasta}', 'fasta')
print(f'Strain ${strain}: {len(records)} contigs >= 500 bp')
" 2>&1
    else
        echo "Already have assembly for $strain"
    fi
done

echo "=== Pipeline Step 1-2 complete ==="
ls -la data/genomes/*.fasta 2>/dev/null | wc -l
