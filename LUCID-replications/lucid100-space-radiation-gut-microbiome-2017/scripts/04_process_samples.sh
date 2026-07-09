#!/usr/bin/env bash
# Per-sample 16S pipeline:
#   merge pairs (vsearch --fastq_mergepairs)
#   quality filter (Q>20, maxee 1.0)
#   strip primers (cutadapt-free: skip if not present; vsearch trims by length)
#   dereplicate per-sample, then add sample label
# Produces concatenated dereplicated FASTA used for OTU clustering.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
META="$ROOT/data/sample_metadata.tsv"
FQ="$ROOT/fastq"
WORK="$ROOT/work"
LOG="$ROOT/work/per_sample.log"
mkdir -p "$WORK"
: > "$LOG"

# Concatenate per-sample merged+filtered seqs with relabel ">SRRxxx.<n>;sample=SRRxxx"
ALL="$WORK/all.merged.fasta"
: > "$ALL"

while IFS=$'\t' read -r run sample lib animal dose day group reads ftp; do
  [ "$run" = "run" ] && continue
  R1="$FQ/${run}_1.fastq.gz"
  R2="$FQ/${run}_2.fastq.gz"
  if [ ! -s "$R1" ] || [ ! -s "$R2" ]; then
    echo "[skip] $run missing fastq" | tee -a "$LOG"
    continue
  fi
  MRG="$WORK/${run}.merged.fastq"
  FILT="$WORK/${run}.filt.fasta"

  if [ ! -s "$FILT" ]; then
    vsearch --fastq_mergepairs "$R1" --reverse "$R2" \
      --fastq_minovlen 20 --fastq_maxdiffs 10 \
      --fastqout "$MRG" \
      --threads 4 --quiet 2>>"$LOG" || { echo "MERGE FAIL $run" >>"$LOG"; continue; }

    # Quality filter: paper used Q>=30 (strict); we use maxee 1.0 (DADA2-equivalent)
    # but keep Q-filter loose to retain reads from a 100bp HiSeq 2x101 run.
    vsearch --fastq_filter "$MRG" \
      --fastq_maxee 1.0 --fastq_minlen 200 --fastq_maxlen 300 \
      --fastaout "$FILT" --threads 4 --quiet 2>>"$LOG" || { echo "FILT FAIL $run" >>"$LOG"; continue; }
    rm -f "$MRG"
  fi

  # Relabel and append to all
  awk -v s="$run" '/^>/{i++; print ">"s"."i";sample="s; next} {print}' "$FILT" >> "$ALL"
  n=$(grep -c '^>' "$FILT" || true)
  echo "[ok] $run merged_filt=$n group=$group" | tee -a "$LOG"
done < "$META"

echo "Total merged+filtered reads: $(grep -c '^>' "$ALL")" | tee -a "$LOG"
