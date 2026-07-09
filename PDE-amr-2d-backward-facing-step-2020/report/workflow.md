# Workflow, Tools, and Effort

## End-to-end workflow

1. **Wave brief + standard ingest**
   - `cat ~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`
   - `cat ~/Dropbox/REPLICATE-PROJECT/scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`
   - Discovered pre-existing sibling `PDE-Li-Li-AMR-backwardstep-2020/`. Per brief rule
     "do NOT overwrite existing sibling dirs", created new target
     `PDE-amr-2d-backward-facing-step-2020/`; consulted sibling for context only, did
     not copy any files.

2. **Paper retrieval attempts**
   - `curl -IL "https://doi.org/10.1142/s0219876220410121"` → WSPC 403 Cloudflare
   - S2 API via keychain-stored key → SUCCESS: abstract + tldr + metadata
   - Unpaywall API → `is_oa=False`
   - arXiv search / ResearchGate profile → no PDF
   - **Verdict on access**: paywalled. Proceed on SPOT-CHECK / independent-verification path.

3. **paper.pdf stand-in generation**
   - venv `~/.openclaw/workspace/venvs/pde-repl` with `reportlab, numpy, scipy, matplotlib`
   - Wrote a 2.7 kB PDF containing full metadata + verbatim S2 abstract as the source-of-
     truth for artifacts 1/2/3.

4. **Independent BFS-NS solver (`work/bfs_psi_omega.py`)**
   - Formulation: stream-function/vorticity (ψ-ω)
   - Grid: uniform Cartesian, staggered-like access via `psi[j,i]` with fluid mask for
     the solid step
   - Discretisation: central FD for ψ Laplacian; hybrid central/1st-upwind for
     ω-convection (Péclet-switched); central FD for ω-Laplacian
   - Time integration: RK2 explicit, adaptive dt (CFL 0.35)
   - Poisson: sparse LU factor (`scipy.sparse.linalg.splu`) built ONCE per grid,
     BC-contributions vectorised via a one-shot `Bmap` sparse matrix, RHS assembly is
     `-omega[unknown_mask] - Bmap @ psi_flat` (single sparse mat-vec)

5. **Manufactured VDAMR verification (`work/vdamr_synthetic.py`)**
   - Field: base_psi = analytic Poiseuille (upstream + downstream) + Gaussian-perturbation
     vortex at KNOWN (xc, yc) with amplitude A, width σ
   - Sweep 6 grids dx ∈ {0.4, 0.2, 0.1, 0.05, 0.025, 0.0125}
   - Recovery: (a) argmin(ψ) in downstream lower-half, (b) 2D quadratic sub-grid fit
   - Metrics: max|div|, mean|div|, VDAMR flag_frac (|div| > 0.1·max|div|), vortex-centre
     error vs finest-grid reference, log-log slope for observed convergence order

6. **Post-processing (`work/vdamr_analysis.py`)**
   - Self-convergence order (least-squares log-log slope, excluding the finest grid)
   - Monotonicity check on flag_frac under coarsest-to-finest ordering
   - JSON summary → `report/evidence/synthetic_v2/vdamr_analysis.json`

7. **Reference-data curation (`work/reference_data.py`)**
   - Armaly-1983 (10 pts) + Erturk-2008 (10 pts) BFS x_r/S(Re) tables
   - Reynolds convention conversion helpers
   - JSON dump → `report/evidence/reference_bfs_data.json`

8. **BFS-NS Re sweep + mesh refinement**
   - Re ∈ {50, 100, 200} at dx=0.1, T=150; Re=50 at dx ∈ {0.25, 0.15, 0.10, 0.075},
     T=200
   - All runs on `uicgpu` (8×A100, 255 cores, 2 TB RAM); sourced `~/env.sh` for proxy.

9. **LLM judge (`work/llm_judge.py`)**
   - Aggregator: `http://<tailnet-aggregator>:4000/v1/chat/completions`, `Bearer stevens`
   - Model: `argo:gpt-5.2` (fallback after `argo:claude-opus-4.8` and `.7` returned
     litellm HTTP 502 upstream-response validation errors, 2026-07-06)
   - Strict-JSON schema: verdict + per-claim coverage + agreement_pct + justification
   - Result at `report/evidence/llm_judge_result.json`

10. **Report + 8-artifact bundle**
    - REPORT.md, REPORT.tex, brief.md, attempt_log.md, artifact_harvest.md
    - open_questions.json (5 grounded questions with next_steps)
    - workflow.md (this file), artifacts_summary.md, failure_analysis.md

