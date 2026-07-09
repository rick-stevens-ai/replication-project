#!/usr/bin/env bash
# Download supplementary materials from BMC Molecular Medicine for
# Grandt et al. 2022 (DOI 10.1186/s10020-022-00520-6).
set -euo pipefail
cd "$(dirname "$0")/../data"

BASE="https://static-content.springer.com/esm/art%3A10.1186%2Fs10020-022-00520-6/MediaObjects/10020_2022_520_MOESM"

declare -A EXT=(
  [1]=xlsx [2]=pdf  [3]=docx [4]=docx [5]=xlsx [6]=docx
  [7]=pptx [8]=pptx [9]=docx [10]=pptx [11]=docx [12]=docx [13]=docx
)

for n in "${!EXT[@]}"; do
  ext="${EXT[$n]}"
  out="AF${n}.${ext}"
  if [[ -f "$out" ]]; then
    echo "[skip] $out already present"
    continue
  fi
  echo "[fetch] $out"
  curl -sL -A "Mozilla/5.0" -o "$out" "${BASE}${n}_ESM.${ext}"
done
ls -la AF*.* 2>/dev/null || true
