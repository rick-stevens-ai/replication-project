"""
Baseline scheduling policies: FCFS, EASY-Backfill, SJF.
Each runs a full simulation and returns metrics.

Optimized version — avoids O(n²) patterns.
"""

from __future__ import annotations
import csv
import numpy as np
from simulator import Job, load_jobs
from dataclasses import dataclass
from typing import Optional
import heapq
import copy


class BaselineSimulator:
    """Event-driven simulator that runs a full trace with a given policy."""

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes

    def run(self, jobs: list[Job], policy: str) -> dict:
        """Run a full simulation. Returns metrics dict."""
        jobs = [copy.deepcopy(j) for j in jobs if j.num_nodes <= self.num_nodes]

        free_nodes = self.num_nodes
        # Track when each allocated "slot" frees up
        # node_free_times: sorted list of (free_time, num_nodes) for running jobs
        running_end_times: list[tuple[int, int]] = []  # heap of (end_time, num_nodes)
        queue: list[Job] = []
        completed: list[Job] = []
        events: list[tuple[int, int, str, Optional[Job]]] = []
        counter = 0

        for j in jobs:
            counter += 1
            heapq.heappush(events, (j.submit_time, counter, "arrival", j))

        def release_completed(t: int):
            nonlocal free_nodes
            while running_end_times and running_end_times[0][0] <= t:
                end_t, n_nodes = heapq.heappop(running_end_times)
                free_nodes += n_nodes

        def allocate(job: Job, t: int):
            nonlocal free_nodes, counter
            assert free_nodes >= job.num_nodes
            free_nodes -= job.num_nodes
            end_t = t + job.run_time
            job.start_time = t
            job.end_time = end_t
            heapq.heappush(running_end_times, (end_t, job.num_nodes))
            completed.append(job)
            counter += 1
            heapq.heappush(events, (end_t, counter, "completion", None))

        def schedule_fcfs(t: int):
            """FCFS: schedule head of queue if it fits, repeat."""
            while queue and queue[0].num_nodes <= free_nodes:
                allocate(queue.pop(0), t)

        def schedule_sjf(t: int):
            """SJF: sort by req_time, greedily pick first that fits."""
            queue.sort(key=lambda j: j.req_time)
            i = 0
            while i < len(queue):
                if queue[i].num_nodes <= free_nodes:
                    allocate(queue.pop(i), t)
                else:
                    i += 1

        def schedule_easy(t: int):
            """EASY backfill."""
            if not queue:
                return

            # Try to schedule head
            while queue and queue[0].num_nodes <= free_nodes:
                allocate(queue.pop(0), t)

            if not queue:
                return

            head = queue[0]
            # Head doesn't fit — compute when it will
            # Collect all running job end times and their node counts
            # sorted ascending
            end_times_sorted = sorted(running_end_times)
            reservation_time = t
            nodes_available = free_nodes
            for end_t, n_nodes in end_times_sorted:
                nodes_available += n_nodes
                if nodes_available >= head.num_nodes:
                    reservation_time = end_t
                    break
            else:
                # Shouldn't happen if job fits in cluster
                reservation_time = t + 999999

            # Backfill: scan rest of queue for jobs that fit AND finish before reservation
            i = 1
            while i < len(queue):
                job = queue[i]
                if job.num_nodes <= free_nodes:
                    if t + job.req_time <= reservation_time:
                        allocate(queue.pop(i), t)
                        continue
                i += 1

        while events:
            t = events[0][0]
            # Process all events at this timestamp
            while events and events[0][0] == t:
                _, _, etype, job = heapq.heappop(events)
                if etype == "arrival":
                    queue.append(job)
                elif etype == "completion":
                    pass  # just releases nodes below

            release_completed(t)

            if policy == "fcfs":
                schedule_fcfs(t)
            elif policy == "easy_backfill":
                schedule_easy(t)
            elif policy == "sjf":
                schedule_sjf(t)

        # Metrics
        if not completed:
            return {"avg_wait": 0, "avg_slowdown": 0, "makespan": 0,
                    "num_completed": 0, "avg_response": 0, "max_wait": 0, "max_slowdown": 0}

        waits = [j.wait_time for j in completed]
        slowdowns = [j.slowdown for j in completed]
        makespan = max(j.end_time for j in completed) - min(j.submit_time for j in completed)

        return {
            "avg_wait": float(np.mean(waits)),
            "max_wait": float(np.max(waits)),
            "avg_slowdown": float(np.mean(slowdowns)),
            "max_slowdown": float(np.max(slowdowns)),
            "makespan": int(makespan),
            "num_completed": len(completed),
            "avg_response": float(np.mean([j.response_time for j in completed])),
        }


def run_all_baselines(csv_path: str, num_nodes: int) -> dict[str, dict]:
    """Run all baseline policies and return {policy_name: metrics}."""
    jobs = load_jobs(csv_path)
    sim = BaselineSimulator(num_nodes)
    results = {}
    for policy in ["fcfs", "easy_backfill", "sjf"]:
        print(f"Running baseline: {policy} ({len(jobs)} jobs, {num_nodes} nodes)...")
        metrics = sim.run(jobs, policy)
        results[policy] = metrics
        print(f"  {policy}: avg_wait={metrics['avg_wait']:.1f}s, "
              f"avg_slowdown={metrics['avg_slowdown']:.2f}, "
              f"makespan={metrics['makespan']}s, "
              f"completed={metrics['num_completed']}")
    return results


if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "../data/hpc2n_subset.csv"
    num_nodes = int(sys.argv[2]) if len(sys.argv) > 2 else 240
    results = run_all_baselines(csv_path, num_nodes)
    print("\n=== Baseline Results ===")
    for policy, metrics in results.items():
        print(f"{policy}: {metrics}")
