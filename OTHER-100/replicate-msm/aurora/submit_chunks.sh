#!/bin/bash
# Submit 8 parallel chunk jobs on Aurora — draco queue (1-32 nodes, 24h)
N_CHUNKS=8

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

for i in $(seq 0 $((N_CHUNKS - 1))); do
    # Skip if already done
    if [ -f "data/alanine_short/dihedrals_chunk${i}.npz" ]; then
        echo "Chunk $i: already complete, skipping"
        continue
    fi

    cat > /tmp/ala_chunk_${i}.sh << JOBEOF
#!/bin/bash
#PBS -N ala_chunk_${i}
#PBS -l select=1
#PBS -l walltime=02:00:00
#PBS -q capacity
#PBS -A datascience
#PBS -l filesystems=home
#PBS -r y

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL

mkdir -p logs
LOGFILE="logs/chunk_aurora_${i}_\$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_chunk.py ${i} ${N_CHUNKS} 2>&1 | tee "\$LOGFILE" &
PID=\$!
trap "kill -TERM \$PID; wait \$PID" SIGTERM SIGUSR1
wait \$PID
JOBEOF
    chmod +x /tmp/ala_chunk_${i}.sh
    JOB=$(qsub /tmp/ala_chunk_${i}.sh)
    echo "Chunk $i: $JOB"
done
