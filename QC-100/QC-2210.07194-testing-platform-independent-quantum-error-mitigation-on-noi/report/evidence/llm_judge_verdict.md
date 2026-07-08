# LLM-Judge Verdict — QC-2210.07194

**Judge model:** `argo:gpt-4.1` via Argo proxy (free ANL endpoint at http://localhost:44497)
**Judge date:** 2026-07-04 CDT
**Judge prompt:** see `/Users/stevens/.openclaw/workspace/tmp_pdfs/judge_prompt.txt` (mirrored below in raw JSON at `llm_judge_raw.json`)

## Judge output (verbatim)

> The replication attempted to match the paper's simulator setup as closely as possible, using the same noise model, circuit structure, and ZNE parameters. The key claims about ZNE (C1, C2, C4, C6) were confirmed at shallow circuit depths (d=1), with improvement factors (mu) well within the reported range and clear reduction in RMSE. At higher depths, the improvement factor dropped to ~1, consistent with the paper's assertion that noise saturation limits error mitigation. The largest improvement was observed at the highest tested noise level, supporting C3 within the scope of the tested models. However, the PEC method (C5) did not replicate the reported improvement factors, likely due to sampling variance and under-budgeted shots, but this does not contradict the ZNE claims. The methodological difference in RB circuit compilation (more 2Q gates per layer) may explain the faster noise saturation observed, but does not fundamentally contradict the paper's findings. Overall, the replication supports the main claims about ZNE on simulators, with minor caveats about PEC and circuit compilation.
>
> **VERDICT: PARTIAL**

## Interpretation

Judge accepted the ZNE replication (5/6 claims cleanly supported at the tested regime) but flagged PEC (C5) as not reproduced under our first-pass configuration and no-hardware coverage as a limitation. Verdict PARTIAL is appropriate: the paper's *headline* claim (ZNE improves noisy simulator expectation values, up to 7×) is honestly reproduced; a secondary claim (PEC also helps) is not reproduced here without further tuning.
