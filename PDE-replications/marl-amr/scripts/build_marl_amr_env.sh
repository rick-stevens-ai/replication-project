#!/bin/bash
# Build marl-amr env on uicgpu. Logs to /data/stevens/projects-active/marl-amr/build.log
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/build.log
mkdir -p "$PROJDIR"
cd "$PROJDIR"

exec > >(tee -a "$LOG") 2>&1

echo "=== $(date -Is) start ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh

# Step 1: create env if missing
if ! conda env list | grep -q "^marlamr "; then
  echo "Creating conda env marlamr (python 3.6) ..."
  conda create -y -n marlamr -c conda-forge python=3.6 swig=4.0.2 cmake make gxx_linux-64=9 gcc_linux-64=9
fi
conda activate marlamr

# Step 2: clone repo into /data
if [ ! -d "$PROJDIR/marl-amr" ]; then
  git clone https://github.com/LLNL/marl-amr.git "$PROJDIR/marl-amr"
fi

# Step 3: clone & build MFEM (custom branch) into PROJDIR/amr_build
mkdir -p "$PROJDIR/amr_build"
cd "$PROJDIR/amr_build"
if [ ! -d mfem ]; then
  echo "Cloning MFEM drl4amr-advection branch ..."
  git clone -b drl4amr-advection https://github.com/mfem/mfem.git
  cd mfem
  git checkout 4127f77bbf4d04680b3f9193ac30e09b7c23d2a9
  echo "Compiling MFEM serial ..."
  make serial MFEM_SHARED=YES -j$(nproc) 2>&1 | tail -100
  make install -j$(nproc) 2>&1 | tail -30
  cd ..
fi

# Step 4: pip install python deps. Use a slim subset first to detect TF wheel availability
cd "$PROJDIR/marl-amr"
pip install --upgrade pip setuptools wheel 2>&1 | tail -5
echo "=== Attempting full requirements.txt install ==="
pip install -r requirements.txt 2>&1 | tail -60 || {
  echo "FULL requirements.txt failed; trying minimal subset for inference only."
  pip install numpy==1.19.5 tensorflow==1.14.0 tensorflow-probability==0.7.0 \
              dm-sonnet==1.35 dm-tree==0.1.6 graph-nets==1.0.4 \
              networkx==2.5.1 matplotlib==3.3.4 pandas==1.1.5 scipy==1.5.4 \
              gym==0.18.0 ray==1.5.1 PyYAML==5.4.1 absl-py 2>&1 | tail -40
}

# Step 5: install PyMFEM custom branch
cd "$PROJDIR/amr_build"
if [ ! -d PyMFEM ]; then
  git clone -b drl4amr https://github.com/mfem/PyMFEM.git
  cd PyMFEM
  git checkout 44bda2efadab39a15225532e4cff62bbcfc38ac0
  mfem_prefix="$PROJDIR/amr_build/mfem/mfem/"
  mfem_source="$PROJDIR/amr_build/mfem/"
  python setup.py install --mfem-prefix=$mfem_prefix --mfem-source=$mfem_source 2>&1 | tail -80
  cd ..
fi

# Step 6: install repo as editable
cd "$PROJDIR/marl-amr"
pip install -e . 2>&1 | tail -10

# Step 7: smoke check
python -c "from marl_amr.envs.solvers.AdvectionSolver import AdvectionSolver; print('OK solver:', AdvectionSolver.name)" 2>&1
python -c "import tensorflow as tf; print('TF', tf.__version__)" 2>&1

echo "=== $(date -Is) done ==="
