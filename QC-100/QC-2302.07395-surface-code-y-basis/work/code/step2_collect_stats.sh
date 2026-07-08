#!/bin/bash

set -e
set -o pipefail

sinter collect \
    --decoders pymatching \
    --processes 4 \
    --circuits out/circuits/*.stim \
    --max_shots 1_000_000 \
    --max_errors 100 \
    --save_resume_filepath out/stats.csv \
    --metadata_func auto

# Collect detection fractions (note: wants different circuits than the normally generated ones; want a variety of noise strengths)
#PYTHONPATH=src tools/sample_det_fracs \
#    --circuits out/circuits/* \
#    > out/det_frac_stats.csv

# Collect logical error heat maps.
#PYTHONPATH=src tools/debug_count_logical_error_edges \
#    --circuit "out/circuits/r=3,d=7,p=0.001,noise=SI1000,b=Y_magic_idle,rb=0,q=97.stim" \
#    --out "out/idle_heat_map.svg" \
#    --batch_size 1000000 \
#    --min_errors 10000 \
#    --max_edge_hits_scale 2500
#PYTHONPATH=src tools/debug_count_logical_error_edges \
#    --circuit "out/circuits/r=1,d=7,p=0.001,noise=SI1000,b=Y_magic_transition,rb=1,q=103.stim" \
#    --out "out/transition_heat_map.svg" \
#    --batch_size 1000000 \
#    --min_errors 10000 \
#    --max_edge_hits_scale 2500
