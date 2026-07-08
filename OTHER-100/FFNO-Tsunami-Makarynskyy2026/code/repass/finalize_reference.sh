#!/bin/bash
# Re-aggregate after Reference inference completes and pull summary back to Dropbox.
set -e

ssh uicgpu '/data/stevens/CAMELS/.venv/bin/python /data/stevens/tsunami/code/repass/aggregate_new_claims.py \
    --selected_root  /data/stevens/tsunami/results \
    --reference_root /data/stevens/tsunami/results_reference \
    --selected_table /data/stevens/tsunami/results/ja/table1_metrics_summary.csv \
    --reference_table /data/stevens/tsunami/results_reference/ja/table1_metrics_summary.csv \
    --out /data/stevens/tsunami/results_reference/repass_all_claims.json'

scp uicgpu:/data/stevens/tsunami/results_reference/repass_all_claims.json \
    /Users/stevens/Dropbox/REPLICATE-PROJECT/FFNO-Tsunami-Makarynskyy2026/results/repass/all_claims.json

scp uicgpu:/data/stevens/tsunami/results_reference/ja/table1_metrics_summary.csv \
    /Users/stevens/Dropbox/REPLICATE-PROJECT/FFNO-Tsunami-Makarynskyy2026/results/repass/reference_table1_metrics_summary.csv

scp uicgpu:/data/stevens/tsunami/results_reference/timing.txt \
    /Users/stevens/Dropbox/REPLICATE-PROJECT/FFNO-Tsunami-Makarynskyy2026/results/repass/reference_wallclock.txt

echo "Files pulled to results/repass/. Now manually update REPORT.md §6.2 with reference numbers."
echo ""
echo "Quick-look:"
python3 -c "
import json
d = json.load(open('/Users/stevens/Dropbox/REPLICATE-PROJECT/FFNO-Tsunami-Makarynskyy2026/results/repass/all_claims.json'))
if 'reference_aggregate' not in d:
    print('Reference aggregate missing.')
else:
    ra = d['reference_aggregate']
    for k in ['rmse_eta','rmse_avg','BEE','ATE_min']:
        if k in ra:
            print(f'  Reference {k}: mean={ra[k][\"mean\"]:.4f} std={ra[k][\"std\"]:.4f}')
    rd = d.get('reference_detection',{})
    print(f'  Reference NATE: {rd.get(\"n_with_detection\",\"?\")}/{rd.get(\"n_cases\",\"?\")}')
"
