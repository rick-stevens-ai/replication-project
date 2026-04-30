# DRAS: Deep Reinforcement Learning for Cluster Scheduling in High Performance Computing

- **OSTI ID:** 1984484
- **Rank:** #20
- **Replication Score:** 9/10
- **Open-Source Tools:** Yes
- **Code Repository:** Yes
- **Tools:** CQGym, OpenAI Gym, CQSim, RL algorithms (DQL, PG, A2C, PPO), Python

## Why This Paper
Open-source RL libraries, public/simulated data, fully specified methodology, and quantitative validation. Fully automatable.

## Replication Plan
AI sets up CQGym, implements DRAS agents, trains/evaluates on job traces, and reproduces scheduling performance metrics.

## Status
- [x] Paper reviewed (2026-04-30)
- [x] Code/tools identified
- [x] Code implemented — custom simulator + DQN/PPO agents (not CQGym)
- [x] Results reproduced — first-pass replication complete
- [ ] Results validated against paper (partial — see REPORT.md)

## First-Pass Replication (2026-04-30)

**Approach:** Built a custom event-driven HPC cluster simulator with DQN and PPO agents, trained on the HPC2N workload trace (240 nodes, 5K jobs). Simplified from paper's hierarchical two-network design.

**Key Result:** PPO achieves best slowdown (125.8) — 24% better than SJF, 57% better than EASY-backfill. Supports paper's core claim that DRL outperforms traditional schedulers.

| Policy | Avg Wait (s) | Avg Slowdown | Makespan (s) |
|---|---:|---:|---:|
| FCFS | 20,307 | 675.9 | 4,255,008 |
| EASY-BF | 13,047 | 294.4 | 4,254,964 |
| SJF | 6,285 | 166.3 | 4,189,982 |
| DQN | 7,122 | 140.8 | 4,189,982 |
| **PPO** | **6,784** | **125.8** | 4,189,982 |

See `replication/REPORT.md` for full details, gaps, and next steps.
