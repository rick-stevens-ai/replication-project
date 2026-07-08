#!/bin/bash

set -e
set -o pipefail

mkdir -p out/plot

sinter plot \
    --title "Comparing X, Y, and Z basis memory experiment error rates" \
    --xaxis "Patch diameter (d)" \
    --in "out/stats.csv" \
    --x_func "metadata['d']" \
    --group_func "f'''b={metadata['b']} p={metadata['p']} mem_rounds={'d' if metadata['r'] == metadata['d'] else str(metadata['r'] / metadata['d']) + '*d'} pad_rounds={'0' if metadata['rb'] == 0 else '⌊d/2⌋' if metadata['rb'] == metadata['d'] // 2 else '2d' if metadata['rb'] == metadata['d'] * 2 else '?'} noise={metadata['noise']}'''" \
    --filter_func "metadata['b'] in ['X', 'Y', 'Z', 'Y_folded'] and metadata['r'] == metadata['d'] and metadata['rb'] == (metadata['d'] // 2 if metadata['b'] == 'Y' else 0)" \
    --plot_args_func "{'color': 'C0' if metadata['b'] == 'X' else 'C1' if metadata['b'] == 'Y' else 'C2' if metadata['b'] == 'Z' else 'gray', 'linestyle': '--' if 'folded' in metadata['b'] else '-'}" \
    --out out/plot/error_rate.png &

sinter plot \
    --title "Benefits of padding saturate around d/2 rounds" \
    --xaxis "Number of padding rounds" \
    --in "out/stats.csv" \
    --x_func "metadata['rb']" \
    --group_func "f'''b={metadata['b']} d={metadata['d']} mem_rounds={'d' if metadata['r'] == metadata['d'] else str(metadata['r'] / metadata['d']) + '*d'} noise={metadata['noise']} p={metadata['p']}'''" \
    --filter_func "metadata['p'] == 0.001 and metadata['r'] == metadata['d'] and metadata['d'] in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21] and metadata['b'] == 'Y'" \
    --out out/plot/pad_saturation.png &

sinter plot \
    --title "Braiding experiment has a timelike error mechanism crossing memory rounds" \
    --xaxis "Number of memory rounds" \
    --in "out/stats.csv" \
    --ymin 1e-10 \
    --group_func "f'''braid={'braid' in metadata['b']} d={metadata['d']} noise={metadata['noise']} p={metadata['p']} pad_rounds=⌊d/2⌋'''" \
    --x_func "metadata['r']" \
    --filter_func "metadata['r'] <= 10 and metadata['d'] in [9, 15] and metadata['p'] == 0.001 and metadata['b'] in ['Y', 'Y_braid'] and metadata['rb'] == metadata['d'] // 2" \
    --plot_args_func "{'color': 'C0' if metadata['d'] == 9 else 'C1', 'linestyle': '-' if 'braid' in metadata['b'] else '--'}" \
    --out out/plot/braiding.png &

sinter plot \
    --title "Comparing idle rounds to the transition round using noiseless time boundaries" \
    --xaxis "Patch diameter (d)" \
    --in "out/stats.csv" \
    --x_func "metadata['d']" \
    --group_func "f'''{metadata['b'].replace('_magic', '')} p={metadata['p']} mem_rounds={metadata['r']} pad_rounds={metadata['rb']} noise={metadata['noise']}'''" \
    --filter_func "'magic' in metadata['b']" \
    --plot_args_func "{'color': 'C0' if metadata['b'] == 'X_magic_idle' else 'C1' if metadata['b'] == 'Y_magic_idle' else 'C2' if metadata['b'] == 'Z_magic_idle' else 'C3'}" \
    --out out/plot/round_error_rate.png &

#sinter plot \
#    --title "Detection Event Fraction of SI1000 Noise Model" \
#    --in out/det_frac_stats.csv \
#    --x_func "metadata['p']" \
#    --xaxis "[log]noise strength (p)" \
#    --group_func "f'''b={metadata['b']} d={metadata['d']} mem_rounds={'d' if metadata['r'] == metadata['d'] else str(metadata['r'] / metadata['d']) + '*d'} pad_rounds={'0' if metadata['rb'] == 0 else '⌊d/2⌋' if metadata['rb'] == metadata['d'] // 2 else '2d' if metadata['rb'] == metadata['d'] * 2 else '?'} noise={metadata['noise']}'''" \
#    --yaxis "[log]Detection Event Fraction" \
#    --filter_func "metadata['b'] in 'XYZ' and metadata['r'] == metadata['d'] and metadata['rb'] == (metadata['d'] // 2 if metadata['b'] == 'Y' else 0) and metadata['d'] == 9" \
#    --ymin 1e-3 \
#    --out out/plot/det_frac.png &

wait
