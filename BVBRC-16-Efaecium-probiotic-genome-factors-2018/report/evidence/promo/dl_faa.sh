#!/usr/bin/env bash
set -uo pipefail
declare -A GIDS=(
  ["17OM39"]="1352.1047"
  ["T110"]="1344042.3"
  ["64-3"]="1352.658"
  ["6E6"]="1352.674"
  ["ATCC_700221"]="1352.804"
  ["Aus0004"]="1155766.14"
  ["Aus0085"]="1305849.3"
  ["DO"]="333849.47"
  ["E39"]="1352.890"
  ["NRRL_B-2354"]="1104325.3"
)
for key in "${!GIDS[@]}"; do
  gid="${GIDS[$key]}"
  faa="faa/${key}.faa"
  if [[ -s "$faa" && $(grep -c '^>' "$faa") -gt 100 ]]; then
    echo "[skip] $key has $(grep -c '^>' $faa) proteins"
    continue
  fi
  echo "[FAA] $key ($gid)"
  curl -sSL --max-time 90 -H "Accept: application/protein+fasta" \
    -o "$faa" \
    "https://www.bv-brc.org/api/genome_feature/?and(eq(genome_id,${gid}),eq(feature_type,CDS),eq(annotation,PATRIC))&limit(10000)"
  n=$(grep -c '^>' "$faa" 2>/dev/null || echo 0)
  echo "    -> $n proteins"
  sleep 1
done
echo "--- summary ---"
for f in faa/*.faa; do echo "$f $(grep -c '^>' $f) proteins"; done
