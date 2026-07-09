# Artifacts Summary — OSTI 2552927 NeuroSEM

## Upstream release (author repo)
Repository: `https://github.com/ZongrenZou/NeuroSEM`
Commit: `b5f027a` (2024-12-20)
Total size: **111 MB**
Status: PUBLIC, complete for the PINN half of the pipeline.

### What ships
| Category | Contents | Notes |
|---|---|---|
| Trained PINN checkpoints | **40+** `.eqx` (JAX/Equinox) files | Case A, Case B, Case C (5 noise variants), Case D subdomain cutout, 16 cylinder-flow variants |
| PyTorch traced models | `traced_rbc_model_*.pt` | Direct drop-in for Nektar++ `torch.jit::load` at the C++/`PINNBodyForce.cpp` interface |
| SEM reference solutions | `cavity/case_b/data/data_{1e4,1e5,1e6}.mat` | 300,832 pts (Ra=1e4), 169,218 pts (Ra=1e5, 1e6); Nektar++ quadrature grid |
| Case A training inputs | `cavity/case_a/outputs/RBC_*.mat` | 10,000 scattered (x,y,u,v) samples per Ra; verified to be exact draws from SEM reference (KD-tree median dist = 0) |
| Real experimental data | `piv/data/PINNdata_dSpace1_dTime1.mat` | Horseshoe-vortex PIV, Re=833.33, 51 snapshots, 725,423 velocity samples |
| Per-scenario scripts | `cavity/case_a/`, `case_b/`, `case_c/`, `case_d/`, `cylinder/`, `piv/` | Training + eval scaffolding |

### What does NOT ship (critical gap)
- The **Nektar++ C++ coupling layer**: `PINNBodyForce.cpp`, modified
  `UnsteadyAdvection.cpp`. These are the actual glue that makes it a
  "hybrid" method. Reimplementation required for downstream end-to-end
  reruns.
- Nektar++ build recipe / dockerfile pinned to a specific
  Nektar++ version.
- Training-seed / iteration manifest per checkpoint (would let outside
  groups verify which noise seed produced which Case C row of Table 3).

## Downstream (this replication)

### Fetched paper
- `paper.pdf` — 6,528,181 B, PDF v1.7 from OSTI purl `2552927`.
- `paper.txt` — 1,197 lines via `pdftotext -layout`.

### Extraction
- `extraction/marker.md` — (not created for this paper; text extraction
  used pdftotext only).

### Working code (in `work/`)
- `eval_case_a.py` — reload Case A T-surrogate, evaluate on SEM ref.
- `eval_case_b.py` — reload Case B (u,v,p)-surrogate, evaluate on SEM ref.

### Evidence (in `evidence/`)
- `eval_case_a.json` — raw L2 error numbers for Ra ∈ {1e4, 1e5, 1e6}.
- `eval_case_b.json` — raw L2 error numbers for u, v components.

### Reports (in `report/`)
- `REPORT.md` — canonical markdown replication report.
- `REPORT.tex` — LaTeX version with dedicated Genuine Critique section.
- `open_questions.json` — 5 truly open questions with basis + next steps.
- `workflow.md` — chronological pipeline record.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — what did not work / what was not attempted.

## Compute footprint
- Host: uicgpu (8×A100).
- Env: `fem-pinns` micromamba.
- GPU usage: single A100, JAX vmap over 300,832 points, sub-minute
  eval per checkpoint.
- Wall clock (component evaluation): < 10 minutes total across all six
  cavity checkpoints.

## Reproducibility check
- All shipped `.eqx` checkpoints load without error under the pinned
  `jax==0.4.30 / equinox==0.11.10` stack.
- All six cavity L2 errors reported in `evidence/eval_case_*.json` are
  deterministic (JAX PRNG not used at inference).
- KD-tree provenance check on Case A training inputs is deterministic
  and returns exact zeros.
