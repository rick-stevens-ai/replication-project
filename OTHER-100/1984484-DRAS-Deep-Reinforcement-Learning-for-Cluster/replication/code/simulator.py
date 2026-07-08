"""
Event-driven HPC cluster simulator.

Simulates a cluster with N homogeneous nodes.  Jobs arrive at submit_time,
request num_nodes for run_time seconds.  The scheduler is called whenever a
job arrives or a running job completes (event-driven).

The simulator exposes an OpenAI-Gym-like interface for RL agents:
  obs, info = env.reset(jobs)
  obs, reward, done, truncated, info = env.step(action)

State representation (simplified DRAS):
  For each of W=50 jobs at the front of the queue:
    [num_nodes/N, req_time/max_req_time, wait_time/max_time, 0-pad]
  For each of N nodes:
    [available (0/1), time_until_free/max_time]
  Flattened to a 1-D vector.

Action: index in [0, W-1] — which queued job to schedule next (or backfill).
  Invalid actions (job won't fit) are masked; if all masked the episode step
  returns with no job scheduled but time advances to next event.
"""

from __future__ import annotations
import heapq
import csv
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class Job:
    job_id: int
    submit_time: int
    run_time: int
    num_nodes: int
    req_time: int  # user estimate of runtime

    # Filled by simulator
    start_time: int = -1
    end_time: int = -1

    @property
    def wait_time_at(self):
        """Compute wait time given current_time externally."""
        ...

    @property
    def response_time(self) -> int:
        assert self.end_time >= 0
        return self.end_time - self.submit_time

    @property
    def wait_time(self) -> int:
        assert self.start_time >= 0
        return self.start_time - self.submit_time

    @property
    def slowdown(self) -> float:
        rt = max(self.run_time, 1)
        return self.response_time / rt


def load_jobs(csv_path: str) -> list[Job]:
    """Load jobs from CSV produced by parse_swf.py."""
    jobs = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append(Job(
                job_id=int(row["job_id"]),
                submit_time=int(row["submit_time"]),
                run_time=int(row["run_time"]),
                num_nodes=int(row["num_nodes"]),
                req_time=int(row["req_time"]),
            ))
    jobs.sort(key=lambda j: (j.submit_time, j.job_id))
    return jobs


