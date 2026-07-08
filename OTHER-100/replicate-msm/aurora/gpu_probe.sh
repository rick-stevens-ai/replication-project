#!/bin/bash
#PBS -N gpu_probe
#PBS -l select=1
#PBS -l walltime=00:10:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home

echo "=== HOST ==="
hostname

echo "=== GPU DEVICES ==="
ls -la /dev/dri/ 2>/dev/null
echo "---"
ls -la /dev/accel/ 2>/dev/null

echo "=== SYCL ==="
sycl-ls 2>/dev/null || echo "sycl-ls not found"

echo "=== CLINFO ==="
clinfo 2>/dev/null | head -40 || echo "clinfo not found"

echo "=== ONEAPI ENV ==="
echo "ONEAPI_ROOT: $ONEAPI_ROOT"
echo "OCL_ICD_VENDORS: $OCL_ICD_VENDORS"
ls /etc/OpenCL/vendors/ 2>/dev/null
echo "---"
ls /usr/lib64/libOpenCL* /usr/lib64/libze* 2>/dev/null

echo "=== ICD FILES ==="
find /etc/OpenCL /opt/intel -name "*.icd" 2>/dev/null | head -10
cat /etc/OpenCL/vendors/*.icd 2>/dev/null

echo "=== LOADED MODULES ==="
module list 2>&1

echo "=== TRY OPENMM ==="
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL
python3 src/gpu_test.py 2>&1
