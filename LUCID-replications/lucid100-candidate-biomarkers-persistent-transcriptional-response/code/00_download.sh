#!/usr/bin/env bash
# Download the three GEO series matrices used by Liu et al. 2023 (DOI 10.1080/09553002.2023.2241897).
# Total ~30 MB compressed. Safe to run on CherryRd.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HERE/data/geo_series_matrix"
mkdir -p "$DEST"
cd "$DEST"

declare -A SERIES=(
    [GSE8917]=GSE8nnn
    [GSE43151]=GSE43nnn
    [GSE23515]=GSE23nnn
)

for acc in "${!SERIES[@]}"; do
    pref="${SERIES[$acc]}"
    out="${acc}_series_matrix.txt.gz"
    if [[ -s "$out" ]]; then
        echo "[skip] $out already present ($(stat -f%z "$out") bytes)"
        continue
    fi
    url="https://ftp.ncbi.nlm.nih.gov/geo/series/${pref}/${acc}/matrix/${out}"
    echo "[get ] $url"
    curl -sS -L -o "$out" "$url"
    ls -la "$out"
done

echo
echo "Done. Files in $DEST"
ls -la "$DEST"
