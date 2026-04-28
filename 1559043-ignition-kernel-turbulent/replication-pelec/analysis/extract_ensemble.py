#!/usr/bin/env python3
"""Extract time-series diagnostics from PeleC ensemble .o log files.

Log format has per-line records:
    TIME = <t> <VAR> = <val>  OR  MIN = <a>  MAX = <b>

We collect records into a per-(phi,realization) time-series table.
"""
import re, os, json, csv
from pathlib import Path
from collections import defaultdict

BASE   = Path.home() / "Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec"
LOGDIR = BASE / "ensemble/logs"
OUTDIR = BASE / "analysis"
CSVDIR = OUTDIR / "timeseries_csv"
CSVDIR.mkdir(parents=True, exist_ok=True)

# Map log filename -> (phi, realization)
RUN_RE = re.compile(r"pele_phi(?P<phi>[\d.]+)_r(?P<r>\d+)\.o\d+")

# Line patterns — single var per line.
MIN_MAX = re.compile(
    r"^TIME = (?P<t>[\d.eE+-]+)\s+(?P<var>\S+)\s+MIN = (?P<mn>[\d.eE+-]+)\s+MAX = (?P<mx>[\d.eE+-]+)"
)
SCALAR = re.compile(
    r"^TIME = (?P<t>[\d.eE+-]+)\s+(?P<var>\S+)\s+=\s+(?P<val>[-\d.eE+nanifNANIF]+)\s*$"
)

MINMAX_VARS = {"Temp", "density", "pressure", "massfrac",
               "x_velocity", "y_velocity", "z_velocity", "eint_e", "sumYminus1"}
SCALAR_VARS = {"MASS", "XMOM", "YMOM", "ZMOM", "RHO*e", "RHO*K", "RHO*E", "FUEL"}
# Note: "FUEL PROD" has a space — handle separately.


def parse_log(path: Path):
    """Return dict: time(float) -> dict of fields."""
    records = defaultdict(dict)
    with path.open() as f:
        for line in f:
            # Handle "FUEL PROD   = ..." by normalizing
            line = line.replace("FUEL PROD", "FUELPROD")
            m = MIN_MAX.match(line)
            if m:
                t = float(m["t"])
                v = m["var"]
                if v in MINMAX_VARS:
                    records[t][f"{v}_min"] = float(m["mn"])
                    records[t][f"{v}_max"] = float(m["mx"])
                continue
            m = SCALAR.match(line)
            if m:
                t = float(m["t"])
                v = m["var"]
                try:
                    val = float(m["val"])
                except ValueError:
                    val = float("nan")
                # Normalize names
                records[t][v] = val
    rows = [records[t] | {"time": t} for t in sorted(records)]
    # Only keep rows that have Temp_max (real summary rows, not partial)
    rows = [r for r in rows if "Temp_max" in r]
    return rows


def classify(rows):
    """Return dict with completeness & ignition diagnostics."""
    if not rows:
        return {"status": "empty", "t_final": 0.0, "n_rows": 0}
    t_final = rows[-1]["time"]
    T_max_series = [(r["time"], r["Temp_max"]) for r in rows]
    # Any NaN?
    nan_hit = any(r["Temp_max"] != r["Temp_max"] for r in rows)
    # T_max late: t > 500μs
    late = [(t, T) for t, T in T_max_series if t > 5e-4]
    if late:
        T_late_max = max(T for _, T in late)
        T_late_mean = sum(T for _, T in late) / len(late)
    else:
        T_late_max = T_late_mean = 0.0
    # Fuel consumed: (FUELPROD_final)/MASS_0
    mass0 = rows[0].get("MASS", float("nan"))
    fuel_final = rows[-1].get("FUELPROD", 0.0)
    # Ignition flags
    ignite_Tlate = t_final > 5e-4 and T_late_max > 1500
    # Consider "complete" if reached ≥ 0.9 ms
    complete = t_final >= 9.0e-4
    status = "complete" if complete else ("partial" if t_final > 1e-5 else "failed")
    if nan_hit:
        status = "nan"
    return {
        "status": status,
        "t_final": t_final,
        "n_rows": len(rows),
        "Temp_max_global": max(T for _, T in T_max_series),
        "Temp_late_max": T_late_max,
        "Temp_late_mean": T_late_mean,
        "T_at_1ms": next((T for t, T in reversed(T_max_series) if t <= 1.0e-3), T_max_series[-1][1]),
        "T_at_500us": next((T for t, T in reversed(T_max_series) if t <= 5.0e-4), T_max_series[0][1]),
        "fuel_prod_final": fuel_final,
        "mass0": mass0,
        "ignite_Tlate_1500": bool(ignite_Tlate),
    }


def write_csv(rows, path: Path):
    if not rows:
        return
    cols = ["time", "Temp_min", "Temp_max", "density_min", "density_max",
            "pressure_min", "pressure_max", "massfrac_min", "massfrac_max",
            "MASS", "RHO*e", "RHO*E", "FUELPROD"]
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c, "") for c in cols])


def main():
    summary = {}
    all_rows = {}
    logs = sorted(LOGDIR.glob("pele_phi*_r*.o*"))
    print(f"Found {len(logs)} logs")
    for lp in logs:
        m = RUN_RE.match(lp.name)
        if not m:
            continue
        key = f"phi{m['phi']}_r{m['r']}"
        rows = parse_log(lp)
        info = classify(rows)
        summary[key] = info
        all_rows[key] = rows
        write_csv(rows, CSVDIR / f"{key}.csv")
        print(f"  {key:14s}  status={info['status']:8s} t_final={info['t_final']:.3e}s rows={info['n_rows']:4d}  "
              f"T_max={info['Temp_max_global']:.0f}K  T_late={info['Temp_late_max']:.0f}K  ignite={info['ignite_Tlate_1500']}")

    (OUTDIR / "ensemble_summary.json").write_text(json.dumps(summary, indent=2))
    # Save compact timeseries (subsample to ~500 pts per run to save size)
    compact = {}
    for k, rows in all_rows.items():
        if not rows:
            compact[k] = []
            continue
        step = max(1, len(rows) // 500)
        compact[k] = [{kk: rr[kk] for kk in ("time", "Temp_max", "Temp_min", "pressure_max",
                                              "density_max", "massfrac_max", "FUELPROD", "MASS")
                        if kk in rr} for rr in rows[::step]]
    (OUTDIR / "ensemble_timeseries.json").write_text(json.dumps(compact))
    print(f"\nWrote: {OUTDIR/'ensemble_summary.json'}")
    print(f"Wrote: {OUTDIR/'ensemble_timeseries.json'}")
    print(f"CSVs in: {CSVDIR}")


if __name__ == "__main__":
    main()
