# Workflow narrative — slot 69 (UNIVERSE + DDRi ion-beam mechanistic model)

**Target paper:** Liew et al., *Combined DNA Damage Repair Interference and Ion Beam Therapy*, IJROBP 112(3):802–817 (2022). DOI 10.1016/j.ijrobp.2021.09.048. PMID 34710524. Elsevier closed-access.

**De-masked model:** UNIVERSE (UNIfied and VErsatile bio-response Engine, DKFZ/HIT).

**Verdict (queue):** REPLICATED. **Verdict (internal, honest):** PARTIAL — mechanistic core replicated; novel helium-SOBP experiment + patient-plan translation not reproducible.

---

## 1. Pipeline overview

The replication was a **model-substitution replication**: the target paper is closed and its source
code (UNIVERSE) has never been released, but the model equations are fully published in two
open-access twin papers (Liew 2019 IJMS, Mein 2019 Radiat Oncol). The workflow:

1. **Identify the paper's actual model** (this was itself work — the paper does not name UNIVERSE
   in the abstract; the identification was done by cross-referencing the Liew 2022 UNIVERSE/FLASH
   companion papers).
2. **Locate open sources.** Pull the OA twins from the publisher (MDPI OA CC-BY) into `source/`.
   Confirm the target paper is closed via Unpaywall + no PMC.
3. **Re-implement the mechanistic core in NumPy.** No external scientific dependencies beyond
   NumPy + SciPy.
4. **Run three sweeps** (photon dose response, DDRi dose response, LET sweep) and compare against
   what the paper claims in its abstract + what the twin papers publish in figures.
5. **Write the report** grounding every claim in either the smoke output or the OA twin paper.

Total compute: negligible (~27 seconds NumPy on CherryRd). Total human/agent work: several hours
of paper reading + model identification + code + reporting.

---

## 2. Tools + versions

| Tool | Role | Version (as of 2026-06-09) |
|---|---|---|
| Python 3 | Runtime | Homebrew Python 3.x on macOS Tahoe (CherryRd) |
| NumPy | MC + LQ fit | Homebrew scientific-Python stack |
| SciPy | LQ fit (`scipy.optimize.curve_fit`) | idem |
| Matplotlib | Figures (`figures/*.png`) | idem |
| Semantic Scholar API | Paper metadata (target paper abstract, authors, IDs) | v1 (S2 REST); key from OpenClaw env `S2_API_KEY` |
| Unpaywall API | OA-status check for target DOI | v2 (public) |
| Argo LLM proxy | Report drafting + planning | localhost:44497, key=stevens; models used: argo:claude-opus-4.8 (default), argo:gpt-5.4 (sanity checks) |
| pdftotext (poppler) | OA twin-paper text conversion (source/*.txt) | poppler-utils bundled with macOS |
| Git (untracked) | Work-in-progress checkpointing | N/A — dir is Dropbox-synced |

**No paid endpoints. No GPU. No closed software (the whole point of the exercise).**

---

## 3. Codebases produced by this replication

| File | LOC | Purpose |
|---|---|---|
| `code/universe_smoke.py` | 266 | Core UNIVERSE + DDRi engine. GLOBLE giant-loop MC + iDSB/cDSB classification + (1−K)^N survival + RSF-on-K_iDSB DDRi + bounded α_DSB(LET) surrogate. |
| `code/run_smoke.py` | 227 | Driver: runs 3 sweeps (photon, DDRi, LET), writes 5 CSV/JSON, plots 3 PNGs. |
| `code/…` (any additional helpers) | (see `code/` directory listing in artifacts_summary.md) | plotting + IO helpers |

Total original code: ~500 LOC. Everything in `code/` was written for this replication.

---

## 4. Codebases pulled in

None. No external code was cloned or vendored. The entire replication is stand-alone NumPy.

The five OA twin PDFs in `source/` were downloaded from the publisher (MDPI OA CC-BY) — those are
literature, not code.

---

## 5. Command-level reproduction (what to type to re-run)

```
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-ddr-interference-ion-beam-mechanistic-slot69/code
python3 run_smoke.py
```

Runtime: ~27 s single-thread on CherryRd (M-series Mac). Regenerates:
- `../results/photon_survival_no_ddri.csv`
- `../results/photon_survival_atmi.csv`
- `../results/lq_fits.csv`
- `../results/let_sweep_ddri.csv`
- `../results/smoke_summary.json`
- `../figures/photon_no_ddri.png`
- `../figures/photon_atmi.png`
- `../figures/let_sweep_rbe_ratio.png`

MC seed is fixed inside `universe_smoke.py`, so successive runs are byte-equivalent modulo
platform-level float behaviour.

---

## 6. Estimate of work done

| Category | Estimate |
|---|---|
| Compute (wall clock) | ~27 s per full smoke; total lifetime including exploratory sweeps: minutes |
| Agent turns (identify paper + de-mask model + write code + write REPORT.md) | high tens across the 2026-06-09 to 2026-06-22 period visible in file mtimes |
| LOC written | ~500 (code) + ~600 lines of REPORT.md + supporting docs |
| Papers read (in full or in relevant sections) | 5 OA papers: Liew 2019 IJMS, Mein 2019 Radiat Oncol, Liew 2020 Cancers, Liew 2022 IJMS (repair), Liew 2022 IJMS (FLASH), Scholz 2020 LEM-IV. Plus the target-paper abstract via S2. |
| API calls (paid endpoints) | 0 |
| API calls (Argo, free) | many during the initial replication; a small number during this backfill |

The 2026-06-22 mtime on REPORT.md indicates a substantial rewrite happened ~2 weeks after the
initial 2026-06-09 code and result files were written — consistent with an iterated draft where
the smoke was written first, then evidence was re-audited, then the report was consolidated.

---

## 7. Backfill workflow (this turn, 2026-07-06)

Per Rick's 2026-07-05 BACKFILL brief:

1. `ls` target dir → REPORT.md + code/ + results/ + figures/ + source/ + FIRST_PASS_REPORT.md
   present. `report/` and `extraction/` absent. Verdict = REPLICATED (from priority queue).
2. Read `REPORT.md` (rich narrative, ~21.5 KB, everything needed for pure-write task).
3. Created `report/` and `extraction/` dirs.
4. Wrote `report/REPORT.tex` grounding every claim in REPORT.md (with genuine critique).
5. Wrote `report/open_questions.json` with 5 truly-open questions, each with concrete next steps.
6. Wrote `report/workflow.md` (this file).
7. Wrote `report/artifacts_summary.md` (inventory).
8. Wrote `report/failure_analysis.md` (honest gaps + evidence-strength critique).
9. Attempted paper.pdf fetch — Elsevier closed, no OA source; wrote `extraction/paper.pdf.MISSING.md`.
10. Wrote `extraction/nougat.mmd` stub (no GPU parse available) + `extraction/marker.md` fallback
    from existing OA twin `.txt` files.

Backfill compute: minutes (mostly Argo/LLM drafting time). No paid endpoints.
