#!/usr/bin/env python3
"""
LUCID-100 slot 25 — End-to-end replication driver.

Goal: actually test the paper's Table 2 (280 kVp x-ray AG1522 fibroblasts) and
Table 3 (3.5 MeV alpha AG1522) headline numbers using:
  - Author's SPT-SDD-Framework (dummy library shipped in repo) to assemble cell
    SDD files at a target dose,
  - MEDRAS-MC (slot 16) Spectrum analysis to compute per-cell dicentrics, rings,
    total aberrations, and viability (alive=1, dead=0).

Honest scope:
  * The author EXCLUDED the full pre-computed SPT-SDD libraries (>50 GB).
    What ships in the repo is the DUMMY library used for framework testing.
    Per the paper's own README and §Data availability, paper-quality numbers
    require the full library + the TOPAS-built reference PHSPs for the three
    in-vitro setups (x-ray, proton SOBP, alpha through Mylar).
  * We re-use the shipped phase-space files (`Ex_PHASE_SPACE/*.phsp`) and dummy
    SDD/Dose libraries, so absolute numbers will differ from Table 2/3 in
    magnitude — but the PIPELINE works end-to-end and we can compare TRENDS
    (monotonic increase with dose, alpha > x-ray, etc.) and report numbers
    with full transparency.
  * We score 30 cells per (particle, dose) — paper used 1000 (x-ray) / 100,000
    (proton, alpha). That's a published gap, called out in REPORT.md §7.

Outputs:
  results/dose_response/<particle>_<dose>Gy/cell_*.sdd
  results/dose_response/medras_<particle>_<dose>Gy.tsv
  results/dose_response/summary.csv
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import shutil
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FRAMEWORK = ROOT / "code" / "SPT-SDD-Framework"
MEDRAS = Path(
    "/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/"
    "lucid-medras-mc/Medras-MC"
)
RESULTS = ROOT / "results" / "dose_response"
RESULTS.mkdir(parents=True, exist_ok=True)

# Imports: SPT-SDD-Framework
sys.path.insert(0, str(FRAMEWORK))
import numpy as np  # noqa: E402

from modules.core_utils import CommonApp  # noqa: E402
from modules.dose_engine import DoseEngine  # noqa: E402
from modules.sdd_io import SDDWriter  # noqa: E402

# Imports: MEDRAS-MC
sys.path.insert(0, str(MEDRAS))
from repairanalysis import medrasrepair  # noqa: E402


# --- Author config templates (replicate alpha & electron configs at chosen dose) ---

def build_cells(particle: str, dose_gy: float, n_cells: int, out_dir: Path,
                seed: int = 42) -> None:
    """Drive SPT-SDD-Framework to write n_cells SDD files at target dose."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # Wipe stale cells
    for old in out_dir.glob("cell_*.sdd"):
        old.unlink()

    # Replicate author config defaults
    if particle == "alpha":
        cfg = {
            "paths": {
                "dose_file_folder": str(FRAMEWORK / "Alpha_Dummy" / "Dose") + "/",
                "DSB_file_folder": str(FRAMEWORK / "Alpha_Dummy" / "SDD") + "/",
                "output_folder": str(out_dir) + "/",
                "mean_dose_csv_path": str(FRAMEWORK / "Average_Dose" / "Alpha.csv"),
                "target_spectrum": str(FRAMEWORK / "Ex_PHASE_SPACE" / "Alpha_Limited.phsp"),
            },
            "simulation": {
                "total_simulations": n_cells,
                "simulation_name": f"Alpha_{dose_gy}Gy",
                "incident_pdg": "1000020040",
                "assigned_dose": float(dose_gy),
                "simulation_type": "high_let",
                "rng_seed": seed,
            },
        }
    elif particle == "electron":
        cfg = {
            "paths": {
                "dose_file_folder": str(FRAMEWORK / "Electron_Dummy" / "Dose") + "/",
                "DSB_file_folder": str(FRAMEWORK / "Electron_Dummy" / "SDD") + "/",
                "output_folder": str(out_dir) + "/",
                "mean_dose_csv_path": "None",
                "target_spectrum": str(FRAMEWORK / "Ex_PHASE_SPACE" / "Electron_Limited.phsp"),
            },
            "simulation": {
                "total_simulations": n_cells,
                "simulation_name": f"Electron_{dose_gy}Gy",
                "incident_pdg": "11",
                "assigned_dose": float(dose_gy),
                "simulation_type": "low_let",
                "dose_rate_Gy_per_min": 0.55,
                "rng_seed": seed,
            },
        }
    elif particle == "proton":
        cfg = {
            "paths": {
                "dose_file_folder": str(FRAMEWORK / "Proton_Dummy" / "Dose") + "/",
                "DSB_file_folder": str(FRAMEWORK / "Proton_Dummy" / "SDD") + "/",
                "output_folder": str(out_dir) + "/",
                "mean_dose_csv_path": "None",
                "target_spectrum": str(FRAMEWORK / "Ex_PHASE_SPACE" / "Proton_Limited.phsp"),
            },
            "simulation": {
                "total_simulations": n_cells,
                "simulation_name": f"Proton_{dose_gy}Gy",
                "incident_pdg": "2212",
                "assigned_dose": float(dose_gy),
                "simulation_type": "low_let",
                "rng_seed": seed,
            },
        }
    else:
        raise ValueError(particle)

    app = CommonApp()
    # CommonApp.load_config expects a path; bypass by writing to a temp file
    cfg_path = out_dir / "_run_config.json"
    cfg_path.write_text(json.dumps(cfg, indent=2))
    config = app.load_config(str(cfg_path))

    engine = DoseEngine(rng_seed=config["simulation"].get("rng_seed"))
    writer = SDDWriter(config["simulation"]["incident_pdg"])
    dose_folder = config["paths"]["dose_file_folder"]
    grid = app.get_energy_grid(dose_folder)
    cdf, pdf = app.get_spectrum_cdf(config["paths"]["target_spectrum"], grid)
    is_high_let = config["simulation"]["simulation_type"] in ["high_let"]
    lambda_p = (
        app.get_high_let_lambda(
            config["paths"]["mean_dose_csv_path"], pdf,
            config["simulation"]["assigned_dose"],
        )
        if is_high_let else None
    )
    dose_rate = config["simulation"].get("dose_rate_Gy_per_min", 0)
    dose_rate_s = dose_rate / 60.0 if dose_rate > 0 else 0

    for i in range(config["simulation"]["total_simulations"]):
        all_track_data, sampled_energies = [], []
        if is_high_let:
            n_particles = engine.get_high_let_count(lambda_p)
            total_dose = 0.0
            for _ in range(n_particles):
                E = engine.sample_energy(cdf, grid)
                sampled_energies.append(E)
                d = app.get_dose_array(E, dose_folder)
                tidx = engine.rng.integers(0, len(d))
                total_dose += d[tidx]
                all_track_data.append(
                    app.get_sdd_groups(E, config["paths"]["DSB_file_folder"]).get(tidx, [])
                )
            primary_count = n_particles
            track_times = None
        else:
            tracks, total_dose = engine.get_low_let_tracks(
                config["simulation"]["assigned_dose"], cdf, grid, app, dose_folder,
            )
            primary_count = len(tracks)
            track_times = None
            if dose_rate_s > 0:
                total_time_s = config["simulation"]["assigned_dose"] / dose_rate_s
                dt = total_time_s / max(primary_count, 1)
                track_times = [int(round((k + 1) * dt) * 1e9) for k in range(primary_count)]
            for E, tidx in tracks:
                sampled_energies.append(E)
                all_track_data.append(
                    app.get_sdd_groups(E, config["paths"]["DSB_file_folder"]).get(tidx, [])
                )

        mean_E = float(np.mean(sampled_energies)) if sampled_energies else 0.0
        out_path = out_dir / f"cell_{i}.sdd"
        writer.save(
            str(out_path),
            total_dose, 0, primary_count, mean_E, all_track_data,
            dose_rate_s, track_times,
        )
        # Patch: ensure the first damage line is tagged NewEvent=2 even when
        # the very first sampled track produced zero damage entries (in which
        # case SDDWriter increments next_pid before writing anything, and the
        # first written line ends up as 1,1 instead of 2,0 — MEDRAS sddparser
        # then crashes with IndexError on events[-1].append(...)).
        _patch_first_event_marker(out_path)


