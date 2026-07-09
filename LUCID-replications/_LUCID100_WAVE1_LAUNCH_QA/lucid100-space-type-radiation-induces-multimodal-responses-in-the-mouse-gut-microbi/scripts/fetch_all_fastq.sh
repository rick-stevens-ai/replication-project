#!/usr/bin/env bash
# Fetch all 80 paired-end FASTQ files for SRP098151 (Casero et al. 2017, Microbiome)
# Total ~2.08 GB. Verifies MD5s against ENA filereport.
# Usage: fetch_all_fastq.sh [DEST_DIR]
# DO NOT run on CherryRd for full analysis — fetch is fine, but QIIME/DESeq2 pipeline should run on uicgpu or similar.
set -euo pipefail
SLOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$SLOT/data/fastq}"
mkdir -p "$DEST"
FRP="$SLOT/harvest/ena_filereport.tsv"
[ -f "$FRP" ] || { echo "Missing $FRP"; exit 1; }

# Generate URL+md5 list
awk -F'\t' 'NR>1 {
  n=split($11, urls, ";");
  m=split($13, mds,  ";");
  for (i=1; i<=n; i++) {
    fname=urls[i]; sub(/.*\//, "", fname);
    print urls[i]"\t"mds[i]"\t"fname;
  }
}' "$FRP" > "$DEST/_urls.tsv"

total=$(wc -l < "$DEST/_urls.tsv" | tr -d ' ')
echo "Downloading $total FASTQ files to $DEST"

i=0
while IFS=$'\t' read -r url md5 fname; do
  i=$((i+1))
  out="$DEST/$fname"
  if [ -f "$out" ]; then
    have=$(md5 -q "$out" 2>/dev/null || md5sum "$out" | awk '{print $1}')
    if [ "$have" = "$md5" ]; then
      echo "[$i/$total] OK $fname (cached)"
      continue
    fi
  fi
  echo "[$i/$total] GET $fname"
  curl -sSL --retry 3 --retry-delay 5 -o "$out" "https://$url"
  have=$(md5 -q "$out" 2>/dev/null || md5sum "$out" | awk '{print $1}')
  if [ "$have" != "$md5" ]; then
    echo "[$i/$total] MD5 MISMATCH for $fname (expected $md5, got $have)" >&2
    exit 2
  fi
done < "$DEST/_urls.tsv"
echo "Done."
