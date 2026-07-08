# Workflow, Tools, and Effort Estimate

## Workflow narrative

1. **Ingest brief and standard.** Read `scripts/WAVE_BRIEF_2026-07-01.md` and `scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`. Confirmed 8-artifact bar, free-endpoint-only rule, real-data-only rule, no-overwrite rule.
2. **Create target dir.** `~/Dropbox/REPLICATE-PROJECT/QC-different-kind-quantum-search-grover-2005/` with `extraction/`, `report/evidence/`, `work/` subdirs. Confirmed a sibling dir `QC-200/QC-quant-ph-0503205-...` already existed; treated it as read-only source for the central-corpus text extractions and did not touch it.
3. **Fetch paper.** `curl` the arXiv PDF → 138 kB.
4. **Text extraction.** Copied `marker.md` + `nougat.mmd` from the central QC-200 corpus (already parsed 2026-07-05); this satisfies artifacts (2) and (3) per the standard's rule "copy from central manifest if already parsed."
5. **Understand the paper.** Read the marker.md through §5 to nail down the exact algorithm (Eq. 3 recursion, R_s/R_t = π/3 phase shifts on source/target, base identity `1 − ε³`, recursion identity `1 − ε^(3^m)`).
6. **Set up venv.** `python3 -m venv work/.venv`; `pip install numpy matplotlib`. No Qiskit needed — the paper's identity is exact in linear algebra and dimension-independent, so pure numpy statevector is not only sufficient but *preferred* (no simulator randomness or shot noise to confound the check).
7. **Implement.** `work/pi3_search.py` (240 LOC): built `W`, `R_x(π/3)`, `R_x(π)`; implemented standard Grover iterate `G = W I_0 W I_t`; implemented the paper's exact recursion `U_{m+1} = U_m R_s U_m† R_t U_m`; ran for `N=16`, target index 5, `m = 0..4` and `k = 0..12`; compared measured to theoretical `1 − ε^(3^m)`; produced 2 figures.
8. **Run and verify.** All 5 recursion levels match theory to 1e-14; monotonicity check `True`; standard Grover shows expected oscillation.
9. **LLM-judge.** `work/llm_judge.py` (130 LOC): POST full evidence to Argo `argo:gpt-4o` (first tried `argo:claude-opus-4.7` — got HTTP 502 from the Argo proxy — switched to `argo:gpt-4o` which worked). Model returned strict JSON: verdict REPLICATED, coverage 1.0, agreement 1.0.
10. **Write the 8 artifacts.** REPORT.md, REPORT.tex, open_questions.json (5 heavy-duty Q's each with basis + next_steps), workflow.md (this file), artifacts_summary.md, failure_analysis.md, plus brief.md, attempt_log.md, artifact_harvest.md.
11. **Print WAVE_RESULT.**

## Tools and versions

| Tool | Version | Where | Purpose |
|------|---------|-------|---------|
| Python | 3.13 (system) | CherryRd macOS | Runtime |
| numpy | 2.5.1 | work/.venv | Statevector linear algebra |
| matplotlib | 3.11.0 | work/.venv | Figures |
| curl | 8.x (macOS) | shell | Fetch arXiv PDF |
| Argo proxy | localhost:44497 | free endpoint | LLM-judge |
| argo:gpt-4o | 2024-11-20 | Argo | JSON verdict scoring |
| Marker | (central corpus, 2026-07-05) | — | Text extraction |
| Nougat | (central corpus, 2026-07-05) | — | Text extraction |
| bash / zsh | macOS 25.3 | CherryRd | Orchestration |

Note: the marker.md file for this paper is actually a `pdftotext`-based fallback per its own header ("marker_single not available on this host, 2026-07-05"). Nougat produced a real `.mmd` (`nougat.mmd`, 31 kB). Both were used as source of truth for reading the paper — the algorithm/derivation sections are unambiguously extracted in both.

## Codes/scripts produced

- `work/pi3_search.py` — main replication driver (240 LOC).
- `work/llm_judge.py` — LLM-judge scoring via Argo (130 LOC).

Total: ~370 lines of new code; no code re-used from the existing QC-200 sibling dir (that dir's `work/` was not opened).

## Effort estimate

| Item | Estimate |
|------|----------|
| Wall-clock elapsed (agent) | ~15 minutes |
| Actual compute time | < 5 seconds total (statevector 16-dim is instant, LLM call ~4 s) |
| Human/agent turn budget | 1 subagent turn (this task) |
| LOC written | ~370 |
| LLM calls | 1 (Argo argo:gpt-4o) after 1 aborted call to argo:claude-opus-4.7 (HTTP 502) |
| Data downloaded | 138 kB (paper.pdf) |
| GPU / HPC time | 0 (uicgpu not used; problem trivially fits laptop) |
| Figures generated | 2 (both real, from measured data — no fabrication) |
