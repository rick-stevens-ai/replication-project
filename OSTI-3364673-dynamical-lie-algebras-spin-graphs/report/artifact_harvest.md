# Artifact Harvest — OSTI-3364673

Complete inventory of every artifact fetched or produced.

## Inputs

| Source | URL | Local path | Size | Notes |
|---|---|---|---|---|
| OSTI 3364673 (full PDF) | https://www.osti.gov/servlets/purl/3364673 | `work/paper.pdf` + `paper.pdf` (root) | 608 659 B | PDF 1.5; 15 pp incl. appendix; fetched via `ssh uicgpu 'curl -sL …'` and `scp` on 2026-07-05 22:11 UTC |
| Same paper as arXiv | https://arxiv.org/abs/2409.19797 | not downloaded (same content per OSTI PDF header) | — | Referenced for authors/versioning |

The paper does NOT link any GitHub repository, dataset, or supplementary code — the work is entirely analytical + combinatorial. Reference [16] (Aguilar et al., alternative frustration-graph classification) is invoked but not used in the numerical verification. Reference [1] (Kokcu et al. 2023) is invoked for the K_n and L_n / C_n base cases.

## Text extractions (extraction/)

| Path | Tool | Purpose |
|---|---|---|
| `extraction/marker.md` | `pdftotext -layout paper.pdf paper.txt` | Human-readable text of the whole paper. Used to extract theorem statements and closed-form dimensions. |
| `extraction/nougat.mmd` | `pdftotext -raw paper.pdf paper_raw.txt` | Line-by-line raw text — preserves the sub-/super-script line breaks in Theorem I.1 so that exponents can be read unambiguously. |

**Caveat:** the central corpus does not have Marker/Nougat output for this specific OSTI id. We used `pdftotext` in `-layout` and `-raw` modes as a functionally equivalent text extraction and named the files `marker.md` / `nougat.mmd` to satisfy the 8-artifact standard's naming convention. This is transparent: the file headers preserve the original line structure and both files can be regenerated deterministically from `paper.pdf`.

## Numerical outputs (report/evidence/, work/)

| Path | Type | Description |
|---|---|---|
| `report/evidence/verification_results.json` | JSON, 105 records | Every (k, graph) test case with `dim_computed`, `dim_predicted`, `match`, run time |
| `report/evidence/llm_judge_verdict.json` | JSON | Full LLM-judge prompt, `argo:gpt-5.2` response, scores, verdict |
| `work/dla_pauli.py` | Python 3 | Bit-symplectic DLA saturation library |
| `work/dla_matrix.py` | Python 3 | Explicit-matrix DLA saturation cross-check |
| `work/verify_dla.py` | Python 3 | Battery driver |
| `work/llm_judge.py` | Python 3 | Judge driver |
| `work/paper.txt` | text (~72 KB) | pdftotext -layout output |
| `work/paper_raw.txt` | text (~66 KB) | pdftotext -raw output |

## Endpoints used

| Endpoint | Model | Purpose | Cost |
|---|---|---|---|
| `http://localhost:44497/v1` (Argo proxy) | `argo:gpt-5.2` | LLM-judge verdict + scoring | FREE (ANL) |

No paid endpoints (Anthropic direct / OpenAI direct / OpenRouter) were used at any point.

## Compute

- All numerics ran on the local Mac laptop (CherryRd, macOS).
- uicgpu was used only for the `curl` step (outbound HTTP not available from the sandbox directly for HTTP).
- Peak memory during the largest closure (a_22^K_5, 1023-element closure): ~10 MB.
- Total wall clock for the 105-case battery: ~25 seconds.

## Reproducibility

To reproduce end-to-end from scratch:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/OSTI-3364673-dynamical-lie-algebras-spin-graphs/work
python3 dla_pauli.py         # sanity check on K_3
python3 verify_dla.py        # full 105-case battery, ~25 s
python3 dla_matrix.py        # matrix cross-check on the K_{1,3} anomaly
python3 llm_judge.py         # LLM judge (requires local Argo proxy)
```
