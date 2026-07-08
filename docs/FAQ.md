# FAQ: AI-Assisted Paper Replication

Answers to the questions people ask most about this project and how to reproduce papers with
an AI agent. New here? Start with [`GETTING_STARTED.md`](GETTING_STARTED.md).

---

## The basics

### What is this project?
A systematic effort to test the reproducibility of published computational-science papers by
having a capable AI agent **independently** reimplement each paper's method, run real code, and
write an honest, scored report on what did and didn't reproduce. It spans several domains,
grouped into sets: **LUCID, OSTI, PDE, BVBRC, QC**.

### What does "replication" mean here — exactly?
Reconstructing the paper's method from the paper (not the authors' code), running it to real
output, and comparing against the paper's quantitative claims **with units, tolerances, and
caveats**. A replication documents what was faithful, what was approximated, and what was
impossible. A *partial* replication is fine — as long as it's honest.

### How is this different from just re-running the authors' code?
We deliberately do **not** copy and rerun authors' repos. Re-running someone's code tests that
their code runs; *reimplementing from the paper* tests whether the paper is a sufficient,
correct description of the work. The second is what "reproducibility" actually means.

### Can an AI really replicate a scientific paper?
For many computational papers, yes — to a useful degree, with a competent agent, the right
compute, and a human keeping it honest. The value isn't "the AI did it alone"; it's a
*repeatable, auditable process* that produces a defensible reproducibility verdict and a list
of exactly where reproduction broke down.

---

## Getting a model to replicate a paper

### What kind of AI agent do I need?
Anything that can read files, write code, run a shell, and iterate: Claude Code, Codex, Gemini
CLI, OpenClaw, Cursor, etc. The key capability is an agent loop that can debug its own runs, not
one-shot text generation.

### What's the actual procedure the agent follows?
The 8-step loop in [`GETTING_STARTED.md`](GETTING_STARTED.md) §2, formalized in
[`../SKILL.md`](../SKILL.md): ingest → assess gaps → reconstruct → run → compare →
score → report (8 artifacts) → 5 open questions.

### How do I prompt the agent?
Give it: (1) the paper PDF + SI, (2) the [`SKILL.md`](../SKILL.md) as its operating procedure,
(3) the [8-artifact standard](../scripts/REPLICATION_DIR_STANDARD_2026-07-05.md) as the
completion bar, and (4) a clear instruction to *reconstruct independently, run real code, and be
honest about gaps*. Then let it work, and review its report critically.

### What makes a replication "good"?
It identifies the central claims and quantitative targets; reconstructs the method; runs
executable code that produces comparable outputs; compares with units/tolerances; and documents
faithful/approximated/impossible parts. It does **not** inflate fidelity by hiding shortcuts,
synthetic substitutes, reduced problem sizes, missing data, or skipped physics.

### How long does one paper take?
Minutes-to-hours of agent time for the write-up and light compute; hours-to-days of wall-clock
for heavy DFT/MD/ML/quantum-chemistry runs. The bottleneck is almost always compute and data
access, not the agent.

---

## Scoring & honesty

### How are replications scored?
By **LLM-as-judge** reading the report against a rubric (coverage / agreement / verdict) —
preferably multiple judges. **Never** by regex or substring matching on the report text. Regex
is allowed only to extract non-judgmental metadata (tool names, dataset IDs, hardware), marked
as evidence-only.

### What are the possible verdicts?
Broadly: **REPLICATED** (claims reproduced within tolerance), **PARTIAL** (some claims
reproduced, others approximated/blocked), and not-reproduced. "Solid" in status counts usually
means REPLICATED + PARTIAL. Exact verdict labels live in the census CSVs and `STATUS_AUDIT.md`.

### What if I can't fully reproduce the paper?
That's a normal, valuable outcome. Scope it honestly (e.g., "methodological replication:
reduced system size / simulated the hardware step / data not deposited"), still deliver all 8
artifacts, and let the failure analysis carry the weight. See the FLiBe QC-100 example.

### Why is the "failure analysis" artifact required even for successes?
Because every replication involves assumptions, approximations, and friction. Documenting them —
even for a clean REPLICATED verdict — is what makes the result auditable and reusable.

---

## Repository structure & tooling

### How is the repo organized?
Replications are grouped by set using directory prefixes (`LUCID-*`, `OSTI-*`, `PDE-*`,
`BVBRC-*`, `QC-*`), with `QC-100/` and `QC-200/` as container subdirectories. Older entries use
numeric-ID prefixes. Project docs are in `docs/`, tooling in `scripts/`, and living status in
`STATUS_AUDIT.md` + `RECONCILED_MASTER_*.csv`.

### What are the scripts in `scripts/` for? {#tooling}
| Script | What it does |
|---|---|
| `census.py` | Scans all replication dirs and builds a status **census** CSV (what exists, what's scored) |
| `rebuild_reconciled.py` | Rebuilds the reconciled master CSV from a census — the canonical status of every paper |
| `reconcile_reports.py` | Cross-checks reports vs the master for consistency |
| `check_repl_dir_standard.py` | Audits each dir for the **8 required artifacts** |
| `harvest_open_questions.py` | Rolls up per-paper `open_questions.json` into a project-wide corpus |
| `harvest_repass_scores.py` | Collects re-pass/re-scoring results into summary tables |

Typical end-of-day reconciliation:
```bash
python scripts/census.py --csv CENSUS_$(date +%F).csv
python scripts/rebuild_reconciled.py CENSUS_$(date +%F).csv
```

### What are the 8 required artifacts again?
1. `paper.pdf` · 2. `extraction/marker.md` · 3. `extraction/nougat.mmd` ·
4. `report/REPORT.tex` (+PDF) · 5. `report/open_questions.json` (5 Qs + next steps) ·
6. `report/workflow.md` · 7. `report/artifacts_summary.md` · 8. `report/failure_analysis.md`.
Full spec: [`../scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`](../scripts/REPLICATION_DIR_STANDARD_2026-07-05.md).

### Where do I see overall status?
`STATUS_AUDIT.md` and the newest `RECONCILED_MASTER_*.csv` / `CENSUS_*.csv` at the repo root.

---

## Practical / gotchas

### Do I need GPUs?
Only for GPU-bound papers (DFT, large MD, deep learning, quantum-chemistry). Many replications
(algorithms, math, signal processing, smaller ML) run fine on a laptop.

### How do I handle huge generated data?
Keep it **out of git**. Record the external location + checksums in the report. The repo tracks
code, small essential inputs, reports, and figures — not multi-GB run outputs.

### What compute policy should I follow for HPC jobs?
Estimate runtime first and right-size the queue; use production (not debug) queues for real runs;
checkpoint-restart anything that could time out; and use all GPUs on a node. Check your
allocation balance before submitting.

### Can I contribute a replication?
Yes — copy the directory skeleton (GETTING_STARTED §3), follow the SKILL, deliver all 8
artifacts, then run `check_repl_dir_standard.py` on your dir and `census.py` to register it.

### I'm overwhelmed — where do I actually start?
Read [`GETTING_STARTED.md`](GETTING_STARTED.md), open one finished example (e.g. the FLiBe
QC-100 dir), read its `REPORT` + `failure_analysis.md`, then replicate a small open-artifact
paper end to end. Don't start with the hardest paper in your field.
