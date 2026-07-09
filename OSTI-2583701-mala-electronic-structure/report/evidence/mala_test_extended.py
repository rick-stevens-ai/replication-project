#!/usr/bin/env python
"""
Extended MALA replication test.
- Load pretrained Be_model from test-data
- Test on all available snapshots (0-3)
- Compute band_energy MAE and density MAPE relative to DFT reference
- Also compare with reference DFT band_energy from info.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, '/data/stevens/mala-repl/mala')
import mala
from mala import printout

MALA_DATA_REPO = "/data/stevens/mala-repl/test-data"
data_path_be = os.path.join(MALA_DATA_REPO, "Be2")

# Load pretrained model
parameters, network, data_handler, tester = mala.Tester.load_run(
    run_name="Be_model", path=data_path_be
)
tester.observables_to_test = ["band_energy", "density"]
tester.output_format = "list"
parameters.data.use_lazy_loading = True

# Add test snapshots 0-3 (0,1 typically used for train/val; 2,3 test)
for snap_id in [0, 1, 2, 3]:
    data_handler.add_snapshot(
        f"Be_snapshot{snap_id}.in.npy",
        data_path_be,
        f"Be_snapshot{snap_id}.out.npy",
        data_path_be,
        "te",
        calculation_output_file=os.path.join(data_path_be, f"Be_snapshot{snap_id}.info.json"),
    )

data_handler.prepare_data(reparametrize_scaler=False)
results = tester.test_all_snapshots()

# Load DFT reference values
dft_refs = []
for snap_id in [0, 1, 2, 3]:
    with open(os.path.join(data_path_be, f"Be_snapshot{snap_id}.info.json")) as f:
        info = json.load(f)
    dft_refs.append({
        "snapshot": snap_id,
        "band_energy_dft_eV": info["band_energy_dft_calculation"],
        "total_energy_dft_eV": info["total_energy_dft_calculation"],
        "n_atoms": len(info["atoms"]["numbers"]),
        "fermi_energy_dft": info["fermi_energy_dft"],
        "T_K": info["temperature"],
    })

# Print + save summary
summary = {
    "model": "Be_model (test-data pretrained, 2-atom Be cell)",
    "test_snapshots": [0, 1, 2, 3],
    "raw_results": {k: [float(v) for v in vals] for k, vals in results.items()},
    "band_energy_MAE_meV_per_atom": {
        f"snapshot{i}": abs(float(v)) for i, v in enumerate(results["band_energy"])
    },
    "density_MAPE_pct": {
        f"snapshot{i}": float(v)*100 for i, v in enumerate(results["density"])
    },
    "dft_reference": dft_refs,
    "paper_thresholds": {
        "accuracy_threshold_meV_per_atom": 10.0,
        "chemical_accuracy_meV_per_atom": 43.4,
        "density_MAPE_target_pct": 1.0,
    },
    "notes": (
        "Be_model is the small 2-atom Be demo model shipped with mala-project/test-data. "
        "It is NOT the paper's production model (which uses 128- or 256-atom cells). "
        "The paper's production models achieve <10 meV/atom for total energy and "
        "<10 meV/atom band energy for aluminum/beryllium/boron. This demo model is trained "
        "on much less data and only illustrates the pipeline works."
    ),
}
print(json.dumps(summary, indent=2))

# Also compute mean/max
be = [abs(float(v)) for v in results["band_energy"]]
dp = [float(v)*100 for v in results["density"]]
print()
print(f"Band energy |error| — mean: {np.mean(be):.3f} meV/atom, max: {np.max(be):.3f} meV/atom")
print(f"Density MAPE — mean: {np.mean(dp):.4f}%, max: {np.max(dp):.4f}%")

with open("/data/stevens/mala-repl/replication_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
