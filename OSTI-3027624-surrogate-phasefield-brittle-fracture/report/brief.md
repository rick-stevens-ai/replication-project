# Brief — OSTI-3027624 phase-field brittle-fracture ML surrogate benchmark

Independent reduced-budget replication of Hamdi & Lejeune (2025) benchmarking FNO vs UNet surrogates for phase-field brittle-fracture crack prediction. Using the paper's real pfm_bench dataset (50 sims) + the paper's own architectures on an A100, a 3-seed benchmark reproduced the headline claim that UNet (Dice 0.53) substantially beats FNO (Dice 0.10) on sparse crack morphology, and that ensembling is stable. Absolute Dice below the paper's full-budget 0.62/0.68 due to reduced training set. Verdict: PARTIAL.
