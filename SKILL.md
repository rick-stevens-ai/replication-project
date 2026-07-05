# Paper Replication Skill

A practical operating procedure for the AI-assisted paper replication project in this repository.

## Purpose

Replicate computational science papers independently, transparently, and at enough depth that the result says something useful about reproducibility. The goal is not to make a demo that resembles the paper; the goal is to test whether the paper's methods, assumptions, data, and claims can be reconstructed and stress-tested by a competent outside team.

## Definition of a Good Replication

A replication is considered useful when it:

- Identifies the paper's central claims and quantitative targets.
- Reconstructs the method from the paper, supplements, equations, and public artifacts.
- Runs executable code or workflows that generate comparable outputs.
- Compares against the paper with units, tolerances, and caveats.
- Documents what was faithful, what was approximated, and what was impossible.
- Produces a durable report that another person can audit.

A partial replication is acceptable if it is honest. Do not inflate fidelity by hiding shortcuts, synthetic substitutes, reduced problem sizes, missing data, or skipped physics.

## Repository Layout

Each paper should live in its own directory, typically named:

```text
<identifier>-<short-title>/
```

Common contents:

```text
README.md                  # short status, paper metadata, how to run
REPORT.md                  # final replication analysis
<paper-id>.pdf             # source paper, when allowed
replication_plan.tex/pdf   # plan, if generated
replication/               # code, scripts, notebooks, configs
report/                    # figures, tables, report assets
results/ or data/          # generated outputs or small input data
```

Keep heavyweight generated data out of Git unless it is small and essential. For large artifacts, record the external location and checksums in the README/report.

## ⚠️ MANDATORY 8-Artifact Completion Standard (Rick, 2026-07-05)

Every paper-replication working directory MUST contain ALL 8 of these before it is "done." Hard
completion bar for EVERY set (QC-100, QC-200, LUCID, PDE, BVBRC, OSTI, all future sets). Canonical
spec: `scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`. Audit: `scripts/check_repl_dir_standard.py`.
Backfill of existing dirs: `scripts/BACKFILL_BRIEF_2026-07-05.md` + the backfill cron driver.

1. **Original PDF** — `paper.pdf`.
2. **Marker text extraction** — `extraction/marker.md` (pull from central Eagle corpus if parsed; else run Marker / pdftotext fallback, labeled as fallback).
3. **Nougat text extraction** — `extraction/nougat.mmd` (pull from central corpus if parsed; Nougat is GPU-only — if unavailable leave a stub noting sha256/DOI for a later corpus sweep; do not block the replication on it).
4. **Detailed LaTeX replication report** — `report/REPORT.tex` (→ `REPORT.pdf` when latex available). Section-by-section: summary; claims table; numbered method (tools+versions+commands); results-vs-paper tables; **per-claim what-worked / what-didn't**; **a genuine CRITIQUE of the replication** (evidence strength, shortcuts, unverified claims); verdict + justification; Open Questions.
5. **Five open questions (heavy-duty, important, NOT superficial), each with next steps** — `report/open_questions.json` = 5 × `{"q":..., "basis":..., "next_steps":...}` + `## Open Questions` (Q1..Q5) in the report. **RE-READ the paper when writing these** — they are used later to open NEW work, so they must be genuinely open, important problems grounded in what the paper leaves unresolved AND what the replication surfaced. Rolled up into `OPEN_QUESTIONS_CORPUS.jsonl` via `scripts/harvest_open_questions.py`.
6. **Comprehensive workflow + tools/codes + effort estimate** — `report/workflow.md`.
7. **Artifacts summary + traces** — `report/artifacts_summary.md`.
8. **Failure analysis** — `report/failure_analysis.md` (required even for clean REPLICATED verdicts).

Items 4-8 for existing dirs are generated from the existing report + evidence + a fresh paper re-read
(do NOT re-run the sim unless there is no report at all). New replications must produce all 8 before
printing the `WAVE_RESULT` line. The Standard Workflow below is HOW you replicate; the 8 artifacts are
WHAT the finished directory must contain (they extend the older Report Writing / Repository Layout sections).

## Standard Workflow

### 1. Intake and Triage

For each candidate paper:

1. Capture bibliographic metadata: title, authors, DOI/OSTI/arXiv, year, domain.
2. Classify the replication type:
   - direct numerical/simulation reproduction
   - algorithm reimplementation
   - ML model/training replication
   - data-analysis reproduction
   - surrogate or reduced-scale reproduction
3. Identify blockers early:
   - closed data
   - proprietary code
   - unavailable experimental inputs
   - compute beyond feasible budget
   - unclear equations or missing parameters
4. Decide expected status before spending heavy compute:
   - `COMPLETE` if key claims are realistically testable
   - `PARTIAL` if only reduced/surrogate tests are feasible
   - `SPOT-CHECK` if only limited quantitative checks are possible
   - `NO-GO` if insufficient information exists

### 2. Claim and Target Extraction

Read the paper and extract a target list before coding.

Minimum target list:

- Main figures/tables to reproduce.
- Headline numerical values and reported uncertainties.
- Claimed scaling laws, ordering relationships, model rankings, or qualitative regimes.
- Required input data, initial conditions, parameters, seeds, meshes, basis sets, or hyperparameters.
- Software stack and version-sensitive dependencies.

Write this into `README.md`, `replication_plan.*`, or a planning note before implementation. This prevents drifting into an easier but irrelevant experiment.

### 3. Reimplementation Principles

Prefer independent implementation from the paper's description.

- Use author code only as a reference when necessary, and label it clearly.
- Do not copy large blocks of author code into this repo unless license and provenance are explicit.
- If using standard packages, record package names, versions, and why they are appropriate.
- Keep scripts runnable from a clean checkout where practical.
- Pin random seeds, but do not rely on one lucky seed; use ensembles when randomness affects conclusions.
- For reduced-scale runs, preserve the relevant nondimensional parameters or algorithmic structure as much as possible.

### 4. Compute Planning

Before any expensive run:

1. Estimate runtime from a pilot or prior runs.
2. Request walltime as `predicted runtime × 1.3 + 10 minutes`, not the queue maximum by habit.
3. Use all GPUs on an allocated node when the machine has scheduled GPUs.
4. Use debug/short queues only for validation, not production.
5. Add checkpoint/restart for jobs that may timeout or be preempted.
6. Log allocation, queue, node count, GPU count, walltime, and job IDs.

Standing HPC policy:

- Check allocation balance before Polaris/Aurora submissions.
- Use positive-balance allocations only.
- Production jobs must be restartable and idempotent.
- Catch preemption signals where supported and save progress.

### 5. Data and Provenance

Every replication should make provenance auditable.

Record:

- Source URLs, DOIs, OSTI IDs, database versions, download dates.
- Checksums for important downloaded data.
- Any filters, preprocessing, exclusions, or synthetic substitutes.
- Environment details: OS, compiler, Python version, CUDA/SYCL/OpenCL stack, major library versions.
- Hardware used: CPU/GPU model, memory, node count.

If real data are inaccessible, build the smallest scientifically meaningful surrogate and state exactly which claims it can and cannot test.

### 6. Validation and Comparison

Compare against the paper in the same units and, where possible, the same plotted quantities.

Good comparisons include:

- numeric tables: paper value, replicated value, absolute error, relative error, tolerance/rationale
- figures recreated from generated data
- trend checks: ordering, slopes, exponents, phase boundaries, rankings
- ablations or sensitivity checks for under-specified parameters
- negative results when a claim fails under faithful reconstruction

Do not overclaim from a visually similar plot. Quantify the match.

### 7. Report Writing

Each final `REPORT.md` should include:

1. **Executive summary** — verdict in a few sentences.
2. **Paper claims tested** — concise target list.
3. **Replication approach** — what was implemented and why.
4. **Environment and data provenance** — enough detail to rerun/audit.
5. **Results** — figures, tables, quantitative comparisons.
6. **Discrepancies** — explain likely causes; separate bugs, approximations, missing information, and real paper issues.
7. **Reproducibility assessment** — what worked, what did not, and what would be needed for a fuller replication.
8. **Artifacts** — code paths, data paths, job IDs, and generated files.

Use direct language. If a result is only a surrogate, call it a surrogate. If a run is underpowered, say so.

## Scoring and Evaluation Rule

Do **not** use regex or substring matching as the final scorer for coverage, agreement, verdict, or other judgment fields.