def _patch_first_event_marker(sdd_path: Path) -> None:
    text = sdd_path.read_text().splitlines(keepends=True)
    in_header = True
    out = []
    fixed = False
    for line in text:
        if in_header:
            out.append(line)
            if line.startswith("***EndOfHeader***"):
                in_header = False
            continue
        if not fixed and line.strip():
            # First non-empty data line — force NewEvent=2.
            # Format: "<NewEvent>,<PID>; ..."  -> rewrite the head only.
            head_sep = line.find(";")
            if head_sep > 0:
                head = line[:head_sep]
                if "," in head:
                    parts = head.split(",", 1)
                    new_head = "2," + parts[1].lstrip()
                    line = new_head + line[head_sep:]
            fixed = True
        out.append(line)
    sdd_path.write_text("".join(out))


# --- MEDRAS Spectrum runner ---

_ABERR_RE = re.compile(
    r"^\s*0\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\s*\s*"
    r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\s*\s*"
    r"(\d+)\s*$"
)


def parse_spectrum_lines(stdout: str):
    """Spectrum output rows look like:
       <Index>  <Breaks>  <Residual>  <Misrepairs> <LargeMisrep> <InterChrom>
            <Dicentrics> <Rings> <ExcessFrags> <TotalAberr>  <Viability>
       Tabs and double-tabs separate sections.
    """
    rows = []
    for line in stdout.splitlines():
        # Tab-cleaned, collapse repeated tabs
        parts = re.split(r"\t+", line.strip())
        if len(parts) < 11:
            continue
        # First field must be index (int)
        try:
            int(parts[0])
        except ValueError:
            continue
        # Parse expected columns:
        # 0: Index, 1: Breaks, 2: Residual, 3: Misrepairs, 4: Large, 5: Inter,
        # 6: Dicentrics, 7: Rings, 8: Excess, 9: Total Aberr, 10: Viability
        try:
            row = {
                "Index": int(parts[0]),
                "Breaks": int(parts[1]),
                "Residual": int(parts[2]),
                "Misrepairs": int(parts[3]),
                "LargeMisrep": int(parts[4]),
                "InterChrom": int(parts[5]),
                "Dicentrics": int(parts[6]),
                "Rings": int(parts[7]),
                "ExcessFrags": int(parts[8]),
                "TotalAberr": int(parts[9]),
                "Viability": int(parts[10]),
            }
            rows.append(row)
        except (ValueError, IndexError):
            continue
    return rows


