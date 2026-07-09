# Attempt Log — OSTI 2881485

Timestamps CDT.

## 2026-07-05 22:08 — Kick-off (subagent OSTI-2881485)
- Read wave brief and REPLICATION_DIR_STANDARD_2026-07-05.md.
- Created target dir `OSTI-2881485-sparse-nonmarkovian-transmon-noise/{work,report/evidence,extraction}`.

## 22:10 — PDF fetch
- `ssh uicgpu` initial `curl -sL https://www.osti.gov/servlets/purl/2881485` returned exit 6 (name resolution) because a bare `ssh uicgpu 'curl ...'` shell does not source `~/env.sh` (proxy needed on uicgpu).
- Retry with `source ~/env.sh; curl -sL -w '%{http_code}' ...` → HTTP 200, 4 027 724 B, valid PDF.
- `scp uicgpu:/tmp/osti_2881485.pdf` → `work/paper.pdf` (+ symlink at `paper.pdf`).

## 22:12 — PDF characterization (pdftotext)
- OpenClaw `pdf` tool blocked (path not under allowed dir; Anthropic credit exhausted). Fell back to `pdftotext -layout`.
- Extracted 2 671 lines, identified: PRX Quantum 7, 020327 (2026), Oda/Schultz/Norris/Shehab/Quiroz (JHU + JHU APL + IBM).
- Located the reproducible core in Sec IV B "VQE for H₂ molecule" (Fig 9): 2-qubit VQE on ibm_algiers Q12/Q15, Bravyi–Kitaev-mapped H₂ Hamiltonian, single θ-parameter ansatz, 5 single-qubit + 2 CNOT gates.
- Found Zenodo pointer at ref [146]: DOI 10.5281/zenodo.19612185.

## 22:13 — Zenodo code+data download
- Public record 19695739 (v0.0.2) — GitHub y-oda2/ibmq-noise-modeling; MIT-CC-BY-4.0. Downloaded `y-oda2-ibmq-noise-modeling-v0.0.2.zip` (8.4 MB) on uicgpu.
- Unpacked: 17 Jupyter notebooks (one per figure), `imports_IBM_NM.py` (60 KB support), `data/*.p` pickles (all published simulation and experimental artifacts).
- Verified the exact Fig 9 notebook `notebooks/fig_09_vqe_H2.ipynb` contains all cells to (i) load g-coefficients, (ii) build the O'Malley et al. 2016 ansatz, (iii) noiseless optimize θ, (iv) IBM-noise-model sim via FakeHanoi + Aer, (v) load pre-computed non-Markovian sim (needs `mezze` package for full rerun).

## 22:15 — Direct claim verification (`verify_claim.py`)
- Loaded pickled `VQE_exp.p`, `VQE_sim_IBM.p`, `VQE_sim_NM.p`, `VQE_H2_theta_opt.p`, `g_values.csv`.
- Computed relative error (paper Eq. 26) per-R.
- **Result at R_opt=0.750 Å (index 11): NM = 0.507 %, IBM = 2.887 %, fold = 5.69×.**
- Mean-|Δ| across 54 R: IBM 4.24 %, NM 0.70 %; medians 2.51 % vs 0.39 %.
- Wrote `report/evidence/verify_summary.json` (per-R energies + errors + summary).

## 22:16 — Fresh IBM baseline rerun (`rerun_ibm_sim_v2.py`)
- Reason: paper text says IBM baseline ≈ 3.6 %, but released pickle gives 2.89 %. Rerun to see whether the released pickle is stale, or whether the discrepancy is intrinsic (FakeHanoi backend properties date-versioning drift).
- Env: `/data/stevens/envs/qexpr` (Qiskit 2.5.0, Aer 0.17.2). Installed `qiskit-ibm-runtime==0.47.0` to get `FakeHanoiV2` (Qiskit 2.x deprecated the v1 `FakeHanoi`).
- Ran 54 R points × 3 bases (162 circuits) via AerSimulator (density_matrix), 100 000 shots, `seed_simulator=seed_transpiler=20260705`.
- Wall time: 57.9 s.
- **Rerun IBM baseline at R_opt=0.75 Å: 2.66 % → fold = 5.25× (using released NM as reference).**
- Confirms the discrepancy with the paper text is stable and independent of released-pickle staleness.

## 22:17 — LLM judge (Argo aggregator, cherryrd :4000)
- First attempt `argo:claude-opus-4.8` → HTTP 502 (Opus 4.8 backend hiccup). Retried immediately, still 502.
- Fell back to `argo:gpt-5.4` (verified live via pong probe). Judge returned:
  - verdict: PARTIAL, confidence: high
  - core_claim_reproduced: true, baseline_claim_reproduced: false, fold_claim_reproduced: false
  - coverage 80 %, agreement 86 %
  - one_line: "Headline NM accuracy replicates, but IBM baseline is lower than stated, so the ~7x improvement claim is not reproduced."
- Saved to `report/evidence/llm_judge.txt`.

## 22:17 — Marker + Nougat extractions launched in parallel on uicgpu
- Marker: `/data/stevens/envs/marker` conda env, CUDA_VISIBLE_DEVICES=0, on `paper.pdf`.
- Nougat: initial run on CUDA_VISIBLE_DEVICES=1 OOM'd (35 GB already in use by another process); retried on GPU 6 (free) with `--batchsize 1` and `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.

## 22:20 — Extractions completed
- Marker: full markdown produced (see extraction/marker.md).
- Nougat: full mmd produced (see extraction/nougat.mmd).

## 22:22 — Report artifacts written
- `report/REPORT.md` (traditional replication report)
- `report/REPORT.tex` (detailed LaTeX per REPLICATION_DIR_STANDARD_2026-07-05.md item 4)
- `report/open_questions.json` (5 heavy questions with `next_steps`)
- `report/workflow.md` (item 6), `report/artifacts_summary.md` (item 7), `report/failure_analysis.md` (item 8)
- `report/artifact_harvest.md` (public artifacts inventory)

## Notes / friction
- OpenClaw `pdf` tool locked out of `/tmp` and Dropbox paths — used `pdftotext` fallback.
- Anthropic direct API credit exhausted; Argo Opus 4.8 502'd; used GPT-5.4 via Argo aggregator (free) for judge.
- SchWARMA / mezze package rerun (needed to fully independently reproduce the NM curve, not just verify against released artifact) was NOT executed — `mezze` is an internal JHU APL package with no public PyPI wheel; would require reaching out to the authors. Documented as an open question.
