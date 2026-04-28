#!/bin/bash
# Run dos.x and projwfc.x on a slab after nscf. Usage: dos_pp.sh <dir> <gpus>
# no set -u due to qe_env.sh
DIR="$1"
GPUS="$2"
NP=$(echo "$GPUS" | awk -F',' '{print NF}')
cd "$DIR" || exit 1
source ~/software/qe-cuda/qe_env.sh
export PATH=$HOME/software/qe-cuda/q-e-qe-7.4.1/bin:$PATH
export CUDA_VISIBLE_DEVICES="$GPUS"
export OMPI_MCA_btl_base_warn_component_unused=0
echo "[$(date)] DOS in $DIR"
mpirun --oversubscribe -n "$NP" dos.x -in lto_dos.in > dos.out 2>&1
echo "[$(date)] DOS exit=$?"
echo "[$(date)] projwfc in $DIR"
mpirun --oversubscribe -n "$NP" projwfc.x -in lto_projwfc.in > projwfc.out 2>&1
echo "[$(date)] projwfc exit=$?"