def run_medras_spectrum(sdd_dir: Path, log_path: Path):
    """Run MEDRAS Spectrum on a directory of SDD files; return per-cell rows."""
    # Reset MEDRAS-MC module-level header flags so headers print on each run.
    medrasrepair.fidelityRun = False
    # analyzeAberrations.headerPrinted is also global; reset
    from repairanalysis import analyzeAberrations
    analyzeAberrations.headerPrinted = False
    # Keep MC repeats at default (50); cell count is the controlled variable
    # (Author uses ~1000 for x-ray, ~100000 for proton/alpha — that's outside
    #  our CherryRd budget.)
    buf = io.StringIO()
    with redirect_stdout(buf):
        medrasrepair.repairSimulation(str(sdd_dir) + "/", "Spectrum")
    out = buf.getvalue()
    log_path.write_text(out)
    return parse_spectrum_lines(out)


# --- Main dose-response sweep ---

def sweep():
    summary = []
    cells_per_dose = 30  # CherryRd-friendly budget; paper uses 1000-100000
    plans = [
        # particle, doses (Gy) — matched to paper Table 2 / Table 3 where possible
        ("electron", [1.0, 2.0, 4.0, 6.0, 9.0]),    # Cornforth & Bedford 1987, AG1522
        ("alpha",    [0.6, 1.1, 1.7, 2.2]),          # Cornforth et al 2002, AG1522
        ("proton",   [1.0, 2.0, 4.0, 6.0]),          # Marshall et al 2016, AG1522
    ]
    t0 = time.time()
    for particle, doses in plans:
        for dose in doses:
            tag = f"{particle}_{dose:g}Gy"
            print(f"\n=== {tag}  (n_cells={cells_per_dose}) ===", flush=True)
            sdd_dir = RESULTS / tag
            log_path = RESULTS / f"medras_{tag}.tsv"
            try:
                t_start = time.time()
                build_cells(particle, dose, cells_per_dose, sdd_dir, seed=42)
                t_build = time.time() - t_start
                rows = run_medras_spectrum(sdd_dir, log_path)
                t_total = time.time() - t_start
                if not rows:
                    print(f"  ! No parsed MEDRAS rows for {tag}")
                    continue
                dicentrics = [r["Dicentrics"] for r in rows]
                total_aberr = [r["TotalAberr"] for r in rows]
                via = [r["Viability"] for r in rows]
                breaks = [r["Breaks"] for r in rows]
                misrep = [r["Misrepairs"] for r in rows]
                n = len(rows)
                mean_dic = float(np.mean(dicentrics))
                sem_dic = float(np.std(dicentrics, ddof=1) / np.sqrt(n)) if n > 1 else 0.0
                mean_tot = float(np.mean(total_aberr))
                sem_tot = float(np.std(total_aberr, ddof=1) / np.sqrt(n)) if n > 1 else 0.0
                sf = float(np.mean(via))
                sf_sem = float(np.std(via, ddof=1) / np.sqrt(n)) if n > 1 else 0.0
                mean_breaks = float(np.mean(breaks))
                mean_misrep = float(np.mean(misrep))
                summary.append({
                    "particle": particle,
                    "dose_Gy": dose,
                    "n_cells": n,
                    "mean_DSBs_per_cell": round(mean_breaks, 3),
                    "mean_misrepairs": round(mean_misrep, 3),
                    "dicentrics_mean": round(mean_dic, 4),
                    "dicentrics_sem":  round(sem_dic, 4),
                    "total_aberr_mean": round(mean_tot, 4),
                    "total_aberr_sem":  round(sem_tot, 4),
                    "surviving_fraction": round(sf, 4),
                    "surviving_fraction_sem": round(sf_sem, 4),
                    "build_time_s": round(t_build, 2),
                    "total_time_s": round(t_total, 2),
                })
                print(
                    f"  -> dic={mean_dic:.3f}±{sem_dic:.3f}, "
                    f"tot={mean_tot:.3f}±{sem_tot:.3f}, "
                    f"SF={sf:.3f}±{sf_sem:.3f}, breaks/cell={mean_breaks:.1f}, "
                    f"time={t_total:.1f}s",
                    flush=True,
                )
            except Exception as e:
                print(f"  ! {tag} failed: {e}", flush=True)
                import traceback
                traceback.print_exc()

    csv_path = RESULTS / "summary.csv"
    if summary:
        with csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
            writer.writeheader()
            writer.writerows(summary)
        print(f"\nWrote {csv_path}  ({len(summary)} rows, elapsed {time.time()-t0:.1f}s)")
    else:
        print("\nNo rows generated.")


if __name__ == "__main__":
    sweep()
