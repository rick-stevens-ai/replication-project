"""
Parse SWF (Standard Workload Format) files from the Parallel Workloads Archive.
Produces a cleaned CSV with columns: job_id, submit_time, run_time, num_nodes, req_time
"""

import argparse
import csv
import sys
from pathlib import Path


def parse_swf(swf_path: str, max_jobs: int = 0) -> list[dict]:
    """Parse SWF file, return list of job dicts."""
    jobs = []
    with open(swf_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            parts = line.split()
            if len(parts) < 18:
                continue

            job_id = int(parts[0])
            submit_time = int(parts[1])
            wait_time = int(parts[2])
            run_time = int(parts[3])
            num_alloc_procs = int(parts[4])
            req_num_procs = int(parts[7])
            req_time = int(parts[8])

            # Filter out bad records
            if run_time <= 0 or submit_time < 0:
                continue
            if num_alloc_procs <= 0 and req_num_procs <= 0:
                continue

            num_nodes = num_alloc_procs if num_alloc_procs > 0 else req_num_procs
            est_time = req_time if req_time > 0 else run_time  # fallback

            jobs.append({
                "job_id": job_id,
                "submit_time": submit_time,
                "run_time": run_time,
                "num_nodes": num_nodes,
                "req_time": est_time,
            })

    # Sort by submit_time
    jobs.sort(key=lambda j: (j["submit_time"], j["job_id"]))

    # Optionally limit
    if max_jobs > 0:
        jobs = jobs[:max_jobs]

    return jobs


def main():
    parser = argparse.ArgumentParser(description="Parse SWF to CSV")
    parser.add_argument("swf_file", help="Path to .swf file")
    parser.add_argument("-o", "--output", default=None, help="Output CSV path")
    parser.add_argument("-n", "--max-jobs", type=int, default=0, help="Max jobs to keep (0=all)")
    args = parser.parse_args()

    jobs = parse_swf(args.swf_file, args.max_jobs)
    print(f"Parsed {len(jobs)} valid jobs from {args.swf_file}", file=sys.stderr)

    out_path = args.output or str(Path(args.swf_file).with_suffix(".csv"))
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["job_id", "submit_time", "run_time", "num_nodes", "req_time"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Wrote {len(jobs)} jobs to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
