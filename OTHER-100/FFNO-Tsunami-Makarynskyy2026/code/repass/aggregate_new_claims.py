#!/usr/bin/env python
"""
Aggregate NEW claims for the FFNO-Tsunami repass.

Inputs (paths are uicgpu-side absolute):
    --selected_root   /data/stevens/tsunami/results              (pass-1 Selected per-case dump)
    --reference_root  /data/stevens/tsunami/results_reference    (repass Reference per-case dump)
    --selected_table  /data/stevens/tsunami/results/ja/table1_metrics_summary.csv
    --reference_table /data/stevens/tsunami/results_reference/ja/table1_metrics_summary.csv (optional)
    --out             /path/to/results/repass/new_claims_summary.json

Computes for each model that's present:
    - aggregate RMSE_eta / RMSE_avg / ATE_min / BEE (mean ± std over cases)
    - NATE detection count   = number of cases with at least one valid (true & predicted) buoy arrival
    - peak-eta RMSE / MAE     across cases (predicted peak vs true peak)
    - rollout-decay summary   = mean RMSE_eta at step 10, step 100, step 200
                                + quartiles (25, 50, 75) at step 200

Designed to be tolerant: if reference root is missing, only Selected derivatives populate.

Run on uicgpu:
    python aggregate_new_claims.py \
        --selected_root  /data/stevens/tsunami/results \
        --reference_root /data/stevens/tsunami/results_reference \
        --selected_table /data/stevens/tsunami/results/ja/table1_metrics_summary.csv \
        --reference_table /data/stevens/tsunami/results_reference/ja/table1_metrics_summary.csv \
        --out /data/stevens/tsunami/results_reference/new_claims_summary.json
"""
import argparse
import csv
import json
import math
import os
import statistics
import sys
from pathlib import Path


def _read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def aggregate_table(csv_path):
    rows = _read_csv(csv_path)
    keys = ["rmse_eta", "rmse_avg", "rmse_u", "rmse_v", "BEE", "peak_eta", "peak_eta_true"]
    out = {"n_cases": len(rows)}
    for k in keys:
        try:
            vals = [float(r[k]) for r in rows if r.get(k) not in (None, "", "nan")]
        except Exception:
            vals = []
        if vals:
            out[k] = {"mean": statistics.mean(vals), "std": statistics.pstdev(vals)}
    # ATE: column is named ATE_seconds in the per-case CSV; convert to minutes
    try:
        ate_min_vals = [float(r["ATE_seconds"]) / 60.0 for r in rows if r.get("ATE_seconds") not in (None, "", "nan")]
    except Exception:
        ate_min_vals = []
    if ate_min_vals:
        out["ATE_min"] = {"mean": statistics.mean(ate_min_vals), "std": statistics.pstdev(ate_min_vals)}
    # Peak elevation RMSE / MAE across cases
    if "peak_eta" in out and "peak_eta_true" in out:
        diffs = []
        for r in rows:
            try:
                pp = float(r["peak_eta"]); tt = float(r["peak_eta_true"])
                diffs.append(pp - tt)
            except Exception:
                continue
        if diffs:
            out["peak_eta_residual"] = {
                "rmse": math.sqrt(sum(d * d for d in diffs) / len(diffs)),
                "mae":  sum(abs(d) for d in diffs) / len(diffs),
                "mean_signed": sum(diffs) / len(diffs),
                "n": len(diffs),
            }
    out["cases"] = [r["case"] for r in rows]
    return out


def detection_count(per_case_root):
    """For each per-case dir, count cases with at least one (true & pred) valid buoy arrival.
    Returns (n_with_detection, n_cases_examined, per_case_detection_dict)."""
    root = Path(per_case_root)
    if not root.exists():
        return None
    case_dirs = sorted([p for p in root.iterdir() if p.is_dir() and p.name.startswith("Case6")])
    n_det = 0
    per_case = {}
    for cd in case_dirs:
        bp = cd / "buoy_metrics.csv"
        if not bp.exists():
            continue
        has_valid = False
        for row in _read_csv(bp):
            tt = row.get("tau_true_h"); pp = row.get("tau_pred_h")
            try:
                if tt not in (None, "", "nan") and pp not in (None, "", "nan") and not math.isnan(float(tt)) and not math.isnan(float(pp)):
                    has_valid = True
                    break
            except Exception:
                continue
        per_case[cd.name] = has_valid
        if has_valid:
            n_det += 1
    return {"n_with_detection": n_det, "n_cases": len(case_dirs), "per_case": per_case}


