# PVMol-Gen on Polaris

## Quick Start

### 1. Transfer from CherryRd to Polaris
```bash
# From CherryRd (or any machine with access):
rsync -avz --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' \
  ~/projects/replicate/ stevens@polaris.alcf.anl.gov:~/pvmol-gen/
```

### 2. Setup (run once on Polaris login node)
```bash
bash ~/pvmol-gen/polaris/setup.sh
```

### 3. Submit test jobs
```bash
# Stage 1: Classifier 5-fold CV (~10-15 min on A100)
qsub ~/pvmol-gen/polaris/test_stage1.pbs

# Stage 2: GPT-2 fine-tune + generation (after Stage 1 passes)
qsub ~/pvmol-gen/polaris/test_stage2.pbs

# Check status
qstat -u stevens
```

### 4. Check results
```bash
cat ~/pvmol-gen/logs/stage1_test.out
ls ~/pvmol-gen/results/
```

## Allocation
- Project: AmSC_Demos
- Queue: debug (1 node, 1 hr max, 1 job at a time)

## Node Resources (debug queue, 1 node)
- 4× NVIDIA A100 (40GB each)
- 1× AMD EPYC 7543P (32 cores)
- 512 GB RAM
