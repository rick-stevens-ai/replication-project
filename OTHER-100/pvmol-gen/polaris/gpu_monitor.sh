#!/bin/bash
# Background GPU monitor — logs utilization every 10 seconds
LOGFILE=${1:-/home/stevens/pvmol-gen/logs/gpu_util.log}
echo "timestamp,gpu_idx,gpu_util%,mem_util%,mem_used_MiB,mem_total_MiB,temp_C" > "$LOGFILE"
while true; do
    nvidia-smi --query-gpu=timestamp,index,utilization.gpu,utilization.memory,memory.used,memory.total,temperature.gpu \
        --format=csv,noheader,nounits >> "$LOGFILE"
    sleep 10
done
