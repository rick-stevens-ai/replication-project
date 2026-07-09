# Artifacts inventory — slot 69

**Paper:** Liew et al. 2022, IJROBP 112(3):802–817. DOI 10.1016/j.ijrobp.2021.09.048.
**Slot dir:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-ddr-interference-ion-beam-mechanistic-slot69/`
**Set:** LUCID.
**Verdict (queue):** REPLICATED. **Verdict (internal, honest):** PARTIAL.

---

## A. Top-level slot artifacts

| File | Size | Content |
|---|---|---|
| `README.md` | 5.6 KB | Slot README |
| `PROGRESS.md` | 6.9 KB | Progress log |
| `ARTIFACT_MANIFEST.md` | 2.4 KB | Original artifact manifest (pre-backfill) |
| `FIRST_PASS_REPORT.md` | 7.0 KB | First-pass narrative report (2026-06-09) |
| `REPORT.md` | 21.5 KB | Consolidated report (2026-06-22) — the primary source of truth |

## B. Report bundle (`report/`, written during 2026-07-06 backfill)

| File | Purpose |
|---|---|
| `report/REPORT.tex` | Detailed LaTeX report with claims table, method, per-claim what-worked, critique, verdict, 5 open questions |
| `report/open_questions.json` | 5 truly-open questions with `{q, basis, next_steps}` each |
| `report/workflow.md` | Pipeline narrative + tools + versions + estimate of work |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest failure analysis + evidence-strength critique |

## C. Extraction bundle (`extraction/`, written during 2026-07-06 backfill)

| File | Purpose |
|---|---|
| `extraction/paper.pdf.MISSING.md` | Marker: target paper is Elsevier closed-access; no PDF in dir; sha256 not applicable |
| `extraction/marker.md` | Marker-format fallback: concatenated OA twin `.txt` extracts with headers |
| `extraction/nougat.mmd` | Stub — pending central Nougat parse (target PDF unavailable) |

## D. Code (`code/`) — all written for this replication

| File | Size | LOC | Purpose |
|---|---|---|---|
| `code/universe_smoke.py` | 11.8 KB | 266 | GLOBLE giant-loop MC + iDSB/cDSB classification + (1−K)^N survival + RSF-on-K_iDSB DDRi + bounded α_DSB(LET) surrogate |
| `code/run_smoke.py` | 9.6 KB | 227 | Driver: 3 sweeps → 5 CSV/JSON + 3 PNG |
| `code/__pycache__/universe_smoke.cpython-314.pyc` | 12.3 KB | — | Python 3.14 bytecode cache (safe to delete) |

## E. Results (`results/`, all produced by `python3 code/run_smoke.py` in ~27 s)

| File | Size | Content |
|---|---|---|
| `results/smoke_summary.json` | 6.7 KB | Master JSON: LQ fits, DDRi dose curves, LET sweep, headline booleans |
| `results/photon_survival_no_ddri.csv` | 462 B | 5 cell lines × 9 doses |
| `results/photon_survival_atmi.csv` | 661 B | 2 cell lines × 4 RSF conditions × 7 doses |
| `results/lq_fits.csv` | 191 B | α (Gy⁻¹), β (Gy⁻²), α/β (Gy) per cell line |
| `results/let_sweep_ddri.csv` | 293 B | 8 LET points × (RBE_noDDRi, RBE_DDRi, ratio) |

## F. Figures (`figures/`)

| File | Size | Content |
|---|---|---|
| `figures/photon_no_ddri.png` | 68 KB | 5-cell-line photon dose-response |
| `figures/photon_atmi.png` | 92 KB | DDRi dose-response (H460, H1437, 4 conditions each) |
| `figures/let_sweep_rbe_ratio.png` | 61 KB | Headline RBE_DDRi/RBE_no-DDRi vs LET |

## G. Source materials (`source/`) — OA papers + metadata

| File | Size | Role |
|---|---|---|
| `source/model_notes.md` | 9.3 KB | Full model derivation, equation numbering, parameter tables, replicability assessment |
| `source/semantic_scholar_metadata.json` | 3.5 KB | S2-fetched target-paper metadata (authors, abstract, IDs) |
| `source/liew2019_ddr_hypoxia_photon.pdf` + `.txt` | 872 KB + 63 KB | Liew 2019 IJMS — photon UNIVERSE + DDRi (Eqs 1–7, Table 1 K, Table 3 RSF). OA CC-BY. |
| `source/mein2019_universe_rbe.pdf` + `.txt` | 4.0 MB + 82 KB | Mein 2019 Radiat Oncol — ion-beam Kiefer–Chatterjee + UNIVERSE-RBE. OA CC-BY. |
| `source/liew2020_hypoxia_direct_indirect.pdf` + `.txt` | 1.7 MB + 52 KB | Liew 2020 Cancers — HRF parameterisation. OA. |
| `source/liew2022_universe_repair.pdf` + `.txt` | 6.4 MB + 103 KB | Liew 2022 IJMS repair companion (de-masks UNIVERSE). OA. |
| `source/liew2022_universe_flash.pdf` + `.txt` | 2.2 MB + 119 KB | Liew 2022 IJMS FLASH companion. OA. |
| `source/scholz2020_lemiv_part1.pdf` + `.txt` | 1.8 MB + 90 KB | Scholz 2020 LEM-IV reference (Friedrich 2015 clustering family). OA. |

## H. Accessions / IDs

| Item | ID |
|---|---|
| Target paper DOI | 10.1016/j.ijrobp.2021.09.048 |
| Target paper PMID | 34710524 |
| Target paper Semantic Scholar (see source/semantic_scholar_metadata.json) | — |
| Model (de-masked) | UNIVERSE (DKFZ/HIT) |
| Priority-queue verdict | REPLICATED (preserved for this backfill) |
| Internal REPORT.md verdict | PARTIAL — mechanistic core only, COVERAGE=5/10 AGREEMENT=7/10 |

## I. Reproducibility trace

The `code/`, `results/`, and `figures/` contents were regenerated in 26.91 s by re-running
`python3 code/run_smoke.py` during the 2026-06-22 REPORT.md pass. MC seed is fixed. No paid
endpoints and no closed software are required.

**How to re-verify from scratch on a fresh Mac/Linux box:**
```
cd .../lucid-ddr-interference-ion-beam-mechanistic-slot69/code
python3 -c "import numpy, scipy, matplotlib"   # ensure deps
python3 run_smoke.py                             # ~27 s
diff -q ../results/smoke_summary.json /tmp/prev_smoke.json  # optional
```

## J. What's NOT in this dir

- `paper.pdf` — the target paper is Elsevier closed-access. No PDF available (see
  `extraction/paper.pdf.MISSING.md`).
- Raw helium-SOBP cell-survival tables — not in any OA supplement. Would need author data request.
- Friedrich 2015 intra-track DSB-clustering formula — paywalled *Radiat Prot Dosim* 166:61–65.
- UNIVERSE source code — never released by DKFZ/HIT (verified via S2 + GitHub search).
- HIT FLUKA-coupled TPS + anonymised patient CT/RT-Plan — institutional/protected.
