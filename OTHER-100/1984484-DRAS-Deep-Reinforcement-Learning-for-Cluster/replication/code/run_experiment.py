#!/usr/bin/env python3
"""
Main experiment runner for DRAS replication.

1. Parse SWF trace → CSV
2. Split into train/val/test
3. Run baselines (FCFS, EASY-backfill, SJF)
4. Train DQN and PPO agents
5. Evaluate all policies on test set
6. Save results and generate figures
"""

import os
import sys
import json
import csv
import time
import argparse
import numpy as np
from pathlib import Path

# Add code dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parse_swf import parse_swf
from simulator import ClusterEnv, Job, load_jobs
from baselines import BaselineSimulator
from drl_agent import train_dqn, train_ppo, DQNAgent, PPOAgent, evaluate_dqn, evaluate_ppo


def split_jobs(jobs: list[dict], train_frac: float = 0.4, val_frac: float = 0.1):
    """Split jobs chronologically into train/val/test."""
    n = len(jobs)
    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))
    return jobs[:train_end], jobs[train_end:val_end], jobs[val_end:]


def dict_to_jobs(job_dicts: list[dict]) -> list[Job]:
    """Convert dicts to Job objects."""
    return [Job(
        job_id=d["job_id"],
        submit_time=d["submit_time"],
        run_time=d["run_time"],
        num_nodes=d["num_nodes"],
        req_time=d["req_time"],
    ) for d in job_dicts]


