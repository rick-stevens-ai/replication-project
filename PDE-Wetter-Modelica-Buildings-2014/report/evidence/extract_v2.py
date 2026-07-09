#!/usr/bin/env python3
"""Extract results from OpenModelica .mat output; column-major name matrix."""
import numpy as np
from scipy.io import loadmat
import sys, json

path = sys.argv[1]
m = loadmat(path, chars_as_strings=True, matlab_compatible=True)

raw = m['name']  # (44, n_vars) — each column is one variable name
n_vars = raw.shape[1]
names = []
for j in range(n_vars):
    col = raw[:, j]
    s = ''.join([str(c) for c in col]).strip('\x00 ')
    names.append(s)

dataInfo = m['dataInfo']  # shape (4, n_vars): rows = [dataMatrix, dataIndex, ?, ?]
d1 = m.get('data_1')  # (n_params, 2): parameters at start/end
d2 = m.get('data_2')  # (n_traj+1, n_times): row 0 is time

print(f"n_vars={n_vars}, dataInfo shape={dataInfo.shape}")
print(f"d1 shape={None if d1 is None else d1.shape}, d2 shape={None if d2 is None else d2.shape}")
print(f"Sample names: {names[:5]}")

name_to_loc = {}
for i, nm in enumerate(names):
    dm = int(dataInfo[0, i])
    di = int(dataInfo[1, i])
    name_to_loc[nm] = (dm, di)

def get_series(name):
    if name not in name_to_loc:
        return None, None
    dm, di = name_to_loc[name]
    mat = d1 if dm == 1 else d2
    if mat is None:
        return None, None
    sign = 1
    if di < 0:
        di = -di
        sign = -1
    row = mat[di-1, :] * sign
    if dm == 2:
        time = d2[0, :]
    else:
        time = d1[0, :] if d1 is not None else np.array([0, 1])
    return time, row

# Search for interesting variables
targets = {
    'time': None,
    'zone_T': None,
    'weather_TDryBul': None,
    'heater_Q_flow': None,
    'radiator_Q_flow': None,
    'wall_T': None,
    'floor_T': None,
    'weather_HGloHor': None,  # solar
}

# Scan names
zone_T_cands = [nm for nm in names if 'zon' in nm.lower() and nm.endswith('.T')]
tdry_cands = [nm for nm in names if 'tdrybul' in nm.lower()]
q_cands = [nm for nm in names if nm.endswith('.Q_flow') and '.' in nm]
solar_cands = [nm for nm in names if 'HGloHor' in nm or 'HDifHor' in nm or 'HDirNor' in nm]

print("\n=== Zone T candidates ===")
for c in zone_T_cands[:10]:
    t, y = get_series(c)
    if y is not None:
        print(f"  {c}: len={len(y)}, min={y.min():.2f}, max={y.max():.2f}, mean={y.mean():.2f}")
print("\n=== TDryBul candidates ===")
for c in tdry_cands[:10]:
    t, y = get_series(c)
    if y is not None:
        print(f"  {c}: len={len(y)}, min={y.min():.2f}, max={y.max():.2f}, mean={y.mean():.2f}")
print("\n=== Q_flow candidates (first 15) ===")
for c in q_cands[:15]:
    t, y = get_series(c)
    if y is not None:
        integ = np.trapz(y, t) if len(t)>1 else 0
        print(f"  {c}: mean={y.mean():.1f} W, integrated={integ/3.6e6:.2f} kWh")

# Best canonical vars for a SimpleHouse
def pick_best(cands):
    if not cands: return None
    # prefer the shortest name (usually the top-level one, e.g. 'zon.T' over 'zon.vol.T')
    return sorted(cands, key=len)[0]

canonical = {
    'zon.T': pick_best(zone_T_cands),
    'weaBus.TDryBul': next((nm for nm in tdry_cands if 'weaBus' in nm and 'weaDat' not in nm), None) or (tdry_cands[0] if tdry_cands else None),
    'heaWat.Q_flow': next((nm for nm in q_cands if nm.startswith('heaWat.')), None),
    'rad.Q_flow': next((nm for nm in q_cands if nm.startswith('rad.') and nm.count('.')==1), None),
    'solar_HGloHor': next((nm for nm in solar_cands if 'HGloHor' in nm and 'weaBus' in nm and 'weaDat' not in nm), None) or (solar_cands[0] if solar_cands else None),
}

# Summary
summary = {'library': 'Buildings 14.0.0 (git a131864, 2026-05-04)',
           'openmodelica': '1.22.0',
           'model': 'Buildings.Examples.SimpleHouse',
           'run': path,
           }
for label, nm in canonical.items():
    if nm is None:
        summary[label] = {'error': 'not found'}
        continue
    t, y = get_series(nm)
    if t is None or len(t) < 2:
        summary[label] = {'name': nm, 'error': 'no data'}
        continue
    entry = {
        'name': nm,
        'n_samples': int(len(t)),
        't_start': float(t[0]),
        't_end': float(t[-1]),
        'min': float(y.min()),
        'max': float(y.max()),
        'mean': float(y.mean()),
    }
    if 'Q_flow' in label or 'HGloHor' in label:
        integ = float(np.trapz(y, t))
        entry['integrated'] = integ
        entry['integrated_kWh_per_m2'] = integ / 3.6e6
    if label.startswith('zon.T') or label == 'weaBus.TDryBul':
        # heating degree hours
        yC = y - 273.15
        entry['mean_C'] = float(yC.mean())
        entry['min_C'] = float(yC.min())
        entry['max_C'] = float(yC.max())
    summary[label] = entry

# Compute HDD/CDD from TDryBul
if canonical.get('weaBus.TDryBul') and canonical['weaBus.TDryBul'] in name_to_loc:
    t, y = get_series(canonical['weaBus.TDryBul'])
    yC = y - 273.15
    if t[-1] >= 30 * 86400:  # at least a month
        # daily mean
        n_days = int(t[-1] // 86400)
        daily_t = np.arange(0, n_days * 86400, 86400)
        daily_T = np.interp(daily_t, t, yC)
        HDD_18 = float(np.sum(np.maximum(18.3 - daily_T, 0)))
        CDD_18 = float(np.sum(np.maximum(daily_T - 18.3, 0)))
        summary['climate_ChicagoOHare'] = {
            'n_days_analyzed': n_days,
            'HDD_base_18.3C': HDD_18,
            'CDD_base_18.3C': CDD_18,
            'mean_annual_C': float(yC.mean()),
        }

print("\n=== SUMMARY ===")
print(json.dumps(summary, indent=2))

with open(path + '.summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print(f"\nWritten: {path}.summary.json")
