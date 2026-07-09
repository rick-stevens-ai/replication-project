#!/bin/bash
set -eu
cd /data/stevens/BVBRC-95/work/assemblies
source /home/stevens/env.sh
export PATH=/home/stevens/micromamba/envs/amr/bin:$PATH
mkdir -p ../amr_out

declare -A ACC2NAME=(
  [SRR12664619]="Megahit"
  [SRR13105837]="metaSpades"
  [SRR12664620]="IDBA-UD"
  [SRR12664586]="HybridSpades"
  [SRR12664608]="Canu"
  [SRR12664575]="Flye"
  [SRR12664597]="OPERA-MS"
)

# 1) Filter each .fa to contigs >= 1000 bp
for acc in SRR12664619 SRR13105837 SRR12664620 SRR12664586 SRR12664608 SRR12664575 SRR12664597; do
  fa="${acc}.fa"
  fa1k="${acc}.1kb.fa"
  if [ -s "$fa1k" ]; then continue; fi
  python3 - "$fa" "$fa1k" <<'PY'
import sys
inp, out = sys.argv[1], sys.argv[2]
kept, total = 0, 0
with open(inp) as f, open(out, 'w') as o:
    name, seq = None, []
    def flush():
        global kept, total
        if name is None: return
        total += 1
        s = ''.join(seq)
        if len(s) >= 1000:
            kept += 1
            o.write(f'>{name}\n')
            for i in range(0, len(s), 80):
                o.write(s[i:i+80] + '\n')
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            flush()
            name = line[1:].split()[0]
            seq = []
        else:
            seq.append(line)
    flush()
print(f'{inp}: kept {kept}/{total} contigs >=1kb', file=sys.stderr)
PY
done

echo "=== 1kb-filtered FASTA sizes ==="
ls -la *.1kb.fa

# 2) Run AMRFinder on filtered
for acc in SRR12664619 SRR13105837 SRR12664620 SRR12664586 SRR12664608 SRR12664575 SRR12664597; do
  name="${ACC2NAME[$acc]}"
  out="../amr_out/${name}.1kb.amr.tsv"
  if [ -s "$out" ]; then
    echo "HAVE $out ($(wc -l<$out) lines)"
    continue
  fi
  echo "=== AMRFinder $acc ($name) on 1kb-filtered ==="
  t0=$(date +%s)
  amrfinder -n "${acc}.1kb.fa" --threads 48 --plus \
    -d /home/stevens/micromamba/envs/amr/share/amrfinderplus/data/latest \
    -o "$out" 2>&1 | tail -3
  t1=$(date +%s)
  echo "  time=$((t1-t0))s lines=$(wc -l<$out)"
done
echo
echo "=== FINAL AMR OUTPUT ==="
wc -l ../amr_out/*.tsv