def rollout_decay(per_case_root, steps=(10, 50, 100, 150, 200)):
    """Pull RMSE_eta at the requested steps across all cases."""
    root = Path(per_case_root)
    if not root.exists():
        return None
    case_dirs = sorted([p for p in root.iterdir() if p.is_dir() and p.name.startswith("Case6")])
    by_step = {s: [] for s in steps}
    for cd in case_dirs:
        rp = cd / "rmse_rollout_eta.csv"
        if not rp.exists():
            continue
        rows = _read_csv(rp)
        for r in rows:
            try:
                step = int(r["step"]); val = float(r["rmse_eta_m"])
            except Exception:
                continue
            if step in by_step:
                by_step[step].append(val)
    out = {}
    for s, vs in by_step.items():
        if not vs:
            continue
        vs_sorted = sorted(vs)
        def q(p):
            k = (len(vs_sorted) - 1) * p
            lo = int(math.floor(k)); hi = int(math.ceil(k))
            if lo == hi: return vs_sorted[lo]
            return vs_sorted[lo] + (vs_sorted[hi] - vs_sorted[lo]) * (k - lo)
        out[s] = {
            "n": len(vs),
            "mean": statistics.mean(vs),
            "std": statistics.pstdev(vs),
            "q25": q(0.25), "q50": q(0.50), "q75": q(0.75),
            "min": min(vs), "max": max(vs),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selected_root",  default=None)
    ap.add_argument("--reference_root", default=None)
    ap.add_argument("--selected_table", default=None)
    ap.add_argument("--reference_table", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    summary = {
        "paper":  "Kim, Koh, Oh, Son 2026 — FFNO Tsunami",
        "table3_paper_testem": {
            "selected":  {"rmse_eta":(0.0763,0.0248), "rmse_avg":(0.0382,0.0123), "ATE_min":(12.1,14.4),  "BEE":(0.0312,0.0107), "NATE":54, "N":54},
            "reference": {"rmse_eta":(0.0836,0.0257), "rmse_avg":(0.0414,0.0127), "ATE_min":(11.7,10.0),  "BEE":(0.0360,0.0057), "NATE":54, "N":54},
            "w_o_DC":    {"rmse_eta":(0.0850,0.0297), "rmse_avg":(0.0418,0.0146), "ATE_min":(12.1, 9.8),  "BEE":(0.0392,0.0073), "NATE":54, "N":54},
            "p_M272":    {"rmse_eta":(0.0889,0.0322), "rmse_avg":(0.0438,0.0158), "ATE_min":(10.6,11.1),  "BEE":(0.0351,0.0125), "NATE":54, "N":54},
        },
    }

    if args.selected_table and os.path.exists(args.selected_table):
        summary["selected_aggregate"] = aggregate_table(args.selected_table)
    if args.reference_table and os.path.exists(args.reference_table):
        summary["reference_aggregate"] = aggregate_table(args.reference_table)

    if args.selected_root:
        summary["selected_detection"]    = detection_count(args.selected_root)
        summary["selected_rollout_decay"] = rollout_decay(args.selected_root)
    if args.reference_root:
        summary["reference_detection"]    = detection_count(args.reference_root)
        summary["reference_rollout_decay"] = rollout_decay(args.reference_root)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote", args.out)
    print(json.dumps({k: (v if not isinstance(v, dict) or len(str(v)) < 600 else f"<{len(v)} keys>") for k, v in summary.items()}, indent=2, default=str)[:2000])


if __name__ == "__main__":
    main()