Required scoring practice:

- Use an LLM judge to read the relevant report text and assign scores under a written rubric.
- Prefer 3 independent judges when feasible; report disagreement when meaningful.
- Regex/substring extraction is allowed only for non-judgmental metadata or candidate evidence, such as tool names, datasets, hardware, URLs, explicit self-reported claims, or job IDs.
- Values extracted by regex must be labeled evidence/provenance, not final scores.

Recommended rubric dimensions:

- **Coverage**: How much of the paper's central scientific/computational claims were tested?
- **Agreement**: How closely did replicated results match paper results for the tested claims?
- **Fidelity**: How close was the implementation/data/scale to the paper?
- **Reproducibility**: Could another team rerun and audit the workflow from the provided artifacts?
- **Verdict**: `REPLICATED`, `PARTIAL`, `SPOT-CHECK`, `NO-GO`, or `FAILED`.

## Status Vocabulary

Use statuses consistently:

- `REPLICATED` / `COMPLETE`: central claims reproduced with meaningful quantitative agreement.
- `PARTIAL`: important pieces reproduced, but missing data, scale, physics, or implementation details limit the conclusion.
- `SPOT-CHECK`: only a narrow claim or diagnostic was tested.
- `NO-GO`: replication could not proceed because key artifacts or specifications are unavailable.
- `FAILED`: attempted faithfully, but results contradict or fail to reproduce the paper without an identified benign explanation.

## Common Failure Modes to Avoid

- Starting coding before extracting the paper's actual target claims.
- Reproducing a nearby toy problem and implying it validates the full paper.
- Letting reduced scale change the scientific regime without saying so.
- Omitting environment, random seeds, or data provenance.
- Treating author self-scores or regex-extracted score text as independent evaluation.
- Reporting only successful plots while hiding failed runs.
- Burning HPC walltime without pilot sizing or checkpoint/restart.
- Naming machines/endpoints after transient hosted models rather than stable hostnames.

## Minimal Per-Paper Checklist

Before marking a replication complete:

- [ ] Paper metadata recorded.
- [ ] Claims/targets listed before or during implementation.
- [ ] Code and commands needed to reproduce core results are present.
- [ ] Data sources and generated artifacts are documented.
- [ ] Environment and hardware are documented.
- [ ] Quantitative comparisons are included.
- [ ] Discrepancies and approximations are explicit.
- [ ] Final verdict is justified by evidence in the report.
- [ ] Any LLM-based scoring used the no-regex-final-scorer rule.
- [ ] Git status is clean after commit, or remaining untracked artifacts are intentional.

### The 8 mandatory artifacts (see standard above) — all required
- [ ] 1. `paper.pdf` present.
- [ ] 2. `extraction/marker.md` present (or labeled fallback).
- [ ] 3. `extraction/nougat.mmd` present (or stub noting sha256/DOI for later corpus sweep).
- [ ] 4. `report/REPORT.tex` — detailed, section-by-section, with per-claim what-worked/didn't + genuine critique.
- [ ] 5. `report/open_questions.json` — 5 heavy-duty open questions w/ next_steps (paper re-read).
- [ ] 6. `report/workflow.md` — workflow + tools/codes + effort estimate.
- [ ] 7. `report/artifacts_summary.md` — artifact inventory + traces.
- [ ] 8. `report/failure_analysis.md` — honest failure analysis + critique.

## Suggested README Skeleton

```markdown
# <Paper Title>

## Metadata
- Paper:
- Authors:
- DOI/OSTI/arXiv:
- Domain:
- Status:

## Claims Tested
- ...

## What Was Reproduced
- ...

## How to Run
```bash
cd replication
python ...
```

## Results
- Key output paths:
- Summary:

## Limitations
- ...
```

## Suggested Report Verdict Sentence

Use a sentence like:

```text
Verdict: PARTIAL. We reproduced the paper's qualitative ranking and two of four headline numerical trends, but the full result depends on unavailable proprietary input data and a 20× larger compute budget; our reduced-scale surrogate therefore tests the algorithmic mechanism, not the full production claim.
```

## Operating Principle

Be useful, not flattering. A rigorous partial replication with clear limits is more valuable than a polished but ambiguous success story.
