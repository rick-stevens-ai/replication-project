# ScaWL Replication (OSTI 2587225)

**Paper:** C. Soss et al., *ScaWL: Scaling k-WL (Weisfeiler–Lehman) Algorithms in Distributed-Memory.* OSTI 2587225.

## Status: ✅ Complete — Score 8/10

Independent Python/NumPy re-implementation of 2-WL color refinement with
`multiprocessing`-based parallelism; strong-scaling benchmark reproduces the
qualitative shape of the paper's Table 4 on a 10-core workstation.

## Headline numbers (n=200, d=4 random-regular graph, CherryRd)

| p  | time (s) | speedup (ours) | speedup (paper avg) |
|----|---------:|---------------:|--------------------:|
| 1  | 5.82     | 1.00           | 1.00   |
| 2  | 3.08     | 1.89           | 2.38   |
| 4  | 1.68     | 3.46           | 4.26   |
| 8  | 0.94     | 6.17           | 7.64   |
| 16 | 0.79     | 7.41           | 13.20* |

*paper at 16 cores uses 2 physical sockets; we only have 10 physical cores.

## Correctness (all pass)
- Iso pair (random 4-regular, n=30 with relabeling) ✓
- Non-iso 2-regular pair C12 vs 2×C6 (distinguished by 2-WL but not 1-WL) ✓
- Strongly-regular pair (Shrikhande vs 4×4 rook) — match expected (2-WL cannot distinguish) ✓

## Layout
```
replication/
  src/
    kwl.py              # 2-WL implementation
    benchmark.py        # strong-scaling harness
    test_correctness.py # 3 oracle tests
    plots.py            # figure generator
  results/              # JSON outputs
  figures/              # PDF + PNG plots
  report/
    replication_report.pdf
    replication_report.tex
```

## Reproduce
```
cd replication
python3 -m venv venv && source venv/bin/activate
pip install networkx numpy matplotlib
cd src
python test_correctness.py
python benchmark.py --n 200 --d 4 --procs 1,2,4,8,10,16 --repeats 2 --out ../results/main_n200.json
python plots.py
```
