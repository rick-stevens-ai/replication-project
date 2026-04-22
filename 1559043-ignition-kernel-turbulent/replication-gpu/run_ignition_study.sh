#!/bin/bash
# Ignition kernel replication study
# Jaravel et al. (2019) - OSTI 1559043
# 4 equivalence ratios on 8 A100 GPUs

set -e

EXEC="./PeleLMeX3d.gnu.TPROF.MPI.CUDA.ex"
BASE_INPUT="ignition-kernel-3d.inp"
OUTDIR="$HOME/Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-gpu"

# Check executable exists
if [ ! -f "$EXEC" ]; then
    echo "ERROR: Executable not found: $EXEC"
    exit 1
fi

# Equivalence ratios from the paper
PHIS="0.6 0.8 1.0 1.2"

for PHI in $PHIS; do
    RUNDIR="${OUTDIR}/phi_${PHI}"
    mkdir -p "$RUNDIR"

    echo "================================================"
    echo "Starting phi = $PHI at $(date)"
    echo "Output: $RUNDIR"
    echo "================================================"

    # Copy input file and modify phi
    cp "$BASE_INPUT" "${RUNDIR}/inputs"

    # Customize for this run
    cat >> "${RUNDIR}/inputs" << EOF

# Override for phi = $PHI
prob.equiv_ratio = $PHI
amr.plot_file = ${RUNDIR}/plt
amr.check_file = ${RUNDIR}/chk
peleLM.tempPlane.file = ${RUNDIR}/diagTemp
peleLM.hrPlane.file = ${RUNDIR}/diagHR
EOF

    # Run with 8 GPUs
    echo "Running phi=$PHI with 8 GPUs..."
    mpirun -np 8 --bind-to none \
        $EXEC ${RUNDIR}/inputs \
        > "${RUNDIR}/run.log" 2>&1

    echo "phi = $PHI completed at $(date)"
    echo ""
done

echo "All runs complete at $(date)"
echo "Results in $OUTDIR"
