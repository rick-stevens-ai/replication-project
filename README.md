# Replication Project

**Systematic, AI-assisted replication of published computational-science papers.**

Each replication is an *independent* reimplementation (not the authors' code), run to real
output, and scored for reproducibility with an honest account of what did and didn't reproduce.

---

## 🚀 New here? Start with these

| I want to… | Read |
|---|---|
| Understand the project and reproduce a paper myself | **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** |
| Get quick answers (how scoring works, tooling, gotchas) | **[docs/FAQ.md](docs/FAQ.md)** |
| Follow the full operating procedure ("the skill") | **[SKILL.md](SKILL.md)** |
| See the big-picture talks | `Can_a_Robot_Replicate_Science.pptx`, `Reproducing_1000_Papers_in_10_Days.pptx` |
| Know exactly what a finished replication must contain | **[scripts/REPLICATION_DIR_STANDARD_2026-07-05.md](scripts/REPLICATION_DIR_STANDARD_2026-07-05.md)** |
| See current status of everything | **[STATUS_AUDIT.md](STATUS_AUDIT.md)** + newest `RECONCILED_MASTER_*.csv` |

> **One-sentence version:** point a capable AI agent at a paper, make it *independently rebuild
> the method and run real code*, then make it write an honest, scored report — including
> everything it could **not** reproduce.

---

## What a replication contains (the 8-artifact bar)

A replication is **not done** until its directory has all 8 (audit with
`python scripts/check_repl_dir_standard.py`):

```
<SET>/<paper-dir>/
  paper.pdf                        # 1. source paper
  extraction/marker.md             # 2. Marker text extraction
  extraction/nougat.mmd            # 3. Nougat math-text extraction
  report/REPORT.tex (+ REPORT.pdf) # 4. detailed section-by-section report + critique
  report/open_questions.json       # 5. five heavy-duty open questions + next steps
  report/workflow.md               # 6. workflow, tools/versions, effort estimate
  report/artifacts_summary.md      # 7. artifact inventory + traces
  report/failure_analysis.md       # 8. honest failure/gap analysis
  report/evidence/                 # real outputs (json/csv/logs/figures/code)
  work/                            # code + data + intermediates
```

---

## How the repo is organized

Replications are grouped into **sets**. Most sets are directory-prefixed at the top level; the
newer QC sets use container directories.

| Set | Domain | Papers | Where |
|---|---|---|---|
| **LUCID-100** | Radiation biology / low-dose | ~142 | `LUCID-replications/` |
| **OSTI-100** | Mixed DOE/OSTI computational science | 111 | `OSTI-*` (top level) |
| **PDE-100** | PDE solvers, numerical methods, SciML | ~131 | `PDE-*` + `PDE-replications/` |
| **BVBRC-100** | Bacterial genomics / AMR | 127 | `BVBRC-*` (top level) |
| **QC-100** | Quantum computing / quantum chemistry | ~146 | `QC-100/` |
| **QC-200** | Quantum computing (second wave) | 105 | `QC-200/` |
| **OTHER-100** | Legacy / cross-domain entries (numeric-ID + slug-named) | ~61 | `OTHER-100/` |

Every paper lives inside a set container — there are **no loose numeric-ID or unsorted paper
directories at the top level**. Project infrastructure (candidate lists, scoring assets,
drafts, corpora) lives under `_support/`.

**Reconciliation status** (from `RECONCILED_MASTER_2026-06-24.csv`, 729 rows):
**275 REPLICATED · 371 PARTIAL · 48 spot-check** (plus a handful NO-GO / blocked / contradicted).
"Solid" = REPLICATED + PARTIAL. Numbers move as waves complete — always trust the newest census.

Supporting locations:
- **`docs/`** — getting-started, FAQ, and planning archive.
- **`scripts/`** — reconciliation & audit tooling (below).
- **`SKILL.md`** — the replication operating procedure.
- **`STATUS_AUDIT.md`, `CENSUS_*.csv`, `RECONCILED_MASTER_*.csv`** — living status.

---

## Tooling (`scripts/`)

| Script | What it does | Usage |
|---|---|---|
| `census.py` | Builds the status census from reports on disk (ground truth) | `python3 scripts/census.py --csv CENSUS_$(date +%F).csv` |
| `rebuild_reconciled.py` | Rebuilds the reconciled master from a census | `python3 scripts/rebuild_reconciled.py CENSUS_$(date +%F).csv` |
| `reconcile_reports.py` | Harvests verdict + coverage/agreement from every report | `python3 scripts/reconcile_reports.py` |
| `check_repl_dir_standard.py` | Audits each dir for the 8 required artifacts | `python3 scripts/check_repl_dir_standard.py --missing` |
| `harvest_open_questions.py` | Rolls per-paper open questions into a corpus | `python3 scripts/harvest_open_questions.py` |
| `harvest_repass_scores.py` | Collects re-pass re-scoring results | `python3 scripts/harvest_repass_scores.py` |

**End-of-day reconciliation** (do this before launching new work):
```bash
python3 scripts/census.py --csv CENSUS_$(date +%F).csv
python3 scripts/rebuild_reconciled.py CENSUS_$(date +%F).csv
```

---

## Principles

- **Independent reimplementation**, not authors' code re-run.
- **Real code to real output**, compared with units and tolerances.
- **LLM-as-judge scoring** — never regex/substring for final scores.
- **Honesty over fidelity theater** — partial/failed reproduction, documented well, is valuable.
- **Every replication carried to a written, scored report.** No unfinished shells.

---

*A slide-deck history of the effort lives in `docs/planning-archive/` alongside dated launch/audit
notes. For the current state, use `STATUS_AUDIT.md` and the newest reconciled master CSV.*
