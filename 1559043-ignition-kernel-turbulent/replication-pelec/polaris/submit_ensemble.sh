#!/bin/bash
# 20 ensemble runs: 5 realizations x 4 phi on Polaris preemptable queue.
# Realization jitter via kernel_x0 (±0.5mm) and turb_intensity (±1%).
set -euo pipefail

BASE=/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043
PELEC_EXE=${BASE}/verify/PeleC3d.gnu.TPROF.MPI.CUDA.ex
BASE_INPUTS=${BASE}/verify/inputs.inp
ALLOC=IMPROVE_Aim1
QUEUE=preemptable
WALLTIME=02:00:00

PHIS=(0.6 0.8 1.0 1.2)
REALS=(1 2 3 4 5)

mkdir -p ${BASE}/ensemble/jobs ${BASE}/ensemble/runs
cd ${BASE}/ensemble

for phi in "${PHIS[@]}"; do
  for r in "${REALS[@]}"; do
    TAG="phi${phi}_r${r}"
    WORKDIR=${BASE}/ensemble/runs/${TAG}
    mkdir -p ${WORKDIR}

    # Realization jitter: ±0.5mm kernel x-position, ±1% turb_intensity
    # (seeds: r=1..5 → -2,-1,0,+1,+2 × delta)
    JITTER=$(echo "($r - 3) * 0.0001" | bc -l)   # meters: ±0.2mm per step
    KERNEL_X=$(echo "0.008 + ${JITTER}" | bc -l)  # 8mm ± up to 0.4mm
    TURB=$(echo "0.10 + ($r - 3) * 0.01" | bc -l) # 0.08..0.12

    # Write per-run inputs
    cp ${BASE_INPUTS} ${WORKDIR}/inputs.inp
    # Strip/override the ensemble-relevant params
    python3 - <<PYEOF
with open("${WORKDIR}/inputs.inp") as f: lines=f.readlines()
out=[]
skip=("prob.equiv_ratio","prob.kernel_x0","prob.turb_intensity","max_step","stop_time","amr.plot_int","amr.check_int","amr.max_level")
for l in lines:
    k=l.strip().split()[0] if l.strip() else ""
    if k in skip: continue
    out.append(l)
out.append("\n# ensemble overrides\n")
out.append(f"prob.equiv_ratio = ${phi}\n")
out.append(f"prob.kernel_x0 = ${KERNEL_X}\n")
out.append(f"prob.turb_intensity = ${TURB}\n")
out.append("max_step = 200000\nstop_time = 1.0e-3\namr.max_level = 0\namr.plot_int = 200\namr.check_int = 2000\n")
open("${WORKDIR}/inputs.inp","w").writelines(out)
PYEOF

    cat > ${BASE}/ensemble/jobs/${TAG}.pbs << PBSEOF
#!/bin/bash
#PBS -l select=1:system=polaris
#PBS -l walltime=${WALLTIME}
#PBS -l filesystems=home:eagle
#PBS -q ${QUEUE}
#PBS -A ${ALLOC}
#PBS -N pele_${TAG}
#PBS -r y
#PBS -j oe

cd ${WORKDIR}
module swap PrgEnv-nvidia PrgEnv-gnu 2>/dev/null || true
module load cuda/12.9 craype-accel-nvidia80 2>/dev/null || true
CUDA_MATH_LIB=/opt/nvidia/hpc_sdk/Linux_x86_64/25.5/math_libs/12.9/targets/x86_64-linux/lib
export LD_LIBRARY_PATH=\$CUDA_MATH_LIB:\$LD_LIBRARY_PATH
export MPICH_GPU_SUPPORT_ENABLED=1

LAST_CHK=\$(ls -d chk* 2>/dev/null | sort | tail -1 || true)
RESUME=""
[ -n "\$LAST_CHK" ] && RESUME="amr.restart=\$LAST_CHK"

mpiexec -n 4 --ppn 4 --depth 8 --cpu-bind depth --env OMP_NUM_THREADS=8 \\
  ${PELEC_EXE} inputs.inp \$RESUME
PBSEOF

    qsub ${BASE}/ensemble/jobs/${TAG}.pbs
    echo "Submitted ${TAG}"
  done
done

qstat -u \$USER
