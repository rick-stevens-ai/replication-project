#!/usr/bin/env python3
"""Time PyWake (the simulator that produced our training data) on equivalent test farms.
Compare to the trained GNN's inference speed."""
import sys, os, time, json, zipfile, io
sys.path.insert(0, '/data/stevens/sowfa_windfarm/windfarm-gnn/graph_farms')
import numpy as np
import torch
import pandas as pd
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

# Load some test layouts (from the generated test set) and time pywake on them
test_root = '/data/stevens/sowfa_windfarm/dataset/test/TwoWT/delaunay'
zips = sorted(os.listdir(test_root))[:10]   # 10 farms for timing

# Reconstruct positions + inflows from saved graphs
from pywake_sim import simulate_farm

times = []
for zfn in zips:
    z = zipfile.ZipFile(os.path.join(test_root, zfn))
    inner = z.namelist()[0]
    g = torch.load(io.BytesIO(z.open(inner).read()), weights_only=False)
    positions = g.pos.numpy()  # [N, 2]
    ws, wd, ti = float(g.globals[0]), float(g.globals[1]), float(g.globals[2]) * 100  # rescale TI
    inflow_df = pd.DataFrame({
        'u': [ws], 'wd': [wd], 'ti': [ti],
        'hflowang': [0.0], 'shearexp': [0.0],
    })
    # warmup once
    if len(times) == 0:
        _ = simulate_farm(inflow_df, positions, 'TwoWT')
    t0 = time.perf_counter()
    _ = simulate_farm(inflow_df, positions, 'TwoWT')
    times.append(time.perf_counter() - t0)
    print(f"  {zfn[:40]:<42} N={positions.shape[0]:>3} t={times[-1]*1000:.1f} ms")

mean_ms = np.mean(times) * 1000
print(f"\nPyWake mean: {mean_ms:.2f} ms/farm/inflow over {len(times)} farms")
print(f"GNN inference: ~2.44 ms/graph (from eval)")
print(f"GNN speedup vs PyWake: {mean_ms/2.44:.1f}x")

out = dict(pywake_ms_mean=float(mean_ms), pywake_times_ms=[float(t*1000) for t in times],
           gnn_ms_mean=2.44, speedup=float(mean_ms/2.44))
with open('/data/stevens/sowfa_windfarm/timing_pywake.json','w') as f:
    json.dump(out,f,indent=2)
print("\nWrote /data/stevens/sowfa_windfarm/timing_pywake.json")
