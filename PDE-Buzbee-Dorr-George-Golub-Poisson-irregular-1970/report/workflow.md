# Workflow, tools, codes, effort

## Workflow (end-to-end)

```
[Semantic Scholar API]                       (paper metadata + OA link)
        |
        v
[OSTI purl 4060961]  --curl via uicgpu-->    paper.pdf (1.34 MB, SHA-256 fd92...)
        |
        v
[pdftotext -layout]                          extraction/marker.md
        |
        v
[hand-structured stub]                       extraction/nougat.mmd
        |
        v
[capacitance_solver.py]  ------------------->  Table 1 replication (evidence.json)
[mms_convergence.py]     ------------------->  O(h^2) convergence (mms_convergence.json)
[lshape_splitting.py]    ------------------->  §5 splitting (lshape_evidence.json)
        |                                              |
        +---> cross-check vs scipy sparse spsolve  <--+
        v
[REPORT.md + REPORT.tex + open_questions.json + failure_analysis.md]
```

## Tools & versions

| Tool | Version | Used for |
|---|---|---|
| Python | 3.13.x (macOS system) | driver, numerics |
| NumPy | 2.4.3 | dense linear algebra |
| SciPy | 1.18.0 | `scipy.sparse.linalg.splu`, `spsolve` |
| pdftotext (poppler) | system | text extraction fallback |
| curl | system | paper fetch via uicgpu proxy |
| ssh + scp | system | cross-host paper retrieval |
| Semantic Scholar API | v1 | paper metadata + OA URL |
| Unpaywall API | v2 | OA fallback (returned null in this case) |

## Compute

- **Local (CherryRd)** — all real numerical work (`N` up to 128, dense
  `p×p` capacitance solve up to `p = 1089`). Total wall time under 1 min.
- **Remote (uicgpu)** — only used for the *one* `curl` that CherryRd's
  firewall blocked. No GPU work was needed (this is 1971-era numerics —
  n < 5000 dense/sparse; SuperLU on a laptop is 5 orders of magnitude
  faster than a CDC 6600).

## Effort estimate

| Phase | Wall time |
|---|---:|
| Paper acquisition (S2 → uicgpu → scp) | ~4 min |
| Extraction (pdftotext + hand-structuring nougat.mmd) | ~5 min |
| Reading paper (esp. §2, §4, §5, Table 1) | ~10 min |
| Solver implementation (capacitance_solver.py) | ~15 min |
| Sign-bug diagnosis + fix | ~3 min |
| MMS convergence study | ~5 min |
| L-shape splitting implementation | ~15 min |
| Report writing | ~15 min |
| **TOTAL** | **~72 min** |

Real human-expert baseline for a numerics grad student first exposure to
capacitance-matrix methods: probably 1-2 days for the same replication.

## Key numerical claims verified

1. **Zero-truncation-error test (paper Table 1, u = x^2+y^2)** — max
   error at float64 machine precision (5e-16 to 9e-15) across all four
   configs. Paper reported 4e-13 to 2e-12 on CDC 6600 (~60-bit
   floating-point). Order-of-magnitude match once precision differences
   are accounted for.
2. **Capacitance-vs-direct-sparse consistency** — <=1e-14 in every
   case. The low-rank Woodbury correction reproduces the direct
   irregular-region solve to machine precision.
3. **O(h^2) convergence with smooth non-quadratic MMS** — measured rates
   1.984, 1.993, 1.997 (imbedding on Region 2) and 1.995, 1.997, 1.999
   (splitting on L-shape). Both regions and both methods.
4. **Preprocessing cost of `p+1` rectangle solves + one dense p x p
   solve** — confirmed operationally; recorded in evidence JSONs.
5. **Per-RHS cost of 2 rectangle solves + one p x p triangular solve** —
   confirmed operationally.
