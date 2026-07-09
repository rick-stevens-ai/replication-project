#!/usr/bin/env bash
# Dereplicate combined reads, cluster at 97% (matches paper's GreenGenes97 OTUs),
# remove chimeras, build OTU x sample count table, assign taxonomy via SILVA V4 ref.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
WORK="$ROOT/work"
REF_V4="$ROOT/reference/silva_seed_v138_1.v4.fasta"
ALL="$WORK/all.merged.fasta"

DEREP="$WORK/all.derep.fasta"
OTUS="$WORK/otus.fasta"
OTU_TABLE_TSV="$WORK/otu_table.tsv"
TAX="$WORK/otu_tax.tsv"
THREADS=8

echo "[1/5] dereplicate"
vsearch --derep_fulllength "$ALL" \
  --output "$DEREP" --sizein --sizeout --minuniquesize 2 --threads $THREADS

echo "[2/5] cluster at 97%"
vsearch --cluster_size "$DEREP" --id 0.97 \
  --centroids "$OTUS" --relabel OTU_ --sizein --sizeout --threads $THREADS

echo "[3/5] de novo chimera removal"
vsearch --uchime3_denovo "$OTUS" --nonchimeras "$WORK/otus.nc.fasta" --sizein
mv "$WORK/otus.nc.fasta" "$OTUS"

echo "[4/5] map reads back to OTUs (build count table)"
vsearch --usearch_global "$ALL" --db "$OTUS" --id 0.97 \
  --otutabout "$OTU_TABLE_TSV" --threads $THREADS

echo "[5/5] assign taxonomy via SILVA v138 V4 reference"
vsearch --usearch_global "$OTUS" --db "$REF_V4" --id 0.80 \
  --top_hits_only --blast6out "$WORK/otu_vs_silva.b6" \
  --threads $THREADS

# Join blast hit with taxonomy
python3 - <<'PY'
import csv, pandas as pd
from pathlib import Path
ROOT = Path("$ROOT".replace("$ROOT", "/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-space-radiation-gut-microbiome-2017"))
b6 = pd.read_csv(ROOT/"work/otu_vs_silva.b6", sep="\t", header=None,
                 names=["qid","sid","pid","aln","mm","go","qs","qe","ss","se","ev","bs"])
tax = pd.read_csv(ROOT/"reference/silva_seed_v138_1.tax.tsv", sep="\t")
tax_map = dict(zip(tax["seqid"], tax["taxonomy"]))
# take best hit per OTU
best = b6.sort_values(["qid","pid","bs"], ascending=[True,False,False]).drop_duplicates("qid")
best["taxonomy"] = best["sid"].map(tax_map).fillna("Unassigned")
best[["qid","sid","pid","taxonomy"]].to_csv(ROOT/"work/otu_tax.tsv", sep="\t", index=False)
print("Taxonomy assigned for", len(best), "OTUs")
PY

echo "Done. Files in $WORK"
wc -l "$DEREP" "$OTUS" "$OTU_TABLE_TSV" "$TAX"
