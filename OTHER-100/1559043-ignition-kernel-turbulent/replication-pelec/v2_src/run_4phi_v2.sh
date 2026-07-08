#!/bin/bash
# Run 4-phi study, one GPU per case, in parallel.
set -e
BASE=~/software/combustion-codes/PeleC/Exec/Production/IgnitionKernel
EXE=$BASE/PeleC3d.gnu.TPROF.MPI.CUDA.ex
RUNROOT=$BASE/runs_v2
STOPT=2.0e-4  # 0.2 ms

cd $RUNROOT

for idx in 0 1 2 3; do
  case $idx in
    0) PHI=0.6 ;;
    1) PHI=0.8 ;;
    2) PHI=1.0 ;;
    3) PHI=1.2 ;;
  esac
  DIR=phi_${PHI}
  rm -rf $DIR
  mkdir -p $DIR
  cp $BASE/inputs.inp $DIR/inputs.inp
  # Override phi and stop_time in a small extra file
  cat >> $DIR/inputs.inp <<EOF

# --- Overrides for 4-phi sweep v2 ---
prob.equiv_ratio = $PHI
stop_time        = $STOPT
max_step         = 20000
amr.plot_int     = 200
amr.check_int    = 2000
EOF
  (
    cd $DIR
    CUDA_VISIBLE_DEVICES=$idx mpirun -np 1 $EXE inputs.inp > run.log 2>&1
    echo "phi=$PHI DONE $(date +%H:%M:%S)" > DONE
  ) &
  echo "Launched phi=$PHI on GPU $idx (pid $!)"
done

wait
echo "All 4 phi cases finished at $(date)"
