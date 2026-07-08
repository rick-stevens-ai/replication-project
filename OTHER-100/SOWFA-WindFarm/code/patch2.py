#!/usr/bin/env python3
"""Second patch: drop yaw arg for TwoWT, py_wake 2.6.11 surrogate doesn't accept it."""
p = '/data/stevens/sowfa_windfarm/windfarm-gnn/graph_farms/pywake_sim.py'
with open(p) as f:
    src = f.read()

old = '''    farm_sim = wf_model(x, y,  # wind turbine positions
                            wd=wd,  # Wind direction 'time series'
                            ws=ws,  # Wind speed 'time series'
                            TI=ti/100,  # Turbulence intensity 'time series'
                            yaw=yaw,  # yaw angles 'time series'
                            Alpha=alpha, # shear exponent 'time series'
                            time=True,  # time stamps
                            )'''

new = '''    # py_wake 2.6.11: IEA34_130_2WT_Surrogate does not accept 'yaw' input
    # (loadFunction expects TI, dw_ijlk, hcw_ijlk; optional Alpha). Drop yaw for TwoWT.
    _call_kwargs = dict(
        wd=wd, ws=ws, TI=ti/100, Alpha=alpha, time=True,
    )
    if loads_method == 'OneWT':
        _call_kwargs['yaw'] = yaw
    farm_sim = wf_model(x, y, **_call_kwargs)'''

assert old in src, "old block not found"
src = src.replace(old, new)

with open(p, 'w') as f:
    f.write(src)
print("Patched")
