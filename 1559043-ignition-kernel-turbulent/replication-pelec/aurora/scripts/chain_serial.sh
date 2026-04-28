#!/bin/bash
# Submit all remaining ensemble jobs as a linear chain depending on 8449560
# (the already-queued phi0.6_r0). They sit in H state until their turn.
set -e
BASE=/lus/flare/projects/datascience_collab/stevens/replicate-1559043
SEED_JOB=${1:-8449560}
MANIFEST=$BASE/logs/chain_serial_$(date +%Y%m%d_%H%M).tsv
echo -e "tag\tdepends_on\tjobid" > $MANIFEST
PREV=$SEED_JOB

# Order: interleave phi values to hit diversity early
ORDER=(
  phi0.8_r0 phi1.0_r0 phi1.2_r0
  phi0.6_r1 phi0.8_r1 phi1.0_r1 phi1.2_r1
  phi0.6_r2 phi0.8_r2 phi1.0_r2 phi1.2_r2
  phi0.6_r3 phi0.8_r3 phi1.0_r3 phi1.2_r3
  phi0.6_r4 phi0.8_r4 phi1.0_r4 phi1.2_r4
)
for TAG in "${ORDER[@]}"; do
  RUNDIR=$BASE/runs/$TAG
  OUT=$(cd $RUNDIR && qsub -W depend=afterany:$PREV run.pbs 2>&1) || true
  JOBID=$(echo "$OUT" | grep -oE '^[0-9]+' | head -1)
  if [ -z "$JOBID" ]; then
    echo "$TAG  → FAIL: $OUT  (dep=$PREV)"
    echo -e "$TAG\t$PREV\tFAIL: $OUT" >> $MANIFEST
    break
  fi
  echo "$TAG  → $JOBID  (dep=$PREV)"
  echo -e "$TAG\t$PREV\t$JOBID" >> $MANIFEST
  PREV=$JOBID
done
echo
echo "=== qstat -u stevens ==="
qstat -u stevens
echo "=== manifest: $MANIFEST ==="
