#!/bin/bash
# Usage: run_qe.sh <input.in> <gpus>  e.g. run_qe.sh bulk_vcrelax.in 0,1,2,3
INP="$1"
GPUS="${2:-0,1,2,3}"
NP=$(echo "$GPUS" | awk -F',' '{print NF}')
source ~/software/qe-cuda/qe_env.sh
export PATH=$HOME/software/qe-cuda/q-e-qe-7.4.1/bin:$PATH
cd "$(dirname "$INP")" || exit 1
INPF="$(basename "$INP")"
OUTF="${INPF%.in}.out"
export CUDA_VISIBLE_DEVICES="$GPUS"
export OMP_NUM_THREADS=2
export OMPI_MCA_btl_base_warn_component_unused=0
echo "[$(date)] running $INPF on GPUs $GPUS (np=$NP), output $OUTF"
mpirun --oversubscribe -n "$NP" pw.x -in "$INPF" > "$OUTF" 2>&1
EXIT=$?
echo "[$(date)] done exit=$EXIT"
tail -15 "$OUTF"
exit $EXIT
