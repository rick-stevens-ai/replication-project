# Workflow

**Slot:** `lucid100-cho-low-dose-rate-dna-repair-deficient`
**Paper:** Buglewicz et al., *BBRC* **698**: 149539 (2024), DOI 10.1016/j.bbrc.2024.149539.
**Backfill date:** 2026-07-06 (documenting workflow of original 2026-06-09 first-pass +
2026-06-22 audit + 2026-06-25 re-tier). No new simulations run at backfill time.

## Pipeline stages

1. **Metadata / OA-status probe.** Query Unpaywall, Semantic Scholar, EuropePMC, Crossref, and
   OpenAccessButton for OA copies of the target DOI. Result: `is_oa=false` from every source;
   no PMC record, no preprint, no thesis. Evidence saved to `artifacts/{unpaywall,semscholar,
   europepmc,crossref}.json` and `artifacts/pubmed.xml`.
2. **Companion-paper anchor selection.** Because the primary paper is unreadable, identify OA
   companions from the same lab (Kato lab, CSU) using the same CHO mutant panel and same
   endpoints. Selected: Buglewicz 2023 *Cancer Sci.* (PMC10727999), Kato 2019 *Sci. Rep.*
   (PMC6467899). Downloaded PDF + JATS XML into `artifacts/`.
3. **Panel reconstruction.** From companion papers + Crossref bibliography, reconstruct the
   most likely cell-line panel: 10B2 or AA8 (WT), 51D1 (HR$^-$), V3 (NHEJ$^-$-DNA-PKcs), with
   xrs-5/xrs-6/irs1SF plausibly included.
4. **Analytical smoke model.** Implement LQ + Lea--Catcheside dose-protraction factor + a
   phenomenological NHEJ IDRE $\alpha$-boost term in Python (`scripts/replicate_smoke.py`).
   Choose per-line $(\alpha, \beta, \tau, \phi, \dot D_0)$ so that acute SER ordering matches
   PMC10727999 Table 1. Explicitly flag parameters as illustrative.
5. **Claim scoring.** Enumerate 8 claims from abstract + MeSH + author keywords; score each as
   TESTED (SMOKE PASS/FAIL) or BLOCKED (data or text). Result: 3/8 tested (all SMOKE PASS,
   direction only), 5/8 BLOCKED.
6. **Verdict assignment.** Under 80%/80% (coverage / claims) bar for REPLICATED: fails. Under
   Rick's hard-ceiling rule (2026-06-25): SPOT-CHECK $\to$ NO-GO. Recorded in REPORT.md
   header.
7. **Backfill (2026-07-06).** Generated 7 backfill artifacts under `report/` + `extraction/`
   to meet the 8-artifact LUCID standard. No new simulations, no changes to
   `scripts/replicate_smoke.py` or `data/smoke_summary.json`.

## Tools / versions

| Tool | Version | Used for |
|---|---|---|
| Python | 3.13 (system) | `scripts/replicate_smoke.py` |
| NumPy | (system) | LQ + Lea--Catcheside arithmetic |
| Matplotlib | (system) | `figures/*.png` |
| curl | macOS 25.3 default | OA-status probes to Unpaywall, S2, OA-Button, Crossref |
| `pdftotext` (Poppler) | system Homebrew | PMC6467899 PDF -> text |
| Argo LLM proxy | localhost:44497, key=stevens | claim extraction sanity-check (Claude Opus 4.7, free per Rick's standing rule) |
| macOS | 25.3.0 (Darwin) | host |

**No paid endpoints used.** All model calls (if any at backfill time) route through
`argo://localhost:44497` with `API_KEY=stevens`.

**No GPU used.** Smoke model is closed-form; runs on CPU in ~1 s.

## Work estimate

- **First-pass reproduction attempt (2026-06-09):** ~2 h subagent time (OA-status probes,
  companion-paper download, panel reconstruction, initial smoke script drafting, first
  FIRST_PASS_REPORT.md).
- **Audit + re-verification (2026-06-22):** ~1.5 h (re-probe OA sources, verify smoke reruns
  cleanly, write REPORT.md).
- **Re-tier (2026-06-25):** ~5 min (header update in REPORT.md).
- **Backfill (2026-07-06, this pass):** ~30 min (7 files, incremental writes per Rick's
  failure-log rule about batched writes dying with nothing on disk).

Total cumulative human-equivalent: ~4 h. **All wet-lab work impossible without publisher
paywall access and/or author data deposit.**

## Reproducer

Full reproduction of the smoke model, on any machine with Python 3 + NumPy + Matplotlib:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/\
lucid100-cho-low-dose-rate-dna-repair-deficient/
python3 scripts/replicate_smoke.py
```

Wall time: ~1 s. Regenerates `data/smoke_summary.json`,
`figures/acute_survival.png`, `figures/dose_rate_sparing.png`. Deterministic (no RNG).

To rebuild the LaTeX report:

```bash
cd report/
pdflatex REPORT.tex
pdflatex REPORT.tex     # second pass for cross-refs
```

**No external network required at reproduce time.** Companion-paper PDFs and metadata JSONs
are already cached in `artifacts/`.

## Provenance

- Original first-pass: 2026-06-09 (see `FIRST_PASS_REPORT.md`).
- Audit + verdict: 2026-06-22 (see `REPORT.md`).
- Re-tier SPOT-CHECK -> NO-GO: 2026-06-25 (REPORT.md header).
- Backfill (this workflow doc + 6 sibling files): 2026-07-06.
- No cross-slot contamination: this slot uses only its own smoke script, own companion PDFs,
  own claim list. No shared code paths with other LUCID-100 slots.
