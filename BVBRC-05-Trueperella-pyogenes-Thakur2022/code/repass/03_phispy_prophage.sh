#!/usr/bin/env bash
# Pass-2: Prophage detection via PhiSpy on each Prokka GBK.
# Paper used PHASTER (web). Free substitute: PhiSpy.

set -uo pipefail
ROOT=/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022
PROKKA=$ROOT/analysis/prokka
OUTBASE=$ROOT/results/repass/phispy
mkdir -p "$OUTBASE"

source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate tpyo

SUMMARY="$OUTBASE/summary.tsv"
echo -e "strain\tn_prophages\tprophages" > "$SUMMARY"

for d in "$PROKKA"/*/; do
    s=$(basename "$d")
    gbk="$d/$s.gbk"
    out="$OUTBASE/$s"
    if [ ! -f "$gbk" ]; then
        echo "Missing $gbk"
        continue
    fi
    rm -rf "$out"
    mkdir -p "$out"
    PhiSpy.py "$gbk" -o "$out" --color --output_choice 1 >/dev/null 2>"$out/err.log" || {
        # Newer PhiSpy uses lowercase
        phispy "$gbk" -o "$out" --color --output_choice 1 >/dev/null 2>>"$out/err.log" || true
    }
    if [ -f "$out/prophage_coordinates.tsv" ]; then
        n=$(wc -l < "$out/prophage_coordinates.tsv" | tr -d ' ')
        regs=$(awk '{printf "%s:%s-%s ", $2,$3,$4}' "$out/prophage_coordinates.tsv")
        echo -e "$s\t$n\t$regs" >> "$SUMMARY"
        echo "  $s: $n prophage region(s)"
    elif [ -f "$out/prophage.tsv" ]; then
        n=$(wc -l < "$out/prophage.tsv" | tr -d ' ')
        echo -e "$s\t$n\t" >> "$SUMMARY"
        echo "  $s: $n prophage region(s) [prophage.tsv]"
    else
        n=0
        # Some PhiSpy versions don't write a file if zero prophages
        if ls "$out" | grep -q prophage; then
            : 
        fi
        echo -e "$s\t0\t" >> "$SUMMARY"
        echo "  $s: 0 prophages"
    fi
done

echo ""
echo "Summary:"
cat "$SUMMARY" | column -t -s $'\t' | head -25
