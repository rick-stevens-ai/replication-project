"""
Step 2: Run Medras-MC repair fidelity analysis on the SDD damage files.

We run the canonical 'Fidelity' analysis. medrasrepair prints per-row results
to stdout; we capture the full output and parse the summary section.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "Medras-MC"))
SDD = os.path.normpath(os.path.join(HERE, "..", "results", "sdd_basicXandIon"))

sys.path.insert(0, REPO)
# medrasrepair uses os.listdir on the path; ensure trailing slash
sdd_path = SDD + os.sep

from repairanalysis import medrasrepair

# Tighten / make deterministic-ish: use fewer repeats so the run finishes
# in a reasonable wall time but still has enough samples for trends.
# Default is repeats=50 per exposure; we keep that.
print(f"Running Fidelity repair simulation on: {sdd_path}")
print(f"Settings: repeats={medrasrepair.repeats}, "
      f"repairFailure={medrasrepair.repairFailure}, "
      f"addFociDelay={medrasrepair.addFociDelay}, "
      f"simulationLimit={medrasrepair.simulationLimit}")
start = time.time()
medrasrepair.repairSimulation(sdd_path, "Fidelity")
print(f"\nDone. Elapsed: {time.time() - start:.1f} s")
