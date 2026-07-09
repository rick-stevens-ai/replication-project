# PROVENANCE

## Paper
- **Title:** *Self-adaptive weights based on balanced residual decay rate for physics-informed neural networks and deep operator networks*
- **Authors:** Wenqian Chen, Amanda A. Howard, Panos Stinis (Pacific Northwest National Laboratory)
- **OSTI:** 2588651 — https://www.osti.gov/biblio/2588651
- **arXiv mirror used:** 2407.01613 v1 (June 2024) — https://arxiv.org/abs/2407.01613
- **Published venue:** *Journal of Computational Physics* (2025), doi: 10.1016/j.jcp.2025.114202

## PDF acquisition
- **OSTI purl** `https://www.osti.gov/servlets/purl/2588651` — **UNREACHABLE** during this replication window (curl timed out twice, including with 30 s max-time and browser User-Agent). Substituted the arXiv version, which the authors' own biblio references as the same paper.
- **Downloaded from:** `https://arxiv.org/pdf/2407.01613` (2026-07-05 14:34 UTC)
- **SHA-256:** `d25f757c6673435eed7ccb7b9ec321d8d7c11c50e1ba3cf0c8959be3c21455a1`
- **Bytes:** 3,617,451
- Local: `./paper.pdf` (kept), `./paper.txt` (pdftotext -layout extract, kept for grep).

## Substitution note
This replication uses the arXiv preprint (v1) as a stand-in for the OSTI record because the OSTI PDF endpoint returned no bytes during the run. The arXiv preprint by the same authors and same title is standard practice for OSTI-mirrored PNNL work and is what the OSTI record links back to. All method equations, hyperparameters, and benchmark tables cited in this replication trace to Sections 3–4 of the arXiv PDF above.

## Reproducer environment
- Host: `CherryRd` (macOS Darwin 25.3.0, x64), CPU-only (no CUDA).
- Python: `/Users/stevens/opt/anaconda3/envs/hf/bin/python`  (Python 3.x, torch 2.2.2, numpy 1.24.3).
- Torch threads: capped at `min(8, os.cpu_count())`.
- Free-tooling policy: only stdlib + `torch` + `numpy` used. No Argo/paid model in the training loop; the LLM (Argo Opus 4.7) was used only for planning, drafting, and interpretation.
