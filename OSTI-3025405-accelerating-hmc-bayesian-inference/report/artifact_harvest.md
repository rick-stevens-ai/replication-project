# artifact_harvest.md — OSTI 3025405

Every public artifact pulled during this replication.

| Artifact | URL | Size | Local path | Notes |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3025405 | 16,995,537 bytes (17 MB) | `work/paper.pdf` | Downloaded via `ssh uicgpu` (CherryRd cannot reach osti.gov directly), then `scp` back. |
| Paper text | (extracted locally via PyMuPDF) | 1931 lines | `/tmp/osti_3025405_text.txt` (transient) | Full 35-page text. |
| Reference GitHub | https://github.com/ponkrshnan/VI-HMC.git | (not cloned) | — | Authors' code — **not used**; we did a clean-room re-implementation to make the replication independent. |

## Data
No external datasets required. All synthetic data generated in-process:
- Case I: 20 noisy samples of `y = 0.4 sin(4x + 0) + 0.5 sin(-3x + π/2) + N(0, 1e-3)`
  on `x ∈ [-1,-0.2] ∪ [0.2,1]`, seed=42.
- Case II: 20 noisy samples of `y = 4 sin(4x) + 5 sin(-12x + π/2) + N(0, 0.05)`,
  same x range, seed=42.

## Software
- Python 3.12.12 (from `/usr/local/bin/python3.12`).
- Local venv at `work/venv/`.
- PyTorch 2.2.2, NumPy 1.26.4, requests (only for Argo LLM judge call).
- Compute: local CPU (CherryRd, macOS Darwin 25.3.0).

## LLM scoring endpoint
- Argo proxy: `http://127.0.0.1:44497/v1/chat/completions`, key=`stevens`.
- Model: `argo:gpt-5` (free, per hard rules; `argo:gpt-5-mini` returned
  `DeploymentNotFound` at the time of run).
- Judge prompt + raw response preserved at `report/evidence/llm_judge_prompt.txt`
  and `report/evidence/llm_judge.json`.
