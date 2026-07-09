# Workflow

## Pipeline

```
[arXiv PDF fetch]                       curl → paper.pdf                        ~5 s
      ↓
[Text extraction]                       pdftotext -layout → paper.txt           ~1 s
      ↓
[extraction/{marker.md, nougat.mmd}]    pdftotext -layout fallback               ~1 s
      ↓
[Independent implementation]            work/vqe_poisson.py
   ├── gate primitives: apply_ry_layer, apply_cnot (big-endian consistent)
   ├── poisson_A(n, bc), poisson_f(n) — problem setup
   ├── cost_Eh(θ) = -½<f|ψ>²/<ψ|A|ψ>
   └── solve_vqe(n, L=5, seed) — L-BFGS-B
      ↓
[Unit tests]                            work/test_gates.py                      ~5 s
   ├── endianness probe (Ry(π) on q0 |00> = |10>)
   ├── CNOT big-endian probe
   └── Poisson matrix sanity
      ↓
[Main sweep]                            work/vqe_poisson.py __main__            ~7 min
   ├── 4 n × 2 BC × 10 trials = 80 runs
   └── evidence/results_summary.json
      ↓
[n=5 deep multistart]                   work/vqe_n5_deep.py                     ~4 min
   └── evidence/n5_dirichlet_3restart.json
      ↓
[O(1) cost structural check]            work/verify_o1_cost.py                  ~3 s
   └── evidence/o1_cost_analysis.txt
      ↓
[LLM judge]                             work/judge.py → Argo gpt-5.2            ~10 s
   └── evidence/judge_response.json
      ↓
[Report assembly]                       report/REPORT.md, REPORT.tex,
                                        open_questions.json, brief.md,
                                        artifact_harvest.md, workflow.md,
                                        failure_analysis.md, artifacts_summary.md
```

## Tools and versions

| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 | driver |
| numpy | 2.4.3 | statevector arithmetic |
| scipy | 1.18.0 | L-BFGS-B optimizer |
| pdftotext | poppler | text extraction (marker fallback) |
| Argo aggregator | localhost:44497 (503 today) / cherryrd:4000 (up) | LLM judge |
| model | `argo:gpt-5.2` | LLM judge (fallback for `argo:claude-opus-4.7`) |

## Effort estimate

| Phase | Wall time | Human time (equivalent) |
|---|---|---|
| Paper fetch + wrong-arXiv-ID triage | 5 min | 10 min |
| Extraction + marker/nougat mirrors | 1 min | 2 min |
| Independent implementation from scratch (Ry, CNOT, ansatz, cost) | 15 min | 3 h if a human wrote it |
| Endianness bug find + fix via unit test | 5 min | 30 min |
| Full sweep run | 7 min | (compute) |
| Multistart deep dive n=5 | 4 min | (compute) |
| O(1) structural check | 3 min | 30 min for a human |
| LLM judge (with aggregator fallback) | 5 min | 10 min |
| Report assembly (all 8 artifacts) | 25 min | 4 h |
| **Total** | **~70 min wall / ~15 min human-attention equivalent for the AI** | **~8 h if a human PhD student did it** |

## Compute footprint

- Host: CherryRd (Apple M1, macOS Darwin 25.3)
- Cores used: 1 (numpy single-thread)
- GPU: none needed
- Memory: <200 MB
- Network: 786 kB (paper.pdf) + ~10 kB (LLM judge)

Heavy compute (uicgpu) NOT required for this replication. The state-vector simulation at
n=5 is a 32-dim vector; even the full 80-trial sweep fits comfortably on any laptop.
