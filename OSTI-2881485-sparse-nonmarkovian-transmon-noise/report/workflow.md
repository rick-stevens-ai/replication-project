# Workflow — OSTI 2881485

## Narrative
1. **Comprehension pass.** Downloaded the paper PDF (OSTI purl) and parsed with `pdftotext -layout` because the OpenClaw `pdf` tool was blocked from `/tmp` and `~/Dropbox`, and Anthropic direct API was credit-exhausted. Identified the paper's reproducible core as Sec IV B, "VQE for H₂ molecule" (Fig 9), and located a Zenodo pointer at ref [146].
2. **Artifact pull.** Confirmed Zenodo record 19695739 (concept DOI 10.5281/zenodo.19612185) is public + open (CC-BY-4.0). Downloaded the 8.4 MB v0.0.2 release ZIP on uicgpu and unpacked. Repository contains one Jupyter notebook per paper figure + all pickled data.
3. **Direct claim verification.** For the headline claim (Fig 9), the pickled arrays `VQE_exp.p`, `VQE_sim_IBM.p`, `VQE_sim_NM.p`, plus `VQE_H2_theta_opt.p` are the numerical objects that appear on the figure. Wrote a ~150-line Python script (`work/verify_claim.py`) to load them, compute relative errors per paper Eq. (26), and report the R_opt=0.75 Å number + whole-curve statistics.
4. **Fresh IBM baseline rerun.** Because the paper's stated 3.6 % IBM baseline differs from the pickled 2.89 %, wrote a second script (`work/rerun_ibm_sim_v2.py`) that runs the IBM-noise-model simulation from scratch on our own machine: build the O'Malley ansatz, pull `FakeHanoiV2` from `qiskit_ibm_runtime.fake_provider`, extract its `NoiseModel`, feed to `AerSimulator.from_backend`, sample 100 000 shots per basis, seed fixed to 20260705. This confirms the IBM baseline drift is not an artifact of a stale pickle.
5. **LLM-judge.** Fed the paper claim + our numbers + methodology summary to `argo:gpt-5.4` via the cherryrd LiteLLM aggregator (`http://<tailnet-aggregator>:4000/v1`), requesting a structured verdict JSON. (First choice `argo:claude-opus-4.8` was returning HTTP 502; picked GPT-5.4 as a live free alternative.)
6. **Text-extraction backfill.** Ran Marker and Nougat on the paper PDF on uicgpu (in parallel on GPUs 0 and 6) to satisfy the REPLICATION_DIR_STANDARD_2026-07-05.md items 2 and 3.
7. **Report authoring.** Wrote the 8 required artifacts (REPORT.md, REPORT.tex, brief.md, attempt_log.md, artifact_harvest.md, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json).

## Tools & codes used
| Tool | Version | Purpose |
|------|---------|---------|
| curl | 8.x (uicgpu) | Fetch PDF and Zenodo release |
| pdftotext | poppler 22.02.0 | Text extraction for LLM comprehension |
| Python | 3.10 (conda env `/data/stevens/envs/qexpr` on uicgpu) | Replication scripts |
| Qiskit | 2.5.0 | Circuit construction, transpilation |
| Qiskit-Aer | 0.17.2 | Noise-model density-matrix simulation |
| qiskit-ibm-runtime | 0.47.0 | `FakeHanoiV2` backend (Qiskit 2.x replacement for v1 `FakeHanoi`) |
| NumPy / SciPy / pickle | stdlib / conda defaults | Data loading + analysis |
| Marker (marker-pdf) | conda env `/data/stevens/envs/marker` | Markdown extraction from PDF |
| Nougat | 0.1.17, `/gpustor/stevens/anaconda3/envs/nougat` | Math-aware markdown (.mmd) extraction |
| LiteLLM aggregator | cherryrd :4000 | LLM-judge routing (free Argo) |
| argo:gpt-5.4 | Argo proxy on cherryrd :44497 (fronted via aggregator) | LLM judgment (Opus 4.8 was 502) |
| ssh + scp (Tailscale mesh) | openssh 9.x | Move code + data between cherryrd, uicgpu |

## Custom scripts
- `work/verify_claim.py` (~140 lines) — loads released pickles, computes rel_err per R, prints table, writes `verify_summary.json`.
- `work/rerun_ibm_sim_v2.py` (~110 lines) — independent AerSimulator IBM-noise-model rerun with `FakeHanoiV2`.
- `work/llm_judge.py` (~70 lines) — POSTs replication summary to Argo aggregator and parses JSON verdict.

## Effort estimate
- **Wall-clock (human-facing):** ~15 minutes (subagent turn window).
- **Compute wall-clock:**
  - PDF text extraction: ~1 s (pdftotext).
  - Direct pickle-based claim verify: <1 s (54 R-point loop, all vectorized).
  - Fresh IBM-baseline AerSimulator rerun: **57.9 s** on uicgpu qexpr env (single-thread, no GPU).
  - Marker extraction (uicgpu, single A100): **166 s**.
  - Nougat extraction (uicgpu, single A100, batchsize 1): ~2-3 min after switching from OOM'd GPU 1 to free GPU 6.
  - LLM-judge single call: ~5 s to Argo GPT-5.4.
- **Lines of code written by the replication:** ~320 LOC (verify_claim.py + rerun_ibm_sim_v2.py + llm_judge.py + dump_nb.py helper).
- **Data volume pulled:** 4.0 MB PDF + 8.4 MB Zenodo release = 12.4 MB.
- **Runs executed:** 1 pdftotext, 1 curl (PDF), 1 curl (Zenodo), 1 unzip, 1 verify_claim run, 1 IBM-model rerun (162 circuits), 2 LLM-judge calls (Opus 4.8 retry then GPT-5.4), 1 marker run, 1 nougat run (retry after OOM).

## What we did NOT run
- Full non-Markovian SchWARMA MC regeneration — requires JHU APL `mezze` package (not on PyPI or public GitHub).
- Any of the LME/qutip-heavy fig 2/3/5/6/7 notebook reruns — out of scope for a single-paper subagent turn; released pickles were used as the source of truth for those figures, and the LLM-judge coverage was scoped to the Fig-9 headline claim only.
- Any live IBM Quantum hardware run — the paper's `VQE_exp.p` provides the same hardware measurements (ibm_algiers Q12/Q15, 100k shots), and ibm_algiers is now retired anyway.
