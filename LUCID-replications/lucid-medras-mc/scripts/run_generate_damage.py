"""
Step 1: Generate DNA damage SDD files for X-rays, protons, and carbon ions
using the public Medras-MC damageModel.basicXandIon() entry point.

Reproduces the canonical demo dataset used by McMahon & Prise's Medras-MC repo:
  - Photons (Z=0), doses 1,2,3,4,6,8 Gy
  - Protons (Z=1) at 10 LETs from 1.77 to 29.78 keV/um, 1 Gy each
  - Carbon ions (Z=6) at 7 LETs from 20.29 to 512 keV/um, 1 Gy each

We use runs=20 per condition to get reasonable statistics in a few minutes.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "Medras-MC"))
OUTDIR = os.path.normpath(os.path.join(HERE, "..", "results", "sdd_basicXandIon"))

# Make sure we import the repo's packages
sys.path.insert(0, REPO)
os.makedirs(OUTDIR, exist_ok=True)
os.chdir(OUTDIR)  # damageModel writes SDD files into cwd

from damagegenerator import damageModel

start = time.time()
print("Generating SDD damage files into:", OUTDIR)
damageModel.basicXandIon(runs=20)
print(f"Done. Elapsed: {time.time() - start:.1f} s")

# List what we generated
files = sorted(f for f in os.listdir(OUTDIR) if f.endswith(".txt"))
print(f"\nGenerated {len(files)} SDD files:")
for f in files:
    print(" ", f)
