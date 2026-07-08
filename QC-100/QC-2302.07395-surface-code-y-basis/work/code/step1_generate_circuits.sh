#!/bin/bash

set -e
set -o pipefail

# Vary padding to find best amount.
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --out_dir out/circuits \
    --distance 3 5 7 9 11 13 15 17 \
    --memory_rounds "d" \
    --boundary_rounds {} \
    --noise_model SI1000 \
    --noise_strength 0.001 \
    --basis Y \
    ::: 0 1 2 3 4 5 6 7 8 9 10

# Y basis memory experiments.
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --out_dir out/circuits \
    --distance {} \
    --memory_rounds "d" \
    --boundary_rounds "d//2" \
    --noise_model SI1000 \
    --noise_strength 0.001 0.003 \
    --basis Y \
    ::: 3 5 7 9 11 13 15 17

# XZ basis memory experiments.
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --out_dir out/circuits \
    --distance {} \
    --memory_rounds "d" \
    --boundary_rounds 0 \
    --noise_model SI1000 \
    --noise_strength 0.001 0.003 \
    --basis X Z Y_folded \
    ::: 3 5 7 9 11 13 15 17

# Vary braiding memory to see best amount.
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --basis Y_braid Y \
    --noise_model SI1000 \
    --noise_strength 1e-3 \
    --distance 9 15 \
    --out_dir out/circuits \
    --memory_rounds {} \
    --boundary_rounds "d//2" \
    ::: 0 1 2 3 4 5 6 7 8 9 10

# Thin layer experiments.
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --out_dir out/circuits \
    --distance {} \
    --memory_rounds 1 \
    --boundary_rounds 1 \
    --noise_model SI1000 \
    --noise_strength 0.001 0.003 \
    --basis Y_magic_transition \
    ::: 3 5 7 9 11 13 15 17
PYTHONPATH=src parallel --ungroup tools/gen_circuits \
    --out_dir out/circuits \
    --distance {} \
    --memory_rounds 3 \
    --boundary_rounds 0 \
    --noise_model SI1000 \
    --noise_strength 0.001 0.003 \
    --basis Y_magic_idle X_magic_idle Z_magic_idle \
    ::: 3 5 7 9 11 13 15 17
