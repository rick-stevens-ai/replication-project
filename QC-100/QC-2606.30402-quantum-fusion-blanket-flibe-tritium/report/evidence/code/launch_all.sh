#!/bin/bash
# launch_all.sh -- parallel driver for the FLiBe replication on uicgpu.
# Runs the full-molecule ladder (RHF/MP2/CCSD/DFT) for all 27 conformers with
# bounded parallelism, then the EWF fragment solve.
cd ~/flibe-repl
source ~/env.sh 2>/dev/null
PY=~/flibe-repl/.venv/bin/python
export OMP_NUM_THREADS=6
mkdir -p results logs

echo "=== LADDER (parallel, incl CCSD) ==="  | tee logs/launch.log
# 4 conformers concurrently, 6 threads each = 24 threads
run_ladder_job () {
  for sys in FLiBe FLiBeF FLiBeTF; do
    for c in $(seq 1 9); do echo "$sys $c"; done
  done | xargs -P 4 -n 2 bash -c 'cd ~/flibe-repl && ~/flibe-repl/.venv/bin/python run_one.py "$0" "$1" --ccsd >> logs/one_$0_c$1.log 2>&1; echo "finished $0 c$1"' 2>&1 | tee -a logs/launch.log
}
run_ladder_job

echo "=== merge ladder results ==="  | tee -a logs/launch.log
$PY - <<'PYEOF'
import json,glob,os
for sysn in ["FLiBe","FLiBeF","FLiBeTF"]:
    rows=[]
    for c in range(1,10):
        p=f"results/one_{sysn}_c{c}.json"
        if os.path.exists(p): rows.append(json.load(open(p)))
    rows.sort(key=lambda r:r["cluster"])
    json.dump(rows, open(f"results/ladder_{sysn}.json","w"), indent=2)
    print(sysn, len(rows),"conformers merged")
PYEOF

echo "=== EWF FRAGMENT SOLVE ==="  | tee -a logs/launch.log
export OMP_NUM_THREADS=24
$PY run_ewf_frag.py all >> logs/ewf_frag.log 2>&1
echo "=== ALL DONE ==="  | tee -a logs/launch.log
