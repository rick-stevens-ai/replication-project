# Artifact Harvest — OSTI-3366147

## Public artifacts pulled

| URL | Local | Bytes | Notes |
|---|---|---|---|
| https://www.osti.gov/servlets/purl/3366147 | work/paper.pdf | 25,265,785 | PDF 1.7; pulled via uicgpu proxy (osti.gov unreachable from CherryRd), scp'd back |
| (derived) | work/paper.txt | ~200 KB | `pdftotext -layout paper.pdf`; used to extract HFS eqs, spectral-error definition, tables 1/2/C.1/D.1 |

## Referenced but not downloaded (out of scope this wave)
- **BubbleML** boiling dataset (Hassan et al. 2023) — cited as ground-truth source; tens of GB; not needed to test the CORE HFS mechanism.
- **Kolmogorov flow** dataset used in the paper's turbulence experiments.
- **Flash-X** simulator (Dubey et al. 2022) — data generator, not required.
- Paper does not provide an official code repo URL in the extracted text; if one exists on GitHub it was not necessary for this replication (independent PyTorch re-implementation from Eqs. 4-6 and B.3).

## Derived / created

| Path | Purpose |
|---|---|
| work/replicate_hfs.py | Independent PyTorch impl: ResUNet + HFS module (paper Eqs. 4-6) + spectral error (Eq. B.3) + trainer |
| work/llm_judge.py | Free-endpoint (Argo proxy :44497) LLM-judge caller |
| work/judge_prompt.txt | Judge prompt with numeric results |
| report/evidence/run_seed0/{results.json, run.log, spectra.png} | Seed 0 outputs (uicgpu, GPU 2) |
| report/evidence/run_seed1/{results.json, run.log, spectra.png} | Seed 1 outputs (uicgpu, GPU 3) |
| report/evidence/run_seed2/{results.json, run.log, spectra.png} | Seed 2 outputs (uicgpu, GPU 4) |
| report/evidence/run_seed{1,2}.log | Stdout logs of the parallel seed runs |
| report/evidence/llm_judge_output.txt | LLM judge scoring output |

## Compute
- Model training: uicgpu, PyTorch 1.11, CUDA on 3 free A100 80GB (GPUs 2, 3, 4), ~90 s each.
- LLM scoring: Argo proxy 127.0.0.1:44497, model `argo:claude-sonnet-4.6` (opus-4.7 returned 502 on this call).
- Egress: paper download via uicgpu (source `~/env.sh` for proxy) then `scp` to workspace.
