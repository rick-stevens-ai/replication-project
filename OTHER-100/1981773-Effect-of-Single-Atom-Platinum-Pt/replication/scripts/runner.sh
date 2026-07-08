#!/bin/bash
set -u
ROOT=~/projects/replicate-1981773
QNAME="${1:-queue.txt}"
LOG=$ROOT/scripts/runner_${QNAME%.txt}.log
echo "[$(date)] runner started PID=$$ queue=$QNAME" >> $LOG
QUEUE=$ROOT/scripts/$QNAME
# Use fd 9 for queue to avoid stdin conflicts
exec 9<"$QUEUE"
while IFS= read -r line <&9; do
    [ -z "$line" ] && continue
    [[ "$line" == \#* ]] && continue
    set -- $line
    inp="$1"; gpus="$2"
    echo "[$(date)] start $inp on $gpus" >> $LOG
    bash $ROOT/scripts/run_qe.sh "$inp" "$gpus" </dev/null
    echo "[$(date)] end $inp exit=$?" >> $LOG
done
exec 9<&-
echo "[$(date)] runner done" >> $LOG
