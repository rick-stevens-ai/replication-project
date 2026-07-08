#!/bin/bash
#PBS -N ala_all_chunks
#PBS -l select=1
#PBS -l walltime=01:00:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home
#PBS -r y

# Run all 8 chunks sequentially in one Aurora job.
# Each chunk checkpoints independently — on preemption/timeout,
# resubmit and completed chunks are skipped automatically.
N_CHUNKS=8

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL

mkdir -p logs

echo "=== Aurora All-Chunks — $(hostname) — $(date) ==="

for i in $(seq 0 $((N_CHUNKS - 1))); do
    # Skip if chunk already has final output
    if [ -f "data/alanine_short/dihedrals_chunk${i}.npz" ]; then
        echo "Chunk $i: already complete, skipping"
        continue
    fi
    echo "--- Chunk $i starting at $(date) ---"
    python src/alanine_dipeptide_chunk.py $i $N_CHUNKS 2>&1 | tee -a logs/aurora_allchunks_$(date +%Y%m%d).log
    echo "--- Chunk $i done at $(date) ---"
done

echo "=== All chunks finished at $(date) ==="
