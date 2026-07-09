#!/usr/bin/env bash
# Pass-2: Genomic Island detection via IslandPath-DIMOB.
# Paper used IslandViewer4 (which itself runs IslandPath-DIMOB + SIGI-HMM + Islander + Islandpick).
# Note: paper used SIGI-HMM + DIMOB for draft genomes; DIMOB alone for complete genomes is the
# closest free single-tool substitute.

set -uo pipefail
ROOT=/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022
PROKKA=$ROOT/analysis/prokka
OUTBASE=$ROOT/results/repass/islandpath
mkdir -p "$OUTBASE"

source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate tpyo

SUMMARY="$OUTBASE/summary.tsv"
echo -e "strain\tn_gis\tmin_size_bp\tmax_size_bp\tcontigs" > "$SUMMARY"

for d in "$PROKKA"/*/; do
    s=$(basename "$d")
    gbk="$d/$s.gbk"
    out="$OUTBASE/${s}_gis.txt"
    [ ! -f "$gbk" ] && continue
    rm -f "$out"
    islandpath "$gbk" "$out" 2>"$OUTBASE/${s}.err.log" || true
    if [ -f "$out" ]; then
        n=$(wc -l < "$out" | tr -d ' ')
        # Each line: contig\tstart\tend
        if [ "$n" -gt 0 ]; then
            mn=$(awk '{print $3-$2+1}' "$out" | sort -n | head -1)
            mx=$(awk '{print $3-$2+1}' "$out" | sort -n | tail -1)
            ctg=$(awk '{print $1}' "$out" | sort -u | tr '\n' ',' | sed 's/,$//')
        else
            mn=0; mx=0; ctg="-"
        fi
        echo -e "$s\t$n\t$mn\t$mx\t$ctg" >> "$SUMMARY"
        echo "  $s: $n GIs (size $mn - $mx bp)"
    else
        echo -e "$s\t0\t0\t0\t-" >> "$SUMMARY"
        echo "  $s: 0 (no output)"
    fi
done

echo ""
echo "Summary:"
column -t -s $'\t' < "$SUMMARY"
