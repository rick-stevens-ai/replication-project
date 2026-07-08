#!/bin/bash
# Submit 8 parallel chunk jobs on Polaris
# Each chunk handles ~1424 sims — should finish in ~30 min on A100
N_CHUNKS=8

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

for i in $(seq 0 $((N_CHUNKS - 1))); do
    cat > /tmp/ala_chunk_${i}.sh << JOBEOF
#!/bin/bash
#PBS -N ala_chunk_${i}
#PBS -l select=1:ngpus=1
#PBS -l walltime=01:00:00
#PBS -q preemptable
#PBS -A datascience
#PBS -l filesystems=home:eagle
#PBS -r y

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

LOGFILE="logs/chunk_${i}_\$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_chunk.py ${i} ${N_CHUNKS} 2>&1 | tee "\$LOGFILE" &
PID=\$!
trap "kill -TERM \$PID; wait \$PID" SIGTERM SIGUSR1
wait \$PID
JOBEOF
    chmod +x /tmp/ala_chunk_${i}.sh
    JOB=$(qsub /tmp/ala_chunk_${i}.sh)
    echo "Chunk $i: $JOB"
done
