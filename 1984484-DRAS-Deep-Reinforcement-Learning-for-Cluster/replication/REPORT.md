# DRAS Replication Report

**Paper:** Fan Zhang et al., "DRAS: Deep Reinforcement Learning for Cluster Scheduling in High Performance Computing" (2020)  
**Replication date:** 2026-04-30  
**Replicator:** Ollie (automated replication subagent)

---

## 1. Summary

This is a first-pass replication of the DRAS paper, which proposes using Deep Reinforcement Learning (DRL) to schedule HPC jobs, outperforming traditional policies like FCFS+backfill on metrics such as average wait time and slowdown.

We implemented:
- An event-driven HPC cluster simulator
- Three baseline policies (FCFS, EASY-Backfill, SJF)
- Two DRL agents (DQN and PPO) trained on the HPC2N workload trace

## 2. Experimental Setup

### Workload Trace
- **Source:** HPC2N-2002-2.2-cln.swf from the [Parallel Workloads Archive](https://www.cs.huji.ac.il/labs/parallel/workload/)
- **Cluster:** 240-node Linux cluster (Seth), MAUI scheduler
- **Jobs used:** 5,000 (first valid jobs from ~203K total)
- **Split:** 2,000 train / 500 validation / 2,500 test (chronological)

### Simulator
- Event-driven: scheduling triggered on job arrival or completion
- 240 homogeneous nodes
- Jobs are rigid (fixed node count throughout execution)

### State Representation (simplified from DRAS)
- **Per-job features (window W=50):** normalized node count, normalized request time, normalized wait time
- **Per-node features (N=240):** availability (0/1), normalized time until free
- **Total obs dimension:** 630 (50×3 + 240×2)

### DRL Agents
| Hyperparameter | DQN | PPO |
|---|---|---|
| Hidden layers | 256, 128 | 256, 128 (shared) |
| Learning rate | 0.001 | 0.0003 |
| Gamma (discount) | 0.99 | 0.99 |
| Epsilon (exploration) | 1.0 → 0.74 (decay 0.995) | N/A (stochastic policy) |
| PPO clip | N/A | 0.2 |
| Entropy coef | N/A | 0.01 |
| Replay buffer | 50,000 | N/A (on-policy) |
| Batch size | 64 | 64 |
| Training episodes | 60 | 60 |
| Training time | 475s | 156s |

### Reward Function (simplified DRAS Eq. 1)
```
R = (wait_frac + size_frac + utilization) / 3
```
where `wait_frac = wait_time / 86400`, `size_frac = job_nodes / total_nodes`, `utilization = occupied_nodes / total_nodes`.

## 3. Results

### Test Set Performance (2,500 jobs)

| Policy | Avg Wait (s) | Avg Slowdown | Makespan (s) | Avg Response (s) | Completed |
|---|---:|---:|---:|---:|---:|
| FCFS | 20,307 | 675.9 | 4,255,008 | 36,266 | 2,500 |
| EASY-Backfill | 13,047 | 294.4 | 4,254,964 | 29,007 | 2,500 |
| SJF | 6,285 | 166.3 | 4,189,982 | 22,245 | 2,500 |
| **DQN** | 7,122 | 140.8 | 4,189,982 | 23,082 | 2,500 |
| **PPO** | **6,784** | **125.8** | 4,189,982 | **22,744** | 2,500 |

### Key Observations

1. **PPO achieves the best slowdown (125.8)** — 24% better than SJF, 57% better than EASY-backfill, 81% better than FCFS.

2. **SJF has the lowest average wait time (6,285s)**, but PPO is within 8% (6,784s) while having 24% better slowdown. This indicates PPO finds a better balance between prioritizing short jobs and managing wait times.

3. **DQN performance is close to PPO** (avg slowdown 140.8 vs 125.8) but slightly worse, consistent with the paper's finding that policy gradient methods outperform DQL.

4. **FCFS is worst across all metrics** — expected, as it has no intelligence about job sizes or resource efficiency.

5. **EASY-Backfill improves significantly over FCFS** (36% lower wait, 56% lower slowdown) by filling gaps with smaller jobs, but is still far from the DRL agents.

6. **Makespan is identical for SJF/DQN/PPO** (4,189,982s) — all three achieve the same total time span. Only FCFS and EASY-backfill have slightly higher makespans.

### Learning Curves

- **DQN:** Validation wait time decreases from ~2,470s to ~2,140s over 60 episodes. Loss diverges (common DQN instability) but scheduling quality still improves.
- **PPO:** Converges quickly — validation wait time is already near-optimal by episode 5 (~2,080s), with loss steadily decreasing from 17,803 to 197.

## 4. Comparison with Original Paper

### Agreements ✅
- DRL agents outperform FCFS and EASY-backfill on wait time and slowdown
- PPO/PG methods outperform DQN (consistent with paper's DRAS-PPO > DRAS-DQL finding)
- DRL achieves competitive or better slowdown than all baselines
- Training converges within ~50 episodes (paper reports similar convergence speed)

### Gaps / Simplifications ⚠️

| Aspect | Original DRAS | Our Replication |
|---|---|---|
| **Trace** | Theta (ALCF) — 121K jobs, 4,360 nodes | HPC2N — 5K jobs, 240 nodes |
| **State rep** | 4,460×2 matrix (conv1D) | 630-dim flat vector (FC layers) |
| **Architecture** | Conv + 4000/1000 FC (~21M params) | 256/128 FC (~0.2M params) |
| **Hierarchical** | Level-1 (select) + Level-2 (backfill) NNs | Single-level (select only) |
| **Backfill** | Learned backfill via Level-2 NN | RL agent can pick any job in window |
| **Reward** | Eq. 1 with w₁=w₂=w₃=1/3 | Simplified version of Eq. 1 |
| **Training data** | 100 jobsets (sampled + real + synthetic) | Single 2K-job trace, replayed 60× |
| **SJF baseline** | Not in paper | Added for comparison |
| **Reservation** | When selected job doesn't fit, reserve earliest nodes | Not implemented (RL skips unfittable jobs) |
| **Job dependencies** | 2.25% of Theta jobs have dependencies | Not modeled |

### Honest Assessment

The replication demonstrates the **core claim** — that DRL can outperform traditional HPC scheduling on slowdown — but uses a much smaller and simpler setup than the paper. The paper's hierarchical two-network design with learned backfill and curriculum training is significantly more sophisticated than our single-policy-network approach.

Our PPO agent beating SJF on slowdown (125.8 vs 166.3) while having only 8% worse wait time is a strong result that supports the paper's thesis. However, our DQN agent showed training instability (loss divergence) that the paper likely avoided with their larger network and different architecture.

## 5. Files

```
replication/
├── code/
│   ├── parse_swf.py          # SWF trace parser
│   ├── simulator.py          # Event-driven cluster simulator
│   ├── baselines.py          # FCFS, EASY-backfill, SJF
│   ├── drl_agent.py          # DQN and PPO agents
│   └── run_experiment.py     # Main experiment runner
├── data/
│   ├── HPC2N-2002-2.2-cln.swf  # Raw workload trace
│   ├── train_jobs.csv        # Training split (2,000 jobs)
│   ├── val_jobs.csv          # Validation split (500 jobs)
│   ├── test_jobs.csv         # Test split (2,500 jobs)
│   ├── test_results.json     # Final per-policy metrics
│   ├── test_results.csv      # Same, CSV format
│   ├── dqn_training_history.csv  # Per-episode DQN metrics
│   ├── ppo_training_history.csv  # Per-episode PPO metrics
│   ├── dqn_model.pt          # Trained DQN weights
│   └── ppo_model.pt          # Trained PPO weights
└── figures/
    ├── avg_wait_time_comparison.png
    ├── avg_slowdown_comparison.png
    ├── makespan_comparison.png
    ├── learning_curves.png
    └── reward_curves.png
```

## 6. Reproducing

```bash
conda create -n dras python=3.11 -y
conda activate dras
pip install torch numpy matplotlib

cd replication/code
python run_experiment.py \
    --swf ../data/HPC2N-2002-2.2-cln.swf \
    --num-nodes 240 \
    --max-jobs 5000 \
    --dqn-episodes 60 \
    --ppo-episodes 60
```

Total runtime: ~11 minutes on a 2020 iMac (CPU only).

## 7. Next Steps (if continuing)

1. **Scale up:** Use full HPC2N trace (200K+ jobs) or download ANL-Intrepid trace (closer to Theta)
2. **Hierarchical design:** Implement Level-2 backfill network
3. **Convolutional architecture:** Use 1×2 conv layer as in paper
4. **Curriculum training:** Implement 3-phase training with synthetic workloads
5. **Reservation mechanism:** When selected job doesn't fit, reserve nodes and activate backfill
6. **Larger networks:** Scale to paper's 4000/1000 FC sizes
7. **Fix DQN instability:** Add gradient clipping, reduce learning rate, use double DQN
