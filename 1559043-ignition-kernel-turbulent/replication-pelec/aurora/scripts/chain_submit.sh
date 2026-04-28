#!/bin/bash
# Chain-submit: 4 parallel chains (one per phi), each chain serial over 5 realizations.
# Uses afterany dependencies so chained jobs sit in 'H' state, not 'Q' — respects queue limits.
set -e
BASE=/lus/flare/projects/datascience_collab/stevens/replicate-1559043
MANIFEST=$BASE/logs/chain_manifest_$(date +%Y%m%d_%H%M).tsv
echo -e "tag\tphi\treal\tdepends_on\tjobid" > $MANIFEST

for PHI in 0.6 0.8 1.0 1.2; do
  PREV=""
  for REAL in 0 1 2 3 4; do
    TAG="phi${PHI}_r${REAL}"
    RUNDIR=$BASE/runs/$TAG
    # Skip if already submitted (e.g. phi0.6_r0)
    if [ -n "$PREV" ]; then
      JOBID=$(cd $RUNDIR && qsub -W depend=afterany:$PREV run.pbs 2>&1) || JOBID="FAILED: $JOBID"
    else
      # First in chain: check if there's already a running/queued job, else submit fresh
      EXISTING=$(qstat -u stevens 2>/dev/null | grep "IK_${TAG} " | awk '{print $1}' | head -1)
      if [ -n "$EXISTING" ]; then
        JOBID="$EXISTING (already in queue)"
      else
        JOBID=$(cd $RUNDIR && qsub run.pbs 2>&1) || JOBID="FAILED: $JOBID"
      fi
    fi
    echo "chain[$PHI] $TAG → $JOBID  (dep=$PREV)"
    echo -e "$TAG\t$PHI\t$REAL\t$PREV\t$JOBID" >> $MANIFEST
    # Extract bare jobid for next dependency
    PREV=$(echo "$JOBID" | grep -oE '^[0-9]+' | head -1)
    [ -z "$PREV" ] && { echo "  ERR: couldn't parse jobid, breaking chain for $PHI"; break; }
  done
done
echo
echo "=== final qstat ==="
qstat -u stevens
echo "=== manifest: $MANIFEST ==="
