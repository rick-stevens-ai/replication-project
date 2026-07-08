#!/bin/bash
# Quick 2-GPU test to verify MPI+CUDA works
set -e

EXEC="./PeleLMeX3d.gnu.TPROF.MPI.CUDA.ex"
TESTDIR="test_2gpu_output"
mkdir -p "$TESTDIR"

echo "Testing MPI+CUDA with 2 GPUs..."
echo "Start: $(date)"

mpirun -np 2 --bind-to none \
    $EXEC ignition-kernel-3d.inp \
    amr.max_step=10 \
    amr.plot_int=5 \
    amr.check_int=10 \
    amr.max_level=0 \
    amr.n_cell="64 32 32" \
    amr.plot_file="${TESTDIR}/plt" \
    amr.check_file="${TESTDIR}/chk" \
    2>&1 | tee "${TESTDIR}/test.log"

echo "Test complete: $(date)"
echo "Check ${TESTDIR}/test.log for errors"
