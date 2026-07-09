#!/usr/bin/env bash
set -uo pipefail
mkdir -p bvbrc_lookups
declare -A STRAINS=(
  ["T110"]="T110"
  ["17OM39"]="17OM39"
  ["NRRL_B-2354"]="NRRL B-2354"
  ["64-3"]="64/3"
  ["DO"]="DO"
  ["Aus0004"]="Aus0004"
  ["Aus0085"]="Aus0085"
  ["6E6"]="6E6"
  ["E39"]="E39"
  ["ATCC_700221"]="ATCC 700221"
)
for key in "${!STRAINS[@]}"; do
  name="${STRAINS[$key]}"
  out="bvbrc_lookups/${key}.json"
  echo "querying $key / $name -> $out"
  # Use BV-BRC RQL via POST with raw query string in URL (proper encoding of comma/paren)
  python3 - <<PY > "$out"
import urllib.parse, urllib.request, sys
name=${name@Q}
q='and(eq(species,%22Enterococcus%20faecium%22),eq(strain,%22'+urllib.parse.quote(name)+'%22))&select(genome_id,genome_name,strain,assembly_accession,genome_status,genome_length,contigs,gc_content,patric_cds,bioproject_accession,genbank_accessions)&limit(20)'
url='https://www.bv-brc.org/api/genome/?'+q
req=urllib.request.Request(url, headers={'Accept':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        sys.stdout.write(r.read().decode('utf-8','replace'))
except Exception as e:
    sys.stdout.write('{"error":"%s"}'%e)
PY
  sleep 0.8
done
echo "--- head of each ---"
for f in bvbrc_lookups/*.json; do
  echo "== $f =="
  head -c 800 "$f"; echo
done
