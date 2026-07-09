#!/bin/bash
# Resume MARL-AMR build at PyMFEM step after fixing crypt.h missing header.
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/build_pymfem.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Is) PyMFEM build resume ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh
conda activate marlamr

# Find a system crypt.h or install libxcrypt; conda-forge ships libxcrypt
# Try installing the dev headers first
if [ ! -f "$CONDA_PREFIX/include/crypt.h" ] && [ ! -f /usr/include/crypt.h ]; then
  echo "Installing libxcrypt headers from conda-forge..."
  conda install -y -n marlamr -c conda-forge libxcrypt 2>&1 | tail -10 || true
fi

# Locate crypt.h
CRYPT_H=""
for cand in /usr/include/crypt.h "$CONDA_PREFIX/include/crypt.h" /usr/include/x86_64-linux-gnu/crypt.h; do
  if [ -f "$cand" ]; then CRYPT_H="$cand"; break; fi
done
if [ -z "$CRYPT_H" ]; then
  echo "crypt.h still missing after conda libxcrypt. Writing minimal stub."
  cat > "$CONDA_PREFIX/include/crypt.h" <<'EOF'
/* Minimal crypt.h shim for Python 3.6 + modern libc */
#ifndef _CRYPT_H
#define _CRYPT_H 1
#ifdef __cplusplus
extern "C" {
#endif
extern char *crypt (const char *__key, const char *__salt);
#ifdef __cplusplus
}
#endif
#endif /* crypt.h */
EOF
  CRYPT_H="$CONDA_PREFIX/include/crypt.h"
fi
echo "Using crypt.h at: $CRYPT_H"

# Ensure header is on the include path for python ext build
export CFLAGS="-I$(dirname $CRYPT_H) ${CFLAGS:-}"
export CPPFLAGS="-I$(dirname $CRYPT_H) ${CPPFLAGS:-}"

cd "$PROJDIR/amr_build"
# Clean PyMFEM partial build
if [ -d PyMFEM ]; then
  echo "Cleaning prior PyMFEM build artifacts ..."
  rm -rf PyMFEM
fi
git clone -b drl4amr https://github.com/mfem/PyMFEM.git
cd PyMFEM
git checkout 44bda2efadab39a15225532e4cff62bbcfc38ac0

mfem_prefix="$PROJDIR/amr_build/mfem/mfem/"
mfem_source="$PROJDIR/amr_build/mfem/"

# Use a more modest --parallel (was 254 by default, that's nproc)
NPROC=$(($(nproc)/4))
echo "Building PyMFEM with --parallel $NPROC ..."
python setup.py install --mfem-prefix=$mfem_prefix --mfem-source=$mfem_source --no-parallel 2>&1 | tail -120 || {
  echo "PyMFEM install failed; trying serial build with explicit flags"
  python setup.py build_ext --inplace 2>&1 | tail -60
}

cd "$PROJDIR/marl-amr"
pip install -e . 2>&1 | tail -10

echo "=== smoke checks ==="
python -c "import mfem.ser as mfem; print('PyMFEM ser OK, version:', mfem.__file__)" 2>&1
python -c "from marl_amr.envs.solvers.AdvectionSolver import AdvectionSolver; print('AdvectionSolver:', AdvectionSolver.name)" 2>&1
python -c "import tensorflow as tf; print('TF', tf.__version__)" 2>&1

echo "=== $(date -Is) done ==="
