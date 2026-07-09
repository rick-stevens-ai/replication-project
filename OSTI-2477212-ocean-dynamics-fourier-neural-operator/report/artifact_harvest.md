# artifact_harvest.md

Public artifacts pulled during this replication.

| Artifact | URL | Route | Size (bytes) | sha256 |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/2477212 | via `ssh uicgpu` (osti.gov is unreachable from CherryRd home network) | 1,152,941 | a0a602a62f931a22453ddd281f81979a6db4a24b5452f7f694866f848dfc9230 |
| Paper plain text | `pdftotext -layout paper.pdf paper.txt` | local | 109,429 | f124265f8082baa3ad98955f20a8f8850d82b6cbb1b73168b8da22809a66559b |

## Referenced tools / libraries (installed but not pinned to a wheel here)
- `torch` 1.11.0 (already on uicgpu; CUDA 11 available, 8× A100).
- Nvidia Modulus v0.4.0 — **not used** here; we implemented FNO2d from scratch
  (Li et al. 2021, arXiv:2010.08895) in ~120 lines to keep the spot-check
  independent of Modulus's Argonne-tuned defaults.
- DeepHyper — **not run**; the paper's HPO uses 80 A100 GPUs × 6 h at ALCF
  Polaris (out of scope for this session). Instead we hand-picked two
  configurations, "Modulus-default" baseline vs. a HPO-winner-like optimized
  configuration, that let us test the *direction of effect* the paper reports.

## Public datasets / code that would be needed for a full REPLICATED verdict
- The SOMA 100-simulation ensemble with per-sim κ_GM ∈ [200, 2000] is **not
  publicly available**. Data availability statement (paper, page 15):
  "The data presented in this study are available on request from the
  corresponding author. The data are not publicly available due to ongoing
  research and data curation processes."
- No GitHub / Zenodo release of the authors' problem-specific training
  script was located via GitHub API keyword searches on 2026-07-02
  (`deephyper+FNO+ocean`, `SOMA+fourier+neural+operator`,
  `yixuan-sun FNO ocean` all returned zero hits).
- MPAS-Ocean SOMA test case itself IS public
  (https://mpas-dev.github.io/), but the specific 100-member κ_GM ensemble
  is not.

## Replicator-produced artifacts (all under `report/evidence/` and `work/`)

### 2026-07-02 spot-check track (ocean-tracer synthetic ensemble)
- `work/fno2d_spotcheck.py` — standalone FNO2d + synthetic dataset +
  training driver. sha256 `499ea0a7f626cb3157d45838360da0dfa16fb54398261e71e886d2b7c0431d39`.
- `work/llm_judge.py` — LLM judge harness for the ocean-proxy run.
- `report/evidence/results_run2.json` (16,510 bytes) — full numerical
  results for baseline vs optimized on synthetic ocean-tracer ensemble.
- `report/evidence/llm_judge_verdict.txt` (697 bytes) — Argo gpt-5.2
  verdict on ocean-proxy track.

### 2026-07-04 canonical FNO benchmark track (1D viscous Burgers)
- `work/fno1d_burgers_benchmark.py` — standalone FNO1d + pseudo-spectral
  IF-RK4 Burgers solver + resolution-invariance evaluator. sha256
  `cbdee6245c4c87adb368839b1174717bd10d64d816736735f309408434f10f8e`.
- `work/llm_judge_burgers.py` — LLM judge harness for the Burgers run.
  sha256 `8f6fadc36e92894ea969f900076e868358b0f7cf872ec6abe906c5f821086f67`.
- `report/evidence/results_burgers_full.json` (11,797 bytes) — full
  numerical results with per-epoch history and resolution sweep for both
  configs. sha256
  `e22f84ce8bae5c6907654b6921223e82a68ce45c402e4603b756dd2844916178`.
- `report/evidence/burgers_full.log` (4,914 bytes) — uicgpu training log.
- `report/evidence/llm_judge_burgers.txt` (2,057 bytes) — Argo gpt-5.2
  verdict on Burgers benchmark track. sha256
  `f6623b8d5ba311ee03371a39ca40c2f6d86dd08a5b406d2133af766f8ba2f7e3`.
