#!/bin/bash
# PyMFEM rebuild attempt #3 — now that crypt.h is in conda sysroot.
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/build_pymfem3.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Is) PyMFEM rebuild #3 ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh
conda activate marlamr

# Purge any prior install
pip uninstall -y mfem 2>&1 | tail -3 || true
rm -rf "$CONDA_PREFIX/lib/python3.6/site-packages/mfem"*

cd "$PROJDIR/amr_build/PyMFEM"
# Clean build artifacts but keep source
rm -rf build mfem/_ser/*.so mfem/_par/*.so 2>/dev/null || true
# Confirm we are on the right commit
git log --oneline -1

mfem_prefix="$PROJDIR/amr_build/mfem/mfem/"
mfem_source="$PROJDIR/amr_build/mfem/"

echo "Running setup.py install with mfem-prefix=$mfem_prefix"
python setup.py install --mfem-prefix=$mfem_prefix --mfem-source=$mfem_source 2>&1 | tail -80

echo "=== smoke checks ==="
python -c "
import mfem.ser as mfem
print('PyMFEM ser OK from:', mfem.__file__)
from mfem._ser import gridfunc
print('has ProlongToMaxOrder:', hasattr(gridfunc, 'ProlongToMaxOrder'))
" 2>&1
python -c "
from marl_amr.envs.solvers.AdvectionSolver import AdvectionSolver
print('AdvectionSolver:', AdvectionSolver.name)
" 2>&1
python -c "import tensorflow as tf; print('TF', tf.__version__)" 2>&1

echo "=== $(date -Is) done ==="