# ---------------------------------------------------------------------------
# Cluster Simulator
# ---------------------------------------------------------------------------
class ClusterEnv:
    """Event-driven cluster simulator with Gym-like API."""

    def __init__(self, num_nodes: int, window_size: int = 50,
                 max_time_norm: float = 86400.0):
        self.num_nodes = num_nodes
        self.window_size = window_size
        self.max_time_norm = max_time_norm  # normalisation constant for times

        # State
        self.current_time: int = 0
        self.node_free_at: np.ndarray = np.zeros(num_nodes, dtype=np.float64)
        self.queue: list[Job] = []
        self.pending_jobs: list[Job] = []  # not yet submitted
        self.running_jobs: list[Job] = []
        self.completed_jobs: list[Job] = []
        self.events: list[tuple[int, str, Optional[Job]]] = []  # min-heap (time, type, job)
        self._event_counter = 0

        # Observation shape
        self.job_feat_dim = 3  # nodes_frac, reqtime_frac, waittime_frac
        self.node_feat_dim = 2  # available, time_until_free_frac
        self.obs_dim = self.window_size * self.job_feat_dim + self.num_nodes * self.node_feat_dim

    # ---------- helpers ----------
    def _push_event(self, time: int, etype: str, job: Optional[Job] = None):
        self._event_counter += 1
        heapq.heappush(self.events, (time, self._event_counter, etype, job))

    def _free_nodes_count(self) -> int:
        return int(np.sum(self.node_free_at <= self.current_time))

    def _allocate(self, job: Job):
        """Allocate nodes to a job, start it running."""
        free_idxs = np.where(self.node_free_at <= self.current_time)[0]
        assert len(free_idxs) >= job.num_nodes, f"Not enough free nodes: {len(free_idxs)} < {job.num_nodes}"
        chosen = free_idxs[:job.num_nodes]
        end_time = self.current_time + job.run_time
        self.node_free_at[chosen] = end_time
        job.start_time = self.current_time
        job.end_time = end_time
        self.running_jobs.append(job)
        self._push_event(end_time, "completion", job)

    def _build_obs(self) -> np.ndarray:
        """Build observation vector."""
        # Job features for top-W queued jobs
        job_obs = np.zeros((self.window_size, self.job_feat_dim), dtype=np.float32)
        for i, job in enumerate(self.queue[:self.window_size]):
            job_obs[i, 0] = job.num_nodes / self.num_nodes
            job_obs[i, 1] = job.req_time / self.max_time_norm
            wt = self.current_time - job.submit_time
            job_obs[i, 2] = wt / self.max_time_norm

        # Node features
        node_obs = np.zeros((self.num_nodes, self.node_feat_dim), dtype=np.float32)
        for i in range(self.num_nodes):
            if self.node_free_at[i] <= self.current_time:
                node_obs[i, 0] = 1.0  # available
                node_obs[i, 1] = 0.0
            else:
                node_obs[i, 0] = 0.0
                diff = (self.node_free_at[i] - self.current_time)
                node_obs[i, 1] = min(diff / self.max_time_norm, 1.0)

        return np.concatenate([job_obs.flatten(), node_obs.flatten()])

    def _action_mask(self) -> np.ndarray:
        """Return boolean mask: True = action is valid (job fits in free nodes)."""
        mask = np.zeros(self.window_size, dtype=bool)
        free = self._free_nodes_count()
        for i, job in enumerate(self.queue[:self.window_size]):
            if job.num_nodes <= free:
                mask[i] = True
        return mask

    # ---------- Gym-like API ----------
    def reset(self, jobs: list[Job]) -> tuple[np.ndarray, dict]:
        """Reset environment with a new list of jobs. Returns (obs, info)."""
        self.current_time = 0
        self.node_free_at[:] = 0
        self.queue = []
        self.running_jobs = []
        self.completed_jobs = []
        self.events = []
        self._event_counter = 0

        # Deep-copy jobs so we can modify them
        self.pending_jobs = []
        for j in jobs:
            self.pending_jobs.append(Job(
                job_id=j.job_id,
                submit_time=j.submit_time,
                run_time=j.run_time,
                num_nodes=j.num_nodes,
                req_time=j.req_time,
            ))
        self.pending_jobs.sort(key=lambda j: (j.submit_time, j.job_id))

        # Schedule first arrival events
        for j in self.pending_jobs:
            self._push_event(j.submit_time, "arrival", j)
        self.pending_jobs = []  # all queued as events now

        # Advance to first event
        self._advance_to_next_event()

        obs = self._build_obs()
        mask = self._action_mask()
        return obs, {"mask": mask, "queue_len": len(self.queue)}

    def _advance_to_next_event(self):
        """Process events until we have a non-empty queue with schedulable jobs,
        or until all jobs are done."""
        while self.events:
            # Peek at next event time
            next_time = self.events[0][0]
            self.current_time = next_time

            # Process ALL events at this timestamp
            while self.events and self.events[0][0] == next_time:
                _, _, etype, job = heapq.heappop(self.events)
                if etype == "arrival":
                    # Only add jobs that actually fit in the cluster
                    if job.num_nodes <= self.num_nodes:
                        self.queue.append(job)
                elif etype == "completion":
                    if job in self.running_jobs:
                        self.running_jobs.remove(job)
                        self.completed_jobs.append(job)

            # If queue has schedulable jobs, return control to agent
            if self.queue and np.any(self._action_mask()):
                return

        # No more events

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        """
        Execute action: schedule the job at queue index `action`.
        Returns (obs, reward, terminated, truncated, info).
        """
        mask = self._action_mask()

        # Handle invalid action
        if action < 0 or action >= self.window_size or not mask[action]:
            # No-op: advance time
            self._advance_to_next_event()
            done = len(self.queue) == 0 and len(self.events) == 0 and len(self.running_jobs) == 0
            obs = self._build_obs()
            new_mask = self._action_mask()
            return obs, -0.01, done, False, {"mask": new_mask, "queue_len": len(self.queue)}

        # Schedule the selected job
        job = self.queue.pop(action)
        self._allocate(job)

        # Reward (simplified DRAS Eq. 1):
        # Positive components: scheduling a job that has waited long + using resources
        wait_frac = (self.current_time - job.submit_time) / max(self.max_time_norm, 1)
        size_frac = job.num_nodes / self.num_nodes
        util = 1.0 - (self._free_nodes_count() / self.num_nodes)
        reward = (wait_frac + size_frac + util) / 3.0

        # Check if more actions possible at same timestep (backfill)
        new_mask = self._action_mask()
        if self.queue and np.any(new_mask):
            # More jobs can be scheduled at this time
            obs = self._build_obs()
            return obs, reward, False, False, {"mask": new_mask, "queue_len": len(self.queue)}

        # Advance to next event
        self._advance_to_next_event()

        done = len(self.queue) == 0 and len(self.events) == 0 and len(self.running_jobs) == 0
        obs = self._build_obs()
        new_mask = self._action_mask()
        return obs, reward, done, False, {"mask": new_mask, "queue_len": len(self.queue)}

    def get_metrics(self) -> dict:
        """Compute final metrics over completed jobs."""
        if not self.completed_jobs:
            return {"avg_wait": 0, "avg_slowdown": 0, "makespan": 0, "num_completed": 0}

        waits = [j.wait_time for j in self.completed_jobs]
        slowdowns = [j.slowdown for j in self.completed_jobs]
        makespan = max(j.end_time for j in self.completed_jobs) - min(j.submit_time for j in self.completed_jobs)

        return {
            "avg_wait": np.mean(waits),
            "max_wait": np.max(waits),
            "avg_slowdown": np.mean(slowdowns),
            "max_slowdown": np.max(slowdowns),
            "makespan": makespan,
            "num_completed": len(self.completed_jobs),
            "avg_response": np.mean([j.response_time for j in self.completed_jobs]),
        }
