# Artifact Harvest

## Paper
- **DOI:** 10.1137/070692108
- **Publisher:** SIAM
- **Journal:** SIAM Journal on Scientific Computing, Vol. 30, Issue 6, pp. 2709–2733 (2008)
- **URL:** https://epubs.siam.org/doi/10.1137/070692108 (paywalled)
- **Local copy:** Not archived (paywalled at SIAM). Persson has a preprint
  on his MIT page at https://persson.berkeley.edu/pub/persson08newton-gmres.pdf
  which was consulted for the method description.

## Code artifacts from the paper
- Persson & Peraire do not release the DG solver used in this paper as an
  independent open-source package. Persson's later `3DG`/`nodal-dg` code
  base underpins much of the follow-up work but the specific line-
  preconditioner implementation used in the 2008 paper is not in a public
  release we could pull directly.
- **What we did instead:** built a fresh DG(p=1) solver from scratch on the
  scalar test problem (see `work/dg_precond_study.py`) and implemented all
  three preconditioners independently based on the method description in
  the paper. All numerical values in the report come from this fresh
  reimplementation running on uicgpu.

## Software dependencies used
- Python 3.8 (uicgpu system)
- NumPy 1.23.5
- SciPy 1.10.1 (`scipy.sparse`, `scipy.sparse.linalg.gmres`, `scipy.sparse.linalg.spilu`)

## LLM judge
- Argo proxy endpoint `http://127.0.0.1:44497` (free)
- Requested model: `argo:claude-opus-4.7` (per wave brief)
- Actually used (fallback): `argo:gpt-4o` (backend `gpt-4o-2024-11-20`) —
  both `claude-opus-4.7` and `claude-opus-4.8` returned HTTP 502 across
  multiple retries at wave time on prompts >a few tokens; gpt-4o on the
  same Argo proxy is the free-tier fallback used and its judgement is
  archived in `evidence/judge_verdict.txt`.

## No datasets downloaded
- This replication is method-focused; no external datasets required
  (the DG problem is defined analytically by the manufactured convection–
  diffusion setup).
