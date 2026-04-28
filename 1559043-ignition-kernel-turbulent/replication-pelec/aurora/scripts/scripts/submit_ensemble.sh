#!/bin/bash
# submit_ensemble.sh — generate and submit 20 PBS jobs (5 real × 4 phi)
# Run from Aurora login node after build is verified.
set -e

BASE=/lus/flare/projects/datascience_collab/stevens/replicate-1559043
EXE=__EXE_PATH__                     # filled in when submitted
BASE_INPUTS=__BASE_INPUTS__          # full path to canonical inputs.inp
TEMPLATE_PBS=$BASE/scripts/pbs_ensemble.sh
TEMPLATE_OV=$BASE/scripts/inputs_overrides.template
WALLTIME=${WALLTIME:-12:00:00}       # preemptable cap is typically 24h; 12h/run with chk-restart is safe
LOGDIR=$BASE/logs
mkdir -p $LOGDIR

PHIS=(0.6 0.8 1.0 1.2)
REALS=(0 1 2 3 4)

JOBS=()
for PHI in "${PHIS[@]}"; do
  for REAL in "${REALS[@]}"; do
    TAG="phi${PHI}_r${REAL}"
    # Pseudo-random jitter in m: ±0.5 mm on kernel x,z (deterministic from indices)
    # Base kernel: x0=0.008 m, z0=0.008 m
    # Use awk for portable math
    read KX0 KZ0 <<< $(awk -v r=$REAL -v p=$PHI 'BEGIN{
        srand(1000 + r*13 + int(p*10)*7);
        dx = (rand()-0.5)*1e-3;
        dz = (rand()-0.5)*1e-3;
        printf("%.6e %.6e\n", 0.008+dx, 0.008+dz);}')
    RUNDIR=$BASE/runs/$TAG
    mkdir -p $RUNDIR
    cp $BASE_INPUTS $RUNDIR/inputs.inp
    sed -e "s/__PHI__/$PHI/g" -e "s/__REAL__/$REAL/g" \
        -e "s/__KX0__/$KX0/g" -e "s/__KZ0__/$KZ0/g" \
        $TEMPLATE_OV >> $RUNDIR/inputs.inp
    # PBS script
    sed -e "s|__EXE_PATH__|$EXE|g" \
        -e "s|PBS_LOGDIR|$LOGDIR|g" \
        -e "s|WALLTIME|$WALLTIME|g" \
        -e "s|IK_PHI_REAL|IK_${TAG}|g" \
        $TEMPLATE_PBS > $RUNDIR/run.pbs
    chmod +x $RUNDIR/run.pbs
    # Submit (throttle: start first 10, leave rest queued explicitly)
    JOBID=$(cd $RUNDIR && qsub run.pbs)
    echo "Submitted $TAG → $JOBID"
    JOBS+=("$TAG:$JOBID")
  done
done
echo "=== Submitted ${#JOBS[@]} jobs ==="
printf '%s\n' "${JOBS[@]}" | tee $LOGDIR/submitted_jobs_$(date +%Y%m%d_%H%M).txt
