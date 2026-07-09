#!/bin/bash
# Properly install custom PyMFEM drl4amr branch (purge pip-installed mfem first).
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/build_pymfem2.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Is) PyMFEM rebuild (purge generic, build custom) ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh
conda activate marlamr

# Purge the generic pip-installed mfem
pip uninstall -y mfem 2>&1 | tail -5 || true
rm -rf "$CONDA_PREFIX/lib/python3.6/site-packages/mfem"*

cd "$PROJDIR/amr_build/PyMFEM"
git status

mfem_prefix="$PROJDIR/amr_build/mfem/mfem/"
mfem_source="$PROJDIR/amr_build/mfem/"

# Clean stale build dirs
rm -rf build mfem/_ser/*.so mfem/_par/*.so 2>/dev/null || true

# Use a modest parallelism via env var (some PyMFEM versions read MFEM_BUILD_PARALLEL or use -j)
echo "Running setup.py install with mfem-prefix=$mfem_prefix"
# Try without --parallel flag, let setup.py default behave
python setup.py install --mfem-prefix=$mfem_prefix --mfem-source=$mfem_source 2>&1 | tail -150
INSTALL_RC=${PIPESTATUS[0]}
echo "install rc=$INSTALL_RC"

echo "=== smoke checks ==="
python -c "import mfem.ser as mfem; print('PyMFEM ser OK from:', mfem.__file__); print('has ProlongToMaxOrder:', hasattr(__import__('mfem._ser.gridfunc', fromlist=['gridfunc']), 'ProlongToMaxOrder'))" 2>&1
python -c "from marl_amr.envs.solvers.AdvectionSolver import AdvectionSolver; print('AdvectionSolver:', AdvectionSolver.name)" 2>&1
python -c "import tensorflow as tf; print('TF', tf.__version__)" 2>&1

echo "=== $(date -Is) done ==="
