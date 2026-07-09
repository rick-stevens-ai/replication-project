#!/usr/bin/env bash
# Download the 4 A. baumannii genomes deposited by Chan et al. 2020 (PMID 32681170)
# Accessions per paper Data Availability:
#   ABUH763 chromosome CP035051  + plasmids CP035052 (~74 kb), CP035053
#   ABUH773 chromosome CP035049  + plasmid CP035050
#   ABUH793 chromosome CP035045  + plasmids CP035046, CP035047, CP035048
#   ABUH796 chromosome CP035043  + plasmid CP035044
set -eo pipefail
set +u
source ~/env.sh || true
set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH
cd /data/stevens/bvbrc69-abgri4/genomes

# Chromosome + plasmid ranges per paper
declare -A STRAINS=(
  [ABUH763]="CP035051 CP035052 CP035053"
  [ABUH773]="CP035049 CP035050"
  [ABUH793]="CP035045 CP035046 CP035047 CP035048"
  [ABUH796]="CP035043 CP035044"
)

for strain in "${!STRAINS[@]}"; do
  mkdir -p "$strain"
  cd "$strain"
  for acc in ${STRAINS[$strain]}; do
    if [[ ! -s "${acc}.fna" ]]; then
      echo "[$strain] fetching $acc ..."
      efetch -db nuccore -id "$acc" -format fasta > "${acc}.fna"
    fi
    if [[ ! -s "${acc}.gbk" ]]; then
      efetch -db nuccore -id "$acc" -format gb > "${acc}.gbk"
    fi
    ls -la "${acc}.fna" "${acc}.gbk"
  done
  # Concatenate replicons to a single genome fasta
  cat *.fna > "${strain}_all.fna"
  cd ..
done

echo "=== DONE ==="
ls -la */
