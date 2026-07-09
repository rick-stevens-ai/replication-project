#!/usr/bin/env bash
# MLST typing of the 4 strains — paper claims all are ST2 (Pasteur) / ST281 (Oxford)
set -eo pipefail
set +u; source ~/env.sh || true; set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH

cd /data/stevens/bvbrc69-abgri4
mkdir -p results/mlst

for s in ABUH763 ABUH773 ABUH793 ABUH796; do
  echo "=== $s ==="
  # Pasteur scheme (abaumannii_2)
  mlst --scheme abaumannii_2 --nopath genomes/$s/${s}_all.fna 2>/dev/null > results/mlst/${s}_pasteur.tsv || echo "pasteur failed"
  cat results/mlst/${s}_pasteur.tsv
  # Oxford scheme (abaumannii)
  mlst --scheme abaumannii --nopath genomes/$s/${s}_all.fna 2>/dev/null > results/mlst/${s}_oxford.tsv || echo "oxford failed"
  cat results/mlst/${s}_oxford.tsv
done

# Combined
{
  echo -e "strain\tpasteur_ST\tpasteur_alleles\toxford_ST\toxford_alleles"
  for s in ABUH763 ABUH773 ABUH793 ABUH796; do
    p_st=$(cut -f3 results/mlst/${s}_pasteur.tsv 2>/dev/null || echo NA)
    p_alleles=$(cut -f4- results/mlst/${s}_pasteur.tsv | tr '\t' ',' 2>/dev/null || echo NA)
    o_st=$(cut -f3 results/mlst/${s}_oxford.tsv 2>/dev/null || echo NA)
    o_alleles=$(cut -f4- results/mlst/${s}_oxford.tsv | tr '\t' ',' 2>/dev/null || echo NA)
    echo -e "${s}\t${p_st}\t${p_alleles}\t${o_st}\t${o_alleles}"
  done
} > results/mlst/summary.tsv
echo "=== SUMMARY ==="
column -t -s $'\t' results/mlst/summary.tsv
