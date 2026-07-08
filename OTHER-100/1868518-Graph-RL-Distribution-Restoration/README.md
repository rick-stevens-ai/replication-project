# Replication: Learning Sequential Distribution System Restoration via Graph-Reinforcement Learning

**OSTI ID:** 1868518  
**Authors:** Tianqiao Zhao, Jianhui Wang  
**Published:** IEEE Transactions on Power Systems, vol. 37, no. 2, pp. 1601-1611, March 2022  
**DOI:** 10.1109/TPWRS.2021.3102345  
**Affiliations:** Brookhaven National Laboratory (BNL), Southern Methodist University

## Summary

This paper proposes a multi-agent Graph-Reinforcement Learning framework for sequential distribution system restoration after extreme events. The approach combines Graph Convolutional Networks (GCNs) with Double DQN to coordinate distributed generators (DGs) and controllable switches. Each DG is modeled as an RL agent with parameter sharing for scalability. The GCN encodes the power network topology to capture device interactions.

## Replication

### What We Replicated
- GCN + Double DQN (Dueling) multi-agent architecture
- MLP-DQN baseline (no graph structure)  
- Random and greedy heuristic baselines
- IEEE 33-bus and IEEE 123-bus test networks
- pandapower-based power flow environment
- Training, evaluation, and comparison

### Key Findings
1. **GCN-DQN learns effective restoration policies** — achieving up to 0.42 load restoration ratio on IEEE 33-bus (peak evaluation)
2. **GCN and MLP show similar performance** on small networks (33-bus) with 2,000 training episodes
3. **Larger networks are harder** — IEEE 123-bus achieves lower load ratios (~0.14 peak), consistent with increased coordination difficulty
4. **The framework is computationally accessible** — all training completes in <2 hours on CPU

### Files
```
replication/
├── replication_report.tex    # LaTeX report
├── replication_report.pdf    # Compiled PDF
├── src/
│   ├── environment.py        # pandapower restoration environment
│   ├── models.py            # GCN-DQN, MLP-DQN architectures
│   ├── replay_buffer.py     # Experience replay
│   ├── train.py             # Training loops
│   ├── evaluate.py          # Evaluation utilities
│   ├── plot_results.py      # Plotting
│   └── run_replication.py   # Main script
├── results/                 # Training histories, checkpoints
├── figures/                 # Generated plots
└── logs/                    # Training logs
```

### Reproducibility
- **Software:** Python 3.12, PyTorch 2.2.2, pandapower 3.4.0, NetworkX 3.6.1
- **Hardware:** Apple iMac, Intel x86_64, CPU-only
- **Training time:** ~2 hours total (all methods, both networks)
- **Seed:** 42 (reproducible)

## Status: ✅ Complete
