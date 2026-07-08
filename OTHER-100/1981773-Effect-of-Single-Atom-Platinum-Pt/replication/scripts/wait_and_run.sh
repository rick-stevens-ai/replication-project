#!/bin/bash
ROOT=~/projects/replicate-1981773
# Wait until the running slab_relax.in on GPUs 4,6 finishes
while pgrep -af "pw.x -in slab_relax.in" | grep -v tailscaled > /dev/null; do
    sleep 10
done
echo "[$(date)] slab_001 relax finished; starting queue1_remaining" >> $ROOT/scripts/wait_and_run.log
exec bash $ROOT/scripts/runner.sh queue1_remaining.txt