def save_csv(data: list[dict], path: str):
    if not data:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--swf", default="../data/HPC2N-2002-2.2-cln.swf",
                        help="Path to SWF trace file")
    parser.add_argument("--num-nodes", type=int, default=240,
                        help="Number of cluster nodes")
    parser.add_argument("--max-jobs", type=int, default=5000,
                        help="Max jobs to use from trace")
    parser.add_argument("--dqn-episodes", type=int, default=60,
                        help="DQN training episodes")
    parser.add_argument("--ppo-episodes", type=int, default=60,
                        help="PPO training episodes")
    parser.add_argument("--output-dir", default="../data",
                        help="Output directory for results")
    parser.add_argument("--fig-dir", default="../figures",
                        help="Output directory for figures")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.fig_dir, exist_ok=True)

    print("=" * 60)
    print("DRAS REPLICATION EXPERIMENT")
    print("=" * 60)

    # ---- Step 1: Parse trace ----
    print(f"\n[1/6] Parsing SWF trace: {args.swf}")
    all_jobs = parse_swf(args.swf, max_jobs=args.max_jobs)
    print(f"  Loaded {len(all_jobs)} valid jobs")

    # ---- Step 2: Split ----
    print("\n[2/6] Splitting trace (40% train / 10% val / 50% test)")
    train_dicts, val_dicts, test_dicts = split_jobs(all_jobs, 0.4, 0.1)
    print(f"  Train: {len(train_dicts)}, Val: {len(val_dicts)}, Test: {len(test_dicts)}")

    # Save splits
    save_csv(train_dicts, os.path.join(args.output_dir, "train_jobs.csv"))
    save_csv(val_dicts, os.path.join(args.output_dir, "val_jobs.csv"))
    save_csv(test_dicts, os.path.join(args.output_dir, "test_jobs.csv"))

    train_jobs = dict_to_jobs(train_dicts)
    val_jobs = dict_to_jobs(val_dicts)
    test_jobs = dict_to_jobs(test_dicts)

    # ---- Step 3: Run baselines on TEST set ----
    print("\n[3/6] Running baselines on test set...")
    sim = BaselineSimulator(args.num_nodes)
    baseline_results = {}
    for policy in ["fcfs", "easy_backfill", "sjf"]:
        t0 = time.time()
        metrics = sim.run(test_jobs, policy)
        elapsed = time.time() - t0
        baseline_results[policy] = metrics
        print(f"  {policy:15s}: avg_wait={metrics['avg_wait']:10.1f}s  "
              f"avg_slowdown={metrics['avg_slowdown']:8.2f}  "
              f"makespan={metrics['makespan']:>10}s  [{elapsed:.1f}s]")

    # ---- Step 4: Train DQN ----
    print(f"\n[4/6] Training DQN ({args.dqn_episodes} episodes on {len(train_jobs)} train jobs)...")
    env = ClusterEnv(args.num_nodes, window_size=50)
    t0 = time.time()
    dqn_history = train_dqn(env, train_jobs, val_jobs,
                            num_episodes=args.dqn_episodes,
                            save_dir=args.output_dir)
    dqn_time = time.time() - t0
    print(f"  DQN training took {dqn_time:.1f}s")

    # Evaluate DQN on test set
    print("  Evaluating DQN on test set...")
    dqn_agent = DQNAgent(env.obs_dim, env.window_size)
    import torch
    dqn_agent.policy_net.load_state_dict(
        torch.load(os.path.join(args.output_dir, "dqn_model.pt"), weights_only=True))
    dqn_agent.eps = 0.0
    dqn_test_metrics = evaluate_dqn(env, dqn_agent, test_jobs)
    baseline_results["dqn"] = dqn_test_metrics
    print(f"  DQN test: avg_wait={dqn_test_metrics['avg_wait']:.1f}s  "
          f"avg_slowdown={dqn_test_metrics['avg_slowdown']:.2f}  "
          f"makespan={dqn_test_metrics['makespan']}")

    # ---- Step 5: Train PPO ----
    print(f"\n[5/6] Training PPO ({args.ppo_episodes} episodes on {len(train_jobs)} train jobs)...")
    t0 = time.time()
    ppo_history = train_ppo(env, train_jobs, val_jobs,
                            num_episodes=args.ppo_episodes,
                            save_dir=args.output_dir)
    ppo_time = time.time() - t0
    print(f"  PPO training took {ppo_time:.1f}s")

    # Evaluate PPO on test set
    print("  Evaluating PPO on test set...")
    ppo_agent = PPOAgent(env.obs_dim, env.window_size)
    ppo_agent.net.load_state_dict(
        torch.load(os.path.join(args.output_dir, "ppo_model.pt"), weights_only=True))
    ppo_test_metrics = evaluate_ppo(env, ppo_agent, test_jobs)
    baseline_results["ppo"] = ppo_test_metrics
    print(f"  PPO test: avg_wait={ppo_test_metrics['avg_wait']:.1f}s  "
          f"avg_slowdown={ppo_test_metrics['avg_slowdown']:.2f}  "
          f"makespan={ppo_test_metrics['makespan']}")

    # ---- Step 6: Save results ----
    print("\n[6/6] Saving results and generating figures...")

    # Save all results
    save_csv(dqn_history, os.path.join(args.output_dir, "dqn_training_history.csv"))
    save_csv(ppo_history, os.path.join(args.output_dir, "ppo_training_history.csv"))

    # Save test results summary
    summary = []
    for policy, metrics in baseline_results.items():
        row = {"policy": policy}
        row.update(metrics)
        summary.append(row)
    save_csv(summary, os.path.join(args.output_dir, "test_results.csv"))

    with open(os.path.join(args.output_dir, "test_results.json"), "w") as f:
        json.dump(baseline_results, f, indent=2, default=str)

    # Print final summary
    print("\n" + "=" * 70)
    print("FINAL TEST RESULTS")
    print("=" * 70)
    print(f"{'Policy':<15} {'Avg Wait (s)':>12} {'Avg Slowdown':>13} {'Makespan (s)':>13} {'Completed':>10}")
    print("-" * 70)
    for policy in ["fcfs", "easy_backfill", "sjf", "dqn", "ppo"]:
        m = baseline_results[policy]
        print(f"{policy:<15} {m['avg_wait']:>12.1f} {m['avg_slowdown']:>13.2f} "
              f"{m['makespan']:>13} {m['num_completed']:>10}")

    # Generate figures
    generate_figures(baseline_results, dqn_history, ppo_history, args.fig_dir)

    print(f"\nAll outputs saved to {args.output_dir} and {args.fig_dir}")


