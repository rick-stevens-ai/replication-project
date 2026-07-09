# Artifact Harvest — OSTI 3007459

| Artifact | Source | Notes |
|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3007459 | 523,213 bytes, PDF v1.5. Direct fetch from CherryRd times out; pulled via `ssh uicgpu` proxy (HTTP_PROXY=<lan-host>:3128). Also on arXiv:2506.02171. → `work/paper.pdf` |
| Paper text | `pdftotext -layout` of the above | `work/paper.txt` (48,884 bytes) |
| Paper code/data | — | **None found.** No GitHub/Zenodo/code artifact linked from OSTI or the paper. This is a method-only paper (no released implementation). Replication is therefore a full reimplementation from the equations. |

## External references used for validation (not code, analytic results)
- Exact ground-state energy of the solvable model (paper Eq. 7): implemented directly.
- Busch et al. (1998) analytic two-boson-in-a-1D-harmonic-trap contact-interaction
  energy: reimplemented via the transcendental Gamma-function relation and solved with
  `scipy.optimize.brentq`. Reproduces the known monotonic curve E(g): 1.0 (g=0) →
  ~2.0 (Tonks-Girardeau, g→∞).
- Tonks-Girardeau limit E = N²/2 for N bosons in a harmonic trap: standard result.

## Compute
- All VMC runs on **uicgpu** (NVIDIA A100, CUDA), PyTorch 1.11.0, float64.
- LLM judge: free **Argo gpt-5.2** via localhost:44497 proxy (key `stevens`).
- No paid endpoints used. No paid `pdf` tool used (pdftotext only).
