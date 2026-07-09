#!/bin/bash
# Build ML trees for 16S, OXA-22, OXA-60 using MAFFT + FastTree
set -e
export PATH=/usr/local/Cellar/mafft/7.526/bin:$PATH
MAFFT=/usr/local/Cellar/mafft/7.526/bin/mafft
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021/results/repass

for name in 16S OXA22 OXA60; do
  in="${name}.fasta"
  aln="${name}.aln.fasta"
  tree="${name}.nwk"
  log="${name}.fasttree.log"

  echo "=== $name ==="
  if [ "$name" = "16S" ]; then
    # nucleotide
    $MAFFT --auto --quiet "$in" > "$aln"
    # FastTree GTR for nucleotide
    fasttree -nt -gtr -log "$log" "$aln" > "$tree" 2>>"$log" || echo "fasttree failed"
  else
    # protein
    $MAFFT --auto --quiet "$in" > "$aln"
    fasttree -log "$log" "$aln" > "$tree" 2>>"$log" || echo "fasttree failed"
  fi
  echo "  aln: $(grep -c '>' $aln) seqs, $(awk '!/^>/{print length($0); exit}' $aln) cols"
  echo "  tree: $(wc -c < $tree) bytes"
  grep -i "log.*lk\|total" "$log" 2>/dev/null | head -3
done
echo "DONE"
