#!/usr/bin/env python
"""Driver: run full NILC pipeline."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src import pipeline

t0 = time.time()
pipeline.run_pipeline('data')
print(f'Total wall time: {time.time()-t0:.1f} s')
