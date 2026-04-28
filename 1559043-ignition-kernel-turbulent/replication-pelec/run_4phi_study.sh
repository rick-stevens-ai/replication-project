#!/bin/bash
# Ignition kernel 4-phi study - PeleC on uicgpu
# Replication of Jaravel et al. (2019) OSTI 1559043
set -e

export PATH=/tmp/cmake-3.28.3-linux-x86_64/bin:/usr/local/cuda-12.2/bin:/usr/local/cuda-12.2/nvvm/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64:$LD_LIBRARY_PATH

EXEC="./PeleC3d.gnu.TPROF.MPI.CUDA.ex"
BASE_INPUT="inputs.inp"
OUTROOT="$HOME/Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec/runs"
mkdir -p "$OUTROOT"

PHIS="0.6 0.8 1.0 1.2"

for PHI in $PHIS; do
    RUNDIR="${OUTROOT}/phi_${PHI}"
    mkdir -p "$RUNDIR"

    echo "================================================================"
    echo "Starting phi = $PHI at $(date)"
    echo "Output: $RUNDIR"
    echo "================================================================"

    mpirun -np 8 --bind-to none \
        $EXEC $BASE_INPUT \
        prob.equiv_ratio=$PHI \
        amr.plot_file="${RUNDIR}/plt" \
        amr.check_file="${RUNDIR}/chk" \
        amr.plot_int=500 \
        amr.check_int=2000 \
        > "${RUNDIR}/run.log" 2>&1 &
    
    # Wait for this phi to finish before starting next (all 8 GPUs used)
    wait
    
    echo "phi = $PHI completed at $(date)"
    tail -5 "${RUNDIR}/run.log"
done

echo ""
echo "==========================================="
echo "All 4 phi values complete at $(date)"
echo "Results in $OUTROOT"
