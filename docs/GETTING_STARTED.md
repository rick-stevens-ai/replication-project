# Getting Started: Replicating a Paper with an AI Agent

This guide walks you from *"I have a paper I want to reproduce"* to *"I have a scored,
auditable replication report."* It is written for someone new to the project who has access
to a capable coding-agent (Claude Code, Codex, an OpenClaw agent, etc.) and some compute.

> **The one-sentence version:** point a competent AI agent at a paper, make it *independently
> rebuild the method and run real code*, then make it write an honest report comparing its
> results to the paper — including everything it could **not** reproduce.

---

## 0. What this project is (and isn't)

- **Is:** a systematic effort to test whether published computational-science papers can be
  independently reproduced by an outside team using AI assistance. Every replication is an
  independent reimplementation, run to real output, and scored for fidelity.
- **Isn't:** a demo generator. We do **not** copy authors' code and rerun it. We do **not**
  claim success from a plot that "looks similar." Honesty about partial/failed reproduction is
  the point, not a failure.

See [`FAQ.md`](FAQ.md) for common questions and [`../SKILL.md`](../SKILL.md) for the full
operating procedure (this is the "skill" people keep asking for).

---

## 1. Prerequisites

| You need | Notes |
|---|---|
| An AI coding agent | Claude Code, Codex, Gemini CLI, OpenClaw, or similar — anything that can read, write, run shell, and iterate |
| The paper | PDF + any supplementary information (SI). A DOI/arXiv ID is enough to start |
| Compute | Laptop is fine for many papers; GPU/HPC for DFT, MD, large ML, or quantum-chem work |
| Domain tools | Installed on demand per paper (PySCF, LAMMPS, Quantum ESPRESSO, PyTorch, etc.) |
| Free LLM endpoints (for scoring) | LLM-as-judge scoring; never regex/substring for final scores |

You do **not** need to be an expert in the paper's field. The workflow is designed so a
competent generalist + a good agent can produce a useful replication and clearly flag the
limits of what they could verify.

---

## 2. The 8-step loop (what the agent actually does)

1. **Ingest the paper.** Pull the PDF, extract the text (Marker/Nougat, or `pdftotext` as a
   fallback), read the methods + SI end to end. Write down: the systems/datasets, the exact
   method, tool/version requirements, and the **quantitative claims** you'll test.
2. **Assess reproducibility up front.** Before running anything, list what is and isn't
   available: Are the input data/geometries deposited? Is the code released? Is the required
   hardware accessible? This "reproducibility gap" table shapes everything and goes in the report.
3. **Reconstruct the method.** Independently implement the pipeline from the paper — not from
   the authors' repo. Small, testable modules. Verify sanity checks early (e.g., "does my
   basis give the same orbital count the paper reports?").
4. **Run real code to real output.** Generate comparable results. Use the right compute; for
   long HPC jobs, checkpoint and right-size the queue.
5. **Compare with units and tolerances.** Put your numbers next to the paper's. State
   agreement in physical units, not vibes. Where you reduced problem size or substituted a
   method, say so and quantify the effect.
6. **Score it (LLM-as-judge).** Coverage / agreement / verdict are judged by reading the
   report against a rubric — **never** by regex on the text. Prefer multiple judges.
7. **Write the report + 8 artifacts** (see §3). Carry every replication all the way to a
   written, scored `REPORT.md`/`REPORT.tex`. An unfinished shell (PDF pulled, no report) is a
   failure mode, not a stopping point.
8. **Gather 5 open questions.** Re-read the paper and record 5 genuinely open, important
   questions the replication surfaced, each with concrete next steps. These feed future work.

---

## 3. The completion bar: 8 required artifacts

A replication is **not done** until its directory contains all 8. Full spec:
[`../scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`](../scripts/REPLICATION_DIR_STANDARD_2026-07-05.md);
audit any dir with `python scripts/check_repl_dir_standard.py`.

```
<SET>/<paper-dir>/
  paper.pdf                       # 1. source paper
  extraction/marker.md            # 2. Marker text extraction (or labeled fallback)
  extraction/nougat.mmd           # 3. Nougat math-text extraction (or stub w/ sha256/DOI)
  report/REPORT.tex (+ REPORT.pdf)# 4. detailed, section-by-section LaTeX report + critique
  report/open_questions.json      # 5. five heavy-duty open questions, each with next steps
  report/workflow.md              # 6. workflow, tools/versions, effort estimate
  report/artifacts_summary.md     # 7. inventory of all artifacts + traces
  report/failure_analysis.md      # 8. honest failure/gap analysis (required even if REPLICATED)
  report/evidence/                # real outputs: json/csv/logs/figures/code
  work/                           # code + downloaded data + intermediates
```

---

## 4. A worked example (the pattern to copy)

The QC-100 entry `QC-2606.30402-quantum-fusion-blanket-flibe-tritium` is a clean, recent
example of a hard replication done honestly:

- **Paper:** a quantum-computing study of tritium binding in FLiBe molten salt (DFT + embedded
  wavefunction + sample-based quantum diagonalization on IBM hardware).
- **Gaps identified up front:** exact AIMD geometries not deposited; no IBM quantum hardware
  access. So it became a **methodological / qualitative-claims** replication.
- **What was done anyway:** built chemically-valid clusters of identical stoichiometry/charge,
  ran the full DFT + RHF/MP2/CCSD ladder, reproduced the embedded-wavefunction fragmentation,
  and **simulated** the quantum step classically (LUCJ + SQD on a simulator).
- **Verified sanity check:** reproduced the paper's exact atomic-orbital count (378 AOs).
- **Delivered:** all 8 artifacts, with the failure analysis stating plainly what could not be
  matched and why.

Read that directory's `report/workflow.md` and `report/failure_analysis.md` to see the
expected level of honesty and detail.

---

## 5. Choosing a paper (fidelity you can actually reach)

Best candidates for a *high-fidelity* replication are **open**: released code, deposited data,
and hardware you can access. When those are missing, you can still do a valuable **partial or
methodological** replication — just scope it honestly. The project favors open-artifact papers
for exactly this reason.

---

## 6. Where things live

- **`README.md`** — top-level navigation.
- **`SKILL.md`** — the full replication operating procedure (the "skill").
- **`docs/`** — this guide + FAQ.
- **`scripts/`** — reconciliation & audit tooling (see [`FAQ.md`](FAQ.md) §Tooling).
- **`<SET>-*/` dirs** — the replications themselves, grouped by set
  (LUCID / OSTI / PDE / BVBRC / QC).
- **`STATUS_AUDIT.md`, `RECONCILED_MASTER_*.csv`** — the living status of every replication.

---

## 7. First command to run

Audit an existing replication to see the standard in action:

```bash
cd REPLICATE-PROJECT
python scripts/check_repl_dir_standard.py            # audit all dirs for the 8 artifacts
python scripts/census.py --csv CENSUS_$(date +%F).csv # rebuild the status census
```

Then open the worked example above, read its report, and start your own paper by copying the
directory skeleton in §3.
