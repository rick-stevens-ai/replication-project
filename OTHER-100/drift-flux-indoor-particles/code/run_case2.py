#!/usr/bin/env python3
"""Run Case 2 (U=0.45 m/s) with OpenFOAM fields."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from run_complete_replication import run_case

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')
fields_dir = os.path.join(BASE, 'data/openfoam_fields_case2')

import time
t0 = time.time()
run_case(0.45, fields_dir=fields_dir)
print(f"\nCase 2 total wall time: {time.time()-t0:.1f}s")
