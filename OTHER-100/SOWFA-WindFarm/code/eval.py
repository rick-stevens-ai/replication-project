#!/usr/bin/env python3
"""Evaluation: per-channel R², MAE, RMSE, MAPE for the trained GEN-4 model.
   Output: JSON metrics dump + console table. Also: inference timing vs PyWake."""
import sys, os, json, time
sys.path.insert(0, '/data/stevens/sowfa_windfarm/windfarm-gnn/gnn_framework')
import numpy as np
import torch
from torch_geometric.loader import DataLoader
from box import Box
import yaml
from data import GraphFarmsDataset
from models import WindFarmGNN

run_dir = sorted([d for d in os.listdir('/data/stevens/sowfa_windfarm/runs')
                  if d.startswith('GEN_')])[-1]
trained_dir = f'/data/stevens/sowfa_windfarm/runs/{run_dir}'
test_path = '/data/stevens/sowfa_windfarm/dataset/test/TwoWT/delaunay'

print(f"trained_dir: {trained_dir}")
print(f"test_path: {test_path}")

config = Box.from_yaml(filename=os.path.join(trained_dir, 'config.yml'), Loader=yaml.FullLoader)
test_dataset = GraphFarmsDataset(root_path=test_path, rel_wd=config.hyperparameters.rel_wd)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)
print(f"test_dataset n={len(test_dataset)}")

model = WindFarmGNN(**config.hyperparameters, **config.model_settings)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
ckpt = torch.load(os.path.join(trained_dir, 'trained_models/best.pt'),
                  map_location=device, weights_only=False)
model.trainset_stats = ckpt['trainset_stats']
model.load_state_dict(ckpt['model_state_dict'])
model.to(device); model.eval()

CHANNELS = ['power_W', 'rotor_avg_ws_mps', 'TI_eff',
            'DEL_blade_flap', 'DEL_blade_edge',
            'DEL_tower_top_torsion', 'DEL_tower_bottom_fa', 'DEL_tower_bottom_ss']

y_all, yhat_all = [], []
inf_times = []
with torch.no_grad():
    # warmup
    for i, d in enumerate(test_loader):
        d = d.to(device); _ = model(d, denorm_output=True); break
    if torch.cuda.is_available(): torch.cuda.synchronize()
    for i, data in enumerate(test_loader):
        data = data.to(device)
        if torch.cuda.is_available(): torch.cuda.synchronize()
        t0 = time.perf_counter()
        data = model(data, denorm_output=True)
        if torch.cuda.is_available(): torch.cuda.synchronize()
        inf_times.append(time.perf_counter() - t0)
        y_all.append(data.y.cpu().numpy())
        yhat_all.append(data.x.cpu().numpy())

y = np.concatenate(y_all, axis=0)       # [N_total_nodes, 8]
yhat = np.concatenate(yhat_all, axis=0)
print(f"\nN samples (graphs) = {len(test_dataset)}, N total nodes = {y.shape[0]}")

# Per-channel metrics
metrics = {}
print(f"\n{'channel':<25} {'R²':>8} {'MAE':>14} {'RMSE':>14} {'MAPE':>9}")
print("-" * 75)
for j, name in enumerate(CHANNELS):
    yj, yhj = y[:, j], yhat[:, j]
    ss_res = ((yj - yhj) ** 2).sum()
    ss_tot = ((yj - yj.mean()) ** 2).sum()
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float('nan')
    mae = float(np.mean(np.abs(yj - yhj)))
    rmse = float(np.sqrt(np.mean((yj - yhj) ** 2)))
    eps = max(1e-9, np.median(np.abs(yj)) * 1e-6)
    mape = float(np.mean(np.abs((yj - yhj) / np.maximum(np.abs(yj), eps)))) * 100
    metrics[name] = dict(r2=r2, mae=mae, rmse=rmse, mape_pct=mape, y_mean=float(yj.mean()), y_std=float(yj.std()))
    print(f"{name:<25} {r2:>8.4f} {mae:>14.4g} {rmse:>14.4g} {mape:>8.2f}%")

mean_r2 = float(np.mean([m['r2'] for m in metrics.values()]))
print(f"\nMean R² (all channels): {mean_r2:.4f}")
inf_mean_ms = float(np.mean(inf_times[1:]) * 1000)
inf_p50 = float(np.percentile(inf_times[1:], 50) * 1000)
print(f"\nInference timing: mean {inf_mean_ms:.2f} ms/graph (median {inf_p50:.2f} ms) over {len(inf_times)-1} test graphs on {device}")

out = dict(
    trained_dir=trained_dir,
    test_path=test_path,
    n_test_graphs=len(test_dataset),
    n_test_nodes=int(y.shape[0]),
    channels=CHANNELS,
    metrics=metrics,
    mean_r2=mean_r2,
    inference_ms_per_graph_mean=inf_mean_ms,
    inference_ms_per_graph_p50=inf_p50,
    device=str(device),
    n_trainable_params=int(sum(p.numel() for p in model.parameters() if p.requires_grad)),
)
out_path = '/data/stevens/sowfa_windfarm/eval_metrics.json'
with open(out_path, 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nWrote {out_path}")
