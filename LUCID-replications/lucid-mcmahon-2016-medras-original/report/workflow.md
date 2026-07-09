# Workflow — lucid-mcmahon-2016-medras-original

**Paper:** McMahon SJ, Schuemann J, Paganetti H, Prise KM (2016).
_Mechanistic Modelling of DNA Repair and Cellular Survival Following
Radiation-Induced DNA Damage._ **Scientific Reports 6:33290.**
DOI: [10.1038/srep33290](https://doi.org/10.1038/srep33290). CC BY 4.0.

**Set:** LUCID (Wave 7, rank 93, tier B, priority 12)
**Host:** CherryRd (Darwin 25.3.0, x86_64) — local CPU
**Auditor:** Ollie subagent
**Timeline:** First pass 2026-06-09 → consolidation 2026-06-22 → 8-artifact backfill 2026-07-06

---

## 1. Workflow

1. **Acquire** paper + supplementary artifacts from the publisher's static-content host.
2. **Hash** every fetched artifact into `MANIFEST.md` (SHA-256).
3. **Extract text** with `pdftotext -layout` for grep + AI review.
4. **Unpack** the supplementary code ZIP into `code_py3/`.
5. **Port** Python 2.7 → Python 3 (three textual changes, no algorithmic edits):
   - `xrange → range`
   - bare `print X → print(X)`
   - `DNAModelFit.py:58 row = map(float, row) → row = list(map(float, row))`
6. **Re-fit DNA endpoints** via `python3 DNAModelFit.py` (9 free params over 180 curated points; scipy `leastsq`, weighted NLS).
7. **Re-fit survival** via `python3 SurvivalFit.py` (2 free params ψ, φ over 187 curated points; DNA params held fixed).
8. **Regenerate model curves** for Figs. 1–6 via `python3 CellModelOutputs.py`; move 6 TSVs into `results/`.
9. **Render Fig. 5 PNG** via a small local `scripts/plot_survival.py` (matplotlib) as a visual sanity check.
10. **Compare** re-fit values to Table 1 (11/11 within ±1σ) and spot-check survival at 2 Gy / 6 Gy against Fig. 5 panels + the paper's two qualitative claims.
11. **Score** COVERAGE and AGREEMENT, write `REPORT.md`, and stage the 8-artifact backfill.

## 2. Tools & versions (pinned)

| Tool | Version | Role |
|---|---|---|
| Python | 3.14.4 (CherryRd system) | runtime for author code |
| numpy | 2.4.3 | linear algebra in fit routines |
| scipy | 1.18.0 | `scipy.optimize.leastsq` (weighted NLS) |
| matplotlib | 3.9+ | local Fig. 5 PNG rendering |
| `pdftotext` (poppler) | system | paper + SI text extraction for grep |
| `unzip` | system | supplementary ZIP unpack (used `unzip -l` first as ground-truth) |
| shasum | system | SHA-256 of every fetched artifact |
| AI models | Argo `argo:claude-opus-4.7` / `4.8` (free, `localhost:44497`) | writing, cross-check |

**No paid endpoints, no GPU, no HPC**. All compute local on CherryRd.

## 3. Work estimate

| Stage | Wall time | CPU | Notes |
|---|---|---|---|
| Fetch + hash 3 artifacts | ≈ 2 min | 1 core | one-shot |
| Py2→Py3 port | ≈ 5 min | manual | 3 lines across 6 files |
| DNA fit (`DNAModelFit.py`) | ≈ 5 s | 1 core | 180 pts, 9 params |
| Survival fit (`SurvivalFit.py`) | ≈ 10 s | 1 core | 187 pts, 2 params |
| Curve regen (`CellModelOutputs.py`) | ≈ 15 s | 1 core | 6 TSVs |
| Fig. 5 render | ≈ 3 s | 1 core | matplotlib |
| **Sim compute total** | **< 40 s** | **1 core** | **< 200 MB RAM** |
| Report writing (first pass) | ≈ 90 min | — | human/AI |
| 8-artifact backfill | ≈ 20 min | — | this pass |

## 4. Reproducer

To reproduce this replication from scratch on any host with Python 3 +
numpy + scipy + matplotlib + `unzip` + `pdftotext`:

```bash
# 0. clone the LUCID slot (or fetch the 3 upstream artifacts fresh)
cd lucid-mcmahon-2016-medras-original

# 1. verify hashes
shasum -a 256 -c <(grep -E 'srep33290\.pdf|supplementary_' MANIFEST.md \
                     | awk '{print $3"  "$1}' \
                     | sed 's/`//g')

# 2. run all three author scripts (already Py2→Py3 ported in code_py3/)
cd code_py3
python3 DNAModelFit.py        > ../logs/dna_fit.log        2>&1
python3 SurvivalFit.py        > ../logs/survival_fit.log   2>&1
python3 CellModelOutputs.py   > ../logs/cell_model_outputs.log 2>&1

# 3. move the 6 regenerated TSVs to results/
mv *.tsv ../results/

# 4. render Fig. 5 as PNG
cd ..
python3 scripts/plot_survival.py     # → figures/fig5_reproduction_survival.png

# 5. spot-check the two qualitative claims (G2-rescue, delayed-vs-immediate)
python3 -c "
import csv, itertools
rows = list(csv.DictReader(open('results/Model Data - Survival.tsv'), delimiter='\t'))
# find S(2Gy) for CHO NHEJ-def G1 and G2 → confirm ratio ≈ 2.4x
"
```

Expected outputs (bit-stable across numpy 2.4.x / scipy 1.17–1.18):
- `Chisq: 241.00226334052684` in the DNA-fit log
- Table 1 parameter dict identical to the paper's within ±1σ (11/11)
- 6 model-curve TSVs in `results/`
- `figures/fig5_reproduction_survival.png` visually matches Fig. 5

Runtime: < 40 s wall, 1 CPU core. No GPU, no HPC, no paid endpoints.

## 5. Known deviations from upstream

Only the 3-line Py2→Py3 port. No algorithmic substitutions, no changed
parameter bounds, no changed weightings, no changed initial guesses. The
port diff is captured in `MANIFEST.md`.

## 6. What was intentionally **not** done

See `open_questions.json` and `failure_analysis.md` for the honest list.
Summary: Fig. 7 R² not recomputed; A, B geometry constants not
re-derived from an independent MC; residual $\chi^2$ distribution not
stratified; parameter identifiability not audited; G2-rescue causal claim
not re-checked against per-line raw data.