def generate_figures(results: dict, dqn_history: list, ppo_history: list, fig_dir: str):
    """Generate comparison bar charts and learning curves."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    policies = ["fcfs", "easy_backfill", "sjf", "dqn", "ppo"]
    labels = ["FCFS", "EASY-BF", "SJF", "DQN", "PPO"]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0"]

    # ---- Bar chart: Average Wait Time ----
    fig, ax = plt.subplots(figsize=(8, 5))
    waits = [results[p]["avg_wait"] for p in policies]
    bars = ax.bar(labels, waits, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Average Wait Time (seconds)")
    ax.set_title("Average Job Wait Time by Scheduling Policy")
    # Add value labels
    for bar, val in zip(bars, waits):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(waits)*0.01,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(waits) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "avg_wait_time_comparison.png"), dpi=150)
    plt.close()

    # ---- Bar chart: Average Slowdown ----
    fig, ax = plt.subplots(figsize=(8, 5))
    slowdowns = [results[p]["avg_slowdown"] for p in policies]
    bars = ax.bar(labels, slowdowns, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Average Slowdown")
    ax.set_title("Average Job Slowdown by Scheduling Policy")
    for bar, val in zip(bars, slowdowns):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(slowdowns)*0.01,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(slowdowns) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "avg_slowdown_comparison.png"), dpi=150)
    plt.close()

    # ---- Bar chart: Makespan ----
    fig, ax = plt.subplots(figsize=(8, 5))
    makespans = [results[p]["makespan"] / 3600 for p in policies]  # hours
    bars = ax.bar(labels, makespans, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Makespan (hours)")
    ax.set_title("Makespan by Scheduling Policy")
    for bar, val in zip(bars, makespans):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(makespans)*0.01,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(makespans) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "makespan_comparison.png"), dpi=150)
    plt.close()

    # ---- Learning curves ----
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # DQN learning curve
    ax = axes[0]
    eps = [h["episode"] for h in dqn_history]
    train_waits = [h["train_avg_wait"] for h in dqn_history]
    val_waits = [h["val_avg_wait"] for h in dqn_history]
    ax.plot(eps, train_waits, label="Train Avg Wait", color="#E91E63", alpha=0.7)
    ax.plot(eps, val_waits, label="Val Avg Wait", color="#E91E63", linestyle="--")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Average Wait Time (s)")
    ax.set_title("DQN Learning Curve")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # PPO learning curve
    ax = axes[1]
    eps = [h["episode"] for h in ppo_history]
    train_waits = [h["train_avg_wait"] for h in ppo_history]
    val_waits = [h["val_avg_wait"] for h in ppo_history]
    ax.plot(eps, train_waits, label="Train Avg Wait", color="#9C27B0", alpha=0.7)
    ax.plot(eps, val_waits, label="Val Avg Wait", color="#9C27B0", linestyle="--")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Average Wait Time (s)")
    ax.set_title("PPO Learning Curve")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "learning_curves.png"), dpi=150)
    plt.close()

    # ---- Combined reward curves ----
    fig, ax = plt.subplots(figsize=(8, 5))
    dqn_rewards = [h["train_reward"] for h in dqn_history]
    ppo_rewards = [h["train_reward"] for h in ppo_history]
    ax.plot(range(len(dqn_rewards)), dqn_rewards, label="DQN", color="#E91E63", alpha=0.7)
    ax.plot(range(len(ppo_rewards)), ppo_rewards, label="PPO", color="#9C27B0", alpha=0.7)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Cumulative Episode Reward")
    ax.set_title("Training Reward Curves")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "reward_curves.png"), dpi=150)
    plt.close()

    print(f"  Saved 5 figures to {fig_dir}/")


if __name__ == "__main__":
    main()
