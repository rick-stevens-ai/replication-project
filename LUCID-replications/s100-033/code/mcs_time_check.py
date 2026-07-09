#!/usr/bin/env python3
"""s100-033 self-consistency arithmetic checks for the paper's calibrations."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVI = ROOT / "evidence"
EVI.mkdir(exist_ok=True)

# ---- 1) MCS <-> minute calibration -------------------------------------
# Paper claim: 0.4 um/min HUVEC speed corresponds to 0.1 pixel/MCS at 4 um/pixel,
# so 1 MCS = 1 min.
pixel_um = 4.0
huvec_um_per_min = 0.4
huvec_pix_per_min = huvec_um_per_min / pixel_um
sim_pix_per_mcs = 0.1
mcs_per_min = huvec_pix_per_min / sim_pix_per_mcs
min_per_mcs = 1.0 / mcs_per_min

# ---- 2) Cell volume from one voxel -------------------------------------
voxel_volume_um3 = pixel_um ** 3   # 64 um^3

# ---- 3) Hyperfractionation cadence (paper §3.5.3) ----------------------
# "1 MCS approximately equals 1 minute ... so we know that roughly there are
# two doses per day" for 5 doses delivered within 4000 MCS.
fractions = 5
mcs_window = 4000
fx_per_day = fractions / (mcs_window / 60.0 / 24.0)

# ---- 4) Lattice volume / cell count plausibility -----------------------
lattice = (50, 50, 80)
total_voxels = lattice[0] * lattice[1] * lattice[2]
# Tumor cells in CPM occupy multiple voxels each in general; with the paper's
# tumor cell volume = 64 um^3 = 1 voxel as a target volume, max cells = total_voxels.
max_cells_if_1voxel = total_voxels

# ---- 5) MRT geometry: 5 microbeams 200 um apart, beam width 50 um ------
beam_width_um = 50
beam_spacing_um = 200
n_beams = 5
mrt_span_um = (n_beams - 1) * beam_spacing_um + beam_width_um
# lattice extent in beam direction (x or y): 50 vox * 4 um = 200 um
lattice_x_um = lattice[0] * pixel_um
lattice_y_um = lattice[1] * pixel_um

out = {
    "mcs_to_min_calibration": {
        "pixel_um": pixel_um,
        "huvec_speed_um_per_min": huvec_um_per_min,
        "huvec_pix_per_min": huvec_pix_per_min,
        "sim_pix_per_mcs": sim_pix_per_mcs,
        "computed_mcs_per_min": mcs_per_min,
        "computed_min_per_mcs": min_per_mcs,
        "paper_claim": "1 MCS = 1 min",
        "consistent": abs(min_per_mcs - 1.0) < 1e-9,
    },
    "voxel_volume_um3": voxel_volume_um3,
    "voxel_volume_um3_paper_claim": 64,
    "voxel_volume_consistent": voxel_volume_um3 == 64,
    "hyperfractionation_cadence": {
        "fractions": fractions,
        "MCS_window": mcs_window,
        "computed_fractions_per_day": fx_per_day,
        "paper_claim": "roughly two doses per day",
        "consistent": abs(fx_per_day - 1.8) < 0.5,  # 5 fx / (4000/1440 days) = 1.8
    },
    "lattice": {
        "dims": lattice,
        "total_voxels": total_voxels,
        "max_cells_if_1voxel_each": max_cells_if_1voxel,
        "lattice_x_um": lattice_x_um,
        "lattice_y_um": lattice_y_um,
        "lattice_z_um": lattice[2] * pixel_um,
    },
    "mrt_geometry_consistency_warning": (
        "Paper says 5-beam MRT with 200 um c-to-c. "
        f"MRT span needs {mrt_span_um} um but lattice x/y extent is only "
        f"{lattice_x_um}/{lattice_y_um} um -- the multi-array MRT example "
        "in Fig. 8/9 must use a LARGER lattice than the single-beam "
        "example in §3.1.1 (which the paper does not explicitly state)."
    ),
}

EVI.joinpath("self_consistency.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
