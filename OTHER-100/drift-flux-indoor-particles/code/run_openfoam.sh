#!/bin/bash
# Run OpenFOAM steady-state airflow simulation
# Must be run from the openfoam/ case directory

set -e

echo "=== Drift-Flux Replication: OpenFOAM Airflow ==="
echo "Working directory: $(pwd)"

# Generate mesh
echo "--- Generating mesh ---"
blockMesh

echo "--- Checking mesh ---"
checkMesh

# Run steady-state solver (simpleFoam with RNG k-epsilon)
echo "--- Running simpleFoam ---"
simpleFoam

echo "--- Post-processing ---"
# Extract velocity profiles at validation locations
postProcess -func "sampleDict" -latestTime 2>/dev/null || echo "sampleDict not configured yet"

echo "=== Airflow simulation complete ==="
