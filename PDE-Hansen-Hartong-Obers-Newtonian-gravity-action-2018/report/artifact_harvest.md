# Artifact harvest — Hansen-Hartong-Obers 2018

## Primary source

| kind | source URL | local path | size | checksum |
|---|---|---|---|---|
| preprint PDF | https://arxiv.org/pdf/1807.04765v2 | `work/paper.pdf` | 163,032 B | md5 `15ce60ac1e1db7a0889275cb6b9a5220` |
| journal version (public DOI) | https://doi.org/10.1103/PhysRevLett.122.061106 | (not fetched — arXiv v2 is the identical published version per authors' NBI page) | — | — |

The paper is a 6-page PRL Letter with 32 references. No supplementary material file, no data,
no code repository.  All content is symbolic mathematics; every equation needed for the
replication is on the 6 pages of the preprint.

## Derived / generated artefacts

| path | description | provenance |
|---|---|---|
| `work/paper.pdf` | primary preprint | pulled fresh from arXiv on 2026-07-04 via `curl -sSL` on uicgpu |
| `work/verify_algebra.py` | SymPy script: builds eq. (11) structure constants, runs full Jacobi scan | written by replicator |
| `work/verify_poisson_reduction.py` | SymPy script: flat NC → Γ̄ → Ricci → Poisson eq. | written by replicator |
| `work/verify_metric_compat.py` | SymPy script: generic TTNC background → ∇̄τ=0, ∇̄h=0, torsion check | written by replicator |
| `report/evidence/algebra_output.txt` | raw stdout of `verify_algebra.py` (d=2,3,4) | produced on uicgpu |
| `report/evidence/poisson_output.txt` | raw stdout of `verify_poisson_reduction.py` | produced on uicgpu |
| `report/evidence/metric_compat_output.txt` | raw stdout of `verify_metric_compat.py` | produced on uicgpu |
| `report/evidence/judge_prompt.txt` | prompt sent to both LLM judges | assembled from script outputs |
| `report/evidence/judge_response_gpt5.json` | full JSON reply from `argo:gpt-5` | Argo proxy, free endpoint |
| `report/evidence/judge_response_argo_claude-opus-46.json` | full JSON reply from `argo:claude-opus-4.6` | Argo proxy, free endpoint |

## Compute environment

- Heavy compute: `uicgpu` (8×A100), Python 3, SymPy 1.13.3.  All scripts finish in < 60 seconds.
- LLM inference: local Argo proxy at `http://127.0.0.1:44497/v1` (`ARGO_API_KEY=stevens`), models
  `argo:gpt-5` and `argo:claude-opus-4.6`.  Both are free endpoints per standing policy.
- PDF text extraction: `pdftotext -layout` (poppler-utils) on uicgpu.

## No paid endpoints used
Bandit check of tool calls: no anthropic.direct, openai.direct, or openrouter.direct calls.
Argo proxy is FREE.  The Anthropic-based `pdf` tool was ATTEMPTED but ERROR-blocked by the
"credit balance too low" upstream error — verified to have made no successful chargeable call.
