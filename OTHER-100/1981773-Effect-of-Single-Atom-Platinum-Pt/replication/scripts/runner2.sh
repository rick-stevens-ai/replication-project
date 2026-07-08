#!/bin/bash
# Runs jobs from queue2.txt
set -u
ROOT=~/projects/replicate-1981773
LOG=$ROOT/scripts/runner2.log
echo "[$(date)] runner2 started PID=$$" >> $LOG
QUEUE=$ROOT/scripts/queue2.txt
while IFS= read -r line; do
    [ -z "$line" ] && continue
    [[ "$line" == \#* ]] && continue
    set -- $line
    inp="$1"; gpus="$2"
    echo "[$(date)] start $inp on $gpus" >> $LOG
    bash $ROOT/scripts/run_qe.sh "$inp" "$gpus"
    echo "[$(date)] end $inp exit=$?" >> $LOG
done < "$QUEUE"
echo "[$(date)] runner2 done" >> $LOG
