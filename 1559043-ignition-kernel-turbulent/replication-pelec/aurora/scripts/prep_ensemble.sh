#!/bin/bash
# prep_ensemble.sh — generate 20 ensemble run dirs (5 real × 4 phi). Optionally submit.
set -e

BASE=/lus/flare/projects/datascience_collab/stevens/replicate-1559043
EXE=/home/stevens/software/PeleC-aurora/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex
BASE_INPUTS=/home/stevens/software/PeleC-aurora/Exec/Production/IgnitionKernel/inputs.inp
TEMPLATE_PBS=$BASE/scripts/templates/pbs_ensemble.sh
TEMPLATE_OV=$BASE/scripts/templates/inputs_overrides.template
WALLTIME=${WALLTIME:-12:00:00}
LOGDIR=$BASE/logs
SUBMIT=${SUBMIT:-no}
mkdir -p $LOGDIR

PHIS=(0.6 0.8 1.0 1.2)
REALS=(0 1 2 3 4)

TS=$(date +%Y%m%d_%H%M)
MANIFEST=$LOGDIR/ensemble_manifest_${TS}.tsv
echo -e "tag\tphi\treal\tkx0_m\tkz0_m\tjobid\trundir" > $MANIFEST

for PHI in "${PHIS[@]}"; do
  for REAL in "${REALS[@]}"; do
    TAG="phi${PHI}_r${REAL}"
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
    sed -e "s|__EXE_PATH__|$EXE|g" \
        -e "s|PBS_LOGDIR|$LOGDIR|g" \
        -e "s|WALLTIME|$WALLTIME|g" \
        -e "s|IK_PHI_REAL|IK_${TAG}|g" \
        $TEMPLATE_PBS > $RUNDIR/run.pbs
    chmod +x $RUNDIR/run.pbs

    JOBID="(not submitted)"
    if [ "$SUBMIT" = "yes" ]; then
      JOBID=$(cd $RUNDIR && qsub run.pbs)
      echo "Submitted $TAG → $JOBID"
    else
      echo "Prepared $TAG (kx0=$KX0, kz0=$KZ0) → $RUNDIR"
    fi
    echo -e "$TAG\t$PHI\t$REAL\t$KX0\t$KZ0\t$JOBID\t$RUNDIR" >> $MANIFEST
  done
done
echo "=== Manifest: $MANIFEST ==="
cat $MANIFEST
