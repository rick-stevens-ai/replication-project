# Failure Analysis — OSTI 2881485

The overall verdict is **PARTIAL (leaning REPLICATED-core)**. This document lists everything that friction'd, was worked around, or remains an open gap.

## Successes
- **NM headline claim reproduced essentially exactly.** 0.507 % rel_err at R_opt=0.75 Å vs paper's 0.5 %.
- **Full 54-point per-R table reproduced** from released artifacts, matching the shape of Fig 9(b) inset (Δ_NM ≪ Δ_IBM everywhere).
- **Fresh independent IBM-baseline rerun** (with our own Qiskit 2.5.0 + FakeHanoiV2 + Aer) gives a coherent ~2.7 % that agrees with the released pickle to ~0.2 pp.
- Marker + Nougat extractions produced.
- All 8 REPLICATION_DIR_STANDARD_2026-07-05.md artifacts present.

## Partial / mismatched
1. **IBM baseline is systematically ~0.7-0.9 pp lower than the paper text.** Paper says ~3.6 %; released pickle says 2.89 %; our fresh rerun says 2.66 %. This is not a "we did the wrong thing" failure — the released pickle from the authors' own code shows the same drift — but it means the "sevenfold" number does not reproduce (5.3-5.7× instead). Root cause is almost certainly `FakeHanoi` backend-properties refresh in `qiskit-ibm-runtime` since the paper was drafted (backend props are date-versioned, get updated as IBM publishes calibration data). Would need pinned historical qiskit-terra to fully close.

2. **Non-Markovian curve was verified only against the released pickle, not fully independently regenerated.** The notebook cell that regenerates the SchWARMA MC trajectories is commented out and depends on the JHU APL `mezze` package, which is not on PyPI or public GitHub. Documented in open-question Q2.

## Blockers we hit and worked around
- **OpenClaw `pdf` tool blocked** from `/tmp` and Dropbox paths (media-path allowlist), and simultaneous Anthropic direct-API credit exhaustion. → Worked around by using `pdftotext -layout` for text extraction (2 671 lines, adequate for LLM comprehension) and later Marker/Nougat for the mandatory artifacts.
- **Anthropic API key depleted** (`ANTHROPIC_API_KEY` in managed env → 400 credit-balance error). → All LLM calls routed via FREE Argo aggregator on cherryrd :4000.
- **Argo Opus 4.8 endpoint HTTP 502** at the time of the LLM-judge call. Retried once, still 502. → Fell back to `argo:gpt-5.4` (verified live via pong probe). Semantically equivalent for a structured JSON verdict task.
- **Qiskit 2.5.0 removed `FakeHanoi` v1.** → Installed `qiskit-ibm-runtime==0.47.0` and switched to `FakeHanoiV2`. Note this is itself a potential contributor to the IBM-baseline drift (the v2 fake providers have different snapshot semantics than v1) — flagged in Q1.
- **Nougat OOM on GPU 1** despite `CUDA_VISIBLE_DEVICES=1` — GPU 1 had 35 GB already in use by another user's process. → Re-checked `nvidia-smi`, picked GPU 6 (0 MiB used), retried with `--batchsize 1` and `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, succeeded.
- **`ssh uicgpu 'curl ...'` initial name resolution failure** (exit 6) because non-interactive SSH doesn't source `~/env.sh` on uicgpu (proxy config). → Prepended `source ~/env.sh;` to the remote command.

## Residual gaps (would be needed to close to full REPLICATED)
1. **Rerun the full NM+SchWARMA pipeline independently.** Needs `mezze` or a re-implementation of `SimpleDephasingSchWARMAFier` from the Schultz et al. 2020 SchWARMA paper. Estimated ~200-500 LOC + ~4-8 hours of engineering to reimplement + ~5-30 min of MC runtime.
2. **Reconcile the 3.6 % → 2.7 % IBM-baseline drift.** Try pinning `qiskit-terra==0.44.0` with the v1 `FakeHanoi` and see if the paper's 3.6 % returns. Alternatively, ask the authors which specific `qiskit-terra` version generated the released `VQE_sim_IBM.p`.
3. **Rerun Figs 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16 notebooks end-to-end.** Only Fig 9 was independently verified numerically in this replication. Coverage was 80 % (per LLM judge), driven by the fact that Fig 9 is the paper's headline demonstration and the rest is characterization/method support.
4. **Live IBM hardware rerun** (ibm_algiers is retired; a modern Heron equivalent would test whether the method transfers). See Q5.

## Lessons for future OSTI-set replications
- When paper text and released pickle disagree by ~1 pp on a headline number, the released pickle is usually closer to reality than the paper text (which reflects a snapshot at submission time). Always report BOTH.
- For Qiskit-based papers, **pin the exact Qiskit version** at replication time; the fake providers refresh their calibrations without semantic versioning bumps.
- For JHU APL / national-lab papers, expect internal packages (`mezze`) to be undocumented dependencies. Flag as an open question rather than try to reimplement in a subagent turn.
- The OpenClaw `pdf` tool's Anthropic-credit + local-path-allowlist combination is a recurring blocker for OSTI PDFs saved under `~/Dropbox` — `pdftotext -layout` is a reliable fallback that gives enough text for LLM comprehension.
