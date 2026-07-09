# Brief

Independent replication of Hawks et al. 2026 (OSTI 3018489), *"wa-hls4ml: A Benchmark
and Surrogate Models for hls4ml Resource and Latency Estimation"* (ACM TRETS 19(2), Article
20; FERMILAB-PUB-25-0359-CSAID). The paper releases a 683k-sample public benchmark
dataset of hls4ml-synthesized FPGA designs on HuggingFace (`fastmachinelearning/wa-hls4ml`,
CC-BY-NC 4.0) plus three surrogate architectures (baseline MLP, GNN, Transformer) that
predict FPGA resource usage (BRAM/DSP/FF/LUT) and latency (Cycles/II) for hls4ml-generated
neural network accelerators.

We downloaded the public HuggingFace release (52,391 fully-connected training samples +
11,229 test samples + 886 exemplar samples), extracted the paper's baseline
`rule4ml`-style aggregate feature set (§4.1: 22 features covering layer counts, size,
BOPs proxy, precision, reuse factor, strategy, and target board), and trained a
per-target MLP (200 epochs, log-transformed targets, Adam, MSE loss on standardized
log-targets — the closest reproducible reading of the paper's "mean squared logarithmic
loss" recipe). Total training time 159 s on one A100. We evaluated with the paper's exact
metric definitions (R², SMAPE with ε=1, RMSE per Eqs. 1–3).

Result: the dataset and baseline-MLP methodology are reproducible from the paper text
alone. On dense-only test data our MLP obtains R²={BRAM 0.46, DSP 0.78, FF 0.90, LUT 0.92,
Cycles 0.92, II 0.91} — in the same order-of-magnitude as (in fact higher than) the paper's
Table 4 "Dense" MLP row for FF/LUT/Cycles/II, and matching the paper's stated ordering that
dense outperforms mixed. On the 886-sample exemplar set the aggregated R²={-49.4, 0.33,
0.24, 0.04, 0.24, 0.28} reproduces the paper's Table-5 generalization-gap finding
(especially the negative-R² collapse for BRAM). GNN and Transformer variants and the
Conv1D/Conv2D subsets are out of scope for this compute budget. Verdict: **PARTIAL**.