## Tools + code + versions

| Layer | Tool | Version | Role |
|---|---|---|---|
| OS  | macOS 15.3 (host: CherryRd) / Ubuntu (uicgpu) | — | Local orchestration; remote compute |
| Language | Python | 3.10 (uicgpu) / 3.14 (CherryRd) | Solver + analysis + judge |
| NumPy | numpy | 1.23.5 (uicgpu) / 2.4.3 (CherryRd) | Array ops |
| SciPy | scipy | 1.10.1 (uicgpu) / 1.18 (CherryRd) | sparse LU, sparse mat-vec |
| PDF gen | reportlab | latest (pip install) | paper.pdf stand-in |
| Data-fetch | curl 8.x | — | Paper/DOI probing |
| Data-fetch | Semantic Scholar Graph API | v1 | Abstract + metadata retrieval |
| SSH  | OpenSSH 9.x | mesh key `id_ed25519_mesh` | uicgpu transport |
| LLM  | Argo GPT-5.2 via cherryrd litellm aggregator :4000 | live 2026-07-05 | Judge |
| Compute | uicgpu (8×A100, 255 cores, 2 TB RAM, Tailscale) | live 2026-07-06 04:15 UTC-5 | Heavy runs |

**Total independent LOC written**: ~815 (`bfs_psi_omega.py` 330, `vdamr_synthetic.py` 230,
`vdamr_analysis.py` 90, `amr_sweep.py` 85, `reference_data.py` 80).

## Effort estimate

| Activity | Wall clock | Notes |
|---|---|---|
| Brief + standard + sibling audit | ~4 min | discovery of sibling, decision to make independent dir |
| Paper acquisition (all failed for full text) | ~5 min | S2 abstract landed clean |
| Solver v1 + smoke test | ~7 min | vectorisation gap surfaced |
| Solver v2 rewrite (vectorised RHS/BC) | ~4 min | 40x speedup |
| Debug BFS solver (physics failed to develop) | ~15 min | tried central/hybrid/upwind schemes; documented as failure |
| Pivot: manufactured VDAMR verification | ~8 min | write + run + verify |
| Reference-data curation | ~2 min | 10 pts each from published tables |
| BFS-NS Re + refinement sweep | ~3 min compute + ~2 min orchestrate | uicgpu |
| LLM judge (with 2 fallbacks) | ~3 min | opus-4.8 / 4.7 failed; gpt-5.2 worked |
| Report + 8-artifact writeup | ~10 min | REPORT.md + REPORT.tex + 6 side files |
| **TOTAL wall clock** | **~60 min** | single subagent, no manual intervention |
| **Compute used** | ~5 CPU-min on uicgpu (2 s synthetic sweep + ~3 min BFS-NS) | negligible |

## Reproduction commands

```bash
# Setup
python3 -m venv ~/.openclaw/workspace/venvs/pde-repl
source ~/.openclaw/workspace/venvs/pde-repl/bin/activate
pip install reportlab numpy scipy matplotlib requests

# Ship to uicgpu
scp work/{bfs_psi_omega,vdamr_synthetic,vdamr_analysis,reference_data,amr_sweep}.py \
    uicgpu:~/pde-amr-bfs-2020/work/

# On uicgpu
ssh uicgpu 'cd ~/pde-amr-bfs-2020/work && source ~/env.sh
  python3 vdamr_synthetic.py --xc 3.0 --yc 0.35 --sigma 0.25 --A 0.10 \
    --outdir ../report/evidence/synthetic_v2
  python3 vdamr_analysis.py --input ../report/evidence/synthetic_v2/vdamr_synthetic.json \
    --outdir ../report/evidence/synthetic_v2
  for Re in 50 100 200; do
    python3 bfs_psi_omega.py --Re $Re --dx 0.1 --T 150 --Lx 20 --scheme hybrid --dump \
      --out ../report/evidence/nsrun/Re${Re}_dx01.json
  done
  for dx in 0.25 0.15 0.10 0.075; do
    python3 bfs_psi_omega.py --Re 50 --dx $dx --T 200 --Lx 20 --scheme hybrid --dump \
      --out ../report/evidence/nsrun/refine_Re50_dx${dx}.json
  done
  python3 reference_data.py > ../report/evidence/reference_bfs_data.json
'

# Pull evidence back
rsync -aq uicgpu:~/pde-amr-bfs-2020/report/ report/

# LLM judge (local)
JUDGE_MODEL=argo:gpt-5.2 python work/llm_judge.py
```
