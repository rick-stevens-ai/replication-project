#!/usr/bin/env python3
"""Patch pywake_sim.py to work with py_wake 2.6.11 where TensorflowSurrogate is renamed/removed.

Strategy: drop the local IEA34_130_1WT_Surrogate redefinition and import the upstream one.
The upstream class uses TI_eff vs TI - for the TwoWT loads model (default) this is irrelevant.
For OneWT use the upstream version; the small input-parser difference won't affect our metric
comparisons because we only use TwoWT by default.
"""
import sys, re
p = '/data/stevens/sowfa_windfarm/windfarm-gnn/graph_farms/pywake_sim.py'
with open(p) as f:
    src = f.read()

# Remove the import of TensorflowSurrogate, add IEA34_130_1WT_Surrogate to upstream import
src = src.replace(
    "from py_wake.examples.data.iea34_130rwt._iea34_130rwt import IEA34_130_Base, IEA34_130_2WT_Surrogate, ThreeRegionLoadSurrogates, IEA34_130_PowerCtSurrogate",
    "from py_wake.examples.data.iea34_130rwt._iea34_130rwt import IEA34_130_Base, IEA34_130_1WT_Surrogate as _IEA34_130_1WT_Surrogate_upstream, IEA34_130_2WT_Surrogate, ThreeRegionLoadSurrogates, IEA34_130_PowerCtSurrogate"
)
src = src.replace(
    "from py_wake.utils.tensorflow_surrogate_utils import TensorflowSurrogate\n",
    ""
)

# Replace the local class definition with an alias to the upstream class
new_class = (
"# Original repo redefined IEA34_130_1WT_Surrogate to override TI_eff->TI input parser.\n"
"# In py_wake 2.6.11 the TensorflowSurrogate API was renamed to TensorFlowModel and the\n"
"# construction path changed. For our replication we default to loads_method='TwoWT'\n"
"# (the repo's own default), so we just alias the upstream class for OneWT and document\n"
"# the small semantic difference in REPORT.md.\n"
"IEA34_130_1WT_Surrogate = _IEA34_130_1WT_Surrogate_upstream\n"
)

# Strip the class definition block
import re as _re
src = _re.sub(
    r"# we redefine here the OneWT surrogate.*?IEA34_130_Base\.__init__\(self, powerCtFunction=powerCtFunction, loadFunction=loadFunction\)\n",
    new_class,
    src,
    flags=_re.DOTALL,
)

with open(p, 'w') as f:
    f.write(src)
print("Patched OK")
print("--- head ---")
print('\n'.join(src.splitlines()[:30]))
