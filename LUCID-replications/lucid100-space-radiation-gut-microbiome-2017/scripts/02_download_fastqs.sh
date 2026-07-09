#!/usr/bin/env bash
# Download all 80 SRR fastq pairs from ENA into ./fastq/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
META="$ROOT/data/sample_metadata.tsv"
OUT="$ROOT/fastq"
LOG="$ROOT/data/download.log"
mkdir -p "$OUT"
: > "$LOG"

# Field 9 = fastq_ftp (semicolon-separated pair)
tail -n +2 "$META" | awk -F'\t' '{print $9}' | tr ';' '\n' | while read -r url; do
  [ -z "$url" ] && continue
  fname="$(basename "$url")"
  dst="$OUT/$fname"
  if [ -s "$dst" ]; then
    echo "skip $fname (exists)" | tee -a "$LOG"
    continue
  fi
  echo "fetch $fname" | tee -a "$LOG"
  curl -sSL --retry 3 --retry-delay 2 -o "$dst.tmp" "https://$url" && mv "$dst.tmp" "$dst"
done

echo "DONE. Total bytes: $(du -sh "$OUT" | cut -f1)"
ls "$OUT" | wc -l
