#!/bin/bash
# Master script for 2D GaN replication (OSTI 1484740)
# Runs on spark-36ac (aarch64 Ubuntu 24.04 with QE installed)

set -e
BASEDIR="$HOME/replication"
PSEUDO="$BASEDIR/pseudopotentials"
INPUTS="$BASEDIR/inputs"
OUTPUTS="$BASEDIR/outputs"

mkdir -p $OUTPUTS/{monolayer_relax,monolayer_scf,monolayer_bands,bilayer_relax,bilayer_scf,bilayer_bands}

NPROC=$(nproc)
echo "Running with $NPROC processors"

# Step 1: Monolayer relaxation
echo "=== Step 1: Monolayer vc-relax ==="
cd $BASEDIR
mpirun -np $NPROC pw.x -input $INPUTS/monolayer_relax.in > $OUTPUTS/monolayer_relax.out 2>&1
echo "Monolayer relax done"

# Extract relaxed coordinates
echo "Extracting relaxed coordinates..."
python3 $BASEDIR/scripts/extract_coords.py $OUTPUTS/monolayer_relax.out monolayer

# Step 2: Monolayer SCF with relaxed coordinates
echo "=== Step 2: Monolayer SCF ==="
mpirun -np $NPROC pw.x -input $INPUTS/monolayer_scf_relaxed.in > $OUTPUTS/monolayer_scf.out 2>&1
echo "Monolayer SCF done"

# Step 3: Monolayer band structure
echo "=== Step 3: Monolayer bands ==="
mpirun -np $NPROC pw.x -input $INPUTS/monolayer_bands_relaxed.in > $OUTPUTS/monolayer_bands.out 2>&1
echo "Monolayer bands done"

# Step 4: Process bands
echo "=== Step 4: Process monolayer bands ==="
mpirun -np $NPROC bands.x -input $INPUTS/monolayer_bands_pp.in > $OUTPUTS/monolayer_bands_pp.out 2>&1
echo "Monolayer bands processing done"

# Step 5: Bilayer relaxation
echo "=== Step 5: Bilayer vc-relax ==="
mpirun -np $NPROC pw.x -input $INPUTS/bilayer_relax.in > $OUTPUTS/bilayer_relax.out 2>&1
echo "Bilayer relax done"

# Extract relaxed coordinates
python3 $BASEDIR/scripts/extract_coords.py $OUTPUTS/bilayer_relax.out bilayer

# Step 6: Bilayer SCF
echo "=== Step 6: Bilayer SCF ==="
mpirun -np $NPROC pw.x -input $INPUTS/bilayer_scf_relaxed.in > $OUTPUTS/bilayer_scf.out 2>&1
echo "Bilayer SCF done"

# Step 7: Bilayer bands
echo "=== Step 7: Bilayer bands ==="
mpirun -np $NPROC pw.x -input $INPUTS/bilayer_bands_relaxed.in > $OUTPUTS/bilayer_bands.out 2>&1
echo "Bilayer bands done"

# Step 8: Process bilayer bands
echo "=== Step 8: Process bilayer bands ==="
mpirun -np $NPROC bands.x -input $INPUTS/bilayer_bands_pp.in > $OUTPUTS/bilayer_bands_pp.out 2>&1

# Step 9: PDOS for monolayer
echo "=== Step 9: Monolayer PDOS ==="
mpirun -np $NPROC projwfc.x -input $INPUTS/monolayer_pdos.in > $OUTPUTS/monolayer_pdos.out 2>&1

echo "=== All calculations complete ==="
