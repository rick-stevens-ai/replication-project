# Workflow

## Steps taken (in order)

1. **Read the wave brief** and target dossier — Diamzon & Venturi (2026), OSTI 2928634.
2. **Fetch PDF** via `ssh uicgpu` (proxy env for OSTI reachability) → `paper.pdf` in target dir.
3. **Extract text** with PyMuPDF (paper exceeds MCP `pdf` tool 10 MB limit).
4. **Read paper** carefully: title, authors, method, Eqs. 37/41/42 (moments), Eq. A.4 (PDF), Table 2 (β=1.5 test), Fig. 10 (depth trend), Section 8 numerical setup (Nx=Ny=31, N=64, L∈{1,5,20}, Adam, 1M samples).
5. **Design replication code** (`work/replicate.py`): GLL grid, operator, MLP, analytic moments (exact Jacobian at μ), analytic PDF (Fourier sinc-product), MC benchmark, per-β sweep, per-L sweep, Table 2 head-to-head extraction.
6. **Push code to uicgpu**, run smoke test (small config).
7. **Full run** on A100: L∈{1,5,20}, 500k train samples, 60 epochs, 100k MC samples.
8. **Notice L=20 collapsed** — retrained with Kaiming init + warmup schedule (`work/retrain_L20.py`).
9. **Pull results** and models back to local Dropbox target dir.
10. **Generate 6 figures** (`work/make_figures.py`).
11. **LLM judge pass** (`work/judge.py`) via Argo (Opus 4.7 502'd; fell back to GPT-5.2).
12. **Write report** (REPORT.md, brief.md, attempt_log.md, artifact_harvest.md, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json).
13. **Emit WAVE_RESULT** line.

## Tools + codes + versions

| Component | Tool / Library | Version | Where |
|---|---|---|---|
| Text extraction | PyMuPDF (`fitz`) | system default (Python 3.14 on cherryrd) | cherryrd |
| GLL / operator | NumPy | system Python 3.14 | cherryrd for figures; uicgpu Python 3.8 for main run |
| MLP training | PyTorch | 1.11.0 | uicgpu |
| GPU | NVIDIA A100 80GB PCIe (CUDA_VISIBLE_DEVICES=0) | driver + CUDA per uicgpu env | uicgpu |
| Analytic PDF | NumPy Fourier integrate | — | cherryrd (post-hoc) and inside training loop on uicgpu |
| Figures | matplotlib | system | cherryrd |
| Judge | Argo LLM proxy (localhost:44497) — `argo:claude-opus-4.7` intended, `argo:gpt-5.2` used after 502s | Argo runtime | cherryrd |

All model weights saved as `report/evidence/model_L{1,5,20}.pt`. Full results in `report/evidence/replication_results.json`. Training + smoke logs in `report/evidence/run.log` and `report/evidence/run_L20.log`.

## Effort estimate

| Phase | Wall time | Human effort |
|---|---|---|
| Read paper + design | ~15 min | active reading |
| Write replication code | ~10 min | one-shot |
| Smoke test on uicgpu | ~1 min | check-only |
| Full sweep L=1,5,20 (60 ep) | ~4 min GPU + overhead | idle |
| Retrain L=20 (150 ep) | ~4 min GPU | idle |
| Figures + judge | ~2 min | idle |
| Report | ~10 min | one-shot |
| **Total** | **≈ 40 min wall clock, ≈ 10 min pure GPU** | **≈ 40 min agent-time** |

A100 utilisation was low; the whole thing could fit on a single mid-range GPU or even a strong CPU-only box (training would just be ~10× slower).
